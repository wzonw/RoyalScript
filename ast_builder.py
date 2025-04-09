# Define your AST Nodes clearly first

GLOBAL_SCOPE = 0
LOCAL_SCOPE = 1

class Node:
    """Base class for all AST nodes"""
    pass


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
    def __init__(self, globals, functions, main_function):
        self.global_declarations = globals
        self.functions = functions
        self.main_function = main_function

class VariableDeclarationNode(Node):
    def __init__(self, datatype, identifier, value=None, is_dynasty=False, scope_level=GLOBAL_SCOPE, array_dimensions=None):
        self.datatype = datatype
        self.identifier = identifier
        self.value = value
        self.is_dynasty = is_dynasty
        self.scope_level = scope_level
        self.array_dimensions = array_dimensions if array_dimensions is not None else []

class VariableReassignmentNode(Node):
    def __init__(self, identifier, operator, expression):
        self.identifier = identifier  # Variable name
        self.operator = operator  # Assignment operator (=, +=, -=, etc.)
        self.expression = expression  # Expression being assigned

class FunctionNode(Node):
    def __init__(self, return_type, identifier, parameters, body, return_val=None, is_global=True, scope_level=GLOBAL_SCOPE):
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.body = body
        self.return_val = return_val
        self.is_global = is_global
        self.scope_level = scope_level

class FunctionCallNode(Node):
    def __init__(self, name, arguments):
        self.name = name  # Function name
        self.arguments = arguments  # List of argument expressions

class DoWhileNode(Node):
    def __init__(self, loop_body, condition):
        self.loop_body = loop_body
        self.condition = condition

class WhileNode(Node):
    def __init__(self, loop_body, condition):
        self.loop_body = loop_body
        self.condition = condition

class IfNode(Node):
    def __init__(self, condition, body, elif_nodes=None, else_node=None):
        self.condition = condition
        self.body = body
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.else_node = else_node

class ElifNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ElseNode(Node):
    def __init__(self, body):
        self.body = body
    
class IfBreakNode(Node):
    def __init__(self, condition, body, elif_nodes=None, else_node=None):
        self.condition = condition
        self.body = body
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.else_node = else_node

class ElifBreakNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ElseBreakNode(Node):
    def __init__(self, body):
        self.body = body

class BreakNode(Node):
    def __init__(self):
        self.type = 'break'

class ContinueNode(Node):
    def __init__(self):
        self.type = 'continue'

class ForLoopNode(Node):
    def __init__(self, loop_var, loop_exp, loop_unary, loop_body):
        self.loop_var = loop_var          # initialization
        self.loop_exp = loop_exp          # condition
        self.loop_unary = loop_unary      # update (unary operation)
        self.loop_body = loop_body        # body of the loop

class LiteralNode(Node):
    def __init__(self, value, datatype):
        self.value = value
        self.datatype = datatype

class MainFunctionNode(Node):
    def __init__(self, identifier, body, return_val):
        self.identifier = identifier
        self.body = body
        self.return_val = return_val

class ArrayAssignmentNode(Node):
    def __init__(self, identifier, indices, operator, expression):
        self.identifier = identifier      # Array name
        self.indices = indices            # List of index expressions
        self.operator = operator          # Assignment operator
        self.expression = expression      # Expression being assigned

class UnaryOperationNode(Node):
    def __init__(self, identifier, operator):
        self.identifier = identifier  # Variable name
        self.operator = operator      # ++ or --

