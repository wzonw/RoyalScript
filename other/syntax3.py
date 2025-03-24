from other.lexer import RoyalScriptLexer, Token
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
                token = self.tokens[self.current_line][self.current_index]
                return token  # No need for extra None check
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
        temp_line, temp_index = self.current_line, self.current_index  # Save current state

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
            self.error_message = f"Syntax Error: Unexpected end of input at Line {self.current_line}"
        else:
            self.error_message = f"Syntax Error: Expected {expected}, but got {repr(token)} at Line {self.current_line}, Index {self.current_index}"
        
        return False

    
    # def peek(self):
    #     """Look ahead at next token without consuming it"""
    #     saved_line = self.current_line
    #     saved_index = self.current_index
    #     token = self.current_token()
    #     self.current_line = saved_line
    #     self.current_index = saved_index
    #     return token
    
    def program(self):
        self.error_message = "" 
        # <program>: crown~ <global_dec> <user-defined_func> castle treasures identifier() {<body> return 0~} reign~

        # Check crown~
        if not self.match("crown"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("~"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False 
            
        # Parse global declarations
        if not self.global_dec():
            return False
            
        # Parse user-defined functions
        # if not self.user_defined_func():
        #     self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
        #     return False
            
        # Parse main function
        if not self.match("castle"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("treasures"):
            self.error_message = f"Syntax Error: Invalid input>> {repr(self.current_token())} at Line {self.current_line}"
            return False
        if not self.match("identifier"):
            self.error_message = f"Syntax Error: Invalid input// {repr(self.current_token())} at Line {self.current_line}"
            return False
        if not self.match("("):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match(")"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("{"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        # if not self.body():
        #     self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
        #     return False
        if not self.match("return"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("0"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("~"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("}"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
            
        # Check reign~
        if not self.match("reign"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match("~"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.match("EOF"):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        return True
    
    def global_dec(self):
            if self.var_dec():
                return self.global_dec()

            token = self.current_token()

            if token in ['castle', 'spell']: 
                return True  

            # self.error_message = f"Syntax Error: Unexpected token>> {repr(token)} at Line {self.current_line + 1}"
            return False  

                                                                            
    def var_dec(self):

        #<var_dec>: <dynasty> <data_type> identifier <vardec_def>
        if not self.dynasty():
            return False
        
        if not self.data_type():
            return False
        
        self.advance()
        
        if not self.match('identifier'):
            return False
        
        if not self.vardec_def():
            return False
        
        return True
                
    
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
        print(f"Current Token before initialization: {repr(self.current_token())}")
        print("=== Entering vardec_def ===")
        traceback.print_stack()  # This will show where the function is being called from
        print(f"Current Token before initialization: {repr(self.current_token())}")

        if self.initialization():
            print("Initialization passed")
            
            if not self.vardec_more():
                self.error_message = f"Syntax Error: Expected more variable declaration but got {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            print("Vardec More passed")

            print(f"Token before matching '~': {repr(self.current_token())}")  
            if not self.match("~"):
                self.error_message = f"Syntax Error: Expected '~' but got {repr(self.current_token())} at Line {self.current_line + 1}"
                return False

            print("Parsing successful!")
            return True  # This ensures the function does not continue!


        # print("Initialization failed, checking for array declaration")

        elif self.match('['):
            print("Array declaration detected")
            if not self.match('pos_treasures_lit'):
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
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        else:
            print("No valid match in vardec_def")
            return False


    def initialization(self):
        token = self.current_token()

        # <initialization>: = <val>
        if self.match('='):  
            # self.advance()  
            if not self.val():  
                self.error_message = f"Syntax Error: Expected value after '=' at Line {self.current_line + 1}"
                return False
            return True  
            
        #<initialization>: λ
        elif token in ['~', ',']:
            return True  # pag nag null next na ay ~ or , agad

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        
    def vardec_more(self):
        #<vardec_more>: , identifier <initialization> <vardec_more>
        token = self.current_token()

        if self.match(','):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.initialization():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return self.vardec_more()
            # if not self.vardec_more():
            #     self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            #     return False
            # return True
    
        #<vardec_more>: λ
        elif token == '~':
            return True # pag nag null next na ay ~ agad
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def column(self):
        #<column>: [num]

        token = self.current_token()

        if token == '[':
            self.advance()
            token = self.current_token()
            if token == 'pos_treasures_lit':
                self.advance()
                token = self.current_token()
            if token == ']':
                self.advance()
                return True
        
        #<column>: λ
        elif token in ['=', ',', '~']:
            return True # pag nag null next na agad ay =, , , ~ ##para magcontinue??
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    
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
        #<array_list>: {<array_content>}

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
        #<array_content>: <array_lit> <lit_more>

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
        #<array_row>: <array_lit> <lit_more>

        if not self.array_lit():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.lit_more():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True
    
    def row_more(self):
        #<row_more>: , {array_row} <row_more>
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
        
        #<row_more>: λ
        elif token == '}':
            return True #if walang row more ang susunod na is } since icoclose na yung array
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def lit_more(self):
        #<lit_more>: , <array_lit> <lit_more>
        token = self.current_token()

        if not self.match(','):    
            if not self.array_lit():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.lit_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<lit_more>: λ
        elif token == '}':
            return True #if walang row more ang susunod na is } since icoclose na yung array
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def array_more(self):
        #<array_more>: , identifier [num] <column> <array_initialization> <array_more>
        token = self.current_token()

        if not self.match(','):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('['):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('pos_treasures_lit'):
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
        
        #<array_more>: λ
        elif token == '~':
            return True #pagnagnull tilde na agad next
        
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

        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.assignment_operator():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.assignment_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True
    

    def assignment_operator(self):
        
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

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def assignment_operand(self):
        
        if self.match('identifier'):
            return True

        elif self.match('treasures_lit'):
            return True

        elif self.match('ocean_lit'):
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
        #<array_element>: identifier <index>

        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        if not self.index():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
        return True
    
    def logical_exp(self):
        #<logical_exp>: <logical_operand> <logical_operator> <logical_operand> <more_log>
            
        if self.logical_operand():
            if not self.logical_operator():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
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

        if self.match('identifier'):
            return True

        elif self.match('mirror_lit'):
            return True

        elif self.treasures_mirror():
            return True

        elif self.relational_exp():
            return True

        elif self.match('('):
            if not self.relational_exp():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        elif self.func_call():
            return True

        elif self.array_element():
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
        #<more_log>: <logical_operator> <more_log_ext>
        token = self.current_token()

        if self.logical_operator():
            if not self.more_log_ext():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True


        #<more_log>: λ
        elif token in [',', '~' , ')']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
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
        #<func_call>: identifier (<args>)

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
        
        return True
    

    def args(self):
        token = self.current_token()

        #<args>: <args_val> <args_more>
        if self.args_val():
           if not self.args_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
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
        #<args_more>: , <args> <args_more>
        token = self.current_token()

        if self.match(','):
            if not self.args():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.args_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<args_more>: λ
        elif token == ')':
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

        if self.match('identifier'):
            return True

        elif self.match('ocean_lit'):
            return True

        elif self.match('treasures_lit'):
            return True

        elif self.arithmetic_exp():
            return True

        elif self.match('('):
            if not self.arithmetic_exp():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        elif self.func_call():
            return True

        elif self.array_element():
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
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
        #<more_arith>: <arithmetic_operator> <arithmetic_operand> <more_arith>
        token = self.current_token()

        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.more_arith():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<more_arith>: λ
        elif token in ['+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '~', ',']:
            return True

        else: 
            return True

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

        if self.match('identifier'):
            return True

        elif self.match('scroll_lit'):
            return True

        elif self.match('treasures_lit'):
            return True

        elif self.match('ocean_lit'):
            return True

        elif self.match('('):
            if not self.arithmetic_exp():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
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
        token = self.current_token()

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
        #<unary>: identifier <unary_operator>
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
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
        #<concat>: <string_operand> + <string_operand> <string_more>
        if not self.string_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.match('+'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not self.string_operand():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if not not self.string_more():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def string_operand(self):

        if self.match('scroll_lit'):
            return True

        elif self.match('identifier'):
            return True

        elif self.match('rose_lit'):
            return True

        elif self.array_element():
            return True

        elif self.match('tooscroll'):
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

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def string_more(self):
        #<string_more>: + <string_operand> <string_more>
        token = self.current_token()

        if self.match('+'):
            if not self.string_operand():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.string_more():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<string_more>: λ
        elif token in ['', '', '~', ')']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
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
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'comment', 'continue', '}', 'return', 'break']:
            return True

        elif self.match('castle'):
            return True
        

        elif self.match('scroll'):
            return True
        
        elif self.match('treasures'):
            return True
        
        elif self.match('mirror'):
            return True
        
        elif self.match('ocean'):
            return True
        
        elif self.match('rose'):
            return True
        
        elif self.match('dynasty'):
            return True
        
        elif self.match('treasures'):
            return True
        
        elif self.match('granted'):
            return True
        
        elif self.match('identifier'):
            return True

        elif self.match('spell'):
            return True

        elif self.match('cast'):
            return True
        
        elif self.match('forever'):
            return True
        
        elif self.match('believe'):
            return True
        
        elif self.match('tale'):
            return True
        
        elif self.match('comment'):
            return True
        
        elif self.match('continue'):
            return True
        
        elif self.match('}'):
            return True
        
        elif self.match('return'):
            return True
        
        elif self.match('break'):
            return True
        
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def return_type(self):

        if self.data_type():
            return True
        elif self.match('chamber'):
            return True
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def param(self):
        token = self.current_token()
        
        #<param>: <data_type> identifier <param_more>
        if self.data_type():
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

        #<body>: <var_dec> <body>
        if self.var_dec():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <output> <body>
        elif self.output():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <func_call>~ <body>
        elif self.func_call():
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            elif not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <user-defined_func> <body>
        elif self.user_defined_func():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <condi_statement> <body>
        elif self.condi_statement():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <for_loop> <body>
        elif self.for_loop():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <var_reassign><body>
        elif self.var_reassign():
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <unary>~ <body>
        elif self.unary():
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            elif not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <assignment_exp>~ <body>
        elif self.assignment_exp():
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            elif not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<body>: <comments> <body>
        # elif self.comments():
        #     if not self.body():
        #         self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            # return False
        #     return True

        #<body>: λ
        elif token == 'return':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    
    def ret_statement(self):
        token = self.current_token()

        #<ret_statement>: return <val1> ~
        if self.match('return'):
            if not self.val1():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
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
    
    def condi_statement(self):
        #<condi_statement>: <if>
        if self.if_statement():
            return True

        #<condi_statement>: <while>
        elif self.while_statement():
            return True

        #<condi_statement>: <do_while>
        elif self.do_while_statement():
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def for_loop(self):
        #<for_loop>: tale (<loop_var> ~ <relational_exp> ~ <unary>) {<loop_body>}
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
        #<loop_var>: treasures identifier = <loop_val>
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

        # <loop_var>: identifier <loop_init>
        elif self.match('identifier'):
            if not self.loop_init():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
    
    def loop_init(self):
        token = self.current_token()

        #<loop_init>: =  <loop_val>
        if self.match('='):
            if not self.loop_val():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        # <loop_init>: λ
        elif token == '~':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def loop_val(self):

        if self.match('identifier'):
            return True

        elif self.match('treasures_lit'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

        
    def loop_body(self):
        if self.body():
            return True
        elif self.if_break():
            return True
        else: 
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    def if_break(self):
        #<if_break>: cast (<condition>) {<body><flow_control>} <elif_break> <else_break>
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

        #<elif_break>: twist(<condition>) {<body><flow_control>}<elif_break>
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

        #<elif_break>: λ
        elif token in ['curse', '}']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
    
    def else_break(self):
        token = self.current_token()

        #<else_break>: curse {<body><flow_control>}
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

        #<else_break>: λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def flow_control(self):
        token = self.current_token()

        #<flow_control>: break~
        if self.match('break'):
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<flow_control>: continue~
        elif self.match('continue'):
            if not self.match('~'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<flow_control>: λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def do_while_statement(self):
        #<do_while>: believe {<loop_body>} forever(<condition>)~
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

        if self.treasures_mirror():
            return True
        elif self.match('identifier'):
            if not self.mirror_init():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
            return True
        elif self.relational_exp():
            return True
        elif self.logical_exp():
            return True
        elif self.logical_operator1():
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

        #<mirror_init>: == mirror_lit
        if self.match('=='):
            if not self.mirror_lit():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<mirror_init>: != mirror_lit
        elif self.match('!='):
            if not self.mirror_lit():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<mirror_init>: λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
    
    def while_statement(self):
        # <while>: forever (<condition>) {<loop_body>}
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
    
    def if_statement(self):
        #<if>: cast (<condition>) {<body>} <elif> <else>
        if self.match('cast'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.match('('):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.condition():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.match(')'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.match('{'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.body():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.match('}'):
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.elif_statement():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        if self.else_statement():
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        return True
    
    def elif_statement(self):
        token = self.current_token()

        #<elif>: twist(<condition>) {<body>}<elif>
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
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.elif_statement():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True

        #<elif>: λ
        elif token in ['curse', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', '?']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False

    def else_statement(self):
        token = self.current_token()

        #<else>: curse {<body>}
        if self.match('curse'):
            if not self.match('{'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
            return True
        
        #<else>: λ
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'comment', 'return', 'break', 'continue']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
            return False
        
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
        elif self.match('phantom'):
            return True
        elif self.set_precision():
            return True
        elif self.type_conversion():
            return True
        elif self.concat():
            return True
        elif self.relational_exp():
            return True
        elif self.logical_exp():
            return True
        elif self.unary():
            return True
        elif self.arithmetic_exp():
            return True
        elif self.array_element():
            return True
        elif self.func_call():
            return True
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

        if token in {'treasures_lit', 'mirror_lit', 'ocean_lit', 'rose_lit', 'identifier', 'phantom'}:
            return self.match(token)
        
        elif token == 'scroll_lit':
            next_token = self.peek_next_token()

            if next_token == '+':
                return self.concat()
            else:
                return self.match(token)
        
        
        elif token == 'wish':  # Check if it's an input function
            return self.input()  # Call input() only once

        elif self.concat():
            return True
        elif self.arithmetic_exp():
            return True
        elif self.type_conversion():
            return True
        elif self.relational_exp():
            return True
        elif self.logical_exp():
            return True
        elif self.treasures_mirror():
            return True
        elif self.func_call():
            return True
        elif self.array_element():
            return True

    # Base Case: Stop recursion when no match is found
        self.error_message = f"Syntax Error: Invalid input {repr(token)} at Line {self.current_line + 1}"
        return False

        
    def val1(self):
        if self.val():
            return True
        elif self.unary():
            return True
        elif self.assignment_exp():
            return True
    
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
            if not self.column1():
                self.error_message = f"Syntax Error: Invalid input {repr(self.current_token())} at Line {self.current_line + 1}"
                return False
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
            if self.match(']'):
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