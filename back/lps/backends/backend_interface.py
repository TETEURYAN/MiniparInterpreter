"""
Interface para backends de geração de Assembly.

Define o contrato para backends que convertem código IR
em Assembly para diferentes arquiteturas.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from interfaces.ir import IRInstruction, IROperation
from interfaces.symbol_table import SymbolTable


class AssemblyEmitter(ABC):
    """Interface para emissores de Assembly."""
    
    @abstractmethod
    def emit_header(self) -> str:
        """Emite cabeçalho do arquivo Assembly."""
        pass
    
    @abstractmethod
    def emit_footer(self) -> str:
        """Emite rodapé do arquivo Assembly."""
        pass
    
    @abstractmethod
    def emit_instruction(self, instruction: IRInstruction) -> str:
        """Emite uma instrução IR como Assembly."""
        pass
    
    @abstractmethod
    def emit_label(self, label: str) -> str:
        """Emite um rótulo."""
        pass
    
    @abstractmethod
    def emit_comment(self, comment: str) -> str:
        """Emite um comentário."""
        pass
    
    @abstractmethod
    def emit_data_section(self, symbol_table: SymbolTable) -> str:
        """Emite seção de dados."""
        pass
    
    @abstractmethod
    def emit_text_section(self) -> str:
        """Emite seção de código."""
        pass


class Backend(ABC):
    """Interface para backends de compilação."""
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.emitter: Optional[AssemblyEmitter] = None
    
    @abstractmethod
    def generate_assembly(self, instructions: List[IRInstruction]) -> str:
        """Gera código Assembly a partir das instruções IR."""
        pass
    
    @abstractmethod
    def get_target_architecture(self) -> str:
        """Retorna a arquitetura de destino."""
        pass
    
    @abstractmethod
    def get_register_allocator(self) -> 'RegisterAllocator':
        """Retorna o alocador de registradores."""
        pass
    
    @abstractmethod
    def get_memory_manager(self) -> 'MemoryManager':
        """Retorna o gerenciador de memória."""
        pass


class RegisterAllocator(ABC):
    """Interface para alocadores de registradores."""
    
    @abstractmethod
    def allocate_register(self, variable: str) -> str:
        """Aloca um registrador para uma variável."""
        pass
    
    @abstractmethod
    def free_register(self, register: str) -> None:
        """Libera um registrador."""
        pass
    
    @abstractmethod
    def get_available_registers(self) -> List[str]:
        """Retorna lista de registradores disponíveis."""
        pass
    
    @abstractmethod
    def spill_register(self, register: str, variable: str) -> str:
        """Despeja um registrador para memória."""
        pass


class MemoryManager(ABC):
    """Interface para gerenciadores de memória."""
    
    @abstractmethod
    def allocate_stack_space(self, size: int) -> int:
        """Aloca espaço na pilha."""
        pass
    
    @abstractmethod
    def get_variable_offset(self, variable: str) -> int:
        """Retorna o offset de uma variável na pilha."""
        pass
    
    @abstractmethod
    def get_stack_pointer(self) -> str:
        """Retorna o registrador do ponteiro de pilha."""
        pass
    
    @abstractmethod
    def get_frame_pointer(self) -> str:
        """Retorna o registrador do ponteiro de frame."""
        pass


class SimpleRegisterAllocator(RegisterAllocator):
    """Implementação simples de alocador de registradores."""
    
    def __init__(self, available_registers: List[str]):
        self.available_registers = available_registers.copy()
        self.allocated_registers: Dict[str, str] = {}
        self.register_usage: Dict[str, str] = {}
    
    def allocate_register(self, variable: str) -> str:
        """Aloca um registrador para uma variável."""
        if variable in self.allocated_registers:
            return self.allocated_registers[variable]
        
        if self.available_registers:
            register = self.available_registers.pop(0)
            self.allocated_registers[variable] = register
            self.register_usage[register] = variable
            return register
        else:
            # Spill strategy: use first allocated register
            register = list(self.register_usage.keys())[0]
            self.spill_register(register, self.register_usage[register])
            self.allocated_registers[variable] = register
            self.register_usage[register] = variable
            return register
    
    def free_register(self, register: str) -> None:
        """Libera um registrador."""
        if register in self.register_usage:
            variable = self.register_usage[register]
            del self.allocated_registers[variable]
            del self.register_usage[register]
            self.available_registers.append(register)
    
    def get_available_registers(self) -> List[str]:
        """Retorna lista de registradores disponíveis."""
        return self.available_registers.copy()
    
    def spill_register(self, register: str, variable: str) -> str:
        """Despeja um registrador para memória."""
        # Implementação básica - retorna instrução de store
        return f"store {register}, {variable}"


class SimpleMemoryManager(MemoryManager):
    """Implementação simples de gerenciador de memória."""
    
    def __init__(self, stack_pointer: str = "rsp", frame_pointer: str = "rbp"):
        self.stack_pointer = stack_pointer
        self.frame_pointer = frame_pointer
        self.variable_offsets: Dict[str, int] = {}
        self.current_offset = 0
    
    def allocate_stack_space(self, size: int) -> int:
        """Aloca espaço na pilha."""
        offset = self.current_offset
        self.current_offset += size
        return offset
    
    def get_variable_offset(self, variable: str) -> int:
        """Retorna o offset de uma variável na pilha."""
        if variable not in self.variable_offsets:
            self.variable_offsets[variable] = self.allocate_stack_space(8)  # 8 bytes por variável
        return self.variable_offsets[variable]
    
    def get_stack_pointer(self) -> str:
        """Retorna o registrador do ponteiro de pilha."""
        return self.stack_pointer
    
    def get_frame_pointer(self) -> str:
        """Retorna o registrador do ponteiro de frame."""
        return self.frame_pointer
