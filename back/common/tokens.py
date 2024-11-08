from enum import Enum

class TokenEnums(Enum):
    # Palavras Reservadas - Tipos
    RW_INT = 1
    RW_BOOL = 2
    RW_STRING = 3
    RW_C_CHANNEL = 4
    RW_TRUE = 5
    RW_FALSE = 6
    RW_NULL = 7

    # Palavras Reservadas - Fluxo de Controle
    RW_SEQ = 8
    RW_PAR = 9
    RW_IF = 10
    RW_ELSE = 11
    RW_WHILE = 12
    RW_CHAN = 13
    RW_FOR = 44
    RW_RETURN = 43
    
    # Operadores e Delimitadores
    OP_ASSIGN = 14  # =
    OP_PLUS = 15    # +
    OP_MINUS = 16   # -
    OP_MULTIPLY = 17  # *
    OP_DIVIDE = 18    # /
    DL_LPAREN = 19    # (
    DL_RPAREN = 20    # )
    DL_SEMICOLON = 21 # ;
    DL_LBRACE = 22    # {
    DL_RBRACE = 23    # }
    DL_COMMA = 24     # ,
    DL_DOT = 25       # .
    DL_LBRACKET = 26  # [
    DL_RBRACKET = 27  # ]
    
    # Identificadores e Literais
    ID = 28
    NUM = 29  
    STRING_LITERAL = 30
    
    # Fim do Arquivo
    EOF = 31
    
    # Funções Internas do Python
    RW_PRINT = 32
    RW_INPUT = 33
    
    # Operadores Booleanos
    OP_AND = 34
    OP_OR = 35
    OP_NOT = 36
    OP_EQ = 37
    OP_NE = 38
    OP_LT = 39
    OP_LE = 40
    OP_GT = 41
    OP_GE = 42
    
    # Incremento e Decremento
    OP_INC = 45
    OP_DEC = 46
    OP_PLUS_ASSIGN = 47
    OP_MINUS_ASSIGN = 48
    
    # Bloco e Declaração
    
    BLOCK = 49
    DECLARATION = 50
    CALL = 51
    PROGRAM = 52

    
    
    