"""
Sistema de configuração de produtos da linha de produto de compiladores.

Este módulo permite definir diferentes produtos de compilação
através de arquivos de configuração YAML/JSON.
"""

from .product_config import ProductConfig, ProductType, BackendType
from .config_loader import ConfigLoader, YAMLConfigLoader, JSONConfigLoader

__all__ = [
    'ProductConfig',
    'ProductType',
    'BackendType',
    'ConfigLoader',
    'YAMLConfigLoader',
    'JSONConfigLoader'
]
