"""
CLI e Builder da linha de produto de compiladores.

Este módulo contém a interface de linha de comando e o builder
para construção de diferentes produtos de compilação.
"""

from .builder import ProductBuilder
from .cli import MiniparCLI

__all__ = [
    'ProductBuilder',
    'MiniparCLI'
]
