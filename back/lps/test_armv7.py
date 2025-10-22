#!/usr/bin/env python3
"""
Teste simples do backend ARMv7
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaces.ir import IRInstruction, IROperation

# Simula uma symbol table simples
class SimpleSymbolTable:
    def __init__(self):
        self.symbols = {}
    
    def allocate_memory(self, size):
        return 0
    
    def declare_symbol(self, name, symbol_type):
        self.symbols[name] = symbol_type
    
    def enter_scope(self, scope_name):
        pass
    
    def exit_scope(self):
        pass
    
    def get_current_scope(self):
        return "global"
    
    def get_memory_layout(self):
        return {}
    
    def get_symbols_in_scope(self, scope):
        return []
    
    def lookup_symbol(self, name):
        return self.symbols.get(name)
    
    def update_symbol(self, name, value):
        self.symbols[name] = value

def test_armv7_backend():
    """Testa o backend ARMv7"""
    try:
        from backends.armv7_backend import ARMv7Backend
        
        # Cria um backend ARMv7
        symbol_table = SimpleSymbolTable()
        backend = ARMv7Backend(symbol_table)
        
        # Cria instruções IR simples
        instructions = [
            IRInstruction(op=IROperation.LOAD_CONST, dest='t0', arg1='5', arg2=None),
            IRInstruction(op=IROperation.LOAD_CONST, dest='t1', arg1='10', arg2=None),
            IRInstruction(op=IROperation.ADD, dest='t2', arg1='t0', arg2='t1'),
            IRInstruction(op=IROperation.LOAD_CONST, dest='t3', arg1='"Hello World"', arg2=None),
        ]
        
        # Gera assembly
        assembly = backend.generate_assembly(instructions)
        print('✅ Backend ARMv7 funcionando!')
        print('Código ARMv7 gerado:')
        print('=' * 50)
        print(assembly)
        print('=' * 50)
        
        return True
        
    except Exception as e:
        print(f'❌ Erro no backend ARMv7: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_armv7_backend()
