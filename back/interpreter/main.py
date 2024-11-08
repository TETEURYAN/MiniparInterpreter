from fastapi import FastAPI
from pydantic import BaseModel
from interpreter.interpreter import Interpreter
from syntax_tree import SyntaxNode
import requests

app = FastAPI()

class InterpreterInput(BaseModel):
    export: bool = False

@app.post("/interpret")
def interpret_code(input_data: InterpreterInput):
    # Solicita a árvore sintática ao microsserviço de árvore sintática
    try:
        response = requests.get("http://localhost:8002/get_syntax_tree")  # URL do microsserviço de árvore sintática

        if response.status_code != 200:
            return {"status": "error", "message": "Failed to obtain syntax tree from the service"}

        syntax_tree_data = response.json()  # Obtemos o JSON com os dados da árvore

        if not syntax_tree_data:
            return {"status": "error", "message": "Received empty syntax tree from the service"}

        # Convertendo o JSON para a árvore sintática (agora via serviço)
        root = SyntaxNode.from_dict(syntax_tree_data)

        # Cria o interpretador com a árvore sintática obtida externamente
        interpreter = Interpreter(export=input_data.export, tree=root)

        try:
            result = interpreter.run()
            return {"status": "success", "output": result}
        except Exception as e:
            return {"status": "error", "message": f"Error while interpreting: {str(e)}"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to contact syntax tree service: {str(e)}"}
