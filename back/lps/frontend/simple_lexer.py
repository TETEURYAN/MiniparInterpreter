#!/usr/bin/env python3
"""
Lexer simplificado para Minipar que não depende do lexer original.
"""

import re
from typing import List, Tuple, Any
from common.tokens import TokenEnums as en


class SimpleMiniparLexer:
    """Lexer simplificado para Minipar."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.tokens: List[Tuple[en, Any]] = []
    
    def tokenize(self) -> List[Tuple[en, Any]]:
        """Tokeniza o código fonte usando regex simples."""
        self.tokens = []
        self.position = 0
        
        # Padrões de tokens (apenas os que existem no TokenEnums)
        patterns = [
            (en.RW_C_CHANNEL, r'\bc_channel\b'),
            (en.RW_SEQ, r'\bSEQ\b'),
            (en.RW_PAR, r'\bPAR\b'),
            (en.RW_PRINT, r'\bprint\b'),
            (en.RW_INPUT, r'\binput\b'),
            (en.RW_IF, r'\bif\b'),
            (en.RW_ELSE, r'\belse\b'),
            (en.RW_WHILE, r'\bwhile\b'),
            (en.RW_FOR, r'\bfor\b'),
            (en.RW_INT, r'\bint\b'),
            (en.RW_BOOL, r'\bbool\b'),
            (en.RW_STRING, r'\bstring\b'),
            (en.RW_TRUE, r'\btrue\b'),
            (en.RW_FALSE, r'\bfalse\b'),
            (en.RW_NULL, r'\bnull\b'),
            (en.RW_CHAN, r'\bchan\b'),
            (en.RW_RETURN, r'\breturn\b'),
            (en.ID, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            (en.NUM, r'\d+'),
            (en.STRING_LITERAL, r'"[^"]*"'),
            (en.DL_LPAREN, r'\('),
            (en.DL_RPAREN, r'\)'),
            (en.DL_LBRACE, r'\{'),
            (en.DL_RBRACE, r'\}'),
            (en.DL_LBRACKET, r'\['),
            (en.DL_RBRACKET, r'\]'),
            (en.DL_COMMA, r','),
            (en.DL_SEMICOLON, r';'),
            (en.DL_DOT, r'\.'),
            (en.OP_PLUS, r'\+'),
            (en.OP_MINUS, r'-'),
            (en.OP_MULTIPLY, r'\*'),
            (en.OP_DIVIDE, r'/'),
            (en.OP_EQ, r'=='),
            (en.OP_NE, r'!='),
            (en.OP_LT, r'<'),
            (en.OP_LE, r'<='),
            (en.OP_GT, r'>'),
            (en.OP_GE, r'>='),
            (en.OP_ASSIGN, r'='),
            (en.OP_AND, r'&&'),
            (en.OP_OR, r'\|\|'),
            (en.OP_NOT, r'!'),
            (en.OP_INC, r'\+\+'),
            (en.OP_DEC, r'--'),
            (en.OP_PLUS_ASSIGN, r'\+='),
            (en.OP_MINUS_ASSIGN, r'-='),
        ]
        
        # Compila padrões
        compiled_patterns = [(token_type, re.compile(pattern)) for token_type, pattern in patterns]
        
        print(f"Iniciando tokenização simplificada...")
        
        while self.position < len(self.source_code):
            matched = False
            
            # Pula whitespace primeiro
            whitespace_match = re.match(r'\s+', self.source_code[self.position:])
            if whitespace_match:
                self.position += whitespace_match.end()
                matched = True
                continue
            
            for token_type, pattern in compiled_patterns:
                match = pattern.match(self.source_code, self.position)
                if match:
                    value = match.group(0)
                    
                    # Adiciona token
                    self.tokens.append((token_type, value))
                    print(f"Token: {token_type} = '{value}'")
                    
                    self.position = match.end()
                    matched = True
                    break
            
            if not matched:
                # Caractere não reconhecido
                char = self.source_code[self.position]
                print(f"⚠️  Caractere não reconhecido: '{char}' (posição {self.position})")
                self.position += 1
        
        # Adiciona EOF
        self.tokens.append((en.EOF, ""))
        print(f"✅ Tokenização concluída com {len(self.tokens)} tokens.")
        
        return self.tokens
