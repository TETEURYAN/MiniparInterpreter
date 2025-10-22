#!/usr/bin/env python3
"""
Demonstração da Linha de Produto de Software para Compiladores Minipar.

Este arquivo demonstra como usar a linha de produto para criar
diferentes produtos de compilação.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent))

from cli import MiniparCLI
from product_config import PREDEFINED_PRODUCTS


def demo_list_products():
    """Demonstra o comando list-products."""
    print("=== Demonstração: Listando Produtos Disponíveis ===")
    print()
    
    cli = MiniparCLI()
    result = cli.run(['list-products'])
    
    print(f"Resultado: {result}")
    print()


def demo_create_config():
    """Demonstra o comando create-config."""
    print("=== Demonstração: Criando Configuração ===")
    print()
    
    cli = MiniparCLI()
    result = cli.run([
        'create-config',
        '--product', 'minipar_compiler_x86_64',
        '--output', 'demo_config.yaml',
        '--format', 'yaml'
    ])
    
    print(f"Resultado: {result}")
    print()
    
    # Mostra o conteúdo do arquivo criado
    if Path('demo_config.yaml').exists():
        print("Conteúdo do arquivo de configuração criado:")
        with open('demo_config.yaml', 'r') as f:
            print(f.read())
        print()


def demo_build_compiler():
    """Demonstra a construção de um compilador."""
    print("=== Demonstração: Construindo Compilador x86_64 ===")
    print()
    
    # Cria um arquivo de teste
    test_code = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('demo_input.mp', 'w') as f:
        f.write(test_code)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--product', 'minipar_compiler_x86_64',
            'demo_input.mp',
            '--output', 'demo_output.s'
        ])
        
        print(f"Resultado: {result}")
        print()
        
        # Mostra o conteúdo do arquivo de saída
        if Path('demo_output.s').exists():
            print("Conteúdo do arquivo de saída (primeiras 20 linhas):")
            with open('demo_output.s', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20]):
                    print(f"{i+1:2d}: {line.rstrip()}")
                if len(lines) > 20:
                    print(f"... e mais {len(lines) - 20} linhas")
        else:
            print("Arquivo de saída não foi criado!")
            
    finally:
        # Limpa arquivos de teste
        for file in ['demo_input.mp', 'demo_output.s']:
            if Path(file).exists():
                Path(file).unlink()


def demo_build_interpreter():
    """Demonstra a construção de um interpretador."""
    print("=== Demonstração: Construindo Interpretador ===")
    print()
    
    # Cria um arquivo de teste
    test_code = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('demo_input.mp', 'w') as f:
        f.write(test_code)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--product', 'minipar_interpreter',
            'demo_input.mp'
        ])
        
        print(f"Resultado: {result}")
        print()
        
    finally:
        # Limpa arquivos de teste
        if Path('demo_input.mp').exists():
            Path('demo_input.mp').unlink()


def demo_build_ir_generator():
    """Demonstra a construção de um gerador de IR."""
    print("=== Demonstração: Construindo Gerador de IR ===")
    print()
    
    # Cria um arquivo de teste
    test_code = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('demo_input.mp', 'w') as f:
        f.write(test_code)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--product', 'minipar_ir_generator',
            'demo_input.mp',
            '--output', 'demo_output.ir'
        ])
        
        print(f"Resultado: {result}")
        print()
        
        # Mostra o conteúdo do arquivo de saída
        if Path('demo_output.ir').exists():
            print("Conteúdo do arquivo de saída IR:")
            with open('demo_output.ir', 'r') as f:
                print(f.read())
        else:
            print("Arquivo de saída não foi criado!")
            
    finally:
        # Limpa arquivos de teste
        for file in ['demo_input.mp', 'demo_output.ir']:
            if Path(file).exists():
                Path(file).unlink()


def demo_build_riscv_compiler():
    """Demonstra a construção de um compilador RISC-V."""
    print("=== Demonstração: Construindo Compilador RISC-V ===")
    print()
    
    # Cria um arquivo de teste
    test_code = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('demo_input.mp', 'w') as f:
        f.write(test_code)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--product', 'minipar_compiler_riscv',
            'demo_input.mp',
            '--output', 'demo_output_riscv.s'
        ])
        
        print(f"Resultado: {result}")
        print()
        
        # Mostra o conteúdo do arquivo de saída
        if Path('demo_output_riscv.s').exists():
            print("Conteúdo do arquivo de saída RISC-V (primeiras 20 linhas):")
            with open('demo_output_riscv.s', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20]):
                    print(f"{i+1:2d}: {line.rstrip()}")
                if len(lines) > 20:
                    print(f"... e mais {len(lines) - 20} linhas")
        else:
            print("Arquivo de saída não foi criado!")
            
    finally:
        # Limpa arquivos de teste
        for file in ['demo_input.mp', 'demo_output_riscv.s']:
            if Path(file).exists():
                Path(file).unlink()


def demo_build_with_custom_config():
    """Demonstra a construção com configuração customizada."""
    print("=== Demonstração: Construindo com Configuração Customizada ===")
    print()
    
    # Cria um arquivo de teste
    test_code = """
    int a = 5;
    int b = 10;
    int c = a + b;
    print(c);
    """
    
    with open('demo_input.mp', 'w') as f:
        f.write(test_code)
    
    # Cria uma configuração customizada
    custom_config = """
