"""
Backend x86_64 para geração de Assembly.

Implementa a geração de código Assembly para arquitetura x86_64
seguindo o algoritmo disponibilizado no Classroom.
"""

from typing import Any, Dict, List, Optional
from .backend_interface import Backend, AssemblyEmitter, SimpleRegisterAllocator, SimpleMemoryManager
from interfaces.ir import IRInstruction, IROperation
from interfaces.symbol_table import SymbolTable


class X86_64AssemblyEmitter(AssemblyEmitter):
    """Emissor de Assembly para x86_64."""
    
    def __init__(self):
        self.instructions: List[str] = []
        self.data_section: List[str] = []
        self.text_section: List[str] = []
    
    def emit_header(self) -> str:
        """Emite cabeçalho do arquivo Assembly."""
        return [
            ".section .data",
            ".section .text",
            ".global _start",
            "_start:",
            "    push %rbp",
            "    mov %rsp, %rbp"
        ]
    
    def emit_footer(self) -> str:
        """Emite rodapé do arquivo Assembly."""
        return [
            "    mov %rbp, %rsp",
            "    pop %rbp",
            "    mov $60, %rax",  # sys_exit
            "    xor %rdi, %rdi",  # exit code 0
            "    syscall"
        ]
    
    def emit_instruction(self, instruction: IRInstruction) -> str:
        """Emite uma instrução IR como Assembly x86_64."""
        op = instruction.op
        dest = instruction.dest
        arg1 = instruction.arg1
        arg2 = instruction.arg2
        
        if op == IROperation.LOAD_CONST:
            return f"    mov ${arg1}, %rax"
        elif op == IROperation.LOAD_VAR:
            return f"    mov {arg1}(%rbp), %rax"
        elif op == IROperation.STORE_VAR:
            return f"    mov %rax, {dest}(%rbp)"
        elif op == IROperation.ADD:
            return f"    add %rbx, %rax"
        elif op == IROperation.SUB:
            return f"    sub %rbx, %rax"
        elif op == IROperation.MUL:
            return f"    imul %rbx, %rax"
        elif op == IROperation.DIV:
            return [
                "    cqo",  # sign extend rax to rdx:rax
                "    idiv %rbx"
            ]
        elif op == IROperation.EQ:
            return [
                "    cmp %rbx, %rax",
                "    sete %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.NE:
            return [
                "    cmp %rbx, %rax",
                "    setne %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.LT:
            return [
                "    cmp %rbx, %rax",
                "    setl %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.LE:
            return [
                "    cmp %rbx, %rax",
                "    setle %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.GT:
            return [
                "    cmp %rbx, %rax",
                "    setg %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.GE:
            return [
                "    cmp %rbx, %rax",
                "    setge %al",
                "    movzb %al, %rax"
            ]
        elif op == IROperation.AND:
            return "    and %rbx, %rax"
        elif op == IROperation.OR:
            return "    or %rbx, %rax"
        elif op == IROperation.NOT:
            return "    not %rax"
        elif op == IROperation.GOTO:
            return f"    jmp {arg1}"
        elif op == IROperation.IF_GOTO:
            return f"    jnz {arg2}"
        elif op == IROperation.IF_FALSE_GOTO:
            return f"    jz {arg2}"
        elif op == IROperation.LABEL:
            return f"{instruction.label}:"
        elif op == IROperation.PRINT:
            return [
                "    mov %rax, %rdi",
                "    call print_int"
            ]
        elif op == IROperation.INPUT:
            return [
                "    call read_int",
                f"    mov %rax, {dest}(%rbp)"
            ]
        else:
            return f"    # {instruction}"
    
    def emit_label(self, label: str) -> str:
        """Emite um rótulo."""
        return f"{label}:"
    
    def emit_comment(self, comment: str) -> str:
        """Emite um comentário."""
        return f"    # {comment}"
    
    def emit_data_section(self, symbol_table: SymbolTable) -> str:
        """Emite seção de dados."""
        lines = [".section .data"]
        
        # Adiciona variáveis globais
        for symbol in symbol_table.get_symbols_in_scope("global"):
            if symbol.symbol_type.value == "VARIABLE":
                lines.append(f"{symbol.name}: .quad 0")
        
        return lines
    
    def emit_text_section(self) -> str:
        """Emite seção de código."""
        return [".section .text"]
    
    def emit_print_function(self) -> str:
        """Emite função de impressão."""
        return [
            "print_int:",
            "    push %rbp",
            "    mov %rsp, %rbp",
            "    push %rdi",
            "    mov $1, %rax",  # sys_write
            "    mov $1, %rdi",  # stdout
            "    mov %rsp, %rsi",  # buffer
            "    mov $1, %rdx",  # count
            "    syscall",
            "    pop %rdi",
            "    mov %rbp, %rsp",
            "    pop %rbp",
            "    ret"
        ]
    
    def emit_input_function(self) -> str:
        """Emite função de entrada."""
        return [
            "read_int:",
            "    push %rbp",
            "    mov %rsp, %rbp",
            "    sub $16, %rsp",  # allocate space for input
            "    mov $0, %rax",  # sys_read
            "    mov $0, %rdi",  # stdin
            "    mov %rsp, %rsi",  # buffer
            "    mov $16, %rdx",  # count
            "    syscall",
            "    mov %rsp, %rdi",
            "    call atoi",  # convert string to int
            "    mov %rbp, %rsp",
            "    pop %rbp",
            "    ret"
        ]
    
    def emit_atoi_function(self) -> str:
        """Emite função atoi (string to int)."""
        return [
            "atoi:",
            "    push %rbp",
            "    mov %rsp, %rbp",
            "    mov %rdi, %rsi",  # string pointer
            "    xor %rax, %rax",  # result
            "    xor %rcx, %rcx",  # counter
            "atoi_loop:",
            "    movb (%rsi, %rcx), %dl",
            "    test %dl, %dl",
            "    jz atoi_done",
            "    sub $48, %dl",  # convert ASCII to digit
            "    imul $10, %rax",
            "    add %rdx, %rax",
            "    inc %rcx",
            "    jmp atoi_loop",
            "atoi_done:",
            "    mov %rbp, %rsp",
            "    pop %rbp",
            "    ret"
        ]


class X86_64Backend(Backend):
    """Backend x86_64 para compilação."""
    
    def __init__(self, symbol_table: SymbolTable):
        super().__init__(symbol_table)
        self.emitter = X86_64AssemblyEmitter()
        self.register_allocator = SimpleRegisterAllocator([
            "%rax", "%rbx", "%rcx", "%rdx", "%rsi", "%rdi", "%r8", "%r9", "%r10", "%r11"
        ])
        self.memory_manager = SimpleMemoryManager()
    
    def generate_assembly(self, instructions: List[IRInstruction]) -> str:
        """Gera código Assembly x86_64 a partir das instruções IR."""
        assembly_lines = []
        
        # Emite cabeçalho
        assembly_lines.extend(self.emitter.emit_header())
        
        # Emite seção de dados
        assembly_lines.extend(self.emitter.emit_data_section(self.symbol_table))
        
        # Emite seção de código
        assembly_lines.extend(self.emitter.emit_text_section())
        
        # Emite instruções principais
        for instruction in instructions:
            if instruction.op == IROperation.LABEL:
                assembly_lines.append(self.emitter.emit_label(instruction.label))
            else:
                result = self.emitter.emit_instruction(instruction)
                if isinstance(result, list):
                    assembly_lines.extend(result)
                else:
                    assembly_lines.append(result)
        
        # Emite funções auxiliares
        assembly_lines.extend(self.emitter.emit_print_function())
        assembly_lines.extend(self.emitter.emit_input_function())
        assembly_lines.extend(self.emitter.emit_atoi_function())
        
        # Emite rodapé
        assembly_lines.extend(self.emitter.emit_footer())
        
        return "\n".join(assembly_lines)
    
    def get_target_architecture(self) -> str:
        """Retorna a arquitetura de destino."""
        return "x86_64"
    
    def get_register_allocator(self) -> SimpleRegisterAllocator:
        """Retorna o alocador de registradores."""
        return self.register_allocator
    
    def get_memory_manager(self) -> SimpleMemoryManager:
        """Retorna o gerenciador de memória."""
        return self.memory_manager
