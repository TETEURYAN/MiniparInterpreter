#!/usr/bin/env python3
"""
Exemplo de teste da linha de produto de compiladores Minipar.

Este arquivo demonstra como usar a linha de produto para criar
diferentes produtos de compilação.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent))

from cli import MiniparCLI
from product_config import PREDEFINED_PRODUCTS


def test_list_products():
    """Testa o comando list-products."""
    print("=== Testando list-products ===")
    
    cli = MiniparCLI()
    result = cli.run(['list-products'])
    
    print(f"Resultado: {result}")
    print()


def test_create_config():
    """Testa o comando create-config."""
    print("=== Testando create-config ===")
    
    cli = MiniparCLI()
    result = cli.run([
        'create-config',
        '--product', 'minipar_compiler_x86_64',
        '--output', 'test_config.yaml',
        '--format', 'yaml'
    ])
    
    print(f"Resultado: {result}")
    print()


def test_build_with_config():
    """Testa o comando build com configuração."""
    print("=== Testando build com configuração ===")
    
    # Cria um arquivo de teste
    test_input = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('test_input.mp', 'w') as f:
        f.write(test_input)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--config', 'test_config.yaml',
            'test_input.mp',
            '--output', 'test_output.s'
        ])
        
        print(f"Resultado: {result}")
        print()
        
        # Verifica se o arquivo de saída foi criado
        if Path('test_output.s').exists():
            print("Arquivo de saída criado com sucesso!")
            with open('test_output.s', 'r') as f:
                content = f.read()
                print(f"Conteúdo do arquivo de saída (primeiras 10 linhas):")
                print('\n'.join(content.split('\n')[:10]))
        else:
            print("Arquivo de saída não foi criado!")
            
    finally:
        # Limpa arquivos de teste
        for file in ['test_input.mp', 'test_config.yaml', 'test_output.s']:
            if Path(file).exists():
                Path(file).unlink()


def test_build_interpreter():
    """Testa o comando build com interpretador."""
    print("=== Testando build com interpretador ===")
    
    # Cria um arquivo de teste
    test_input = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('test_input.mp', 'w') as f:
        f.write(test_input)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--product', 'minipar_interpreter',
            'test_input.mp'
        ])
        
        print(f"Resultado: {result}")
        print()
        
    finally:
        # Limpa arquivos de teste
        if Path('test_input.mp').exists():
            Path('test_input.mp').unlink()


def main():
    """Função principal de teste."""
    print("=== Testes da Linha de Produto de Compiladores Minipar ===")
    print()
    
    try:
        # Testa listagem de produtos
        test_list_products()
        
        # Testa criação de configuração
        test_create_config()
        
        # Testa build com configuração
        test_build_with_config()
        
        # Testa build com interpretador
        test_build_interpreter()
        
        print("=== Todos os testes concluídos ===")
        
    except Exception as e:
        print(f"Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
