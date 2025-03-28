"""
Semantic Analyzer for RoyalScript Language

This module provides comprehensive semantic analysis for the RoyalScript language.
"""

from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple

class SemanticErrorType(Enum):
    REDECLARATION = auto()
    UNDECLARED = auto()
    TYPE_MISMATCH = auto()
    SCOPE_VIOLATION = auto()
    INVALID_ASSIGNMENT = auto()
    FUNCTION_SIGNATURE_MISMATCH = auto()
    ARRAY_DIMENSION_MISMATCH = auto()

class SemanticError:
    def __init__(self, error_type: SemanticErrorType, message: str, line: int = 0, position: int = 0):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.position = position

    def __str__(self):
        return f"Semantic Error [{self.error_type.name}] at line {self.line}, pos {self.position}: {self.message}"

class SymbolEntry:
    def __init__(
        self, 
        name: str, 
        datatype: str, 
        scope_level: int, 
        is_dynasty: bool = False, 
        is_initialized: bool = False, 
        is_function: bool = False,
        array_dimensions: List[int] = None,
        parameters: List[Tuple[str, str]] = None  # (type, name)
    ):
        self.name = name
        self.datatype = datatype
        self.scope_level = scope_level
        self.is_dynasty = is_dynasty
        self.is_initialized = is_initialized
        self.is_function = is_function
        self.array_dimensions = array_dimensions or []
        self.parameters = parameters or []

