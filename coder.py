import textwrap
import ast
import black  # For code formatting
import re
from io import StringIO

class RoyalScriptToPythonTranslator:
    def __init__(self):
        self.indent_level = 0
        self.symbol_table = {}  # To track variable types

    def indent(self, text):
        """Indent the given text according to the current indent_level.
           This method uses textwrap.indent to handle multi-line strings.
        """
        prefix = "    " * self.indent_level
        return textwrap.indent(text, prefix)

    def translate(self, node):
        """Dispatches to the appropriate translation method based on node type."""
        method_name = f"translate_{type(node).__name__}"
        method = getattr(self, method_name, self.unsupported_node)
        return method(node)

    def unsupported_node(self, node):
        """Handles unsupported node types."""
        raise NotImplementedError(f"No translation method defined for {type(node).__name__}")

    def format_code(self, code):
        """Format Python code using Black formatter."""
        try:
            # Use black to format the code
            formatted_code = black.format_str(
                code, 
                mode=black.Mode(
                    line_length=88,
                    string_normalization=True,
                    is_pyi=False,
                )
            )
            return formatted_code
        except Exception as e:
            # If formatting fails, return the original code with a comment
            print(f"Warning: Code formatting failed: {e}")
            return f"# Note: Auto-formatting failed\n{code}"

    def validate_code(self, code):
        """Validates Python code by parsing it with the ast module."""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"Generated code has syntax error: {e}")
            return False

    def translate_ProgramNode(self, node):
        """Translates the root program node to Python code."""
        # Start with module imports
        code = ["import sys"]
        
        # Add global declarations
        for decl in node.global_declarations:
            translated = self.translate(decl)
            if translated.strip():  # Only add non-empty translations
                code.append(translated)
        
        # Add functions with proper spacing
        for func in node.functions:
            code.append("")  # Add empty line before each function
            code.append(self.translate(func))
        
        # Add main function
        code.append("")  # Add empty line before main
        code.append(self.translate(node.main_function))
        
        # Join all code and format it
        raw_code = "\n".join(code)
        return self.format_code(raw_code)

    def translate_VariableDeclarationNode(self, node):
        """Translates variable declarations to Python assignments."""
        # Handle multiple variable declarations
        if isinstance(node.identifier, list):
            # Extract identifiers
            identifiers = []
            for ident in node.identifier:
                if isinstance(ident, tuple) and len(ident) >= 2:
                    identifiers.append(ident[1])
                    # Update symbol table with variable type
                    if hasattr(node, 'datatype'):
                        self.symbol_table[ident[1]] = node.datatype[1]
                else:
                    identifiers.append(str(ident))
            
            identifiers_str = ", ".join(identifiers)
            
            # Handle values
            if isinstance(node.value, list) and all(isinstance(val, list) for val in node.value):
                values = ", ".join(self.translate_expression(val, node.datatype[1]) for val in node.value)
            else:
                values = self.translate_expression(node.value, node.datatype[1])
                
            return self.indent(f"{identifiers_str} = {values}")
        
        # Handle single variable declaration
        else:
            # Update symbol table
            if isinstance(node.identifier, tuple) and len(node.identifier) >= 2:
                var_name = node.identifier[1]
                if hasattr(node, 'datatype') and isinstance(node.datatype, tuple):
                    self.symbol_table[var_name] = node.datatype[1]
            
            # Handle arrays specially
            if node.array_dimensions:
                return self.translate_array_declaration(node)
                
            # Regular variable declaration
            value = self.translate_expression(node.value, node.datatype[1]) if node.value else "None"
            if isinstance(node.identifier, tuple):
                return self.indent(f"{node.identifier[1]} = {value}")
            else:
                return self.indent(f"{node.identifier} = {value}")

    def translate_array_declaration(self, node):
        """Translates array declarations to Python lists or nested lists."""
        var_name = node.identifier[1]
        
        # Get array dimensions
        dimensions = []
        for dim in node.array_dimensions:
            if isinstance(dim, tuple):
                dimensions.append(dim[1])
            else:
                dimensions.append(str(dim))
        
        # Create array initialization code
        if len(dimensions) == 1:
            # 1D array
            if node.value:
                return self.indent(f"{var_name} = {self.translate_expression(node.value, None)}")
            else:
                return self.indent(f"{var_name} = [None] * {dimensions[0]}")
        elif len(dimensions) == 2:
            # 2D array
            if node.value:
                return self.indent(f"{var_name} = {self.translate_expression(node.value, None)}")
            else:
                return self.indent(f"{var_name} = [[None] * {dimensions[1]} for _ in range({dimensions[0]})]")
        else:
            return self.indent(f"# Unsupported array dimension: {len(dimensions)}")

    def translate_VariableReassignmentNode(self, node):
        """Translates variable reassignments."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        operator = node.operator[1] if isinstance(node.operator, tuple) else node.operator
        expr = self.translate_expression(node.expression, None)
        return self.indent(f"{var_name} {operator} {expr}")

    def translate_FunctionNode(self, node):
        """Translates function definitions."""
        # Extract function name
        func_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Extract parameters
        params = []
        for param in (node.parameters or []):
            if isinstance(param, tuple) and len(param) >= 2:
                # param is (datatype, (token_type, token_value))
                param_name = param[1][1] if isinstance(param[1], tuple) else param[1]
                params.append(param_name)
        param_str = ", ".join(params)
        
        # Function definition
        code = [f"def {func_name}({param_str}):"]
        
        # If body is empty, add a pass statement
        if not node.body and node.return_type == 'chamber':
            self.indent_level += 1
            code.append(self.indent("pass"))
            self.indent_level -= 1
        else:
        # Translate function body
            self.indent_level += 1
            for stmt in node.body:
                translated = self.translate(stmt)
                if translated.strip():  # Only add non-empty translations
                    code.append(translated)
            
            # Add return statement if present
            if node.return_val:
                ret_expr = self.translate_expression(node.return_val, None)
                code.append(self.indent(f"return {ret_expr}"))
            self.indent_level -= 1
    
        return "\n".join(code)

    def translate_MainFunctionNode(self, node):
        """Translates the main function and adds code to call it."""
        # Extract main function name
        main_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Function definition
        code = [f"def {main_name}():"]
        
        # Translate function body
        self.indent_level += 1
        for stmt in node.body:
            translated = self.translate(stmt)
            if translated.strip():  # Only add non-empty translations
                code.append(translated)
        
        # Add return statement
        return_val = node.return_val[1] if isinstance(node.return_val, tuple) else node.return_val
        code.append(self.indent(f"return {return_val}"))
        self.indent_level -= 1
        
        # Add code to call the main function
        code.append("")
        code.append(f"if __name__ == \"__main__\":")
        code.append(f"    {main_name}()")
        
        return "\n".join(code)

    def translate_IfNode(self, node):
        """Translates if statements with elif and else branches."""
        code = []
        
        # Translate the condition
        condition = self.translate_expression(node.condition, None)
        code.append(self.indent(f"if {condition}:"))
        
        # Translate if body
        self.indent_level += 1
        if node.body:
            for stmt in node.body:
                code.append(self.translate(stmt))
        else:
            code.append(self.indent("pass"))
        self.indent_level -= 1
        
        # Translate elif nodes
        for elif_node in (node.elif_nodes or []):
            elif_condition = self.translate_expression(elif_node.condition, None)
            code.append(self.indent(f"elif {elif_condition}:"))
            
            self.indent_level += 1
            if elif_node.body:
                for stmt in elif_node.body:
                    code.append(self.translate(stmt))
            else:
                code.append(self.indent("pass"))
            self.indent_level -= 1
        
        # Translate else node
        if node.else_node:
            code.append(self.indent("else:"))
            
            self.indent_level += 1
            if node.else_node.body:
                for stmt in node.else_node.body:
                    code.append(self.translate(stmt))
            else:
                code.append(self.indent("pass"))
            self.indent_level -= 1
        
        return "\n".join(code)

    def translate_WhileNode(self, node):
        """Translates while loops."""
        code = []
        
        # Translate condition
        condition = self.translate_expression(node.condition, None)
        code.append(self.indent(f"while {condition}:"))
        
        # Translate loop body
        self.indent_level += 1
        if node.loop_body:
            for stmt in node.loop_body:
                code.append(self.translate(stmt))
        else:
            code.append(self.indent("pass"))
        self.indent_level -= 1
        
        return "\n".join(code)

    def translate_DoWhileNode(self, node):
        """Translates do-while loops to Python using a while True with break."""
        code = []
        
        # In Python we emulate do-while with while True + break
        code.append(self.indent("while True:"))
        
        # Translate loop body
        self.indent_level += 1
        if node.loop_body:
            for stmt in node.loop_body:
                code.append(self.translate(stmt))
        
        # Add condition check at the end with break
        condition = self.translate_expression(node.condition, None)
        code.append(self.indent(f"if not ({condition}):"))
        self.indent_level += 1
        code.append(self.indent("break"))
        self.indent_level -= 1
        self.indent_level -= 1
        
        return "\n".join(code)

    def translate_ForLoopNode(self, node):
        """Translates for loops."""
        code = []
        
        # Extract initialization, condition, and update parts
        init = self.translate_expression(node.loop_var, None)
        condition = self.translate_expression(node.loop_exp, None)
        update = self.translate_expression(node.loop_unary, None)
        
        # In Python, we need to emulate C-style for loops with while
        code.append(self.indent(f"{init}"))
        code.append(self.indent(f"while {condition}:"))
        
        # Translate loop body
        self.indent_level += 1
        if node.loop_body:
            for stmt in node.loop_body:
                code.append(self.translate(stmt))
        
        # Add the update statement at the end of each iteration
        code.append(self.indent(f"{update}"))
        self.indent_level -= 1
        
        return "\n".join(code)

    def translate_BreakNode(self, node):
        """Translates break statements."""
        return self.indent("break")

    def translate_ContinueNode(self, node):
        """Translates continue statements."""
        return self.indent("continue")

    def translate_OutputNode(self, node):
        """Translates output statements (print statements)."""
        # Parse the expressions to print
        expressions = []
        i = 0
        
        # Group tokens into separate expressions (separated by commas)
        current_expr = []
        while i < len(node.expressions):
            token = node.expressions[i]
            
            if token[0] == ',':
                if current_expr:  # Only add non-empty expressions
                    expressions.append(current_expr)
                    current_expr = []
            elif token[0] == 'setprecission':
                # Handle precision specifier specially
                precision_value = None
                if i + 2 < len(node.expressions) and node.expressions[i+1][0] == ',':
                    precision_value = node.expressions[i+2]
                    i += 2  # Skip the comma and value
                
                # Store as a special token with its value
                if precision_value:
                    current_expr.append(('precision', precision_value))
            else:
                current_expr.append(token)
            
            i += 1
        
        # Add the last expression if not empty
        if current_expr:
            expressions.append(current_expr)
        
        # Translate each expression
        print_args = []
        for expr in expressions:
            # Check for precision formatting
            has_precision = False
            precision_value = None
            filtered_expr = []
            
            for token in expr:
                if token[0] == 'precision':
                    has_precision = True
                    precision_value = token[1]
                else:
                    filtered_expr.append(token)
            
            translated = self.translate_expression(filtered_expr, None)
            
            # Apply precision formatting if needed
            if has_precision and precision_value:
                prec_val = precision_value[1] if isinstance(precision_value, tuple) else precision_value
                translated = f"f'{{{float({translated}):.{prec_val}f}}}'"
            
            print_args.append(translated)
        
        # Construct the print statement without automatic newline
        return self.indent(f"print({', '.join(print_args)}, end='')")  # Added `end=''` to prevent newline


    def translate_FunctionCallNode(self, node):
        """Translates function calls."""
        # Translate each argument
        args = []
        for arg in node.arguments:
            args.append(self.translate_expression(arg, None))
        
        return self.indent(f"{node.name}({', '.join(args)})")

    def translate_ArrayAssignmentNode(self, node):
        """Translates array assignments."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Build index access
        indices = []
        for idx in node.indices:
            indices.append(self.translate_expression(idx, None))
        
        index_str = "".join(f"[{idx}]" for idx in indices)
        
        # Handle the expression
        expr = self.translate_expression(node.expression, None)
        
        # Compose the assignment
        return self.indent(f"{var_name}{index_str} {node.operator} {expr}")

    def translate_UnaryOperationNode(self, node):
        """Translates unary operations (++ and --)."""
        var_name = node.identifier
        
        # Map ++ and -- to Python equivalents
        if node.operator == "++":
            return self.indent(f"{var_name} += 1")
        elif node.operator == "--":
            return self.indent(f"{var_name} -= 1")
        else:
            return self.indent(f"# Unsupported unary operator: {node.operator}")

    def translate_expression(self, tokens, name):
        if not tokens:
            return ""
        
        # Handle wish() function call for input
        if isinstance(tokens, list) and tokens and tokens[0][0] == 'wish':
            return self.translate_wish_function(tokens, name)
        
        # Process tokens into Python expression
        parts = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if isinstance(token, tuple):
                token_type, token_val = token
                
                # Handle type conversion functions
                if token_type in ['totreasures', 'toocean', 'torose', 'toscroll', 'tomirror']:
                    # This is a type conversion function
                    conversion_type = token_val
                    
                    # Find opening parenthesis
                    i += 1
                    while i < len(tokens) and (not isinstance(tokens[i], tuple) or tokens[i][0] != '('):
                        i += 1
                    
                    if i < len(tokens):
                        i += 1  # Skip '('
                    
                    # Collect tokens for the inner expression
                    inner_tokens = []
                    paren_count = 1
                    
                    while i < len(tokens) and paren_count > 0:
                        if isinstance(tokens[i], tuple):
                            if tokens[i][0] == '(':
                                paren_count += 1
                            elif tokens[i][0] == ')':
                                paren_count -= 1
                                
                        if paren_count > 0:
                            inner_tokens.append(tokens[i])
                        
                        i += 1
                    
                    # Convert the inner expression
                    inner_expr = self.translate_expression(inner_tokens, None)
                    
                    # Apply the appropriate type conversion
                    if conversion_type == 'totreasures':
                        parts.append(f"int({inner_expr})")
                    elif conversion_type == 'toocean':
                        parts.append(f"float({inner_expr})")
                    elif conversion_type == 'torose':
                        parts.append(f"{inner_expr}[0] if {inner_expr} else ''")  # Get first char
                    elif conversion_type == 'toscroll':
                        parts.append(f"str({inner_expr})")
                    elif conversion_type == 'tomirror':
                        parts.append(f"bool({inner_expr})")
                    
                    # Skip to next token
                    i -= 1  # Adjust for the loop increment
                elif token_type == 'scroll_lit':
                    # String literal
                    parts.append(token_val)
                elif token_type == 'rose_lit':
                    # Character literal, ensuring it's properly quoted
                    parts.append("'" + token_val.strip("'") + "'")
                elif token_type == 'mirror_lit':
                    # Boolean literal
                    parts.append("True" if token_val.lower() == "true" else "False")
                elif token_type == 'phantom':
                    # None/null value
                    parts.append("None")
                elif token_type in ['treasures_lit', 'ocean_lit', 'identifier']:
                    # Numbers and identifiers
                    parts.append(token_val)
                elif token_type in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '++', '--']:
                    # Operators, with special handling for logical operators
                    if token_val == '&&':
                        parts.append('and')
                    elif token_val == '||':
                        parts.append('or')
                    elif token_val == '++':
                        parts.append('+= 1')
                    elif token_val == '--':
                        parts.append('-= 1')
                    else:
                        parts.append(token_val)
                elif token_type == '(':
                    parts.append('(')
                elif token_type == ')':
                    parts.append(')')
                elif token_type == '!':
                    # NOT operator - replace ! with not but preserve the rest of the value
                    parts.append("not" + token_val[1:] if len(token_val) > 1 else "not")
                else:
                    # Default case: use the token value
                    parts.append(str(token_val))
            else:
                # If not a tuple, just add the token as string
                parts.append(str(token))
            
            i += 1
        
        return " ".join(parts)

    def translate_wish_function(self, tokens, datatype):
        """Special handler for wish() function (input in RoyalScript)."""
        
        # Extract the prompt inside wish()
        prompt = ""
        i = 1  # Skip 'wish' token
        
        # Skip opening parenthesis
        while i < len(tokens) and tokens[i][0] != '(':
            i += 1
        if i < len(tokens):
            i += 1  # Move past '('
        
        # Collect tokens until closing parenthesis
        prompt_tokens = []
        while i < len(tokens) and tokens[i][0] != ')':
            prompt_tokens.append(tokens[i])
            i += 1
        
        # Format the prompt
        if prompt_tokens:
            prompt =  prompt_tokens[0][1].strip("'")
            # prompt = prompt.replace('"', '\"')  # Escape quotes

        # Guarantee the prompt shows before input
        input_expr = f'input({prompt})'
        
        # Handle appropriate type casting based on datatype
        if datatype == "treasures":     # int
            return f"int(input({prompt}))"
        elif datatype == "ocean":       # float
            return f"float(input({prompt}))"
        elif datatype == "rose":        # char
            return f"input({prompt})[:1]"
        elif datatype == "mirror":      # bool
            return f"input({prompt}).lower() in ['true', '1', 'yes', 'y']"
        else:
            # Default to string if we can't determine type
            return input_expr


    def get_assignment_target(self, tokens):
        """
        Try to determine the variable being assigned to in the current context.
        Used to guide type casting for input functions.
        """
        # This is a simplified approach - actual implementation would need
        # to look at the parent node in the AST
        return True # Placeholder