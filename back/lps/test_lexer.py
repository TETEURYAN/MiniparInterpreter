#!/usr/bin/env python3
"""
Script de teste para diagnosticar problemas no lexer.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent))

from frontend.lexer_impl import MiniparLexer

def test_lexer():
    """Testa o lexer com o arquivo us01.mp"""
    
    print("=== TESTE DO LEXER ===")
    
    # Lê o arquivo
    try:
        with open('us01.mp', 'r', encoding='utf-8') as f:
            source_code = f.read()
        print(f"Arquivo lido com sucesso. Tamanho: {len(source_code)} caracteres")
        print(f"Conteúdo:\n{source_code}")
        print("-" * 50)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    
    # Testa o lexer
    try:
        print("Iniciando tokenização...")
        lexer = MiniparLexer(source_code)
        tokens = lexer.tokenize()
        
        print(f"\nTokenização concluída. Total de tokens: {len(tokens)}")
        
        # Mostra os primeiros 20 tokens
        print("\nPrimeiros 20 tokens:")
        for i, (token_type, token_value) in enumerate(tokens[:20]):
            print(f"  {i+1:2d}: {token_type} = '{token_value}'")
        
        if len(tokens) > 20:
            print(f"  ... e mais {len(tokens) - 20} tokens")
            
    except Exception as e:
        print(f"Erro na tokenização: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_lexer()
