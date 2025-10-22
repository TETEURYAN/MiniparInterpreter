"""
Carregadores de configuração para a linha de produto de compiladores.

Este módulo implementa carregadores para diferentes formatos
de configuração (YAML, JSON).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path
import yaml
import json

from product_config.product_config import ProductConfig


class ConfigLoader(ABC):
    """Interface para carregadores de configuração."""
    
    @abstractmethod
    def load_config(self, config_path: str) -> ProductConfig:
        """Carrega configuração de arquivo."""
        pass
    
    @abstractmethod
    def save_config(self, config: ProductConfig, output_path: str) -> None:
        """Salva configuração em arquivo."""
        pass


class YAMLConfigLoader(ConfigLoader):
    """Carregador de configuração YAML."""
    
    def load_config(self, config_path: str) -> ProductConfig:
        """Carrega configuração YAML."""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return ProductConfig.from_dict(data)
    
    def save_config(self, config: ProductConfig, output_path: str) -> None:
        """Salva configuração YAML."""
        data = config.to_dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)


class JSONConfigLoader(ConfigLoader):
    """Carregador de configuração JSON."""
    
    def load_config(self, config_path: str) -> ProductConfig:
        """Carrega configuração JSON."""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return ProductConfig.from_dict(data)
    
    def save_config(self, config: ProductConfig, output_path: str) -> None:
        """Salva configuração JSON."""
        data = config.to_dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
