from common.tokens import TokenEnums as en
from trees.syntax_tree import SyntaxNode


class Parser:
    # Inicializador da classe Parser
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    # Função principal de análise sintática
    def parse(self):
        syntax_tree = self.parse_program()
        return syntax_tree

    # Analisa um programa
    def parse_program(self):
        syntax_tree = SyntaxNode(en.PROGRAM)

        while self.current_token[0] != en.EOF:
            if self.current_token[0] == en.ID:
                assignment_node = self.parse_assignment()
                syntax_tree.add_children(assignment_node)
            elif self.current_token[0] in (en.RW_INT, en.RW_BOOL, en.RW_STRING):
                declaration_node = self.parse_declaration()
                syntax_tree.add_children(declaration_node)
            elif self.current_token[0] in (
                en.RW_IF,
                en.RW_WHILE,
                en.RW_FOR,
                en.RW_PRINT,
                en.RW_INPUT,
                en.RW_C_CHANNEL,
                en.RW_SEQ,
                en.RW_PAR,
            ):
                statement_node = self.parse_statement()
                syntax_tree.add_children(statement_node)
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        return syntax_tree

    # Analisa uma declaração
    def parse_declaration(self):
        token = self.current_token
        if token[0] in (en.RW_INT, en.RW_BOOL, en.RW_STRING):
            self.eat(token[0])
            identifier = self.current_token
        else:
            raise SyntaxError(f"Invalid declaration: {token[0]}, expected a type")

        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)

        assignment_node = SyntaxNode(en.OP_ASSIGN)

        identifier_node = SyntaxNode(en.ID, identifier[1])
        assignment_node.add_children(identifier_node)
        assignment_node.add_children(value)

        declaration_node = SyntaxNode(token[0])
        declaration_node.add_children(assignment_node)

        return declaration_node

    # Analisa um bloco de código delimitado por chaves { }
    def parse_block(self):
        block_node = SyntaxNode(en.BLOCK)
        self.eat(en.DL_LBRACE)
        while self.current_token[0] != en.DL_RBRACE:
            statement_node = self.parse_statement()
            block_node.add_children(statement_node)
        self.eat(en.DL_RBRACE)
        return block_node

    # Analisa uma declaração ou instrução
    def parse_statement(self):
        token_type = self.current_token[0]

        if token_type == en.RW_INT:
            return self.parse_declaration()
        elif token_type == en.ID:
            return self.parse_assignment()
        elif token_type == en.RW_IF:
            return self.parse_if_statement()
        elif token_type == en.RW_WHILE:
            return self.parse_while_statement()
        elif token_type == en.RW_FOR:
            return self.parse_for_statement()
        elif token_type == en.RW_PRINT:
            return self.parse_print()
        elif token_type == en.RW_INPUT:
            return self.parse_input()
        elif token_type == en.RW_C_CHANNEL:
            return self.parse_c_channel()
        elif token_type == en.RW_SEQ:
            return self.parse_seq()
        elif token_type == en.RW_PAR:
            return self.parse_par()
        elif token_type == en.RW_CHAN_SEND:
            return self.parse_chan_send()
        elif token_type == en.RW_CHAN_RECV:
            return self.parse_chan_recv()
        else:
            return self.parse_expression()

    # Analisa uma instrução IF
    def parse_if_statement(self):
        self.eat(en.RW_IF)
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        if_block = self.parse_block()
        else_block = None
        if self.current_token[0] == en.RW_ELSE:
            self.eat(en.RW_ELSE)
            else_block = self.parse_block()
        if_node = SyntaxNode(en.RW_IF, condition)
        if_node.add_children(if_block)
        if else_block:
            if_node.add_children(else_block)
        return if_node

    def parse_chan_send(self):
        # chan_send(chan, v1, v2);
        self.eat(en.RW_CHAN_SEND)
        params = self.parse_params()
        if len(params) != 3:
            raise SyntaxError("Invalid number of parameters for chan_send")
        send_node = SyntaxNode(en.RW_CHAN_SEND, params[0])
        send_node.add_children(params[1])
        send_node.add_children(params[2])
        self.eat(en.DL_SEMICOLON)
        return send_node

    def parse_chan_recv(self):
        # chan_recv(chan, v1, v2, res);
        self.eat(en.RW_CHAN_RECV)
        params = self.parse_params()
        if len(params) != 4:
            raise SyntaxError("Invalid number of parameters for chan_recv")
        recv_node = SyntaxNode(en.RW_CHAN_RECV, params[0])
        recv_node.add_children(params[1])
        recv_node.add_children(params[2])
        recv_node.add_children(params[3])
        self.eat(en.DL_SEMICOLON)

    # Analisa uma instrução WHILE
    def parse_while_statement(self):
        self.eat(en.RW_WHILE)
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        block = self.parse_block()

        while_node = SyntaxNode(en.RW_WHILE, condition)
        while_node.add_children(block)

        return while_node

    # Analisa uma instrução FOR
    def parse_for_statement(self):
        self.eat(en.RW_FOR)
        self.eat(en.DL_LPAREN)
        init = None

        if self.current_token[0] == en.RW_INT:
            init = self.parse_declaration()
        else:
            init = self.parse_assignment()

        condition = self.parse_expression()

        self.eat(en.DL_SEMICOLON)

        increment = self.parse_assignment()

        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        for_node = SyntaxNode(en.RW_FOR, condition)
        for_node.add_children(init)
        for_node.add_children(increment)
        for_node.add_children(block)

        return for_node

    # Analisa uma instrução de comunicação em canal C
    def parse_c_channel(self):
        token = self.current_token
        self.eat(en.RW_C_CHANNEL)
        params = self.parse_params()

        if len(params) != 3:
            raise SyntaxError("Invalid number of parameters for c_channel")

        channel_node = SyntaxNode(en.RW_C_CHANNEL)
        channel_node.add_children(params[0])
        channel_node.add_children(params[1])
        self.eat(en.DL_SEMICOLON)
        return channel_node

    # Analisa os parâmetros de uma função ou método
    def parse_params(self):
        self.eat(en.DL_LPAREN)
        params = []
        while self.current_token[0] != en.DL_RPAREN:
            param = self.parse_expression()
            params.append(param)
            if self.current_token[0] == en.DL_COMMA:
                self.eat(en.DL_COMMA)
        self.eat(en.DL_RPAREN)
        return params

    # Analisa uma instrução SEQ
    def parse_seq(self):
        self.eat(en.RW_SEQ)
        block = self.parse_block()
        seq_node = SyntaxNode(en.RW_SEQ)
        seq_node.add_children(block)
        return seq_node

    # Analisa uma instrução PAR
    def parse_par(self):
        self.eat(en.RW_PAR)
        block = self.parse_block()
        par_node = SyntaxNode(en.RW_PAR)
        par_node.add_children(block)
        return par_node

    # Analisa uma instrução de entrada
    def parse_input(self):
        self.eat(en.RW_INPUT)
        params = self.parse_params()
        if len(params) != 1:
            raise SyntaxError("Invalid number of parameters for input")
        input_node = SyntaxNode(en.RW_INPUT)
        input_node.add_children(params[0])
        self.eat(en.DL_SEMICOLON)
        return input_node

    # Analisa uma instrução de impressão
    def parse_print(self):
        self.eat(en.RW_PRINT)
        self.eat(en.DL_LPAREN)
        expression = self.parse_expression()
        print_node = SyntaxNode(en.RW_PRINT)
        print_node.add_children(expression)
        while self.current_token[0] == en.DL_COMMA:
            self.eat(en.DL_COMMA)
            expression = self.parse_expression()
            print_node.add_children(expression)
        self.eat(en.DL_RPAREN)
        self.eat(en.DL_SEMICOLON)
        return print_node

    # Analisa uma instrução de atribuição
    def parse_assignment(self):
        identifier = self.current_token
        self.eat(en.ID)
        token = self.current_token
        if token[0] == en.OP_ASSIGN:
            self.eat(en.OP_ASSIGN)
            value = self.parse_expression()
            try:
                self.eat(en.DL_SEMICOLON)
            except SyntaxError:
                print("WARNING: Expected semicolon, but did not find one.")

            assignment_node = SyntaxNode(en.OP_ASSIGN)
            identifier_node = SyntaxNode(en.ID, identifier[1])
            assignment_node.add_children(identifier_node)
            assignment_node.add_children(value)
            return assignment_node

        elif token[0] in (en.OP_PLUS, en.OP_MINUS):
            operator = token[0]
            self.eat(operator)
            value = self.parse_expression()
            self.eat(en.DL_SEMICOLON)
            operation_node = SyntaxNode(operator)
            operation_node.add_children(SyntaxNode(en.ID, identifier[1]))
            operation_node.add_children(value)
            return operation_node
        elif token[0] in (en.OP_INCREMENT, en.OP_DECREMENT):
            operator = token[0]
            self.eat(operator)
            self.eat(en.DL_SEMICOLON)
            operation_node = SyntaxNode(operator)
            operation_node.add_children(SyntaxNode(en.ID, identifier[1]))
            return operation_node

        else:
            raise SyntaxError("Invalid assignment statement")

    # Analisa uma expressão
    def parse_expression(self):

        node = self.parse_term()

        while self.current_token[0] in (
            en.OP_PLUS,
            en.OP_MINUS,
            en.OP_MULTIPLY,
            en.OP_DIVIDE,
            en.OP_GT,
            en.OP_LT,
            en.OP_GE,
            en.OP_LE,
            en.OP_EQ,
            en.OP_NE,
        ):
            token = self.current_token

            self.eat(token[0])
            operator_node = SyntaxNode(token[0])
            operator_node.add_children(node)
            operator_node.add_children(self.parse_term())
            node = operator_node
        return node

    # Analisa um termo
    def parse_term(self):
        node = self.parse_factor()

        while self.current_token[0] in (
            en.OP_MULTIPLY,
            en.OP_DIVIDE,
            en.OP_PLUS,
            en.OP_MINUS,
        ):
            token = self.current_token
            self.eat(token[0])
            operator = token[0]
            rhs = self.parse_factor()

            operator_node = SyntaxNode(operator)

            operator_node.add_children(node)

            operator_node.add_children(rhs)

            node = operator_node

        return node

    # Analisa um fator
    def parse_factor(self):
        token = self.current_token
        if token[0] == en.RW_INT:
            self.eat(en.RW_INT)
            return SyntaxNode(en.RW_INT, token[1])
        elif token[0] == en.DL_LPAREN:
            self.eat(en.DL_LPAREN)
            node = self.parse_expression()
            self.eat(en.DL_RPAREN)
            return node
        elif token[0] == en.ID:
            identifier_token = self.current_token
            self.eat(en.ID)
            return SyntaxNode(en.ID, identifier_token[1])
        elif token[0] == en.NUM:
            num_token = self.current_token
            self.eat(en.NUM)
            return SyntaxNode(en.NUM, num_token[1])
        elif token[0] == en.STRING_LITERAL:
            string_token = self.current_token
            self.eat(en.STRING_LITERAL)
            return SyntaxNode(en.STRING_LITERAL, string_token[1])
        else:
            raise SyntaxError(
                f"Invalid factor: {token[0]}, expected an identifier, integer, or expression"
            )

    # Consome um token
    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = (en.EOF, None)
        elif self.current_token[0] == en.EOF:
            raise SyntaxError(f"Unexpected end of file: expected {token_type}")
        else:
            raise SyntaxError(
                f"Unexpected token: expected {token_type}, got {self.current_token[0]}"
            )
