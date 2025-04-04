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

class SemanticError(Exception):
    def __init__(self, error_type: SemanticErrorType, message: str, line: int = 0, position: int = 0):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.position = position

    def __str__(self):
        return f"Semantic Error: {self.message}" #at Line {self.line}, Index {self.position}."

class SymbolEntry:
    def __init__(
        self, 
        name: str, 
        datatype: str,
        value: str, 
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
        self.value = value
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
        self.errors.clear()
        try:
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
        
        except SemanticError as e:
            # As soon as we encounter the FIRST semantic error,
            # we can store it (if you want to show it somewhere),
            # or just re-raise, or do both:
            self.errors.append(e.semantic_error)
            
            # Stop immediately—no more analysis
            # Optionally re-raise if you want the caller to handle it:
            # raise
        
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
            value=node.value,
            scope_level=node.scope_level,
            is_dynasty=node.is_dynasty,
            is_initialized=node.value is not None,
            array_dimensions=node.array_dimensions
        )
        
        # Check for Redeclaration
        redecl_error = self.symbol_table.declare(symbol)
        if redecl_error:
            self.errors.append(redecl_error)

        # if array required may value
        if node.array_dimensions:
            if not node.value:
                raise ValueError(f"Array '{node.identifier[1]}' must be initialized with values during declaration.")
        
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

                        if element[0] == 'identifier':
                            raise ValueError(f"Mismatch in array dimensions during initialization, declared as 1-dimension array but initialized as 2-dimension array")
                        

                    print('curly ===================', curly)
                    # Bracket depth check
                    if curly != 2:
                        raise ValueError(f"Mismatch in array dimensions during initialization, declared as 1-dimension array but initialized as 2-dimension array")
                    
                    # Element count check
                    if len(elements_val) != num_elements :
                        raise ValueError(f"Array size does not match, expected {num_elements} elements but got {len(elements_val)}")
                    
                    print(elements_val, '-------------------------')
                    for element in elements_val:
                        # Type-specific validation
                        print(element, '+++++++++++++++++++++++++++', node.datatype)
                        try:
                            if node.datatype[0] == 'treasures':
                                self.validate_treasures([element], node.datatype[0], node)
                            elif node.datatype[0] == 'ocean':
                                self.validate_ocean([element], node.datatype[0], node)
                            elif node.datatype[0] == 'scroll':
                                self.validate_scroll([element], node.datatype[0], node)
                            elif node.datatype[0] == 'rose':
                                self.validate_rose([element], node.datatype[0], node)
                            elif node.datatype[0] == 'mirror':
                                self.validate_mirror([element], node.datatype[0], node)
                        except ValueError as e:
                            self.errors.append(SemanticError(
                                SemanticErrorType.Invalid_Assignment,
                                f"{str(e)}"
                            ))
                    
                    return True
                
                elif dimension == 2:
                    num_elements = int(node.array_dimensions[1][1])
                    elements_val = []
                    curly = int(node.array_dimensions[0][1]) * 2
                    cur_element = []
                    count = 0
                    id_elements = 0

                    print(num_elements, elements_val, curly)

                    
                    for element in node.value[1:-1]:
                        # Check if the element is a tuple and has at least one item
                        if isinstance(element, tuple) and len(element) > 0:
                            # Handle separators - note element[0] is now properly checked as a tuple's first item
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
                            # Handle identifiers - moved outside the separator check
                            elif element[0] == 'identifier':
                                elements_val.append(element)
                                count += 2
                                continue
                            
                            # Collect actual value elements (only if not a separator or identifier)
                            cur_element.append(element)

                    # Check if there's a remaining cur_element to add at the end
                    if cur_element:
                        elements_val.append(cur_element)

                    # Bracket depth check
                    if curly != count:
                        self.errors.append(SemanticError(
                                SemanticErrorType.Invalid_Assignment,
                                f"Mismatch in array size during initialization, declared as {int(curly/2)} row but as initialized {int(count/2)} row"))
                        

                    print(elements_val, "++++++++++++++++++++++")

                    for element in elements_val:
                        if element[0] == 'identifier':
                            id = element[1]
                            symbol_entry = self.symbol_table.lookup(id)
        
                            # Check if the identifier is declared
                            if not symbol_entry or id == node.identifier[1]:
                                raise ValueError(f"Undeclared identifier '{id}'")
                            
                            if symbol_entry.datatype != node.datatype[1]:
                                raise ValueError(f"Mismatched data type. Expected {node.datatype[1]} but got {symbol_entry.datatype} array.")
                            
                            if not symbol_entry.array_dimensions:
                                raise ValueError(f"Invalid array value '{id}', must be an array list")
                            
                            if len(symbol_entry.array_dimensions) != 1:
                                raise ValueError(f"Invalid ID format. Expected 1-dimensional array but received 2-dimensional array.")
                            
                            if num_elements != int(symbol_entry.array_dimensions[0][1]):
                                raise ValueError(f"ID index mismatch. The provided index '{symbol_entry.array_dimensions[0][1]}' does not match the expected '{num_elements}' initialization variable.")
                            

                            # id_elements += int(symbol_entry.array_dimensions[0][1])
                        elif element[0] != 'identifier':
                            for elem in element:
                                try:
                                    if node.datatype[0] == 'treasures':
                                        self.validate_treasures([elem], node.datatype[0], node)
                                    elif node.datatype[0] == 'ocean':
                                        self.validate_ocean([elem], node.datatype[0], node)
                                    elif node.datatype[0] == 'scroll':
                                        self.validate_scroll([elem], node.datatype[0], node)
                                    elif node.datatype[0] == 'rose':
                                        self.validate_rose([elem], node.datatype[0], node)
                                    elif node.datatype[0] == 'mirror':
                                        self.validate_mirror([elem], node.datatype[0], node)
                                except ValueError as e:
                                    self.errors.append(SemanticError(
                                        SemanticErrorType.Invalid_Assignment,
                                        f"{str(e)}"
                                    ))

                        if num_elements != len(element):
                            self.errors.append(SemanticError(
                                SemanticErrorType.Invalid_Assignment,
                                f"Array size does not match, expected {num_elements} elements but got {len(element)}")) 

                    return True

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
            self.validate_arithmetic(value, datatype, node)

        elif expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type in ['treasures_lit', '1', '0']:
                return True 

            elif value_type == 'totreasures':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                if len(value) > 1:
                    if value[1][0] in ['++', '--']:
                        self.unary(value, datatype, node, True)
                self.validate_id(value, datatype, node, "Not_expr")

            elif value_type == 'wish':
                return True

            elif value_type == 'lengthof':
                self.lengthof(node)

            elif value_type == 'phantom':
                return True
            
            else:
                raise ValueError(f"Invalid treasures initialization '{value_string}' ")
        
        else:
            raise ValueError(f"Invalid treasures initialization '{value_string}' ")

    def validate_ocean(self, value, datatype, node):
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
    
            if value_type == 'ocean_lit':
                return True 

            elif value_type == 'toocean':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                if len(value) > 1:
                    if value[1][0] in ['++', '--']:
                        self.unary(value, datatype, node, True)
                self.validate_id(value, datatype, node, "Not_expr")

            elif value_type == 'wish':
                return True
            
            
            elif value_type == 'phantom':
                return True
            
            else:
                raise ValueError(f"Invalid ocean initialization '{value_string}' ")
        
        else:
            raise ValueError(f"Invalid ocean initialization '{value_string}' ")
        
    
    def validate_scroll(self, value, datatype, node):
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
            self.string_op(content)

        elif expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type == 'scroll_lit':
                return True 

            elif value_type == 'toscroll':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                self.validate_id(value, datatype, node, "Not_expr")

            elif value_type == 'wish':
                return True
        
            elif value_type == 'phantom':
                return True
            
            else:
                raise ValueError(f"Invalid scroll initialization '{value_string}' ")
        
        else:
            raise ValueError(f"Invalid scroll initialization '{value_string}' ")

    def validate_rose(self, value, datatype, node):
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

        if expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type == 'rose_lit':
                return True 

            elif value_type == 'torose':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                self.validate_id(value, datatype, node, "Not_expr")

            elif value_type == 'wish':
                return True
        
            elif value_type == 'phantom':
                return True
            
            else:
                raise ValueError(f"Invalid rose initialization '{value_string}' ")
        
        else:
            raise ValueError(f"Invalid rose initialization '{value_string}' ")
        
    def validate_mirror(self, value, datatype, node):
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

        if expr_type in ['logical', 'relational']:
            return True

        elif expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type == 'mirror_lit':
                return True 
            
            elif value_type in ['1', '0']:
                return True 

            elif value_type == 'tomirror':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                self.validate_id(value, datatype, node)

            elif value_type == 'wish':
                return True
            
            else:
                raise ValueError(f"Invalid mirror initialization '{value_string}' ")
        
        else:
            raise ValueError(f"Invalid mirror initialization '{value_string}' ")

    def validate_conversion_func(self, value, value_type, node):
        val = value[2]

        # totreasures
        if value_type == 'treasures':
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0', 'mirror_lit']:
                return True
            elif val[0] == 'scroll_lit':
                if val[1][1:-1].isdigit() or (val[1][1:-1].startswith('-') and val[1][2:-1].isdigit()):
                    return True
                else:
                    raise ValueError(f"Invalid value '{val[1]}' for type conversion totreasure")
            elif val[0] == 'rose_lit':
                if val[1][1].isdigit():
                    return True
                else:
                    raise ValueError(f"Invalid value '{val[1]}' for type conversion totreasure")
                
            if val[0] == 'identifier':
            # check if nageexist
                identifier_name = value[2][1]
        
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)

                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                # if mirror / treasures
                datatype = symbol_entry.datatype

                if datatype == "mirror":
                    return True

                # if treasures yung val = 1 or 0
                if datatype == "treasures":
                    return True
                
                if datatype == "ocean":
                    return True

                if datatype == "rose":
                    val_rose = symbol_entry.value[0][1].strip("'")
                    if val_rose.isdigit():
                        return True
                    else:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion totreasures")
                
                if datatype == "scroll":
                    val_scroll = symbol_entry.value[0][1].strip('"')
                    if symbol_entry.value[0][1][1:-1].isdigit() or (symbol_entry.value[0][1][1:-1].startswith('-') and symbol_entry.value[0][1][2:-1].isdigit()) or self.is_float(val_scroll):
                        return True
                    else:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion totreasures")

            else:
                raise ValueError(f"Invalid value '{val[1]}' for type conversion totreasure")
        
        #toocean
        
        elif value_type == 'ocean':
            
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0']:
                return True
            if val[0] == "rose_lit":
                if val[1].strip("'") in ["1", "0"]:
                    return True
                raise ValueError(f"Invalid value '{identifier_name}' for type conversion toocean")
            if val[0] == 'scroll_lit':
                self.is_float(val[1])
                return True
            if val[0] == 'identifier':
            # check if nageexist
                identifier_name = value[2][1]
        
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)

                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                # if mirror / treasures
                datatype = symbol_entry.datatype

                if datatype == "mirror":
                    if symbol_entry.value[0][1] not in ["1", "0"]:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion toocean")

                # if treasures yung val = 1 or 0
                if datatype == "treasures":
                    return True
                
                if datatype == "ocean":
                    return True

                if datatype == "rose":
                    val_rose = symbol_entry.value[0][1].strip("'")
                    if val_rose not in ["1", "0"]:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion toocean")
                
                if datatype == "scroll":
                    val_scroll = symbol_entry.value[0][1].strip('"')
                    self.is_float(val_scroll)
            else:
                print(float(val[1]), '----------------------')
                raise ValueError(f"Invalid value '{val[1]}' for type conversion toocean")
        
        #toscroll
        elif value_type == 'scroll':
            if val[0] in ['treasures_lit', 'ocean_lit', '1', '0', 'mirror_lit', 'scroll_lit', 'rose_lit']:
                return True
            if val[0] == 'identifier':
            # check if nageexist
                identifier_name = value[2][1]
        
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)

                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                
                
            
        #torose
        elif value_type == 'rose':
            if val[0] == 'treasures_lit':
                if len(str(val[1])) == 1:
                    return True
                raise ValueError(f"Invalid value '{val[1]}' for type conversion torose")
            elif val[0] == 'scroll_lit':
                if len(val[1]) == 3:
                    return True
                raise ValueError(f"Invalid value '{val[1]}' for type conversion torose")
            elif val[0] in ['rose_lit', '1', '0']:
                return True
            elif val[0] == 'identifier':
                # if if exist
                identifier_name = value[2][1]
        
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)
                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if symbol_entry.datatype == "rose":
                    return True
                
                # if id is scroll
                if symbol_entry.datatype == "scroll":
                    # raise ValueError(f"Invalid value '{identifier_name }' for type conversion torose")
                
                    print(symbol_entry.value)
                    print("[4][1]", value[3][1])

                    if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                    
                    # if id ay may index
                    if value[3][1] != '[':
                        raise ValueError(f"Invalid value '{identifier_name }' for type conversion torose. Must have an index to convert scroll to rose")
                    

                    if value[5][1] == '[':
                        raise ValueError(f"Invalid value '{identifier_name }' for type conversion torose. scroll cannot have a column")
                

                    index = int(value[4][1])

                    symbol_value = symbol_entry.value[0][1].strip('"')
                    print(symbol_value, len(symbol_value))
                    if index >= len(symbol_value):
                        raise ValueError(f"Array index out of bounds. Attempted to access index {index} in an array of size {len(symbol_value)}")
                    
                
                if symbol_entry.datatype == "treasures":
                    if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                    
                    if len(symbol_entry.value[0][1]) != 1:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion torose")
                    

                # if yung index less than the len of the scroll
            else:
                raise ValueError(f"Invalid value '{val[1]}' for type conversion torose")

        #tomirror
        elif value_type == 'mirror':
            if val[0] in ['mirror_lit', '1', '0']:
                return True
            elif val[0] == 'scroll_lit':
                if val[1][1:-1] in ['true', 'false', '1', '0']:
                    return True
                raise ValueError(f"Invalid value '{val[1]}' for type conversion tomirror")
            elif val[0] == 'rose_lit':
                if val[1][1] in ['1', '0']:
                    return True
                raise ValueError(f"Invalid value '{val[1]}' for type conversion tomirror")
            elif val[0] == 'treasures_lit':
                if val[1] in ['1', '0']:
                    return True
                raise ValueError(f"Invalid value '{val[1]}' for type conversion tomirror")
            elif val[0] == 'identifier':
                # check if nageexist
                identifier_name = value[2][1]
        
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)

                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if not symbol_entry.value:
                        raise ValueError(f"Uninitialized identifier '{identifier_name}'")
                # if mirror / treasures
                datatype = symbol_entry.datatype

                if datatype == "mirror":
                    return True

                # if treasures yung val = 1 or 0
                if datatype == "treasures":
                    if symbol_entry.value[0][1] not in ["1", "0"]:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion tomirror")

                if datatype == "rose":
                    val_rose = symbol_entry.value[0][1].strip("'")
                    if val_rose not in ["1", "0"]:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion tomirror")
                
                if datatype == "scroll":
                    val_scroll = symbol_entry.value[0][1].strip('"')
                    if val_scroll not in ['true', 'false', '1', '0']:
                        raise ValueError(f"Invalid value '{identifier_name}' for type conversion tomirror")
                # if 
                
            else:
                raise ValueError(f"Invalid value '{val[1]}' for type conversion tomirror")
        
        else:
                raise ValueError(f"Invalid value '{val[1]}' for type conversion")

    def is_float(self, value_string):

        string = value_string.strip('"').strip("'")
        print(string, '++++++++++++++===========')
        try:
            float(string)
            return True
        except ValueError:
            return False
        
    def string_op(self, content):
        value_string = ' '.join(content)
        # Remove closing parentheses and '~' if present
        content = [token for token in content if token not in [')', '~']]
        
        # Define operator types
        arithmetic_ops = ['-', '*', '/', '%']
        
        # Check for the presence of each operator type
        has_arithmetic = any(op in content for op in arithmetic_ops)
        
        # Determine operation type based on rules
        if has_arithmetic:
           raise ValueError(f"Invalid scroll initialization '{value_string}' ")
        
        return True
    
    def unary(self, value, datatype, node, is_varVal):
        content = [

        ]
        for val in value:   
            content.append(val[1]) 
        value_string = ' '.join(content)

        if is_varVal:
            if value[0][0] == 'identifier':
                # Extract the identifier name
                identifier_name = value[0][1]
                
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)
                
                # Check if the identifier is declared
                if not symbol_entry or identifier_name == node.identifier[1]:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if symbol_entry.datatype != datatype:
                    raise ValueError(f"Invalid {datatype} initialization '{value_string}', requires {datatype} unary operand.")

    def lengthof(self, node):
        value = node.value
        len_val = []

        for val in value:
            if val[1] not in ['lengthof', '(', ')', '[', ']']:
                len_val.append(val[1])

        identifier_name = len_val[0]
        
        # Look up the symbol in the symbol table
        symbol_entry = self.symbol_table.lookup(identifier_name)
        
        if not symbol_entry or identifier_name == node.identifier[1]:
            raise ValueError(f"Undeclared identifier '{identifier_name}'")
        

        # If it's an array, perform array-specific checks
        if symbol_entry.array_dimensions:
            dimensions = 0
            array_size = []
            id_index  = symbol_entry.array_dimensions

            print(node.datatype[1], '==========', symbol_entry.datatype)

            
            # buong array ng yung kinukuhaan ng length
            if len(len_val) == 1:
                return True
                
            for element in node.value[1:]:
                if element[0] not in ['(', ')', 'identifier']:
                    if element[1] == '[':
                        dimensions += 1
                        continue

                    if element[1] != ']':
                        array_size.append(element[1])
            if node.datatype[0] in ['mirror', 'rose', 'treasures', 'ocean']:
                if dimensions != 0:
                    raise ValueError(f"Cannot use array variable '{identifier_name}', datatype {node.datatype[0]} with an index in variable initialization.")

            print(f"array_size before conversion: {array_size}")
            print(f"id_index before conversion: {id_index}")
            #check if pasok yung index and dimensions
            if dimensions != len(id_index):
                if dimensions == 0:
                    raise ValueError(f"Cannot use array variable '{identifier_name}' without an index in variable initialization. Array elements must be accessed using an index")
                raise ValueError(f"Mismatched array dimensions for '{identifier_name}'. Declared as a {len(id_index)}-dimensional array, but used as a {dimensions}-dimensional array.")
            
            if dimensions == 1:
                print('array size', array_size[0], id_index[0][1])
                if int(array_size[0]) >= int(id_index[0][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[0]} in an array of size {id_index[0][1]}")
                
            if dimensions == 2:
                if int(array_size[0]) >= int(id_index[0][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[0]} in an array of size {id_index[0][1]}")
                if int(array_size[1]) >= int(id_index[1][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[1]} in an array of size {id_index[1][1]}")


            print(array_size, dimensions, id_index)
            return True

        # Check type compatibility
        if not self.validate_type_compatibility('scroll', symbol_entry.datatype):
            raise ValueError(f"Invalid lengthof value '{node.identifier[1]}' with a datatype of {node.datatype[1]}, must be a scroll")
            
        # Check if the identifier is initialized
        if not symbol_entry.is_initialized:
            raise ValueError(f"Uninitialized identifier '{identifier_name}'")

        print(len_val)
        return True
    
    def validate_id(self, value, datatype, node, expr_type):
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
            print('1 ==================')
            arguments = []
            for val in node.value[1:-1]:
                    if val[0] not in ['(', ',', ')']:
                        arguments.append(val)
            if symbol_entry.parameters:
                
                    
                # if getattr(node, 'Arguments', None) is None:
                #     param_details = ", ".join([f"{param[0][0]} {param[1][1]}" for param in symbol_entry.parameters])
                #     raise ValueError(f"Function '{identifier_name}' requires arguments: ({param_details})")

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
                    
                    if symbol_entry.datatype[0] == 'chamber':
                        raise ValueError(f"Cannot initialize variable '{node.identifier[1]}' with chamber function '{identifier_name}'")
                    
                    if expr_type == "Arithmetic":
                        # Check type compatibility
                        if symbol_entry.datatype not in ["ocean", "treasures"]:
                            raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype} as arithmetic operand, must be ocean or treasures")
                    
                    if expr_type == "Not_expr":
                        # Additional check for return type compatibility
                        if symbol_entry.datatype[0] != datatype:
                            raise ValueError(f"Function '{identifier_name}' returns {symbol_entry.datatype[1]}, but expected {datatype}")
                    
                return True
            print('false---------', identifier_name)
            has_open = False
            has_close = False
            
            for token_type, token_value in value:
                if token_type == '(' and token_value == '(':
                    has_open = True
                elif token_type == ')' and token_value == ')':
                    has_close = True
            if not has_open and not has_close:
                raise ValueError(f"'{identifier_name}' is defined as a function but is referenced without parentheses in variable initialization. Did you mean to call '{identifier_name}()' ?")
            if len(arguments) != 0:
                raise ValueError(f"Function '{identifier_name}' does not accept arguments but {len(arguments)} were provided")
            # Ensure function return type matches the variable type
            if symbol_entry.datatype[0] == 'chamber':
                raise ValueError(f"Cannot initialize variable '{node.identifier[1]}' with chamber function '{identifier_name}'")
            
            # Additional check for return type compatibility
            if symbol_entry.datatype[0] != datatype:
                raise ValueError(f"Function '{identifier_name}' returns {symbol_entry.datatype[1]}, but expected {datatype}")
            
            return True
        
        print('not a function -----------------', identifier_name)

        # If it's an array, perform array-specific checks
        if symbol_entry.array_dimensions:
            dimensions = 0
            array_size = []
            id_index  = symbol_entry.array_dimensions

            print(node.datatype[1], '==========', symbol_entry.datatype)
            # if expr_type == "Arithmetic":
            #     # Check type compatibility
            #     if symbol_entry.datatype not in ["ocean", "treasures"]:
            #         raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype} as arithmetic operand, must be ocean or treasures")
            
            # if expr_type == "Not_expr":
            #     # if same data type
            if node.datatype[1] != symbol_entry.datatype:
                raise ValueError(f"Invalid treasures initialization of array '{node.identifier[1]}' with a datatype of {node.datatype[1]}")
            
            for element in node.value[1:]:
                if element[1] == '[':
                    dimensions += 1
                    continue

                if element[1] != ']':
                    array_size.append(element[1])

            #check if pasok yung index and dimensions
            if dimensions != len(id_index):
                if dimensions == 0:
                    raise ValueError(f"Cannot use array variable '{identifier_name}' without an index in variable initialization. Array elements must be accessed using an index")
                raise ValueError(f"Mismatched array dimensions for '{identifier_name}'. Declared as a {len(id_index)}-dimensional array, but used as a {dimensions}-dimensional array.")
            
            if dimensions == 1:
                print('array size', array_size[0], id_index[0][1])
                if int(array_size[0]) >= int(id_index[0][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[0]} in an array of size {id_index[0][1]}")
                
            if dimensions == 2:
                if int(array_size[0]) >= int(id_index[0][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[0]} in an array of size {id_index[0][1]}")
                if int(array_size[1]) >= int(id_index[1][1]):
                    raise ValueError(f"Array index out of bounds. Attempted to access index {array_size[1]} in an array of size {id_index[1][1]}")


            print(array_size, dimensions, id_index)
            return True
        
        if len(node.value) > 1:
            if node.value[1][0] in ['(', '[']:
                raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")
        
        if expr_type == "Arithmetic":
            # Check type compatibility
            if symbol_entry.datatype not in ["ocean", "treasures"]:
                raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype} as arithmetic operand, must be ocean or treasures")
            

        # Check type compatibility
        if not self.validate_type_compatibility(datatype, symbol_entry.datatype):
            raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype}")
            
        # Check if the identifier is initialized
        # if not symbol_entry.is_initialized:
        #     raise ValueError(f"Uninitialized identifier '{identifier_name}'")
        
        
        return True
    
    def validate_arithmetic(self, value, datatype, node):
        # result = []
        # i = 0
        # n = len(value)
        
        # while i < n:
        #     token_type, token_value = value[i]
            
        #     # Check if this is an identifier
        #     if token_type == 'identifier':
        #         # Start building up the final string for this identifier
        #         combined = token_value
        #         i += 1
                
        #         # While the next token is an opening bracket or parenthesis,
        #         # consume everything until the matching closing symbol
        #         while i < n and value[i][0] in ['[', '(']:
        #             open_sym_type, open_sym_val = value[i]
                    
        #             # For readability, we'll accumulate everything in bracket_expr
        #             bracket_expr = open_sym_val  # '(' or '['
        #             i += 1
                    
        #             # Determine which closing symbol we need
        #             closing_sym = ')' if open_sym_val == '(' else ']'
                    
        #             # Grab everything until we hit the matching closing symbol or run out
        #             while i < n and value[i][1] != closing_sym:
        #                 bracket_expr += value[i][1]
        #                 i += 1
                    
        #             # If we haven't run out of tokens, add the closing symbol
        #             if i < n and value[i][1] == closing_sym:
        #                 bracket_expr += value[i][1]
        #                 i += 1
                    
        #             # Append this bracket chunk to the identifier
        #             combined += bracket_expr
                
        #         # Store the fully combined result for this identifier
        #         result.append(combined)
            
        #     else:
        #         # Not an identifier, move on
        #         i += 1

        # print('extracted', result)
        # if result:
        #     for res in result:
        #         self.validate_id(res, datatype, node, "Arithmetic")
        
        # return True
        pass

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
                datatype=param_type[0],
                scope_level=self.symbol_table.current_scope_level,
                is_initialized=True
            )
            self.symbol_table.declare(param_symbol)
        
        # Validate function body
        self.validate_function_body(node.body)
        
        # Validate return value if present
        if node.return_type[1] != 'chamber':
            if node.return_val:
                self.validate_return_value(node)
            else:
                raise ValueError(f"A function declared to return '{node.return_type[1]}' must return a value.")
            
        if node.return_type[1] == 'chamber':
            print('enter chamber++++++++++++++++++++===========')
            if node.return_val:
                raise ValueError(f"A function returning 'chamber' cannot return any value.")
        
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
        value = node.return_val
        print(value)
        val_type = value[0][0]
        content = []
        datatype = node.return_type[0]
        print(datatype)

        for val in value:   
            content.append(val[1]) 

        # determine if the value is an expression and what type of expression
        value_string = ' '.join(content)
        expr_type = self.type_expr(content)

        if expr_type == 'assignment':
            return True
        
        if val_type == 'identifier':
            if len(value) > 1:
                if value[1][0] in ['++', '--']:
                    return True

        
        try:
            print('data_type ---- ', datatype)
            if datatype == 'treasures':
                print('enetered treasures')
                self.validate_treasures( value, datatype, node)
            elif datatype == 'ocean':
                self.validate_ocean(value, datatype, node)
            elif datatype == 'scroll':
                self.validate_scroll(value, datatype, node)
            elif datatype == 'rose':
                self.validate_rose(value, datatype, node)
            elif datatype == 'mirror':
                self.validate_mirror(value, datatype, node)
        except Exception as e:
            self.errors.append(SemanticError(
                SemanticErrorType.Invalid_Assignment,
                f"{str(e)}"
            ))
        

        print("++++++++++++++++++++",node.return_val, node.return_type)
        return True


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

        if symbol.array_dimensions:
            raise ValueError(f"Cannot use array variable '{node.identifier[1]}' without an index in variable initialization. Array elements must be accessed using an index")
        
        if not symbol:
            raise ValueError(f"Undeclared identifier '{node.identifier[1]}'")
        
        if symbol.is_dynasty:
            raise ValueError(f"Cannot reassign dynasty (constant) variable '{node.identifier[1]}'")
        
        datatype = symbol.datatype
        if node.expression:
            try:
                print('data_type ---- ', datatype)
                if datatype == 'treasures':
                    print('enetered treasures')
                    self.validate_treasures( node.expression, datatype, node)
                elif datatype == 'ocean':
                    self.validate_ocean(node.expression, datatype, node)
                elif datatype == 'scroll':
                    self.validate_scroll(node.expression, datatype, node)
                elif datatype == 'rose':
                    self.validate_rose(node.expression, datatype, node)
                elif datatype == 'mirror':
                    self.validate_mirror(node.expression, datatype, node)
            except Exception as e:
                self.errors.append(SemanticError(
                    SemanticErrorType.Invalid_Assignment,
                    f"{str(e)}"
                ))


    def validate_FunctionCallNode(self, node):
        """
        Validate function call.
        Checks:
        - Function exists
        - Argument count matches
        - Argument types are compatible
        """
        symbol_entry = self.symbol_table.lookup(node.name)
        
        if not symbol_entry or not symbol_entry.is_function:
            raise ValueError(f"Function '{node.name}' not declared")
        
        identifier_name = node.name

        if symbol_entry.is_function:
             # Check if the function has parameters
            print('1 ==================')
            arguments = []
            flat_args = [item for sublist in node.arguments for item in sublist]
            for val in flat_args:
                if val[0] not in ['(', ',', ')']:
                    arguments.append(val)
            print(arguments,"===========")
            if symbol_entry.parameters:
                
                # if getattr(node, 'Arguments', None) is None:
                #     param_details = ", ".join([f"{param[0][0]} {param[1][1]}" for param in symbol_entry.parameters])
                #     raise ValueError(f"Function '{identifier_name}' requires arguments: ({param_details})")

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

                    print(expected_type, "=============+++")
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
                    
                return True
            print('false---------', identifier_name, len(arguments))

            if len(arguments) != 0:
                raise ValueError(f"Function '{identifier_name}' does not accept arguments but {len(arguments)} were provided")
            
            return True
    
    def validate_UnaryOperationNode(self, node):
        symbol_entry = self.symbol_table.lookup(node.identifier)
        
        if not symbol_entry:
            raise ValueError(f"Undeclared identifier '{node.identifier}'")
        
        if symbol_entry.datatype not in ['treasures', 'ocean']:
            raise ValueError(f"Unary operator requires a numeric operand (treasures or ocean), but received {symbol_entry.datatype} instead.")
        
        return True

    def validate_ArrayAssignmentNode(self, node):
        index = 0
        column = 0
        flat_indices = [item for sublist in node.indices for item in sublist]
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
        datatype = symbol.datatype
        if len(symbol.array_dimensions) == 1:

            if len(flat_indices) != 1:
                raise ValueError(f"Mismatched array dimensions for '{symbol.identifier}'. Declared as a 1-dimensional array, but used as a {len(flat_indices)}-dimensional array.")
            
            if int(flat_indices[0][1]) > int(symbol.array_dimensions[0][1]):
                raise ValueError(f"Array index out of bounds. Attempted to access index {flat_indices[0][1]} in an array of size {symbol.array_dimensions[0][1]}")

            try:
                print('data_type ---- ', datatype)
                if datatype == 'treasures':
                    print('enetered treasures')
                    self.validate_treasures( node.expression, datatype, node)
                elif datatype == 'ocean':
                    self.validate_ocean(node.expression, datatype, node)
                elif datatype == 'scroll':
                    self.validate_scroll(node.expression, datatype, node)
                elif datatype == 'rose':
                    self.validate_rose(node.expression, datatype, node)
                elif datatype == 'mirror':
                    self.validate_mirror(node.expression, datatype, node)
            except Exception as e:
                self.errors.append(SemanticError(
                    SemanticErrorType.Invalid_Assignment,
                    f"{str(e)}"
                ))

        return True

    # di pa nagagawa
    def validate_DoWhileNode(node):
        pass

    def validate_WhileNode(node):
        pass

    def validate_IfNode(node):
        pass

    def validate_ElifNode(node):
        pass

    def validate_ElseNode(node):
        pass

    def validate_IfBreakNode(node):
        pass

    def validate_ElifBreakNode(node):
        pass

    def validate_ElseBreakNode(node):
        pass

    def validate_BreakNode(node):
        pass

    def validate_ContinueNode(node):
        pass

    def validate_ForLoopNode(node):
        pass

    def validate_LiteralNode(node):
        pass

    def validate_OutputNode(node):
        pass


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
        assign_ops = ['+=',  '-=', '/=', '*=', '%=']
        
        # Check for the presence of each operator type
        has_relational = any(op in content for op in relational_ops)
        has_arithmetic = any(op in content for op in arithmetic_ops)
        has_logical = any(op in content for op in logical_ops)
        has_assign = any(op in content for op in assign_ops)
        
        # Determine operation type based on rules
        if has_assign:
            return 'assignment'
        
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