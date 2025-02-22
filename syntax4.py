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
        print(f"Matching {repr(self.current_token())} against {repr(expected)}")
        return False
    
    def program(self):
        """Main program parser."""
        self.error_message = ""

        if not self.match("crown") or not self.match("~"):
            return False
        
        if not self.global_dec():
            return False
        
        if not self.user_defined_func():
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
        
        if not self.body():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
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
        
        # Case 1: Variable declaration with initialization (e.g., `identifier = value`)
        if self.initialization():
            if not self.vardec_more():
                return False
            return self.match("~")

        # Case 2: Variable declaration for array (e.g., `identifier[2][2]`)
        elif self.match('['):
            # Handle the first dimension (e.g., `identifier[2]`)
            if not self.match('treasures_lit'):  # This should match the dimension literal (e.g., a number)
                return False
            if not self.match(']'):  # Closing the first dimension
                return False
            
            # If there are additional dimensions (e.g., `[2][2]`), handle them
            if not self.column():  # This handles the second dimension (and beyond)
                return False
            
            # Proceed with array initialization (e.g., `= {1, 2, 3}`)
            if not self.array_initialization():
                return False
            
            # Check for additional array declarations if needed
            if not self.array_more():
                return False
            
            # Match the end of the variable declaration with "~"
            return self.match('~')

        # Case 3: Syntax Error if neither condition is met
        self.error_message = f"Syntax Error: Expected '=', but got '{repr(self.current_token())}' at Line {self.current_line + 1}"
        return False


    def initialization(self):
        token = self.current_token()
        """Parse initialization values."""
        print(f"This is {token}")
        if self.match('='):
            print("Enter initialization")
            return self.val()
        return self.current_token() in ['~', ',']

    def vardec_more(self):
        """Handle additional variable declarations separated by commas."""
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                return False
            return self.vardec_more()
        return self.current_token() == '~'
    
    def column(self):
        # <column>: [num]

        token = self.current_token()

        if self.match('['):
            if not self.match('treasures_lit'):
                return False
            if not self.match(']'):
                return False
            return True
        
        # <column>: λ (Null)
        elif token in ['=', ',', '~']:  # End of the array definition
            return True  # Null transition, as there’s no further dimension
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False  # Error if the token doesn't match valid patterns

        
    def array_initialization(self):
        # <array_initialization>: = <array_list>

        token = self.current_token()

        if self.match('='):
            if not self.array_list():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        elif token in [',', '~']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_list(self):
        # <array_list>: {<array_content>}

        if not self.match('{'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.array_content():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.match('}'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True


    def array_content(self):
        # <array_content>: <array_lit> <lit_more>

        if self.array_lit():
            if not self.lit_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # <array_content>: {<array_row>} <row_more>
        elif self.match('{'):
            if not self.array_row():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.row_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_row(self):
        # <array_row>: <array_lit> <lit_more>

        if not self.array_lit():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.lit_more():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True


    def row_more(self):
        # <row_more>: , {array_row} <row_more>
        token = self.current_token()

        if self.match(','):
            if not self.match('{'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.array_row():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.row_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # <row_more>: λ
        elif token == '}':
            return True  # If no more rows, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def lit_more(self):
        # <lit_more>: , <array_lit> <lit_more>
        token = self.current_token()

        if self.match(','):
            if not self.array_lit():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.lit_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # <lit_more>: λ
        elif token == '}':
            return True  # If no more literals, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_more(self):
        # <array_more>: , identifier [num] <column> <array_initialization> <array_more>
        token = self.current_token()

        if self.match(','):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('['):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('treasures_lit'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(']'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.column():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.array_initialization():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.array_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # <array_more>: λ
        elif token == '~':
            return True  # End of array initialization with tilde

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_lit(self):
        if self.match('scroll_lit'):
            return True
        elif self.match('rose_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('ocean_lit'):
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.match('identifier'):
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def assignment_exp(self):
        #<assignment_exp>: identifier <assignment_operator> <assignment_operand>

        print("Entering assignment_exp")  # Debugging line
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        print(f"Passed ID match: {repr(self.current_token())}")  # Debugging line
        
        if not self.assignment_operator():
            self.error_message = f"Syntax Error: Invalid input// {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.assignment_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True


    def assignment_operator(self):
        token = self.current_token()  # Get the current token
        print(f"Current token in assignment_operator: {token}")  # Debugging line to check the token
        
        if self.match('+='):
            return True

        elif self.match('-='):
            return True

        elif self.match('*='):
            return True

        elif self.match('/='):
            return True

        elif self.match('%='):
            return True
        
        # if naging assignment operand ang arithmetic exp
        elif self.match('+'):
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
            self.error_message = f"Syntax Error: Invalid input // {repr(token)} at Line {self.current_line + 1}"
            return False


    def assignment_operand(self):
        print("Entering assignment_operand")  # Debugging line
        next_token = self.peek_next_token()
        token = self.current_token()
        start_pos = self.current_index
        
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':  # If it's a function call
                while self.current_token() and self.current_token() != ')':
                    self.advance()
                # self.advance()
                token = self.current_token()
                print(f" Token: {token}")
                next_paren_token = self.peek_next_token()
                if next_paren_token in ['+', '-', '/', '*', '%']:
                    self.current_index = start_pos
                    if not self.arithmetic_exp():
                        return False
                    return True
                elif not self.func_call():  # Parse the function call
                    return False
                print(f" Token: {token}")
                return True  # Successfully parsed function call as operand
            elif next_token == '[':
                brackets = 1  # Track nested brackets
                self.advance()
                token = self.current_token()
                print(f" Token: {token}")
                while self.current_token() == '[' or self.current_token() == ']' or self.current_token() == 'treasures_lit' or self.current_token() == '0':
                    self.advance()
                    # If we reach the end of tokens, prevent infinite loop
                    if self.current_token() is None:
                        print("Error: Unexpected end of tokens while parsing array indexing")
                        return False
                    
                    if self.current_token in ['[', ']']:
                        brackets += 1

                if brackets > 4:
                    print("Error: Only 2d array is allowed")
                    return False

                
                token = self.current_token()
                print(f"Token after ]: {token}")  # Debugging line

                # Check for arithmetic operators after the array indexing
                next_paren_token = self.current_token()
                print(f"Next token after array indexing: {next_paren_token}")  # Debugging line

                if next_paren_token in ['+', '-', '/', '*', '%']:
                    self.current_index = start_pos
                    if not self.arithmetic_exp():
                        self.advance()
                        return False
                    return True
                
                elif not self.index():  # Parse the function call
                    return False
                print(f" Token: {token}")
                return True  # Successfully parsed function call as operand

        elif token == 'treasures_lit':
            if next_token in ['+', '-', '/', '*', '%']:
                if not self.arithmetic_exp():
                    return False
                return True
            else:
                return self.match('treasures_lit')

        elif self.match('ocean_lit'):
            return True
        
        elif self.match('('):  # Only call arithmetic_exp() if inside parentheses
            if not self.arithmetic_operand():
                return False
            if not (self.match('+') or self.match('-') or self.match('/') or self.match('*') or self.match('%')):
                print("Invalid operand")
                return False
            if not self.arithmetic_operand():
                return False
            if not self.more_arith():
                return False
            if not self.match(')'):
                return False
            return True

        elif self.array_element():
            return True

        elif self.arithmetic_exp():
            return True

        elif self.func_call():
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False




    def array_element(self):
        # <array_element>: identifier <index>

        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.index():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True


    def logical_exp(self):
        #<logical_exp>: <logical_operand> <logical_operator> <logical_operand> <more_log>
        token = self.current_token()
        print(f"enter log_exp {token}")
        if self.logical_operand():
            print(f"passed log_operand {token}")
            if not self.logical_operator():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print(f"passed log_operator {token}")
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print(f"passed log_operand {token}")
            if not self.more_log():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<logical_exp>: <logical_operator1> <logical_operand> <more_log>
        
        elif self.logical_operator1():
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.more_log():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    
    def logical_operand(self):
        token = self.current_token()
        print(f"Checking logical operand: {token}")

        if token == 'identifier':
            next_token = self.peek_next_token()
            print(f"Next token after identifier: {next_token}")

            if next_token == '(':
                if self.func_call():  # Parse the function call
                    print("Function call detected and parsed.")
                    return True
            elif next_token == '[':
                self.advance()
                if self.index():
                    print("Array element detected and parsed.")
                    return True
            else:
                return self.match('identifier')

        elif self.match('treasures_lit'):
            return True

        elif self.match('mirror_lit'):
            return True

        elif self.match('0'):
            return True

        elif self.treasures_mirror():
            return True

        elif self.relational_exp():
            return True

        elif self.match('('):  
            if not self.relational_operand():
                return False
            if not (self.match('<') or self.match('>') or self.match('<=') or self.match('>=') or self.match('==') or self.match('!=')):
                print("Invalid operand")
                return False
            if not self.relational_operand():
                return False
            if not self.relational_more():
                return False
            if not self.match(')'):
                return False
            return True

        elif self.func_call():  # Function calls as logical operands
            return True

        elif self.array_element():  # Array elements as logical operands
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

  
    def logical_operator(self):

        if self.match('&&'):
            return True

        elif self.match('||'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
    def logical_operator1(self):

        if self.match('!'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def more_log(self):
        token = self.current_token()
        print(f"Checking more_log: {token}")

        if self.logical_operator():
            print("Logical operator detected, continuing more_log_ext...")
            if not self.more_log_ext():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        elif token in [',', '~', ')']:
            print(f"End of logical expression detected: {token}")
            return True

        else:
            self.error_message = f"Syntax Error: Unexpected token {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def more_log_ext(self):
        #<more_log_ext>: <logical_operand><more_log>
        if self.logical_operand():
            if not self.more_log():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<more_log_ext>: <logical_operator1> <logical_operand><more_log>
        elif self.logical_operator1():
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.more_log():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    

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
        token = self.current_token()
        #<arithmetic_exp>: <arithmetic_operand> <arithmetic_operator> <arithmetic_operand> <more_arith>
        print(f"Enter Arith_exp {token}")
        if not self.arithmetic_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        print("Enter Arith_op success")
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
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')
            
        
        elif self.match('ocean_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('0'):
            return True
        elif self.match('('):  # Only call arithmetic_exp() if inside parentheses
            if not self.arithmetic_operand():
                return False
            if not (self.match('+') or self.match('-') or self.match('/') or self.match('*') or self.match('%')):
                print("Invalid operand")
                return False
            if not self.arithmetic_operand():
                return False
            if not self.more_arith():
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
        

        # if may kahalong relational (arithmetic as relational-operand)
        elif self.match('<'):
            return True

        elif self.match('>'):
            return True

        elif self.match('<='):
            return True

        elif self.match('>='):
            return True

        elif self.match('=='):
            return True

        elif self.match('!='):
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


    def relational_exp(self):
       #<relational_exp>: <relational_operand> <relational_operator> <relational_operand> <relational_more> 
       if not self.relational_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
       if not self.relational_operator():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
       if not self.relational_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
       if not self.relational_more():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
       return True
    
    def relational_operand(self):
        token = self.current_token()

        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':  # If it's a function call
                if not self.func_call():  # Parse the function call
                    return False
                return True  # Successfully parsed function call as operand
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')

        elif self.match('scroll_lit'):
            return True

        elif self.match('treasures_lit'):
            return True
        
        elif self.match('0'):
            return True

        elif self.match('ocean_lit'):
            return True

        elif self.match('('):  # Only call arithmetic_exp() if inside parentheses
            if not self.arithmetic_operand():
                return False
            if not (self.match('+') or self.match('-') or self.match('/') or self.match('*') or self.match('%')):
                print("Invalid operand")
                return False
            if not self.arithmetic_operand():
                return False
            if not self.more_arith():
                return False
            if not self.match(')'):
                return False
            return True

        elif self.arithmetic_exp():
            return True

        elif self.func_call():
            return True

        elif self.array_element():
            return True
        

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def relational_operator(self):

        if self.match('<'):
            return True

        elif self.match('>'):
            return True

        elif self.match('<='):
            return True

        elif self.match('>='):
            return True

        elif self.match('=='):
            return True

        elif self.match('!='):
            return True
        
        #if naging logical operand yung relational 
        elif self.match('&&'):
            return True

        elif self.match('||'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def relational_more(self):
        #<relational_more>: <relational_operator> <relational_operand> <relational_more>
        token = self.current_token()

        if self.relational_operator():
            if not self.relational_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.relational_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<relational_more>: λ
        elif token in [')', '', '', '~', '&&', '||']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def unary(self):
        token = self.current_token()
        #<unary>: identifier <unary_operator>
        print("Unary")
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        print(f"This is {token}")
        if not self.unary_operator():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def unary_operator(self):
        
        if self.match('++'):
            return True

        elif self.match('--'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False



    def concat(self):
        """Handle string concatenation."""
        token = self.current_token()
        print(f"Enter concat {token}")
        if not self.string_operand():
            return False
        if not self.match('+'):
            return False
        if not self.string_operand():
            return False
        return self.string_more()

    def string_operand(self):
        token = self.current_token()
        """Handle string operand parsing."""
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':  # If it's a function call
                if not self.func_call():  # Parse the function call
                    return False
                return True  # Successfully parsed function call as operand
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')
        elif self.match('scroll_lit'):
            return True
        elif self.match('rose_lit'):
            return True
        elif self.array_element():
            return True
        elif self.match('toscroll'):
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            print(f"Token = {token}")
            return True
        else:
            return False

    def string_more(self):
        """Handle additional string concatenation."""
        if self.match('+'):
            if not self.string_operand():
                return False
            return self.string_more()
        return True  # Can be empty (λ)


    def user_defined_func(self):

        token = self.current_token()

        #<user-defined_func>: spell <return_type> identifier(<param>) {<body><ret_statement>} <user-defined_func>
        if self.match('spell'):
            if not self.return_type():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('('):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.param():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('{'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.ret_statement():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.user_defined_func():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return self.user_defined_func()

        #<user-defined_func>: λ
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'comment', 'continue', '}', 'return', 'break', 'castle']:
            return True
        
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def return_type(self):

        if self.match('treasures'):
            return True
        elif self.match('ocean'):
            return True
        elif self.match('scroll'):
            return True
        elif self.match('rose'):
            return True
        elif self.match('mirror'):
            return True
        elif self.match('chamber'):
            return True
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def param(self):
        token = self.current_token()
        
        #<param>: <data_type> identifier <param_more>
        print("enter param")
        if self.data_type():
            self.advance()
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.param_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<param>: λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def param_more(self):
        token = self.current_token()

        #<param_more>: , <data_type> identifier <param_more>
        if self.match(','):
            if not self.data_type():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            self.advance()
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.param_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<param_more>: λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def body(self):
        token = self.current_token()
        next_token = self.peek_next_token()

        # Base Case: Stop recursion when we reach 'return' or '}'
        if token in ['return', '}']:
            return True  # Successfully ended parsing

        elif token == 'identifier':
            if next_token == '=':
                if not self.var_reassign():
                    return False
                return self.body()
            elif next_token in ['++', '--']:
                if not self.unary():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
            elif next_token in ['+=', '-=', '*=', '/=', '%=']:
                if not self.assignment_exp():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
            elif next_token == '(':
                if not self.func_call():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
        
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'rose', 'ocean']:
            if not self.var_dec():
                return False
            return self.body()
        
        elif token == 'granted':
            if not self.output():
                return False
            return self.body()
        
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.body()
            
        elif token in ["single_comment", "multi_comment"]:
            return self.body()
        
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        
    
    def ret_statement(self):
        token = self.current_token()
        print(f"This is {token}")
        #<ret_statement>: return <val1> ~
        if self.match('return'):
            print('passed return')
            if not self.val1():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print('val1')
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<ret_statement>: λ
        elif token == '}':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def var_reassign(self):
        #<var_reassign>: identifier = <val> ~
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('='):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.val():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def output(self):
        #<output>: granted(<granted_content> <more_granted>) ~
        if not self.match('granted'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.granted_content():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.more_granted():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    

    def granted_content(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        if token == 'identifier':
            if next_token == '(':  # Function call
                start_pos = self.current_index  # Save starting position
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)
            
        elif token == 'rose_lit':
            if next_token == '+':
                return self.concat()
            return self.match(token)
        
        elif token == 'phantom':
            return self.match(token)
        
        elif token == '!':
            return self.logical_exp()
    
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()

            if next_token == '+':
                return self.concat()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
            
        elif token == 'treasures_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
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
            
        elif token == '(':
            print(f"This is {token}")
            start_pos = self.current_index
            # Skip until we find the matching closing parenthesis
            paren_count = 1
            content = []
            
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:  # End of tokens before closing parenthesis
                    self.error_message = ("Syntax Error: Missing closing parenthesis")
                    return False  # Or raise an exception

                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            
            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)

            if next_after_paren == '~':
                # Advance past both the closing parenthesis and the tilde
                self.advance()  # Move past ')'
                self.advance()  # Move past '~'
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    return False
            else:
                # Reset position and parse according to the operator
                self.current_index = start_pos
                
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren == 'relational':
                        return self.logical_exp()
                    print("Error invalid operand")
                    return False
                else:
                    print(f"This is == {token}")
                    return False
                
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose']:
            start_pos = self.current_index  # Store initial position
            self.advance()  # Move past the current token
            
            paren_count = 1  # Assuming '(' has already been encountered

            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()  # Move to the next token
                cur_token = self.current_token()
                
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1

            # If loop exited without closing parenthesis, there's a syntax error
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                return False

            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos

            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == ')' :
                return self.type_conversion()
            else:
                print("Invalid string operations")
                return False
            
        # elif self.set_precision():
        #     return True
        # elif self.concat():
        #     return True
        # elif self.relational_exp():
        #     return True
        # elif self.logical_exp():
        #     return True
        # elif self.unary():
        #     return True
        # elif self.arithmetic_exp():
        #     return True
        # elif self.array_element():
        #     return True
        # elif self.func_call():
        #     return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def set_precision(self):
        #<set_precision>: %.[treasures_lit]f
        if not self.match('%'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('.'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('['):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('treasures_lit'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(']'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('f'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
        


    def more_granted(self):
        token = self.current_token()

        #<more_granted>: , <granted_content> <more_granted>
        if self.match(','):
            if not self.granted_content():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.more_granted():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<more_granted>: λ
        elif token == ')':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


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
                start_pos = self.current_index  # Save starting position
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)

        elif token == 'rose_lit':
            if next_token == '+':
                return self.concat()
            return self.match(token)
        
        elif token == 'phantom':
            return self.match(token)
        
        elif token == '!':
            return self.logical_exp()
    
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()

            if next_token == '+':
                return self.concat()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
            
        elif token == 'treasures_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
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
            
        elif token == '(':
            print(f"This is {token}")
            start_pos = self.current_index
            # Skip until we find the matching closing parenthesis
            paren_count = 1
            content = []
            
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:  # End of tokens before closing parenthesis
                    self.error_message = ("Syntax Error: Missing closing parenthesis")
                    return False  # Or raise an exception

                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            
            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)

            if next_after_paren == '~':
                # Advance past both the closing parenthesis and the tilde
                self.advance()  # Move past ')'
                self.advance()  # Move past '~'
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    return False
            else:
                # Reset position and parse according to the operator
                self.current_index = start_pos
                
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren == 'relational':
                        return self.logical_exp()
                    print("Error invalid operand")
                    return False
                else:
                    print(f"This is == {token}")
                    return False
                
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose']:
            start_pos = self.current_index  # Store initial position
            self.advance()  # Move past the current token
            
            paren_count = 1  # Assuming '(' has already been encountered

            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()  # Move to the next token
                cur_token = self.current_token()
                
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1

            # If loop exited without closing parenthesis, there's a syntax error
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                return False

            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos

            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == '~':
                return self.type_conversion()
            else:
                print("Invalid string operations")
                return False

                
        elif token == 'wish':
            return self.input()
        
        
            
        # elif self.type_conversion():
        #     return True
        # elif self.arithmetic_exp():
        #     return True
        # elif self.relational_exp():
        #     return True
        # elif self.logical_exp():
        #     return True
        return False
    
    def val1(self):
        token = self.current_token()


        token = self.current_token()
        next_token = self.peek_next_token()

        if token == 'identifier':
            if next_token == '(':  # Function call
                start_pos = self.current_index  # Save starting position
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    return True  
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    return True  
                return False
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            # Check if it's an assignment operator (+=, -=, /=, *=, %=)
            elif next_token in ['+=', '-=', '/=', '*=', '%=']:
                return self.assignment_exp()
            # Check if it's a unary operator (++ or --)
            elif next_token in ['++', '--']:
                return self.unary()
            else:
                return self.match(token)

        elif token == 'rose_lit':
            if next_token == '+':
                return self.concat()
            return self.match(token)
        
        elif token == 'phantom':
            return self.match(token)
        
        elif token == '!':
            return self.logical_exp()
    
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()

            if next_token == '+':
                return self.concat()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
            
        elif token == 'treasures_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
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
            
        elif token == '(':
            print(f"This is {token}")
            start_pos = self.current_index
            # Skip until we find the matching closing parenthesis
            paren_count = 1
            content = []
            
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:  # End of tokens before closing parenthesis
                    self.error_message = ("Syntax Error: Missing closing parenthesis")
                    return False  # Or raise an exception

                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            
            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)

            if next_after_paren == '~':
                # Advance past both the closing parenthesis and the tilde
                self.advance()  # Move past ')'
                self.advance()  # Move past '~'
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    return False
            else:
                # Reset position and parse according to the operator
                self.current_index = start_pos
                
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    print("Error invalid operand")
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren == 'relational':
                        return self.logical_exp()
                    print("Error invalid operand")
                    return False
                else:
                    print(f"This is == {token}")
                    return False
            
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose']:
            start_pos = self.current_index  # Store initial position
            self.advance()  # Move past the current token
            
            paren_count = 1  # Assuming '(' has already been encountered

            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()  # Move to the next token
                cur_token = self.current_token()
                
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1

            # If loop exited without closing parenthesis, there's a syntax error
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                return False

            # Now we're at the closing parenthesis, check what follows
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos

            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == '~':
                return self.type_conversion()
            else:
                print("Invalid string operations")
                return False


            
        elif token == 'wish': 
            return self.input() 

        # elif self.type_conversion():
        #     return True
        # elif self.arithmetic_exp():
        #     return True
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
        else:
            return False

    
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
    
    def determine_operation_type(self, content):
        """Analyze the content inside parentheses to determine operation type."""
        # Remove the closing parenthesis if it's there
        if content and content[-1] == ')':
            content.pop()
            
        # Join the list of tokens into a single string
        content_str = ' '.join(str(token) for token in content).lower()
        
        # Check for arithmetic operators
        if any(op in content_str for op in ['+', '-', '*', '/', '%']):
            return 'arithmetic'
        # Check for relational operators
        elif any(op in content_str for op in ['>', '<', '>=', '<=', '==', '!=']):
            return 'relational'
        # Check for logical operators
        elif any(op in content_str for op in ['and', 'or', '&&', '||']):
            return 'logical'
        # Invalid operation case
        return 'Not Valid'


    def parse(self):
        """Parse the program starting from the 'crown' keyword."""
        if self.program():
            self.parsing_result = "Parsing successful."
            return True
        else:
            # Raise the error instead of just printing it
            raise SyntaxError(self.error_message)
            # print(self.error_message)

    def get_parsing_result(self):
        """Return parsing result."""
        return self.parsing_result
    