#!/usr/bin/env python3
"""
Exemplo de uso dos pontos de variação da linha de produto de compiladores.

Este script demonstra como usar os diferentes pontos de variação:
- Ponto de Variação 1: Interface do Compilador (Terminal vs GUI)
- Ponto de Variação 2: Geração de Código (Mostrar vs Ocultar)
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent))

from cli.builder import ProductBuilder
from product_config.product_config import PREDEFINED_PRODUCTS


def demonstrate_variation_points():
    """Demonstra os pontos de variação implementados."""
    
    print("=" * 80)
    print("    DEMONSTRAÇÃO DOS PONTOS DE VARIAÇÃO - LINHA DE PRODUTO MINIPAR")
    print("=" * 80)
    print()
    
    # Arquivo de exemplo para compilação
    example_file = "examples/example.mp"
    
    # Lista os produtos disponíveis com pontos de variação
    variation_products = [
        "minipar_compiler_terminal",
        "minipar_compiler_gui", 
        "minipar_compiler_show_code",
        "minipar_compiler_hide_code"
    ]
    
    print("PRODUTOS COM PONTOS DE VARIAÇÃO DISPONÍVEIS:")
    print("-" * 50)
    
    for product_name in variation_products:
        if product_name in PREDEFINED_PRODUCTS:
            config = PREDEFINED_PRODUCTS[product_name]
            print(f"📦 {product_name}")
            print(f"   Descrição: {config.description}")
            print(f"   Interface: {config.interface_type.value}")
            print(f"   Exibição de Código: {config.code_display_mode.value}")
            if config.backend:
                print(f"   Backend: {config.backend.backend_type.value}")
            print()
    
    print("=" * 80)
    print("EXEMPLO DE USO:")
    print("=" * 80)
    print()
    
    # Exemplo 1: Compilador com Interface Terminal
    print("🔹 EXEMPLO 1: Compilador com Interface Terminal")
    print("-" * 50)
    try:
        config = PREDEFINED_PRODUCTS["minipar_compiler_terminal"]
        builder = ProductBuilder(config)
        
        print("Configuração:")
        print(f"  - Interface: {config.interface_type.value}")
        print(f"  - Exibição de Código: {config.code_display_mode.value}")
        print(f"  - Backend: {config.backend.backend_type.value}")
        print()
        
        # Simula compilação (sem arquivo real)
        print("Simulando compilação...")
        print("✅ Produto configurado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    
    # Exemplo 2: Compilador com Interface GUI
    print("🔹 EXEMPLO 2: Compilador com Interface Gráfica")
    print("-" * 50)
    try:
        config = PREDEFINED_PRODUCTS["minipar_compiler_gui"]
        builder = ProductBuilder(config)
        
        print("Configuração:")
        print(f"  - Interface: {config.interface_type.value}")
        print(f"  - Exibição de Código: {config.code_display_mode.value}")
        print(f"  - Backend: {config.backend.backend_type.value}")
        print()
        
        print("Simulando compilação...")
        print("✅ Produto configurado com sucesso!")
        print("ℹ️  Nota: Interface GUI requer tkinter instalado")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    
    # Exemplo 3: Compilador que mostra código
    print("🔹 EXEMPLO 3: Compilador que mostra código de 3 endereços e assembly ARMv7")
    print("-" * 50)
    try:
        config = PREDEFINED_PRODUCTS["minipar_compiler_show_code"]
        builder = ProductBuilder(config)
        
        print("Configuração:")
        print(f"  - Interface: {config.interface_type.value}")
        print(f"  - Exibição de Código: {config.code_display_mode.value}")
        print(f"  - Backend: {config.backend.backend_type.value}")
        print(f"  - Arquitetura: {config.backend.target_arch}")
        print()
        
        print("Simulando compilação...")
        print("✅ Produto configurado com sucesso!")
        print("ℹ️  Este produto mostrará:")
        print("   - Código intermediário (3 endereços)")
        print("   - Código assembly ARMv7 para CPUlator")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    
    # Exemplo 4: Compilador que oculta código
    print("🔹 EXEMPLO 4: Compilador que não mostra código gerado")
    print("-" * 50)
    try:
        config = PREDEFINED_PRODUCTS["minipar_compiler_hide_code"]
        builder = ProductBuilder(config)
        
        print("Configuração:")
        print(f"  - Interface: {config.interface_type.value}")
        print(f"  - Exibição de Código: {config.code_display_mode.value}")
        print(f"  - Backend: {config.backend.backend_type.value}")
        print()
        
        print("Simulando compilação...")
        print("✅ Produto configurado com sucesso!")
        print("ℹ️  Este produto ocultará:")
        print("   - Código intermediário")
        print("   - Código assembly")
        print("   - Apenas salvará o arquivo de saída")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print()
    print("=" * 80)
    print("COMO USAR:")
    print("=" * 80)
    print()
    print("Para usar os pontos de variação, execute:")
    print()
    print("  # Interface Terminal")
    print("  python main.py build --product minipar_compiler_terminal input.mp")
    print()
    print("  # Interface Gráfica")
    print("  python main.py build --product minipar_compiler_gui input.mp")
    print()
    print("  # Mostrar código de 3 endereços e assembly ARMv7")
    print("  python main.py build --product minipar_compiler_show_code input.mp")
    print()
    print("  # Não mostrar código gerado")
    print("  python main.py build --product minipar_compiler_hide_code input.mp")
    print()
    print("=" * 80)


if __name__ == '__main__':
    demonstrate_variation_points()
