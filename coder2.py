class RoyalScriptTranslator:
    """
    Translator for converting RoyalScript AST to Python code.
    """
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces for indentation
        self.output = []
        self.in_loop = False
        self.global_vars = set()
        
    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1
        
    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
        
    def write_line(self, line):
        """Write a line of code with proper indentation."""
        self.output.append(self.indent_str * self.indent_level + line)
        
    def write(self, code):
        """Write code without a newline."""
        if not self.output:
            self.output.append("")
        self.output[-1] += code
        
    def translate(self, ast_root):
        """
        Translate the AST to Python code.
        
        Args:
            ast_root: The root node of the AST (ProgramNode)
            
        Returns:
            str: The translated Python code
        """
        if not isinstance(ast_root, ProgramNode):
            raise ValueError("Expected ProgramNode as root of AST")
            
        # Add Python imports and setup
        self.write_line("# Generated Python code from RoyalScript")
        self.write_line("import sys")
        self.write_line("")
        
        # Translate global declarations
        if ast_root.global_declarations:
            self.write_line("# Global declarations")
            for decl in ast_root.global_declarations:
                self.translate_declaration(decl)
            self.write_line("")
        
        # Translate functions
        if ast_root.functions:
            self.write_line("# Function definitions")
            for func in ast_root.functions:
                self.translate_function(func)
                self.write_line("")
        
        # Translate main function
        if ast_root.main_function:
            self.write_line("# Main function")
            self.translate_main_function(ast_root.main_function)
        else:
            self.write_line("# No main function found")
        
        # Add code to call main function
        self.write_line("")
        self.write_line("if __name__ == '__main__':")
        self.indent()
        self.write_line("sys.exit(main())")
        
        return "\n".join(self.output)
    
    def translate_declaration(self, declaration):
        """Translate variable declaration to Python."""
        # Handle multiple declarations (we get a list)
        if isinstance(declaration, list):
            for decl in declaration:
                self.translate_declaration(decl)
            return
            
        # Skip type information as Python is dynamically typed
        name = declaration.identifier[1] if isinstance(declaration.identifier, tuple) else declaration.identifier
        
        # Add to global vars set if global
        if declaration.scope_level == GLOBAL_SCOPE:
            self.global_vars.add(name)
            
        # Handle array declarations
        if declaration.array_dimensions:
            # 1D array
            if len(declaration.array_dimensions) == 1:
                size = declaration.array_dimensions[0][1] if isinstance(declaration.array_dimensions[0], tuple) else declaration.array_dimensions[0]
                if declaration.value:
                    value_str = self.translate_expression(declaration.value)
                    self.write_line(f"{name} = {value_str}")
                else:
                    self.write_line(f"{name} = [None] * {size}")
            # 2D array
            elif len(declaration.array_dimensions) == 2:
                size1 = declaration.array_dimensions[0][1] if isinstance(declaration.array_dimensions[0], tuple) else declaration.array_dimensions[0]
                size2 = declaration.array_dimensions[1][1] if isinstance(declaration.array_dimensions[1], tuple) else declaration.array_dimensions[1]
                if declaration.value:
                    value_str = self.translate_expression(declaration.value)
                    self.write_line(f"{name} = {value_str}")
                else:
                    self.write_line(f"{name} = [[None] * {size2} for _ in range({size1})]")
        # Regular variable declaration
        else:
            if declaration.value:
                value_str = self.translate_expression(declaration.value)
                self.write_line(f"{name} = {value_str}")
            else:
                self.write_line(f"{name} = None")
                
    def translate_function(self, function):
        """Translate function definition to Python."""
        name = function.identifier[1] if isinstance(function.identifier, tuple) else function.identifier
        
        # Create parameter list
        params = []
        for param in function.parameters:
            datatype, identifier = param
            param_name = identifier[1] if isinstance(identifier, tuple) else identifier
            params.append(param_name)
        param_str = ", ".join(params)
        
        # Function definition
        self.write_line(f"def {name}({param_str}):")
        self.indent()
        
        # Add global variable declarations if needed
        globals_in_func = []
        for global_var in self.global_vars:
            globals_in_func.append(global_var)
        
        if globals_in_func:
            self.write_line(f"global {', '.join(globals_in_func)}")
        
        # Empty function body
        if not function.body:
            self.write_line("pass")
        else:
            # Translate function body
            self.translate_body(function.body)
        
        # Return statement
        if function.return_val:
            return_str = self.translate_expression(function.return_val)
            self.write_line(f"return {return_str}")
        else:
            # Add default return None for functions if no return statement
            # Only add if the return type isn't 'void'
            if function.return_type[0] != 'void':
                self.write_line("return None")
                
        self.dedent()
    
    def translate_main_function(self, main_function):
        """Translate the main function to Python."""
        name = main_function.identifier[1] if isinstance(main_function.identifier, tuple) else main_function.identifier
        
        self.write_line(f"def main():")
        self.indent()
        
        # Add global variable declarations if needed
        globals_in_main = []
        for global_var in self.global_vars:
            globals_in_main.append(global_var)
        
        if globals_in_main:
            self.write_line(f"global {', '.join(globals_in_main)}")
        
        # Empty main function body
        if not main_function.body:
            self.write_line("pass")
        else:
            # Translate main function body
            self.translate_body(main_function.body)
        
        # Return statement (should be 0 for main)
        return_val = main_function.return_val[1] if isinstance(main_function.return_val, tuple) else main_function.return_val
        self.write_line(f"return {return_val}")
        
        self.dedent()
    
    def translate_body(self, body):
        """Translate function/block body to Python."""
        for node in body:
            if isinstance(node, list):
                for item in node:
                    self.translate_node(item)
            else:
                self.translate_node(node)
    
    def translate_node(self, node):
        """Translate a single AST node to Python code."""
        if isinstance(node, VariableDeclarationNode):
            self.translate_declaration(node)
        elif isinstance(node, VariableReassignmentNode):
            self.translate_var_reassignment(node)
        elif isinstance(node, FunctionNode):
            self.translate_function(node)
        elif isinstance(node, FunctionCallNode):
            self.write_line(self.translate_function_call(node))
        elif isinstance(node, DoWhileNode):
            self.translate_do_while(node)
        elif isinstance(node, WhileNode):
            self.translate_while(node)
        elif isinstance(node, IfNode):
            self.translate_if(node)
        elif isinstance(node, ForLoopNode):
            self.translate_for_loop(node)
        elif isinstance(node, BreakNode):
            self.write_line("break")
        elif isinstance(node, ContinueNode):
            self.write_line("continue")
        elif isinstance(node, ArrayAssignmentNode):
            self.translate_array_assignment(node)
        elif isinstance(node, UnaryOperationNode):
            self.translate_unary_operation(node)
        elif isinstance(node, OutputNode):
            self.translate_output(node)
        else:
            self.write_line(f"# Unknown node type: {type(node)}")
    
    def translate_var_reassignment(self, node):
        """Translate variable reassignment to Python."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        op = node.operator[0] if isinstance(node.operator, tuple) else node.operator
        expr = self.translate_expression(node.expression)
        
        # Direct assignment
        if op == '=':
            self.write_line(f"{var_name} = {expr}")
        # Compound assignment
        elif op in ['+=', '-=', '*=', '/=', '%=']:
            self.write_line(f"{var_name} {op} {expr}")
    
    def translate_function_call(self, node):
        """Translate function call to Python."""
        func_name = node.name
        args = []
        
        for arg in node.arguments:
            args.append(self.translate_expression(arg))
        
        arg_str = ", ".join(args)
        return f"{func_name}({arg_str})"
    
    def translate_do_while(self, node):
        """Translate do-while loop to Python."""
        # Python doesn't have a direct do-while, so we simulate it
        self.write_line("# do-while loop")
        self.write_line("while True:")
        self.indent()
        
        # Mark that we're in a loop for break/continue context
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Translate loop body
        self.translate_body(node.loop_body)
        
        # Translate condition for while check (with negation to break)
        condition = self.translate_expression(node.condition)
        self.write_line(f"if not ({condition}):")
        self.indent()
        self.write_line("break")
        self.dedent()
        
        self.dedent()
        self.in_loop = old_in_loop
    
    def translate_while(self, node):
        """Translate while loop to Python."""
        condition = self.translate_expression(node.condition)
        
        self.write_line(f"while {condition}:")
        self.indent()
        
        # Mark that we're in a loop for break/continue context
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Translate loop body
        self.translate_body(node.loop_body)
        
        self.dedent()
        self.in_loop = old_in_loop
    
    def translate_if(self, node):
        """Translate if statement to Python."""
        condition = self.translate_expression(node.condition)
        
        self.write_line(f"if {condition}:")
        self.indent()
        self.translate_body(node.body)
        self.dedent()
        
        # Translate elif statements
        for elif_node in node.elif_nodes:
            elif_condition = self.translate_expression(elif_node.condition)
            self.write_line(f"elif {elif_condition}:")
            self.indent()
            self.translate_body(elif_node.body)
            self.dedent()
        
        # Translate else statement if present
        if node.else_node:
            self.write_line("else:")
            self.indent()
            self.translate_body(node.else_node.body)
            self.dedent()
    
    def translate_for_loop(self, node):
        """Translate for loop to Python."""
        # Initialize loop variable
        init = self.translate_tokens(node.loop_var)
        
        # Extract parts of the for loop
        condition = self.translate_tokens(node.loop_exp)
        update = self.translate_tokens(node.loop_unary)
        
        # Determine the variable name and initial value
        if '=' in init:
            var_name, initial_value = init.split(' = ', 1)
        else:
            self.write_line(f"# Could not parse for loop initialization: {init}")
            var_name = "i"
            initial_value = "0"
        
        # Determine the condition for continuing the loop
        if '<' in condition:
            parts = condition.split(' < ', 1)
            end_value = parts[1]
            comparison = '<'
        elif '<=' in condition:
            parts = condition.split(' <= ', 1)
            end_value = parts[1]
            comparison = '<='
        elif '>' in condition:
            parts = condition.split(' > ', 1)
            end_value = parts[1]
            comparison = '>'
        elif '>=' in condition:
            parts = condition.split(' >= ', 1)
            end_value = parts[1]
            comparison = '>='
        else:
            self.write_line(f"# Could not parse for loop condition: {condition}")
            end_value = "10" 
            comparison = '<'
        
        # Determine the step value
        if '++' in update:
            step = "1"
        elif '--' in update:
            step = "-1"
        else:
            # Try to extract step value from compound assignment
            if '+=' in update:
                step = update.split(' += ', 1)[1]
            elif '-=' in update:
                step = f"-({update.split(' -= ', 1)[1]})"
            else:
                self.write_line(f"# Could not parse for loop update: {update}")
                step = "1"
        
        # Write the for loop in Python style
        if comparison in ['<', '<='] and step == "1":
            # Standard incrementing loop
            end_adjust = "1" if comparison == '<=' else "0"
            self.write_line(f"for {var_name} in range({initial_value}, {end_value} + {end_adjust}):")
        elif comparison in ['>', '>='] and step == "-1":
            # Standard decrementing loop
            end_adjust = "1" if comparison == '>=' else "0"
            self.write_line(f"for {var_name} in range({initial_value}, {end_value} - {end_adjust}, -1):")
        else:
            # Custom step loop, we need to use while
            self.write_line(f"{var_name} = {initial_value}")
            self.write_line(f"while {var_name} {comparison} {end_value}:")
            self.indent()
            
            # Mark that we're in a loop
            old_in_loop = self.in_loop
            self.in_loop = True
            
            # Translate loop body
            self.translate_body(node.loop_body)
            
            # Update the loop variable
            if step != "1" and step != "-1":
                self.write_line(f"{var_name} += {step}")
            elif step == "1":
                self.write_line(f"{var_name} += 1")
            else:  # step == "-1"
                self.write_line(f"{var_name} -= 1")
                
            self.dedent()
            self.in_loop = old_in_loop
            return
        
        # For the standard range-based loops
        self.indent()
        
        # Mark that we're in a loop
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Translate loop body
        self.translate_body(node.loop_body)
        
        self.dedent()
        self.in_loop = old_in_loop
    
    def translate_array_assignment(self, node):
        """Translate array assignment to Python."""
        var_name = node.identifier[1] if isinstance(node.identifier, tuple) else node.identifier
        
        # Build the indices
        indices_str = ""
        for index in node.indices:
            index_expr = self.translate_expression(index)
            indices_str += f"[{index_expr}]"
        
        # Get the expression being assigned
        expr = self.translate_expression(node.expression)
        
        # Handle different assignment operators
        if node.operator == '=':
            self.write_line(f"{var_name}{indices_str} = {expr}")
        elif node.operator in ['+=', '-=', '*=', '/=', '%=']:
            self.write_line(f"{var_name}{indices_str} {node.operator} {expr}")
    
    def translate_unary_operation(self, node):
        """Translate unary operation (++ or --) to Python."""
        var_name = node.identifier
        
        if node.operator == '++':
            self.write_line(f"{var_name} += 1")
        elif node.operator == '--':
            self.write_line(f"{var_name} -= 1")
    
    def translate_output(self, node):
        """Translate output statement to Python print statement."""
        expr_str = self.translate_expression(node.expressions)
        self.write_line(f"print({expr_str})")
    
    def translate_expression(self, expression):
        """Translate an expression to Python code."""
        if not expression:
            return ""
            
        # Handle token types
        if isinstance(expression, tuple):
            token_type, token_value = expression
            
            if token_type == 'string_literal':
                return f'"{token_value}"'
            elif token_type == 'int_literal':
                return token_value
            elif token_type == 'float_literal':
                return token_value
            elif token_type == 'identifier':
                return token_value
            else:
                return token_value
        
        # Handle lists of tokens
        return self.translate_tokens(expression)
    
    def translate_tokens(self, tokens):
        """Translate a list of tokens to a Python expression string."""
        if not tokens:
            return ""
            
        result = []
        for token in tokens:
            if isinstance(token, tuple):
                token_type, token_value = token
                
                # Handle different token types
                if token_type == 'string_literal':
                    result.append(f'"{token_value}"')
                elif token_type in ['int_literal', 'float_literal', 'identifier']:
                    result.append(token_value)
                elif token_type == 'input_prompt':  # Handle input token
                    result.append("input()")
                else:
                    # Handle operators and other tokens
                    result.append(token_value)
            else:
                # Basic token
                result.append(str(token))
        
        # Join with spaces, except for specific punctuation
        no_space_before = set([')', ']', '.', ',', ';', ':', '~'])
        no_space_after = set(['(', '['])
        
        formatted_result = ""
        for i, part in enumerate(result):
            if i > 0:
                prev = result[i-1]
                if (part not in no_space_before and 
                    prev not in no_space_after):
                    formatted_result += " "
            formatted_result += part
            
        return formatted_result


def translate_royalscript(ast_root):
    """
    Convenience function to translate a RoyalScript AST to Python code.
    
    Args:
        ast_root: The root node of the AST (ProgramNode)
        
    Returns:
        str: The translated Python code
    """
    translator = RoyalScriptTranslator()
    return translator.translate(ast_root)


# Example usage (commented out)
"""
# Create an AST manually or parse it from source
ast = ProgramNode(
    globals=[
        VariableDeclarationNode('int', ('identifier', 'x'), [('int_literal', '10')], False, GLOBAL_SCOPE, [])
    ],
    functions=[
        FunctionNode(('int', 'int'), ('identifier', 'add'), 
                   [(('int', 'int'), ('identifier', 'a')), (('int', 'int'), ('identifier', 'b'))], 
                   [], [('identifier', 'a'), ('+', '+'), ('identifier', 'b')], True, GLOBAL_SCOPE)
    ],
    main_function=MainFunctionNode(('identifier', 'main'), 
                                 [
                                     OutputNode([('string_literal', 'Hello, world!')])
                                 ], 
                                 ('int_literal', '0'))
)

# Translate
code = translate_royalscript(ast)
print(code)
"""