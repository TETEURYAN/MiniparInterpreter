"""
Configuração de produtos da linha de produto de compiladores.

Define os diferentes tipos de produtos que podem ser criados
e suas configurações específicas.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


class ProductType(Enum):
    """Tipos de produtos disponíveis."""
    COMPILER = "compiler"
    INTERPRETER = "interpreter"
    IR_GENERATOR = "ir_generator"


class BackendType(Enum):
    """Tipos de backends disponíveis."""
    X86_64 = "x86_64"
    RISCV = "riscv"
    ARM64 = "arm64"
    CUSTOM = "custom"


class OptimizationLevel(Enum):
    """Níveis de otimização."""
    NONE = "none"
    BASIC = "basic"
    AGGRESSIVE = "aggressive"


class InterfaceType(Enum):
    """Tipos de interface disponíveis."""
    TERMINAL = "terminal"
    GUI = "gui"


class CodeDisplayMode(Enum):
    """Modos de exibição de código."""
    SHOW_ALL = "show_all"  # Mostra código de 3 endereços e assembly ARMv7
    HIDE_ALL = "hide_all"  # Não mostra código nenhum


@dataclass
class FrontendConfig:
    """Configuração do frontend."""
    enable_lexer: bool = True
    enable_parser: bool = True
    enable_semantic_checker: bool = True
    enable_ast_builder: bool = True
    enable_symbol_table: bool = True


@dataclass
class BackendConfig:
    """Configuração do backend."""
    backend_type: BackendType
    enable_register_allocation: bool = True
    enable_optimization: bool = True
    optimization_level: OptimizationLevel = OptimizationLevel.BASIC
    enable_debug_info: bool = False
    target_os: str = "linux"
    target_arch: str = "x86_64"


@dataclass
class IRConfig:
    """Configuração do gerador de IR."""
    enable_ir_generation: bool = True
    enable_optimization: bool = True
    enable_constant_folding: bool = True
    enable_peephole_optimization: bool = True
    output_format: str = "json"


@dataclass
class InterpreterConfig:
    """Configuração do interpretador."""
    enable_ast_execution: bool = True
    enable_ir_execution: bool = False
    enable_debug_mode: bool = False
    enable_tracing: bool = False


@dataclass
class ProductConfig:
    """Configuração completa de um produto."""
    name: str
    product_type: ProductType
    description: str
    version: str
    
    # Configurações dos módulos
    frontend: FrontendConfig
    backend: Optional[BackendConfig] = None
    ir: Optional[IRConfig] = None
    interpreter: Optional[InterpreterConfig] = None
    
    # Pontos de variação
    interface_type: InterfaceType = InterfaceType.TERMINAL
    code_display_mode: CodeDisplayMode = CodeDisplayMode.SHOW_ALL
    
    # Configurações gerais
    output_file: Optional[str] = None
    input_file: Optional[str] = None
    verbose: bool = False
    debug: bool = False
    
    def __post_init__(self):
        """Validação pós-inicialização."""
        if self.product_type == ProductType.COMPILER and not self.backend:
            raise ValueError("Compilador deve ter configuração de backend")
        
        if self.product_type == ProductType.INTERPRETER and not self.interpreter:
            raise ValueError("Interpretador deve ter configuração de interpretador")
        
        if self.product_type == ProductType.IR_GENERATOR and not self.ir:
            raise ValueError("Gerador de IR deve ter configuração de IR")
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            "name": self.name,
            "product_type": self.product_type.value,
            "description": self.description,
            "version": self.version,
            "frontend": {
                "enable_lexer": self.frontend.enable_lexer,
                "enable_parser": self.frontend.enable_parser,
                "enable_semantic_checker": self.frontend.enable_semantic_checker,
                "enable_ast_builder": self.frontend.enable_ast_builder,
                "enable_symbol_table": self.frontend.enable_symbol_table
            },
            "backend": {
                "backend_type": self.backend.backend_type.value,
                "enable_register_allocation": self.backend.enable_register_allocation,
                "enable_optimization": self.backend.enable_optimization,
                "optimization_level": self.backend.optimization_level.value,
                "enable_debug_info": self.backend.enable_debug_info,
                "target_os": self.backend.target_os,
                "target_arch": self.backend.target_arch
            } if self.backend else None,
            "ir": {
                "enable_ir_generation": self.ir.enable_ir_generation,
                "enable_optimization": self.ir.enable_optimization,
                "enable_constant_folding": self.ir.enable_constant_folding,
                "enable_peephole_optimization": self.ir.enable_peephole_optimization,
                "output_format": self.ir.output_format
            } if self.ir else None,
            "interpreter": {
                "enable_ast_execution": self.interpreter.enable_ast_execution,
                "enable_ir_execution": self.interpreter.enable_ir_execution,
                "enable_debug_mode": self.interpreter.enable_debug_mode,
                "enable_tracing": self.interpreter.enable_tracing
            } if self.interpreter else None,
            "interface_type": self.interface_type.value,
            "code_display_mode": self.code_display_mode.value,
            "output_file": self.output_file,
            "input_file": self.input_file,
            "verbose": self.verbose,
            "debug": self.debug
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductConfig':
        """Cria configuração a partir de dicionário."""
        frontend_data = data.get("frontend", {})
        frontend = FrontendConfig(
            enable_lexer=frontend_data.get("enable_lexer", True),
            enable_parser=frontend_data.get("enable_parser", True),
            enable_semantic_checker=frontend_data.get("enable_semantic_checker", True),
            enable_ast_builder=frontend_data.get("enable_ast_builder", True),
            enable_symbol_table=frontend_data.get("enable_symbol_table", True)
        )
        
        backend = None
        if "backend" in data:
            backend_data = data["backend"]
            backend = BackendConfig(
                backend_type=BackendType(backend_data["backend_type"]),
                enable_register_allocation=backend_data.get("enable_register_allocation", True),
                enable_optimization=backend_data.get("enable_optimization", True),
                optimization_level=OptimizationLevel(backend_data.get("optimization_level", "basic")),
                enable_debug_info=backend_data.get("enable_debug_info", False),
                target_os=backend_data.get("target_os", "linux"),
                target_arch=backend_data.get("target_arch", "x86_64")
            )
        
        ir = None
        if "ir" in data:
            ir_data = data["ir"]
            ir = IRConfig(
                enable_ir_generation=ir_data.get("enable_ir_generation", True),
                enable_optimization=ir_data.get("enable_optimization", True),
                enable_constant_folding=ir_data.get("enable_constant_folding", True),
                enable_peephole_optimization=ir_data.get("enable_peephole_optimization", True),
                output_format=ir_data.get("output_format", "json")
            )
        
        interpreter = None
        if "interpreter" in data:
            interpreter_data = data["interpreter"]
            interpreter = InterpreterConfig(
                enable_ast_execution=interpreter_data.get("enable_ast_execution", True),
                enable_ir_execution=interpreter_data.get("enable_ir_execution", False),
                enable_debug_mode=interpreter_data.get("enable_debug_mode", False),
                enable_tracing=interpreter_data.get("enable_tracing", False)
            )
        
        return cls(
            name=data["name"],
            product_type=ProductType(data["product_type"]),
            description=data["description"],
            version=data["version"],
            frontend=frontend,
            backend=backend,
            ir=ir,
            interpreter=interpreter,
            interface_type=InterfaceType(data.get("interface_type", "terminal")),
            code_display_mode=CodeDisplayMode(data.get("code_display_mode", "show_all")),
            output_file=data.get("output_file"),
            input_file=data.get("input_file"),
            verbose=data.get("verbose", False),
            debug=data.get("debug", False)
        )


# Configurações pré-definidas de produtos
PREDEFINED_PRODUCTS = {
    # Ponto de Variação 1 - Interface: Terminal
    "minipar_compiler_terminal": ProductConfig(
        name="minipar_compiler_terminal",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar com Interface Terminal",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.X86_64,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC
        ),
        ir=IRConfig(
            enable_ir_generation=True,
            enable_optimization=True,
            enable_constant_folding=True,
            enable_peephole_optimization=True,
            output_format="json"
        ),
        interface_type=InterfaceType.TERMINAL,
        code_display_mode=CodeDisplayMode.SHOW_ALL,
        output_file="output.s"
    ),
    
    # Ponto de Variação 1 - Interface: GUI
    "minipar_compiler_gui": ProductConfig(
        name="minipar_compiler_gui",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar com Interface Gráfica",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.X86_64,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC
        ),
        ir=IRConfig(
            enable_ir_generation=True,
            enable_optimization=True,
            enable_constant_folding=True,
            enable_peephole_optimization=True,
            output_format="json"
        ),
        interface_type=InterfaceType.GUI,
        code_display_mode=CodeDisplayMode.SHOW_ALL,
        output_file="output.s"
    ),
    
    # Ponto de Variação 2 - Geração de Código: Mostrar tudo
    "minipar_compiler_show_code": ProductConfig(
        name="minipar_compiler_show_code",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar que mostra código de 3 endereços e assembly ARMv7",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.ARM64,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC,
            target_arch="armv7"
        ),
        ir=IRConfig(
            enable_ir_generation=True,
            enable_optimization=True,
            enable_constant_folding=True,
            enable_peephole_optimization=True,
            output_format="json"
        ),
        interface_type=InterfaceType.TERMINAL,
        code_display_mode=CodeDisplayMode.SHOW_ALL,
        output_file="output.s"
    ),
    
    # Ponto de Variação 2 - Geração de Código: Não mostrar nada
    "minipar_compiler_hide_code": ProductConfig(
        name="minipar_compiler_hide_code",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar que não mostra código gerado",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.X86_64,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC
        ),
        ir=IRConfig(
            enable_ir_generation=True,
            enable_optimization=True,
            enable_constant_folding=True,
            enable_peephole_optimization=True,
            output_format="json"
        ),
        interface_type=InterfaceType.TERMINAL,
        code_display_mode=CodeDisplayMode.HIDE_ALL,
        output_file="output.s"
    ),
    
    # Produtos originais mantidos para compatibilidade
    "minipar_compiler_x86_64": ProductConfig(
        name="minipar_compiler_x86_64",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar para x86_64",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.X86_64,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC
        ),
        output_file="output.s"
    ),
    
    "minipar_compiler_riscv": ProductConfig(
        name="minipar_compiler_riscv",
        product_type=ProductType.COMPILER,
        description="Compilador Minipar para RISC-V",
        version="1.0.0",
        frontend=FrontendConfig(),
        backend=BackendConfig(
            backend_type=BackendType.RISCV,
            enable_optimization=True,
            optimization_level=OptimizationLevel.BASIC
        ),
        output_file="output.s"
    ),
    
    "minipar_interpreter": ProductConfig(
        name="minipar_interpreter",
        product_type=ProductType.INTERPRETER,
        description="Interpretador Minipar",
        version="1.0.0",
        frontend=FrontendConfig(),
        interpreter=InterpreterConfig(
            enable_ast_execution=True,
            enable_debug_mode=True
        )
    ),
    
    "minipar_ir_generator": ProductConfig(
        name="minipar_ir_generator",
        product_type=ProductType.IR_GENERATOR,
        description="Gerador de código intermediário Minipar",
        version="1.0.0",
        frontend=FrontendConfig(),
        ir=IRConfig(
            enable_ir_generation=True,
            enable_optimization=True,
            output_format="json"
        ),
        output_file="output.ir"
    )
}
