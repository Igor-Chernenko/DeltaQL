#!/usr/bin/env python3
"""
DeltaQL Language Interpreter
Entry point for running DeltaQL programs.

Usage: python deltaql.py <program.dql>
"""

import sys
import os
from lark import Lark, UnexpectedInput
from ast_nodes import ASTTransformer
from interpreter import Interpreter


def main():
    """Main entry point for the DeltaQL interpreter."""
    if len(sys.argv) != 2:
        print("Usage: python deltaql.py <program.dql>")
        sys.exit(1)
    
    program_file = sys.argv[1]
    
    # Normalize the path for the current OS
    program_file = os.path.normpath(program_file)
    
    # Check if file exists
    if not os.path.exists(program_file):
        print(f"Error: File '{program_file}' not found.")
        print(f"Current directory: {os.getcwd()}")
        print(f"Looking for absolute path: {os.path.abspath(program_file)}")
        print("\nTrying to diagnose:")
        
        # Check if demo directory exists
        if os.path.exists('demo'):
            print("✓ demo directory exists")
            print(f"  Contents: {os.listdir('demo')}")
        else:
            print("✗ demo directory NOT found")
        
        sys.exit(1)
    
    try:
        # Read the program file
        with open(program_file, 'r', encoding='utf-8') as f:
            program_code = f.read()
        
        # Get the directory of this script to find grammar.lark
        script_dir = os.path.dirname(os.path.abspath(__file__))
        grammar_path = os.path.join(script_dir, 'grammar.lark')
        
        # Load the grammar
        if not os.path.exists(grammar_path):
            print(f"Error: grammar.lark not found at {grammar_path}")
            sys.exit(1)
            
        with open(grammar_path, 'r', encoding='utf-8') as f:
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
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except UnexpectedInput as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

