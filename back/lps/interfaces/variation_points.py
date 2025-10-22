"""
Interfaces para pontos de variação da linha de produto.

Este módulo define as interfaces para os diferentes pontos de variação:
- Interface do Compilador (Terminal vs GUI)
- Geração de Código (Mostrar vs Ocultar)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from interfaces.ast import ASTNode
from interfaces.ir import IRInstruction


class CompilerInterface(ABC):
    """Interface base para diferentes tipos de interface do compilador."""
    
    @abstractmethod
    def display_welcome(self) -> None:
        """Exibe mensagem de boas-vindas."""
        pass
    
    @abstractmethod
    def display_progress(self, stage: str, message: str) -> None:
        """Exibe progresso da compilação."""
        pass
    
    @abstractmethod
    def display_result(self, result: str) -> None:
        """Exibe resultado da compilação."""
        pass
    
    @abstractmethod
    def display_error(self, error: str) -> None:
        """Exibe erro."""
        pass


class TerminalInterface(CompilerInterface):
    """Implementação da interface para terminal."""
    
    def display_welcome(self) -> None:
        """Exibe mensagem de boas-vindas no terminal."""
        print("=" * 60)
        print("    COMPILADOR MINIPAR - INTERFACE TERMINAL")
        print("=" * 60)
        print()
    
    def display_progress(self, stage: str, message: str) -> None:
        """Exibe progresso da compilação no terminal."""
        print(f"[{stage}] {message}")
    
    def display_result(self, result: str) -> None:
        """Exibe resultado da compilação no terminal."""
        print("\n" + "=" * 60)
        print("    RESULTADO DA COMPILAÇÃO")
        print("=" * 60)
        print(result)
        print("=" * 60)
    
    def display_error(self, error: str) -> None:
        """Exibe erro no terminal."""
        print(f"\n❌ ERRO: {error}")


class GUIInterface(CompilerInterface):
    """Implementação da interface para GUI."""
    
    def __init__(self):
        self.window = None
        self._init_gui()
    
    def _init_gui(self) -> None:
        """Inicializa a interface gráfica."""
        try:
            import tkinter as tk
            from tkinter import ttk, scrolledtext
            
            self.root = tk.Tk()
            self.root.title("Compilador Minipar - Interface Gráfica")
            self.root.geometry("800x600")
            
            # Frame principal
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Área de texto para saída
            self.output_text = scrolledtext.ScrolledText(
                main_frame, 
                width=80, 
                height=30,
                wrap=tk.WORD
            )
            self.output_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Botões
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=1, column=0, columnspan=2, pady=10)
            
            ttk.Button(button_frame, text="Limpar", command=self._clear_output).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Fechar", command=self.root.quit).pack(side=tk.LEFT, padx=5)
            
            # Configurar grid
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(0, weight=1)
            
            # Armazena referência ao tk para uso posterior
            self.tk = tk
            
        except ImportError:
            # Fallback para terminal se tkinter não estiver disponível
            self.output_text = None
            self.root = None
            self.tk = None
            print("⚠️  tkinter não disponível. Usando interface de terminal.")
    
    def display_welcome(self) -> None:
        """Exibe mensagem de boas-vindas na GUI."""
        welcome_msg = """
