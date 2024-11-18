# 🖥️ MiniparInterpreter - Interpretador

Este documento descreve o **interpretador** do projeto **MiniparInterpreter**, responsável por executar código em uma linguagem específica utilizando uma árvore sintática abstrata (AST).

## 📋 Visão Geral

O interpretador recebe como entrada uma árvore sintática abstrata (AST) gerada durante o processo de parsing e executa o código contido nela. Ele realiza a análise semântica e a execução, suportando funcionalidades como:

- Execução sequencial e paralela de código.
- Exportação da AST para um arquivo JSON.
- Execução de expressões matemáticas.
- Comunicação via socket para execução remota.

## 🛠️ Funcionalidades Principais

### 1. **Execução de Código**

O interpretador percorre a árvore sintática, executando as instruções contidas nela. Ele usa a função `exec()` para a execução dinâmica do código Python gerado a partir da árvore.

### 2. **Análise Semântica**

Utiliza o módulo `SemanticAnalyzer` para validar e analisar a árvore sintática antes da execução. Isso garante que o código seja semanticamente válido.

### 3. **Exportação da AST**

Se o parâmetro `export` for definido como `True`, a árvore sintática abstrata é exportada para um arquivo JSON, facilitando o debug e a análise da estrutura do código.

### 4. **Execução Concorrente**

Suporte para execução paralela de blocos de código utilizando threading, permitindo a execução simultânea de diferentes trechos de código.

## 📦 Estrutura de Arquivo

O arquivo principal é `interpreter.py` e ele depende dos seguintes módulos:

- `common.tokens`: Define os tokens da linguagem.
- `semantic.src.semantic_analyzer`: Analisador semântico.
- `syntactic.src.parser`: Parser para gerar a AST.
- `trees.syntax_tree`: Define a estrutura da árvore sintática.

## 📜 Classe e Métodos

### `Interpreter`

A classe principal que executa o código.

#### **Métodos:**

- `__init__(self, tree: SyntaxNode | None = None, export=False)`: Inicializa o interpretador com a árvore sintática e a opção de exportação.
- `run()`: Executa o código representado pela árvore sintática.
- `save_tree()`: Exporta a árvore sintática para um arquivo JSON (`tree.json`).

### Funções Auxiliares

- `_calculate(num1, operator, num2)`: Realiza cálculos aritméticos básicos (`+`, `-`, `*`, `/`).
- `c_channel(host, type)`: Implementa um canal de comunicação cliente-servidor usando sockets.
- `par_block(block)`: Executa um bloco de código em paralelo usando threading.
- `seq_block()`: Placeholder para execução sequencial.

## 🌐 Comunicação via Socket

O interpretador permite a execução remota de procedimentos através de um canal de comunicação socket.


