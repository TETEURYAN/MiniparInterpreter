from lexical.src.tokens import TokenEnums as en


class WordDict:
    # Palavras
    words = {
        "seq": en.RW_SEQ,
        "par": en.RW_PAR,
        "if": en.RW_IF,
        "else": en.RW_ELSE,
        "while": en.RW_WHILE,
        "chan": en.RW_CHAN,
        "int": en.RW_INT,
        "bool": en.RW_BOOL,
        "string": en.RW_STRING,
        "c_channel": en.RW_C_CHANNEL,
        "true": en.RW_TRUE,
        "false": en.RW_FALSE,
        "null": en.RW_NULL,
        "print": en.RW_PRINT,
        "input": en.RW_INPUT,
        "for": en.RW_FOR,
        "return": en.RW_RETURN,
    }
    # Símbolos
    symbols = {
        "=": en.OP_ASSIGN,
        "+": en.OP_PLUS,
        "-": en.OP_MINUS,
        "*": en.OP_MULTIPLY,
        "/": en.OP_DIVIDE,
        "(": en.DL_LPAREN,
        ")": en.DL_RPAREN,
        ";": en.DL_SEMICOLON,
        "{": en.DL_LBRACE,
        "}": en.DL_RBRACE,
        ",": en.DL_COMMA,
        ".": en.DL_DOT,
        "[": en.DL_LBRACKET,
        "]": en.DL_RBRACKET,
        "&&": en.OP_AND,
        "||": en.OP_OR,
        "!": en.OP_NOT,
        "==": en.OP_EQ,
        "!=": en.OP_NE,
        "<": en.OP_LT,
        "<=": en.OP_LE,
        ">": en.OP_GT,
        ">=": en.OP_GE,
        "++": en.OP_INC,
        "--": en.OP_DEC,
        "+=": en.OP_PLUS_ASSIGN,
        "-=": en.OP_MINUS_ASSIGN,
    }
