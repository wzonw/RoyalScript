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
    
class ParameterNode(Node):
    def __init__(self, datatype, identifier):
        self.datatype = datatype
        self.identifier = identifier

class ReturnNode(Node):
    def __init__(self, expression):
        self.expression = expression

class ExpressionNode(Node):
    def __init__(self, tokens):
        self.tokens = tokens

class BinaryOperationNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOperationNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class LiteralNode(Node):
    def __init__(self, value, type):
        self.value = value
        self.type = type

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

class ArrayAccessNode(Node):
    def __init__(self, identifier, indices):
        self.identifier = identifier
        self.indices = indices

class FunctionCallNode(Node):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

class IfNode(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode(Node):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

class MainFunctionNode(Node):
    def __init__(self, body):
        self.body = body

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
        functions = self.build_global_functions()
        main_function = None #self.build_main_function()

        self.match('reign')
        self.match('~')

        return ProgramNode(global_declarations, functions, main_function)

    def build_declaration(self, scope_level):
        is_dynasty = False
        token = self.current_token()
        array_dimensions = []

        # Check for optional 'dynasty' token
        if token and token[0] == 'dynasty':
            is_dynasty = True
            self.advance()
            token = self.current_token()

        # Expect a data type next
        datatype = token  # use the literal value for the type
        self.advance()
        token = self.current_token()

        # Expect an identifier
        identifier = token  # extract the identifier's name
        self.advance()

        
        value = None
        token = self.current_token()
        declarations = None

        # array
        if token[0] == '[':
            self.match('[')
            token = self.current_token()
            array_dimensions.append(token)
            self.advance()
            self.match(']')
            token = self.current_token()

            if token[0] == '[':
                self.match('[')
                token = self.current_token()
                array_dimensions.append(token)
                self.advance()
                self.match(']')
            
            # with initialization
            elif token[0] == '=':
                self.match('=')
                value = self.build_expression()
                # after val init
                self.advance()
                token = self.current_token()
                declarations.append([VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)])

            elif token[0] == ',':
                declarations.extend(self.build_vardec_more(datatype, is_dynasty, scope_level))

            elif token[0] == '~':
                self.match('~')
            
        # with initialization
        elif token[0] == '=':
            self.match('=')
            value = self.build_expression()
            # after val init
            self.advance()
            token = self.current_token()
            declarations.append([VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)])

        elif token[0] == ',':
            declarations.extend(self.build_vardec_more(datatype, is_dynasty, scope_level))

        elif token[0] == '~':
            self.match('~')

    
        return declarations


    def build_vardec_more(self, datatype, is_dynasty, scope_level):
        additional_declarations = []
        
        while True:
            token = self.current_token()
            if not token or token[0] != ',':
                break
                
            self.match(',')
            
            # Get the identifier
            token = self.current_token()
            if not token:
                break
                
            identifier = token
            self.advance()
            
            value = None
            array_dimensions = []
            
            token = self.current_token()
            
            # Array handling
            if token and token[0] == '[':
                self.match('[')
                token = self.current_token()
                array_dimensions.append(token)
                self.advance()
                self.match(']')
                token = self.current_token()
                
                if token and token[0] == '[':
                    self.match('[')
                    token = self.current_token()
                    array_dimensions.append(token)
                    self.advance()
                    self.match(']')
                    token = self.current_token()
                
                # Initialize array if needed
                if token and token[0] == '=':
                    self.match('=')
                    value = self.build_expression()
                    token = self.current_token()
            
            # Regular variable initialization
            elif token and token[0] == '=':
                self.match('=')
                value = self.build_expression()
                token = self.current_token()
            
            # Create the declaration node and add it to our list
            decl = VariableDeclarationNode(datatype, identifier, value, is_dynasty, scope_level, array_dimensions)
            additional_declarations.append(decl)
            
            # Check if we need to terminate
            if token and token[0] == '~':
                self.match('~')
                break
                
        return additional_declarations


    def build_global_declarations(self):
        declarations = []
        
        while True:
            token = self.current_token()
            
            # End parsing if we encounter function or main program
            if token is None or token[0] in ['spell', 'castle']:
                break
                
            declarations.extend(self.build_declaration(scope_level=GLOBAL_SCOPE))
            
        return declarations

    def build_expression(self):
        token = self.current_token()  # Get the current token
        expression = []
        
        # Loop until we hit a terminator ('~' or ',')
        while token[0] not in ['~', ',']:
            expression.append(token)
            self.advance()
            token = self.current_token()  # update token
        
        return expression
    

    def build_global_functions(self):
        functions = []
        
        while True:
            token = self.current_token()
            
            # End parsing if we encounter the main function 
            if token is None or token[0] == 'castle':
                break
                
            if token[0] == 'spell':
                functions.append(self.build_function(True))
                
        return functions
    

    def build_function(self, is_global):
        self.match('spell')
        
        # Get the return type
        token = self.current_token()
        return_type = token
        self.advance()
        
        # Get the function name
        token = self.current_token()
        identifier = token
        self.advance()
        
        # Parse parameters
        self.match('(')
        parameters = self.build_parameters()
        self.match(')')
        
        # Function body
        self.match('{')
        body = self.build_block(LOCAL_SCOPE)
        self.match('}')
        
        # Check for return value
        return_val = None
        token = self.current_token()
        if token and token[0] == 'return':
            self.match('return')
            return_val = self.build_expression()
            self.match('~')
            
        return FunctionNode(return_type, identifier, parameters, body, return_val, is_global, GLOBAL_SCOPE)
    
    def build_parameters(self):
        parameters = []
        
        token = self.current_token()
        if token and token[0] == ')':  # Empty parameters
            return parameters
            
        # Parse the first parameter
        datatype = token
        self.advance()
        
        token = self.current_token()
        identifier = token
        self.advance()
        
        parameters.append(ParameterNode(datatype, identifier))
        
        # Parse additional parameters
        token = self.current_token()
        while token and token[0] == ',':
            self.match(',')
            
            token = self.current_token()
            datatype = token
            self.advance()
            
            token = self.current_token()
            identifier = token
            self.advance()
            
            parameters.append(ParameterNode(datatype, identifier))
            token = self.current_token()
            
        return parameters
    

    def build_main_function(self):
        token = self.current_token()
        if not token or token[0] != 'castle':
            return None
            
        self.match('castle')
        self.match('{')
        
        body = self.build_block(LOCAL_SCOPE)
        
        self.match('}')
        
        return MainFunctionNode(body)


