# 🛠️ MiniparAnalyzer - Analisador Semântico

Este documento descreve o **analisador semântico** do projeto **MiniparAnalyzer**, responsável por verificar a semântica do código-fonte, garantindo que as regras da linguagem sejam respeitadas.

## 📋 Visão Geral

A análise semântica ocorre após a análise sintática e verifica a correção lógica do código, como:

- Declaração e uso correto de variáveis.
- Tipagem adequada em expressões.
- Verificação de escopo e visibilidade de identificadores.
- Detecção de construções inválidas.

## 📦 Estrutura de Arquivos

O analisador semântico é implementado em `semantic_analyzer.py` e faz uso de classes auxiliares para a tabela de símbolos e para a verificação de tipos.

### Dependências

- **common.tokens**: Enumeração de tokens, utilizada para identificação de tipos.
- **trees.syntax_tree**: Define a estrutura da árvore sintática abstrata.
- **contextlib**: Usado para redirecionamento de saída.

## 🚀 Funcionalidades

### 1. **Análise Semântica**

O analisador semântico percorre a árvore sintática abstrata (AST) e realiza as seguintes verificações:

- **Declaração de Variáveis**: Garante que todas as variáveis sejam declaradas antes do uso.
- **Verificação de Tipos**: Confirma que as operações aritméticas e lógicas sejam realizadas entre operandos do mesmo tipo.
- **Verificação de Escopo**: Garante que variáveis locais e globais sejam usadas de forma correta, respeitando o escopo.

### 2. **Tabela de Símbolos**

Utiliza uma **tabela de símbolos** para armazenar informações sobre variáveis, como tipo e escopo. A tabela de símbolos é atualizada durante a análise e auxilia na verificação de erros.

### 3. **Tratamento de Erros Semânticos**

O analisador levanta exceções quando encontra erros semânticos, como uso de variável não declarada ou incompatibilidade de tipos.

## 📜 Classe e Métodos

### `SemanticAnalyzer`

A classe principal do analisador semântico.

#### **Métodos:**

- `__init__(self)`: Inicializa o analisador e a tabela de símbolos.
- `visit(node: SyntaxNode)`: Percorre a árvore sintática abstrata e realiza a análise semântica de cada nó.
- `check_declaration(identifier)`: Verifica se um identificador foi declarado.
- `check_type(expression)`: Verifica a compatibilidade de tipos em expressões.
- `enter_scope()`: Cria um novo escopo na tabela de símbolos.
- `exit_scope()`: Remove o escopo atual da tabela de símbolos.

## 📝 Exemplo de Uso

```python
from semantic_analyzer import SemanticAnalyzer
from syntactic.src.parser import Parser
from common.tokens import TokenEnums
from trees.syntax_tree import SyntaxNode

# Código-fonte para análise
code = """
int x = 5;
int y = 10;
x = y + 2;
print(x);
"""

# Parsing para obter a árvore sintática
parser = Parser(code)
syntax_tree = parser.parse()

# Inicializa o analisador semântico
analyzer = SemanticAnalyzer()

# Executa a análise semântica
try:
    analyzer.visit(syntax_tree)
    print("Análise semântica concluída com sucesso!")
except Exception as e:
    print(f"Erro semântico: {e}")
