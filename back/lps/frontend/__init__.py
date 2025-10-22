"""
Frontend da linha de produto de compiladores.

Este módulo contém o frontend completo:
- Lexer: Análise léxica
- Parser: Análise sintática
- AST Builder: Construção da árvore sintática
- Semantic Checker: Análise semântica
- Symbol Table: Tabela de símbolos
"""

from .ast_impl import MiniparASTNode, MiniparASTVisitor
from .lexer_impl import MiniparLexer
from .parser_impl import MiniparParser
from .semantic_impl import MiniparSemanticAnalyzer
from .symbol_table_impl import MiniparSymbolTable

__all__ = [
    'MiniparASTNode',
    'MiniparASTVisitor', 
    'MiniparLexer',
    'MiniparParser',
    'MiniparSemanticAnalyzer',
    'MiniparSymbolTable'
]
