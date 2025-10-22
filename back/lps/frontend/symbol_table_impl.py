"""
Implementação da tabela de símbolos para Minipar.

Implementa a tabela de símbolos seguindo as interfaces da linha de produto.
"""

from typing import Any, Dict, List, Optional
from interfaces.symbol_table import SymbolTable, Symbol, SymbolType, DataType


class MiniparSymbolTable(SymbolTable):
    """Implementação da tabela de símbolos para Minipar."""
    
    def __init__(self):
        self.symbols: Dict[str, List[Symbol]] = {}
        self.scope_stack: List[str] = ["global"]
        self.current_offset = 0
    
    def enter_scope(self, scope_name: str) -> None:
        """Entra em um novo escopo."""
        self.scope_stack.append(scope_name)
        if scope_name not in self.symbols:
            self.symbols[scope_name] = []
    
    def exit_scope(self) -> None:
        """Sai do escopo atual."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    
    def declare_symbol(self, symbol: Symbol) -> None:
        """Declara um novo símbolo."""
        current_scope = self.get_current_scope()
        
        # Verifica se já existe no escopo atual
        if current_scope in self.symbols:
            for existing_symbol in self.symbols[current_scope]:
                if existing_symbol.name == symbol.name:
                    raise ValueError(f"Símbolo já declarado: {symbol.name}")
        
        # Adiciona o símbolo
        if current_scope not in self.symbols:
            self.symbols[current_scope] = []
        
        self.symbols[current_scope].append(symbol)
    
    def lookup_symbol(self, name: str, scope: Optional[str] = None) -> Optional[Symbol]:
        """Busca um símbolo por nome."""
        if scope:
            # Busca no escopo específico
            if scope in self.symbols:
                for symbol in self.symbols[scope]:
                    if symbol.name == name:
                        return symbol
        else:
            # Busca na hierarquia de escopos
            for current_scope in reversed(self.scope_stack):
                if current_scope in self.symbols:
                    for symbol in self.symbols[current_scope]:
                        if symbol.name == name:
                            return symbol
        
        return None
    
    def update_symbol(self, symbol: Symbol) -> None:
        """Atualiza um símbolo existente."""
        current_scope = self.get_current_scope()
        
        if current_scope in self.symbols:
            for i, existing_symbol in enumerate(self.symbols[current_scope]):
                if existing_symbol.name == symbol.name:
                    self.symbols[current_scope][i] = symbol
                    return
        
        # Se não encontrou, declara como novo
        self.declare_symbol(symbol)
    
    def get_symbols_in_scope(self, scope: str) -> List[Symbol]:
        """Retorna todos os símbolos de um escopo."""
        return self.symbols.get(scope, []).copy()
    
    def get_current_scope(self) -> str:
        """Retorna o escopo atual."""
        return self.scope_stack[-1]
    
    def allocate_memory(self, symbol: Symbol) -> int:
        """Aloca memória para um símbolo."""
        offset = self.current_offset
        symbol.location = offset
        
        # Calcula tamanho baseado no tipo
        if symbol.data_type == DataType.INT:
            size = 8  # 8 bytes para inteiros
        elif symbol.data_type == DataType.BOOL:
            size = 1  # 1 byte para booleanos
        elif symbol.data_type == DataType.STRING:
            size = 16  # 16 bytes para strings (assumindo tamanho fixo)
        else:
            size = 8  # Tamanho padrão
        
        symbol.size = size
        self.current_offset += size
        
        return offset
    
    def get_memory_layout(self) -> Dict[str, List[Symbol]]:
        """Retorna o layout de memória por escopo."""
        return self.symbols.copy()
    
    def get_all_symbols(self) -> List[Symbol]:
        """Retorna todos os símbolos de todos os escopos."""
        all_symbols = []
        for scope_symbols in self.symbols.values():
            all_symbols.extend(scope_symbols)
        return all_symbols
    
    def clear(self) -> None:
        """Limpa a tabela de símbolos."""
        self.symbols.clear()
        self.scope_stack = ["global"]
        self.current_offset = 0
    
    def get_scope_hierarchy(self) -> List[str]:
        """Retorna a hierarquia de escopos."""
        return self.scope_stack.copy()
    
    def get_symbol_count(self) -> int:
        """Retorna o número total de símbolos."""
        return sum(len(symbols) for symbols in self.symbols.values())
    
    def get_scope_count(self) -> int:
        """Retorna o número de escopos."""
        return len(self.symbols)
    
    def has_symbol(self, name: str, scope: Optional[str] = None) -> bool:
        """Verifica se um símbolo existe."""
        return self.lookup_symbol(name, scope) is not None
    
    def get_symbols_by_type(self, symbol_type: SymbolType) -> List[Symbol]:
        """Retorna todos os símbolos de um tipo específico."""
        symbols = []
        for scope_symbols in self.symbols.values():
            for symbol in scope_symbols:
                if symbol.symbol_type == symbol_type:
                    symbols.append(symbol)
        return symbols
    
    def get_symbols_by_data_type(self, data_type: DataType) -> List[Symbol]:
        """Retorna todos os símbolos de um tipo de dados específico."""
        symbols = []
        for scope_symbols in self.symbols.values():
            for symbol in scope_symbols:
                if symbol.data_type == data_type:
                    symbols.append(symbol)
        return symbols
