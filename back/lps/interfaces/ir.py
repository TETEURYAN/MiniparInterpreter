"""
Interface para Intermediate Representation (IR) - Código de 3 endereços.

Define o contrato para representação intermediária que serve como ponte
entre o frontend e os backends do compilador.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass


class IROperation(Enum):
    """Operações do código de 3 endereços."""
    # Operações aritméticas
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    
    # Operações de comparação
    EQ = "EQ"
    NE = "NE"
    LT = "LT"
    LE = "LE"
    GT = "GT"
    GE = "GE"
    
    # Operações lógicas
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Operações de memória
    LOAD_CONST = "LOAD_CONST"
    LOAD_VAR = "LOAD_VAR"
    STORE_VAR = "STORE_VAR"
    LOAD_ADDR = "LOAD_ADDR"
    STORE_ADDR = "STORE_ADDR"
    
    # Operações de controle de fluxo
    GOTO = "GOTO"
    IF_GOTO = "IF_GOTO"
    IF_FALSE_GOTO = "IF_FALSE_GOTO"
    LABEL = "LABEL"
    CALL = "CALL"
    RETURN = "RETURN"
    
    # Operações de entrada/saída
    PRINT = "PRINT"
    INPUT = "INPUT"
    
    # Operações especiais
    NOP = "NOP"
    HALT = "HALT"


@dataclass
class IRInstruction:
    """Instrução do código de 3 endereços."""
    op: IROperation
    dest: Optional[str] = None
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    type: Optional[str] = None
    label: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        """Representação string da instrução."""
        parts = [self.op.value]
        if self.dest:
            parts.append(self.dest)
        if self.arg1:
            parts.append(self.arg1)
        if self.arg2:
            parts.append(self.arg2)
        return " ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "op": self.op.value,
            "dest": self.dest,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "type": self.type,
            "label": self.label,
            "meta": self.meta or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IRInstruction':
        """Cria a partir de dicionário."""
        return cls(
            op=IROperation(data["op"]),
            dest=data.get("dest"),
            arg1=data.get("arg1"),
            arg2=data.get("arg2"),
            type=data.get("type"),
            label=data.get("label"),
            meta=data.get("meta")
        )


class IRGenerator(ABC):
    """Interface para geradores de IR."""
    
    @abstractmethod
    def generate(self, ast: 'ASTNode') -> List[IRInstruction]:
        """Gera código IR a partir da AST."""
        pass
    
    @abstractmethod
    def new_temp(self) -> str:
        """Gera um novo nome de temporário."""
        pass
    
    @abstractmethod
    def new_label(self) -> str:
        """Gera um novo rótulo."""
        pass


class IROptimizer(ABC):
    """Interface para otimizadores de IR."""
    
    @abstractmethod
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Otimiza uma lista de instruções IR."""
        pass


class ConstantFoldingOptimizer(IROptimizer):
    """Otimizador de dobramento de constantes."""
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica dobramento de constantes."""
        # Implementação básica - pode ser expandida
        return instructions


class PeepholeOptimizer(IROptimizer):
    """Otimizador de janela deslizante."""
    
    def optimize(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Aplica otimizações de janela deslizante."""
        # Implementação básica - pode ser expandida
        return instructions


class IRSerializer(ABC):
    """Interface para serialização de IR."""
    
    @abstractmethod
    def serialize(self, instructions: List[IRInstruction]) -> str:
        """Serializa lista de instruções para string."""
        pass
    
    @abstractmethod
    def deserialize(self, data: str) -> List[IRInstruction]:
        """Deserializa string para lista de instruções."""
        pass


class JSONIRSerializer(IRSerializer):
    """Implementação de serialização JSON para IR."""
    
    def serialize(self, instructions: List[IRInstruction]) -> str:
        """Serializa IR para JSON."""
        import json
        data = [inst.to_dict() for inst in instructions]
        return json.dumps(data, indent=2)
    
    def deserialize(self, data: str) -> List[IRInstruction]:
        """Deserializa JSON para IR."""
        import json
        data_list = json.loads(data)
        return [IRInstruction.from_dict(inst) for inst in data_list]
