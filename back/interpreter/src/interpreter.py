import json  # Importa o módulo JSON para manipulação de dados JSON
import socket  # Importa o módulo socket para comunicação em rede
import threading  # Importa o módulo threading para concorrência

from common.tokens import TokenEnums as en  # Importa TokenEnums do módulo enum_tokens
from semantic.src.semantic_analyzer import SemanticAnalyzer
from syntactic.src.parser import Parser  # Importa o módulo Parser
from trees.syntax_tree import SyntaxNode

import io
import contextlib


def _calculate(num1, operator, num2):
    """
    Função para realizar cálculos aritméticos básicos.
    """
    result = 0
    if operator == "+":
        result = float(num1) + float(num2)
    elif operator == "-":
        result = float(num1) - float(num2)
    elif operator == "*":
        result = float(num1) * float(num2)
    elif operator == "/":
        if num2 != 0:
            result = float(num1) / float(num2)
        else:
            return "Error: Invalid Operation, Division by zero!"
    else:
        return "Error: Invalid operator!"
    return result


def c_channel(host, type):
    """
    Função para criar canais de soquete cliente ou servidor com base no tipo fornecido.
    A entrada é agora passada por parâmetros, sem a necessidade de usar input().
    """
    this_addr = (host, 5546)
    size = 1024
    format = "utf-8"
    procedure = None

    if type == "server":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(this_addr)
        server.listen()
        print("[SERVER] Waiting for connections...")
        first = True
        op = False
        conn, addr = server.accept()
        try:
            while True:
                if first:
                    print(f"[SERVER] Connected to {addr}")
                    conn.send("What procedure do you wish to execute?".encode(format))
                    first = False

                a = conn.recv(size).decode(format)
                print(f"[SERVER] Received command: {a} from {addr}")
                if a == "exit":
                    break

                elif a == "calculadora" and not op:
                    op = True
                    procedure = a
                    conn.send("Awaiting expression...".encode(format))

                elif a.startswith("Expression:"):
                    print(f"[SERVER] Received expression: {a} from {addr}")
                    a = a.replace("Expression: ", "").split()
                    result = _calculate(a[0], a[1], a[2])
                    message = f"Result: {result}"
                    conn.send(message.encode("ascii"))
                    break
                else:
                    conn.send("Invalid command".encode("ascii"))
        finally:
            server.close()

    elif type == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(this_addr)
        message = client.recv(size).decode(format)
        print(f"Message from server: {message}")

        # Recebe o procedimento como parâmetro ou via rede (sem usar input())
        procedure = "calculadora"  # Exemplo de valor passado diretamente
        client.send(procedure.encode(format))

        while True:
            message = client.recv(size).decode(format)
            print(f"Message from server: {message}")

            if message == "Awaiting expression...":
                expression = "5 + 3"  # Exemplo de expressão passada diretamente
                client.send(f"Expression: {expression}".encode(format))
            elif "Invalid" in message:
                break
            elif message.startswith("Result"):
                print(f"{message}")
                break

        client.close()

def par_block(block):
    """
    Função para executar um bloco de código concorrentemente usando threading.
    """
    thread = threading.Thread(target=lambda: exec(block[0]))
    thread.start()


def seq_block():
    """
    Função de espaço reservado para a execução sequencial de blocos de código.
    """
    pass


class Interpreter:
    """
    Classe que representa um interpretador para uma linguagem de programação.
    """

    def __init__(self, tree: SyntaxNode | None = None, export=False):
        self.semantic = SemanticAnalyzer()  # Instância do analisador semântico
        self.output = []  # Saída gerada durante a interpretação
        self.export = (
            export  # Sinalizador indicando se os resultados devem ser exportados
        )
        self.tree = tree  # Árvore de sintaxe abstrata gerada durante o parsing

    def run(self):
        """
        Método para executar o programa interpretado.
        """
        self.tree.print_tree()
        if self.export:
            self.save_tree()
        self.semantic.visit(self.tree)

        evalueted_tree = self.tree.evaluate()

        # Criar um buffer para capturar a saída
        buffer = io.StringIO()

        print("ÁRVORE: ", evalueted_tree)
        # Redirecionar a saída padrão para o buffer
        with contextlib.redirect_stdout(buffer):
            exec(evalueted_tree)

        # Obter a saída capturada
        saida = buffer.getvalue()

        # Atualiza o self.output com o resultado do exec()

        if self.export:
            self.save_tree()
        return saida

    def save_tree(self):
        """
        Salva a árvore sintática abstrata em um arquivo JSON.
        """
        with open("tree.json", "w") as file:
            file.write(json.dumps(self.tree.to_json(), indent=4))
