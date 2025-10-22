"""
Backend RISC-V para geração de Assembly.

Implementa a geração de código Assembly para arquitetura RISC-V.
"""

from typing import Any, Dict, List, Optional
from .backend_interface import Backend, AssemblyEmitter, SimpleRegisterAllocator, SimpleMemoryManager
from interfaces.ir import IRInstruction, IROperation
from interfaces.symbol_table import SymbolTable


class RISCVAssemblyEmitter(AssemblyEmitter):
    """Emissor de Assembly para RISC-V."""
    
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
            "    addi sp, sp, -16",
            "    sw ra, 12(sp)",
            "    sw s0, 8(sp)",
            "    addi s0, sp, 16"
        ]
    
    def emit_footer(self) -> str:
        """Emite rodapé do arquivo Assembly."""
        return [
            "    lw ra, 12(sp)",
            "    lw s0, 8(sp)",
            "    addi sp, sp, 16",
            "    li a7, 93",  # sys_exit
            "    li a0, 0",   # exit code 0
            "    ecall"
        ]
    
    def emit_instruction(self, instruction: IRInstruction) -> str:
        """Emite uma instrução IR como Assembly RISC-V."""
        op = instruction.op
        dest = instruction.dest
        arg1 = instruction.arg1
        arg2 = instruction.arg2
        
        if op == IROperation.LOAD_CONST:
            return f"    li a0, {arg1}"
        elif op == IROperation.LOAD_VAR:
            return f"    lw a0, {arg1}(s0)"
        elif op == IROperation.STORE_VAR:
            return f"    sw a0, {dest}(s0)"
        elif op == IROperation.ADD:
            return f"    add a0, a0, a1"
        elif op == IROperation.SUB:
            return f"    sub a0, a0, a1"
        elif op == IROperation.MUL:
            return f"    mul a0, a0, a1"
        elif op == IROperation.DIV:
            return f"    div a0, a0, a1"
        elif op == IROperation.EQ:
            return [
                "    beq a0, a1, eq_true",
                "    li a0, 0",
                "    j eq_done",
                "eq_true:",
                "    li a0, 1",
                "eq_done:"
            ]
        elif op == IROperation.NE:
            return [
                "    bne a0, a1, ne_true",
                "    li a0, 0",
                "    j ne_done",
                "ne_true:",
                "    li a0, 1",
                "ne_done:"
            ]
        elif op == IROperation.LT:
            return [
                "    blt a0, a1, lt_true",
                "    li a0, 0",
                "    j lt_done",
                "lt_true:",
                "    li a0, 1",
                "lt_done:"
            ]
        elif op == IROperation.LE:
            return [
                "    ble a0, a1, le_true",
                "    li a0, 0",
                "    j le_done",
                "le_true:",
                "    li a0, 1",
                "le_done:"
            ]
        elif op == IROperation.GT:
            return [
                "    bgt a0, a1, gt_true",
                "    li a0, 0",
                "    j gt_done",
                "gt_true:",
                "    li a0, 1",
                "gt_done:"
            ]
        elif op == IROperation.GE:
            return [
                "    bge a0, a1, ge_true",
                "    li a0, 0",
                "    j ge_done",
                "ge_true:",
                "    li a0, 1",
                "ge_done:"
            ]
        elif op == IROperation.AND:
            return f"    and a0, a0, a1"
        elif op == IROperation.OR:
            return f"    or a0, a0, a1"
        elif op == IROperation.NOT:
            return f"    xori a0, a0, 1"
        elif op == IROperation.GOTO:
            return f"    j {arg1}"
        elif op == IROperation.IF_GOTO:
            return f"    bnez a0, {arg2}"
        elif op == IROperation.IF_FALSE_GOTO:
            return f"    beqz a0, {arg2}"
        elif op == IROperation.LABEL:
            return f"{instruction.label}:"
        elif op == IROperation.PRINT:
            return [
                "    mv a0, a0",
                "    call print_int"
            ]
        elif op == IROperation.INPUT:
            return [
                "    call read_int",
                f"    sw a0, {dest}(s0)"
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
                lines.append(f"{symbol.name}: .word 0")
        
        return lines
    
    def emit_text_section(self) -> str:
        """Emite seção de código."""
        return [".section .text"]
    
    def emit_print_function(self) -> str:
        """Emite função de impressão."""
        return [
            "print_int:",
            "    addi sp, sp, -16",
            "    sw ra, 12(sp)",
            "    sw s0, 8(sp)",
            "    addi s0, sp, 16",
            "    sw a0, 4(s0)",
            "    li a7, 64",  # sys_write
            "    li a0, 1",   # stdout
            "    addi a1, s0, 4",  # buffer
            "    li a2, 1",   # count
            "    ecall",
            "    lw ra, 12(sp)",
            "    lw s0, 8(sp)",
            "    addi sp, sp, 16",
            "    ret"
        ]
    
    def emit_input_function(self) -> str:
        """Emite função de entrada."""
        return [
            "read_int:",
            "    addi sp, sp, -16",
            "    sw ra, 12(sp)",
            "    sw s0, 8(sp)",
            "    addi s0, sp, 16",
            "    li a7, 63",  # sys_read
            "    li a0, 0",   # stdin
            "    addi a1, s0, -8",  # buffer
            "    li a2, 16",  # count
            "    ecall",
            "    addi a0, s0, -8",
            "    call atoi",  # convert string to int
            "    lw ra, 12(sp)",
            "    lw s0, 8(sp)",
            "    addi sp, sp, 16",
            "    ret"
        ]
    
    def emit_atoi_function(self) -> str:
        """Emite função atoi (string to int)."""
        return [
            "atoi:",
            "    addi sp, sp, -16",
            "    sw ra, 12(sp)",
            "    sw s0, 8(sp)",
            "    addi s0, sp, 16",
            "    mv s1, a0",  # string pointer
            "    li a0, 0",   # result
            "    li s2, 0",   # counter
            "atoi_loop:",
            "    add s3, s1, s2",
            "    lb s4, 0(s3)",
            "    beqz s4, atoi_done",
            "    addi s4, s4, -48",  # convert ASCII to digit
            "    li s5, 10",
            "    mul a0, a0, s5",
            "    add a0, a0, s4",
            "    addi s2, s2, 1",
            "    j atoi_loop",
            "atoi_done:",
            "    lw ra, 12(sp)",
            "    lw s0, 8(sp)",
            "    addi sp, sp, 16",
            "    ret"
        ]


class RISCVBackend(Backend):
    """Backend RISC-V para compilação."""
    
    def __init__(self, symbol_table: SymbolTable):
        super().__init__(symbol_table)
        self.emitter = RISCVAssemblyEmitter()
        self.register_allocator = SimpleRegisterAllocator([
            "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
            "t0", "t1", "t2", "t3", "t4", "t5", "t6"
        ])
        self.memory_manager = SimpleMemoryManager("sp", "s0")
    
    def generate_assembly(self, instructions: List[IRInstruction]) -> str:
        """Gera código Assembly RISC-V a partir das instruções IR."""
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
        return "riscv"
    
    def get_register_allocator(self) -> SimpleRegisterAllocator:
        """Retorna o alocador de registradores."""
        return self.register_allocator
    
    def get_memory_manager(self) -> SimpleMemoryManager:
        """Retorna o gerenciador de memória."""
        return self.memory_manager
