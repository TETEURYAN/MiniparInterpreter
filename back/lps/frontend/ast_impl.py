"""
Implementação concreta da AST para Minipar.

Esta implementação adapta a AST existente do projeto para seguir
as interfaces definidas na linha de produto.
"""

from typing import Any, Dict, List, Optional
from interfaces.ast import ASTNode, ASTNodeType, ASTVisitor
from common.tokens import TokenEnums as en


class MiniparASTNode(ASTNode):
    """Implementação concreta de nó AST para Minipar."""
    
    def __init__(self, node_type: ASTNodeType, value: Any = None, 
                 location: Optional[Dict[str, int]] = None):
        super().__init__(node_type, value, location)
        self._minipar_type = self._convert_to_minipar_type(node_type)
    
    def _convert_to_minipar_type(self, node_type: ASTNodeType) -> en:
        """Converte ASTNodeType para TokenEnums do Minipar."""
        mapping = {
            ASTNodeType.PROGRAM: en.PROGRAM,
            ASTNodeType.BLOCK: en.BLOCK,
            ASTNodeType.DECLARATION: en.DECLARATION,
            ASTNodeType.ASSIGNMENT: en.OP_ASSIGN,
            ASTNodeType.EXPRESSION: en.ID,  # Usa ID como fallback para EXPRESSION
            ASTNodeType.IDENTIFIER: en.ID,
            ASTNodeType.LITERAL: en.NUM,
            ASTNodeType.BINARY_OP: en.OP_PLUS,  # Será ajustado dinamicamente
            ASTNodeType.UNARY_OP: en.OP_NOT,
            ASTNodeType.IF_STATEMENT: en.RW_IF,
            ASTNodeType.WHILE_STATEMENT: en.RW_WHILE,
            ASTNodeType.FOR_STATEMENT: en.RW_FOR,
            ASTNodeType.PRINT_STATEMENT: en.RW_PRINT,
            ASTNodeType.INPUT_STATEMENT: en.RW_INPUT,
            ASTNodeType.FUNCTION_CALL: en.CALL,
            ASTNodeType.RETURN_STATEMENT: en.RW_RETURN,
        }
        return mapping.get(node_type, en.PROGRAM)
    
    def add_child(self, child: 'ASTNode') -> None:
        """Adiciona um nó filho."""
        self.children.append(child)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o nó para dicionário."""
        return {
            "node_type": self.node_type.value,
            "value": self.value,
            "location": self.location,
            "children": [child.to_dict() for child in self.children],
            "meta": self.meta
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ASTNode':
        """Cria nó a partir de dicionário."""
        node_type = ASTNodeType(data["node_type"])
        node = cls(node_type, data.get("value"), data.get("location"))
        node.meta = data.get("meta", {})
        
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data)
            node.add_child(child)
        
        return node
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Aceita um visitante."""
        method_name = f"visit_{self.node_type.value.lower()}"
        method = getattr(visitor, method_name, None)
        if method:
            return method(self)
        else:
            return visitor.visit_default(self)
    
    def get_minipar_type(self) -> en:
        """Retorna o tipo Minipar correspondente."""
        return self._minipar_type
    
    def set_minipar_type(self, minipar_type: en) -> None:
        """Define o tipo Minipar."""
        self._minipar_type = minipar_type


class MiniparASTVisitor(ASTVisitor):
    """Implementação base de visitante para AST Minipar."""
    
    def visit_program(self, node: ASTNode) -> Any:
        """Visita nó de programa."""
        results = []
        for child in node.children:
            result = child.accept(self)
            if result is not None:
                results.append(result)
        return results
    
    def visit_block(self, node: ASTNode) -> Any:
        """Visita nó de bloco."""
        results = []
        for child in node.children:
            result = child.accept(self)
            if result is not None:
                results.append(result)
        return results
    
    def visit_declaration(self, node: ASTNode) -> Any:
        """Visita nó de declaração."""
        return self._visit_children(node)
    
    def visit_assignment(self, node: ASTNode) -> Any:
        """Visita nó de atribuição."""
        return self._visit_children(node)
    
    def visit_expression(self, node: ASTNode) -> Any:
        """Visita nó de expressão."""
        return self._visit_children(node)
    
    def visit_identifier(self, node: ASTNode) -> Any:
        """Visita nó de identificador."""
        return node.value
    
    def visit_literal(self, node: ASTNode) -> Any:
        """Visita nó de literal."""
        return node.value
    
    def visit_binary_op(self, node: ASTNode) -> Any:
        """Visita nó de operação binária."""
        return self._visit_children(node)
    
    def visit_unary_op(self, node: ASTNode) -> Any:
        """Visita nó de operação unária."""
        return self._visit_children(node)
    
    def visit_if_statement(self, node: ASTNode) -> Any:
        """Visita nó de if."""
        return self._visit_children(node)
    
    def visit_while_statement(self, node: ASTNode) -> Any:
        """Visita nó de while."""
        return self._visit_children(node)
    
    def visit_for_statement(self, node: ASTNode) -> Any:
        """Visita nó de for."""
        return self._visit_children(node)
    
    def visit_print_statement(self, node: ASTNode) -> Any:
        """Visita nó de print."""
        return self._visit_children(node)
    
    def visit_input_statement(self, node: ASTNode) -> Any:
        """Visita nó de input."""
        return self._visit_children(node)
    
    def visit_function_call(self, node: ASTNode) -> Any:
        """Visita nó de chamada de função."""
        return self._visit_children(node)
    
    def visit_return_statement(self, node: ASTNode) -> Any:
        """Visita nó de return."""
        return self._visit_children(node)
    
    def visit_default(self, node: ASTNode) -> Any:
        """Método padrão para nós não tratados."""
        return self._visit_children(node)
    
    def _visit_children(self, node: ASTNode) -> Any:
        """Visita todos os filhos de um nó."""
        results = []
        for child in node.children:
            result = child.accept(self)
            if result is not None:
                results.append(result)
        return results if results else None


