from fastapi import FastAPI
from pydantic import BaseModel
from parser import Parser
from enum_tokens import TokenEnums as en

app = FastAPI()

# Estrutura para armazenar a árvore sintática
syntax_tree = None

class ParserInput(BaseModel):
    tokens: list

@app.post("/parse")
def parse_code(input_data: ParserInput):
    global syntax_tree
    parser = Parser(input_data.tokens)
    syntax_tree = parser.parse()
    return {"status": "success", "syntax_tree": syntax_tree.to_json()}

@app.get("/get_syntax_tree")
def get_syntax_tree():
    if syntax_tree is None:
        return {"status": "error", "message": "No syntax tree available"}
    return {"status": "success", "syntax_tree": syntax_tree.to_json()}
