from common.tokens import TokenEnums
from lexical.src.dictionary import WordDict


class LexerInterpreter:

    # Inicializa o objeto Lexer com o texto fornecido.
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    # Avança para o próximo caractere no texto.
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    # Pula os caracteres de espaço em branco.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Analisa um identificador ou palavra-chave.
    def parse_id_or_keyword(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):

            result += self.current_char
            self.advance()

        if result.lower() in WordDict.words:
            return WordDict.words[result.lower()], result
        else:
            return TokenEnums.ID, result

    # Obtém o próximo token do texto.
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                return self.parse_id_or_keyword()

            if self.current_char.isdigit():
                num_str = ""
                while self.current_char is not None and self.current_char.isdigit():
                    num_str += self.current_char
                    self.advance()
                return TokenEnums.NUM, int(num_str)

            char = self.current_char

            if char == "=":
                if self.text[self.pos + 1] == "=":
                    self.advance()
                    self.advance()
                    return TokenEnums.OP_EQ, "=="
                else:
                    self.advance()
                    return TokenEnums.OP_ASSIGN, char
            if char == "<":
                if self.text[self.pos + 1] == "=":
                    self.advance()
                    self.advance()
                    return TokenEnums.OP_LE, "<="
                else:
                    self.advance()
                    return TokenEnums.OP_LT, char
            if char == ">":
                if self.text[self.pos + 1] == "=":
                    self.advance()
                    self.advance()
                    return TokenEnums.OP_GE, ">="
                else:
                    self.advance()
                    return TokenEnums.OP_GT, char
            if char == "!":
                if self.text[self.pos + 1] == "=":
                    self.advance()
                    self.advance()
                    return TokenEnums.OP_NE, "!="
                else:
                    self.advance()
                    return TokenEnums.OP_NOT, char
            if char == '"':
                string_value = ""
                self.advance()
                while self.current_char is not None and self.current_char != '"':
                    string_value += self.current_char
                    self.advance()
                self.advance()
                return TokenEnums.STRING_LITERAL, string_value

            if char == "{":
                self.advance()
                return TokenEnums.DL_LBRACE, char
            elif char == "}":
                self.advance()
                return TokenEnums.DL_RBRACE, char
            elif char == "(":
                self.advance()
                return TokenEnums.DL_LPAREN, char
            elif char == ")":
                self.advance()
                return TokenEnums.DL_RPAREN, char
            elif char == ",":
                self.advance()
                return TokenEnums.DL_COMMA, char
            elif char in WordDict.symbols:
                self.advance()
                return WordDict.symbols[char], char
            elif char == "#":
                while self.current_char is not None and self.current_char != "\n":
                    self.advance()
                continue

        return TokenEnums.EOF, None