╔══════════════════════════════════════════════════════════════╗
║                COMPILADOR MINIPAR - INTERFACE GRÁFICA        ║
║                                                              ║
║  Bem-vindo ao Compilador Minipar com Interface Gráfica!     ║
║  Esta interface oferece uma experiência visual para        ║
║  compilação de código Minipar.                               ║
╚══════════════════════════════════════════════════════════════╝
"""
        if self.output_text and self.tk:
            self.output_text.insert(self.tk.END, welcome_msg + "\n")
            self.output_text.see(self.tk.END)
        else:
            print(welcome_msg)
    
    def display_progress(self, stage: str, message: str) -> None:
        """Exibe progresso da compilação na GUI."""
        progress_msg = f"[{stage}] {message}\n"
        if self.output_text and self.tk:
            self.output_text.insert(self.tk.END, progress_msg)
            self.output_text.see(self.tk.END)
            self.root.update()
        else:
            print(progress_msg.strip())
    
    def display_result(self, result: str) -> None:
        """Exibe resultado da compilação na GUI."""
        result_msg = f"\n{'='*60}\n    RESULTADO DA COMPILAÇÃO\n{'='*60}\n{result}\n{'='*60}\n"
        if self.output_text and self.tk:
            self.output_text.insert(self.tk.END, result_msg)
            self.output_text.see(self.tk.END)
        else:
            print(result_msg)
    
    def display_error(self, error: str) -> None:
        """Exibe erro na GUI."""
        error_msg = f"\n❌ ERRO: {error}\n"
        if self.output_text and self.tk:
            self.output_text.insert(self.tk.END, error_msg)
            self.output_text.see(self.tk.END)
        else:
            print(error_msg)
    
    def _clear_output(self) -> None:
        """Limpa a área de saída."""
        if self.output_text and self.tk:
            self.output_text.delete(1.0, self.tk.END)
    
    def run(self) -> None:
        """Executa o loop principal da GUI."""
        if self.root:
            self.root.mainloop()


class CodeDisplayManager(ABC):
    """Interface base para gerenciamento de exibição de código."""
    
    @abstractmethod
    def should_show_ir(self) -> bool:
        """Determina se deve mostrar código IR."""
        pass
    
    @abstractmethod
    def should_show_assembly(self) -> bool:
        """Determina se deve mostrar código assembly."""
        pass
    
    @abstractmethod
    def format_ir_output(self, ir_instructions: List[IRInstruction]) -> str:
        """Formata saída do código IR."""
        pass
    
    @abstractmethod
    def format_assembly_output(self, assembly_code: str) -> str:
        """Formata saída do código assembly."""
        pass


class ShowAllCodeDisplay(CodeDisplayManager):
    """Implementação que mostra todo o código gerado."""
    
    def should_show_ir(self) -> bool:
        """Sempre mostra código IR."""
        return True
    
    def should_show_assembly(self) -> bool:
        """Sempre mostra código assembly."""
        return True
    
    def format_ir_output(self, ir_instructions: List[IRInstruction]) -> str:
        """Formata saída do código IR com detalhes."""
        output = []
        output.append("CÓDIGO INTERMEDIÁRIO (3 ENDEREÇOS):")
        output.append("-" * 50)
        
        for i, instruction in enumerate(ir_instructions):
            output.append(f"{i+1:3d}: {instruction.op.value}")
            if instruction.dest:
                output.append(f"      Destino: {instruction.dest}")
            if instruction.arg1:
                output.append(f"      Arg1: {instruction.arg1}")
            if instruction.arg2:
                output.append(f"      Arg2: {instruction.arg2}")
            output.append("")
        
        return "\n".join(output)
    
    def format_assembly_output(self, assembly_code: str) -> str:
        """Formata saída do código assembly."""
        output = []
        output.append("CÓDIGO ASSEMBLY ARMv7 (CPUlator):")
        output.append("-" * 50)
        output.append(assembly_code)
        output.append("-" * 50)
        
        return "\n".join(output)


class HideAllCodeDisplay(CodeDisplayManager):
    """Implementação que oculta todo o código gerado."""
    
    def should_show_ir(self) -> bool:
        """Nunca mostra código IR."""
        return False
    
    def should_show_assembly(self) -> bool:
        """Nunca mostra código assembly."""
        return False
    
    def format_ir_output(self, ir_instructions: List[IRInstruction]) -> str:
        """Retorna mensagem indicando que o código foi ocultado."""
        return "Código intermediário gerado (oculto conforme configuração)."
    
    def format_assembly_output(self, assembly_code: str) -> str:
        """Retorna mensagem indicando que o código foi ocultado."""
        return "Código assembly gerado (oculto conforme configuração)."


def create_interface(interface_type) -> CompilerInterface:
    """Factory para criar interfaces baseadas no tipo."""
    if interface_type.value == "terminal":
        return TerminalInterface()
    elif interface_type.value == "gui":
        return GUIInterface()
    else:
        raise ValueError(f"Tipo de interface não suportado: {interface_type}")


def create_code_display(display_mode) -> CodeDisplayManager:
    """Factory para criar gerenciadores de exibição baseados no modo."""
    if display_mode.value == "show_all":
        return ShowAllCodeDisplay()
    elif display_mode.value == "hide_all":
        return HideAllCodeDisplay()
    else:
        raise ValueError(f"Modo de exibição não suportado: {display_mode}")
