"""
Semantic Analyzer for RoyalScript Language

This module provides comprehensive semantic analysis for the RoyalScript language.
"""

from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple


class SemanticErrorType(Enum):
    Redeclaration = auto()
    Undeclared = auto()
    Type_Mismatch = auto()
    Scope_Violation = auto()
    Invalid_Assignment = auto()
    Function_Signature_Mismatch = auto()
    Array_Dimension_Mismatch = auto()

class SemanticError:
    def __init__(self, error_type: SemanticErrorType, message: str, line: int = 0, position: int = 0):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.position = position

    def __str__(self):
        return f"Semantic Error: {self.message} at Line {self.line}, Index {self.position}."

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
        Check for Redeclaration in the same scope.
        """
        current_scope = self.scopes[self.current_scope_level]
        
        # Check for Redeclaration in the same scope
        if symbol.name in current_scope:
            return SemanticError(
                SemanticErrorType.Redeclaration, 
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
        self.primitive_types = {'treasures', 'scroll', 'mirror', 'ocean', 'rose'}

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
                self.validate_VariableDeclarationNode(decl)
        
        # Process global functions
        if hasattr(ast_root, 'functions'):
            for func in ast_root.functions:
                self.validate_FunctionNode(func)
        
        # Process main function
        if hasattr(ast_root, 'main_function'):
            self.validate_MainFunctionNode(ast_root.main_function)
        
        return self.errors

    def validate_VariableDeclarationNode(self, node):
        """
        Validate a variable declaration.
        Checks:
        - Type validity
        - Initialization
        - Scope rules
        - Dynasty (constant) variable rules
        """
        # Validate data type
        if node.datatype[0] not in self.primitive_types:
            self.errors.append(SemanticError(
                SemanticErrorType.Type_Mismatch, 
                f"Invalid type '{node.datatype[0]}'"
            ))
        
        # Create symbol entry
        symbol = SymbolEntry(
            name=node.identifier[1],  # Assuming identifier is a token with value at index 1
            datatype=node.datatype[0],
            scope_level=node.scope_level,
            is_dynasty=node.is_dynasty,
            is_initialized=node.value is not None,
            array_dimensions=node.array_dimensions
        )
        
        # Check for Redeclaration
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
        datatype = node.datatype[1] # store data type
        print('data_type', datatype)
        
        
        
        if node.value:  
            if node.array_dimensions:
                dimension = len(node.array_dimensions)
                if dimension == 1:
                    num_elements = int(node.array_dimensions[0][1])
                    elements_val = []
                    curly = 0
             
                    for element in node.value:
                        # Only count actual value elements, not separators or brackets
                        if element[0] not in ['{', '}', ',']:
                            elements_val.append(element)
                        
                        # Count nested brackets
                        if element[0] in ['{', '}']:
                            curly += 1

                    # Bracket depth check
                    if curly != 2:
                        raise ValueError(f"Mismatch in array dimensions during initialization, unexpected bracket nesting")
                        
                    # Element count check
                    if len(elements_val) != num_elements :
                        raise ValueError(f"Array size does not match, expected {num_elements} elements but got {len(elements_val)}")
                    
                    return True
                
                elif dimension == 2:
                    num_elements = int(node.array_dimensions[1][1])
                    elements_val = []
                    curly = int(node.array_dimensions[0][1]) * 2
                    count = 0

                    print(num_elements, elements_val, curly)

                    for element in node.value[1:-1]:
                        # Skip separators
                        if element[0] in {',', '{', '}'}:
                            # Handle start of a new nested element
                            if element[0] == '{':
                                count += 1
                                cur_element = []
                            # Handle end of a nested element
                            elif element[0] == '}':
                                if cur_element:
                                    elements_val.append(cur_element)
                                cur_element = []
                                count += 1 
                            continue
                        
                        # Collect actual value elements
                        cur_element.append(element)
                
                    # Bracket depth check
                    if curly != count:
                        raise ValueError(f"Mismatch in array dimensions during initialization, declared {int(curly /2)} initialized {int(count/2)}")
                    
                    for element in elements_val:
                        if num_elements != len(element):
                            raise ValueError(f"Array size does not match, expected {num_elements} elements but got {len(elements_val)}")

                    return True
                
                else:
                    self.errors.append(SemanticError(
                        SemanticErrorType.Invalid_Assignment,
                        f"{str(e)}"
                    ))

            try:
                print('data_type ---- ', datatype)
                if datatype == 'treasures':
                    print('enetered treasures')
                    self.validate_treasures( node.value, datatype, node)
                elif datatype == 'ocean':
                    self.validate_ocean(node.value, datatype, node)
                elif datatype == 'scroll':
                    self.validate_scroll(node.value, datatype, node)
                elif datatype == 'rose':
                    self.validate_rose(node.value, datatype, node)
                elif datatype == 'mirror':
                    self.validate_mirror(node.value, datatype, node)
            except Exception as e:
                self.errors.append(SemanticError(
                    SemanticErrorType.Invalid_Assignment,
                    f"{str(e)}"
                ))


    #============================= Value validation based on data type =================================#

    def validate_treasures(self, value, datatype, node):
        print('entered validate treasuress', value)
        value_type = value[0][0]
        content = [] 

        print(value_type, value)

        for val in value:   
            content.append(val[1]) 

        # determine if the value is an expression and what type of expression
        value_string = ' '.join(content)
        expr_type = self.type_expr(content)

        print('expression', expr_type, content, value, value_string,)

        if expr_type == 'arithmetic':
            return True

        elif expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type in ['treasures_lit', '1', '0']:
                return True 

            elif value_type == 'totreasures':
                self.validate_conversion_func(value, datatype)

            elif value_type == 'identifier':
                self.validate_id(value, datatype, node)

            elif value_type == 'wish':
                return True
            
            elif value_type == 'phantom':
                return True
            
            else:
                raise ValueError(f"Invalid treasures initialization <{value_string}> ")
        
        else:
            raise ValueError(f"Invalid treasures initialization <{value_string}> ")
        


    def validate_conversion_func(self, value, value_type):
        val = value[2]

        # totreasures
        if value_type == 'treasures':
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0', 'mirror_lit']:
                return True
            elif val[0] == 'scroll_lit':
                if val[1][1:-1].isdigit() or (val[1][1:-1].startswith('-') and val[1][2:-1].isdigit()):
                    return True
                else:
                    raise ValueError(f"Invalid value <{val[1]}> for type conversion totreasure")
            elif val[0] == 'rose_lit':
                if val[1][1].isdigit():
                    return True
                else:
                    raise ValueError(f"Invalid value <{val[1]}> for type conversion totreasure")
            else:
                raise ValueError(f"Invalid value <{val[1]}> for type conversion totreasure")
        
        #toocean
        elif value_type == 'ocean':
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0']:
                return True
            elif self.is_float(val[1]):
                return True
            else:
                raise ValueError(f"Invalid value <{val[1]}> for type conversion toocean")
        
        #toscroll
        elif value_type == 'scroll':
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0', 'mirror_lit', 'scroll_lit', 'rose_lit']:
                return True
            
        #torose
        elif value_type == 'rose':
            if val[0] == 'treasures_lit':
                if len(val[1]) == 1:
                    return True
            elif val[0] == 'scroll_lit':
                if len(val[1]) == 3:
                    return True
            elif val[0] in ['rose_lit', '1', '0']:
                return True
            else:
                raise ValueError(f"Invalid value <{val[1]}> for type conversion torose")

        #tomirror
        elif value_type == 'mirror':
            if val[0] in ['mirror_lit', '1', '0']:
                return True
            elif val[0] == 'scroll_lit':
                if val[1][1:-1] in ['true', 'false', '1', '0']:
                    return True
            elif val[0] == 'rose_lit':
                if val[1][1] in ['1', '0']:
                    return True
            elif val[0] == 'treasures_lit':
                if val[1] in ['1', '0']:
                    return True
            else:
                raise ValueError(f"Invalid value <{val[1]}> for type conversion tomirror")

    def is_float(self, value_string):
        try:
            float(value_string)
            return True
        except ValueError:
            return False
        
    def validate_id(self, value, datatype, node):
        """
        Validate an identifier used in variable initialization
        
        Args:
            value (list): The identifier value from the AST
            datatype (str): The expected datatype of the variable being initialized
            node: The AST node for additional context
        
        Raises:
            ValueError: If the identifier is invalid or type-incompatible
        """
        # Extract the identifier name
        identifier_name = value[0][1]
        
        # Look up the symbol in the symbol table
        symbol_entry = self.symbol_table.lookup(identifier_name)
        
        # Check if the identifier is declared
        if not symbol_entry or identifier_name == node.identifier[1]:
            raise ValueError(f"Undeclared identifier '{identifier_name}'")
        
        print(identifier_name, node.identifier[1])
        # If it's a function, perform additional checks
        if symbol_entry.is_function:
            # Check if the function has parameters
            if symbol_entry.parameters:
                
                arguments = []
                # if getattr(node, 'Arguments', None) is None:
                #     param_details = ", ".join([f"{param[0][0]} {param[1][1]}" for param in symbol_entry.parameters])
                #     raise ValueError(f"Function '{identifier_name}' requires arguments: ({param_details})")

                for val in node.value[1:-1]:
                    if val[0] not in ['(', ',', ')']:
                        arguments.append(val)
            

                print('++++++++++++',len(symbol_entry.parameters))
                print('----------------',len(arguments), arguments)
                
                # Validate number of arguments
                if len(arguments) == 0:
                    param_details = ", ".join([f"{param[0][0]} {param[1][1]}" for param in symbol_entry.parameters])
                    raise ValueError(f"Function '{identifier_name}' requires arguments: ({param_details})")
                
                # Check if argument count matches parameter count
                if len(arguments) != len(symbol_entry.parameters):
                    raise ValueError(f"Function '{identifier_name}' requires {len(symbol_entry.parameters)} arguments but got {len(arguments)}")
                
                # Validate argument types
                for i, param in enumerate(symbol_entry.parameters):
                    expected_type = param[0][0]  # First element of the first tuple is the type
                    arg = arguments[i]
        
                    # Type-specific validation
                    try:
                        if expected_type == 'treasures':
                            self.validate_treasures([arg], expected_type, node)
                        elif expected_type == 'ocean':
                            self.validate_ocean([arg], expected_type, node)
                        elif expected_type == 'scroll':
                            self.validate_scroll([arg], expected_type, node)
                        elif expected_type == 'rose':
                            self.validate_rose([arg], expected_type, node)
                        elif expected_type == 'mirror':
                            self.validate_mirror([arg], expected_type, node)
                    except ValueError as e:
                        raise ValueError(f"Invalid argument for function '{identifier_name}': {str(e)}")
            
            # Ensure function return type matches the variable type
            if symbol_entry.datatype[0] == 'chamber':
                raise ValueError(f"Cannot initialize variable '{node.identifier[1]}' with chamber function '{identifier_name}'")
            
            # Additional check for return type compatibility
            if symbol_entry.datatype[0] != datatype:
                raise ValueError(f"Function '{identifier_name}' returns {symbol_entry.datatype[1]}, but expected {datatype}")
                    

        # # If it's an array, perform array-specific checks
        # if symbol_entry.array_dimensions:
        #     # If the identifier is used as an array, it should have index specifications
        #     # This is a placeholder - you'd need to add more complex array indexing validation
        #     if len(value) < 2 or value[1][0] != 'array_access':
        #         raise ValueError(f"Array '{identifier_name}' must be accessed with indices")
            
        #     # Validate array index types and dimensions
        #     # This is a simplified check and can be expanded
        #     array_indices = value[1][1:]
        #     if len(array_indices) != len(symbol_entry.array_dimensions):
        #         raise ValueError(f"Incorrect number of indices for array '{identifier_name}'")
            
        # # Check if the identifier is initialized
        # if not symbol_entry.is_initialized:
        #     raise ValueError(f"Uninitialized identifier '{identifier_name}'")
        
        # # Check type compatibility
        # if not self.validate_type_compatibility(datatype, symbol_entry.datatype):
        #     raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype}")
        
        return True
        

    #===================================================================================================#

    def validate_FunctionNode(self, node):
        """
        Validate a function declaration.
        Checks:
        - Return type validity
        - Parameter types
        - Function body semantics
        """
        # Validate return type
        if node.return_type[0] not in self.primitive_types and node.return_type[0] != 'chamber':
            self.errors.append(SemanticError(
                SemanticErrorType.Type_Mismatch,
                f"Invalid return type '{node.return_type[0]}'"
            ))
        
        # Create function symbol entry
        func_symbol = SymbolEntry(
            name=node.identifier[1],
            datatype=node.return_type,
            scope_level=node.scope_level,
            is_function=True,
            parameters=node.parameters
        )
        
        # Check for function Redeclaration
        redecl_error = self.symbol_table.declare(func_symbol)
        if redecl_error:
            self.errors.append(redecl_error)
        
        # Enter function scope
        self.symbol_table.enter_scope()
        
        # Validate parameters
        for param_type, param_name in node.parameters:
            if param_type[0] not in self.primitive_types:
                self.errors.append(SemanticError(
                    SemanticErrorType.Type_Mismatch,
                    f"Invalid parameter type '{param_type[0]}' for parameter '{param_name[1]}'"
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

    def validate_MainFunctionNode(self, node):
        """
        Validate the main function with specific rules.
        """
        # Ensure main function returns 0
        if node.return_val[1] != '0':
            self.errors.append(SemanticError(
                SemanticErrorType.Function_Signature_Mismatch,
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
                SemanticErrorType.Undeclared,
                f"Variable '{node.identifier[1]}' not declared"
            ))
            return
        
        if symbol.is_dynasty:
            self.errors.append(SemanticError(
                SemanticErrorType.Scope_Violation,
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
                SemanticErrorType.Undeclared,
                f"Function '{node.name}' not declared"
            ))
            return
        
        # Check argument count
        if len(node.arguments) != len(symbol.parameters):
            self.errors.append(SemanticError(
                SemanticErrorType.Function_Signature_Mismatch,
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
                SemanticErrorType.Undeclared,
                f"Array '{node.identifier[1]}' not declared"
            ))
            return
        
        # Check array dimensions
        if len(node.indices) != len(symbol.array_dimensions):
            self.errors.append(SemanticError(
                SemanticErrorType.Array_Dimension_Mismatch,
                f"Incorrect number of indices for array '{node.identifier[1]}'"
            ))

    # Add more validation methods for other node types as needed
    # (IfNode, WhileNode, ForLoopNode, etc.)


    def type_expr(self, content):
        """
        Analyze the content to determine operation type with complex combination rules.
        
        Args:
            content (list): A list of tokens to analyze
        
        Returns:
            str: The type of operation
        """
        # Remove closing parentheses and '~' if present
        content = [token for token in content if token not in [')', '~']]
        
        # Define operator types
        relational_ops = ['>', '<', '>=', '<=', '==', '!=']
        arithmetic_ops = ['+', '-', '*', '/', '%']
        logical_ops = ['&&', '||', 'and', 'or']
        
        # Check for the presence of each operator type
        has_relational = any(op in content for op in relational_ops)
        has_arithmetic = any(op in content for op in arithmetic_ops)
        has_logical = any(op in content for op in logical_ops)
        
        # Determine operation type based on rules
        if has_logical:
            return 'logical'
        
        if has_relational:
            return 'relational'
        
        if not has_relational and not has_logical and has_arithmetic:
            return 'arithmetic'
        
        # Invalid operation case
        return 'Not Valid'

def semantic_analyze(ast_root):
    """
    Convenience function to perform semantic analysis on an AST.
    Returns list of semantic errors if any.
    """
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(ast_root)