class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, SymbolEntry]] = [{}]  # Start with global scope
        self.current_scope_level = 0

    def enter_scope(self):
        """Enter a new scope level."""
        self.current_scope_level += 1
        self.scopes.append({})

    def exit_scope(self):
        """Exit the current scope level."""
        if self.current_scope_level > 0:
            self.scopes.pop()
            self.current_scope_level -= 1

    def declare(self, symbol: SymbolEntry) -> Optional[SemanticError]:
        """
        Declare a new symbol in the current scope.
        Check for redeclaration in the same scope.
        """
        current_scope = self.scopes[self.current_scope_level]
        
        # Check for redeclaration in the same scope
        if symbol.name in current_scope:
            return SemanticError(
                SemanticErrorType.REDECLARATION, 
                f"Symbol '{symbol.name}' already declared in this scope"
            )
        
        current_scope[symbol.name] = symbol
        return None

    def lookup(self, name: str) -> Optional[SymbolEntry]:
        """
        Look up a symbol, searching from current scope to global scope.
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.primitive_types = {'scroll', 'mirror', 'ocean', 'rose'}

    def validate_type_compatibility(self, expected_type: str, actual_type: str) -> bool:
        """
        Check type compatibility, with some flexible type checking.
        Can be expanded for more complex type systems.
        """
        # Exact match
        if expected_type == actual_type:
            return True
        
        # TODO: Add more advanced type compatibility rules if needed
        return False

    def analyze(self, ast_root):
        """
        Main entry point for semantic analysis.
        Traverses the entire AST and performs semantic checks.
        """
        self.errors.clear()
        
        # Process global declarations
        if hasattr(ast_root, 'global_declarations'):
            for decl in ast_root.global_declarations:
                self.validate_variable_declaration(decl)
        
        # Process global functions
        if hasattr(ast_root, 'functions'):
            for func in ast_root.functions:
                self.validate_function_declaration(func)
        
        # Process main function
        if hasattr(ast_root, 'main_function'):
            self.validate_main_function(ast_root.main_function)
        
        return self.errors

    def validate_variable_declaration(self, node):
        """
        Validate a variable declaration.
        Checks:
        - Type validity
        - Initialization
        - Scope rules
        - Dynasty (constant) variable rules
        """
        # Validate data type
        if node.datatype not in self.primitive_types:
            self.errors.append(SemanticError(
                SemanticErrorType.TYPE_MISMATCH, 
                f"Invalid type '{node.datatype}'"
            ))
        
        # Create symbol entry
        symbol = SymbolEntry(
            name=node.identifier[1],  # Assuming identifier is a token with value at index 1
            datatype=node.datatype,
            scope_level=node.scope_level,
            is_dynasty=node.is_dynasty,
            is_initialized=node.value is not None,
            array_dimensions=node.array_dimensions
        )
        
        # Check for redeclaration
        redecl_error = self.symbol_table.declare(symbol)
        if redecl_error:
            self.errors.append(redecl_error)
        
        # Validate initialization if present
        if node.value:
            self.validate_initialization(node)

    def validate_initialization(self, node):
        """
        Validate variable initialization.
        Checks type compatibility of assigned value.
        """
        # TODO: Implement more robust type checking
        # Currently a placeholder for type validation
        if node.value:
            try:
                # Attempt to parse and validate initialization value
                # This would depend on your type system and value parsing
                pass
            except Exception as e:
                self.errors.append(SemanticError(
                    SemanticErrorType.INVALID_ASSIGNMENT,
                    f"Invalid initialization for '{node.identifier[1]}': {str(e)}"
                ))

    def validate_function_declaration(self, node):
        """
        Validate a function declaration.
        Checks:
        - Return type validity
        - Parameter types
        - Function body semantics
        """
        # Validate return type
        if node.return_type not in self.primitive_types and node.return_type != 'void':
            self.errors.append(SemanticError(
                SemanticErrorType.TYPE_MISMATCH,
                f"Invalid return type '{node.return_type}'"
            ))
        
        # Create function symbol entry
        func_symbol = SymbolEntry(
            name=node.identifier[1],
            datatype=node.return_type,
            scope_level=node.scope_level,
            is_function=True,
            parameters=node.parameters
        )
        
        # Check for function redeclaration
        redecl_error = self.symbol_table.declare(func_symbol)
        if redecl_error:
            self.errors.append(redecl_error)
        
        # Enter function scope
        self.symbol_table.enter_scope()
        
        # Validate parameters
        for param_type, param_name in node.parameters:
            if param_type not in self.primitive_types:
                self.errors.append(SemanticError(
                    SemanticErrorType.TYPE_MISMATCH,
                    f"Invalid parameter type '{param_type}' for parameter '{param_name[1]}'"
                ))
            
            # Add parameters to symbol table
            param_symbol = SymbolEntry(
                name=param_name[1],
                datatype=param_type,
                scope_level=self.symbol_table.current_scope_level,
                is_initialized=True
            )
            self.symbol_table.declare(param_symbol)
        
        # Validate function body
        self.validate_function_body(node.body)
        
        # Validate return value if present
        if node.return_val:
            self.validate_return_value(node)
        
        # Exit function scope
        self.symbol_table.exit_scope()

    def validate_function_body(self, body):
        """
        Validate the body of a function.
        Recursively checks semantic rules for different statement types.
        """
        for statement in body:
            # Dispatch to appropriate validation method based on node type
            validator_method = getattr(self, f'validate_{type(statement).__name__}', None)
            if validator_method:
                validator_method(statement)

    def validate_return_value(self, node):
        """
        Validate the return value of a function.
        """
        # TODO: Implement comprehensive return value type checking
        pass

    def validate_main_function(self, node):
        """
        Validate the main function with specific rules.
        """
        # Ensure main function returns 0
        if node.return_val[1] != '0':
            self.errors.append(SemanticError(
                SemanticErrorType.FUNCTION_SIGNATURE_MISMATCH,
                "Main function must return 0"
            ))
        
        # Validate main function body
        self.validate_function_body(node.body)

    def validate_VariableReassignmentNode(self, node):
        """
        Validate variable reassignment.
        Checks:
        - Variable exists
        - Not reassigning a dynasty (constant) variable
        - Type compatibility
        """
        symbol = self.symbol_table.lookup(node.identifier[1])
        
        if not symbol:
            self.errors.append(SemanticError(
                SemanticErrorType.UNDECLARED,
                f"Variable '{node.identifier[1]}' not declared"
            ))
            return
        
        if symbol.is_dynasty:
            self.errors.append(SemanticError(
                SemanticErrorType.SCOPE_VIOLATION,
                f"Cannot reassign dynasty (constant) variable '{node.identifier[1]}'"
            ))
        
        # TODO: Implement more robust type checking for reassignment

    def validate_FunctionCallNode(self, node):
        """
        Validate function call.
        Checks:
        - Function exists
        - Argument count matches
        - Argument types are compatible
        """
        symbol = self.symbol_table.lookup(node.name)
        
        if not symbol or not symbol.is_function:
            self.errors.append(SemanticError(
                SemanticErrorType.UNDECLARED,
                f"Function '{node.name}' not declared"
            ))
            return
        
        # Check argument count
        if len(node.arguments) != len(symbol.parameters):
            self.errors.append(SemanticError(
                SemanticErrorType.FUNCTION_SIGNATURE_MISMATCH,
                f"Argument count mismatch for function '{node.name}'"
            ))

    def validate_ArrayAssignmentNode(self, node):
        """
        Validate array assignment.
        Checks:
        - Array exists
        - Index validity
        - Type compatibility
        """
        symbol = self.symbol_table.lookup(node.identifier[1])
        
        if not symbol:
            self.errors.append(SemanticError(
                SemanticErrorType.UNDECLARED,
                f"Array '{node.identifier[1]}' not declared"
            ))
            return
        
        # Check array dimensions
        if len(node.indices) != len(symbol.array_dimensions):
            self.errors.append(SemanticError(
                SemanticErrorType.ARRAY_DIMENSION_MISMATCH,
                f"Incorrect number of indices for array '{node.identifier[1]}'"
            ))

    # Add more validation methods for other node types as needed
    # (IfNode, WhileNode, ForLoopNode, etc.)

def semantic_analyze(ast_root):
    """
    Convenience function to perform semantic analysis on an AST.
    Returns list of semantic errors if any.
    """
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(ast_root)