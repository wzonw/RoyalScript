from lexer import RoyalScriptLexer, Token
from RS_RegDef import Delims, RegDef
import traceback    

class RoyalScriptParser:
    def __init__(self, tokens):
        """Initialize with tokens and syntax rules."""
        self.tokens = tokens  # List of token types for each line
        self.current_line = 0  # Current line index
        self.current_index = 0  # Current token index
        self.error_message = ""
        self.parsing_result = ""  # Parsing output
    
    def current_token(self):
        """Return the current token type in the current line, skipping empty tokens."""
        while self.current_line < len(self.tokens):
            if self.current_index < len(self.tokens[self.current_line]):
                return self.tokens[self.current_line][self.current_index]
            self.current_line += 1
            self.current_index = 0
        return None  # End of tokens

    def advance(self):
        """Move to the next token."""
        if self.current_index + 1 < len(self.tokens[self.current_line]):
            self.current_index += 1
        elif self.current_line + 1 < len(self.tokens):
            self.current_line += 1
            self.current_index = 0
        else:
            return None  # End of tokens

    def peek_next_token(self):
        """Peek at the next token without advancing the position."""
        temp_line, temp_index = self.current_line, self.current_index  

        if temp_index + 1 < len(self.tokens[temp_line]):
            return self.tokens[temp_line][temp_index + 1]  # Next token in the same row
        elif temp_line + 1 < len(self.tokens):
            return self.tokens[temp_line + 1][0]  # First token of the next row

        return None  # No more tokens

    def match(self, expected):
        """Match the current token against the expected value."""
        token = self.current_token()
        if token == expected:
            self.advance()
            return True
        
        if token is None:
            self.error_message = f"Syntax Error: Unexpected end of input at Line {self.current_line + 1}"
        else:
            self.error_message = f"Syntax Error: Expected {expected}, but got {repr(token)} at Line {self.current_line + 1}, Index {self.current_index}"
        
        return False
    
    def program(self):
        """Main program parser."""
        self.error_message = ""

        if not self.match("crown") or not self.match("~"):
            return False
        
        if not self.global_dec():
            return False

        if not self.match("castle"):
            return False
        if not self.match("treasures"):
            return False
        if not self.match("identifier"):
            return False
        if not self.match("(") or not self.match(")"):
            return False
        if not self.match("{"):
            return False
        if not self.match("return") or not self.match("0") or not self.match("~") or not self.match("}"):
            return False

        if not self.match("reign") or not self.match("~"):
            return False
        
        return self.match("EOF")  # Ensure the end of the file is reached

    def global_dec(self):
        """Handle global declarations."""
        if self.var_dec():
            token = self.current_token()
            if token in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures']:
                return self.global_dec()
            return True

        token = self.current_token()
        return token in ['castle', 'spell', 'reign']

    def var_dec(self):
        """Parse variable declarations."""
        if not self.dynasty():
            return False
        if not self.data_type():
            return False
        self.advance()
        if not self.match('identifier'):
            return False
        
        return self.vardec_def()

    def dynasty(self):
        #<dynasty>: dynasty
        if self.match('dynasty'):
            return True
        elif self.data_type():
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def vardec_def(self):
        """Parse variable declarations after identifier."""
        if self.initialization():
            if not self.vardec_more():
                return False
            return self.match("~")

        elif self.match('['):
            if not self.match('pos_treasures_lit'):
                return False
            if not self.match(']'):
                return False
            if not self.column():
                return False
            if not self.array_initialization():
                return False
            if not self.array_more():
                return False
            return self.match('~')

        return False

    def initialization(self):
        """Parse initialization values."""
        if self.match('='):
            return self.val()
        return self.current_token() in ['~', ',']

    def vardec_more(self):
        """Handle additional variable declarations separated by commas."""
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                return False
            return self.vardec_more()
        return self.current_token() == '~'
    

    def array_element(self):
        #<array_element>: identifier <index>

        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.index():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True
    

    def func_call(self):
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.args():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        print("pass func_call")
        return True
    

    def args(self):
        token = self.current_token()

        #<args>: <args_val> <args_more>
        if self.args_val():
            # Don't check args_more if we're at the end of arguments
            if token == ')':
                return True
            if not self.args_more():
                return False
            return True

        #<args>:λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    

    def args_val(self):
        token = self.current_token()

        if self.match('identifier'):
            return True

        elif self.match('scroll_lit'):
            return True

        elif self.match('rose_lit'):
            return True

        elif self.match('treasures_lit'):
            return True

        elif self.match('ocean_lit'):
            return True

        elif self.match('mirror_lit'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
    def args_more(self):
        token = self.current_token()

        #<args_more>: , <args> <args_more>
        if token == ',':
            self.advance()
            if not self.args():
                return False
            return self.args_more()
        
        #<args_more>: λ
        # Allow any token that could follow a function call
        elif token in [')', '+', '-', '*', '/', '%', '~']:
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def treasures_mirror(self):
        token = self.current_token()

        if self.match('1'):
            return True
        
        elif self.match('0'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    

    def arithmetic_exp(self):
        #<arithmetic_exp>: <arithmetic_operand> <arithmetic_operator> <arithmetic_operand> <more_arith>

        if not self.arithmetic_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.arithmetic_operator():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.arithmetic_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.more_arith():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True
    
    def arithmetic_operand(self):
        token = self.current_token()
        
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':  # If it's a function call
                if not self.func_call():  # Parse the function call
                    return False
                return True  # Successfully parsed function call as operand
            return self.match('identifier')
        elif self.match('ocean_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('('):  # Only call arithmetic_exp() if inside parentheses
            if not self.arithmetic_exp():
                return False
            if not self.match(')'):
                return False
            return True
        else:
            return False



        
    def arithmetic_operator(self):
        if self.match('+'):
            return True

        elif self.match('-'):
            return True

        elif self.match('/'):
            return True

        elif self.match('*'):
            return True

        elif self.match('%'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def more_arith(self):
        token = self.current_token()

        # If there's an arithmetic operator, we expect another operand afterward
        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                self.error_message = f"Syntax Error: Expected operand but got {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return self.more_arith()  # Continue parsing if there's more arithmetic

        # Valid stopping points for arithmetic expressions
        elif token in [')', '~', ',', '<', '>', '<=', '>=', '==', '!=']:
            return True  

        else:
            self.error_message = f"Syntax Error: Unexpected token {repr(token)} at Line {self.current_line + 1}"
            return False





    def concat(self):
        """Handle string concatenation."""
        if not self.string_operand():
            return False
        if not self.match('+'):
            return False
        if not self.string_operand():
            return False
        return self.string_more()

    def string_operand(self):
        """Handle string operand parsing."""
        if self.match('scroll_lit'):
            return True
        if self.match('identifier'):
            return True
        if self.match('rose_lit'):
            return True
        if self.array_element():
            return True
        if self.match('tooscroll'):
            if not self.match('(') or not self.conversion_value() or not self.match(')'):
                return False
            return True
        return False

    def string_more(self):
        """Handle additional string concatenation."""
        if self.match('+'):
            if not self.string_operand():
                return False
            return self.string_more()
        return True  # Can be empty (λ)



    def data_type(self):
        token = self.current_token()
        if token in {'scroll', 'treasures', 'mirror', 'ocean', 'rose'}:
            # self.advance()  # Consume the data_type token
            return True
        self.error_message = f"Syntax Error: Invalid data type {repr(token)} at Line {self.current_line}"
        return False


    def val(self):
        token = self.current_token()
        next_token = self.peek_next_token()

        if token == 'identifier':
            if next_token == '(':  # Function call
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index -= 1  # Back up to include operator
                        return self.arithmetic_exp()  # Parse whole thing as arithmetic expression
                    return True  # Just a standalone function call
                return False
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()

        elif token in {'rose_lit', 'phantom'}:
            return self.match(token)
    
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()

            if next_token == '+':
                return self.concat()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                self.relational_exp()
            else:
                return self.match(token)
            
        elif token == 'treasures_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
            
        elif token == 'ocean_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        
        elif token == 'mirror_lit':
            next_token = self.peek_next_token()
            if next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)
        
        elif token == 'wish': 
            return self.input() 

        elif self.type_conversion():
            return True
        elif self.arithmetic_exp():
            return True
        # elif self.relational_exp():
        #     return True
        # elif self.logical_exp():
        #     return True
        # elif self.treasures_mirror():
        #     return True
        # elif self.func_call():
        #     return True
        # elif self.array_element():
        #     return True
    
    def type_conversion(self):
        #<type_conversion>: <conversion_func> (<conversion_value>)
        if not self.conversion_func():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.conversion_value():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def conversion_func(self):
        if self.match('toscroll'):
            return True
        elif self.match('totreasures'):
            return True
        # elif self.match('tomirror'):
        #     return True
        elif self.match('toocean'):
            return True
        elif self.match('torose'):
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def conversion_value(self):
        if self.match('scroll_lit'):
            return True
        elif self.match('rose_lit'):
            return True
        elif self.match('ocean_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.match('identifier'):
            if not self.index():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        elif self.func_call():
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def index(self):
        token = self.current_token()

        #<index>: [treasures_lit] <column1>
        if self.match('['):
            if not self.match('treasures_lit'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(']'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print("index-done")
            if not self.column1():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print("column1")
            return True

        #<index>: λ
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
            

    def column1(self): 
        token = self.current_token()

        #<column1>: [treasures_lit]
        if self.match('['):
            if not self.match('treasures_lit'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(']'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<column1>: λ
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{' ]:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        
    def input(self):
        #<input>: wish (scroll_lit)
        if not self.match('wish'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('scroll_lit'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True


    def parse(self):
        """Parse the program starting from the 'crown' keyword."""
        if self.program():
            self.parsing_result = "Parsing successful."
            return True
        else:
            # Raise the error instead of just printing it
            # raise SyntaxError(self.error_message)
            print(self.error_message)

    def get_parsing_result(self):
        """Return parsing result."""
        return self.parsing_result