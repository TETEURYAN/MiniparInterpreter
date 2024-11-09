from common.tokens import TokenEnums
from fastapi import FastAPI, HTTPException
from lexical.src.lexer import LexerInterpreter
from pydantic import BaseModel

app = FastAPI()


class CodeInput(BaseModel):
    code: str


@app.post("/lex")
def lex_code(input_data: CodeInput):
    try:
        lexer = LexerInterpreter(input_data.code)
        tokens = []
        token = lexer.get_next_token()

        # Processa tokens até encontrar o "EOF"
        while token[0] != TokenEnums.EOF:
            tokens.append(token)
            token = lexer.get_next_token()

        return {"tokens": tokens}

    except Exception as e:
        # Se houver algum erro durante o processo de lexing, retorna uma mensagem de erro
        raise HTTPException(status_code=400, detail=f"Error during lexing: {str(e)}")
