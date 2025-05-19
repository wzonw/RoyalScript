GLOBAL_SCOPE = 0
LOCAL_SCOPE = 1

class Node:
    """Base class for all AST nodes"""
    def __init__(self, line=None, position=None):
        self.line = line
        self.position = position


class ASTBuildingException(Exception):
    """
    Custom exception raised when there's an error specific
    to building the AST (not just a syntax or semantic error).
    """
    def __init__(self, message: str, line: int = None, position: int = None):
        """
        Args:
            message (str): A descriptive error message.
            line (int, optional): The line where the error occurred.
            position (int, optional): The position (column) in the line.
        """
        super().__init__(message)
        self.line = line
        self.position = position

    def __str__(self):
        base_msg = super().__str__()
        if self.line is not None and self.position is not None:
            return f"{base_msg} at line {self.line + 1}, position {self.position + 1}"
        return base_msg


class ProgramNode(Node):
    def __init__(self, globals, functions, main_function, line=None, position=None):
        super().__init__(line, position)
        self.global_declarations = globals
        self.functions = functions
        self.main_function = main_function

class VariableDeclarationNode(Node):
    def __init__(self, datatype, identifier, value=None, is_dynasty=False, scope_level=GLOBAL_SCOPE, array_dimensions=None, line=None, position=None):
        super().__init__(line, position)
        self.datatype = datatype
        self.identifier = identifier
        self.value = value
        self.is_dynasty = is_dynasty
        self.scope_level = scope_level
        self.array_dimensions = array_dimensions if array_dimensions is not None else []

class VariableReassignmentNode(Node):
    def __init__(self, identifier, operator, expression, line=None, position=None):
        super().__init__(line, position)
        self.identifier = identifier  # Variable name
        self.operator = operator  # Assignment operator (=, +=, -=, etc.)
        self.expression = expression  # Expression being assigned

class FunctionNode(Node):
    def __init__(self, return_type, identifier, parameters, body, return_val=None, is_global=True, scope_level=GLOBAL_SCOPE, line=None, position=None):
        super().__init__(line, position)
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.body = body
        self.return_val = return_val
        self.is_global = is_global
        self.scope_level = scope_level

class FunctionCallNode(Node):
    def __init__(self, name, arguments, line=None, position=None):
        super().__init__(line, position)
        self.name = name  # Function name
        self.arguments = arguments  # List of argument expressions

class DoWhileNode(Node):
    def __init__(self, loop_body, condition, line=None, position=None):
        super().__init__(line, position)
        self.loop_body = loop_body
        self.condition = condition

class WhileNode(Node):
    def __init__(self, loop_body, condition, line=None, position=None):
        super().__init__(line, position)
        self.loop_body = loop_body
        self.condition = condition

class IfNode(Node):
    def __init__(self, condition, body, elif_nodes=None, else_node=None, line=None, position=None):
        super().__init__(line, position)
        self.condition = condition
        self.body = body
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.else_node = else_node if else_node else []

class ElifNode(Node):
    def __init__(self, condition, body, line=None, position=None):
        super().__init__(line, position)
        self.condition = condition
        self.body = body

class ElseNode(Node):
    def __init__(self, body, line=None, position=None):
        super().__init__(line, position)
        self.body = body

class BreakNode(Node):
    def __init__(self, line=None, position=None):
        super().__init__(line, position)
        self.type = 'break'

class ContinueNode(Node):
    def __init__(self, line=None, position=None):
        super().__init__(line, position)
        self.type = 'continue'

class ForLoopNode(Node):
    def __init__(self, loop_var, loop_exp, loop_unary, loop_body, line=None, position=None):
        super().__init__(line, position)
        self.loop_var = loop_var          # initialization
        self.loop_exp = loop_exp          # condition
        self.loop_unary = loop_unary      # update (unary operation)
        self.loop_body = loop_body        # body of the loop

class LiteralNode(Node):
    def __init__(self, value, datatype, line=None, position=None):
        super().__init__(line, position)
        self.value = value
        self.datatype = datatype

