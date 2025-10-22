"""
Linha de Produto de Software para Compiladores Minipar

Esta linha de produto permite criar diferentes produtos de compilação:
- Compiladores com backends específicos (x86_64, RISC-V, etc.)
- Interpretadores
- Geradores de código intermediário (IR)

Arquitetura modular:
- frontend: Lexer + Parser + AST + Semantic Checker
- ir_generator: Geração de código intermediário de 3 endereços
- backends: Geração de Assembly para diferentes targets
- interpreter: Execução direta da AST
- product_config: Configuração de produtos
- cli: Ferramenta de construção
"""

__version__ = "1.0.0"
__author__ = "Minipar Compiler Product Line Team"
