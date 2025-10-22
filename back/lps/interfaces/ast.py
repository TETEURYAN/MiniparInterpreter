"""
Interface para Abstract Syntax Tree (AST).

Define o contrato para representação de árvores sintáticas abstratas
que podem ser serializadas e consumidas por diferentes módulos.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class ASTNodeType(Enum):
    """Tipos de nós da AST."""
    PROGRAM = "PROGRAM"
    BLOCK = "BLOCK"
    DECLARATION = "DECLARATION"
    ASSIGNMENT = "ASSIGNMENT"
    EXPRESSION = "EXPRESSION"
    IDENTIFIER = "IDENTIFIER"
    LITERAL = "LITERAL"
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    IF_STATEMENT = "IF_STATEMENT"
    WHILE_STATEMENT = "WHILE_STATEMENT"
    FOR_STATEMENT = "FOR_STATEMENT"
    PRINT_STATEMENT = "PRINT_STATEMENT"
    INPUT_STATEMENT = "INPUT_STATEMENT"
    FUNCTION_CALL = "FUNCTION_CALL"
    RETURN_STATEMENT = "RETURN_STATEMENT"


class ASTNode(ABC):
    """Interface base para nós da AST."""
    
    def __init__(self, node_type: ASTNodeType, value: Any = None, 
                 location: Optional[Dict[str, int]] = None):
        self.node_type = node_type
        self.value = value
        self.location = location or {}
        self.children: List['ASTNode'] = []
        self.meta: Dict[str, Any] = {}
    
    @abstractmethod
    def add_child(self, child: 'ASTNode') -> None:
        """Adiciona um nó filho."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte o nó para dicionário (serialização)."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ASTNode':
        """Cria nó a partir de dicionário (deserialização)."""
        pass
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Aceita um visitante (padrão Visitor)."""
        pass


class ASTVisitor(ABC):
    """Interface para visitantes da AST."""
    
    @abstractmethod
    def visit_program(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_declaration(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_expression(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_print_statement(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_input_statement(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: ASTNode) -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: ASTNode) -> Any:
        pass


class ASTSerializer(ABC):
    """Interface para serialização da AST."""
    
    @abstractmethod
    def serialize(self, ast: ASTNode) -> str:
        """Serializa AST para string."""
        pass
    
    @abstractmethod
    def deserialize(self, data: str) -> ASTNode:
        """Deserializa string para AST."""
        pass


class JSONASTSerializer(ASTSerializer):
    """Implementação de serialização JSON para AST."""
    
    def serialize(self, ast: ASTNode) -> str:
        """Serializa AST para JSON."""
        import json
        return json.dumps(ast.to_dict(), indent=2)
    
    def deserialize(self, data: str) -> ASTNode:
        """Deserializa JSON para AST."""
        import json
        return ASTNode.from_dict(json.loads(data))