class OutputNode(Node):
    def __init__(self, expressions):
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
        self.match('crown')
        self.match('~')

        global_declarations = self.build_global_declarations()
        functions = self.build_global_functions()
        main_function = self.build_main_function()

        self.match('reign')
        self.match('~')

        return ProgramNode(global_declarations, functions, main_function)

    def build_declaration(self, scope_level):
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
            self.match('=')
            # Only capture tokens up to a comma or '~' so that subsequent variables aren’t included.
            value = self.build_val()
            token = self.current_token()
            
        # Create the first declaration node
        decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)
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
                self.match('=')
                value = self.build_val()
                token = self.current_token()
                
            # Create a new declaration for this variable and add to declarations list
            decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)
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
            return_val = self.build_val()
            self.match('~')

        self.match('}')

        return FunctionNode(return_type, identifier, params, body, return_val, is_global, scope_level)

    def build_main_function(self):
        """Build the main function node."""
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
        
        return MainFunctionNode(identifier, body, return_value)

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
                self.match('granted')
                self.match('(')
                output = self.build_output()
                self.match(')')
                self.match('~')
                body_nodes.append(OutputNode(output))

            elif token[0] == 'identifier':
                next_token = self.peek_next_token()

                if next_token and next_token[0] in ['=', '+=', '-=', '*=', '/=', '%=']:  
                    # Variable reassignment case: x = 5~, x += 2~, etc.
                    var_reassign = self.build_var_reassign()
                    body_nodes.append(var_reassign)

                elif next_token and next_token[0] == '(':
                    # Function call case: funcName(args)~
                    function_call = self.build_function_call()
                    body_nodes.append(function_call)

                elif next_token and next_token[0] == '[':
                    # Array access case: arr[2] = 10~
                    array_assignment = self.build_array_assignment()
                    body_nodes.append(array_assignment)
                
                elif next_token and next_token[0] in ['++', '--']:
                    # Unary operation: i++~, count--~
                    unary = self.build_unary_operation()
                    body_nodes.append(unary)

                else:
                    raise SyntaxError(f"Unexpected identifier usage: '{token[1]}' at {self.current_token_position()}")

            elif token[0] == 'believe':
                do_while = self.build_do_while()
                body_nodes.append(do_while)

            elif token[0] == 'forever':
                while_stmt = self.build_while()
                body_nodes.append(while_stmt)

            elif token[0] == 'cast':
                if_stmt = self.build_if()
                body_nodes.append(if_stmt)

            elif token[0] == 'tale':
                for_loop = self.build_for_loop()
                body_nodes.append(for_loop)

            elif token[0] == 'break':
                break_node = self.build_break()
                body_nodes.append(break_node)

            elif token[0] == 'continue':
                continue_node = self.build_continue()
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


    def build_var_reassign(self):
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

        return VariableReassignmentNode(identifier, operator, expression)

    def build_expression(self):  # for condition, parameters, arguments
        """Build an expression node."""
        token = self.current_token()  # Get the current token
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")

        expression = []
        # Loop until we hit a terminator ('~', ',', or ')')
        while token is not None and token[0] not in [')', ']']:
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
        # Loop until we hit a terminator ('~', ',', or ')')
        while token is not None and token[0] not in ['~', ',']:
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
        
        print(expression)
        return expression
    
    # def build_array(self, is_2d):
    #     """Build an array expression node for both 1D and 2D arrays."""
    #     token = self.current_token()
    #     if token is None:
    #         raise SyntaxError("Unexpected end of input while parsing array")
        
    #     # Expect opening brace
    #     if token[0] != '{':
    #         raise SyntaxError(f"Expected '{{' at start of array, found {token}")
        
    #     self.advance()  # Move past the opening brace
    #     token = self.current_token()
        
    #     array_values = []
        
    #     if is_2d:
    #         # Handle 2D array: array of arrays
    #         while token is not None and token[0] != '}':
    #             # Skip commas between inner arrays
    #             if token[0] == ',':
    #                 self.advance()
    #                 token = self.current_token()
    #                 continue
                    
    #             # Each inner array should start with '{'
    #             if token[0] != '{':
    #                 raise SyntaxError(f"Expected '{{' for inner array, found {token}")
                    
    #             self.advance()  # Move past the inner opening brace
                
    #             # Parse inner array elements
    #             inner_array = []
    #             token = self.current_token()
                
    #             while token is not None and token[0] != '}':
    #                 # Skip commas between elements
    #                 if token[0] == ',':
    #                     self.advance()
    #                     token = self.current_token()
    #                     continue
                        
    #                 # Add the element to the inner array
    #                 inner_array.append(token)
    #                 self.advance()
    #                 token = self.current_token()
                
    #             # Make sure we found the closing brace for inner array
    #             if token is None or token[0] != '}':
    #                 raise SyntaxError("Unexpected end of input while parsing inner array")
                    
    #             # Add completed inner array to our 2D array
    #             array_values.append(inner_array)
    #             self.advance()  # Move past inner closing brace
    #             token = self.current_token()
    #     else:
    #         # Handle 1D array: simpler case
    #         while token is not None and token[0] != '}':
    #             # Skip commas between elements
    #             if token[0] == ',':
    #                 self.advance()
    #                 token = self.current_token()
    #                 continue
                    
    #             # Add the element
    #             array_values.append(token)
    #             self.advance()
    #             token = self.current_token()
        
    #     # Make sure we found the closing brace
    #     if token is None or token[0] != '}':
    #         raise SyntaxError("Unexpected end of input while parsing array")
            
    #     self.advance()  # Move past the closing brace
    #     return array_values

    def build_function_call(self):
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

        return FunctionCallNode(function_name, arguments)
    
    def build_array_assignment(self):
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
        
        return ArrayAssignmentNode(identifier, indices, operator, expression)

    def build_unary_operation(self):
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
        
        return UnaryOperationNode(identifier, operator)
    
    def build_do_while(self):
        """Build a do-while loop node."""
        self.match('believe')
        self.match('{')

        loop_body = self.build_body()

        self.match('}')
        self.match('forever')
        self.match('(')

        condition = self.build_condition()

        self.match(')')
        self.match('~')

        return DoWhileNode(loop_body, condition)

    def build_while(self):
        """Build a while loop node."""
        self.match('forever')
        self.match('(')

        condition = self.build_condition()

        self.match(')')
        self.match('{')

        loop_body = self.build_body()

        self.match('}')

        return WhileNode(loop_body, condition)
    
    def build_if(self):
        """Build an if statement node with optional elif and else branches."""
        self.match('cast')
        self.match('(')
        condition = self.build_condition()
        self.match(')')
        self.match('{')
        body = self.build_body()
        self.match('}')

        # Collect optional 'twist' (elif) statements
        elif_nodes = []
        while self.current_token() and self.current_token()[0] == 'twist':
            self.match('twist')
            self.match('(')
            twist_condition = self.build_condition()
            self.match(')')
            self.match('{')
            twist_body = self.build_body()
            self.match('}')
            elif_nodes.append(ElifNode(twist_condition, twist_body))

        # Optional 'curse' (else) statement
        else_node = None
        if self.current_token() and self.current_token()[0] == 'curse':
            self.match('curse')
            self.match('{')
            else_body = self.build_body()
            self.match('}')
            else_node = ElseNode(else_body)

        return IfNode(condition, body, elif_nodes, else_node)

    def build_for_loop(self):
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

        return ForLoopNode(loop_var, loop_exp, loop_unary, loop_body)

    def build_loop_var(self):
        """Build the initialization part of a for loop."""
        loop_var = []
        
        while self.current_token() and self.current_token()[0] != '~':
            if self.current_token()[0] == 'treasures':
                self.advance()
            else:
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

    def build_break(self):
        """Build a break statement node."""
        self.match('break')
        self.match('~')
        return BreakNode()
    
    def build_continue(self):
        """Build a continue statement node."""
        self.match('continue')
        self.match('~')
        return ContinueNode()

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
    
    def build_condition(self):
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
