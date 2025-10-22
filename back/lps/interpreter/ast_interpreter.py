"""
Interpretador de AST para Minipar.

Este módulo implementa um interpretador que executa diretamente
a árvore sintática abstrata.
"""

from typing import Any, Dict, List, Optional
from ..interfaces.ast import ASTNode, ASTNodeType
from ..interfaces.symbol_table import SymbolTable, Symbol, SymbolType, DataType
from ..interfaces.ir import IROperation


class MiniparASTInterpreter:
    """Interpretador de AST para Minipar."""
    
    def __init__(self, ast: ASTNode, symbol_table: SymbolTable):
        self.ast = ast
        self.symbol_table = symbol_table
        self.output: List[str] = []
        self.debug_mode = False
        self.tracing = False
    
    def execute(self) -> str:
        """Executa a AST e retorna a saída."""
        try:
            self._execute_node(self.ast)
            return "\n".join(self.output)
        except Exception as e:
            if self.debug_mode:
                raise
            else:
                return f"Erro na execução: {e}"
    
    def _execute_node(self, node: ASTNode) -> Any:
        """Executa um nó da AST."""
        if self.tracing:
            print(f"Executando nó: {node.node_type.value}")
        
        if node.node_type == ASTNodeType.PROGRAM:
            return self._execute_program(node)
        elif node.node_type == ASTNodeType.BLOCK:
            return self._execute_block(node)
        elif node.node_type == ASTNodeType.DECLARATION:
            return self._execute_declaration(node)
        elif node.node_type == ASTNodeType.ASSIGNMENT:
            return self._execute_assignment(node)
        elif node.node_type == ASTNodeType.EXPRESSION:
            return self._execute_expression(node)
        elif node.node_type == ASTNodeType.IDENTIFIER:
            return self._execute_identifier(node)
        elif node.node_type == ASTNodeType.LITERAL:
            return self._execute_literal(node)
        elif node.node_type == ASTNodeType.BINARY_OP:
            return self._execute_binary_op(node)
        elif node.node_type == ASTNodeType.UNARY_OP:
            return self._execute_unary_op(node)
        elif node.node_type == ASTNodeType.IF_STATEMENT:
            return self._execute_if_statement(node)
        elif node.node_type == ASTNodeType.WHILE_STATEMENT:
            return self._execute_while_statement(node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            return self._execute_for_statement(node)
        elif node.node_type == ASTNodeType.PRINT_STATEMENT:
            return self._execute_print_statement(node)
        elif node.node_type == ASTNodeType.INPUT_STATEMENT:
            return self._execute_input_statement(node)
        else:
            raise ValueError(f"Tipo de nó não suportado: {node.node_type}")
    
    def _execute_program(self, node: ASTNode) -> None:
        """Executa um programa."""
        for child in node.children:
            self._execute_node(child)
    
    def _execute_block(self, node: ASTNode) -> None:
        """Executa um bloco de código."""
        for child in node.children:
            self._execute_node(child)
    
    def _execute_declaration(self, node: ASTNode) -> None:
        """Executa uma declaração de variável."""
        if node.children and node.children[0].node_type == ASTNodeType.ASSIGNMENT:
            self._execute_assignment(node.children[0])
    
    def _execute_assignment(self, node: ASTNode) -> Any:
        """Executa uma atribuição."""
        if len(node.children) >= 2:
            var_name = node.children[0].value
            value = self._execute_expression(node.children[1])
            
            # Atualiza a tabela de símbolos
            symbol = Symbol(
                name=var_name,
                symbol_type=SymbolType.VARIABLE,
                data_type=DataType.INT,
                scope=self.symbol_table.get_current_scope(),
                value=value,
                is_initialized=True
            )
            self.symbol_table.declare_symbol(symbol)
            
            return value
        
        return None
    
    def _execute_expression(self, node: ASTNode) -> Any:
        """Executa uma expressão."""
        if node.node_type == ASTNodeType.IDENTIFIER:
            return self._execute_identifier(node)
        elif node.node_type == ASTNodeType.LITERAL:
            return self._execute_literal(node)
        elif node.node_type == ASTNodeType.BINARY_OP:
            return self._execute_binary_op(node)
        elif node.node_type == ASTNodeType.UNARY_OP:
            return self._execute_unary_op(node)
        else:
            # Para outros tipos de expressão
            return self._execute_node(node.children[0]) if node.children else None
    
    def _execute_identifier(self, node: ASTNode) -> Any:
        """Executa um identificador."""
        var_name = node.value
        symbol = self.symbol_table.lookup_symbol(var_name)
        
        if symbol:
            return symbol.value
        else:
            raise NameError(f"Variável não definida: {var_name}")
    
    def _execute_literal(self, node: ASTNode) -> Any:
        """Executa um literal."""
        return node.value
    
    def _execute_binary_op(self, node: ASTNode) -> Any:
        """Executa uma operação binária."""
        if len(node.children) >= 2:
            left = self._execute_expression(node.children[0])
            right = self._execute_expression(node.children[1])
            operator = node.value
            
            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                if right == 0:
                    raise ZeroDivisionError("Divisão por zero")
                return left / right
            elif operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == "<":
                return left < right
            elif operator == "<=":
                return left <= right
            elif operator == ">":
                return left > right
            elif operator == ">=":
                return left >= right
            elif operator == "&&":
                return left and right
            elif operator == "||":
                return left or right
            else:
                raise ValueError(f"Operador não suportado: {operator}")
        
        return None
    
    def _execute_unary_op(self, node: ASTNode) -> Any:
        """Executa uma operação unária."""
        if node.children:
            operand = self._execute_expression(node.children[0])
            operator = node.value
            
            if operator == "!":
                return not operand
            elif operator == "-":
                return -operand
            else:
                raise ValueError(f"Operador unário não suportado: {operator}")
        
        return None
    
    def _execute_if_statement(self, node: ASTNode) -> None:
        """Executa uma instrução if."""
        if len(node.children) >= 2:
            condition = self._execute_expression(node.children[0])
            
            if condition:
                self._execute_node(node.children[1])
            elif len(node.children) > 2:
                self._execute_node(node.children[2])
    
    def _execute_while_statement(self, node: ASTNode) -> None:
        """Executa uma instrução while."""
        if len(node.children) >= 2:
            while True:
                condition = self._execute_expression(node.children[0])
                if not condition:
                    break
                self._execute_node(node.children[1])
    
    def _execute_for_statement(self, node: ASTNode) -> None:
        """Executa uma instrução for."""
        if len(node.children) >= 3:
            # Inicialização
            self._execute_node(node.children[0])
            
            # Loop
            while True:
                condition = self._execute_expression(node.children[1])
                if not condition:
                    break
                self._execute_node(node.children[2])
                # Incremento (assumindo que o segundo filho é o incremento)
                if len(node.children) > 3:
                    self._execute_node(node.children[3])
    
    def _execute_print_statement(self, node: ASTNode) -> None:
        """Executa uma instrução print."""
        values = []
        for child in node.children:
            value = self._execute_expression(child)
            values.append(str(value))
        
        output_line = " ".join(values)
        self.output.append(output_line)
        
        if self.debug_mode:
            print(f"PRINT: {output_line}")
    
    def _execute_input_statement(self, node: ASTNode) -> Any:
        """Executa uma instrução input."""
        if node.children:
            var_name = node.children[0].value
            try:
                value = int(input())
                
                # Atualiza a tabela de símbolos
                symbol = Symbol(
                    name=var_name,
                    symbol_type=SymbolType.VARIABLE,
                    data_type=DataType.INT,
                    scope=self.symbol_table.get_current_scope(),
                    value=value,
                    is_initialized=True
                )
                self.symbol_table.declare_symbol(symbol)
                
                return value
            except ValueError:
                raise ValueError("Entrada inválida: esperado um número inteiro")
        
        return None
    
    def set_debug_mode(self, enabled: bool) -> None:
        """Habilita/desabilita modo debug."""
        self.debug_mode = enabled
    
    def set_tracing(self, enabled: bool) -> None:
        """Habilita/desabilita rastreamento."""
        self.tracing = enabled
    
    def get_output(self) -> List[str]:
        """Retorna a saída gerada."""
        return self.output.copy()
    
    def clear_output(self) -> None:
        """Limpa a saída."""
        self.output.clear()
