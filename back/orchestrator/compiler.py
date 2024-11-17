import requests

def compile_code(code: str, export: bool):
    # 1. Chama o serviço de análise léxica
    lexical_response = requests.post(
        "http://localhost:8001/lex",
        json={"code": code},
    )
    if lexical_response.status_code != 200:
        raise Exception("Erro ao obter tokens do serviço léxico")

    tokens = lexical_response.json()["tokens"]

    # 2. Chama o serviço de análise sintática
    syntactic_response = requests.post(
        "http://localhost:8004/parse",
        json={"tokens": tokens},
    )

    print("TOKENS: ", tokens)
    if syntactic_response.status_code != 200:
        raise Exception("Erro ao obter a árvore sintática do serviço sintático")

    syntax_tree = syntactic_response.json()["syntax_tree"]

    print("ÁRVORE SINTÁTIVA: ", syntax_tree)

    # 3. Chama o serviço de análise semântica
    semantic_response = requests.post(
        "http://localhost:8002/semantic",
        json={"syntax_tree": syntax_tree},
    )

    print("ANÁLISE SEMÂNTICA: ", semantic_response  )
    if semantic_response.status_code != 200:
        raise Exception("Erro na análise semântica")

    semantic_result = semantic_response.json()
    if semantic_result["status"] == "error":
        raise Exception(f"Erros semânticos: {semantic_result['errors']}")

    # 4. Chama o interpretador
    interpreter_response = requests.post(
        "http://localhost:8000/interpret",
        json={"export": export, "syntax_tree": syntax_tree},
    )
    if interpreter_response.status_code != 200:
        raise Exception("Erro ao executar o interpretador")

    result = interpreter_response.json()["output"]
    return result
