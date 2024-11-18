import requests
from fastapi import FastAPI
from interpreter.src.interpreter import Interpreter
from pydantic import BaseModel
from trees.syntax_tree import SyntaxNode
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InterpreterInput(BaseModel):
    code: str
    export: bool = False


@app.post("/interpret")
def interpret_code(input_data: InterpreterInput):
    # Solicita a árvore sintática ao microsserviço de árvore sintática
    print(input_data.code)

    try:

        test_text = """
        PAR{
            int i = 1;
            int resultado = 1;

            for(i = 1; i < 10; i = i+1){
                resultado = resultado * i;
            }

            print(resultado);
        }

        """

     
        reponse_lexical = requests.post(
            "http://localhost:8001/lex",
            json={"code": input_data.code},
        )

        if reponse_lexical.status_code != 200:
            return {
                "status": "error",
                "message": "Failed to obtain syntax tree from the service",
            }

        tokens = reponse_lexical.json()  # Obtemos o JSON com os dados da árvore

        parser_response = requests.post(
            "http://localhost:8004/parse",
            json=tokens,
        )

        # response = requests.get(
        #     "http://localhost:8002/get_syntax_tree"
        # )  # URL do microsserviço de árvore sintática   

        # if response.status_code != 200:
        #     return {
        #         "status": "error",
        #         "message": "Failed to obtain syntax tree from the service",
        #     }

        syntax_tree_data = (
            parser_response.json()
        )  # Obtemos o JSON com os dados da árvore

        if not syntax_tree_data:
            return {
                "status": "error",
                "message": "Received empty syntax tree from the service",
            }

        # Convertendo o JSON para a árvore sintática (agora via serviço)
        root = SyntaxNode.from_dict(syntax_tree_data["syntax_tree"])
    
        # Cria o interpretador com a árvore sintática obtida externamente
        interpreter = Interpreter(export=input_data.export, tree=root)

        # result = interpreter.run()
        # return {"status": "success", "output": result}

        try:
            result = interpreter.run()  
            return {"status": "success", "output": result}
        except Exception as e:
            return {"status": "error", "message": f"Error while interpreting: {str(e)}"}
    
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Failed to contact syntax tree service: {str(e)}",
        }
