# 🛠️ MiniparLexer - Analisador Léxico

Este documento descreve o **analisador léxico** do projeto **MiniparLexer**, que é responsável por transformar o código-fonte em uma sequência de tokens, facilitando o processo de parsing e interpretação.

## 📋 Visão Geral

O analisador léxico é o primeiro estágio de um compilador ou interpretador. Ele recebe como entrada o código-fonte e realiza a análise léxica, identificando padrões e convertendo-os em tokens. Esses tokens são então utilizados pelos módulos de análise sintática e semântica.

## 📦 Estrutura de Arquivos

O analisador léxico é implementado em `lexer.py` e utiliza a enumeração de tokens definida em `common.tokens`.

### Dependências

- **common.tokens**: Define os tipos de tokens reconhecidos pelo analisador léxico.
- **re**: Biblioteca de expressões regulares para a correspondência de padrões léxicos.

## 🚀 Funcionalidades

### 1. **Análise Léxica**

O analisador utiliza expressões regulares para identificar e extrair tokens do código-fonte. Os principais tipos de tokens reconhecidos são:

- **Palavras-chave**: `int`, `for`, `if`, `while`, `print`, etc.
- **Identificadores**: Variáveis e nomes de funções.
- **Literais**: Números inteiros e strings.
- **Operadores**: `+`, `-`, `*`, `/`, `=`, `==`, etc.
- **Delimitadores**: Parênteses, chaves e ponto e vírgula.

### 2. **Tratamento de Erros Léxicos**

O analisador identifica caracteres desconhecidos e levanta exceções, informando a posição e o caractere inválido.

### 3. **Geração de Tokens**

Os tokens são representados como instâncias de uma classe `Token`, contendo informações como tipo, valor e posição no código.

## 📜 Classe e Métodos

### `Lexer`

A classe principal do analisador léxico.

#### **Métodos:**

- `__init__(self, code: str)`: Inicializa o analisador léxico com o código-fonte.
- `tokenize()`: Percorre o código-fonte e gera a lista de tokens.
- `next_token()`: Retorna o próximo token da sequência.
- `peek()`: Permite visualizar o próximo token sem consumi-lo.
- `raise_error(position, char)`: Levanta um erro léxico ao encontrar um caractere inválido.

## 📝 Exemplo de Uso

```python
from lexer import Lexer

# Código-fonte a ser analisado
code = """
int x = 10;
for (int i = 0; i < x; i = i + 1) {
    print(i);
}
"""

    