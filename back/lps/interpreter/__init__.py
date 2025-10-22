"""
Interpretador da linha de produto de compiladores.

Este módulo contém implementações de interpretadores que podem
executar AST diretamente ou via código IR.
"""

from .ast_interpreter import MiniparASTInterpreter
from .ir_interpreter import MiniparIRInterpreter

__all__ = [
    'MiniparASTInterpreter',
    'MiniparIRInterpreter'
]
