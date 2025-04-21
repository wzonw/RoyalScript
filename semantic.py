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


    def validate_VariableDeclarationNode(self, node, scope_level):
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
            name=node.identifier[1],  
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
            raise ValueError(self.errors)

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

        print('vardec passed ')
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
                self.lengthof(node, 'Not granted')

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
            self.string_op(content, value, node)

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

        if expr_type == 'logical':
            self.validate_logical(value, datatype, node)
        
        elif expr_type == 'relational':
            self.validate_relational(value, datatype, node)

        elif expr_type not in ['logical', 'relational', 'arithmetic']:
    
            if value_type == 'mirror_lit':
                return True 
            
            elif value_type in ['1', '0']:
                return True 

            elif value_type == 'tomirror':
                self.validate_conversion_func(value, datatype, node)

            elif value_type == 'identifier':
                self.validate_id(value, datatype, node, 'Not_expr')

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
        
    def string_op(self, content, value, node):
        value_string = ' '.join(content)
        identifiers= []
        toscrolls = []
        others = []
        i = 0
        n = len(value)

        # Remove closing parentheses and '~' if present
        content = [token for token in content if token not in [')', '~']]
        
        # Define operator types
        arithmetic_ops = ['-', '*', '/', '%']
        
        # Check for the presence of each operator type
        has_arithmetic = any(op in content for op in arithmetic_ops)
        
        # Determine operation type based on rules
        if has_arithmetic:
           raise ValueError(f"Invalid scroll initialization '{value_string}' ")
        
        print(content, value, "=============++++++========")
        
        while i < n:
            token_type, token_value = value[i]
            
            # Check if this is an identifier
            if token_type == 'identifier':
                combined = []
                # Start with the original token value
                combined.append(value[i])
                i += 1
                
                # While the next token is an opening bracket or parenthesis,
                # consume everything until the matching closing symbol
                while i < n and value[i][0] in ['[', '(']:
                    open_sym_type, open_sym_val = value[i]
                    
                    # For readability, we'll accumulate everything in bracket_expr
                    combined.append(value[i])  # '(' or '['
                    i += 1
                    
                    # Determine which closing symbol we need
                    closing_sym = ')' if open_sym_val == '(' else ']'
                    
                    # Grab everything until we hit the matching closing symbol or run out
                    while i < n and value[i][1] != closing_sym:
                        combined.append(value[i])
                        i += 1
                    
                    # If we haven't run out of tokens, add the closing symbol
                    if i < n and value[i][1] == closing_sym:
                        combined.append(value[i])
                        i += 1
                
                # Store the fully combined result for this identifier, preserving the tuple structure
                identifiers.append(combined)

            # Check if this is an toscroll
            elif token_type == 'toscroll':
                combined = []
                # Start with the original token value
                combined.append(value[i])
                i += 1
                
                # While the next token is an opening bracket or parenthesis,
                # consume everything until the matching closing symbol
                while i < n and value[i][0] in ['(']:
                    open_sym_type, open_sym_val = value[i]
                    
                    # For readability, we'll accumulate everything in bracket_expr
                    combined.append(value[i])  # '(' or '['
                    i += 1
                    
                    # Determine which closing symbol we need
                    closing_sym = ')'
                    
                    # Grab everything until we hit the matching closing symbol or run out
                    while i < n and value[i][1] != closing_sym:
                        combined.append(value[i])
                        i += 1
                    
                    # If we haven't run out of tokens, add the closing symbol
                    if i < n and value[i][1] == closing_sym:
                        combined.append(value[i])
                        i += 1
                
                # Store the fully combined result for this identifier, preserving the tuple structure
                toscrolls.append(combined)
            
            elif token_type not in ['+']:
                others.append(value[i])
                i += 1

            else:
                # Not an identifier, move on
                i += 1

        print('extracted', identifiers)
        if identifiers:
            for id in identifiers:
                print("id: ",id)
                self.validate_id(id, ['scroll', 'rose'], node, 'String_op')

        if toscrolls:
            for scroll in toscrolls:
                print("id: ",scroll)
                self.validate_conversion_func(scroll, 'scroll', node)

        if others:
            for other in others:
                print("others: ",other)
                if other[0] not in ['scroll_lit', 'rose_lit']:
                    raise ValueError(f"Invalid string operand '{other[1]}'.")
                
        
        return True
    
        
    def validate_arithmetic(self, value, datatype, node):
        print('entered arith validate')
        result = []
        others = []
        i = 0
        n = len(value)
        
        while i < n:
            token_type, token_value = value[i]
            
            # Check if this is an identifier
            if token_type == 'identifier':
                combined = []
                # Start with the original token value
                combined.append(value[i])
                i += 1
                
                # While the next token is an opening bracket or parenthesis,
                # consume everything until the matching closing symbol
                while i < n and value[i][0] in ['[', '(']:
                    open_sym_type, open_sym_val = value[i]
                    
                    # For readability, we'll accumulate everything in bracket_expr
                    combined.append(value[i])  # '(' or '['
                    i += 1
                    
                    # Determine which closing symbol we need
                    closing_sym = ')' if open_sym_val == '(' else ']'
                    
                    # Grab everything until we hit the matching closing symbol or run out
                    while i < n and value[i][1] != closing_sym:
                        combined.append(value[i])
                        i += 1
                    
                    # If we haven't run out of tokens, add the closing symbol
                    if i < n and value[i][1] == closing_sym:
                        combined.append(value[i])
                        i += 1
                
                # Store the fully combined result for this identifier, preserving the tuple structure
                result.append(combined)

            elif token_type not in ['+', '-', '/', '*', '%', '(', ')']:
                others.append(value[i])
                i += 1

            else:
                # Not an identifier, move on
                i += 1

        print('extracted', result)
        if result:
            for res in result:
                print(res)
                # Check if res contains an opening parenthesis
                if ('(', '(') in res:
                    print(f"Found opening parenthesis in: {res}")
                    self.validate_id(res, datatype, node, 'Arithmetic')
                else:
                    self.validate_id(res, datatype, node, 'Arithmetic')
                    
        if others:
            for other in others:
                print('others:', other)
                if other[0] not in ['treasures_lit', 'ocean_lit', '1', '0']:
                    raise ValueError(f"Invalid arithmetic operand '{other[1]}'.")

        print(n, i, '+++++++++')
        
        return True
    
    def validate_logical(self, value, datatype, node):
        i = 0
        n = len(value)

        operand_log = [] 
        operand = [] 

        while i < n:
            if value[i][0] in ['&&', '||']:
                if operand:
                    operand_log.append(operand)  # Store the left operand
                operand = []  # Reset for right operand
            elif value[i][0] != '!':
                operand.append(value[i])  # Accumulate tokens for this operand
            # You may want to handle the negation case here
            i += 1
        
        # Don't forget to add the last operand
        if operand:
            operand_log.append(operand)
            
        print(operand_log, '+++++++++++++')

        for operand in operand_log:
            is_relational = False
            for op in operand:
                if op[0] in ['>', '<', '<=', '>=', '==', '!=']:
                    is_relational = True

            if is_relational:
                self.validate_relational(op, datatype, node)
            
            else:
                if operand[0][0] == 'identifier':
                    is_Comp, dtype = self.validate_id(operand, ['mirror'], node, 'Relational')
                    if not is_Comp:
                        raise ValueError(f"Invalid logical operand '{operand[0][1]}' with a datatype of '{dtype}'.")
                elif operand[0][0] not in ['mirror_lit', '1', '0']:
                    raise ValueError(f"Invalid logical operand '{operand[0][1]}'")
            
        return True

    
    def validate_relational(self, value, datatype, node):
        i = 0
        n = len(value)
        j = 0
        k = 1
        has_equality = False

        # Arrays to store operands around equality operators
        operand_eq = []  # Will store operands for equality operators
        operand = []     # Temporary storage for current operand
        
        # First pass: Identify equality operations and their operands
        while i < n:
            # If we find an equality operator, store the accumulated operand and reset
            if value[i][0] in ['==', '!=']:
                if operand:  # Only append if we have collected an operand
                    operand_eq.append(operand)  # Store the left operand
                    has_equality = True
                # operand_eq.append([value[i]])  # Store the operator
                operand = []  # Reset for right operand
            else:
                operand.append(value[i])  # Accumulate tokens for this operand
            i += 1
            
        # Don't forget the last operand if there is one
        if operand:
            operand_eq.append(operand)

        print(operand_eq, '=========---------==========', has_equality)

        if has_equality:
            while k < len(operand_eq):
                op1 = operand_eq[j]
                op2 = operand_eq[k]
                is_op1Rel = False
                is_op2Rel = False

                # check if operands are relational exp
                for op in op1:
                    if op[0] in ['>', '<', '<=', '>=']:
                        is_op1Rel = True

                for op in op2:
                    if op[0] in ['>', '<', '<=', '>=']:
                        is_op2Rel = True

                if is_op1Rel or is_op2Rel:
                    # op1 is expr
                    if is_op1Rel and not is_op2Rel:
                        self.validate_relOp(op1, datatype, node)
                        if op2[0][0] == 'identifier':
                            is_Comp, dtype = self.validate_id(op2, ['mirror'], node, 'Relational')
                            if not is_Comp:
                                raise ValueError(f"Invalid operand '{op2[0][1]}' with a datatype of '{dtype}'  for [==, !=].")
                        elif op2[0][0] not in ['mirror_lit', '1', '0']:
                            raise ValueError(f"Invalid operand '{op2[0][1]}' for [==, !=], must be a mirror literal.")
                    
                    #op2 is expr
                    if not is_op1Rel and is_op2Rel:
                        self.validate_relOp(op2, datatype, node)
                        print('enter1 =>>>>>>>>>>>>>')
                        if op1[0][0] == 'identifier':
                            print('enter id =>>>>>>>>>>>>>', op1)
                            is_Comp, dtype = self.validate_id(op1, ['mirror'], node, 'Relational')
                            print('enter2 =>>>>>>>>>>>>>', is_Comp, dtype )
                            if not is_Comp:
                                raise ValueError(f"Invalid operand '{op1[0][1]}' with a datatype of '{dtype}'  for [==, !=].")
                        elif op1[0][0] not in ['mirror_lit', '1', '0']:
                            raise ValueError(f"Invalid operand '{op1[0][1]}' for [==, !=], must be a mirror literal.")
                        

                    #both operand are relational exp 
                    if is_op1Rel and is_op2Rel:
                        self.validate_relOp(op1, datatype, node)
                        self.validate_relOp(op2, datatype, node)

                else:
                    valid_types = ['treasures_lit', 'ocean_lit', '1', '0', 'scroll_lit', 'rose_lit', 'mirror_lit', 'identifier']
            
                    if op1[0][0] not in valid_types:
                        print('here---------------------')
                        raise ValueError(f"Invalid operand '{op1[0][1]}' for [==, !=], operands must be of same datatype.")
                    
                    if op2[0][0] not in valid_types:
                        raise ValueError(f"Invalid operand '{op2[0][1]}' for [==, !=], operands must be of same datatype.")
                    
                    # Check compatibility between operands
                    op1_type = op1[0][0]
                    op2_type = op2[0][0]

                    print('here---------------------', op1, op2)
                    
                    if op1_type != op2_type and op1_type != 'identifier' and op2_type != 'identifier':
                        # Check for numeric types which can be compatible
                        numeric_types = ['treasures_lit', 'ocean_lit']
                        mirror_types = ['mirror_lit']
                        treasures_mirror = ['1', '0']
                        string_types = ['scroll_lit', 'rose_lit']
                        if op1_type in numeric_types and op2_type not in ['treasures_lit', 'ocean_lit', '1', '0']:
                            raise ValueError(f"Incompatible types for comparison: '{op1[0][1]}' and '{op2[0][1]}' ====")
                        elif op1_type in mirror_types and op2_type not in ['mirror_lit', '1', '0']:
                            raise ValueError(f"Incompatible types for comparison: '{op1[0][1]}' and '{op2[0][1]}' -----")
                        elif op1_type in string_types and op2_type not in string_types:
                            raise ValueError(f"Incompatible types for comparison: '{op1[0][1]}' and '{op2[0][1]}' ??????")
                        elif op1_type in treasures_mirror and op2_type not in ['mirror_lit', '1', '0', 'treasures_lit', 'ocean_lit'] :
                            print('here---------------------')
                            raise ValueError(f"Incompatible  types for comparison: '{op1[0][1]}' and '{op2[0][1]}' )))))")
                        
                    # If identifiers, check their types
                    if op1_type == 'identifier' or op2_type == 'identifier':
                        # is_Comp = False
                        # Need to compare their actual types from symbol table
                        print(op1, op2, 'op1 & op2 content =================')
                        if op1_type == 'identifier' and op2_type != 'identifier':
                            is_Comp, dtype = self.validate_id(op1, ['treasures', 'ocean', 'scroll', 'rose', 'mirror'], node, 'Relational')
                            if not is_Comp:
                                raise ValueError(f"Invalid operand '{op1[0][1]}' with a datatype of '{dtype}'  for [==, !=].")
                            if dtype in ['treasures', 'ocean']:
                                if op2_type not in ['ocean_lit', 'treasures_lit', '1', '0']:
                                    raise ValueError(f"Incompatible types for comparison: '{dtype }' identifier and '{op2_type}'")
                            if dtype in ['scroll', 'rose']:
                                if op2_type not in ['scroll_lit', 'rose_lit']:
                                    raise ValueError(f"Incompatible types for comparison: '{dtype }' identifier and '{op2_type}'")
                            if dtype in ['mirror']:
                                if op2_type not in ['mirror_lit', '1', '0']:
                                    raise ValueError(f"Incompatible types for comparison: '{dtype }' identifier and '{op2_type}'")
                            
                        # print(is_Comp)
                        if op1_type != 'identifier' and op2_type == 'identifier':
                            # Need to compare their actual types from symbol table
                            
                            is_Comp, dtype = self.validate_id(op2, ['treasures', 'ocean', 'scroll', 'rose', 'mirror'], node, 'Relational')
                            print('entered ====================', is_Comp)
                            if not is_Comp:
                                raise ValueError(f"Invalid operand '{op2[0][1]}' with a datatype of '{dtype}'  for [==, !=].")
                            if dtype in ['treasures', 'ocean']:
                                if op1_type not in ['ocean_lit', 'treasures_lit', '1', '0']:
                                    raise ValueError(f"Incompatible types for comparison: '{op1_type}' and '{dtype }' identifier")
                            if dtype in ['scroll', 'rose']:
                                if op1_type not in ['scroll_lit', 'rose_lit']:
                                    raise ValueError(f"Incompatible types for comparison: '{op1_type}' and '{dtype }' identifier")
                            if dtype in ['mirror']:
                                if op1_type not in ['mirror_lit', '1', '0']:
                                    raise ValueError(f"Incompatible types for comparison: '{op1_type}' and '{dtype }' identifier")
                        # print(is_Comp)
                        if op1_type == 'identifier' and op2_type == 'identifier':
                            is_Comp1, d1 = self.validate_id(op1, ['treasures', 'ocean', 'scroll', 'rose', 'mirror'], node, 'Relational')
                            if not is_Comp1:
                                raise ValueError(f"Invalid operand '{op1[0][1]}' with a datatype of '{d1}'  for [==, !=].")
                            print('done1 ==>>>>>>>>>>', d1, is_Comp1)
                            is_Comp2, d2 = self.validate_id(op2, ['treasures', 'ocean', 'scroll', 'rose', 'mirror'], node, 'Relational')
                            print('done2 ==>>>>>>>>>>', d2, is_Comp2)
                            if not is_Comp2:
                                raise ValueError(f"Invalid operand '{op2[0][1]}' with a datatype of '{d2}'  for [==, !=].")
                            
                            if d1 in ['treasures', 'ocean']:
                                if d2 not in ['treasures', 'ocean']:
                                    raise ValueError(f"Incompatible types for comparison: '{d1}' and '{d2}'")
                                
                            elif d1 in ['scroll', 'rose']:
                                if d2 not in ['scroll', 'rose']:
                                    raise ValueError(f"Incompatible types for comparison: '{d1}' and '{d2}'")
                            
                            elif d1 in ['mirror']:
                                if d2 not in ['mirror']:
                                    raise ValueError(f"Incompatible types for comparison: '{d1}' and '{d2}'")
                k += 1


        else:
            self.validate_relOp(value, datatype, node)
        return True

    def validate_relOp(self, value, datatype, node):
        print("entered validate relational", value)
        i = 0
        n = len(value)
        
        op1 = None
        operator = None
        op2 = None
        
        while i < n:
            # Parse first operand if not already set
            if op1 is None and i < n:
                if value[i][0] not in ['+', '-', '/', '*', '%', '<', '>', '<=', '>=', '!=', '==', '(', ')']:
                    if value[i][0] == 'identifier':
                        combined = []
                        # Start with the original token value
                        combined.append(value[i])
                        i += 1
                        
                        # While the next token is an opening bracket or parenthesis,
                        # consume everything until the matching closing symbol
                        while i < n and (i < len(value)) and (value[i][0] == '[' or value[i][0] == '('):
                            open_sym = value[i]
                            
                            # For readability, we'll accumulate everything
                            combined.append(open_sym)  # '(' or '['
                            i += 1
                            
                            # Determine which closing symbol we need
                            closing_sym = ')' if open_sym[1] == '(' else ']'
                            
                            # Grab everything until we hit the matching closing symbol or run out
                            while i < n and value[i][1] != closing_sym:
                                combined.append(value[i])
                                i += 1
                            
                            # If we haven't run out of tokens, add the closing symbol
                            if i < n and value[i][1] == closing_sym:
                                combined.append(value[i])
                                i += 1
                        
                        # Store the fully combined result for this identifier
                        op1 = combined
                    else:
                        op1 = [value[i]]
                        i += 1
                else:
                    i += 1
                    continue
            
            # Parse operator if first operand is set
            if op1 is not None and operator is None and i < n:
                if value[i][0] in ['+', '-', '/', '*', '%', '<', '>', '<=', '>=', '!=', '==']:
                    operator = value[i]
                    i += 1
                else:
                    i += 1
                    continue
            
            # Parse second operand if first operand and operator are set
            if op1 is not None and operator is not None and op2 is None and i < n:
                if value[i][0] not in ['+', '-', '/', '*', '%', '<', '>', '<=', '>=', '!=', '==', '(', ')']:
                    if value[i][0] == 'identifier':
                        combined = []
                        # Start with the original token value
                        combined.append(value[i])
                        i += 1
                        
                        # While the next token is an opening bracket or parenthesis,
                        # consume everything until the matching closing symbol
                        while i < n and (i < len(value)) and (value[i][0] == '[' or value[i][0] == '('):
                            open_sym = value[i]
                            
                            # For readability, we'll accumulate everything
                            combined.append(open_sym)  # '(' or '['
                            i += 1
                            
                            # Determine which closing symbol we need
                            closing_sym = ')' if open_sym[1] == '(' else ']'
                            
                            # Grab everything until we hit the matching closing symbol or run out
                            while i < n and value[i][1] != closing_sym:
                                combined.append(value[i])
                                i += 1
                            
                            # If we haven't run out of tokens, add the closing symbol
                            if i < n and value[i][1] == closing_sym:
                                combined.append(value[i])
                                i += 1
                        
                        # Store the fully combined result for this identifier
                        op2 = combined
                    else:
                        op2 = [value[i]]
                        i += 1
                else:
                    i += 1
                    continue
            
            # Validate the expression once we have both operands and an operator
            if op1 is not None and operator is not None and op2 is not None:
                # Print debug info - now we know op1 and op2 exist
                is_Comp = False

                if isinstance(op2, list):
                    print(op2, op1, 'operators==========')
                else:
                    print(op2, op1, 'operators==========')
                    
                # Validate arithmetic operators
                if operator[0] in ['+', '-', '/', '*', '%', '<', '>', '<=', '>=']:
                    valid_numeric_types = ['treasures_lit', 'ocean_lit', '1', '0', 'identifier']
                    dtype1 = ['treasures', 'ocean']
    
                    if op1[0][0] not in valid_numeric_types:
                        raise ValueError(f"Invalid operand '{op1[0][1]}' for '{operator[0]}'.")
              
                    if op2[0][0] not in valid_numeric_types:
                        raise ValueError(f"Invalid operand '{op2[0][1]}' for '{operator[0]}'.")

                    # Validate identifiers
                    if op1[0][0] == 'identifier':
                        is_Comp, dtype = self.validate_id(op1, dtype1, node, 'Relational')
                        if not is_Comp:
                            raise ValueError(f"Invalid operand '{op1[0][1]}' with a  datatype of '{dtype}' for '{operator[0]}'.")

                    if op2[0][0] == 'identifier':
                        is_Comp, dtype = self.validate_id(op2, dtype1, node, 'Relational')
                        if not is_Comp:
                            raise ValueError(f"Invalid operand '{op2[0][1]}' with a datatype of '{dtype}'  for '{operator[0]}'.")
                        
                    op1 = op2
                    operator = None
                    op2 = None
                        
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
        else:
            if value[0][0] == 'identifier':
                # Extract the identifier name
                identifier_name = value[0][1]
                
                # Look up the symbol in the symbol table
                symbol_entry = self.symbol_table.lookup(identifier_name)
                
                # Check if the identifier is declared
                if not symbol_entry:
                    raise ValueError(f"Undeclared identifier '{identifier_name}'")
                
                if symbol_entry.datatype not in ['treasures', 'ocean']:
                    raise ValueError(f"Invalid {datatype} initialization '{value_string}', requires 'treasures or ocean' unary operand.")

    def lengthof(self, node, type):
        if type == 'Granted':
            value = node
        else:
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
        
        print(expr_type, "+++++++", identifier_name)
        # Check if the identifier is declared
        if hasattr(node, 'identifier') and node.identifier is not None:
            if not symbol_entry or identifier_name == node.identifier[1]:
                raise ValueError(f"Undeclared identifier '{identifier_name}'")
        else:
            print('entered 1')
            if not symbol_entry:
                raise ValueError(f"Undeclared identifier '{identifier_name}'")

        
        print(identifier_name, symbol_entry.is_function, '////////////????????')
        
        
        # print(identifier_name, node.identifier[1])
        # If it's a function, perform additional checks
        if symbol_entry.is_function:
            if expr_type == 'Function':
                value = node.return_val
                datatype = node.return_type[0]
     
            # Check if the function has parameters
            print('1 ==================', value)
            arguments = []
            for val in value[1:-1]:
                    if val[0] not in ['(', ',', ')']:
                        arguments.append(val)

            print(arguments, '+++++++++++')
            if symbol_entry.parameters:
                print('with parameters')
                    
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
                    print(f'args {arg}')
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
                    
                    if expr_type not in ['Setprecission', 'Granted']:
                        if symbol_entry.datatype[0] == 'chamber':
                            raise ValueError(f"Cannot initialize variable '{node.identifier[1]}' with chamber function '{identifier_name}'")
                    else:
                        if symbol_entry.datatype[0] == 'chamber':
                            raise ValueError(f"Invalid set precission value '{identifier_name}' with chamber return type")
                
                    if expr_type == "Arithmetic":

                        if symbol_entry.datatype[0] not in ["ocean", "treasures", '1', '0']:
                            raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype[0]} as arithmetic operand, must be ocean or treasures")
                    
                    elif expr_type == "Setprecission":

                        if symbol_entry.datatype[0] not in ["ocean", "treasures", '1', '0']:
                            raise ValueError(f"Invalid set precission value '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                        
                    elif expr_type == "Granted":

                        if symbol_entry.datatype[0] not in datatype:
                            raise ValueError(f"Invalid granted content '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                        
                    elif expr_type == "Relational":
                        if symbol_entry.datatype[0] not in datatype:
                            return False, symbol_entry.datatype[0]
                                        
                    elif expr_type == 'Function':

                        # Check type compatibility
                        if not self.validate_type_compatibility(datatype, symbol_entry.datatype[0]):
                            raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype[0]}")
                        
                    elif expr_type == 'String_op':

                        if symbol_entry.datatype not in datatype:
                            raise ValueError(f"Invalid string operand '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                    
                    elif expr_type == "Condition":

                        if symbol_entry.datatype[0] not in ['mirror']:
                            raise ValueError(f"Invalid condition '{symbol_entry.name}' of '{symbol_entry.datatype}' data type, must be mirror.")
                        
                    else:

                        # Check type compatibility
                        if not self.validate_type_compatibility(datatype, symbol_entry.datatype[0]):
                            raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype[0]}")
                    
                return True, symbol_entry.datatype[0]
            print('false---------', identifier_name, symbol_entry.datatype)
            has_open = False
            has_close = False
            
            for token_type, token_value in value:
                if token_type == '(' and token_value == '(':
                    has_open = True
                elif token_type == ')' and token_value == ')':
                    has_close = True

            if not has_open and not has_close:
                raise ValueError(f"'{identifier_name}' is defined as a function but is referenced without parentheses in variable initialization. Did you mean to call '{identifier_name}()' ?")
            print(len(arguments), '+++++++++++++]]')
            if len(arguments) != 0:
                raise ValueError(f"Function '{identifier_name}' does not accept arguments but {len(arguments)} were provided")
            
            # Ensure function return type matches the variable type
            if expr_type not in ['Setprecission', 'Granted']:
                if symbol_entry.datatype[0] == 'chamber':
                    raise ValueError(f"Cannot initialize variable '{node.identifier[1]}' with chamber function '{identifier_name}'")
            else:
                if symbol_entry.datatype[0] == 'chamber':
                    raise ValueError(f"Invalid set precission value '{identifier_name}' with chamber return type")
            
            if expr_type == "Arithmetic":

                if symbol_entry.datatype[0] not in ["ocean", "treasures", '1', '0']:
                    raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype[0]} as arithmetic operand, must be ocean or treasures")
            
            elif expr_type == "Setprecission":

                if symbol_entry.datatype[0] not in ["ocean", "treasures", '1', '0']:
                    raise ValueError(f"Invalid set precission value '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            elif expr_type == "Granted":

                if symbol_entry.datatype[0] not in datatype:
                    raise ValueError(f"Invalid granted content '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            elif expr_type == "Relational":
                print(datatype, '==============+++============', symbol_entry.datatype)
                if symbol_entry.datatype[0] not in datatype:
                    return False, symbol_entry.datatype[0]
                                
            elif expr_type == 'Function':

                # Check type compatibility
                if not self.validate_type_compatibility(datatype, symbol_entry.datatype[0]):
                    raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype[0]}")
                
            elif expr_type == 'String_op':

                if symbol_entry.datatype not in datatype:
                    raise ValueError(f"Invalid string operand '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            elif expr_type == "Condition":

                        if symbol_entry.datatype[0] not in ['mirror']:
                            raise ValueError(f"Invalid condition '{symbol_entry.name}' of '{symbol_entry.datatype}' data type, must be mirror.")
                
            else:
            
                # Check type compatibility
                if not self.validate_type_compatibility(datatype, symbol_entry.datatype[0]):
                    raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype[0]}")
            
            print('function call passed')
            
            return True, symbol_entry.datatype[0]
        
        print('not a function -----------------', identifier_name)

        # If it's an array, perform array-specific checks
        if symbol_entry.array_dimensions:
            dimensions = 0
            array_size = []
            id_index  = symbol_entry.array_dimensions
            if expr_type == 'Function':
                value = node.return_val
                datatype = node.return_type[0]

            # print(node.datatype[1], '==========', symbol_entry.datatype)
            if expr_type == "Arithmetic":

                if symbol_entry.datatype not in ["ocean", "treasures", '1', '0']:
                    raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype} as arithmetic operand, must be ocean or treasures")
                
            elif expr_type == "Setprecission":

                if symbol_entry.datatype not in ["ocean", "treasures", '1', '0']:
                    raise ValueError(f"Invalid set precission value '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            elif expr_type == "Granted":

                if symbol_entry.datatype[0] not in datatype:
                    raise ValueError(f"Invalid granted content '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            elif expr_type == "Relational":
                print(datatype, '==============+++============', symbol_entry.datatype)
                if symbol_entry.datatype not in datatype:
                    return False, symbol_entry.datatype
                                
            elif expr_type == 'Function':

                # Check type compatibility
                if not self.validate_type_compatibility(datatype, symbol_entry.datatype):
                    raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype}")
                
            elif expr_type == 'String_op':

                if symbol_entry.datatype not in datatype:
                    raise ValueError(f"Invalid string operand '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
                
            else:
            
                if datatype != symbol_entry.datatype:
                    raise ValueError(f"Invalid {datatype} initialization of array '{node.identifier[1]}' with a datatype of {datatype}")
            
            for element in value[1:]:
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
            return True, symbol_entry.datatype 
        
        print(value)
        if expr_type == 'Function':
                value = node.return_val
                datatype = node.return_type[0]

        print(datatype, 'datatype=============', expr_type)
        
        if expr_type == "Arithmetic":
            # Check type compatibility

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype not in ["ocean", "treasures", '1', '0']:
                raise ValueError(f"Type mismatch: Cannot use {symbol_entry.datatype} as arithmetic operand, must be ocean or treasures")
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")
            
        elif expr_type == "Relational":
            # Check type compatibility

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype not in datatype:
                print('---------------------------==',symbol_entry.datatype)
                return False, symbol_entry.datatype
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")
        
        elif expr_type in "Setprecission":
            # Check type compatibility

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype not in ["ocean", "treasures", '1', '0']:
                raise ValueError(f"Invalid set precission value '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")
            
        elif expr_type in "Granted":
            # Check type compatibility

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype not in datatype:
                raise ValueError(f"Invalid granted '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")


        elif expr_type == 'Function':
            if len(node.return_val) > 1:
                if node.return_val[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")
        
            # Check type compatibility
            if not self.validate_type_compatibility(datatype, symbol_entry.datatype):
                raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype}")
        
        elif expr_type == 'String_op':

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype not in datatype:
                raise ValueError(f"Invalid string operand '{symbol_entry.name}' of '{symbol_entry.datatype}' data type. ")
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")

        elif expr_type == "Condition":

            if len(value) > 1:
                if value[1][0] in ['(', '[']:
                    raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")

            if symbol_entry.datatype != 'mirror':
                raise ValueError(f"Invalid condition '{symbol_entry.name}' of '{symbol_entry.datatype}' data type, must be mirror.")
            
            # Check if the identifier is initialized
            if not symbol_entry.is_initialized:
                raise ValueError(f"Uninitialized identifier '{identifier_name}'")
            
        else:
            
            # First check if node.value exists and is not None
            if hasattr(node, 'value') and node.value is not None:
                # Then check if it has length > 1
                if len(node.value) > 1:
                    if node.value[1][0] in ['(', '[']:
                        raise ValueError(f"{symbol_entry.name} is declared as a variable but is used as an array or function.")
                
                # Check type compatibility
                if not self.validate_type_compatibility(datatype, symbol_entry.datatype):
                    raise ValueError(f"Type mismatch: Cannot initialize {datatype} with {symbol_entry.datatype}")
    
            
        # Check if the identifier is initialized
        # if not symbol_entry.is_initialized:
        #     raise ValueError(f"Uninitialized identifier '{identifier_name}'")
        
        
        return True, symbol_entry.datatype

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
            value=None,
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
                value=None,
                datatype=param_type[0],
                scope_level=self.symbol_table.current_scope_level,
                is_initialized=True,
                is_function=False
            )
            self.symbol_table.declare(param_symbol)
        
        print(node.body, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        # Validate function body
        if  node.body or len(node.body) > 0:
            print("entered body not none")
            self.validate_function_body(node.body, node.scope_level)
        
        # Validate return value if present
        if node.return_type[1] != 'chamber':
            if node.return_val:
                self.validate_return_value(node, node.scope_level)
            else:
                raise ValueError(f"A function declared to return '{node.return_type[1]}' must return a value.")
            
        if node.return_type[1] == 'chamber':
            print('enter chamber++++++++++++++++++++===========')
            if node.return_val:
                raise ValueError(f"A function returning 'chamber' cannot return any value.")
        
        # Exit function scope
        self.symbol_table.exit_scope()
        print('Function Node done')

    def validate_function_body(self, body, scope_level):
        """
        Validate the body of a function.
        Recursively checks semantic rules for different statement types.
        """
        for statement in body:
            # Dispatch to appropriate validation method based on node type
            validator_method = getattr(self, f'validate_{type(statement).__name__}', None)
            if validator_method:
                validator_method(statement, scope_level)

    def validate_return_value(self, node, scope_level):
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
        
        elif expr_type == 'arithmetic':
            if datatype in ['ocean', 'treasures']:
                self.validate_arithmetic(value, datatype, node)
            else:
                raise ValueError(f"Cannot return arithmetic operation for datatype '{datatype}'.")
            
        elif expr_type in ['relational', 'logical']:
            if datatype == 'mirror':
                if expr_type == 'relational':
                    self.validate_relational(value, datatype, node)
                elif expr_type == 'logical':
                    self.validate_logical(value, datatype, node)
            else:
                raise ValueError(f"Cannot return {expr_type} operation for datatype '{datatype}'.")
        
        else:
            if val_type == 'identifier':
                if len(value) > 1:
                    if value[1][0] in ['++', '--']:
                        return True
                    self.validate_id(value, datatype, node, 'Function')
                else:
                    self.validate_id(value, datatype, node, 'Function')
            else:
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
        print('main func passed')
        self.validate_function_body(node.body, 1)

    def validate_VariableReassignmentNode(self, node, scope_level):
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

                new_value = node.expression
                symbol.value = new_value
                # Optionally, mark the symbol as initialized.
                symbol.is_initialized = True

            except Exception as e:
                self.errors.append(SemanticError(
                    SemanticErrorType.Invalid_Assignment,
                    f"{str(e)}"
                ))

        


    def validate_FunctionCallNode(self, node, scope_level):
        """
        Validate function call.
        Checks:
        - Function exists
        - Argument count matches
        - Argument types are compatible
        - Passes argument values to symbol table
        """
        symbol_entry = self.symbol_table.lookup(node.name)
        
        if not symbol_entry or not symbol_entry.is_function:
            raise ValueError(f"Function '{node.name}' not declared")
        
        identifier_name = node.name

        if symbol_entry.is_function:
            print('1 ==================')
            arguments = []
            flat_args = [item for sublist in node.arguments for item in sublist]
            for val in flat_args:
                if val[0] not in ['(', ',', ')']:
                    arguments.append(val)
            print(arguments,"===========")
            
            if symbol_entry.parameters:
                print('++++++++++++',len(symbol_entry.parameters))
                print('----------------',len(arguments), arguments)
                
                # Validate number of arguments
                if len(arguments) == 0:
                    param_details = ", ".join([f"{param[0][0]} {param[1][1]}" for param in symbol_entry.parameters])
                    raise ValueError(f"Function '{identifier_name}' requires arguments: ({param_details})")
                
                # Check if argument count matches parameter count
                if len(arguments) != len(symbol_entry.parameters):
                    raise ValueError(f"Function '{identifier_name}' requires {len(symbol_entry.parameters)} arguments but got {len(arguments)}")
                
                # Create a new scope for function parameters
                self.symbol_table.enter_scope()
                
                # Validate argument types and add parameters to symbol table
                for i, param in enumerate(symbol_entry.parameters):
                    param_type = param[0][0]  # Type
                    param_name = param[1][1]  # Parameter name
                    arg_value = arguments[i]  # Argument value

                    print(param_type, "=============+++")
                    
                    # Type-specific validation
                    try:
                        if param_type == 'treasures':
                            self.validate_treasures([arg_value], param_type, node)
                        elif param_type == 'ocean':
                            self.validate_ocean([arg_value], param_type, node)
                        elif param_type == 'scroll':
                            self.validate_scroll([arg_value], param_type, node)
                        elif param_type == 'rose':
                            self.validate_rose([arg_value], param_type, node)
                        elif param_type == 'mirror':
                            self.validate_mirror([arg_value], param_type, node)
                    except ValueError as e:
                        self.symbol_table.exit_scope()  # Clean up scope on error
                        raise ValueError(f"Invalid argument for function '{identifier_name}': {str(e)}")
                    
                    # Add the parameter with its argument value to the symbol table
                    # self.symbol_table.insert(param_name, {
                    #     'type': param_type,
                    #     'value': arg_value,
                    #     'is_function': False,
                    #     'line': node.line if hasattr(node, 'line') else None
                    # })
                    symbol_entry = self.symbol_table.lookup(param_name)

                    symbol_entry.type = param_type
                    symbol_entry.value = arg_value
                    symbol_entry.is_function = False,
                    symbol_entry.line = node.line if hasattr(node, 'line') else None

                
                # Note: You'll need to handle exiting this scope elsewhere,
                # typically after function body execution is completed
                
                return True
            print('false---------', identifier_name, len(arguments))

            if len(arguments) != 0:
                raise ValueError(f"Function '{identifier_name}' does not accept arguments but {len(arguments)} were provided")
            
            return True
        # pass
        

    def validate_UnaryOperationNode(self, node, scope_level):
        symbol_entry = self.symbol_table.lookup(node.identifier)
        
        if not symbol_entry:
            raise ValueError(f"Undeclared identifier '{node.identifier}'")
        
        if symbol_entry.datatype not in ['treasures', 'ocean']:
            raise ValueError(f"Unary operator requires a numeric operand (treasures or ocean), but received {symbol_entry.datatype} instead.")
        
        return True

    def validate_ArrayAssignmentNode(self, node, scope_level):
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
    def validate_DoWhileNode(self, node, scope_level):
        # condition
        conditions = node.condition
        condition = []
        for exp in conditions:
                condition.append(exp[0])

                
        expr_type = self.type_expr(condition)

        print(condition, expr_type)

        if expr_type == 'relational':
            self.validate_relational(conditions, None, node)

        elif expr_type == 'logical':
            self.validate_logical(conditions, None, node)

        elif expr_type == 'Not Valid':
            if conditions[0][0] == 'identifier':
                self.validate_id(conditions, ('mirror', 'mirror'), node, 'Condition')

        # body
        self.validate_function_body(node.loop_body, scope_level)

        return True

    def validate_WhileNode(self, node, scope_level):
        # condition
        conditions = node.condition
        condition = []
        for exp in conditions:
                condition.append(exp[0])
                        
        expr_type = self.type_expr(condition)
        print(conditions, ">>>>>>>>>>>>")
        print(condition, expr_type)

        if expr_type == 'relational':
            self.validate_relational(conditions, None, node)

        elif expr_type == 'logical':
            self.validate_logical(conditions, None, node)

        elif expr_type == 'Not Valid':
            if conditions[0][0] == 'identifier':
                self.validate_id(conditions, ('mirror', 'mirror'), node, 'Condition')

        # body
        self.validate_function_body(node.loop_body, scope_level)

        return True


    def validate_IfNode(self,node, scope_level):
        # condition
        conditions = node.condition
        condition = []
        for exp in conditions:
                condition.append(exp[0])
                        
        expr_type = self.type_expr(condition)
        print(conditions, ">>>>>>>>>>>>")
        print(condition, expr_type)

        if expr_type == 'relational':
            self.validate_relational(conditions, None, node)

        elif expr_type == 'logical':
            self.validate_logical(conditions, None, node)

        elif expr_type == 'Not Valid':
            if conditions[0][0] == 'identifier':
                self.validate_id(conditions, ('mirror', 'mirror'), node, 'Condition')

        # body
        self.validate_function_body(node.body, scope_level)

        # elif
        if node.elif_nodes:
            self.validate_ElifNode(node.elif_nodes, scope_level)

        # else
        if node.else_node:
            self.validate_ElseNode(node.else_node, scope_level)
        
        return True

    def validate_ElifNode(self, elif_nodes, scope_level):
        # Handle each elif node in the list
        for node in elif_nodes:
            # condition
            conditions = node.condition
            condition = []
            for exp in conditions:
                condition.append(exp[0])
                        
            expr_type = self.type_expr(condition)
            print(conditions, ">>>>>>>>>>>>")
            print(condition, expr_type)

            if expr_type == 'relational':
                self.validate_relational(conditions, None, node)
            elif expr_type == 'logical':
                self.validate_logical(conditions, None, node)
            elif expr_type == 'Not Valid':
                if conditions[0][0] == 'identifier':
                    self.validate_id(conditions, ('mirror', 'mirror'), node, 'Condition')

            # body
            self.validate_function_body(node.body, scope_level)

    def validate_ElseNode(self, node, scope_level):
        # body
        self.validate_function_body(node.body, scope_level)

        return True


    def validate_BreakNode(self, node, scope_level):
        return True

    def validate_ContinueNode(self, node, scope_level):
        return True

    def validate_ForLoopNode(self, node, scope_level):
        loop_var = node.loop_var
        loop_exp = node.loop_exp
        loop_unary = node.loop_unary
        loop_body = node.loop_body
        print(loop_body, 'loop_var')
        # loop variable
        if loop_var[0][0] == 'treasures':
            # Create symbol entry
            symbol = SymbolEntry(
                name=loop_var[1][1],  
                datatype=loop_var[0][0],
                value=loop_var[3][1],
                scope_level=scope_level,
                is_dynasty=False,
                is_initialized=True,
            )
            redecl_error = self.symbol_table.declare(symbol)
            if redecl_error:
                self.errors.append(redecl_error)
                raise ValueError(self.errors)
        

        else:
            print("FALSE")
            self.validate_id([loop_var[0]], ('treasures', 'treasures'), node, 'Not expr')
            symbol_entry = self.symbol_table.lookup(loop_var[0][1])

            symbol_entry.value = loop_var[2][1]
            symbol_entry.is_initialized = True

        # condition
        self.validate_relational(loop_exp, ('treasures', 'treasures'), node)

        # unary
        self.unary(loop_unary, ('treasures', 'treasures'), node, False)

        # body
        self.validate_function_body(node.loop_body, scope_level)

        return True
    
    # def validate_LiteralNode(self, node, scope_level):
    #     pass

    # def validate_IfBreakNode(self, node, scope_level):
    #     pass


    # def validate_ElifBreakNode(self, node, scope_level):
    #     pass

    # def validate_ElseBreakNode(self, node, scope_level):
    #     pass

    def validate_OutputNode(self, node, scope_level):
        expr = node.expressions
        expressions = []
        expression = []
        exp_content = []
        i = 0
        n = len(expr)
        setprecission = False
        
        while i < n:  # Process all tokens
            if expr[i][0] == 'identifier':
                expression.append(expr[i])
                i += 1
                if i < n and expr[i][0] == '(':
                    expression.append(expr[i])  # Add the opening parenthesis
                    i += 1
                    # Collect everything until the closing parenthesis
                    paren_count = 1  # We've seen one opening parenthesis
                    while i < n and paren_count > 0:
                        if expr[i][0] == '(':
                            paren_count += 1
                        elif expr[i][0] == ')':
                            paren_count -= 1
                        expression.append(expr[i])
                        i += 1
                    continue  # Skip the normal increment since we've already incremented i
            
            if i < n:  # Check bounds before accessing
                if expr[i][0] == ',':
                    expressions.append(expression)
                    expression = []
                else:
                    expression.append(expr[i])
                i += 1
        
        # Don't forget to append the last expression
        if expression:
            expressions.append(expression)
        
        i = 0
        n = len(expressions)

        while i < n:
            if expressions[i][0][0] == 'setprecission':
                if n == 1:
                    raise ValueError("Expected value after set_precision token - formatting directives should be before the value they format")
                
                i+=1

                if len(expressions[i]) == 1:
                    if expressions[i][0][0] not in ['treasures_lit', 'ocean_lit', 'identifier', '1', '0']:
                        raise ValueError("Invalid value for set precission, must be a treasures or ocean literal")
                    if expressions[i][0][0] == 'identifier':
                        self.validate_id(expressions[i], ['treasures_lit', 'ocean_lit'], node, 'Setprecission')
                
                    print(expressions, "------========", len(expressions[i]))
                else:
                    is_Arith = False

                    for exp in expressions[i]:
                        if exp[0] in ['+', '-', '/', '*', '%']:
                            is_Arith = True
                        if exp[0] in ['<', '>', '<=', '>=', '==', '!=', '&&', '||']:
                            raise ValueError("Invalid value for set precission, must be a treasures or ocean literal")
                        
                    if is_Arith:
                        self.validate_arithmetic(expressions[i], ['treasures', 'ocean'], node)
                    
                    else:
                        if expressions[i][0][0] == 'identifier':
                            self.validate_id(expressions[i], ['treasures', 'ocean'], node, 'Setprecission')
                        
                        elif expressions[i][0][0] == 'totreasures':
                            self.validate_conversion_func(expressions[i],'treasures', node)

                        elif expressions[i][0][0] == 'toocean':
                            self.validate_conversion_func(expressions[i],'ocean', node)

                        else:
                            raise ValueError("Invalid value for set precission, must be a treasures or ocean literal")
            print("here =???????????")     
            for exp in expressions[i]:
                exp_content.append(exp[0])

            print(exp_content)
                    
            expr_type = self.type_expr(exp_content)

            print(expr_type, expressions[i], '----===-------')

            if expr_type == 'arithmetic':
                has_string = False
                for expr in expressions[i]:
                    if 'scroll_lit' in expr[0] or 'rose_lit' in expr[0]:
                        has_string = True
                    
                    if expr[0] == 'identifier':
                        id = expr[1]
                        symbol_entry = self.symbol_table.lookup(id)

                        if symbol_entry and symbol_entry.datatype in ['scroll', 'rose']:
                            has_string = True

                if has_string:
                    print("ttttttttttttrrrrrrrrrruuuuuuuuuuuuueee", exp_content, expressions[i])
                    self.string_op(exp_content, expressions[i], node)
                else:
                    print("ffffffffffaaaaaaalllllllsssseeeeeeee")
                    self.validate_arithmetic(expressions[i], None, node) # check if concat

            elif expr_type == 'logical':
                self.validate_logical(expressions[i], None, node)
            
            elif expr_type == 'relational':
                self.validate_relational(expressions[i], None, node)
            
            elif expr_type == 'assignment':
                 raise ValueError("Invalid granted content 'assignment expression' ")
            
            elif expr_type == 'Not Valid':
                print(expressions[i], "========++=========")
                if expressions[i][0][0] == 'lengthof':
                    self.lengthof(node, 'Granted')

                if expressions[i][0][0] == 'identifier':
                    is_unary = False
                    for exp in expressions[i]:
                        if exp[0] in ['++', '--']:
                            is_unary = True
                    
                    if is_unary:
                        self.unary(expressions[i], None, node, False)

                    else:
                        self.validate_id(expressions[i], ['treasures', 'ocean', 'scroll', 'rose', 'mirror'], node, 'Granted')

                elif expressions[i][0][0] == 'totreasures':
                    self.validate_conversion_func(expressions[i], 'treasures', node)

                elif expressions[i][0][0] == 'toocean':
                    self.validate_conversion_func(expressions[i], 'ocean', node)

                elif expressions[i][0][0] == 'toscroll':
                    self.validate_conversion_func(expressions[i], 'scroll', node)

                elif expressions[i][0][0] == 'torose':
                    self.validate_conversion_func(expressions[i], 'rose', node)

                elif expressions[i][0][0] == 'tomirror':
                    self.validate_conversion_func(expressions[i], 'mirror', node)
                
                elif expressions[i][0][0] == '!':
                    self.validate_logical(expressions[i], 'mirror', node)

                elif expressions[i][0][0] not in ['treasures_lit', 'ocean_lit', 'scroll_lit', 'rose_lit', '1', '0', 'phantom']:
                    raise ValueError(f"Invalid granted content '{expressions[i][0][0]}' ")


            i += 1

        print(expressions)

        return True
        # pass






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