
# 🏗️ Arquitetura do Projeto - MiniparAnalyzer

Este documento descreve a **arquitetura do projeto MiniparAnalyzer**, os padrões de projeto adotados, e as rotas da API. O objetivo é fornecer uma visão geral sobre a estrutura do sistema e como os diferentes componentes se interagem.

## 📋 Visão Geral

O **MiniparAnalyzer** é um sistema de análise de código-fonte, composto por diversos microsserviços especializados. Cada microsserviço tem um papel distinto, como análise léxica, sintática e semântica, além de um interpretador responsável pela execução do código.

### Componentes principais:
- **Backend**: Responsável pela lógica de análise e execução. Inclui a análise léxica, sintática, semântica e execução do código (interpretador).
- **Frontend**: Interface de usuário que permite ao usuário enviar código e receber os resultados das análises.
  
O sistema segue uma arquitetura modular, com a comunicação entre os módulos baseada em **APIs RESTful** e **microservices**.

## 🏗️ Arquitetura do Sistema

### 1. **Padrões de Projeto**

O projeto adota alguns padrões de projeto para garantir uma boa escalabilidade, reutilização e manutenção do código. Aqui estão os principais:

#### **Arquitetura Baseada em Microservices**

- Cada serviço (como análise léxica, sintática e semântica) é desenvolvido de forma independente e interage com outros serviços via APIs.
- Isso permite que os serviços sejam escaláveis e facilmente substituíveis, além de facilitar a manutenção e a distribuição da carga de trabalho.

#### **Padrão de Injeção de Dependências (Dependency Injection)**

- Utilizado para permitir que cada componente do sistema (como o analisador sintático, semântico e o interpretador) seja configurado de forma flexível sem acoplamento excessivo.

#### **Padrão de Projeto Factory (Factory Pattern)**

- O **Factory Pattern** é utilizado para criar instâncias de classes (como o Parser, Interpreter e SemanticAnalyzer) sem expor diretamente sua implementação, proporcionando flexibilidade e modularidade.

#### **Padrão de Projeto Strategy**

- O **Strategy Pattern** é utilizado na análise semântica e no interpretador, permitindo a escolha dinâmica de diferentes estratégias de execução de código ou de verificação semântica.

### 2. **Divisão de Camadas**

A arquitetura é dividida em camadas, com cada camada tendo uma responsabilidade clara:

- **Frontend**: Interface de comunicação com o usuário (em React ou similar).
- **Backend**: Contém os microsserviços de análise léxica, sintática, semântica e o interpretador.
- **Microsserviços**:
  - **Léxico**: Analisa o código e gera os tokens.
  - **Sintático**: Constrói a árvore de sintaxe abstrata (AST) a partir dos tokens.
  - **Semântico**: Realiza a análise semântica para verificar a consistência do código.
  - **Interpretador**: Executa o código, gerando a saída com base na AST.

## 🖧 Comunicação entre os Componentes

A comunicação entre os serviços é realizada via chamadas HTTP usando a biblioteca **requests** e **FastAPI** para expor as APIs.

### **Fluxo de Execução**

1. O **frontend** envia o código para o **backend** via API.
2. O **backend** chama os microsserviços:
   - **Analisador Léxico**: Realiza a análise léxica e envia os tokens para o analisador sintático.
   - **Analisador Sintático**: Verifica a conformidade do código com a gramática e gera a árvore sintática.
   - **Analisador Semântico**: Verifica a consistência do código (tipos, variáveis, etc.).
   - **Interpretador**: Executa o código e retorna o resultado para o frontend.

## 🗂️ Estrutura de Diretórios

A estrutura de diretórios segue um padrão modular, com as responsabilidades bem definidas:

```plaintext
MiniparInterpreter/
├── back/                    # Backend (API e lógica do interpretador)
│   ├── interpreter/
│   │   └── src/interpreter.py     
│   ├── interpreter.py       # Implementação do interpretador
│   ├── main.py              # Endpoints da API (FastAPI)
│   ├── common/
│   │   └── tokens.py        # Definições de tokens
│   ├── semantic/
│   │   └── src/semantic_analyzer.py
│   ├── syntactic/
│   │   └── src/parser.py    # Analisador sintático
│   ├── trees/
│   │   └── syntax_tree.py   # Implementação da árvore sintática
│   └── requirements.txt     # Dependências do backend
└── front/                   # Frontend (Interface com o usuário)
```


- **back/src/lexical**: Implementação do analisador léxico.
- **back/src/syntactic**: Implementação do analisador sintático.
- **back/src/semantic**: Implementação do analisador semântico.
- **back/src/interpreter**: Implementação do interpretador.
- **back/src/app.py**: Ponto de entrada para a API, que conecta todos os microsserviços.

## 📡 Rotas da API

As rotas da API estão organizadas para corresponder às funcionalidades dos microsserviços. A seguir, estão as principais rotas do sistema.

### **Rotas de Analisadores**

#### 1. **Analisador Léxico** - `/lex`

- **Método**: `POST`
- **Descrição**: Recebe o código-fonte e retorna os tokens gerados pela análise léxica.
- **Corpo da requisição**:
  ```json
  {
    "code": "int x = 5; if(x > 3) { print(x); }"
  }
  ```

### 2. **Analisador Sintático** - `/parse`

- **Método**: `POST`
- **Descrição**: Recebe os tokens e retorna a árvore sintática (AST).
- **Corpo da requisição**:
  ```json
  
  "syntax_tree": {
    "type": "Program",
    "children": [
      {"type": "Declaration", "name": "x", "value": 5},
      {"type": "IfStatement", "condition": "x > 3", "body": [...]},
      {"type": "PrintStatement", "value": "x"}
    ]
  }
```

#### 3. **Analisador Semântico** - `/semantic`

- **Método**: `POST`
- **Descrição**: Realiza a verificação semântica do código.
- **Corpo da requisição**:
  ```json
  {
  "syntax_tree": { ... }
  }

  ```

  #### 3. **Interpretator** - `/interpret`

- **Método**: `POST`
- **Descrição**: Realiza a execução do código.
- **Corpo da requisição**:
  ```json
  {
  "code": "int x = 5; if(x > 3) { print(x); }"
  }

  ```