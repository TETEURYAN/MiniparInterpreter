"""
Implementação do otimizador de IR para Minipar.

Este módulo contém a implementação do otimizador de código intermediário
que aplica várias técnicas de otimização no código IR.
"""

from typing import List
from interfaces.ir import IROptimizer, IRInstruction, IROperation


class MiniparIROptimizer(IROptimizer):
    """Otimizador de IR para Minipar."""
    
    def __init__(self):
        self.constant_folding_optimizer = ConstantFoldingOptimizer()
        self.peephole_optimizer = PeepholeOptimizer()
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica todas as otimizações disponíveis."""
        optimized = instructions.copy()
        
        # Aplica dobramento de constantes
        optimized = self.constant_folding_optimizer.optimize(optimized)
        
        # Aplica otimização de janela deslizante
        optimized = self.peephole_optimizer.optimize(optimized)
        
        return optimized
    
    def optimize_constant_folding(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica apenas dobramento de constantes."""
        return self.constant_folding_optimizer.optimize(instructions)
    
    def optimize_peephole(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica apenas otimização de janela deslizante."""
        return self.peephole_optimizer.optimize(instructions)


class ConstantFoldingOptimizer(IROptimizer):
    """Otimizador de dobramento de constantes."""
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica dobramento de constantes."""
        optimized = []
        
        for instruction in instructions:
            # Verifica se é uma operação aritmética com constantes
            if (instruction.op in [IROperation.ADD, IROperation.SUB, 
                                        IROperation.MUL, IROperation.DIV] and
                self._is_constant(instruction.arg1) and 
                self._is_constant(instruction.arg2)):
                
                # Calcula o resultado da operação
                result = self._evaluate_operation(
                    instruction.op,
                    instruction.arg1,
                    instruction.arg2
                )
                
                # Substitui por uma instrução de atribuição com o resultado
                from interfaces.ir import IRInstruction
                optimized.append(IRInstruction(
                    op=IROperation.LOAD_CONST,
                    dest=instruction.dest,
                    arg1=str(result),
                    arg2=None
                ))
            else:
                optimized.append(instruction)
        
        return optimized
    
    def _is_constant(self, operand: str) -> bool:
        """Verifica se um operando é uma constante numérica."""
        if not operand:
            return False
        try:
            float(operand)
            return True
        except ValueError:
            return False
    
    def _evaluate_operation(self, operation: IROperation, op1: str, op2: str) -> float:
        """Avalia uma operação aritmética."""
        val1 = float(op1)
        val2 = float(op2)
        
        if operation == IROperation.ADD:
            return val1 + val2
        elif operation == IROperation.SUB:
            return val1 - val2
        elif operation == IROperation.MUL:
            return val1 * val2
        elif operation == IROperation.DIV:
            return val1 / val2 if val2 != 0 else 0
        else:
            return 0


class PeepholeOptimizer(IROptimizer):
    """Otimizador de janela deslizante."""
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica otimizações de janela deslizante."""
        optimized = []
        i = 0
        
        while i < len(instructions):
            current = instructions[i]
            
            # Otimização: eliminação de instruções redundantes
            if (i + 1 < len(instructions) and
                current.op == IROperation.LOAD_CONST and
                instructions[i + 1].op == IROperation.LOAD_CONST and
                current.dest == instructions[i + 1].arg1):
                # Remove instrução redundante
                i += 1
                continue
            
            # Otimização: eliminação de operações com zero
            if (current.op == IROperation.ADD and current.arg2 == "0"):
                # t1 = x + 0 -> t1 = x
                from interfaces.ir import IRInstruction
                optimized.append(IRInstruction(
                    op=IROperation.LOAD_VAR,
                    dest=current.dest,
                    arg1=current.arg1,
                    arg2=None
                ))
            elif (current.op == IROperation.MUL and 
                  (current.arg1 == "0" or current.arg2 == "0")):
                # t1 = x * 0 -> t1 = 0
                from interfaces.ir import IRInstruction
                optimized.append(IRInstruction(
                    op=IROperation.LOAD_CONST,
                    dest=current.dest,
                    arg1="0",
                    arg2=None
                ))
            else:
                optimized.append(current)
            
            i += 1
        
        return optimized
