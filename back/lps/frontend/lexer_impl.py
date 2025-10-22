"""
Implementação do lexer para Minipar.

Adapta o lexer existente para seguir as interfaces da linha de produto.
"""

from typing import List, Tuple, Any
from interfaces.ast import ASTNode, ASTNodeType
from common.tokens import TokenEnums as en
from .simple_lexer import SimpleMiniparLexer


class MiniparLexer:
    """Lexer para Minipar adaptado para a linha de produto."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lexer = SimpleMiniparLexer(source_code)
        self.tokens: List[Tuple[en, Any]] = []
    
    def tokenize(self) -> List[Tuple[en, Any]]:
        """Tokeniza o código fonte."""
        print("Usando lexer simplificado...")
        self.tokens = self.lexer.tokenize()
        return self.tokens
    
    def get_tokens(self) -> List[Tuple[en, Any]]:
        """Retorna a lista de tokens."""
        return self.tokens