name: demo_compiler
product_type: compiler
description: Compilador de demonstração
version: 1.0.0

frontend:
  enable_lexer: true
  enable_parser: true
  enable_semantic_checker: true
  enable_ast_builder: true
  enable_symbol_table: true

backend:
  backend_type: x86_64
  enable_register_allocation: true
  enable_optimization: true
  optimization_level: basic
  enable_debug_info: false
  target_os: linux
  target_arch: x86_64

ir:
  enable_ir_generation: true
  enable_optimization: true
  enable_constant_folding: true
  enable_peephole_optimization: true
  output_format: json

output_file: demo_custom_output.s
verbose: true
debug: false
"""
    
    with open('demo_custom_config.yaml', 'w') as f:
        f.write(custom_config)
    
    try:
        cli = MiniparCLI()
        result = cli.run([
            'build',
            '--config', 'demo_custom_config.yaml',
            'demo_input.mp'
        ])
        
        print(f"Resultado: {result}")
        print()
        
        # Mostra o conteúdo do arquivo de saída
        if Path('demo_custom_output.s').exists():
            print("Conteúdo do arquivo de saída customizado (primeiras 20 linhas):")
            with open('demo_custom_output.s', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20]):
                    print(f"{i+1:2d}: {line.rstrip()}")
                if len(lines) > 20:
                    print(f"... e mais {len(lines) - 20} linhas")
        else:
            print("Arquivo de saída não foi criado!")
            
    finally:
        # Limpa arquivos de teste
        for file in ['demo_input.mp', 'demo_custom_config.yaml', 'demo_custom_output.s']:
            if Path(file).exists():
                Path(file).unlink()


def main():
    """Função principal de demonstração."""
    print("=== Demonstração da Linha de Produto de Compiladores Minipar ===")
    print()
    
    try:
        # Demonstra listagem de produtos
        demo_list_products()
        
        # Demonstra criação de configuração
        demo_create_config()
        
        # Demonstra construção de compilador x86_64
        demo_build_compiler()
        
        # Demonstra construção de interpretador
        demo_build_interpreter()
        
        # Demonstra construção de gerador de IR
        demo_build_ir_generator()
        
        # Demonstra construção de compilador RISC-V
        demo_build_riscv_compiler()
        
        # Demonstra construção com configuração customizada
        demo_build_with_custom_config()
        
        print("=== Demonstração concluída com sucesso! ===")
        
    except Exception as e:
        print(f"Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
