# Define your AST Nodes clearly first

GLOBAL_SCOPE = 0
LOCAL_SCOPE = 1

class Node:
    pass

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


class RoyalScriptASTBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_line = 0
        self.current_index = 0

    def current_token(self):
        while self.current_line < len(self.tokens):
            if self.tokens[self.current_line]:
                if self.current_index < len(self.tokens[self.current_line]):
                    return self.tokens[self.current_line][self.current_index]
            self.current_line += 1
            self.current_index = 0
        return None

    def advance(self):
        # If we've already gone past the token list, do nothing.
        if self.current_line >= len(self.tokens):
            return
        if self.current_index + 1 < len(self.tokens[self.current_line]):
            self.current_index += 1
        else:
            self.current_line += 1
            self.current_index = 0


    def match(self, expected):
        token = self.current_token()
        if token and token[0] == expected:
            self.advance()
            return True
        raise SyntaxError(f"Expected {expected}, got {token}")

    def build_ast(self):
        return self.build_program()

    def build_program(self):
        self.match('crown')
        self.match('~')

        global_declarations = self.build_global_declarations()
        functions = self.build_function()
        main_function = self.build_main_function()

        self.match('reign')
        self.match('~')

        return ProgramNode(global_declarations, functions, main_function)

    def build_declaration(self, scope_level):
        is_dynasty = False
        token = self.current_token()

        # Check for optional 'dynasty' token
        if token and token[0] == 'dynasty':
            is_dynasty = True
            self.advance()
            token = self.current_token()

        # Expect a data type next
        if token is None:
            raise SyntaxError("Unexpected end of input, expected data type")
        datatype = token[1]  # use the literal value for the type
        self.advance()

        # Expect an identifier
        identifier_token = self.current_token()
        if identifier_token is None or identifier_token[0] != 'identifier':
            raise SyntaxError("Expected variable name")
        identifier = identifier_token[1]  # extract the identifier's name
        self.advance()

        # Check for array declaration (only 1D and 2D allowed)
        array_dimensions = []
        token = self.current_token()
        if token and token[0] == '[':
            self.match('[')
            # Parse first dimension expression
            dim_expr = self.current_token()
            if dim_expr is None:
                raise SyntaxError("Expected expression for array dimension")
            array_dimensions.append(dim_expr[1])
            self.advance()
            self.match(']')

            # Optionally check for a second dimension
            token = self.current_token()
            if token and token[0] == '[':
                self.match('[')
                dim_expr = self.current_token()
                if dim_expr is None:
                    raise SyntaxError("Expected expression for second array dimension")
                array_dimensions.append(dim_expr[1])
                self.advance()
                self.match(']')
            
            # Disallow more than 2 dimensions
            token = self.current_token()
            if token and token[0] == '[':
                raise SyntaxError("Only 1D and 2D arrays are allowed")

        # Check for initialization for the first variable
        value = None
        token = self.current_token()
        declarations = None
        if token and token[0] == '=':
            self.match('=')
            value_node = self.build_expression()
            if value_node is None:
                raise SyntaxError("Expected value after '='")
            value = value_node
            declarations = [VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)]
        elif token and token[0] == ',':
            # Create declaration without initialization, then parse additional declarations
            declarations = [VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)]
            declarations.extend(self.build_vardec_more(datatype, is_dynasty, scope_level))
        elif token and token[0] == '~':
            declarations = [VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)]
        else:
            raise SyntaxError(f"Unexpected token {token} in declaration")
        
        # Consume the '~' at the end of the declaration
        self.advance()
        
        return declarations


    def build_vardec_more(self, datatype, is_dynasty, scope_level):
        """
        Handles additional variable declarations separated by commas.
        Each additional variable may have its own optional initialization and array dimensions.
        """
        additional_declarations = []
        # Continue while the current token is a comma
        while self.current_token() and self.current_token()[0] == ',':
            self.match(',')  # Consume the comma

            # Expect an identifier after the comma
            identifier_token = self.current_token()
            if identifier_token is None or identifier_token[0] != 'identifier':
                raise SyntaxError("Expected variable name after ','")
            identifier = identifier_token[1]
            self.advance()

            # Check for array declaration (only 1D and 2D allowed)
            array_dimensions = []
            token = self.current_token()
            if token and token[0] == '[':
                self.match('[')
                # Parse first dimension expression
                dim_expr = self.current_token()
                if dim_expr is None:
                    raise SyntaxError("Expected expression for array dimension")
                array_dimensions.append(dim_expr[1])
                self.advance()
                self.match(']')
                
                # Optionally check for a second dimension
                token = self.current_token()
                if token and token[0] == '[':
                    self.match('[')
                    dim_expr = self.current_token()
                    if dim_expr is None:
                        raise SyntaxError("Expected expression for second array dimension")
                    array_dimensions.append(dim_expr[1])
                    self.advance()
                    self.match(']')
                
                # Disallow more than 2 dimensions
                token = self.current_token()
                if token and token[0] == '[':
                    raise SyntaxError("Only 1D and 2D arrays are allowed")
            
            # Check for initialization for this variable
            value = None
            token = self.current_token()
            if token and token[0] == '=':
                self.match('=')
                value = self.build_expression()
            
            # Create the declaration node and append it to the list
            decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)
            additional_declarations.append(decl)
        
        return additional_declarations



    def build_global_declarations(self):
        declarations = []

        while True:
            token = self.current_token()

            # End parsing if we encounter function or main program
            if token is None or token[0] in ['spell', 'castle']:
                break

            declarations.append(self.build_declaration(scope_level=GLOBAL_SCOPE))

        return declarations


    def build_global_functions(self):
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
        self.match('spell')

        # Parse return type
        return_type = self.current_token()
        self.advance()

        # Parse function identifier
        identifier_token = self.current_token()
        if identifier_token[0] != 'identifier':
            raise SyntaxError("Expected function name identifier.")
        identifier = identifier_token
        self.advance()

        # Parse parameters
        self.match('(')
        params = self.build_parameters()
        self.match(')')

        # Parse function body
        self.match('{')
        body = self.build_body()

        return_val = None
        if self.current_token()[0] == 'return':
            self.match('return')
            return_expr_token = self.current_token()
            return_val = LiteralNode(return_expr_token[1], return_expr_token[0])
            self.advance()
            self.match('~')

        self.match('}')

        return FunctionNode(return_type, identifier, params, body, return_val, is_global, scope_level)


    def build_main_function(self):
        self.match('castle')
        self.match('treasures')
        if self.current_token() and self.current_token()[0] == 'identifier':
            identifier = self.current_token()
            self.advance()
        self.match('(')
        self.match(')')
        self.match('{')
        body = self.build_body()
        self.match('return')
        if self.current_token() and self.current_token()[1] == '0':
            return_value= self.current_token()
            self.advance()
        self.match('~')
        self.match('}')
        return MainFunctionNode(identifier, body, return_value)

    def build_body(self):
        body_nodes = []

        while True:
            token = self.current_token()

            if token is None or token[0] in ['return', '}']:
                break

            if token[0] in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
                declaration = self.build_declaration(scope_level=LOCAL_SCOPE)
                body_nodes.append(declaration)

            elif token[0] == 'spell':
                function = self.build_function(is_global=False, scope_level=LOCAL_SCOPE)
                body_nodes.append(function)

            elif token[0] == 'granted':
                output = self.build_output()
                body_nodes.append(output)

            elif token[0] == 'identifier':
                next_token = self.peek_next_token()

                if next_token and next_token[0] in ['=', '+=', '-=', '*=', '/=']:  
                    # Variable reassignment case: x = 5~, x += 2~, etc.
                    var_reassign = self.build_var_reassign()
                    body_nodes.append(var_reassign)

                elif next_token and next_token[0] == '(':
                    # Function call case: funcName(args)~
                    function_call = self.build_function_call()
                    body_nodes.append(function_call)

                elif next_token and next_token[0] == '[':
                    # Array access case: arr[2] = 10~
                    array_access = self.build_array_assignment()
                    body_nodes.append(array_access)
                
                elif next_token and next_token[0] in ['++', '--']:
                    # Unary
                    unary = self.build_loop_unary()
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

            else:
                raise SyntaxError(f"Unexpected token '{token[0]}' in body")

        return body_nodes


    def build_output(self):
        output = []

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input while parsing output statement")

            if token[0] == '~':
                self.advance()  # consume the '~' token
                break

            output.append(token)
            self.advance()

        return output

    def build_var_reassign(self):
        # Capture the variable being reassigned
        identifier = self.current_token()
        self.match('identifier')  # Consume the variable name

        # Capture the assignment operator
        operator = self.current_token()
        if operator[1] not in ['=', '+=', '-=', '*=', '/=']:
            raise SyntaxError(f"Invalid assignment operator '{operator[1]}' for variable reassignment")
        self.match(operator)  # Consume the assignment operator

        # Capture the expression being assigned
        expression = self.build_expression()

        # Ensure '~' at the end
        if not self.match('~'):
            raise SyntaxError("Expected '~' at the end of variable reassignment")

        return VariableReassignmentNode(identifier, operator, expression)

    def build_expression(self):
        token = self.current_token()  # Get the current token
        expression = []
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")
        
        # Loop until we hit a terminator ('~' or ',')
        while token is not None and token[0] not in ['~', ',']:
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
        
        # Consume the terminator if present
        if token is not None:
            self.advance()
        
        return expression




    def build_function_call(self):
        function_name = self.current_token()  # Store function identifier
        self.match('identifier')  # Consume function name
        self.match('(')  # Consume '('

        arguments = []
        current_arg = []

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input while parsing function arguments")

            if token[0] == ')':  # End of function call
                if current_arg:
                    arguments.append(current_arg)  # Append last argument if exists
                self.advance()  # Consume ')'
                break

            elif token[0] == ',':  # Argument separator
                if not current_arg:
                    raise SyntaxError("Unexpected ',' without preceding argument")
                arguments.append(current_arg)
                current_arg = []
                self.advance()  # Consume ','

            else:
                current_arg.append(token)
                self.advance()

        if not self.match('~'):  # Ensure '~' at the end
            raise SyntaxError("Expected '~' at the end of function call")

        return FunctionCallNode(function_name, arguments)
    
    def build_array_assignment(self):
        token = self.current_token()
        array_assignment = []
        self.match('[')
        self.match('treasures_lit') or self.match('0') or self.match('1')
        self.match(']')
        if token in ['=', '+=', '-=', '*=', '/=']:
            self.advance()

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input while parsing output statement")

            if token[0] == '~':
                self.advance()  # consume the '~' token
                break

            array_assignment.append(token)
            self.advance()

        return array_assignment

    
    def build_do_while(self):
        self.match('believe')
        self.match('{')

        loop_body = self.build_loop_body()

        self.match('}')
        self.match('forever')
        self.match('(')

        condition = self.build_condition()

        self.match(')')
        self.match('~')

        return DoWhileNode(loop_body, condition)


    def build_while(self):
        self.match('forever')
        self.match('(')

        condition = self.build_condition()

        self.match(')')
        self.match('{')

        loop_body = self.build_loop_body()

        self.match('}')

        return WhileNode(loop_body, condition)
    
    def build_if(self):
        self.match('cast')
        self.match('(')
        condition = self.build_condition()
        self.match(')')
        self.match('{')
        body = self.build_body()
        self.match('}')

        # Collect optional 'twist' (elif) statements
        elif_nodes = []
        while True:
            token = self.current_token()
            if token and token[0] == 'twist':
                self.match('twist')
                self.match('(')
                twist_condition = self.build_condition()
                self.match(')')
                self.match('{')
                twist_body = self.build_body()
                elif_nodes.append(ElifNode(twist_condition, twist_body))
            else:
                break

        
        # Optional 'curse' (else) statement
        else_node = None
        token = self.current_token()
        if token and token[0] == 'curse':
            self.match('curse')
            self.match('{')
            else_body = self.build_body()
            self.match('}')
            else_node = ElseNode(else_body)

        return IfBreakNode(condition, body, elif_nodes, else_node)

    def build_if_break(self):
        self.match('cast')
        self.match('(')
        condition = self.build_condition()
        self.match(')')
        self.match('{')
        body = self.build_body()
        # Optional break/continue
        token = self.current_token()
        if token and token[0] == 'break':
            self.match('break')
            self.match('~')
            else_body.append(BreakNode())
        elif token and token[0] == 'continue':
            self.match('continue')
            self.match('~')
            else_body.append(ContinueNode())
        self.match('}')

        # Collect optional 'twist' (elif) statements
        elif_nodes = []
        while True:
            token = self.current_token()
            if token and token[0] == 'twist':
                self.match('twist')
                self.match('(')
                twist_condition = self.build_condition()
                self.match(')')
                self.match('{')
                twist_body = self.build_body()
                # Optional break/continue
                token = self.current_token()
                if token and token[0] == 'break':
                    self.match('break')
                    self.match('~')
                    else_body.append(BreakNode())
                elif token and token[0] == 'continue':
                    self.match('continue')
                    self.match('~')
                    else_body.append(ContinueNode())
                elif_nodes.append(ElifBreakNode(twist_condition, twist_body))
            else:
                break

        
        # Optional 'curse' (else) statement
        else_node = None
        token = self.current_token()
        if token and token[0] == 'curse':
            self.match('curse')
            self.match('{')
            else_body = self.build_body()
            # Optional break/continue
            token = self.current_token()
            if token and token[0] == 'break':
                self.match('break')
                self.match('~')
                else_body.append(BreakNode())
            elif token and token[0] == 'continue':
                self.match('continue')
                self.match('~')
                else_body.append(ContinueNode())
            self.match('}')
            else_node = ElseBreakNode(else_body)

        return IfNode(condition, body, elif_nodes, else_node)
    
    def build_for_loop(self):
        self.match('tale')
        self.match('(')

        loop_var = self.build_loop_var()
        self.match('~')

        loop_exp = self.build_loop_exp()
        self.match('~')

        loop_unary = self.build_loop_unary()
        self.match(')')

        self.match('{')
        loop_body = self.build_loop_body()
        self.match('}')

        return ForLoopNode(loop_var, loop_exp, loop_unary, loop_body)

    def build_loop_var(self):
        token = self.current_token()
        loop_var = []

        while token[0] != '~':
            loop_var.append(token)
        

        return loop_var
    
    def build_loop_exp(self):
        token = self.current_token()
        loop_exp = []

        while token[0] != '~':
            loop_exp.append(token)
        

        return loop_exp
    
    def build_loop_unary(self):
        token = self.current_token()
        loop_unary = []

        while token[0] not in [')', '~']:
            loop_unary.append(token)
        

        return loop_unary


    def build_parameters(self):
        parameters = []
        current_param = []

        while True:
            token = self.current_token()

            if token is None:
                raise SyntaxError("Unexpected end of input while parsing parameters")

            if token[0] == ')':
                if current_param:
                    parameters.append(current_param)
                break

            elif token[0] == ',':
                if not current_param:
                    raise SyntaxError("Unexpected ',' without preceding parameter")
                parameters.append(current_param)
                current_param = []
                self.advance()

            else:
                current_param.append(token)
                self.advance()

        return parameters
    
    def build_loop_body(self):
        loop_body_nodes = []

        while True:
            token = self.current_token()

            if token is None or token[0] in ['return', '}']:
                break

            if token[0] in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
                declaration = self.build_declaration(scope_level=LOCAL_SCOPE)
                loop_body_nodes.append(declaration)

            elif token[0] == 'spell':
                function = self.build_function(is_global=False, scope_level=LOCAL_SCOPE)
                loop_body_nodes.append(function)

            elif token[0] == 'granted':
                output = self.build_output()
                loop_body_nodes.append(output)

            elif token[0] == 'identifier':
                var_reassign = self.build_var_reassign()
                loop_body_nodes.append(var_reassign)

            elif token[0] == 'believe':
                do_while = self.build_do_while()
                loop_body_nodes.append(do_while)

            elif token[0] == 'forever':
                while_stmt = self.build_while()
                loop_body_nodes.append(while_stmt)

            elif token[0] == 'cast':
                if_stmt = self.build_if_break()
                loop_body_nodes.append(if_stmt)

            elif token[0] == 'tale':
                for_loop = self.build_for_loop()
                loop_body_nodes.append(for_loop)

            else:
                raise SyntaxError(f"Unexpected token '{token[0]}' in body")

        return loop_body_nodes


    def build_condition(self):
        conditions = []
        
        token = self.current_token()
        # Loop until we find the closing parenthesis or run out of tokens
        while token is not None and token[0] != ')':
            conditions.append(token)
            self.advance()  # Consume the current token and move to the next
            token = self.current_token()
        
        # Ensure that we found a closing ')'
        if token is None:
            raise SyntaxError("Expected ')' to close the condition")
        
        # Consume the closing ')'
        self.advance()
        
        return conditions
