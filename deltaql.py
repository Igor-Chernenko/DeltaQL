#!/usr/bin/env python3
"""
DataVal Language Interpreter
Entry point for running DataVal programs.

Usage: python dataval.py <program.dv>
"""

import sys
from lark import Lark, UnexpectedInput
from ast_nodes import ASTTransformer
from interpreter import Interpreter


def main():
    """Main entry point for the DataVal interpreter."""
    if len(sys.argv) != 2:
        print("Usage: python dataval.py <program.dv>")
        sys.exit(1)
    
    program_file = sys.argv[1]
    
    try:
        # Read the program file
        with open(program_file, 'r') as f:
            program_code = f.read()
        
        # Load the grammar
        with open('grammar.lark', 'r') as f:
            grammar = f.read()
        
        # Create parser
        parser = Lark(grammar, start='program', parser='lalr')
        
        # Parse the program
        parse_tree = parser.parse(program_code)
        
        # Transform to AST
        transformer = ASTTransformer()
        ast = transformer.transform(parse_tree)
        
        # Create interpreter and execute
        interpreter = Interpreter()
        interpreter.execute(ast)
        
    except FileNotFoundError as e:
        print(f"Error: File '{program_file}' not found.")
        sys.exit(1)
    except UnexpectedInput as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

