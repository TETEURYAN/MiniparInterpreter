"""
Interface de linha de comando para a linha de produto de compiladores.

Este módulo implementa o CLI principal que permite construir
diferentes produtos de compilação.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent.parent.parent))

from cli.builder import ProductBuilder
from product_config.product_config import ProductConfig, PREDEFINED_PRODUCTS
from product_config.config_loader import YAMLConfigLoader, JSONConfigLoader


class MiniparCLI:
    """Interface de linha de comando para Minipar."""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.config_loaders = {
            'yaml': YAMLConfigLoader(),
            'json': JSONConfigLoader()
        }
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos."""
        parser = argparse.ArgumentParser(
            prog='minipar',
            description='Linha de Produto de Software para Compiladores Minipar',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemplos de uso:
  minipar build --product minipar_compiler_x86_64 input.mp
  minipar build --product minipar_interpreter input.mp
  minipar build --config config.yaml input.mp
  minipar list-products
  minipar create-config --product minipar_compiler_riscv --output config.yaml
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
        
        # Comando build
        build_parser = subparsers.add_parser('build', help='Constrói um produto de compilação')
        build_parser.add_argument('input_file', help='Arquivo de entrada (.mp)')
        build_parser.add_argument('--product', '-p', help='Nome do produto pré-definido')
        build_parser.add_argument('--config', '-c', help='Arquivo de configuração')
        build_parser.add_argument('--output', '-o', help='Arquivo de saída')
        build_parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
        build_parser.add_argument('--debug', '-d', action='store_true', help='Modo debug')
        
        # Comando list-products
        list_parser = subparsers.add_parser('list-products', help='Lista produtos disponíveis')
        
        # Comando create-config
        config_parser = subparsers.add_parser('create-config', help='Cria arquivo de configuração')
        config_parser.add_argument('--product', '-p', help='Nome do produto base')
        config_parser.add_argument('--output', '-o', required=True, help='Arquivo de saída')
        config_parser.add_argument('--format', '-f', choices=['yaml', 'json'], default='yaml', help='Formato do arquivo')
        
        return parser
    
    def run(self, args: Optional[list] = None) -> int:
        """Executa o CLI."""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 1
            
            if parsed_args.command == 'build':
                return self._handle_build(parsed_args)
            elif parsed_args.command == 'list-products':
                return self._handle_list_products()
            elif parsed_args.command == 'create-config':
                return self._handle_create_config(parsed_args)
            else:
                print(f"Comando desconhecido: {parsed_args.command}")
                return 1
                
        except Exception as e:
            print(f"Erro: {e}")
            return 1
    
    def _handle_build(self, args) -> int:
        """Manipula o comando build."""
        try:
            # Carrega configuração
            config = self._load_config(args)
            
            # Constrói o produto
            builder = ProductBuilder(config)
            output = builder.build(args.input_file)
            
            # Salva a saída
            if args.output or config.output_file:
                builder.save_output(args.output)
                print(f"Produto construído com sucesso: {args.output or config.output_file}")
            else:
                print("Saída:")
                print(output)
            
            return 0
            
        except Exception as e:
            print(f"Erro na construção: {e}")
            return 1
    
    def _handle_list_products(self) -> int:
        """Manipula o comando list-products."""
        print("Produtos disponíveis:")
        print()
        
        for name, config in PREDEFINED_PRODUCTS.items():
            print(f"  {name}")
            print(f"    Tipo: {config.product_type.value}")
            print(f"    Descrição: {config.description}")
            print(f"    Versão: {config.version}")
            if config.backend:
                print(f"    Backend: {config.backend.backend_type.value}")
            if config.interpreter:
                print(f"    Interpretador: Sim")
            if config.ir:
                print(f"    Gerador de IR: Sim")
            print()
        
        return 0
    
    def _handle_create_config(self, args) -> int:
        """Manipula o comando create-config."""
        try:
            # Seleciona configuração base
            if args.product:
                if args.product not in PREDEFINED_PRODUCTS:
                    print(f"Produto não encontrado: {args.product}")
                    return 1
                config = PREDEFINED_PRODUCTS[args.product]
            else:
                # Configuração padrão
                config = ProductConfig(
                    name="custom_product",
                    product_type=config.product_type.COMPILER,
                    description="Produto customizado",
                    version="1.0.0",
                    frontend=config.frontend
                )
            
            # Salva configuração
            loader = self.config_loaders[args.format]
            loader.save_config(config, args.output)
            
            print(f"Configuração salva em: {args.output}")
            return 0
            
        except Exception as e:
            print(f"Erro na criação da configuração: {e}")
            return 1
    
    def _load_config(self, args) -> ProductConfig:
        """Carrega configuração do produto."""
        if args.config:
            # Carrega de arquivo
            config_path = Path(args.config)
            if not config_path.exists():
                raise FileNotFoundError(f"Arquivo de configuração não encontrado: {args.config}")
            
            extension = config_path.suffix.lower()
            if extension == '.yaml' or extension == '.yml':
                loader = self.config_loaders['yaml']
            elif extension == '.json':
                loader = self.config_loaders['json']
            else:
                raise ValueError(f"Formato de configuração não suportado: {extension}")
            
            config = loader.load_config(str(config_path))
            
        elif args.product:
            # Usa produto pré-definido
            if args.product not in PREDEFINED_PRODUCTS:
                raise ValueError(f"Produto não encontrado: {args.product}")
            config = PREDEFINED_PRODUCTS[args.product]
            
        else:
            raise ValueError("Deve especificar --product ou --config")
        
        # Aplica configurações da linha de comando
        if args.output:
            config.output_file = args.output
        if args.verbose:
            config.verbose = True
        if args.debug:
            config.debug = True
        
        return config


def main():
    """Função principal do CLI."""
    cli = MiniparCLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
