from common.tokens import TokenEnums as en
from fastapi import FastAPI
from pydantic import BaseModel
from syntactic.src.parser import Parser

app = FastAPI()

# Estrutura para armazenar a árvore sintática


class ParserInput(BaseModel):
    tokens: list[list]


@app.post("/parse")
def parse_code(input_data: ParserInput):
    def convert_to_enum(item):
        if isinstance(item[0], str):
            return [getattr(en, item[0]), item[1]]

        if isinstance(item[0], int):
            return [en(item[0]), item[1]]

        return item

    tokens = input_data.tokens

    tokens_mapped = [convert_to_enum(item) for item in tokens]

    parser = Parser(tokens_mapped)
    syntax_tree = parser.parse()
    return {"status": "success", "syntax_tree": syntax_tree.to_json()}
