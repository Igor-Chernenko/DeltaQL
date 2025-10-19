"""
Core interpreter for DataVal language.
Implements visitor pattern to execute AST nodes.
"""

from ast_nodes import *
from environment import Environment
from builtin import get_builtins


class ReturnException(Exception):
    """Exception used to handle return statements."""
    def __init__(self, value):
        self.value = value


class Interpreter:
    """Main interpreter class that executes DataVal programs."""
    
    def __init__(self):
        """Initialize the interpreter with global environment."""
        self.global_env = Environment()
        self.current_env = self.global_env
        
        # Register built-in functions
        builtins = get_builtins()
        for name, func in builtins.items():
            self.global_env.define(name, func)
    
    def execute(self, program):
        """
        Execute a DataVal program.
        
        Args:
            program: Program AST node
        """
        if not isinstance(program, Program):
            raise TypeError("Expected Program AST node")
        
        for statement in program.statements:
            self.execute_statement(statement)
    
    def execute_statement(self, stmt):
        """Execute a single statement."""
        if isinstance(stmt, VarDecl):
            self.execute_var_decl(stmt)
        elif isinstance(stmt, Assignment):
            self.execute_assignment(stmt)
        elif isinstance(stmt, FunctionDef):
            self.execute_function_def(stmt)
        elif isinstance(stmt, IfStatement):
            self.execute_if_stmt(stmt)
        elif isinstance(stmt, ForLoop):
            self.execute_for_loop(stmt)
        elif isinstance(stmt, ReturnStatement):
            self.execute_return(stmt)
        elif isinstance(stmt, ExprStatement):
            self.evaluate_expression(stmt.expression)
        else:
            raise TypeError(f"Unknown statement type: {type(stmt)}")
    
    def execute_var_decl(self, stmt):
        """Execute variable declaration."""
        value = self.evaluate_expression(stmt.value)
        self.current_env.define(stmt.name, value)
    
    def execute_assignment(self, stmt):
        """Execute assignment statement."""
        value = self.evaluate_expression(stmt.value)
        self.current_env.set(stmt.name, value)
    
    def execute_function_def(self, stmt):
        """Execute function definition (store in environment)."""
        # Store the function definition as a closure
        function_obj = {
            'type': 'user_function',
            'parameters': stmt.parameters,
            'body': stmt.body,
            'closure_env': self.current_env  # Capture current environment
        }
        self.current_env.define(stmt.name, function_obj)
    
    def execute_if_stmt(self, stmt):
        """Execute if statement."""
        condition = self.evaluate_expression(stmt.condition)
        
        if self.is_truthy(condition):
            for s in stmt.then_block:
                self.execute_statement(s)
        elif stmt.else_block:
            for s in stmt.else_block:
                self.execute_statement(s)
    
    def execute_for_loop(self, stmt):
        """Execute for loop."""
        iterable = self.evaluate_expression(stmt.iterable)
        
        if not isinstance(iterable, list):
            raise TypeError(f"Cannot iterate over {type(iterable).__name__}")
        
        # Create new scope for loop
        loop_env = Environment(parent=self.current_env)
        prev_env = self.current_env
        self.current_env = loop_env
        
        try:
            for item in iterable:
                # Bind loop variable
                self.current_env.define(stmt.var_name, item)
                
                # Execute loop body
                for s in stmt.body:
                    self.execute_statement(s)
        finally:
            # Restore previous environment
            self.current_env = prev_env
    
    def execute_return(self, stmt):
        """Execute return statement."""
        value = None
        if stmt.value:
            value = self.evaluate_expression(stmt.value)
        raise ReturnException(value)
    
    def evaluate_expression(self, expr):
        """Evaluate an expression and return its value."""
        if isinstance(expr, Literal):
            return expr.value
        
        elif isinstance(expr, Identifier):
            return self.current_env.get(expr.name)
        
        elif isinstance(expr, ListLiteral):
            return [self.evaluate_expression(e) for e in expr.elements]
        
        elif isinstance(expr, BinaryOp):
            return self.evaluate_binary_op(expr)
        
        elif isinstance(expr, UnaryOp):
            return self.evaluate_unary_op(expr)
        
        elif isinstance(expr, FunctionCall):
            return self.evaluate_function_call(expr)
        
        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")
    
    def evaluate_binary_op(self, expr):
        """Evaluate binary operation."""
        left = self.evaluate_expression(expr.left)
        
        # Short-circuit evaluation for logical operators
        if expr.operator == "and":
            if not self.is_truthy(left):
                return False
            right = self.evaluate_expression(expr.right)
            return self.is_truthy(right)
        
        elif expr.operator == "or":
            if self.is_truthy(left):
                return True
            right = self.evaluate_expression(expr.right)
            return self.is_truthy(right)
        
        # Evaluate right side for other operators
        right = self.evaluate_expression(expr.right)
        
        # Arithmetic operators
        if expr.operator == "+":
            # Support string concatenation and list concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            elif isinstance(left, list) and isinstance(right, list):
                return left + right
            else:
                return left + right
        elif expr.operator == "-":
            return left - right
        elif expr.operator == "*":
            return left * right
        elif expr.operator == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        
        # Comparison operators
        elif expr.operator == "==":
            return left == right
        elif expr.operator == "!=":
            return left != right
        elif expr.operator == "<":
            return left < right
        elif expr.operator == ">":
            return left > right
        elif expr.operator == "<=":
            return left <= right
        elif expr.operator == ">=":
            return left >= right
        
        else:
            raise ValueError(f"Unknown operator: {expr.operator}")
    
    def evaluate_unary_op(self, expr):
        """Evaluate unary operation."""
        operand = self.evaluate_expression(expr.operand)
        
        if expr.operator == "not":
            return not self.is_truthy(operand)
        elif expr.operator == "-":
            return -operand
        else:
            raise ValueError(f"Unknown unary operator: {expr.operator}")
    
    def evaluate_function_call(self, expr):
        """Evaluate function call."""
        # Get function object
        func = self.current_env.get(expr.name)
        
        # Evaluate arguments
        args = [self.evaluate_expression(arg) for arg in expr.arguments]
        
        # Check if it's a built-in function
        if callable(func):
            try:
                return func(*args)
            except Exception as e:
                raise RuntimeError(f"Error in built-in function '{expr.name}': {e}")
        
        # User-defined function
        elif isinstance(func, dict) and func.get('type') == 'user_function':
            parameters = func['parameters']
            body = func['body']
            closure_env = func['closure_env']
            
            # Check argument count
            if len(args) != len(parameters):
                raise TypeError(f"Function '{expr.name}' expects {len(parameters)} arguments, got {len(args)}")
            
            # Create new environment for function execution
            func_env = Environment(parent=closure_env)
            
            # Bind parameters to arguments
            for param, arg in zip(parameters, args):
                func_env.define(param, arg)
            
            # Save current environment and switch to function environment
            prev_env = self.current_env
            self.current_env = func_env
            
            try:
                # Execute function body
                for stmt in body:
                    self.execute_statement(stmt)
                # If no return statement, return None
                return None
            except ReturnException as ret:
                return ret.value
            finally:
                # Restore previous environment
                self.current_env = prev_env
        
        else:
            raise TypeError(f"'{expr.name}' is not a function")
    
    def is_truthy(self, value):
        """
        Determine if a value is truthy.
        False and 0 are falsy, everything else is truthy.
        """
        if isinstance(value, bool):
            return value
        elif value == 0 or value == "" or value == [] or value is None:
            return False
        else:
            return True

