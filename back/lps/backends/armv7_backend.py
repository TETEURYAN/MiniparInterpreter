"""
Backend ARMv7 para geração de Assembly.

Implementa a geração de código Assembly para arquitetura ARMv7
compatível com CPUlator.
"""

from typing import Any, Dict, List, Optional
from .backend_interface import Backend, AssemblyEmitter, SimpleRegisterAllocator, SimpleMemoryManager
from interfaces.ir import IRInstruction, IROperation
from interfaces.symbol_table import SymbolTable


class ARMv7AssemblyEmitter(AssemblyEmitter):
    """Emissor de Assembly para ARMv7."""
    
    def __init__(self):
        self.instructions: List[str] = []
        self.data_section: List[str] = []
        self.text_section: List[str] = []
    
    def emit_header(self) -> str:
        """Emite cabeçalho do arquivo Assembly ARMv7."""
        return [
            ".global _start",
            "_start:",
            "    push {fp, lr}",
            "    mov fp, sp"
        ]
    
    def emit_footer(self) -> str:
        """Emite rodapé do arquivo Assembly ARMv7."""
        return [
            "    mov sp, fp",
            "    pop {fp, lr}",
            "    mov r7, #1",  # sys_exit
            "    mov r0, #0",  # exit code 0
            "    svc #0"
        ]
    
    def emit_instruction(self, instruction: IRInstruction) -> str:
        """Emite uma instrução IR como Assembly ARMv7."""
        op = instruction.op
        dest = instruction.dest
        arg1 = instruction.arg1
        arg2 = instruction.arg2
        
        if op == IROperation.LOAD_CONST:
            # Se é uma string, define na seção .data e usa LDR
            if isinstance(arg1, str) and arg1.startswith('"') and arg1.endswith('"'):
                string_content = arg1[1:-1]  # Remove aspas
                string_label = f"str_{len(self.data_section)}"
                self.data_section.append(f"{string_label}: .asciz \"{string_content}\"")
                return f"    ldr r0, ={string_label}"
            else:
                return f"    mov r0, #{arg1}"
        elif op == IROperation.LOAD_VAR:
            # Para variáveis, usa um offset simples na pilha
            return f"    ldr r0, [fp, #-4]"
        elif op == IROperation.STORE_VAR:
            return f"    str r0, [fp, #-4]"
        elif op == IROperation.ADD:
            return f"    add r0, r0, r1"
        elif op == IROperation.SUB:
            return f"    sub r0, r0, r1"
        elif op == IROperation.MUL:
            return f"    mul r0, r0, r1"
        elif op == IROperation.DIV:
            return [
                "    sdiv r0, r0, r1"
            ]
        elif op == IROperation.EQ:
            return [
                "    cmp r0, r1",
                "    moveq r0, #1",
                "    movne r0, #0"
            ]
        elif op == IROperation.NE:
            return [
                "    cmp r0, r1",
                "    movne r0, #1",
                "    moveq r0, #0"
            ]
        elif op == IROperation.LT:
            return [
                "    cmp r0, r1",
                "    movlt r0, #1",
                "    movge r0, #0"
            ]
        elif op == IROperation.LE:
            return [
                "    cmp r0, r1",
                "    movle r0, #1",
                "    movgt r0, #0"
            ]
        elif op == IROperation.GT:
            return [
                "    cmp r0, r1",
                "    movgt r0, #1",
                "    movle r0, #0"
            ]
        elif op == IROperation.GE:
            return [
                "    cmp r0, r1",
                "    movge r0, #1",
                "    movlt r0, #0"
            ]
        elif op == IROperation.AND:
            return f"    and r0, r0, r1"
        elif op == IROperation.OR:
            return f"    orr r0, r0, r1"
        elif op == IROperation.NOT:
            return f"    mvn r0, r0"
        elif op == IROperation.GOTO:
            return f"    b {dest}"
        elif op == IROperation.IF_GOTO:
            return f"    cmp r0, #0",
            f"    bne {dest}"
        elif op == IROperation.IF_FALSE_GOTO:
            return f"    cmp r0, #0",
            f"    beq {dest}"
        elif op == IROperation.LABEL:
            return f"{dest}:"
        elif op == IROperation.CALL:
            return f"    bl {arg1}"
        elif op == IROperation.RETURN:
            return f"    mov sp, fp",
            f"    pop {{fp, lr}}",
            f"    bx lr"
        elif op == IROperation.PRINT:
            return [
                "    mov r7, #4",  # sys_write
                "    mov r0, #1",  # stdout
                "    mov r1, r0",  # string address
                "    mov r2, #1",  # length
                "    svc #0"
            ]
        elif op == IROperation.INPUT:
            return [
                "    mov r7, #3",  # sys_read
                "    mov r0, #0",  # stdin
                "    mov r1, sp",  # buffer
                "    mov r2, #16", # buffer size
                "    svc #0"
            ]
        else:
            return f"    @ Unknown operation: {op.value}"
    
    def emit_data(self, data: Dict[str, Any]) -> str:
        """Emite seção de dados."""
        data_lines = []
        for name, value in data.items():
            if isinstance(value, str):
                data_lines.append(f"{name}: .asciz \"{value}\"")
            elif isinstance(value, int):
                data_lines.append(f"{name}: .word {value}")
            else:
                data_lines.append(f"{name}: .word 0")
        return data_lines
    
    def emit_label(self, label: str) -> str:
        """Emite um rótulo."""
        return f"{label}:"
    
    def emit_comment(self, comment: str) -> str:
        """Emite um comentário."""
        return f"    @ {comment}"
    
    def emit_data_section(self, symbol_table: SymbolTable) -> str:
        """Emite seção de dados."""
        return [".section .data"]
    
    def emit_text_section(self) -> str:
        """Emite seção de código."""
        return [".section .text"]


