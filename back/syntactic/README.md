# 🛠️ MiniparAnalyzer - Analisador Sintático

Este documento descreve o **analisador sintático** do projeto **MiniparAnalyzer**, responsável por verificar a estrutura gramatical do código-fonte e gerar a árvore de sintaxe abstrata (AST).

## 📋 Visão Geral

O analisador sintático (Parser) analisa o código-fonte após a análise léxica, verificando a conformidade com as regras gramaticais definidas para a linguagem. Ele gera a **árvore de sintaxe abstrata (AST)**, uma representação hierárquica do programa que será utilizada pelo analisador semântico e pelo interpretador.

## 📦 Estrutura de Arquivos

O analisador sintático é implementado em `parser.py` e depende da seguinte estrutura de arquivos:

- **common.tokens**: Enumeração de tokens identificados durante a análise léxica.
- **trees.syntax_tree**: Define a estrutura da árvore sintática abstrata (AST).

### Dependências

- **Enumerações de Tokens**: Utilizadas para identificar os tipos de tokens recebidos.
- **Árvore Sintática**: Estrutura para armazenar os nós da AST.

## 🚀 Funcionalidades

### 1. **Análise Sintática**

O parser valida a sequência de tokens e verifica se o código está de acordo com as regras gramaticais da linguagem. Ele constrói a árvore sintática abstrata (AST) durante o processo.

### 2. **Construção da Árvore Sintática (AST)**

A árvore sintática representa a estrutura do programa e contém os seguintes nós:

- **Declarações**: Declaração de variáveis, funções, etc.
- **Expressões**: Operações aritméticas e lógicas.
- **Blocos de Código**: Estruturas de controle, como `if`, `while`, e `for`.

### 3. **Tratamento de Erros Sintáticos**

O parser detecta e reporta erros sintáticos, como:

- Parênteses não balanceados.
- Estruturas de controle malformadas.
- Instruções incompletas.

## 📜 Classe e Métodos

### `Parser`

A classe principal do analisador sintático.

#### **Métodos:**

- `__init__(self, tokens)`: Inicializa o parser com uma lista de tokens.
- `parse()`: Inicia o processo de análise sintática e retorna a árvore sintática abstrata (AST).
- `parse_statement()`: Analisa declarações e instruções.
- `parse_expression()`: Analisa expressões aritméticas e lógicas.
- `parse_block()`: Analisa blocos de código (como loops e condicionais).
- `match(token_type)`: Verifica se o próximo token é do tipo esperado.

## 📝 Exemplo de Uso

```python
from syntactic.src.parser import Parser
from lexical.src.lexer import Lexer
from common.tokens import TokenEnums

# Código-fonte para análise
code = """
int x = 5;
int y = 10;
if (x < y) {
    print("x é menor que y");
}
"""

# Realiza a análise léxica para obter os tokens
lexer = Lexer(code)
tokens = lexer.tokenize()

# Inicializa o parser com os tokens
parser = Parser(tokens)

# Executa a análise sintática
try:
    syntax_tree = parser.parse()
    syntax_tree.print_tree()  # Imprime a árvore sintática abstrata
except Exception as e:
    print(f"Erro sintático: {e}")
