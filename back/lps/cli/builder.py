"""
Builder para construção de produtos da linha de produto de compiladores.

Este módulo implementa o builder que orquestra a construção
de diferentes produtos de compilação.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
import os
import sys

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent.parent))

from product_config.product_config import ProductConfig, ProductType, BackendType
from frontend.lexer_impl import MiniparLexer
from frontend.parser_impl import MiniparParser
from frontend.semantic_impl import MiniparSemanticAnalyzer
from frontend.symbol_table_impl import MiniparSymbolTable
from ir_generator import MiniparIRGenerator
from backends import X86_64Backend, RISCVBackend, ARMv7Backend
from interfaces.ast import ASTNode
from interfaces.ir import IRInstruction
from interfaces.variation_points import (
    create_interface, create_code_display,
    CompilerInterface, CodeDisplayManager
)


class ProductBuilder:
    """Builder para construção de produtos de compilação."""
    
    def __init__(self, config: ProductConfig):
        self.config = config
        self.symbol_table = MiniparSymbolTable()
        self.ast: Optional[ASTNode] = None
        self.ir_instructions: List[IRInstruction] = []
        self.output: str = ""
        
        # Inicializa pontos de variação
        self.interface = create_interface(config.interface_type)
        self.code_display = create_code_display(config.code_display_mode)
    
    def build(self, input_file: str) -> str:
        """Constrói o produto de compilação."""
        try:
            # Exibe mensagem de boas-vindas
            self.interface.display_welcome()
            
            # Fase 1: Frontend
            self.interface.display_progress("FRONTEND", "Iniciando análise léxica e sintática...")
            self._build_frontend(input_file)
            
            # Fase 2: Geração de IR (se necessário)
            if self.config.product_type in [ProductType.COMPILER, ProductType.IR_GENERATOR]:
                self.interface.display_progress("IR", "Gerando código intermediário...")
                self._build_ir()
            
            # Fase 3: Backend (se necessário)
            if self.config.product_type == ProductType.COMPILER:
                self.interface.display_progress("BACKEND", "Gerando código assembly...")
                self._build_backend()
            
            # Fase 4: Interpretador (se necessário)
            if self.config.product_type == ProductType.INTERPRETER:
                self.interface.display_progress("INTERPRETER", "Executando código...")
                self._build_interpreter()
            
            # Exibe resultado final
            self.interface.display_progress("SUCCESS", "Compilação concluída com sucesso!")
            self.interface.display_result(self.output)
            
            return self.output
            
        except Exception as e:
            self.interface.display_error(str(e))
            raise RuntimeError(f"Erro na construção do produto: {e}")
    
    def _build_frontend(self, input_file: str) -> None:
        """Constrói o frontend."""
        if not self.config.frontend.enable_lexer:
            raise ValueError("Lexer é obrigatório")
        
        if not self.config.frontend.enable_parser:
            raise ValueError("Parser é obrigatório")
        
        # Lê o arquivo de entrada
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Análise léxica
        lexer = MiniparLexer(source_code)
        tokens = lexer.tokenize()
        
        # Análise sintática
        parser = MiniparParser(tokens)
        self.ast = parser.parse()
        
        # Análise semântica (se habilitada)
        if self.config.frontend.enable_semantic_checker:
            semantic_analyzer = MiniparSemanticAnalyzer(self.symbol_table)
            semantic_analyzer.analyze(self.ast)
        
        if self.config.verbose:
            print(f"Frontend construído com sucesso. AST gerada com {len(self.ast.children)} nós.")
    
    def _build_ir(self) -> None:
        """Constrói o gerador de IR."""
        if not self.config.ir or not self.config.ir.enable_ir_generation:
            raise ValueError("Geração de IR não habilitada")
        
        if not self.ast:
            raise ValueError("AST não disponível para geração de IR")
        
        # Gera código IR
        ir_generator = MiniparIRGenerator(self.symbol_table)
        self.ir_instructions = ir_generator.generate(self.ast)
        
        # Aplica otimizações (se habilitadas)
        if self.config.ir.enable_optimization:
            self._apply_ir_optimizations()
        
        # Adiciona código IR à saída se configurado para mostrar
        if self.code_display.should_show_ir():
            ir_output = self.code_display.format_ir_output(self.ir_instructions)
            self.output += ir_output + "\n\n"
        
        if self.config.verbose:
            print(f"IR gerado com sucesso. {len(self.ir_instructions)} instruções geradas.")
    
    def _apply_ir_optimizations(self) -> None:
        """Aplica otimizações no código IR."""
        if not self.config.ir:
            return
        
        # Aplica dobramento de constantes
        if self.config.ir.enable_constant_folding:
            from ir_generator.ir_optimizer_impl import MiniparIROptimizer
            optimizer = MiniparIROptimizer()
            self.ir_instructions = optimizer.optimize_constant_folding(self.ir_instructions)
        
        # Aplica otimização de janela deslizante
        if self.config.ir.enable_peephole_optimization:
            from ir_generator.ir_optimizer_impl import MiniparIROptimizer
            optimizer = MiniparIROptimizer()
            self.ir_instructions = optimizer.optimize_peephole(self.ir_instructions)
    
    def _build_backend(self) -> None:
        """Constrói o backend."""
        if not self.config.backend:
            raise ValueError("Configuração de backend não disponível")
        
        if not self.ir_instructions:
            raise ValueError("Instruções IR não disponíveis para geração de Assembly")
        
        # Seleciona o backend apropriado
        if self.config.backend.backend_type == BackendType.X86_64:
            backend = X86_64Backend(self.symbol_table)
        elif self.config.backend.backend_type == BackendType.RISCV:
            backend = RISCVBackend(self.symbol_table)
        elif self.config.backend.backend_type == BackendType.ARM64:
            # Para ARM64, usa ARMv7 backend
            backend = ARMv7Backend(self.symbol_table)
        else:
            raise ValueError(f"Backend {self.config.backend.backend_type} não suportado")
        
        # Gera código Assembly
        assembly_code = backend.generate_assembly(self.ir_instructions)
        
        # Adiciona código assembly à saída se configurado para mostrar
        if self.code_display.should_show_assembly():
            assembly_output = self.code_display.format_assembly_output(assembly_code)
            self.output += assembly_output + "\n\n"
        else:
            self.output += assembly_code
        
        if self.config.verbose:
            print(f"Backend {self.config.backend.backend_type.value} construído com sucesso.")
    
    def _build_interpreter(self) -> None:
        """Constrói o interpretador."""
        if not self.config.interpreter:
            raise ValueError("Configuração de interpretador não disponível")
        
        if not self.ast:
            raise ValueError("AST não disponível para interpretação")
        
        # Executa a AST diretamente
        if self.config.interpreter.enable_ast_execution:
            from ..interpreter import MiniparInterpreter
            interpreter = MiniparInterpreter(self.ast, self.symbol_table)
            self.output = interpreter.execute()
        
        # Executa via IR (se habilitado)
        elif self.config.interpreter.enable_ir_execution and self.ir_instructions:
            from ..interpreter import MiniparIRInterpreter
            interpreter = MiniparIRInterpreter(self.ir_instructions, self.symbol_table)
            self.output = interpreter.execute()
        
        if self.config.verbose:
            print("Interpretador executado com sucesso.")
    
    def save_output(self, output_file: Optional[str] = None) -> None:
        """Salva a saída em arquivo."""
        if not self.output:
            raise ValueError("Nenhuma saída para salvar")
        
        output_path = output_file or self.config.output_file
        if not output_path:
            raise ValueError("Arquivo de saída não especificado")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.output)
        
        if self.config.verbose:
            print(f"Saída salva em: {output_path}")
    
    def get_ast(self) -> Optional[ASTNode]:
        """Retorna a AST gerada."""
        return self.ast
    
    def get_ir_instructions(self) -> List[IRInstruction]:
        """Retorna as instruções IR geradas."""
        return self.ir_instructions
    
    def get_output(self) -> str:
        """Retorna a saída gerada."""
        return self.output
    
    def get_symbol_table(self) -> MiniparSymbolTable:
        """Retorna a tabela de símbolos."""
        return self.symbol_table
