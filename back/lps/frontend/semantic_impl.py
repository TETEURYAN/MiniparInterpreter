"""
Implementação do analisador semântico para Minipar.

Adapta o analisador semântico existente para seguir as interfaces da linha de produto.
"""

from typing import Any, Dict, List, Optional
from interfaces.ast import ASTNode, ASTNodeType
from interfaces.symbol_table import SymbolTable, Symbol, SymbolType, DataType
from common.tokens import TokenEnums as en


class MiniparSemanticAnalyzer:
    """Analisador semântico para Minipar adaptado para a linha de produto."""
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.current_scope = "global"
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def analyze(self, ast: ASTNode) -> None:
        """Analisa a AST semanticamente."""
        self.errors.clear()
        self.warnings.clear()
        
        try:
            self._analyze_node(ast)
        except Exception as e:
            self.errors.append(f"Erro semântico: {e}")
    
    def _analyze_node(self, node: ASTNode) -> Any:
        """Analisa um nó da AST."""
        if node.node_type == ASTNodeType.PROGRAM:
            return self._analyze_program(node)
        elif node.node_type == ASTNodeType.BLOCK:
            return self._analyze_block(node)
        elif node.node_type == ASTNodeType.DECLARATION:
            return self._analyze_declaration(node)
        elif node.node_type == ASTNodeType.ASSIGNMENT:
            return self._analyze_assignment(node)
        elif node.node_type == ASTNodeType.EXPRESSION:
            return self._analyze_expression(node)
        elif node.node_type == ASTNodeType.IDENTIFIER:
            return self._analyze_identifier(node)
        elif node.node_type == ASTNodeType.LITERAL:
            return self._analyze_literal(node)
        elif node.node_type == ASTNodeType.BINARY_OP:
            return self._analyze_binary_op(node)
        elif node.node_type == ASTNodeType.UNARY_OP:
            return self._analyze_unary_op(node)
        elif node.node_type == ASTNodeType.IF_STATEMENT:
            return self._analyze_if_statement(node)
        elif node.node_type == ASTNodeType.WHILE_STATEMENT:
            return self._analyze_while_statement(node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            return self._analyze_for_statement(node)
        elif node.node_type == ASTNodeType.PRINT_STATEMENT:
            return self._analyze_print_statement(node)
        elif node.node_type == ASTNodeType.INPUT_STATEMENT:
            return self._analyze_input_statement(node)
        else:
            return None
    
    def _analyze_program(self, node: ASTNode) -> None:
        """Analisa um programa."""
        for child in node.children:
            self._analyze_node(child)
    
    def _analyze_block(self, node: ASTNode) -> None:
        """Analisa um bloco de código."""
        self.symbol_table.enter_scope(f"block_{id(node)}")
        
        for child in node.children:
            self._analyze_node(child)
        
        self.symbol_table.exit_scope()
    
    def _analyze_declaration(self, node: ASTNode) -> None:
        """Analisa uma declaração de variável."""
        if node.children and node.children[0].node_type == ASTNodeType.ASSIGNMENT:
            self._analyze_assignment(node.children[0])
    
    def _analyze_assignment(self, node: ASTNode) -> Any:
        """Analisa uma atribuição."""
        if len(node.children) >= 2:
            var_name = node.children[0].value
            value_type = self._analyze_expression(node.children[1])
            
            # Cria símbolo na tabela
            symbol = Symbol(
                name=var_name,
                symbol_type=SymbolType.VARIABLE,
                data_type=DataType.INT,  # Assumindo tipo inteiro por padrão
                scope=self.symbol_table.get_current_scope(),
                is_initialized=True
            )
            
            try:
                self.symbol_table.declare_symbol(symbol)
            except Exception as e:
                self.errors.append(f"Erro na declaração de {var_name}: {e}")
            
            return value_type
        
        return None
    
    def _analyze_expression(self, node: ASTNode) -> DataType:
        """Analisa uma expressão."""
        if node.node_type == ASTNodeType.IDENTIFIER:
            return self._analyze_identifier(node)
        elif node.node_type == ASTNodeType.LITERAL:
            return self._analyze_literal(node)
        elif node.node_type == ASTNodeType.BINARY_OP:
            return self._analyze_binary_op(node)
        elif node.node_type == ASTNodeType.UNARY_OP:
            return self._analyze_unary_op(node)
        else:
            return DataType.INT  # Tipo padrão
    
    def _analyze_identifier(self, node: ASTNode) -> DataType:
        """Analisa um identificador."""
        var_name = node.value
        symbol = self.symbol_table.lookup_symbol(var_name)
        
        if symbol:
            return symbol.data_type
        else:
            self.errors.append(f"Variável não definida: {var_name}")
            return DataType.INT
    
    def _analyze_literal(self, node: ASTNode) -> DataType:
        """Analisa um literal."""
        if isinstance(node.value, str):
            return DataType.STRING
        elif isinstance(node.value, bool):
            return DataType.BOOL
        else:
            return DataType.INT
    
    def _analyze_binary_op(self, node: ASTNode) -> DataType:
        """Analisa uma operação binária."""
        if len(node.children) >= 2:
            left_type = self._analyze_expression(node.children[0])
            right_type = self._analyze_expression(node.children[1])
            
            # Verifica compatibilidade de tipos
            if left_type != right_type:
                self.warnings.append(f"Operação entre tipos diferentes: {left_type} e {right_type}")
            
            # Retorna o tipo resultante
            if node.value in ["==", "!=", "<", "<=", ">", ">=", "&&", "||"]:
                return DataType.BOOL
            else:
                return DataType.INT
        
        return DataType.INT
    
    def _analyze_unary_op(self, node: ASTNode) -> DataType:
        """Analisa uma operação unária."""
        if node.children:
            operand_type = self._analyze_expression(node.children[0])
            
            if node.value == "!":
                return DataType.BOOL
            else:
                return operand_type
        
        return DataType.INT
    
    def _analyze_if_statement(self, node: ASTNode) -> None:
        """Analisa uma instrução if."""
        if len(node.children) >= 2:
            condition_type = self._analyze_expression(node.children[0])
            
            if condition_type != DataType.BOOL:
                self.errors.append("Condição do if deve ser booleana")
            
            self._analyze_node(node.children[1])
            
            if len(node.children) > 2:
                self._analyze_node(node.children[2])
    
    def _analyze_while_statement(self, node: ASTNode) -> None:
        """Analisa uma instrução while."""
        if len(node.children) >= 2:
            condition_type = self._analyze_expression(node.children[0])
            
            if condition_type != DataType.BOOL:
                self.errors.append("Condição do while deve ser booleana")
            
            self._analyze_node(node.children[1])
    
    def _analyze_for_statement(self, node: ASTNode) -> None:
        """Analisa uma instrução for."""
        if len(node.children) >= 3:
            # Inicialização
            self._analyze_node(node.children[0])
            
            # Condição
            condition_type = self._analyze_expression(node.children[1])
            if condition_type != DataType.BOOL:
                self.errors.append("Condição do for deve ser booleana")
            
            # Corpo
            self._analyze_node(node.children[2])
            
            # Incremento (se existir)
            if len(node.children) > 3:
                self._analyze_node(node.children[3])
    
    def _analyze_print_statement(self, node: ASTNode) -> None:
        """Analisa uma instrução print."""
        for child in node.children:
            self._analyze_expression(child)
    
    def _analyze_input_statement(self, node: ASTNode) -> None:
        """Analisa uma instrução input."""
        if node.children:
            var_name = node.children[0].value
            symbol = self.symbol_table.lookup_symbol(var_name)
            
            if not symbol:
                self.errors.append(f"Variável não definida para input: {var_name}")
    
    def get_errors(self) -> List[str]:
        """Retorna lista de erros encontrados."""
        return self.errors.copy()
    
    def get_warnings(self) -> List[str]:
        """Retorna lista de avisos encontrados."""
        return self.warnings.copy()
    
    def has_errors(self) -> bool:
        """Verifica se há erros."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Verifica se há avisos."""
        return len(self.warnings) > 0
