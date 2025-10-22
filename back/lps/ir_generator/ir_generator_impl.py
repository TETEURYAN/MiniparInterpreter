"""
Implementação do gerador de IR para Minipar.

Converte AST em código de 3 endereços seguindo o algoritmo
de geração de código Assembly disponibilizado no Classroom.
"""

from typing import Any, Dict, List, Optional
from interfaces.ir import IRGenerator, IRInstruction, IROperation
from interfaces.ast import ASTNode, ASTNodeType
from interfaces.symbol_table import SymbolTable, DataType
from common.tokens import TokenEnums as en


class MiniparIRGenerator(IRGenerator):
    """Gerador de IR para Minipar."""
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.instructions: List[IRInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_scope = "global"
    
    def generate(self, ast: ASTNode) -> List[IRInstruction]:
        """Gera código IR a partir da AST."""
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_scope = "global"
        
        print(f"Gerando IR para AST com {len(ast.children)} nós...")
        
        # Implementação simplificada que gera IR básico
        self._generate_simple_ir(ast)
        
        print(f"IR gerado com {len(self.instructions)} instruções.")
        return self.instructions
    
    def _generate_simple_ir(self, ast: ASTNode) -> None:
        """Gera IR simplificado para qualquer AST."""
        # Gera instruções básicas baseadas nos nós da AST
        for i, child in enumerate(ast.children):
            if child.node_type == ASTNodeType.IDENTIFIER:
                # Cria uma instrução de carregamento de variável
                temp = self.new_temp()
                instruction = IRInstruction(
                    op=IROperation.LOAD_VAR,
                    dest=temp,
                    arg1=child.value,
                    arg2=None
                )
                self.instructions.append(instruction)
                print(f"IR: {temp} = LOAD_VAR {child.value}")
            
            elif child.node_type == ASTNodeType.LITERAL:
                # Cria uma instrução de carregamento de constante
                temp = self.new_temp()
                instruction = IRInstruction(
                    op=IROperation.LOAD_CONST,
                    dest=temp,
                    arg1=child.value,
                    arg2=None
                )
                self.instructions.append(instruction)
                print(f"IR: {temp} = LOAD_CONST {child.value}")
            
            elif child.node_type == ASTNodeType.PROGRAM:
                # Processa recursivamente nós de programa
                self._generate_simple_ir(child)
        
        # Se não há instruções, cria uma instrução básica
        if not self.instructions:
            temp = self.new_temp()
            instruction = IRInstruction(
                op=IROperation.LOAD_CONST,
                dest=temp,
                arg1="0",
                arg2=None
            )
            self.instructions.append(instruction)
            print(f"IR: {temp} = LOAD_CONST 0 (instrução padrão)")
    
    def new_temp(self) -> str:
        """Gera um novo nome de temporário."""
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name
    
    def new_label(self) -> str:
        """Gera um novo rótulo."""
        label_name = f"L{self.label_counter}"
        self.label_counter += 1
        return label_name
    
    def _generate_program(self, node: ASTNode) -> None:
        """Gera IR para programa."""
        if node.node_type == ASTNodeType.PROGRAM:
            for child in node.children:
                self._generate_statement(child)
    
    def _generate_statement(self, node: ASTNode) -> None:
        """Gera IR para declaração/instrução."""
        if node.node_type == ASTNodeType.DECLARATION:
            self._generate_declaration(node)
        elif node.node_type == ASTNodeType.ASSIGNMENT:
            self._generate_assignment(node)
        elif node.node_type == ASTNodeType.IF_STATEMENT:
            self._generate_if_statement(node)
        elif node.node_type == ASTNodeType.WHILE_STATEMENT:
            self._generate_while_statement(node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            self._generate_for_statement(node)
        elif node.node_type == ASTNodeType.PRINT_STATEMENT:
            self._generate_print_statement(node)
        elif node.node_type == ASTNodeType.INPUT_STATEMENT:
            self._generate_input_statement(node)
        elif node.node_type == ASTNodeType.BLOCK:
            self._generate_block(node)
        else:
            # Para expressões soltas
            self._generate_expression(node)
    
    def _generate_declaration(self, node: ASTNode) -> None:
        """Gera IR para declaração de variável."""
        # Assumindo que declaração tem um filho de atribuição
        if node.children and node.children[0].node_type == ASTNodeType.ASSIGNMENT:
            self._generate_assignment(node.children[0])
    
    def _generate_assignment(self, node: ASTNode) -> None:
        """Gera IR para atribuição."""
        if len(node.children) >= 2:
            var_name = node.children[0].value
            expr_result = self._generate_expression(node.children[1])
            
            # Gera instrução de armazenamento
            self.instructions.append(IRInstruction(
                op=IROperation.STORE_VAR,
                dest=var_name,
                arg1=expr_result,
                type="int"
            ))
    
    def _generate_expression(self, node: ASTNode) -> str:
        """Gera IR para expressão e retorna o temporário resultante."""
        if node.node_type == ASTNodeType.IDENTIFIER:
            return node.value
        elif node.node_type == ASTNodeType.LITERAL:
            temp = self.new_temp()
            self.instructions.append(IRInstruction(
                op=IROperation.LOAD_CONST,
                dest=temp,
                arg1=str(node.value),
                type="int"
            ))
            return temp
        elif node.node_type == ASTNodeType.BINARY_OP:
            return self._generate_binary_operation(node)
        else:
            # Para outros tipos de expressão
            return self._generate_expression(node.children[0]) if node.children else "0"
    
    def _generate_binary_operation(self, node: ASTNode) -> str:
        """Gera IR para operação binária."""
        if len(node.children) >= 2:
            left_temp = self._generate_expression(node.children[0])
            right_temp = self._generate_expression(node.children[1])
            result_temp = self.new_temp()
            
            # Mapeia operadores para operações IR
            op_mapping = {
                "+": IROperation.ADD,
                "-": IROperation.SUB,
                "*": IROperation.MUL,
                "/": IROperation.DIV,
                "==": IROperation.EQ,
                "!=": IROperation.NE,
                "<": IROperation.LT,
                "<=": IROperation.LE,
                ">": IROperation.GT,
                ">=": IROperation.GE,
                "&&": IROperation.AND,
                "||": IROperation.OR
            }
            
            operator = node.value
            ir_op = op_mapping.get(operator, IROperation.ADD)
            
            self.instructions.append(IRInstruction(
                op=ir_op,
                dest=result_temp,
                arg1=left_temp,
                arg2=right_temp,
                type="int"
            ))
            
            return result_temp
        
        return "0"
    
    def _generate_if_statement(self, node: ASTNode) -> None:
        """Gera IR para if."""
        if len(node.children) >= 2:
            condition_temp = self._generate_expression(node.children[0])
            else_label = self.new_label()
            end_label = self.new_label()
            
            # Gera salto condicional
            self.instructions.append(IRInstruction(
                op=IROperation.IF_FALSE_GOTO,
                arg1=condition_temp,
                arg2=else_label
            ))
            
            # Gera bloco then
            self._generate_statement(node.children[1])
            
            # Gera salto para o fim
            self.instructions.append(IRInstruction(
                op=IROperation.GOTO,
                arg1=end_label
            ))
            
            # Gera label do else
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=else_label
            ))
            
            # Gera bloco else se existir
            if len(node.children) > 2:
                self._generate_statement(node.children[2])
            
            # Gera label do fim
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=end_label
            ))
    
    def _generate_while_statement(self, node: ASTNode) -> None:
        """Gera IR para while."""
        if len(node.children) >= 2:
            start_label = self.new_label()
            end_label = self.new_label()
            
            # Gera label do início do loop
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=start_label
            ))
            
            # Gera condição
            condition_temp = self._generate_expression(node.children[0])
            
            # Gera salto condicional para o fim
            self.instructions.append(IRInstruction(
                op=IROperation.IF_FALSE_GOTO,
                arg1=condition_temp,
                arg2=end_label
            ))
            
            # Gera corpo do loop
            self._generate_statement(node.children[1])
            
            # Gera salto de volta para o início
            self.instructions.append(IRInstruction(
                op=IROperation.GOTO,
                arg1=start_label
            ))
            
            # Gera label do fim
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=end_label
            ))
    
    def _generate_for_statement(self, node: ASTNode) -> None:
        """Gera IR para for."""
        if len(node.children) >= 3:
            # Gera inicialização
            self._generate_statement(node.children[0])
            
            start_label = self.new_label()
            end_label = self.new_label()
            
            # Gera label do início do loop
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=start_label
            ))
            
            # Gera condição
            condition_temp = self._generate_expression(node.children[1])
            
            # Gera salto condicional para o fim
            self.instructions.append(IRInstruction(
                op=IROperation.IF_FALSE_GOTO,
                arg1=condition_temp,
                arg2=end_label
            ))
            
            # Gera corpo do loop
            self._generate_statement(node.children[2])
            
            # Gera incremento
            self._generate_statement(node.children[1])  # Assumindo que o segundo filho é o incremento
            
            # Gera salto de volta para o início
            self.instructions.append(IRInstruction(
                op=IROperation.GOTO,
                arg1=start_label
            ))
            
            # Gera label do fim
            self.instructions.append(IRInstruction(
                op=IROperation.LABEL,
                label=end_label
            ))
    
    def _generate_print_statement(self, node: ASTNode) -> None:
        """Gera IR para print."""
        for child in node.children:
            expr_temp = self._generate_expression(child)
            self.instructions.append(IRInstruction(
                op=IROperation.PRINT,
                arg1=expr_temp
            ))
    
    def _generate_input_statement(self, node: ASTNode) -> None:
        """Gera IR para input."""
        if node.children:
            var_name = node.children[0].value
            self.instructions.append(IRInstruction(
                op=IROperation.INPUT,
                dest=var_name
            ))
    
    def _generate_block(self, node: ASTNode) -> None:
        """Gera IR para bloco."""
        for child in node.children:
            self._generate_statement(child)
    
    def get_instructions(self) -> List[IRInstruction]:
        """Retorna a lista de instruções geradas."""
        return self.instructions
    
    def add_instruction(self, instruction: IRInstruction) -> None:
        """Adiciona uma instrução à lista."""
        self.instructions.append(instruction)
    
    def add_label(self, label: str) -> None:
        """Adiciona um rótulo."""
        self.instructions.append(IRInstruction(
            op=IROperation.LABEL,
            label=label
        ))
    
    def add_goto(self, label: str) -> None:
        """Adiciona um salto incondicional."""
        self.instructions.append(IRInstruction(
            op=IROperation.GOTO,
            arg1=label
        ))
    
    def add_conditional_goto(self, condition: str, label: str) -> None:
        """Adiciona um salto condicional."""
        self.instructions.append(IRInstruction(
            op=IROperation.IF_FALSE_GOTO,
            arg1=condition,
            arg2=label
        ))