class MainFunctionNode(Node):
    def __init__(self, identifier, body, return_val, line=None, position=None):
        super().__init__(line, position)
        self.identifier = identifier
        self.body = body
        self.return_val = return_val

class ArrayAssignmentNode(Node):
    def __init__(self, identifier, indices, operator, expression, line=None, position=None):
        super().__init__(line, position)
        self.identifier = identifier      # Array name
        self.indices = indices            # List of index expressions
        self.operator = operator          # Assignment operator
        self.expression = expression      # Expression being assigned

class UnaryOperationNode(Node):
    def __init__(self, identifier, operator, line=None, position=None):
        super().__init__(line, position)
        self.identifier = identifier  # Variable name
        self.operator = operator      # ++ or --

class OutputNode(Node):
    def __init__(self, expressions, line=None, position=None):
        super().__init__(line, position)
        self.expressions = expressions

class RoyalScriptASTBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_line = 0
        self.current_index = 0
        self.current_position = (0, 0)  # (line, index) for better error messages

    def _skip_comments(self):
        """Internal method to skip comments across lines."""
        while self.current_line < len(self.tokens):
            # If line is empty, move to next line
            if not self.tokens[self.current_line]:
                self.current_line += 1
                self.current_index = 0
                continue

            # Check if current token is a comment
            while (self.current_index < len(self.tokens[self.current_line]) and 
                   self.tokens[self.current_line][self.current_index][0] in ['single_comment', 'multi_comment']):
                self.current_index += 1

            # If we've reached a non-comment token, break
            if (self.current_index < len(self.tokens[self.current_line]) and 
                self.tokens[self.current_line][self.current_index][0] not in ['single_comment', 'multi_comment']):
                break

            # If this line is all comments, move to next line
            self.current_line += 1
            self.current_index = 0

    def current_token(self):
        """Get the current token without advancing, skipping comments."""
        self._skip_comments()

        # Check if we've reached the end of tokens
        if self.current_line >= len(self.tokens):
            return None

        # Update current position and return current token
        self.current_position = (self.current_line, self.current_index)
        return self.tokens[self.current_line][self.current_index]

    def peek_next_token(self):
        """Look ahead to the next token without advancing, skipping comments."""
        # Save current position
        saved_line = self.current_line
        saved_index = self.current_index
        
        # Move past current position and skip comments
        self.advance()
        self._skip_comments()
        
        # Get the next token
        next_token = self.current_token()
        
        # Restore original position
        self.current_line = saved_line
        self.current_index = saved_index
        
        return next_token

    def advance(self):
        """Move to the next token, skipping comments."""
        # If we've gone past the token list, do nothing
        if self.current_line >= len(self.tokens):
            return
        
        # Move to next token
        self.current_index += 1
        
        # If we've reached the end of the current line, move to next line
        if self.current_index >= len(self.tokens[self.current_line]):
            self.current_line += 1
            self.current_index = 0
        
        # Skip any comments
        self._skip_comments()

    def match(self, expected):
        """
        Check if the current token matches the expected type, advance if it does,
        raise an error if it doesn't.
        """
        token = self.current_token()
        if token is None:
            raise SyntaxError(f"Unexpected end of input when parsing. Expected {expected}")
        
        if token[0] == expected:
            self.advance()
            return True
        
        raise SyntaxError(f"Expected {expected}, got {token} at line {self.current_position[0]+1}, position {self.current_position[1]+1}")

    def try_match(self, expected):
        """
        Try to match the expected token type, return True and advance if matched,
        return False without advancing if not matched.
        """
        token = self.current_token()
        if token and token[0] == expected:
            self.advance()
            return True
        return False

    def current_token_position(self):
        """Returns a string representation of the current token position for error messages."""
        return f"line {self.current_position[0]+1}, position {self.current_position[1]+1}"

    def get_token_position(self):
        """Returns current token's line and position as a tuple"""
        return (self.current_position[0], self.current_position[1])

    def build_ast(self):
        """Entry point for AST building."""
        try:
            return self.build_program()
        except SyntaxError as e:
            # Enhance the error message with position information
            raise SyntaxError(f"{str(e)} at {self.current_token_position()}")
        except Exception as e:
            # Catch other exceptions and provide context
            raise Exception(f"Error building AST: {str(e)} at {self.current_token_position()}")

    def build_program(self):
        """Build the root program node."""
        line, pos = self.get_token_position()
        self.match('crown')
        self.match('~')

        global_declarations = self.build_global_declarations()
        functions = self.build_global_functions()
        main_function = self.build_main_function()

        self.match('reign')
        self.match('~')

        return ProgramNode(global_declarations, functions, main_function, line, pos)

    def build_declaration(self, scope_level):
        line, pos = self.get_token_position()
        is_dynasty = False
        self.is_array = False
        self.is_2d = False
        token = self.current_token()
        array_dimensions = []
        declarations = []

        # Check for optional 'dynasty' token
        if token and token[0] == 'dynasty':
            is_dynasty = True
            self.advance()
            token = self.current_token()

        # Expect a data type next
        datatype = token
        self.advance()
        token = self.current_token()

        # Expect an identifier for the first variable
        identifier = token
        self.advance()
        token = self.current_token()

        value = None

        # Array handling if needed
        if token and token[0] == '[':
            self.is_array = True
            self.match('[')
            token = self.current_token()
            array_dimensions.append(token)
            self.advance()
            self.match(']')
            token = self.current_token()

            if token and token[0] == '[':
                self.is_2d = True
                self.match('[')
                token = self.current_token()
                array_dimensions.append(token)
                self.advance()
                self.match(']')
                token = self.current_token()

        # With initialization: stop at a comma or tilde.
        if token and token[0] == '=':
            print("ENTEREES")
            self.match('=')
            # Only capture tokens up to a comma or '~' so that subsequent variables aren't included.
            if self.is_array:
                print('is arrsyyy')
                value = self.build_array()
            else:
                print('not arrsyyy')
                value = self.build_val()
            token = self.current_token()
            
        # Create the first declaration node
        decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions, line, pos)
        declarations.append(decl)

        # Process multiple declarations (after the first variable)
        while True:
            self.is_array = False
            self.is_2d = False
            token = self.current_token()
            if not token or token[0] != ',':
                break
                    
            self.match(',')
                
            # Get the next identifier
            line, pos = self.get_token_position()  # Get position for this declaration
            token = self.current_token()
            if not token:
                break
                    
            identifier = token
            self.advance()
            value = None
            array_dimensions = []
            token = self.current_token()
                
            # Array handling (if declared for the subsequent variable)
            if token and token[0] == '[':
                self.is_array = True
                self.match('[')
                token = self.current_token()
                array_dimensions.append(token)
                self.advance()
                self.match(']')
                token = self.current_token()

                if token and token[0] == '[':
                    self.is_2d = True
                    self.match('[')
                    token = self.current_token()
                    array_dimensions.append(token)
                    self.advance()
                    self.match(']')
                    token = self.current_token()
                
            # with initialization for the variable: stop at comma or tilde
            if token and token[0] == '=':
                print("ENTEREES")
                self.match('=')
                if self.is_array:
                    print('is arrsyyy')
                    value = self.build_array()
                else:
                    print('not arrsyyy')
                    value = self.build_val()
                token = self.current_token()
                
            # Create a new declaration for this variable and add to declarations list
            decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions, line, pos)
            declarations.append(decl)

        # End of declaration, match the tilde
        token = self.current_token()
        if token and token[0] == '~':
            self.match('~')

        return declarations


    def build_global_declarations(self):
        print('entered global +++++++++++++++', self.current_token())
        declarations = []
        
        while True:
            token = self.current_token()
            
            # End parsing if we encounter function or main program
            if token is None or token[0] in ['spell', 'castle']:
                break
                
            declarations.extend(self.build_declaration(scope_level=GLOBAL_SCOPE))
            
        return declarations

    def build_global_functions(self):
        """Build all global functions."""
        functions = []

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input when parsing global functions.")

            if token[0] == 'castle':
                break  # end of global functions parsing

            if token[0] == 'spell':
                functions.append(self.build_function(is_global=True, scope_level=GLOBAL_SCOPE))
            else:
                raise SyntaxError(f"Unexpected token '{token[0]}', expected 'spell' or 'castle'.")

        return functions

    def build_function(self, is_global, scope_level):
        """Build a function definition node."""
        line, pos = self.get_token_position()
        self.match('spell')

        # Parse return type
        return_type_token = self.current_token()
        if return_type_token is None:
            raise SyntaxError("Expected return type for function")
        return_type = return_type_token
        self.advance()

        # Parse function identifier
        token = self.current_token()
        if token is None or token[0] != 'identifier':
            raise SyntaxError(f"Expected function name identifier, got {token}")
        identifier = token
        self.advance()

        # Parse parameters
        self.match('(')
        params = self.build_parameters()
        self.match(')')

        # Parse function body
        self.match('{')
        body = self.build_body()

        # Parse optional return value
        return_val = None
        if self.current_token() and self.current_token()[0] == 'return':
            self.match('return')
            return_expr_token = self.current_token()
            if return_expr_token is None:
                raise SyntaxError("Expected expression after 'return'")
            return_val = self.build_rval()
            self.match('~')

        self.match('}')

        return FunctionNode(return_type, identifier, params, body, return_val, is_global, scope_level, line, pos)

    def build_main_function(self):
        """Build the main function node."""
        line, pos = self.get_token_position()
        self.match('castle')
        self.match('treasures')
        
        identifier = None
        if self.current_token() and self.current_token()[0] == 'identifier':
            identifier = self.current_token()
            self.advance()
        else:
            raise SyntaxError("Expected identifier for main function")
            
        self.match('(')
        self.match(')')
        self.match('{')
        
        body = self.build_body()
        
        self.match('return')
        
        return_value = None
        if self.current_token():
            if self.current_token()[1] == '0':
                return_value = self.current_token()
                self.advance()
            else:
                raise SyntaxError("Main function must return 0")
        else:
            raise SyntaxError("Expected return value for main function")
            
        self.match('~')
        self.match('}')
        
        return MainFunctionNode(identifier, body, return_value, line, pos)

    def build_body(self):
        """Build the body of a function or control structure."""
        body_nodes = []

        while True:
            token = self.current_token()

            if token is None or token[0] in ['return', '}']:
                break

            if token[0] in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
                declarations = self.build_declaration(scope_level=LOCAL_SCOPE)
                body_nodes.extend(declarations)

            elif token[0] == 'spell':
                function = self.build_function(is_global=False, scope_level=LOCAL_SCOPE)
                body_nodes.append(function)

            elif token[0] == 'granted':
                line, pos = self.get_token_position()
                self.match('granted')
                self.match('(')
                output = self.build_output()
                self.match(')')
                self.match('~')
                body_nodes.append(OutputNode(output, line, pos))

            elif token[0] == 'identifier':
                line, pos = self.get_token_position()
                next_token = self.peek_next_token()

                if next_token and next_token[0] in ['=', '+=', '-=', '*=', '/=', '%=']:  
                    # Variable reassignment case: x = 5~, x += 2~, etc.
                    var_reassign = self.build_var_reassign(line, pos)
                    body_nodes.append(var_reassign)

                elif next_token and next_token[0] == '(':
                    # Function call case: funcName(args)~
                    function_call = self.build_function_call(line, pos)
                    body_nodes.append(function_call)

                elif next_token and next_token[0] == '[':
                    # Array access case: arr[2] = 10~
                    array_assignment = self.build_array_assignment(line, pos)
                    body_nodes.append(array_assignment)
                
                elif next_token and next_token[0] in ['++', '--']:
                    # Unary operation: i++~, count--~
                    unary = self.build_unary_operation(line, pos)
                    body_nodes.append(unary)

                else:
                    raise SyntaxError(f"Unexpected identifier usage: '{token[1]}' at {self.current_token_position()}")

            elif token[0] == 'believe':
                line, pos = self.get_token_position()
                do_while = self.build_do_while(line, pos)
                body_nodes.append(do_while)

            elif token[0] == 'forever':
                line, pos = self.get_token_position()
                while_stmt = self.build_while(line, pos)
                body_nodes.append(while_stmt)

            elif token[0] == 'cast':
                line, pos = self.get_token_position()
                if_stmt = self.build_if(line, pos)
                body_nodes.append(if_stmt)

            elif token[0] == 'tale':
                line, pos = self.get_token_position()
                for_loop = self.build_for_loop(line, pos)
                body_nodes.append(for_loop)

            elif token[0] == 'break':
                line, pos = self.get_token_position()
                break_node = self.build_break(line, pos)
                body_nodes.append(break_node)

            elif token[0] == 'continue':
                line, pos = self.get_token_position()
                continue_node = self.build_continue(line, pos)
                body_nodes.append(continue_node)

            else:
                raise SyntaxError(f"Unexpected token '{token[0]}' in body")

        return body_nodes

    def build_output(self):
        """Build an output statement."""
        output = []
        paren = 0

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input while parsing output statement")
            
            if token[0] == ')' and paren == 0:
                break
            
            if token[0] == '(':
                paren = 1
            
            if token[0] == ')' and paren == 1:
                paren = 0


            output.append(token)
            self.advance()

        return output


    def build_var_reassign(self, line=None, pos=None):
        """Build a variable reassignment node."""
        # Capture the variable being reassigned
        token = self.current_token()
        identifier = token
        self.match('identifier')  # Consume the variable name

        # Capture the assignment operator
        operator_token = self.current_token()
        if operator_token[0] not in ['=', '+=', '-=', '*=', '/=', '%=']:
            raise SyntaxError(f"Invalid assignment operator '{operator_token[0]}' for variable reassignment")
        operator = operator_token
        self.advance()  # Consume the assignment operator

        # Capture the expression being assigned
        expression = self.build_val()

        # Ensure '~' at the end
        self.match('~')

        return VariableReassignmentNode(identifier, operator, expression, line, pos)

    def build_expression(self):  # for condition, parameters, arguments
        """Build an expression node."""
        token = self.current_token()  # Get the current token
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")

        expression = []
        # Loop until we hit a terminator ('~', ',', ')', '}', or ']')
        while token is not None and token[0] not in [')', ']', ',', '}']:
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
        
        return expression
    
    def build_val(self):
        """Build an expression node."""
        token = self.current_token()  # Get the current token
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")
            
        expression = []
        
        # Track parentheses level to handle commas inside parentheses
        paren_level = 0
        
        # Loop until we hit a terminator ('~', ',', or ')') at the top level
        while token is not None:
            if token[0] == '(':
                paren_level += 1
            elif token[0] == ')':
                paren_level -= 1
                # If we've closed all parentheses and the next token is a terminator, add the token and break
                if paren_level == 0 and self.peek_next_token() and self.peek_next_token()[0] in ['~', ',']:
                    expression.append(token)
                    self.advance()
                    break
            
            # Only treat ',' and '~' as terminators when at the top level (paren_level == 0)
            if paren_level == 0 and token[0] in ['~', ',']:
                break
                
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
                
        print(expression)
        return expression
    
    def build_array(self):
        """Build an array expression node that captures the entire array literal."""
        # Store starting position
        start_token = self.current_token()
        
        # Create a list to store the entire array expression
        array_tokens = [start_token]  # Start with opening brace
        self.match('{')
        
        # Track the brace nesting level to handle nested arrays
        brace_level = 1
        
        # Continue until we find the matching closing brace
        while brace_level > 0:
            token = self.current_token()
            
            if token is None:
                raise SyntaxError("Unexpected end of input while parsing array, unclosed '{'")
            
            array_tokens.append(token)
            
            if token[0] == '{':
                brace_level += 1
            elif token[0] == '}':
                brace_level -= 1
            
            self.advance()
        
        print(array_tokens, "")

        # The last token added was the closing brace, which we've already consumed with advance()
        # So we're done - just return the collected tokens
        return array_tokens
    
        
    def build_rval(self):
        """Build an expression node."""
        token = self.current_token()  # Get the current token
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")
    
        expression = []
        # Loop until we hit a terminator ('~', ',', or ')')
        while token is not None and token[0] not in ['~']:
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
        
        print(expression)
        return expression
    
    def build_function_call(self, line=None, pos=None):
        """Build a function call node."""
        function_name_token = self.current_token()  # Store function identifier
        function_name = function_name_token[1]
        self.match('identifier')  # Consume function name
        self.match('(')  # Consume '('

        arguments = []
        
        # Check for empty argument list
        if self.current_token() and self.current_token()[0] == ')':
            self.match(')')
        else:
            # Parse arguments
            while True:
                current_arg = self.build_expression()
                arguments.append(current_arg)
                
                # Check for more arguments or end of arguments
                if self.current_token() and self.current_token()[0] == ',':
                    self.match(',')
                elif self.current_token() and self.current_token()[0] == ')':
                    self.match(')')
                    break
                else:
                    raise SyntaxError("Expected ',' or ')' in function call arguments")

        # Ensure '~' at the end
        self.match('~')

        return FunctionCallNode(function_name, arguments, line, pos)
    
    def build_array_assignment(self, line=None, pos=None):
        """Build an array assignment node."""
        # Get array identifier
        token = self.current_token()
        identifier = token
        self.match('identifier')
        
        # Parse indices (can be multiple for multi-dimensional arrays)
        indices = []
        while self.current_token() and self.current_token()[0] == '[':
            self.match('[')
            index_expr = self.build_expression()
            indices.append(index_expr)
            self.match(']')
            
        # Get assignment operator
        operator_token = self.current_token()
        if operator_token[0] not in ['=', '+=', '-=', '*=', '/=']:
            raise SyntaxError(f"Invalid assignment operator '{operator_token[0]}' for array assignment")
        operator = operator_token[0]
        self.advance()
        
        # Get the expression being assigned
        expression = self.build_val()
        
        # Ensure '~' at the end
        self.match('~')
        
        return ArrayAssignmentNode(identifier, indices, operator, expression, line, pos)

    def build_unary_operation(self, line=None, pos=None):
        """Build a unary operation node (++ or --)."""
        identifier_token = self.current_token()
        identifier = identifier_token[1]
        self.match('identifier')
        
        operator_token = self.current_token()
        if operator_token[0] not in ['++', '--']:
            raise SyntaxError(f"Expected '++' or '--', got {operator_token[0]}")
        operator = operator_token[0]
        self.advance()
        
        # Ensure '~' at the end
        self.match('~')
        
        return UnaryOperationNode(identifier, operator, line, pos)

    def build_parameters(self):
        """Build function parameters."""
        parameters = []
        
        # Handle empty parameter list
        if self.current_token() and self.current_token()[0] == ')':
            return parameters
            
        # Parse parameters separated by commas
        while True:
            # Parse data type
            datatype_token = self.current_token()
            if datatype_token is None:
                raise SyntaxError("Unexpected end of input in parameter list")
            datatype = datatype_token
            self.advance()
            
            # Parse parameter name
            identifier_token = self.current_token()
            if identifier_token is None or identifier_token[0] != 'identifier':
                raise SyntaxError(f"Expected parameter name, got {identifier_token}")
            identifier = identifier_token
            self.advance()
            
            # Create parameter and add to list
            parameters.append((datatype, identifier))
            
            # Check for more parameters
            if self.current_token() and self.current_token()[0] == ',':
                self.match(',')
            else:
                break
                
        return parameters

    def build_do_while(self, line=None, pos=None):
        """Build a do-while loop node."""
        self.match('believe')
        self.match('{')
        
        # Parse loop body
        loop_body = self.build_body()
        
        self.match('}')
        self.match('forever')
        self.match('(')
        
        # Parse condition
        condition = self.build_condition()
        
        self.match(')')
        self.match('~')
        
        return DoWhileNode(loop_body, condition, line, pos)

    def build_while(self, line=None, pos=None):
        """Build a while loop node."""
        self.match('forever')
        self.match('(')
        
        # Parse condition
        condition = self.build_condition()
        
        self.match(')')
        self.match('{')
        
        # Parse loop body
        loop_body = self.build_body()
        
        self.match('}')
        
        return WhileNode(loop_body, condition, line, pos)

    def build_if(self, line=None, pos=None):
        """Build an if statement node with optional elif and else branches."""
        self.match('cast')
        self.match('(')
        
        # Parse condition
        condition = self.build_condition()
        
        self.match(')')
        self.match('{')
        
        # Parse if body
        body = self.build_body()
        
        self.match('}')

        # Collect optional 'twist' (elif) statements
        elif_nodes = []
        while self.current_token() and self.current_token()[0] == 'twist':
            elif_line, elif_pos = self.get_token_position()
            self.match('twist')
            self.match('(')
            twist_condition = self.build_condition()
            self.match(')')
            self.match('{')
            twist_body = self.build_body()
            self.match('}')
            elif_nodes.append(ElifNode(twist_condition, twist_body, elif_line, elif_pos))

        # Optional 'curse' (else) statement
        else_node = None
        if self.current_token() and self.current_token()[0] == 'curse':
            else_line, else_pos = self.get_token_position()
            self.match('curse')
            self.match('{')
            else_body = self.build_body()
            self.match('}')
            else_node = ElseNode(else_body, else_line, else_pos)
        
        return IfNode(condition, body, elif_nodes, else_node, line, pos)

    def build_for_loop(self, line=None, pos=None):
        """Build a for loop node."""
        self.match('tale')
        self.match('(')

        # Parse initialization
        loop_var = self.build_loop_var()
        self.match('~')

        # Parse condition
        loop_exp = self.build_loop_exp()
        self.match('~')

        # Parse update expression
        loop_unary = self.build_loop_unary()
        self.match(')')

        # Parse loop body
        self.match('{')
        loop_body = self.build_body()
        self.match('}')

        return ForLoopNode(loop_var, loop_exp, loop_unary, loop_body, line, pos)

    def build_loop_var(self):
        """Build the initialization part of a for loop."""
        loop_var = []
        
        while self.current_token() and self.current_token()[0] != '~':
            loop_var.append(self.current_token())
            self.advance()
        
        return loop_var
    
    def build_loop_exp(self):
        """Build the condition part of a for loop."""
        loop_exp = []
        
        while self.current_token() and self.current_token()[0] != '~':
            loop_exp.append(self.current_token())
            self.advance()
        
        return loop_exp
    
    def build_loop_unary(self):
        """Build the update part of a for loop."""
        loop_unary = []
        
        while self.current_token() and self.current_token()[0] not in [')', '~']:
            loop_unary.append(self.current_token())
            self.advance()
        
        return loop_unary

    def build_break(self, line=None, pos=None):
        """Build a break statement node."""
        self.match('break')
        self.match('~')
        return BreakNode(line, pos)

    def build_continue(self, line=None, pos=None):
        """Build a continue statement node."""
        self.match('continue')
        self.match('~')
        return ContinueNode(line, pos)
        
    def build_condition(self):
        """Build a condition expression for control structures."""
        condition = []
        nest = 0
        while self.current_token():
            token = self.current_token()
            if token[0] == '(':
                nest += 1
            elif token[0] == ')':
                if nest == 0:
                    # This ')' is the matching one for the caller's '('; stop here.
                    break
                else:
                    nest -= 1
            condition.append(token)
            self.advance()
        return condition