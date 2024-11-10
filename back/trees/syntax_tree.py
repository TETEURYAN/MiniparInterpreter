from common.tokens import TokenEnums as en


class SyntaxNode:
    # Inicializa um nó da árvore sintática com um tipo de nó e um valor opcional
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.scope = None
        self.nparams = None
        self.children = []

    # Adiciona um nó filho ao nó atual
    def add_children(self, child_node):
        self.children.append(child_node)

    # Imprime a árvore sintática
    def print_tree(self, level=0):
        indent = "    " * level
        print(
            f'{indent}{self.node_type} of value {self.value if self.value is not None else "--"}'
        )

        for child in self.children:
            child.print_tree(level + 1)

    # Converte o nó da árvore sintática em JSON
    def to_json(self):
        def convert_enum_to_str(value):
            if isinstance(value, en):
                return value.name
            return value

        node_json = {
            "node_type": convert_enum_to_str(self.node_type),
            "value": (
                self.value.to_json()
                if isinstance(self.value, SyntaxNode)
                else convert_enum_to_str(self.value) if self.value is not None else "--"
            ),
            "children": [child.to_json() for child in self.children],
        }
        return node_json

    # Avalia a árvore sintática e gera código Python correspondente
    def evaluate(self, indent_level=0):
        indent = "    " * indent_level  # Quatro espaços por nível de indentação

        if self.node_type == en.PROGRAM:
            code = ""
            for child in self.children:
                code += child.evaluate(indent_level) + "\n"
            return code

        if self.node_type in [en.RW_INT, en.RW_STRING]:
            output = ""
            for child in self.children:
                output += child.evaluate(indent_level) + "\n"
            return output

        elif self.node_type == en.OP_ASSIGN:
            variable = self.children[0].value
            expression = self.children[1]
            return f"{indent}{variable} = {expression.evaluate()}"

        # Operações aritméticas
        elif self.node_type in [en.OP_PLUS, en.OP_MINUS, en.OP_MULTIPLY, en.OP_DIVIDE]:
            left = self.children[0].evaluate()
            right = self.children[1].evaluate()

            match self.node_type:
                case en.OP_PLUS:
                    return f"({left} + {right})"
                case en.OP_MINUS:
                    return f"({left} - {right})"
                case en.OP_MULTIPLY:
                    return f"({left} * {right})"
                case en.OP_DIVIDE:
                    return f"({left} / {right})"
                case _:
                    raise ValueError(f"Invalid node_type enum {self.node_type}")

        # Identificador
        elif self.node_type == en.ID:
            return self.value

        # Número
        elif self.node_type == en.NUM:
            return str(self.value)

        # Literal de string
        elif self.node_type == en.STRING_LITERAL:
            return f'"{self.value}"'

        # Loop for
        elif self.node_type == en.RW_FOR:
            init = self.children[0].evaluate()
            condition = self.value.evaluate()
            increment = self.children[1].evaluate(indent_level + 1)
            block = self.children[2].evaluate(indent_level + 1)
            return f"{indent}{init}\n{indent}while {condition}:\n{increment}\n{block}"

        # Estrutura de controle if
        elif self.node_type == en.RW_IF:
            condition = self.value.evaluate()
            block_true = self.children[0].evaluate(indent_level + 1)
            if len(self.children) > 1:
                block_false = self.children[1].evaluate(indent_level + 1)
                return (
                    f"{indent}if {condition}:\n{block_true}{indent}else:\n{block_false}"
                )
            else:
                return f"{indent}if {condition}:\n{block_true}"

        # Bloco de código
        elif self.node_type == en.BLOCK:
            block_code = ""
            for child in self.children:
                block_code += child.evaluate(indent_level + 1) + "\n"
            return f"{block_code}"

        # Impressão
        elif self.node_type == en.RW_PRINT:
            expression = ""
            num_children = len(self.children)
            for i, child in enumerate(self.children):
                expression += child.evaluate()
                if i < num_children - 1:
                    expression += ", "

            return f"{indent}print({expression})\n"

        # Entrada de dados
        elif self.node_type == en.RW_INPUT:
            variable = self.children[0].evaluate()
            return f"{indent}{variable} = input()"

        # Operações de comparação
        elif self.node_type in [
            en.OP_GT,
            en.OP_LT,
            en.OP_GE,
            en.OP_LE,
            en.OP_EQ,
            en.OP_NE,
        ]:
            left = self.children[0].evaluate()
            right = self.children[1].evaluate()
            if self.node_type == en.OP_GT:
                return f"{left} > {right}"
            elif self.node_type == en.OP_LT:
                return f"{left} < {right}"
            elif self.node_type == en.OP_GE:
                return f"{left} >= {right}"
            elif self.node_type == en.OP_LE:
                return f"{left} <= {right}"
            elif self.node_type == en.OP_EQ:
                return f"{left} == {right}"
            elif self.node_type == en.OP_NE:
                return f"{left} != {right}"

        # Loop while
        elif self.node_type == en.RW_WHILE:
            condition = self.value.evaluate()
            block = self.children[0].evaluate(indent_level + 1)
            return f"{indent}while {condition}:\n{block}"

        # Paralelismo
        elif self.node_type == en.RW_PAR:
            block_code = self.children[0].evaluate(indent_level + 1).strip()
            return f"{indent}par_block(['''{block_code}'''])"

        # Sequencial
        elif self.node_type == en.RW_SEQ:
            block = self.children[0].evaluate(indent_level)
            return f"{indent}{block}"

        # Canal de comunicação
        elif self.node_type == en.RW_C_CHANNEL:
            host = self.children[0].evaluate(indent_level)
            type = self.children[1].evaluate(indent_level)
            return f"{indent}c_channel({host}, {type})\n"
        else:
            raise ValueError(f"Invalid node_type enum {self.node_type}")

    @classmethod
    def from_dict(cls, node_dict) -> "SyntaxNode":
        def convert_str_to_enum(value):
            if isinstance(value, str) and hasattr(en, value):
                return getattr(en, value)

            return value

        node_type = convert_str_to_enum(node_dict["node_type"])
        value = node_dict["value"]
        if isinstance(value, dict):
            value = cls.from_dict(value)
        else:
            value = convert_str_to_enum(value) if value != "--" else None

        node = cls(node_type, value)
        for child_dict in node_dict["children"]:
            child_node = cls.from_dict(child_dict)
            node.add_children(child_node)
        return node
