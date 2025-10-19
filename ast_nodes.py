"""
Abstract Syntax Tree node definitions for DeltaQL language.
"""

from lark import Transformer, Token
from dataclasses import dataclass
from typing import Any, List, Optional


# Base AST Node
@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


# Program
@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List[ASTNode]


# Statements
@dataclass
class VarDecl(ASTNode):
    """Variable declaration: var x = expr"""
    name: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    """Assignment: x = expr"""
    name: str
    value: ASTNode


@dataclass
class FunctionDef(ASTNode):
    """Function definition: function name(params) { body }"""
    name: str
    parameters: List[str]
    body: List[ASTNode]


@dataclass
class IfStatement(ASTNode):
    """If statement: if condition { then_block } else { else_block }"""
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None


@dataclass
class ForLoop(ASTNode):
    """For loop: for var in iterable { body }"""
    var_name: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    """Return statement: return expr"""
    value: Optional[ASTNode] = None


@dataclass
class ExprStatement(ASTNode):
    """Expression statement (e.g., function call)"""
    expression: ASTNode


# Expressions
@dataclass
class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """Unary operation: op operand"""
    operator: str
    operand: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """Function call: name(args)"""
    name: str
    arguments: List[ASTNode]


@dataclass
class Identifier(ASTNode):
    """Variable reference"""
    name: str


@dataclass
class Literal(ASTNode):
    """Literal value (number, string, boolean)"""
    value: Any


@dataclass
class ListLiteral(ASTNode):
    """List literal: [expr, expr, ...]"""
    elements: List[ASTNode]


@dataclass
class IndexAccess(ASTNode):
    """Index access: object[index]"""
    object: ASTNode
    index: ASTNode


# Transformer to convert Lark parse tree to AST
class ASTTransformer(Transformer):
    """Transforms Lark parse tree into AST."""
    
    def program(self, statements):
        return Program(statements=list(statements))
    
    def var_decl(self, items):
        name = items[0].value
        value = items[1]
        return VarDecl(name=name, value=value)
    
    def assignment(self, items):
        name = items[0].value
        value = items[1]
        return Assignment(name=name, value=value)
    
    def function_def(self, items):
        name = items[0].value
        # Check if parameters exist
        if isinstance(items[1], list) and all(isinstance(p, str) for p in items[1]):
            parameters = items[1]
            body = items[2:]
        else:
            parameters = []
            body = items[1:]
        return FunctionDef(name=name, parameters=parameters, body=list(body))
    
    def parameters(self, items):
        return [item.value for item in items]
    
    def if_stmt(self, items):
        condition = items[0]
        # Find where then_block ends and else_block begins
        then_block = []
        else_block = None
        
        i = 1
        # Collect then_block statements
        while i < len(items) and isinstance(items[i], ASTNode):
            then_block.append(items[i])
            i += 1
        
        return IfStatement(condition=condition, then_block=then_block, else_block=else_block)
    
    def for_stmt(self, items):
        var_name = items[0].value
        iterable = items[1]
        body = items[2:]
        return ForLoop(var_name=var_name, iterable=iterable, body=list(body))
    
    def return_stmt(self, items):
        value = items[0] if items else None
        return ReturnStatement(value=value)
    
    def expr_stmt(self, items):
        return ExprStatement(expression=items[0])
    
    # Expressions
    def logical_or(self, items):
        result = items[0]
        for i in range(1, len(items)):
            result = BinaryOp(left=result, operator="or", right=items[i])
        return result
    
    def logical_and(self, items):
        result = items[0]
        for i in range(1, len(items)):
            result = BinaryOp(left=result, operator="and", right=items[i])
        return result
    
    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        i = 1
        while i < len(items):
            op = items[i].value if isinstance(items[i], Token) else items[i]
            right = items[i + 1]
            result = BinaryOp(left=result, operator=op, right=right)
            i += 2
        return result
    
    def addition(self, items):
        result = items[0]
        i = 1
        while i < len(items):
            op = items[i].value if isinstance(items[i], Token) else items[i]
            right = items[i + 1]
            result = BinaryOp(left=result, operator=op, right=right)
            i += 2
        return result
    
    def multiplication(self, items):
        result = items[0]
        i = 1
        while i < len(items):
            op = items[i].value if isinstance(items[i], Token) else items[i]
            right = items[i + 1]
            result = BinaryOp(left=result, operator=op, right=right)
            i += 2
        return result
    
    def unary(self, items):
        if len(items) == 1:
            return items[0]
        op = items[0].value if isinstance(items[0], Token) else items[0]
        return UnaryOp(operator=op, operand=items[1])
    
    def postfix(self, items):
        """Handle index access: obj[index]"""
        result = items[0]
        # Process any index accesses
        for i in range(1, len(items)):
            index = items[i]
            result = IndexAccess(object=result, index=index)
        return result
    
    def function_call(self, items):
        name = items[0].value
        arguments = items[1] if len(items) > 1 else []
        return FunctionCall(name=name, arguments=arguments)
    
    def arguments(self, items):
        return list(items)
    
    def list_literal(self, items):
        return ListLiteral(elements=list(items))
    
    def identifier(self, items):
        return Identifier(name=items[0].value)
    
    def number(self, items):
        value = items[0].value
        # Convert to int or float
        if '.' in value:
            return Literal(value=float(value))
        else:
            return Literal(value=int(value))
    
    def string(self, items):
        # Remove quotes
        value = items[0].value[1:-1]
        # Handle escape sequences
        value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'")
        return Literal(value=value)
    
    def true(self, items):
        return Literal(value=True)
    
    def false(self, items):
        return Literal(value=False)

