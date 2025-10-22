"""
Backends da linha de produto de compiladores.

Este módulo contém os backends para geração de Assembly
para diferentes arquiteturas de processador.
"""

from .backend_interface import Backend, AssemblyEmitter
from .x86_64_backend import X86_64Backend, X86_64AssemblyEmitter
from .riscv_backend import RISCVBackend, RISCVAssemblyEmitter
from .armv7_backend import ARMv7Backend, ARMv7AssemblyEmitter

__all__ = [
    'Backend',
    'AssemblyEmitter',
    'X86_64Backend',
    'X86_64AssemblyEmitter',
    'RISCVBackend',
    'RISCVAssemblyEmitter',
    'ARMv7Backend',
    'ARMv7AssemblyEmitter'
]
