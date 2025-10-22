"""
Interface para Tabela de Símbolos.

Define o contrato para gerenciamento de símbolos (variáveis, funções, tipos)
que é compartilhado entre o analisador semântico e os backends.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass


class SymbolType(Enum):
    """Tipos de símbolos."""
    VARIABLE = "VARIABLE"
    FUNCTION = "FUNCTION"
    TYPE = "TYPE"
    CONSTANT = "CONSTANT"
    LABEL = "LABEL"
    TEMPORARY = "TEMPORARY"


class DataType(Enum):
    """Tipos de dados."""
    INT = "INT"
    BOOL = "BOOL"
    STRING = "STRING"
    VOID = "VOID"
    ARRAY = "ARRAY"
    STRUCT = "STRUCT"
    POINTER = "POINTER"


@dataclass
class Symbol:
    """Representação de um símbolo na tabela."""
    name: str
    symbol_type: SymbolType
    data_type: DataType
    scope: str
    location: Optional[int] = None  # endereço/offset de pilha
    size: Optional[int] = None  # tamanho em bytes
    is_initialized: bool = False
    is_constant: bool = False
    value: Optional[Any] = None
    parameters: Optional[List['Symbol']] = None  # para funções
    return_type: Optional[DataType] = None  # para funções
    meta: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        """Representação string do símbolo."""
        return f"{self.name}: {self.data_type.value} ({self.symbol_type.value})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "name": self.name,
            "symbol_type": self.symbol_type.value,
            "data_type": self.data_type.value,
            "scope": self.scope,
            "location": self.location,
            "size": self.size,
            "is_initialized": self.is_initialized,
            "is_constant": self.is_constant,
            "value": self.value,
            "parameters": [p.to_dict() for p in (self.parameters or [])],
            "return_type": self.return_type.value if self.return_type else None,
            "meta": self.meta or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Symbol':
        """Cria a partir de dicionário."""
        return cls(
            name=data["name"],
            symbol_type=SymbolType(data["symbol_type"]),
            data_type=DataType(data["data_type"]),
            scope=data["scope"],
            location=data.get("location"),
            size=data.get("size"),
            is_initialized=data.get("is_initialized", False),
            is_constant=data.get("is_constant", False),
            value=data.get("value"),
            parameters=[Symbol.from_dict(p) for p in (data.get("parameters") or [])],
            return_type=DataType(data["return_type"]) if data.get("return_type") else None,
            meta=data.get("meta")
        )


class SymbolTable(ABC):
    """Interface para tabela de símbolos."""
    
    @abstractmethod
    def enter_scope(self, scope_name: str) -> None:
        """Entra em um novo escopo."""
        pass
    
    @abstractmethod
    def exit_scope(self) -> None:
        """Sai do escopo atual."""
        pass
    
    @abstractmethod
    def declare_symbol(self, symbol: Symbol) -> None:
        """Declara um novo símbolo."""
        pass
    
    @abstractmethod
    def lookup_symbol(self, name: str, scope: Optional[str] = None) -> Optional[Symbol]:
        """Busca um símbolo por nome."""
        pass
    
    @abstractmethod
    def update_symbol(self, symbol: Symbol) -> None:
        """Atualiza um símbolo existente."""
        pass
    
    @abstractmethod
    def get_symbols_in_scope(self, scope: str) -> List[Symbol]:
        """Retorna todos os símbolos de um escopo."""
        pass
    
    @abstractmethod
    def get_current_scope(self) -> str:
        """Retorna o escopo atual."""
        pass
    
    @abstractmethod
    def allocate_memory(self, symbol: Symbol) -> int:
        """Aloca memória para um símbolo."""
        pass
    
    @abstractmethod
    def get_memory_layout(self) -> Dict[str, List[Symbol]]:
        """Retorna o layout de memória por escopo."""
        pass


class ScopeManager(ABC):
    """Interface para gerenciamento de escopos."""
    
    @abstractmethod
    def create_scope(self, name: str, parent: Optional[str] = None) -> str:
        """Cria um novo escopo."""
        pass
    
    @abstractmethod
    def get_scope_hierarchy(self, scope: str) -> List[str]:
        """Retorna a hierarquia de escopos."""
        pass
    
    @abstractmethod
    def is_scope_accessible(self, from_scope: str, to_scope: str) -> bool:
        """Verifica se um escopo é acessível de outro."""
        pass


class TypeChecker(ABC):
    """Interface para verificação de tipos."""
    
    @abstractmethod
    def check_type_compatibility(self, type1: DataType, type2: DataType) -> bool:
        """Verifica compatibilidade entre tipos."""
        pass
    
    @abstractmethod
    def get_common_type(self, type1: DataType, type2: DataType) -> Optional[DataType]:
        """Retorna o tipo comum entre dois tipos."""
        pass
    
    @abstractmethod
    def is_assignable(self, target_type: DataType, source_type: DataType) -> bool:
        """Verifica se um tipo pode ser atribuído a outro."""
        pass


class SymbolTableSerializer(ABC):
    """Interface para serialização da tabela de símbolos."""
    
    @abstractmethod
    def serialize(self, symbol_table: SymbolTable) -> str:
        """Serializa tabela de símbolos para string."""
        pass
    
    @abstractmethod
    def deserialize(self, data: str) -> SymbolTable:
        """Deserializa string para tabela de símbolos."""
        pass


class JSONSymbolTableSerializer(SymbolTableSerializer):
    """Implementação de serialização JSON para tabela de símbolos."""
    
    def serialize(self, symbol_table: SymbolTable) -> str:
        """Serializa tabela de símbolos para JSON."""
        import json
        # Implementação básica - pode ser expandida
        return json.dumps({})
    
    def deserialize(self, data: str) -> SymbolTable:
        """Deserializa JSON para tabela de símbolos."""
        import json
        # Implementação básica - pode ser expandida
        return None
