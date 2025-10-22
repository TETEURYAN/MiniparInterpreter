# Linha de Produto de Software para Compiladores Minipar

Esta linha de produto permite criar diferentes produtos de compilação para a linguagem Minipar, incluindo compiladores para diferentes arquiteturas, interpretadores e geradores de código intermediário.

## Arquitetura

A linha de produto segue uma arquitetura modular que pode ser implantada como monorepo com módulos ou como microserviços:

### Componentes

- **frontend**: Lexer + Parser + AST builder + Semantic Checker + SymbolTable
- **ir_generator**: Transforma AST em IR de 3 endereços (intermediate representation)
- **backends**: Gera Assembly a partir do IR (múltiplos backends por target)
- **interpreter**: Implementação que executa diretamente a AST
- **product_config**: Definição de produto (YAML/JSON) que liga frontend + escolhas de backend/interpreter
- **cli/builder**: Ferramenta única para construir produtos

### Fluxo de Dados

**Com backend (Compilador):**
```
source -> frontend -> AST -> ir_generator -> IR -> backend -> assembly
```

**Sem backend (Interpretador):**
```
source -> frontend -> AST -> interpreter -> execução
```

## Produtos Disponíveis

### Pontos de Variação Implementados

A linha de produto implementa dois pontos de variação principais:

#### Ponto de Variação 1 - Interface do Compilador
- **Terminal**: Interface de linha de comando tradicional
- **GUI**: Interface gráfica com janelas e botões

#### Ponto de Variação 2 - Geração de Código
- **Mostrar**: Exibe código de 3 endereços e assembly ARMv7
- **Ocultar**: Não mostra código gerado, apenas salva arquivos

### Produtos com Pontos de Variação

#### Compiladores com Interface Terminal
- `minipar_compiler_terminal`: Compilador com interface terminal
- `minipar_compiler_gui`: Compilador com interface gráfica

#### Compiladores com Controle de Exibição
- `minipar_compiler_show_code`: Mostra código de 3 endereços e assembly ARMv7
- `minipar_compiler_hide_code`: Não mostra código gerado

### Produtos Tradicionais (Compatibilidade)
- `minipar_compiler_x86_64`: Compilador para arquitetura x86_64
- `minipar_compiler_riscv`: Compilador para arquitetura RISC-V
- `minipar_interpreter`: Interpretador que executa AST diretamente
- `minipar_ir_generator`: Gera código intermediário de 3 endereços

## Uso

### CLI Principal

```bash
# Listar produtos disponíveis
python main.py list-products

# Compilar para x86_64
python main.py build --product minipar_compiler_x86_64 input.mp

# Interpretar
python main.py build --product minipar_interpreter input.mp

# Usar configuração customizada
python main.py build --config config.yaml input.mp

# Criar arquivo de configuração
python main.py create-config --product minipar_compiler_x86_64 --output config.yaml
```

### Usando Pontos de Variação

#### Ponto de Variação 1 - Interface do Compilador

```bash
# Interface Terminal
python main.py build --product minipar_compiler_terminal input.mp

# Interface Gráfica (requer tkinter)
python main.py build --product minipar_compiler_gui input.mp
```

#### Ponto de Variação 2 - Geração de Código

```bash
# Mostrar código de 3 endereços e assembly ARMv7
python main.py build --product minipar_compiler_show_code input.mp

# Não mostrar código gerado
python main.py build --product minipar_compiler_hide_code input.mp
```

### Exemplo de Configuração YAML

```yaml
name: minipar_compiler_x86_64
product_type: compiler
description: Compilador Minipar para arquitetura x86_64
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

output_file: output.s
verbose: false
debug: false
```

## Estrutura do Projeto

```
compiler_product_line/
├── interfaces/           # Interfaces e contratos
│   ├── ast.py           # Interface da AST
│   ├── ir.py            # Interface do IR
│   └── symbol_table.py  # Interface da tabela de símbolos
├── frontend/            # Frontend completo
│   ├── ast_impl.py      # Implementação da AST
│   ├── lexer_impl.py    # Implementação do lexer
│   ├── parser_impl.py   # Implementação do parser
│   └── semantic_impl.py # Implementação do analisador semântico
├── ir_generator/        # Gerador de código intermediário
│   └── ir_generator_impl.py
├── backends/            # Backends para diferentes arquiteturas
│   ├── x86_64_backend.py
│   └── riscv_backend.py
├── interpreter/         # Interpretadores
│   └── ast_interpreter.py
├── product_config/      # Configuração de produtos
│   ├── product_config.py
│   └── config_loader.py
├── cli/                 # Interface de linha de comando
│   ├── builder.py
│   └── cli.py
├── examples/            # Exemplos de configuração
└── main.py             # Arquivo principal
```

## Características

### Frontend
- Análise léxica completa
- Análise sintática com construção de AST
- Análise semântica com verificação de tipos
- Tabela de símbolos compartilhada

### Geração de IR
- Código de 3 endereços
- Otimizações (dobramento de constantes, janela deslizante)
- Serialização JSON

### Backends
- x86_64: Assembly para arquitetura x86_64
- RISC-V: Assembly para arquitetura RISC-V
- Alocação de registradores
- Gerenciamento de memória

### Interpretador
- Execução direta da AST
- Modo debug
- Rastreamento de execução

## Dependências

- Python 3.8+
- PyYAML (para configurações YAML)
- json (biblioteca padrão)

## Instalação

```bash
# Instalar dependências
pip install PyYAML

# Executar
python main.py --help
```

## Exemplos de Uso

### Compilação para x86_64

```bash
python main.py build --product minipar_compiler_x86_64 input.mp --output output.s
```

### Interpretação

```bash
python main.py build --product minipar_interpreter input.mp
```

### Geração de IR

```bash
python main.py build --product minipar_ir_generator input.mp --output output.ir
```

## Contribuição

Para contribuir com a linha de produto:

1. Implemente novas interfaces seguindo os contratos definidos
2. Adicione novos backends para outras arquiteturas
3. Implemente novas otimizações de IR
4. Adicione novos tipos de produtos

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
