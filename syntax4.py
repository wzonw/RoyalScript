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
            if self.tokens[self.current_line]:  # Ensure line is not empty
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
            while self.current_line < len(self.tokens) and not self.tokens[self.current_line]:  # Skip empty lines
                self.current_line += 1
        else:
            return None  # End of tokens


    def peek_next_token(self):
        """Peek at the next token without advancing the position."""
        if self.current_line < len(self.tokens):
            temp_line, temp_index = self.current_line, self.current_index

            if temp_index + 1 < len(self.tokens[temp_line]):  # Ensure next token exists in the same row
                return self.tokens[temp_line][temp_index + 1]
            elif temp_line + 1 < len(self.tokens) and self.tokens[temp_line + 1]:  # Ensure next line has tokens
                return self.tokens[temp_line + 1][0]

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
        # 1	<program>	→	crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~
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
            return False

        if not self.match("return") or not self.match("0") or not self.match("~") or not self.match("}"):
            return False

        if not self.match("reign") or not self.match("~"):
            return False
        
        return self.match("EOF")  # Ensure the end of the file is reached

    def global_dec(self):
        # 2	<global_dec>	→	<var_dec> <global_dec>
        if self.var_dec():
            token = self.current_token()
            if token in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures']:
                return self.global_dec()
            return True
        
        # 3	<global_dec>	→	λ
        token = self.current_token()
        return token in ['castle', 'spell', 'reign']

    def var_dec(self):
        # 4	<var_dec>	→	<dynasty> <data_type> id_lit <vardec_def>
        if not self.dynasty():
            return False
        if not self.data_type():
            return False
        self.advance()
        if not self.match('identifier'):
            return False
        
        return self.vardec_def()

    def dynasty(self):
        # 5	<dynasty>	→	dynasty
        if self.match('dynasty'):
            return True
        # 6	<dynasty>	→	λ
        elif self.data_type():
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def vardec_def(self):

        # 7	<vardec_def>	→	<initialization> <vardec_more>~
        if self.initialization():
            if not self.vardec_more():
                return False
            return self.match("~")

        # 8	<vardec_def>	→	[treasures_lit] <column> <array_initialization> <array_more>~
        elif self.match('['):
            # Handle the first dimension (e.g., `identifier[2]`)
            if not self.match('treasures_lit'):  
                return False
            if not self.match(']'): 
                return False
            
            # If there are additional dimensions (e.g., `[2][2]`)
            if not self.column():  
                return False
            
            # Proceed with array initialization
            if not self.array_initialization():
                return False
            
            # Check for additional array declarations if needed
            if not self.array_more():
                return False
            
            # Match the end of the variable declaration with "~"
            return self.match('~')

        self.error_message = f"Syntax Error: Expected '=', but got '{repr(self.current_token())}' at Line {self.current_line + 1}"
        return False


    def initialization(self):
        # 9	<initialization>	→	= <val>
        if self.match('='):
            return self.val()
        # 10	<initialization>	→	λ  
        return self.current_token() in ['~', ',']

    def vardec_more(self):
        # 11	<vardec_more>	→	, id_lit <initialization> <vardec_more>
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                return False
            return self.vardec_more()
        # 12	<vardec_more>	→	λ
        return self.current_token() == '~'
    
    def column(self):
        # 13	<column>	→	[treasures_lit]

        token = self.current_token()

        if self.match('['):
            if not self.match('treasures_lit'):
                return False
            if not self.match(']'):
                return False
            return True
        
        # 14	<column>	→	λ
        elif token in ['=', ',', '~']:  # End of the array definition
            return True  
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False 

        
    def array_initialization(self):
        # 15	<array_initialization>	→	= <array_list>

        token = self.current_token()

        if self.match('='):
            if not self.array_list():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        # 16	<array_initialization>	→	λ
        elif token in [',', '~']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_list(self):
        # 17	<array_list>	→	{<array_content>}

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
        # 18	<array_content>	→	<array_lit> <lit_more> 

        if self.array_lit():
            if not self.lit_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 19	<array_content>	→	{<array_row>} <row_more>
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
        # 20	<array_row>	→	<array_lit> <lit_more> 

        if not self.array_lit():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.lit_more():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True


    def row_more(self):
        # 21	<row_more>	→	, {array_row} <row_more>
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

        # 22	<row_more>	→	λ
        elif token == '}':
            return True  # If no more rows, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def lit_more(self):
        # 23	<lit_more>	→	, <array_lit> <lit_more>
        token = self.current_token()

        if self.match(','):
            if not self.array_lit():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.lit_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 24	<lit_more>	→	λ
        elif token == '}':
            return True  # If no more literals, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_more(self):
        # 25	<array_more>	→	, id_lit [treasures_lit] <column> <array_initialization> <array_more>
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

        # 26	<array_more>	→	λ
        elif token == '~':
            return True  # End of array initialization with tilde

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def array_lit(self):
        # 27	<array_lit>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        # 28	<array_lit>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        # 29	<array_lit>	→	treasures_lit
        elif self.match('treasures_lit'):
            return True
        # 30	<array_lit>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        # 31	<array_lit>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True
        # 32	<array_lit>	→	id_lit
        elif self.match('identifier'):
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def assignment_exp(self):
        # 33	<assignment_exp>	→	id_lit <assignment_operator> <assignment_operand>

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
        # 34	<assignment_operator>	→	+=
        if self.match('+='):
            return True
        # 35	<assignment_operator>	→	-=
        elif self.match('-='):
            return True
        # 36	<assignment_operator>	→	*=
        elif self.match('*='):
            return True
        # 37	<assignment_operator>	→	/=
        elif self.match('/='):
            return True
        # 38	<assignment_operator>	→	%=
        elif self.match('%='):
            return True
        
        # if naging assignment operand ang arithmetic exp based on => 43	<assignment_operand>	→	<aritmethic_exp>
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
        next_token = self.peek_next_token()
        token = self.current_token()
        start_pos = self.current_index
        #39	<assignment_operand>	→	id_lit
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
            # 42	<assignment_operand>	→	<array_element>
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
        # 40	<assignment_operand>	→	treasures_lit
        elif token == 'treasures_lit':
            if next_token in ['+', '-', '/', '*', '%']:
                if not self.arithmetic_exp():
                    return False
                return True
            else:
                return self.match('treasures_lit')
        # 41	<assignment_operand>	→	ocean_lit
        elif token == 'ocean_lit':
            if next_token in ['+', '-', '/', '*', '%']:
                if not self.arithmetic_exp():
                    return False
                return True
            else:
                return self.match('ocean_lit')
        # 43	<assignment_operand>	→	<aritmethic_exp> and yung nasa operator
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

        # di ko alam if may effect to // for testing pa if wala naman effect tanggalin
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
        # 45	<array_element>	→	id_lit <index>

        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        if not self.index():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True


    def logical_exp(self):
        # 46	<logical_exp>	→	<logical_operand> <logical_operator> <logical_operand> <more_log>
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
        
        # 47	<logical_exp>	→	<logical_operator1> <logical_operand> <more_log> 
        
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
        # 48	<logical_operand>	→	id_lit
        if token == 'identifier':
            next_token = self.peek_next_token()
            print(f"Next token after identifier: {next_token}")
            # 53	<logical_operand>	→	<func_call>
            if next_token == '(':
                if self.func_call():  # Parse the function call
                    print("Function call detected and parsed.")
                    return True
            #54	<logical_operand>	→	<array_element>
            elif next_token == '[':
                self.advance()
                if self.index():
                    print("Array element detected and parsed.")
                    return True
            else:
                return self.match('identifier')
        # 50	<logical_operand>	→	<treasures_mirror> for tokenize pa yung 1
        elif self.match('treasures_lit'):
            return True
        # 49	<logical_operand>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True

        elif self.match('0'):
            return True

        elif self.treasures_mirror():
            return True
        # 51	<logical_operand>	→	<relational_exp>
        elif self.relational_exp():
            return True
        # 52	<logical_operand>	→	(<relational_exp>)
        elif self.match('('):  
            if not self.relational_operand():
                return False
            if not (self.match('<') or self.match('>') or self.match('<=') or self.match('>=') or self.match('==') or self.match('!=')):
                return False
            if not self.relational_operand():
                return False
            if not self.relational_more():
                return False
            if not self.match(')'):
                return False
            return True
        # for checking if pwede tanggalin
        elif self.func_call():  # Function calls as logical operands
            return True

        elif self.array_element():  # Array elements as logical operands
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

  
    def logical_operator(self):
        # 55	<logical_operator>	→	&&
        if self.match('&&'):
            return True
        # 56	<logical_operator>	→	||
        elif self.match('||'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
    def logical_operator1(self):
        # 57	<logical_operator1>	→	!
        if self.match('!'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def more_log(self):
        token = self.current_token()
        # 58	<more_log>	→	<logical_operator> <more_log_ext>
        if self.logical_operator():
            print("Logical operator detected, continuing more_log_ext...")
            if not self.more_log_ext():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        # 59	<more_log>	→	λ
        elif token in [',', '~', ')']:
            print(f"End of logical expression detected: {token}")
            return True

        else:
            self.error_message = f"Syntax Error: Unexpected token {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def more_log_ext(self):
        # 60	<more_log_ext>	→	<logical_operand><more_log>
        if self.logical_operand():
            if not self.more_log():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 61	<more_log_ext>	→	<logical_operator1> <logical_operand><more_log>
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
        # 62	<func_call>	→	id_lit (<args>)
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

        # 63	<args>	→	<args_val> <args_more>
        if self.args_val():
            # Don't check args_more if we're at the end of arguments
            if token == ')':
                return True
            if not self.args_more():
                return False
            return True

        # 64	<args>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    

    def args_val(self):
        # 65	<args_val>	→	id_lit
        if self.match('identifier'):
            return True
        # 66	<args_val>	→	scroll_lit
        elif self.match('scroll_lit'):
            return True
        # 67	<args_val>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        # 68	<args_val>	→	treasures_lit
        elif self.match('treasures_lit'):
            return True
        # 69	<args_val>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        # 70	<args_val>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
    def args_more(self):
        token = self.current_token()

        # 71	<args_more>	→	, <args> <args_more>
        if token == ',':
            self.advance()
            if not self.args():
                return False
            return self.args_more()
        
        # 72	<args_more>	→	λ

        elif token in [')', '+', '-', '*', '/', '%', '~']:
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def treasures_mirror(self):
        # 73	<treasures_mirror>	→	1
        if self.match('1'):
            return True
        # 74	<treasures_mirror>	→	0
        elif self.match('0'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    

    def arithmetic_exp(self):
        token = self.current_token()
        # 75	<arithmetic_exp>	→	<arithmetic_operand> <arithmetic_operator><arithmetic_operand><more_arith>
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
        # 76	<arithmetic_operand>	→	id_lit
        if token == 'identifier':
            next_token = self.peek_next_token()
            # 81	<arithmetic_operand>	→	<func_call>
            if next_token == '(':  # If it's a function call
                if not self.func_call():  # Parse the function call
                    return False
                return True  # Successfully parsed function call as operand
            # 82	<arithmetic_operand>	→	<array_element>
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')
            
        # 77	<arithmetic_operand>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        # 78	<arithmetic_operand>	→	treasures_lit 
        elif self.match('treasures_lit'):
            return True
        elif self.match('0'):
            return True
        # 80	<arithmetic_operand>	→	(<arithmetic_exp>)
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
        # 83	<arithmetic_operator>	→	+
        if self.match('+'):
            return True
        # 84	<arithmetic_operator>	→	-
        elif self.match('-'):
            return True
        # 85	<arithmetic_operator>	→	/
        elif self.match('/'):
            return True
        # 86	<arithmetic_operator>	→	*
        elif self.match('*'):
            return True
        # 87	<arithmetic_operator>	→	%
        elif self.match('%'):
            return True
        

        # if may kahalong relational (arithmetic as relational-operand) based => 96	<relational_operand>	→	<arithmetic_exp>
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

        # 88	<more_arith>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                self.error_message = f"Syntax Error: Expected operand but got {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return self.more_arith()  # Continue parsing if there's more arithmetic

        # 89	<more_arith>	→	λ
        elif token in [')', '~', ',', '<', '>', '<=', '>=', '==', '!=']:
            return True  

        else:
            self.error_message = f"Syntax Error: Unexpected token {repr(token)} at Line {self.current_line + 1}"
            return False


    def relational_exp(self):
       # 90	<relational_exp>	→	<relational_operand> <relational_operator> <relational_operand> <relational_more>  
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
        # 91	<relational_operand>	→	id_lit
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':  # If it's a function call
                # 97	<relational_operand>	→	<func_call>
                if not self.func_call(): 
                    return False
                return True  
            # 98	<relational_operand>	→	<array_element>
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')
        # 92	<relational_operand>	→	scroll_lit
        elif self.match('scroll_lit'):
            return True
        # 93	<relational_operand>	→	treasures_lit
        elif self.match('treasures_lit'):
            return True
        
        elif self.match('0'):
            return True
        # 94	<relational_operand>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        # 95	<relational_operand>	→	(<arithmetic_exp>)
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
        # for checking if pwede tanggalin
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
        # 99	<relational_operator>	→	<
        if self.match('<'):
            return True 
        # 100	<relational_operator>	→	>
        elif self.match('>'):
            return True
        # 101	<relational_operator>	→	<=
        elif self.match('<='):
            return True
        # 102	<relational_operator>	→	>=
        elif self.match('>='):
            return True
        # 103	<relational_operator>	→	==
        elif self.match('=='):
            return True
        # 104	<relational_operator>	→	!=
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
        # 105	<relational_more>	→	<relational_operator> <relational_operand><relational_more>
        token = self.current_token()

        if self.relational_operator():
            if not self.relational_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.relational_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 106	<relational_more>	→	λ
        elif token in [')', '', '', '~', '&&', '||']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def unary(self):
        token = self.current_token()
        # 107	<unary>	→	id_lit <unary_operator>
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
        # 108	<unary_operator>	→	++
        if self.match('++'):
            return True
        # 109	<unary_operator>	→	--
        elif self.match('--'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def concat(self):
        # 110	<concat>	→	<string_operand> + <string_operand> <string_more>
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
        # 112	<string_operand>	→	id_lit
        if token == 'identifier':
            next_token = self.peek_next_token()
            # 115	<string_operand>	→	<func_call>
            if next_token == '(':  # If it's a function call
                if not self.func_call():  # Parse the function call
                    return False
                return True  # Successfully parsed function call as operand
            # 114	<string_operand>	→	<array_element>
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match('identifier')
        # 111	<string_operand>	→	scroll_lit
        elif self.match('scroll_lit'):
            return True
        # 113	<string_operand>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        elif self.array_element():
            return True
        # 116	<string_operand>	→	toscroll(<conver_value>)
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
        # 117	<string_more>	→	+ <string_operand> <string_more>
        if self.match('+'):
            if not self.string_operand():
                return False
            return self.string_more()
        # 118	<string_more>	→	λ
        return True  # Can be empty (λ)


    def user_defined_func(self):

        token = self.current_token()

        # 119	<user-defined_func>	→	spell <return_type> id_lit(<param>) {<body><ret_statement>} <user-defined_func>
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

        # 120	<user-defined_func>	→	λ
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'comment', 'continue', '}', 'return', 'break', 'castle']:
            return True
        
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def return_type(self):
        # 121	<return_type>	→	<data_type>
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
        # 122	<return_type>	→	chamber
        elif self.match('chamber'):
            return True
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def param(self):
        token = self.current_token()
        
        # 123	<param>	→	<data_type> id_lit <param_more>
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

        # 124	<param>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def param_more(self):
        token = self.current_token()

        # 125	<param_more>	→	, <data_type> id_lit <param_more>
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

        # 126	<param_more>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def body(self):
        token = self.current_token()
        next_token = self.peek_next_token()

        # 137	<body>	→	λ
        if token in ['return', '}', 'break', 'continue']:
            return True  # Successfully ended parsing

        elif token == 'identifier':
            # 133	<body>	→	<var_reassign><body>
            if next_token == '=':
                if not self.var_reassign():
                    return False
                return self.body()
            # 134	<body>	→	<unary>~ <body>
            elif next_token in ['++', '--']:
                if not self.unary():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
            # 135	<body>	→	<assignment_exp>~ <body>
            elif next_token in ['+=', '-=', '*=', '/=', '%=']:
                if not self.assignment_exp():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
            # 129	<body>	→	<func_call>~ <body>
            elif next_token == '(':
                if not self.func_call():
                    return False
                if not self.match('~'):
                    return False
                return self.body()
        # 127	<body>	→	<var_dec> <body>
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'rose', 'ocean']:
            if not self.var_dec():
                return False
            return self.body()
        # 131	<body>	→	<condi_statement> <body>
        elif token in ['believe', 'forever', 'cast']:
            if not self.condi_statement():
                return False
            return self.body()
        # 128	<body>	→	<output> <body>
        elif token == 'granted':
            if not self.output():
                return False
            return self.body()
        # 130	<body>	→	<user-defined_func> <body>
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.body()
        # 132	<body>	→	<for_loop> <body>
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.body()
        # 136	<body>	→	<comments> <body>
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
            # 141	<ret_statement>	→	return <val1> ~
            if not self.val1():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print('val1')
            # 142	<ret_statement>	→	λ
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
        # 143	<var_reassign>	→	id_lit = <val> ~
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
    
    def condi_statement(self):
        token = self.current_token()
        # 144	<condi_statement>	→	<if>
        if token == 'cast':
            return self.if_statement()

        # 145	<condi_statement>	→	<while>
        elif token == 'forever':
            return self.while_statement()

        # 146	<condi_statement>	→	<do_while>
        elif token == 'believe':
            return self.do_while_statement()
        
        else:
            return False
    
    def for_loop(self):
        # 147	<for_loop>	→	tale (<loop_var> ~ <relational_exp> ~ <unary>) {<loop_body>}
        if not self.match('tale'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.loop_var():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.relational_exp():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.unary():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('{'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.loop_body():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('}'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True

    def loop_var(self):
        # 148	<loop_var>	→	treasures id_lit = <loop_val>
        if self.match('treasures'):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('='):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.loop_val():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 149	<loop_var>	→	id_lit <loop_init>
        elif self.match('identifier'):
            if not self.loop_init():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
    
    def loop_init(self):
        token = self.current_token()

        # 150	<loop_init>	→	=  <loop_val>
        if self.match('='):
            if not self.loop_val():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 151	<loop_init>	→	λ
        elif token == '~':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def loop_val(self):
        # 152	<loop_val>	→	id_lit
        if self.match('identifier'):
            return True
        # 153	<loop_val>	→	treasures_lit
        elif self.match('treasures_lit'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def loop_body(self):
        token = self.current_token()
        next_token = self.peek_next_token()     
        # 154	<loop_body>	→	<body>
        if token is None:
            return True  # No more tokens, end successfully

        if token in ['return', '}', 'break', 'continue']:
            return True

        elif token == 'identifier':
            if next_token is None:
                return False  # Prevent index errors

            if next_token == '=':
                if not self.var_reassign():
                    return False
                return self.loop_body()
            elif next_token in ['++', '--']:
                if not self.unary():
                    return False
                if not self.match('~'):
                    return False
                return self.loop_body()
            elif next_token in ['+=', '-=', '*=', '/=', '%=']:
                if not self.assignment_exp():
                    return False
                if not self.match('~'):
                    return False
                return self.loop_body()
            elif next_token == '(':
                if not self.func_call():
                    return False
                if not self.match('~'):
                    return False
                return self.loop_body()

        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'rose', 'ocean']:
            if not self.var_dec():
                return False
            return self.loop_body()

        elif token in ['believe', 'forever']:
            if not self.condi_statement():
                return False
            return self.loop_body()
        # 155	<loop_body>	→	<if_break>
        elif token == 'cast':
            if not self.if_break():
                return False
            return self.loop_body()

        elif token == 'granted':
            if not self.output():
                return False
            return self.loop_body()

        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.loop_body()

        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.loop_body()

        elif token in ["single_comment", "multi_comment"]:
            return self.loop_body()

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
    def if_break(self):
        # 156	<if_break>	→	cast (<condition>) {<body><flow_control>} <elif_break> <else_break>
        if not self.match('cast'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.condition():
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
        if not self.flow_control():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('}'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.elif_break():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.else_break():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def elif_break(self):
        token = self.current_token()

        # 157	<elif_break>	→	twist(<condition>) {<body><flow_control>}<elif_break>
        if self.match('twist'):
            if not self.match('('):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.condition():
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
            if not self.flow_control():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.elif_break():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 158	<elif_break>	→	λ
        elif token in ['curse', '}']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    
    def else_break(self):
        token = self.current_token()

        # 159	<else_break>	→	curse {<body><flow_control>}
        if self.match('curse'):
            if not self.match('{'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.flow_control():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 160	<else_break>	→	λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def flow_control(self):
        token = self.current_token()

        # 161	<flow_control>	→	break~
        if self.match('break'):
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        # 162	<flow_control>	→	continue~
        elif self.match('continue'):
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        # 163	<flow_control>	→	λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def do_while_statement(self):
        # 164	<do_while>	→	believe {<loop_body>} forever(<condition>)~
        if not self.match('believe'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('{'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.loop_body():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('}'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('forever'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.condition():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def condition(self):

        # if self.treasures_mirror():
        #     return True
        token = self.current_token()
        next_token = self.peek_next_token()
        # 166	<condition>	→	id_lit <mirror_init>
        if token == 'identifier':
            if next_token == '(':  # Function call
                start_pos = self.current_index  # Save starting position
                # <condition>	→	<func_call>
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    # 167	<condition>	→	<relational_exp>
                    if next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # <condition>	→	<logical_exp>
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
                    # 167	<condition>	→	<relational_exp>
                    if next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # <condition>	→	<logical_exp>
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)
        # 165	<condition>	→	<treasures_mirror>
        elif self.match('mirror_lit'):
            return True
        elif self.relational_exp():
            return True
        elif self.logical_exp():
            return True
        # <condition>	→	<logical_operator1> (<condition>)
        elif self.match('!'):
            print(f"Current Token: {self.current_token()}, Next Token: {self.peek_next_token()}")
            if not self.match('('):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.condition():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        elif self.func_call():
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def mirror_init(self):
        token = self.current_token()

        # 171	<mirror_init>	→	== mirror_lit
        if self.match('=='):
            if not(self.match('mirror_lit') or self.match('0'), self.match('treasures_lit')):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 172	<mirror_init>	→	!= mirror_lit
        elif self.match('!='):
            if not(self.match('mirror_lit') or self.match('0'), self.match('treasures_lit')):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        # 173	<mirror_init>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def while_statement(self):
        # 174	<while>	→	forever (<condition>) {<loop_body>}
        token = self.current_token()
        if not self.match('forever'):
            self.error_message = f"Syntax Error: Expected forever, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        print(f"passed forever {token}")
        if not self.match('('):
            self.error_message = f"Syntax Error: Expected ((, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        print(f"passed ( {token}")
        if not self.condition():
            return False
        print(f"passed condition {token}")
        if not self.match(')'):
            self.error_message = f"Syntax Error: Expected )), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        print(f"passed ) {token}")
        if not self.match('{'):
            self.error_message = f"Syntax Error: Expected {{, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        print(f"passed open curly {token}")
        if not self.loop_body():
            return False
        print(f"passed loop body {token}")
            
        if not self.match('}'):
            self.error_message = f"Syntax Error: Expected }}, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        print(f"passed close curly {token}")
        return True
        
    
    def if_statement(self):
        # 175	<if>	→	cast (<condition>) {<body>} <elif> <else>
        if not self.match('cast'):
            self.error_message = f"Syntax Error: Expected cast, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Expected (, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.condition():
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Expected ), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('{'):
            self.error_message = f"Syntax Error: Expected {{, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.body():
            return False
        if not self.match('}'):
            self.error_message = f"Syntax Error: Expected }}, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.elif_statement():
            return False
        if not self.else_statement():
            return False
        return True
    
    def elif_statement(self):
        token = self.current_token()

        # 176	<elif>	→	twist(<condition>) {<body>}<elif>
        if self.match('twist'):
            if not self.match('('):
                self.error_message = f"Syntax Error: Expected (, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Expected ), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.match('{'):
                self.error_message = f"Syntax Error: Expected {{, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.body():
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Expected }}, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.elif_statement():
                return False
            return True

        # 177	<elif>	→	λ
        elif token in ['curse', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', '?']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def else_statement(self):
        token = self.current_token()

        # 178	<else>	→	curse {<body>}
        if self.match('curse'):
            if not self.match('{'):
                self.error_message = f"Syntax Error: Expected {{, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.body():
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Expected }}, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            return True
        
        # 179	<else>	→	λ
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'comment', 'return', 'break', 'continue']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def output(self):
        # 180	<output>	→	granted(<granted_content> <more_granted>) ~
        if not self.match('granted'):
            self.error_message = f"Syntax Error: Expected granted, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Expected (, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.granted_content():
            return False
        if not self.more_granted():
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Expected ), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('~'):
            self.error_message = f"Syntax Error: Expected ~, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        return True
    

    def granted_content(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        # 181	<granted_content>	→	id_lit
        if token == 'identifier':
            # 196	<granted_content>	→	<func_call>
            if next_token == '(':  # Function call
                start_pos = self.current_index  # Save starting position
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    # 194	<granted_content>	→	<arithmetic_exp>
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    # 191	<granted_content>	→	<relational_exp>
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # 192	<granted_content>	→	<logical_exp>
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            # 195	<granted_content>	→	<array_element>
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    # 194	<granted_content>	→	<arithmetic_exp>
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    # 191	<granted_content>	→	<relational_exp>
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # 192	<granted_content>	→	<logical_exp>
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            # 194	<granted_content>	→	<arithmetic_exp>
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            # 193	<granted_content>	→	<unary>
            elif next_token in ['++', '--']:
                return self.unary()
            else:
                return self.match(token)
        # 183	<granted_content>	→	rose_lit
        elif token == 'rose_lit':
            if next_token == '+':
                return self.concat()
            return self.match(token)
        # 187	<granted_content>	→	phantom
        elif token == 'phantom':
            return self.match(token)
        
        elif token == '!':
            return self.logical_exp()
        # 182	<granted_content>	→	scroll_lit and 188	<granted_content>	→	<set_precision>
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()
            # 190	<granted_content>	→	<concat>
            if next_token == '+':
                return self.concat()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        # 184	<granted_content>	→	treasures_lit
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
        # 185	<granted_content>	→	ocean_lit
        elif token == 'ocean_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        # 186	<granted_content>	→	mirror_lit
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
        # 189	<granted_content>	→	<type_conversion>
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
        # 197	<set_precision>	→	“%.[treasures_lit]f”
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

        # 198	<more_granted>	→	, <granted_content> <more_granted>
        if self.match(','):
            if not self.granted_content():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.more_granted():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # 199	<more_granted>	→	λ
        elif token == ')':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False


    def data_type(self):
        token = self.current_token()
        # 200	<data_type>	→	scroll
        # 201	<data_type>	→	treasures
        # 202	<data_type>	→	mirror
        # 203	<data_type>	→	ocean
        # 204	<data_type>	→	rose
        if token in {'scroll', 'treasures', 'mirror', 'ocean', 'rose'}:
            # self.advance()  # Consume the data_type token
            return True
        self.error_message = f"Syntax Error: Expected wish, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
        return False


    def val(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        # 210	<val>	→	id_lit
        if token == 'identifier':
            # 219	<val>	→	<func_call>
            if next_token == '(':  # Function call
                start_pos = self.current_index  # Save starting position
                if self.func_call():  # Parse initial function call
                    next_after_func = self.current_token()
                    # 213	<val>	→	<arithmetic_exp>
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    # 216	<val>	→	<relational_exp>
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # 217	<val>	→	<logical_exp>
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            # 220	<val>	→	<array_element>
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    # 213	<val>	→	<arithmetic_exp>
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:  # If followed by arithmetic operator
                        self.current_index = start_pos  # Reset back to identifier
                        return self.arithmetic_exp()  # Let arithmetic_exp handle from identifier onwards
                    # 216	<val>	→	<relational_exp>
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    # 217	<val>	→	<logical_exp>
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                return False
            # 213	<val>	→	<arithmetic_exp>
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            # 216	<val>	→	<relational_exp>
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            # 217	<val>	→	<logical_exp>
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)
        # 209	<val>	→	rose_lit
        elif token == 'rose_lit':
            if next_token == '+':
                return self.concat()
            return self.match(token)
        # 211	<val>	→	phantom
        elif token == 'phantom':
            return self.match(token)
        
        elif token == '!':
            return self.logical_exp()
        # 205	<val>	→	scroll_lit
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()
            # 212	<val>	→	<concat>
            if next_token == '+':
                return self.concat()
            # 216	<val>	→	<relational_exp>
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        # 206	<val>	→	treasures_lit
        elif token == 'treasures_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            # 216	<val>	→	<relational_exp>
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        # 208	<val>	→	ocean_lit
        elif token == 'ocean_lit':
            next_token = self.peek_next_token()
            if next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            # 216	<val>	→	<relational_exp>
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            else:
                return self.match(token)
        # 207	<val>	→	mirror_lit
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
                # 216	<val>	→	<relational_exp>
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
        # 215	<val>	→	<type_conversion>
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

        # 214	<val>	→	<input>        
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
        # 221	<val1>	→	<val>
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
            # 223	<val1>	→	<assignment_exp>
            elif next_token in ['+=', '-=', '/=', '*=', '%=']:
                return self.assignment_exp()
            # 222	<val1>	→	<unary>
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
        # 224	<type_conversion>	→	<conversion_func> (<conversion_value>)
        if not self.conversion_func():
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Expected (, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.conversion_value():
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Expected ), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        return True
    
    def conversion_func(self):
        # 225	<conversion_func>	→	toscroll
        if self.match('toscroll'):
            return True
        # 227	<conversion_func>	→	totreasures
        elif self.match('totreasures'):
            return True
        # elif self.match('tomirror'):
        #     return True
        # 228	<conversion_func>	→	toocean
        elif self.match('toocean'):
            return True
        # 226	<conversion_func>	→	torose
        elif self.match('torose'):
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def conversion_value(self):
        # 229	<conversion_value>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        # 230	<conversion_value>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        # 231	<conversion_value>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        # 232	<conversion_value>	→	treasures_lit
        elif self.match('treasures_lit'):
            return True
        # 233	<conversion_value>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True
        # 234	<conversion_value>	→	id_lit <index>
        elif self.match('identifier'):
            if not self.index():
                return False
            return True
        # 235	<conversion_value>	→	<func_call>
        elif self.func_call():
            return True
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def index(self):
        token = self.current_token()

        # 236	<index>	→	[treasures_lit] <column1>
        if self.match('['):
            if not self.match('treasures_lit'):
                self.error_message = f"Syntax Error: Expected treasures literals, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.match(']'):
                self.error_message = f"Syntax Error: Expected ], but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            print("index-done")
            if not self.column1():
                return False
            print("column1")
            return True

        # 237	<index>	→	λ
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
            

    def column1(self): 
        token = self.current_token()

        # 238	<column1>	→	[treasures_lit]
        if self.match('['):
            if not self.match('treasures_lit'):
                self.error_message = f"Syntax Error: Expected treasures literals, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            if not self.match(']'):
                self.error_message = f"Syntax Error: Expected ], but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
                return False
            return True

        # 239	<column1>	→	λ
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{' ]:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        
    def input(self):
        # 240	<input>	→	wish (scroll_lit)
        if not self.match('wish'):
            self.error_message = f"Syntax Error: Expected wish, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('('):
            self.error_message = f"Syntax Error: Expected (, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match('scroll_lit'):
            self.error_message = f"Syntax Error: Expected scroll literals, but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
            return False
        if not self.match(')'):
            self.error_message = f"Syntax Error: Expected ), but got {repr(self.current_token())} at Line {self.current_line + 1}, Index {self.current_index}"
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
    