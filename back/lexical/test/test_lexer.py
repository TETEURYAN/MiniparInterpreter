import unittest
import src.lexer as lx
from src.tokens import TokenEnums as en

class TestLexer(unittest.TestCase):

    def test_lexer(self):
        test_text = """
        int a = 10; # Comment
        if (a > 5) {
        print("Hello");
        par {
            a = a + 5;
            print("World");
        }
        } else {
        seq {
            print("World");
            print("!");
        }
        }
        """
        
        lexer = lx.LexerInterpreter(test_text)  # Inicializando o Lexer
        tokens = []
        
        # Pegando os tokens do lexer até o EOF
        token, value = lexer.get_next_token()
        while token != en.EOF:
            print(f"Token: {token}, Value: {value}")  # Adicione isso para ver o que está sendo retornado
            tokens.append((token, value))
            token, value = lexer.get_next_token()
        
        # Tokens esperados
        expected_tokens = [
            (en.RW_INT, "int"),
            (en.ID, "a"),
            (en.OP_ASSIGN, "="),
            (en.NUM, "10"),
            (en.DL_SEMICOLON, ";"),
            (en.RW_IF, "if"),
            (en.DL_LPAREN, "("),
            (en.ID, "a"),
            (en.OP_GT, ">"),
            (en.NUM, "5"),
            (en.DL_RPAREN, ")"),
            (en.DL_LBRACE, "{"),
            (en.RW_PRINT, "print"),
            (en.DL_LPAREN, "("),
            (en.STRING_LITERAL, "Hello"),
            (en.DL_RPAREN, ")"),
            (en.DL_SEMICOLON, ";"),
            (en.RW_PAR, "par"),
            (en.DL_LBRACE, "{"),
            (en.ID, "a"),
            (en.OP_ASSIGN, "="),
            (en.ID, "a"),
            (en.OP_PLUS, "+"),
            (en.NUM, "5"),
            (en.DL_SEMICOLON, ";"),
            (en.RW_PRINT, "print"),
            (en.DL_LPAREN, "("),
            (en.STRING_LITERAL, "World"),
            (en.DL_RPAREN, ")"),
            (en.DL_SEMICOLON, ";"),
            (en.DL_RBRACE, "}"),
            (en.DL_RBRACE, "}"),
            (en.RW_ELSE, "else"),
            (en.DL_LBRACE, "{"),
            (en.RW_SEQ, "seq"),
            (en.DL_LBRACE, "{"),
            (en.RW_PRINT, "print"),
            (en.DL_LPAREN, "("),
            (en.STRING_LITERAL, "World"),
            (en.DL_RPAREN, ")"),
            (en.DL_SEMICOLON, ";"),
            (en.RW_PRINT, "print"),
            (en.DL_LPAREN, "("),
            (en.STRING_LITERAL, "!"),
            (en.DL_RPAREN, ")"),
            (en.DL_SEMICOLON, ";"),
            (en.DL_RBRACE, "}"),
            (en.DL_RBRACE, "}"),
        ]
        
        # Verificando se os tokens gerados são iguais aos esperados
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()
