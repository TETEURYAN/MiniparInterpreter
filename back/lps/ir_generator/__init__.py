"""
Gerador de código intermediário (IR) - Código de 3 endereços.

Este módulo contém a implementação do gerador de código intermediário
que converte AST em instruções de 3 endereços.
"""

from .ir_generator_impl import MiniparIRGenerator
from .ir_optimizer_impl import MiniparIROptimizer

__all__ = [
    'MiniparIRGenerator',
    'MiniparIROptimizer'
]