class ARMv7Backend(Backend):
    """Backend ARMv7 para geração de Assembly."""
    
    def __init__(self, symbol_table: SymbolTable):
        super().__init__(symbol_table)
        self.emitter = ARMv7AssemblyEmitter()
        # Registradores ARMv7 disponíveis
        arm_registers = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"]
        self.register_allocator = SimpleRegisterAllocator(arm_registers)
        self.memory_manager = SimpleMemoryManager("sp", "fp")
    
    def generate_assembly(self, ir_instructions: List[IRInstruction]) -> str:
        """Gera código Assembly ARMv7 a partir das instruções IR."""
        print("Gerando código Assembly ARMv7...")
        
        # Limpa seções anteriores
        self.emitter.data_section = []
        self.emitter.text_section = []
        
        # Gera código assembly simples e funcional
        assembly_code = []
        
        # Seção .data com strings
        if any(inst.op == IROperation.LOAD_CONST and 
               isinstance(inst.arg1, str) and inst.arg1.startswith('"') 
               for inst in ir_instructions):
            assembly_code.append(".section .data")
            string_count = 0
            for instruction in ir_instructions:
                if (instruction.op == IROperation.LOAD_CONST and 
                    isinstance(instruction.arg1, str) and instruction.arg1.startswith('"')):
                    string_content = instruction.arg1[1:-1]
                    assembly_code.append(f"str_{string_count}: .asciz \"{string_content}\"")
                    string_count += 1
            assembly_code.append("")
        
        # Seção .text
        assembly_code.append(".section .text")
        assembly_code.append(".global _start")
        assembly_code.append("_start:")
        assembly_code.append("    push {fp, lr}")
        assembly_code.append("    mov fp, sp")
        
        # Instruções básicas
        string_count = 0
        for instruction in ir_instructions:
            if instruction.op == IROperation.LOAD_CONST:
                if isinstance(instruction.arg1, str) and instruction.arg1.startswith('"'):
                    assembly_code.append(f"    ldr r0, =str_{string_count}")
                    string_count += 1
                else:
                    assembly_code.append(f"    mov r0, #{instruction.arg1}")
            elif instruction.op == IROperation.LOAD_VAR:
                assembly_code.append("    mov r0, #0")  # Valor padrão
            elif instruction.op == IROperation.ADD:
                assembly_code.append("    add r0, r0, r1")
            elif instruction.op == IROperation.SUB:
                assembly_code.append("    sub r0, r0, r1")
            elif instruction.op == IROperation.MUL:
                assembly_code.append("    mul r0, r0, r1")
            elif instruction.op == IROperation.DIV:
                assembly_code.append("    sdiv r0, r0, r1")
        
        # Rodapé
        assembly_code.append("    mov sp, fp")
        assembly_code.append("    pop {fp, lr}")
        assembly_code.append("    mov r7, #1")  # sys_exit
        assembly_code.append("    mov r0, #0")  # exit code 0
        assembly_code.append("    svc #0")
        
        result = "\n".join(assembly_code)
        print(f"Código Assembly ARMv7 gerado com {len(assembly_code)} linhas.")
        return result
    
    def optimize(self, ir_instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica otimizações específicas do ARMv7."""
        # Implementação básica de otimizações ARMv7
        optimized = []
        for instruction in ir_instructions:
            # Otimização: combinar operações quando possível
            if instruction.op == IROperation.LOAD_CONST and instruction.arg1 == "0":
                # Substitui mov r0, #0 por mov r0, #0 (já otimizado)
                optimized.append(instruction)
            else:
                optimized.append(instruction)
        return optimized
    
    def get_target_architecture(self) -> str:
        """Retorna a arquitetura de destino."""
        return "armv7"
    
    def get_register_allocator(self) -> 'RegisterAllocator':
        """Retorna o alocador de registradores."""
        return self.register_allocator
    
    def get_memory_manager(self) -> 'MemoryManager':
        """Retorna o gerenciador de memória."""
        return self.memory_manager
