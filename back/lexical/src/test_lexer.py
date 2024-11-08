import unittest
import lexer as lx
from tokens import TokenEnums

class TestLexer(unittest.TestCase):

    def test_lexer(self):
        test_text = """
        x = 10
        if x == 10:
            print("x é igual a 10")
        """
        
        lexer =  lx.LexerInterpreter(test_text)
        tokens = []
        token, value = lexer.get_next_token()
        
        while token != TokenEnums.EOF:
            tokens.append((token, value))
            token, value = lexer.get_next_token()
        
        expected_tokens = [
            (TokenEnums.ID, 'x'),
            (TokenEnums.OP_ASSIGN, '='),
            (TokenEnums.NUM, 10),
            (TokenEnums.ID, 'if'),
            (TokenEnums.ID, 'x'),
            (TokenEnums.OP_EQ, '=='),
            (TokenEnums.NUM, 10),
            (TokenEnums.DL_COLON, ':'),
            (TokenEnums.ID, 'print'),
            (TokenEnums.DL_LPAREN, '('),
            (TokenEnums.STRING_LITERAL, 'x é igual a 10'),
            (TokenEnums.DL_RPAREN, ')'),
            (TokenEnums.EOF, None)
        ]
        
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()