class MiniparASTBuilder:
    """Construtor de AST para Minipar."""
    
    def __init__(self):
        self.current_location = {"line": 1, "column": 1}
    
    def create_node(self, node_type: ASTNodeType, value: Any = None) -> MiniparASTNode:
        """Cria um novo nó AST."""
        return MiniparASTNode(node_type, value, self.current_location.copy())
    
    def create_program(self) -> MiniparASTNode:
        """Cria nó de programa."""
        return self.create_node(ASTNodeType.PROGRAM)
    
    def create_block(self) -> MiniparASTNode:
        """Cria nó de bloco."""
        return self.create_node(ASTNodeType.BLOCK)
    
    def create_declaration(self, var_type: str, name: str, value: MiniparASTNode) -> MiniparASTNode:
        """Cria nó de declaração."""
        decl_node = self.create_node(ASTNodeType.DECLARATION, var_type)
        
        # Cria nó de atribuição
        assign_node = self.create_node(ASTNodeType.ASSIGNMENT)
        assign_node.add_child(self.create_identifier(name))
        assign_node.add_child(value)
        
        decl_node.add_child(assign_node)
        return decl_node
    
    def create_assignment(self, name: str, value: MiniparASTNode) -> MiniparASTNode:
        """Cria nó de atribuição."""
        assign_node = self.create_node(ASTNodeType.ASSIGNMENT)
        assign_node.add_child(self.create_identifier(name))
        assign_node.add_child(value)
        return assign_node
    
    def create_identifier(self, name: str) -> MiniparASTNode:
        """Cria nó de identificador."""
        return self.create_node(ASTNodeType.IDENTIFIER, name)
    
    def create_literal(self, value: Any, literal_type: str = "NUM") -> MiniparASTNode:
        """Cria nó de literal."""
        return self.create_node(ASTNodeType.LITERAL, value)
    
    def create_binary_op(self, operator: str, left: MiniparASTNode, right: MiniparASTNode) -> MiniparASTNode:
        """Cria nó de operação binária."""
        op_node = self.create_node(ASTNodeType.BINARY_OP, operator)
        op_node.add_child(left)
        op_node.add_child(right)
        return op_node
    
    def create_if_statement(self, condition: MiniparASTNode, then_block: MiniparASTNode, 
                           else_block: Optional[MiniparASTNode] = None) -> MiniparASTNode:
        """Cria nó de if."""
        if_node = self.create_node(ASTNodeType.IF_STATEMENT)
        if_node.add_child(condition)
        if_node.add_child(then_block)
        if else_block:
            if_node.add_child(else_block)
        return if_node
    
    def create_while_statement(self, condition: MiniparASTNode, block: MiniparASTNode) -> MiniparASTNode:
        """Cria nó de while."""
        while_node = self.create_node(ASTNodeType.WHILE_STATEMENT)
        while_node.add_child(condition)
        while_node.add_child(block)
        return while_node
    
    def create_print_statement(self, expressions: List[MiniparASTNode]) -> MiniparASTNode:
        """Cria nó de print."""
        print_node = self.create_node(ASTNodeType.PRINT_STATEMENT)
        for expr in expressions:
            print_node.add_child(expr)
        return print_node
    
    def update_location(self, line: int, column: int) -> None:
        """Atualiza a localização atual."""
        self.current_location = {"line": line, "column": column}
