# from _parser import Parser
from common.tokens import TokenEnums as en
from trees.syntax_tree import SyntaxNode


class SemanticAnalyzer:
     # Inicializa o ambiente global e local, e define o tipo e o escopo atuais como nulos
    def __init__(self):
        self.global_env = {}
        self.local_envs = [{}]
        self.current_type = None
        self.current_scope = None

    def enter_scope(self):
        # Adiciona um novo ambiente local
        self.local_envs.append({})

    def exit_scope(self):
        # Remove o ambiente local atual
        self.local_envs.pop()

    def update_global_variable(self, name, value, var_type):
        # Atualiza uma variável global
        self.global_env[name] = {"type": var_type, "value": value}

    def get_operands(self, node):
        # Obtém os operandos de uma operação
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        # Verifica se ambos os operandos são inteiros
        if not left.node_type == en.RW_INT or not right.node_type == en.RW_INT:
            raise Exception("Type error: both operands must be integers")
        return {"left": left.value, "right": right.value}

    def visit(self, node):
        # Visita um nó da árvore sintática
        method_name = f"visit_{node.node_type.name}"
        # Se for um operador de comparação, redireciona para visit_comparison
        if method_name.replace("visit_", "") in (
            "OP_GT",
            "OP_LT",
            "OP_GE",
            "OP_LE",
            "OP_EQ",
            "OP_NE",
        ):
            method_name = "visit_comparison"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        # Método padrão quando não há método de visita definido para um nó
        raise Exception(f"No visit_{node.node_type.name} method defined")

    def visit_PROGRAM(self, node):
        # Visita um nó PROGRAM, que consiste em uma sequência de declarações ou comandos
        for child in node.children:
            self.visit(child)

    def visit_children(self, node):
        # Visita todos os filhos de um nó
        for child in node.children:
            return self.visit(child)

    # As próximas funções visit_* lidam com tipos específicos de nós na árvore sintática, como palavras-chave ou operadores

    # Função visit_RW_INT: define o tipo atual como inteiro
    def visit_RW_INT(self, node):
        self.current_type = en.RW_INT
        child = self.visit_children(node)
        return child

    # Função visit_RW_BOOL: define o tipo atual como booleano
    def visit_RW_BOOL(self, node):
        self.current_type = en.RW_BOOL
        self.visit_children(node)

    # Função visit_RW_STRING: define o tipo atual como string
    def visit_RW_STRING(self, node):
        self.current_type = en.RW_STRING
        self.visit_children(node)
    
    # Função visit_RW_C_CHANNEL: define o tipo atual canal de conexão entre dois computadores e retorna um nó de sintaxe
    def visit_RW_C_CHANNEL(self, node):
        self.current_type = en.RW_C_CHANNEL
        self.visit_children(node)

        return SyntaxNode(en.RW_C_CHANNEL, None)
    

        return node

    # Função visit_RW_PRINT: visita um nó de impressão
    def visit_RW_PRINT(self, node):

        value = self.visit(node.children[0]).value
        if value is None:
            raise Exception("ValueError: cannot print None")
    
    # Função visit_RW_INPUT: visita um nó de entrada
    def visit_RW_INPUT(self, node):
        value = self.visit(node.children[0])

    # Função visit_OP_ASSIGN: visita um nó de atribuição
    def visit_OP_ASSIGN(self, node):
        name = node.children[0].value
        value_node = node.children[1]

        # Se o valor não for numérico ou literal de string, visita o nó
        if (
            value_node.node_type is not en.NUM
            and value_node.node_type is not en.STRING_LITERAL
        ):
            value_node = self.visit(value_node)

        value = value_node.value
        var_type = value_node.node_type

        # Atualiza a variável global ou local, dependendo de onde está definida
        if name in self.global_env:
            self.update_global_variable(name, value, var_type)
        else:
            self.local_envs[-1][name] = {"type": var_type, "value": value}

        # Retorna um nó de sintaxe representando a variável atribuída
        return_node = SyntaxNode(var_type, value)
        return return_node

    # Função visit_ID: visita um nó identificador
    def visit_ID(self, node):
        name = node.value

        # Procura a variável em todos os ambientes locais, depois no global
        for env in reversed(self.local_envs):
            if name in env:
                found_var = env[name]
                if isinstance(found_var["value"], int):
                    return SyntaxNode(en.RW_INT, found_var["value"])
                elif isinstance(found_var["value"], str):
                    return SyntaxNode(en.STRING_LITERAL, found_var["value"])
                else:
                    return SyntaxNode(env[name]["type"], env[name]["value"])

        if name in self.global_env:
            return SyntaxNode(
                self.global_env[name]["type"], self.global_env[name]["value"]
            )

        raise Exception(f"NameError: name '{name}' is not defined")

    # As próximas funções visit_* tratam de nós com valores específicos, como números ou literais de string

    # Função visit_NUM: visita um nó numérico
    def visit_NUM(self, node):
        if isinstance(node.value, int):
            return SyntaxNode(en.RW_INT, node.value)
        raise Exception("Type error: expected integer")
    
    # Função visit_STRING_LITERAL: visita um nó literal de string
    def visit_STRING_LITERAL(self, node):
        if isinstance(node.value, str):
            return SyntaxNode(en.STRING_LITERAL, node.value)
        else:
            raise Exception("Type error: expected string")

    # Função visit_BLOCK: visita um bloco de código
    def visit_BLOCK(self, node):

        prev_global_env = self.global_env.copy()
        
        # Entra em um novo escopo e visita todas as declarações ou comandos dentro do bloco
        self.enter_scope()
        for statement_node in node.children:
            self.visit(statement_node)
        self.exit_scope()
        
        # Atualiza as variáveis globais se elas tiverem sido modificadas dentro do bloco
        for name, value in self.global_env.items():
            if name not in prev_global_env or prev_global_env[name] != value:
                self.update_global_variable(name, value)
    
    # Função visit_OP_MULTIPLY: visita um nó de multiplicação
    def visit_OP_MULTIPLY(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] * op["right"])
    
    # Função visit_OP_DIVIDE: visita um nó de divisão
    def visit_OP_DIVIDE(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] / op["right"])
    
    # Função visit_OP_PLUS: visita um nó de adição
    def visit_OP_PLUS(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] + op["right"])
    
    # Função visit_OP_MINUS: visita um nó de subtração
    def visit_OP_MINUS(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] - op["right"])
    
    # Função visit_RW_PAR: visita um parêntese
    def visit_RW_PAR(self, node):
        self.enter_scope()
        self.visit(node.children[0])
        self.exit_scope()

    # Função visit_RW_SEQ: visita o bloco da função seq
    def visit_RW_SEQ(self, node):
        for child in node.children:
            self.visit(child)

    # Função visit_RW_FOR: visita um laço 'for'
    def visit_RW_FOR(self, node):
        # Entra em um novo escopo
        self.enter_scope()
        init = self.visit(node.children[0])
        condition_node = self.visit(node.value)
        increment = self.visit(node.children[1])
        
        # Converte os nós de inicialização e incremento em números se necessário
        if init.node_type is not None and init.node_type == en.NUM:
            init = self.visit(init)
        if increment.node_type == en.NUM:
            increment = self.visit(increment)
        
        # Verifica se a condição é booleana e se os tipos de inicialização e incremento são inteiros
        if not condition_node == en.RW_BOOL:
            raise Exception("Type error: condition must be boolean")

        if not init.node_type == en.RW_INT or not increment.node_type == en.RW_INT:
            raise Exception(
                "Type error: both operands must be integers. Got: ",
                init.node_type,
                increment.node_type,
            )
        
        # Visita o corpo do laço 'for'
        self.visit(node.children[2])
        
        # Sai do escopo do laço 'for'
        self.exit_scope()

    # Função visit_RW_WHILE: visita um laço 'while'
    def visit_RW_WHILE(self, node):
        condition_node = node.value
        block_node = node.children[0]

        condition_value = self.visit(condition_node).value
        
        # Se a condição for verdadeira, entra em um novo escopo e visita o bloco
        if condition_value:
            self.enter_scope()
            self.visit(block_node)
            self.exit_scope()
   
    # Função visit_comparison: visita um nó de comparação
    def visit_comparison(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        
        # Se os tipos dos operandos forem iguais, retorna booleano
        if left.node_type == right.node_type:
            return en.RW_BOOL

        else:
            raise Exception("Type error: both operands must be of the same type")

    # Função visit_RW_IF: visita um bloco 'if'
    def visit_RW_IF(self, node):
        condition_type = self.visit(node.value)
        if condition_type == en.RW_BOOL:
            self.enter_scope()
            self.visit(node.children[0])
            self.exit_scope()

        else:
            raise Exception("Type error: condition in 'if' statement must be boolean")