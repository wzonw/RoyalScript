import textwrap  # For handling indentation of multi-line strings
import ast       # For parsing and validating Python code
import black     # For code formatting

class RoyalScriptToPythonTranslator:
    def __init__(self, global_variable_types=None):
        self.indent_level = 0  # Set initial indentation level to 0
        self.symbol_table = {}  # Initialize symbol table for variable types
        self.global_variable_types = global_variable_types or {}  # Set global variable types or empty dict
        self.struct_definitions = {}

    def indent(self, text):
        """Indent the given text according to the current indent_level."""
        prefix = "    " * self.indent_level  # Create indentation prefix based on indent_level
        return textwrap.indent(text, prefix)  # Indent the text using textwrap

    def translate(self, node): # node = ast
        """Dispatches to the appropriate translation method based on node type."""
        method_name = f"translate_{type(node).__name__}"  # Build method name string
        method = getattr(self, method_name, self.unsupported_node)  # Get translation method or fallback 
        return method(node)  # Call the translation method

    def unsupported_node(self, node):
        """Handles unsupported node types."""
        raise NotImplementedError(f"No translation method defined for {type(node).__name__}")  # Raise error

    def format_code(self, code):
        """Format Python code using Black formatter."""
        try:
            formatted_code = black.format_str(  # Format code using black
                code, 
                mode=black.Mode(
                    line_length=88,  # Set line length for formatting
                    string_normalization=True,  # Normalize string quotes
                    is_pyi=False,  # Not a .pyi file
                )
            )   
            return formatted_code  # Return formatted code
        except Exception as e:
            print(f"Warning: Code formatting failed: {e}")  # Print warning if formatting fails
            return f"# Note: Auto-formatting failed\n{code}"  # Return unformatted code with comment

    def validate_code(self, code):
        """Validates Python code by parsing it with the ast module."""
        try:
            ast.parse(code)  # Try parsing the code
            return True  # Return True if code is valid
        except SyntaxError as e:
            print(f"Generated code has syntax error: {e}")  # Print error if code is invalid
            return False  # Return False if code is invalid

    def translate_ProgramNode(self, node):
        """Translates the root program node to Python code."""
        code = ["import sys"]  # Start code list with import sys
        for decl in node.global_declarations:  # Loop through global declarations
            translated = self.translate(decl)  # Translate each declaration
            if translated.strip():  # If translation is not empty
                code.append(translated)  # Add translated code to code list
        for func in node.functions:  # Loop through functions
            code.append("")  # Add empty line before each function
            code.append(self.translate(func))  # Add translated function code
        code.append("")  # Add empty line before main function
        code.append(self.translate(node.main_function))  # Add translated main function
        raw_code = "\n".join(code)  # Join code list into a single string ["import sys", "def Main():", "N = 12 * 7", "return 0", "if_name_ == "_main_: Main()""]
        return self.format_code(raw_code)  # Format and return the code
    
    def translate_StructDeclarationNode(self, node):
        """Translates struct declarations to Python classes."""
        struct_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Store struct definition for later reference
        self.struct_definitions[struct_name] = node.members
        
        code = [f"class {struct_name}:"]
        self.indent_level += 1
        
        # Add __init__ method
        init_params = ["self"]
        init_body = []
        self.indent_level += 1
        for member in node.members:
            if isinstance(member, list) and len(member) >= 2:
                member_type = member[0]
                member_name = member[1]
                
                # Add parameter with default value based on type
                default_value = self.get_default_value_for_type(member_type)
                init_params.append(f"{member_name}={default_value}")
                init_body.append(self.indent(f"self.{member_name} = {member_name}"))
        
        # Create __init__ method signature
        self.indent_level -= 1
        init_signature = f"def __init__({', '.join(init_params)}):"
        code.append(self.indent(init_signature))
        self.indent_level += 1
        if init_body:
            code.extend(init_body)
        else:
            code.append(self.indent("pass"))
        self.indent_level -= 1
        
        # Add __str__ method for better representation
        code.append("")
        code.append(self.indent("def __str__(self):"))
        self.indent_level += 1
        
        member_strs = []
        for member in node.members:
            if isinstance(member, list) and len(member) >= 2:
                member_name = member[1]
                member_strs.append(f"{member_name}={{self.{member_name}}}")
        
        str_format = f"{struct_name}({', '.join(member_strs)})"
        code.append(self.indent(f'return f"{str_format}"'))
        self.indent_level -= 1
        
        # Add __repr__ method
        code.append("")
        code.append(self.indent("def __repr__(self):"))
        self.indent_level += 1
        code.append(self.indent("return self.__str__()"))
        self.indent_level -= 1
        
        self.indent_level -= 1
        return "\n".join(code)


    def translate_StructInstantiationNode(self, node):
        """Translates struct instantiation to Python class instantiation."""
        struct_type = node.struct_type[1] if isinstance(node.struct_type, tuple) else node.struct_type
        instance_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Build constructor arguments
        args = []
        if hasattr(node, 'member_initializations') and node.member_initializations:
            for member_name, value_tokens in node.member_initializations.items():
                # Translate the value expression
                translated_value = self.translate_expression(value_tokens, None)
                args.append(f"{member_name}={translated_value}")
        
        # Create instantiation statement
        if args:
            constructor_call = f"{struct_type}({', '.join(args)})"
        else:
            constructor_call = f"{struct_type}()"
        
        return self.indent(f"{instance_name} = {constructor_call}")


    def get_default_value_for_type(self, type_name):
        """Returns appropriate default value for RoyalScript data types."""
        type_defaults = {
            'treasures': '0',      # int
            'ocean': '0.0',        # float
            'rose': "''",          # char (empty string)
            'scroll': '""',        # string
            'mirror': 'False'      # bool
        }
        return type_defaults.get(type_name, 'None')

    def translate_VariableDeclarationNode(self, node):
        """Translates variable declarations to Python assignments."""
        if isinstance(node.identifier, list):  # If multiple variables are declared
            identifiers = []  # Initialize list for variable names
            for ident in node.identifier:  # Loop through identifiers
                if isinstance(ident, tuple) and len(ident) >= 2:  # If identifier is a tuple
                    identifiers.append(ident[1])  # Add variable name to list
                    if hasattr(node, 'datatype'):  # If node has datatype
                        self.symbol_table[ident[1]] = node.datatype[1]  # Update symbol table
                else:
                    identifiers.append(str(ident))  # Add identifier as string
            identifiers_str = ", ".join(identifiers)  # Join identifiers with comma
            if isinstance(node.value, list) and all(isinstance(val, list) for val in node.value):  # If values is a list of lists
                values = ", ".join(self.translate_expression(val, node.datatype[1]) for val in node.value)  # Translate each value
            else:
                values = self.translate_expression(node.value, node.datatype[1])  # Translate value
            return self.indent(f"{identifiers_str} = {values}")  # Return assignment statement
        else:  # If single variable is declared
            if isinstance(node.identifier, tuple) and len(node.identifier) >= 2:  # If identifier is a tuple
                var_name = node.identifier[1]  # Get variable name
                if hasattr(node, 'datatype') and isinstance(node.datatype, tuple):  # If node has datatype
                    self.symbol_table[var_name] = node.datatype[1]  # Update symbol table 'N' : {'treasures'}
            if hasattr(node, 'array_dimensions') and node.array_dimensions:  # If array dimensions exist
                return self.translate_array_declaration(node)  # Translate array declaration
           
            value = self.translate_expression( # "12 * 7"
                node.value,
                node.datatype[1] if hasattr(node, 'datatype') and isinstance(node.datatype, tuple) else None
            ) if node.value else "None"  # Translate value or set to None
            
            if isinstance(node.identifier, tuple):  # If identifier is a tuple
                return self.indent(f"{node.identifier[1]} = {value}")  # Return assignment
               # "N = 12 * 7"
            else:
                return self.indent(f"{node.identifier} = {value}")  # Return assignment

    def translate_array_declaration(self, node):
        """Translates array declarations to Python lists or nested lists."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier  # Get variable name
        dimensions = []  # Initialize list for dimensions
        for dim in node.array_dimensions:  # Loop through array dimensions
            if isinstance(dim, tuple):  # If dimension is a tuple
                dimensions.append(dim[1])  # Add dimension value
            else:
                dimensions.append(str(dim))  # Add dimension as string
        if node.value:  # If array has initial value
            value_str = self.translate_expression(node.value, None)  # Translate value
            if value_str.startswith('{') and value_str.endswith('}'):  # If value uses curly braces
                value_str = value_str.replace('{', '[').replace('}', ']')  # Replace with square brackets
            return self.indent(f"{var_name} = {value_str}")  # Return array assignment
        else:  # If array has no initial value
            if len(dimensions) == 1:  # If 1D array
                return self.indent(f"{var_name} = [None] * {dimensions[0]}")  # Return 1D array initialization
            
            elif len(dimensions) == 2:  # If 2D array
                return self.indent(f"{var_name} = [[None] * {dimensions[1]} for _ in range({dimensions[0]})]")  # Return 2D array initialization
            else:
                return self.indent(f"# Unsupported array dimension: {len(dimensions)}")  # Return unsupported dimension comment

    def translate_VariableReassignmentNode(self, node):
        """Translates variable reassignments."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier  # Get variable name
        operator = node.operator[1] if isinstance(node.operator, tuple) else node.operator  # Get operator
        var_type = self.symbol_table.get(var_name)  # Get variable type from symbol table
        if var_type is None:  # If not found in symbol table
            var_type = self.global_variable_types.get(var_name)  # Get from global variable types
        print(var_type, 'varrtyopeee', var_name, self.global_variable_types.get(var_name))  # Print debug info
        if operator == "/=" and var_type == "treasures":  # If integer division for treasures
            operator = "//="  # Use integer division operator
        expr = self.translate_expression(node.expression, var_type)  # Translate expression
        return self.indent(f"{var_name} {operator} {expr}")  # Return reassignment statement

    def translate_FunctionNode(self, node):
        """Translates function definitions."""
        func_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier  # Get function name
        params = []  # Initialize parameter list
        for param in (node.parameters or []):  # Loop through parameters
            if isinstance(param, tuple) and len(param) >= 2:  # If parameter is a tuple
                param_name = param[1][1] if isinstance(param[1], tuple) else param[1]  # Get parameter name
                params.append(param_name)  # Add to parameter list
        param_str = ", ".join(params)  # Join parameters with comma
        code = [f"def {func_name}({param_str}):"]  # Start function definition
        if not node.body and node.return_type == 'chamber':  # If function body is empty
            self.indent_level += 1  # Increase indentation
            code.append(self.indent("pass"))  # Add pass statement
            self.indent_level -= 1  # Decrease indentation
        else:
            self.indent_level += 1  # Increase indentation
            for stmt in node.body:  # Loop through function body statements
                translated = self.translate(stmt)  # Translate statement
                if translated.strip():  # If translation is not empty
                    code.append(translated)  # Add to code list
            if node.return_val:  # If function has return value
                ret_expr = self.translate_expression(node.return_val, None)  # Translate return value
                code.append(self.indent(f"return {ret_expr}"))  # Add return statement
            self.indent_level -= 1  # Decrease indentation
        return "\n".join(code)  # Join code list into string

    def translate_MainFunctionNode(self, node):
        """Translates the main function and adds code to call it."""
        main_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier  # Get main function name
        code = [f"def {main_name}():"]  # Start main function definition
        self.indent_level += 1  # Increase indentation
        for stmt in node.body:  # Loop through main function body
            translated = self.translate(stmt)  # Translate statement N = 12 * 7 
            if translated.strip():  # If translation is not empty
                code.append(translated)  # Add to code list
        return_val = node.return_val[1] if isinstance(node.return_val, tuple) else node.return_val  # Get return value 0
        code.append(self.indent(f"return {return_val}"))  # Add return statement
        self.indent_level -= 1  # Decrease indentation
        code.append("")  # Add empty line
        code.append(f"if __name__ == \"__main__\":")  # Add main check
        code.append(f"    {main_name}()")  # Call main function
        return "\n".join(code)  # Join code list into string

    def translate_IfNode(self, node):
        """Translates if statements with elif and else branches."""
        code = []  # Initialize code list
        condition = self.translate_expression(node.condition, None)  # Translate if condition
        code.append(self.indent(f"if {condition}:"))  # Add if statement
        self.indent_level += 1  # Increase indentation
        if node.body:  # If if-body exists
            for stmt in node.body:  # Loop through if-body
                code.append(self.translate(stmt))  # Translate and add statement
        else:
            code.append(self.indent("pass"))  # Add pass if body is empty
        self.indent_level -= 1  # Decrease indentation
        for elif_node in (node.elif_nodes or []):  # Loop through elif nodes
            elif_condition = self.translate_expression(elif_node.condition, None)  # Translate elif condition
            code.append(self.indent(f"elif {elif_condition}:"))  # Add elif statement
            self.indent_level += 1  # Increase indentation
            if elif_node.body:  # If elif-body exists
                for stmt in elif_node.body:  # Loop through elif-body
                    code.append(self.translate(stmt))  # Translate and add statement
            else:
                code.append(self.indent("pass"))  # Add pass if body is empty
            self.indent_level -= 1  # Decrease indentation
        if node.else_node:  # If else node exists
            code.append(self.indent("else:"))  # Add else statement
            self.indent_level += 1  # Increase indentation
            if node.else_node.body:  # If else-body exists
                for stmt in node.else_node.body:  # Loop through else-body
                    code.append(self.translate(stmt))  # Translate and add statement
            else:
                code.append(self.indent("pass"))  # Add pass if body is empty
            self.indent_level -= 1  # Decrease indentation
        return "\n".join(code)  # Join code list into string

    def translate_WhileNode(self, node):
        """Translates while loops."""
        code = []  # Initialize code list
        condition = self.translate_expression(node.condition, None)  # Translate while condition
        code.append(self.indent(f"while {condition}:"))  # Add while statement
        self.indent_level += 1  # Increase indentation
        if node.loop_body:  # If loop body exists
            for stmt in node.loop_body:  # Loop through loop body
                code.append(self.translate(stmt))  # Translate and add statement
        else:
            code.append(self.indent("pass"))  # Add pass if body is empty
        self.indent_level -= 1  # Decrease indentation
        return "\n".join(code)  # Join code list into string

    def translate_DoWhileNode(self, node):
        """Translates do-while loops to Python using a while True with break."""
        code = []  # Initialize code list
        code.append(self.indent("while True:"))  # Add while True statement
        self.indent_level += 1  # Increase indentation
        if node.loop_body:  # If loop body exists
            for stmt in node.loop_body:  # Loop through loop body
                code.append(self.translate(stmt))  # Translate and add statement
        condition = self.translate_expression(node.condition, None)  # Translate do-while condition
        code.append(self.indent(f"if not ({condition}):"))  # Add if not condition
        self.indent_level += 1  # Increase indentation
        code.append(self.indent("break"))  # Add break statement
        self.indent_level -= 1  # Decrease indentation
        self.indent_level -= 1  # Decrease indentation
        return "\n".join(code)  # Join code list into string

    def translate_ForLoopNode(self, node):
        """Translates for loops."""
        code = []  # Initialize code list
        init = self.translate_expression(node.loop_var, None)  # Translate loop initialization
        condition = self.translate_expression(node.loop_exp, None)  # Translate loop condition
        update = self.translate_expression(node.loop_unary, None)  # Translate loop update
        code.append(self.indent(f"{init.replace('treasures ', '')}"))  # Add initialization statement
        code.append(self.indent(f"while {condition}:"))  # Add while statement
        self.indent_level += 1  # Increase indentation
        if node.loop_body:  # If loop body exists
            for stmt in node.loop_body:  # Loop through loop body
                code.append(self.translate(stmt))  # Translate and add statement
        code.append(self.indent(f"{update}"))  # Add update statement
        self.indent_level -= 1  # Decrease indentation
        return "\n".join(code)  # Join code list into string

    def translate_BreakNode(self, node):
        """Translates break statements."""
        return self.indent("break")  # Return break statement

    def translate_ContinueNode(self, node):
        """Translates continue statements."""
        return self.indent("continue")  # Return continue statement

    def translate_OutputNode(self, node):
        """Translates output statements (print statements)."""
        expressions = []  # Initialize list for expressions
        i = 0  # Set index to 0
        current_expr = []  # Initialize current expression list
        paren_count = 0  # Set parenthesis count to 0
        while i < len(node.expressions):  # Loop through expressions
            token = node.expressions[i]  # Get current token
            if isinstance(token, tuple):  # If token is a tuple
                if token[0] == '(':  # If token is opening parenthesis
                    paren_count += 1  # Increment parenthesis count
                elif token[0] == ')':  # If token is closing parenthesis
                    paren_count -= 1  # Decrement parenthesis count
            if token[0] == ',' and paren_count == 0:  # If token is comma and not inside parentheses
                if current_expr:  # If current expression is not empty
                    expressions.append(current_expr)  # Add current expression to expressions list
                    current_expr = []  # Reset current expression
            elif token[0] == 'setprecission':  # If token is setprecision
                precision_value = ""  # Initialize precision value
                if i + 2 < len(node.expressions) and node.expressions[i+1][0] == ',':  # If next token is comma
                    cur_pos = node.expressions[i][1][2]  # Get current position
                    cur = 2  # Set current index
                    while cur_pos != 'f':  # Loop until 'f' is found
                        precision_value += cur_pos  # Add to precision value
                        cur += 1  # Increment index
                        cur_pos = node.expressions[i][1][cur]  # Get next position
                    if paren_count == 0:  # If not inside parentheses
                        i += 1  # Skip comma
                if precision_value:  # If precision value exists
                    current_expr.append(('precision', precision_value))  # Add precision to current expression
            else:
                current_expr.append(token)  # Add token to current expression
            i += 1  # Increment index
        if current_expr:  # If current expression is not empty
            expressions.append(current_expr)  # Add to expressions list
        print_args = []  # Initialize print arguments list
        for expr in expressions:  # Loop through expressions
            has_precision = False  # Set precision flag to False
            precision_value = None  # Set precision value to None
            filtered_expr = []  # Initialize filtered expression list
            for token in expr:  # Loop through tokens in expression
                if token[0] == 'precision':  # If token is precision
                    has_precision = True  # Set precision flag to True
                    precision_value = token[1]  # Set precision value
                    if int(precision_value) > 15:  # If precision is greater than 15
                        raise ValueError("Up to 15 decimal precision is only allowed.")  # Raise error
                else:
                    filtered_expr.append(token)  # Add token to filtered expression
            translated = self.translate_expression(filtered_expr, None)  # Translate filtered expression
            if has_precision and precision_value:  # If precision is set
                prec_val = precision_value[1] if isinstance(precision_value, tuple) else precision_value  # Get precision value
                translated = f"f'{{({translated}):.{prec_val}f}}'"  # Format with precision
            translated = f"str({translated}).replace('None', 'phantom')"  # Replace None with phantom
            print_args.append(translated)  # Add to print arguments
        return self.indent(f"print({', '.join(print_args)}, end='')")  # Return print statement

    def translate_FunctionCallNode(self, node):
        """Translates function calls."""
        args = []  # Initialize arguments list
        for arg in node.arguments:  # Loop through arguments
            args.append(self.translate_expression(arg, None))  # Translate and add argument
        return self.indent(f"{node.name}({', '.join(args)})")  # Return function call

    def translate_ArrayAssignmentNode(self, node):
        """Translates array assignments."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier  # Get variable name
        indices = []  # Initialize indices list
        for idx in node.indices:  # Loop through indices
            indices.append(self.translate_expression(idx, None))  # Translate and add index
        index_str = "".join(f"[{idx}]" for idx in indices)  # Build index string
        expr = self.translate_expression(node.expression, None)  # Translate expression
        return self.indent(f"{var_name}{index_str} {node.operator} {expr}")  # Return array assignment

    def translate_UnaryOperationNode(self, node):
        """Translates unary operations (++ and --)."""
        var_name = node.identifier  # Get variable name
        if node.operator == "++":  # If operator is increment
            return self.indent(f"{var_name} += 1")  # Return increment statement
        elif node.operator == "--":  # If operator is decrement
            return self.indent(f"{var_name} -= 1")  # Return decrement statement
        else:
            return self.indent(f"# Unsupported unary operator: {node.operator}")  # Return unsupported operator comment

    def translate_expression(self, tokens, name):
        if not tokens:  # If tokens is empty
            return ""  # Return empty string
        if isinstance(tokens, list) and tokens and tokens[0][0] == 'wish':  # If wish() function
            return self.translate_wish_function(tokens, name)  # Translate wish function
        if isinstance(tokens, list) and len(tokens) >= 3:  # If tokens is a list of length >= 3
            has_opening_brace = False  # Set opening brace flag to False
            has_closing_brace = False  # Set closing brace flag to False
            for token in tokens:  # Loop through tokens
                if isinstance(token, tuple):  # If token is a tuple
                    if token[0] == '{' or (token[0] == 'identifier' and token[1] == '{'):  # If opening brace
                        has_opening_brace = True  # Set flag to True
                    elif token[0] == '}' or (token[0] == 'identifier' and token[1] == '}'):  # If closing brace
                        has_closing_brace = True  # Set flag to True
            if has_opening_brace and has_closing_brace:  # If both braces exist
                return self.translate_array_initializer(tokens)  # Translate array initializer
        parts = []  # Initialize parts list
        i = 0  # Set index to 0
        while i < len(tokens):  # Loop through tokens
            token = tokens[i]  # Get current token
            if isinstance(token, tuple):  # If token is a tuple
                token_type, token_val = token  # Unpack token
                if token_type in ['totreasures', 'toocean', 'torose', 'toscroll', 'tomirror']:  # If type conversion
                    conversion_type = token_val  # Get conversion type
                    i += 1  # Increment index
                    while i < len(tokens) and (not isinstance(tokens[i], tuple) or tokens[i][0] != '('):  # Find opening parenthesis
                        i += 1  # Increment index
                    if i < len(tokens):  # If not at end
                        i += 1  # Skip opening parenthesis
                    inner_tokens = []  # Initialize inner tokens list
                    paren_count = 1  # Set parenthesis count to 1
                    while i < len(tokens) and paren_count > 0:  # Loop until closing parenthesis
                        if isinstance(tokens[i], tuple):  # If token is a tuple
                            if tokens[i][0] == '(':  # If opening parenthesis
                                paren_count += 1  # Increment count
                            elif tokens[i][0] == ')':  # If closing parenthesis
                                paren_count -= 1  # Decrement count
                        if paren_count > 0:  # If still inside parentheses
                            inner_tokens.append(tokens[i])  # Add token to inner tokens
                        i += 1  # Increment index
                    inner_expr = self.translate_expression(inner_tokens, None)  # Translate inner expression
                    if conversion_type == 'totreasures':  # If to int
                        parts.append(f"int({inner_expr})")  # Add int conversion
                    elif conversion_type == 'toocean':  # If to float
                        parts.append(f"float({inner_expr})")  # Add float conversion
                    elif conversion_type == 'torose':  # If to char
                        parts.append(f"{inner_expr}[0] if {inner_expr} else ''")  # Add char conversion
                    elif conversion_type == 'toscroll':  # If to string
                        parts.append(f"str({inner_expr})")  # Add string conversion
                    elif conversion_type == 'tomirror':  # If to bool
                        parts.append(f"bool({inner_expr})")  # Add bool conversion
                    i -= 1  # Decrement index for loop increment
                elif token_type == 'scroll_lit':  # If string literal
                    parts.append(token_val)  # Add string literal
                elif token_type == 'rose_lit':  # If char literal
                    parts.append(token_val)  # Add char literal
                elif token_type == 'mirror_lit':  # If boolean literal
                    parts.append("True" if token_val.lower() == "true" else "False")  # Add boolean value
                elif token_type == 'phantom':  # If None/null
                    parts.append("None")  # Add None
                elif token_type in ['treasures_lit', 'ocean_lit', 'identifier']:  # If number or identifier
                    parts.append(token_val)  # Add value
                elif token_type in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '++', '--']:  # If operator
                    if token_val == '&&':  # If logical and
                        parts.append('and')  # Add and
                    elif token_val == '||':  # If logical or
                        parts.append('or')  # Add or
                    elif token_val == '++':  # If increment
                        parts.append('+= 1')  # Add increment
                    elif token_val == '--':  # If decrement
                        parts.append('-= 1')  # Add decrement
                    else:
                        parts.append(token_val)  # Add operator
                elif token_type == '(':  # If opening parenthesis
                    parts.append('(')  # Add parenthesis
                elif token_type == ')':  # If closing parenthesis
                    parts.append(')')  # Add parenthesis
                elif token_type == '{':  # If opening brace
                    parts.append('[')  # Add opening bracket
                elif token_type == '}':  # If closing brace
                    parts.append(']')  # Add closing bracket
                elif token_type == 'lengthof':  # If lengthof
                    parts.append("len" + token_val[8:])  # Add len function
                elif token_type == '!':  # If not operator
                    parts.append("not" + token_val[1:])  # Add not
                else:
                    parts.append(str(token_val))  # Add token value
            else:
                parts.append(str(token))  # Add token as string
            i += 1  # Increment index
        return " ".join(parts)  # Join parts into string ['12', '*', '7'] = > 12 * 7

    def translate_array_initializer(self, tokens):
        """Translates array initializer expressions with curly braces to Python list syntax."""
        result = []  # Initialize result list
        self.in_array = False  # Set in_array flag to False
        for token in tokens:  # Loop through tokens
            if isinstance(token, tuple):  # If token is a tuple
                token_type, token_val = token  # Unpack token
                if token_type == '{' or (token_type == 'identifier' and token_val == '{'):  # If opening brace
                    result.append('[')  # Add opening bracket
                    self.in_array= True  # Set in_array flag to True
                elif token_type == '}' or (token_type == 'identifier' and token_val == '}'):  # If closing brace
                    result.append(']')  # Add closing bracket
                    self.in_array = False  # Set in_array flag to False
                elif token_type == ',':  # If comma
                    result.append(',')  # Add comma
                else:
                    result.append(token_val)  # Add token value
            else:
                result.append(str(token))  # Add token as string
        return " ".join(result)  # Join result into string

    def translate_wish_function(self, tokens, datatype):
        """Special handler for wish() function (input in RoyalScript)."""
        i = 2  # Set index to 2 to skip 'wish('
        prompt_tokens = []  # Initialize prompt tokens list
        while i < len(tokens) and tokens[i][0] != ')':  # Loop until closing parenthesis
            prompt_tokens.append(tokens[i])  # Add token to prompt tokens
            i += 1  # Increment index
        prompt_text = ""  # Initialize prompt text
        if prompt_tokens:  # If prompt tokens exist
            prompt_text = prompt_tokens[0][1].strip("'").strip('"')  # Get prompt text
            if not prompt_text.endswith('\n'):  # If prompt does not end with newline
                prompt_text += '\\n'  # Add newline
            prompt_text = f'"{prompt_text}"'  # Format prompt text
        # Handle appropriate type casting based on datatype
        if datatype == "treasures":     # int
            return f"(lambda v: int(v) if v.isdigit() else (print('Semantic Error: Invalid input value for treasures datatype.') or __import__('sys').exit()))(input({prompt_text}).strip())"
        elif datatype == "ocean":       # float
            return f"(lambda v: float(v) if (v.count('.') == 1 and v.replace('.', '', 1).replace('-', '', 1).isdigit() and v != '.' and v != '-.' and v[0] != '.' and v != '-0.' and v[0] in '-0123456789' and not v.replace('.', '', 1).replace('-', '', 1).isdigit() == v.lstrip('-')) else (print('Semantic Error: Invalid input value for ocean datatype.') or __import__('sys').exit()))(input({prompt_text}).strip())"
        elif datatype == "rose":  # char
            return f"(lambda v: v if len(v)==1 else (print('Semantic Error: Invalid input value for rose datatype.') or __import__('sys').exit()))(input({prompt_text}).strip())"
        elif datatype == "mirror":      # bool
            return f"(lambda v: v if v in ['true', '1', 'false', '0'] else (print('Semantic Error: Invalid input value for mirror datatype.') or __import__('sys').exit()))(input({prompt_text}).strip().lower())"
        else:
            # Default to string if we can't determine type
            return f"input({prompt_text})"
