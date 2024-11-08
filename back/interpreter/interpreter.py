from semantic import SemanticAnalyzer  # Importa o módulo SemanticAnalyzer
from _parser import Parser  # Importa o módulo Parser
from enum_tokens import TokenEnums as en  # Importa TokenEnums do módulo enum_tokens
import json  # Importa o módulo JSON para manipulação de dados JSON
import threading  # Importa o módulo threading para concorrência
import socket  # Importa o módulo socket para comunicação em rede

def _calculate(num1, operator, num2):
    """
    Função para realizar cálculos aritméticos básicos.
    """
    result = 0
    if operator == '+':
        result =  float(num1) + float(num2)
    elif operator == '-':
        result = float(num1) - float(num2)
    elif operator == '*':
        result = float(num1) * float(num2)
    elif operator == '/':
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
    """
    this_addr = (host, 5546) # Número da porta para comunicação
    size = 1024 # Tamanho do buffer para receber dados
    format = "utf-8" # Formato de codificação para dados de string
    procedure = None # Espaço reservado para o procedimento a ser executado

    if type == "server":
        # Criando um soquete do servidor
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(this_addr)  # Vinculando o servidor ao endereço
        server.listen()  # Aguardando conexões de entrada
        print("[SERVER] Waiting for connections...")
        first = True
        op = False
        print("Waiting for connections...")
        conn, addr = server.accept()  # Aceitando conexão do cliente
        try:
            while True:
                if first:
                    print(f"[SERVER] Connected to {addr}")
                    conn.send("What procedure do you wish to execute?".encode(format))
                    first = False

                a = conn.recv(size).decode(format) # Recebendo dados do cliente
                print(f"[SERVER] Received command: {a} from {addr}")
                if a == "exit":
                    break

                elif a == "calculadora" and op == False:
                    op = True
                    procedure = a
                    conn.send("Awaiting expression...".encode("ascii"))

                elif a.startswith("Expression:"):
                    print(f"[SERVER] Received expression: {a} from {addr}")
                    a = a.replace("Expression: ", "")
                    a = a.split()
                    result = _calculate(a[0],a[1],a[2]) # Realizando cálculo
                    message = f"Result: {result}"
                    conn.send(message.encode("ascii")) # Enviando resultado de volta para o cliente
                    break
                else:
                    conn.send("Invalid command".encode("ascii")) # Lidando com comandos inválidos
        finally:
            server.close() # Fechando soquete do servidor ao finalizar

    elif type == "client":
        # Criando um soquete do cliente
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(this_addr) # Conectando ao servidor
        message = client.recv(size).decode(format) # Recebendo mensagem do servidor
        print(f"Message from server: {message}")
        procedure = input("Enter the procedure you wish to execute: ") # Enviando procedimento para o servidor
        client.send(procedure.encode(format)) # Recebendo mensagem do servidor
        while True:
            message = client.recv(size).decode(format) # Enviando expressão para o servidor
            print(f"Message from server: {message}")

            if message == "Awaiting expression...":
                expression = input("Enter your expression: ")
                expression = "Expression: " + expression
                client.send(expression.encode(format))
                print(f"Message Sent: {expression}")
            elif "Invalid" in message:
                break
            elif message.startswith("Result"):
                print(f"{message}")
                break
        client.close() # Fechando soquete do cliente ao finalizar

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
    def __init__(self, program, export=False):
        self.program = program  # Código do programa a ser interpretado
        self.semantic = SemanticAnalyzer()  # Instância do analisador semântico
        self.parser = Parser(program)  # Instância do analisador
        self.output = []  # Saída gerada durante a interpretação
        self.export = export  # Sinalizador indicando se os resultados devem ser exportados
        self.tree = None  # Árvore de sintaxe abstrata gerada durante o parsing

    def run(self):
        """
        Método para executar o programa interpretado.
        """
        self.tree = self.parser.parse()
        self.tree.print_tree()
        if self.export:
            self.save_tree()
        self.semantic.visit(self.tree)
        exec(self.tree.evaluate())
        if self.export:
            self.save_tree()
        return self.output

    def save_tree(self):
        """
        Salva a árvore sintática abstrata em um arquivo JSON.
        """
        with open("tree.json", "w") as file:
            file.write(json.dumps(self.tree.to_json(), indent=4))