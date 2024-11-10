# Variáveis
PYTHON = python3
UVICORN = uvicorn
INTERPRETER_PORT = 8000
LEXER_PORT = 8001
SEMANTIC_PORT = 8002
SYNTACTIC_PORT = 8004

# Inicializa o serviço do interpretador
run-interpreter:
	$(UVICORN) interpreter.main:app --host 0.0.0.0 --port $(INTERPRETER_PORT) --reload

# Inicializa o serviço do lexer
run-lexer:
	$(UVICORN) lexical.main:app --host 0.0.0.0 --port $(LEXER_PORT) --reload

# Inicializa o serviço do analisador semântico
run-semantic:
	$(UVICORN) semantic.main:app --host 0.0.0.0 --port $(SEMANTIC_PORT) --reload

# Inicializa o serviço do analisador sintático
run-syntactic:
	$(UVICORN) syntactic.main:app --host 0.0.0.0 --port $(SYNTACTIC_PORT) --reload

# Inicializa todos os serviços
run-all:
	@make run-interpreter &
	@make run-lexer &
	@make run-semantic &
	@make run-syntactic

# Instala as dependências
install:
	$(PYTHON) -m pip install -r requirements.txt