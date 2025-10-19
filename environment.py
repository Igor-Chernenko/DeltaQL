"""
Environment and scope management for the DataVal interpreter.
Handles variable storage, lookup, and scope chaining.
"""


class Environment:
    """
    Represents a scope/environment for variable bindings.
    Supports nested scopes through parent reference.
    """
    
    def __init__(self, parent=None):
        """
        Initialize a new environment.
        
        Args:
            parent: Parent environment for scope chaining (None for global scope)
        """
        self.parent = parent
        self.variables = {}
    
    def define(self, name, value):
        """
        Define a variable in the current scope.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.variables[name] = value
    
    def get(self, name):
        """
        Get a variable value, searching up the scope chain.
        
        Args:
            name: Variable name
            
        Returns:
            Variable value
            
        Raises:
            NameError: If variable is not defined
        """
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: '{name}'")
    
    def set(self, name, value):
        """
        Set a variable value, searching up the scope chain.
        
        Args:
            name: Variable name
            value: New value
            
        Raises:
            NameError: If variable is not defined
        """
        if name in self.variables:
            self.variables[name] = value
        elif self.parent is not None:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable: '{name}'")
    
    def exists(self, name):
        """
        Check if a variable exists in this scope or parent scopes.
        
        Args:
            name: Variable name
            
        Returns:
            True if variable exists, False otherwise
        """
        if name in self.variables:
            return True
        elif self.parent is not None:
            return self.parent.exists(name)
        else:
            return False

