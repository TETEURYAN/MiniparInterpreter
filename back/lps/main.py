#!/usr/bin/env python3
"""
Arquivo principal da linha de produto de compiladores Minipar.

Este arquivo demonstra como usar a linha de produto para criar
diferentes produtos de compilação.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent))

from cli.cli import MiniparCLI
from product_config.product_config import PREDEFINED_PRODUCTS


def main():
    """Função principal."""
    print("=== Linha de Produto de Software para Compiladores Minipar ===")
    print()
    
    # Lista produtos disponíveis
    print("Produtos disponíveis:")
    for name, config in PREDEFINED_PRODUCTS.items():
        print(f"  - {name}: {config.description}")
    print()
    
    # Exemplo de uso do CLI
    print("Exemplo de uso:")
    print("  python main.py build --product minipar_compiler_x86_64 input.mp")
    print("  python main.py build --product minipar_interpreter input.mp")
    print("  python main.py list-products")
    print()
    
    # Executa o CLI
    cli = MiniparCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
