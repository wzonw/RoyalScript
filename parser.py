from other.lexer import RoyalScriptLexer, Token
from RS_RegDef import Delims, RegDef
import traceback    

class RoyalScriptParser:
    def __init__(self, tokens):
        """Initialize with tokens and syntax rules."""
        self.tokens = tokens  # List of token tuples for each line: each token is (token_type, token_value)
        self.current_line = 0  # Current line index
        self.current_index = 0  # Current token index in current line
        self.error_message = ""
        self.parsing_result = ""  # Parsing output

    def current_token(self):
        """Return the current token type in the current line, skipping empty tokens."""
        while self.current_line < len(self.tokens):
            if self.tokens[self.current_line]:  # Ensure line is not empty
                if self.current_index < len(self.tokens[self.current_line]):
                    # Return ONLY the token type, not the whole tuple
                    return self.tokens[self.current_line][self.current_index][0]  # token_type
            self.current_line += 1
            self.current_index = 0
        return None

    def advance(self):
        """Move to the next token, automatically skipping comments and empty lines."""
        original_line = self.current_line  # Track the original starting line
        
        while True:
            if self.current_index + 1 < len(self.tokens[self.current_line]):
                self.current_index += 1
            elif self.current_line + 1 < len(self.tokens):
                self.current_line += 1
                self.current_index = 0
                
                # Count non-empty lines to get the "true" line number
                true_line = sum(1 for line in self.tokens[:self.current_line] if line)
            else:
                return None  # End of tokens

            # Automatically skip comments
            if self.current_token() not in ["single_comment", "multi_comment"]:
                break

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
        """Match the current token type against the expected value while ignoring comments."""
        # Skip comment tokens first
        while self.current_token() in ["single_comment", "multi_comment"]:
            self.advance()
        token = self.current_token()
        if token == expected:
            self.advance()
            return True
        # If no token or token does not match, prepare an error message.
        full_token = self.current_token()
        if token is None:
            self.error_message = f"Syntax Error: Unexpected end of input at Line {self.current_line + 1}"
        else:
            if expected == 'crown':
                self.error_message = f"Syntax Error: Program must start with 'crown'"
            elif expected == '~':
                self.error_message = f"Syntax Error: Missing tilde '~' at Line {self.current_line}, Index {self.current_index + 1}"
            elif expected == 'castle':
                self.error_message = f"Syntax Error: Program must have a main function starting with 'castle'"
            elif expected == 'treasures':
                self.error_message = f"Syntax Error: Expected treasures, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'identifier':
                self.error_message = f"Syntax Error: Missing identifier at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == '(':
                self.error_message = f"Syntax Error: Expected (, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == ')':
                self.error_message = f"Syntax Error: Unclosed ( at Line {self.current_line}, Index {self.current_index + 1}"
            elif expected == '{':
                self.error_message = f"Syntax Error: Expected {{, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == '}':
                self.error_message = f"Syntax Error: Unclosed {{ at Line {self.current_line}, Index {self.current_index + 1}"
            elif expected == ']':
                self.error_message = f"Syntax Error: Unclosed ] at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'return':
                self.error_message = f"Syntax Error: Missing return statement at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == '0':
                self.error_message = f"Syntax Error: Expected 0, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'reign':
                self.error_message = f"Syntax Error: Program must end with 'reign'"
            elif expected == 'EOF':
                self.error_message = f"Syntax error: extraneous input after reign "
            elif expected == 'scroll_lit':
                self.error_message = f"Syntax Error: Expected scroll literal, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected in ['treasures_lit', '1', '0']:
                self.error_message = f"Syntax Error: Expected treasures literal, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif self.error_message == None:
                self.error_message = f"Syntax Error: Expected {expected}, but got '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False

    def program(self):
        """Main program parser."""
        # 1	<program>	→	crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~

        self.error_message = ""
        # Skip comments at the beginning
        while self.current_token() in ["single_comment", "multi_comment"]:
            self.advance()

        if not self.match("crown") or not self.match("~"):
            return False
        
      
        if not self.global_dec():
            return False
      
    
        if not self.user_defined_func():
            return False
    
        
         # Skip comments at the beginning
        while self.current_token() in ["single_comment", "multi_comment"]:
            self.advance()

        if not self.match("castle"):
            return False
        print('matchec castle --------------', self.current_token())
        if not self.match("treasures"):
            return False
        print('matchec treasures --------------', self.current_token())
        if not self.match("identifier"):
            return False
        print('matchec identifier --------------', self.current_token())
        if not self.match("(") or not self.match(")"):
            return False
        print('matchec () --------------', self.current_token())
        if not self.match("{"):
            return False
        print('matchec { --------------', self.current_token())
        token = self.current_token()
        if not self.body():
            return False
        print('matchec body --------------', self.current_token())
        if not self.match("return") or not self.match("0") or not self.match("~") or not self.match("}"):
            return False
        print('matchec return --------------', self.current_token())
        if not self.match("reign") or not self.match("~"):
            return False
        
        return self.match("EOF")  # Ensure the end of the file is reached

    def global_dec(self):
        token = self.current_token()
        #2	<global_dec>	→	<var_dec> <global_dec>
        if token in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
            if not self.var_dec():
                return False
            return self.global_dec()
        
        elif token in ['castle', 'spell', 'EOF']:
            return True
        
        raise SyntaxError(f"Syntax Error: Invalid input '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
        

    def var_dec(self):
        # 4	<var_dec>	→	<dynasty> <data_type> id_lit <vardec_def>
        if not self.dynasty():
    
            return False
        
        if not self.data_type():
            self.error_message = f"Syntax Error: Missing data type at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        self.advance()

        if not self.match('identifier'):
            return False
        
        if not self.vardec_def():
            return False
        
        return True

    def dynasty(self):
        token = self.current_token()
        print('enter dynasty --------------------', self.current_token())
        # 5	<dynasty>	→	dynasty
        if self.match('dynasty'):
            print('matched dynasty --------------------', self.current_token())
            return True
        
        # 6	<dynasty>	→	λ
        # Directly check token without calling data_type() to prevent recursion
        if token in {'scroll', 'treasures', 'mirror', 'ocean', 'rose'}:
            print('passed dynasty --------------------', self.current_token())
            return True
        
        return False


    def vardec_def(self):
        token = self.current_token()
        print("ente vardec_def  -----------------------------", self.current_token())
        # 7	<vardec_def>	→	<initialization> <vardec_more>~
    
        print('enter init --------------------', self.current_token())
        if self.initialization() and self.vardec_more(): 
            if not self.match("~"):
                raise SyntaxError(f"Missing terminator '~' for variable declaration at Line {self.current_line + 1}, Index {self.current_index + 1}")
            return True

        # 8	<vardec_def>	→	[<array_size>] <column> <array_initialization> <array_more>~
        elif self.match('['):
            # Handle the first dimension (e.g., `identifier[2]`)
            print("enter index vardec_def ", self.current_token())
            if not self.array_size() :  
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}"
                return False
            print('passed array size')
            if not self.match(']'): 
                return False
            print('matched ]')
            # If there are additional dimensions (e.g., `[2][2]`)
            if not self.column():  
                return False
            print('passed column')
            # Proceed with array initialization
            if not self.array_initialization():
                return False
            print('passed array_initialization')
            # Check for additional array declarations if needed
            if not self.array_more():
                return False
            print('passed array_more')
            # Match the end of the variable declaration with "~"
            if not self.match('~'):
                return False
            print('matched ~')
            return True

        return False
    
    def initialization(self):
        token = self.current_token()
        # 11	<initialization>	→	= <val>
        print({self.current_token()}, "init ---------------- ")
        if self.match('='):
            if not self.val():
                token = self.current_token()
                if token in [ 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted', 'identifier', 'spell', 'tale', 'cast', 'forever', 'believe', 'spell', 'castle', 'return', '}', 'break', 'continue' ]:
                    raise SyntaxError(f"Missing terminator '~' for variable declaration at Line {self.current_line + 1}, Index {self.current_index + 1}")
                    return False
                else:
                    raise SyntaxError(self.error_message)
                    return False
            return True

        # 12	<initialization>	→	λ 
        elif token in ['~', ',']:
            return True
        
        # raise SyntaxError(f"Missing terminator '~' for variable declaration at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False

    def vardec_more(self):
        token = self.current_token() 
        print({self.current_token()}, "vardec more", self.current_token())
        # 13	<vardec_more>	→	, id_lit <initialization> <vardec_more>
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                return False
            return self.vardec_more()
        
        # 14	<vardec_more>	→	λ
        # print('enter null vardec more --------------------', self.current_token())
        elif token in ['~']:
            return True
        
        self.error_message = f"Syntax Error: Missing tilde '~' at Line {self.current_line}, Index {self.current_index + 1}"
        return False

    def column(self):
        # 15	<column>	→	[<array_size>]
        token = self.current_token()
        if self.match('['):
            if not self.array_size() :  
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}"
                return False
            if not self.match(']'):
                return False
            return True
        
        # 16	<column>	→	λ
        elif token in ['+=', '-=', '*=', '/=', '%=', '=', '&&', '||', ')', '+', '-', '/', '*', '%', '~', '<', '>', '<=', '>=', '==', '!=', '=', ',' , 'identifier', 'ocean_lit', 'treasures_lit', '(', '~']:  # End of the array definition
            return True  
        
        return True

    def array_initialization(self):
        print('entered array init')
        token = self.current_token()
        # 17	<array_initialization>	→	= <array_list>  
        if self.match('='):
            if not self.array_list():
                return False
            return True
        # 18	<array_initialization>	→	λ
        elif token in [',', '~', ')']:
            return True

        self.error_message = f"Syntax Error: Missing tilde '~' at Line {self.current_line}, Index {self.current_index + 1}"
        return False


    def array_list(self):
        print('entered array list')
        # 19	<array_list>	→	{<array_content>}
        if not self.match('{'):
            self.error_message = f"Syntax Error: Invalid array initialization '{repr(self.tokens[self.current_line][self.current_index][1])}', must be an array list at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
        print('matched {')
        if not self.array_content():
            return False
        
        print('passed array content ', self.current_token())
        if not self.match('}'):
            return False
        
        print('matched }')

        return True


    def array_content(self):
        current_pos = self.current_index
        print('entered array content', self.current_token())
        # 20	<array_content>	→	<array_lit> <lit_more> 
        if self.array_lit() and self.lit_more():
            return True

        self.current_index = current_pos
        # 21	<array_content>	→	{<array_row>} <row_more>
        if self.match('{') and  self.array_row() and self.match('}') and self.row_more():
            return True
        
        # 22	<array_content>	→	id_lit <row_more>
        elif self.match('identifier'):
            print('entered array content - matched id')
            if not self.row_more():
                return False
            return True

        return False

    def array_row(self):
        print('entered array row')
        # 23	<array_row>	→	<array_lit> <lit_more> 

        if not self.array_lit():
            return False
        
        print('passed array lit')

        if not self.lit_more():
            return False
        
        print('passed lit more')

        return True
    
    def row_more(self):
        print('entered row more', self.current_token())
        token = self.current_token()
        # 24	<row_more>	→	, <row_more_ext>
        if self.match(','):
            print('entered matched ,')
            if not self.row_more_ext():
                return False
            return True
        
        # 25	<row_more>	→	λ
        elif token == '}':
            return True  # If no more rows, end with closing bracket

        return False

    
    def row_more_ext(self):
        print('entered row more ext')
        # 25	<row_more_ext>	→	{<array_row>} <row_more>
        if self.match('{'):
            print('entered matched {')
            if not self.array_row():
                return False
            if not self.match('}'):
                return False
            if not self.row_more():
                return False
            return True
        
        # 26	<row_more_ext>	→	id_lit <row_more>
        elif self.match('identifier'):
            if not self.row_more():
                return False
            return True
        
        return False
        
    
    def lit_more(self):
        # 28	<lit_more>	→	, <array_lit> <lit_more>
        token = self.current_token()

        if self.match(','):
            if not self.array_lit():
                return False
            if not self.lit_more():
                return False
            return True

        # 29	<lit_more>	→	λ
        elif token == '}':
            return True  # If no more literals, end with closing bracket

        return False
        
    def array_more(self):
        print('entered array more ---', self.current_token())
        # 30	<array_more>	→	, id_lit [<array_size>] <column> <array_initialization> <array_more>
        token = self.current_token()

        if self.match(','):
            if not self.match('identifier'):
                return False
            print({self.current_token()}, "enter index", self.current_token())
            if not self.match('['):
                return False
            print({self.current_token()}, "enter array size", self.current_token())
            if not self.array_size():
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(']'):
                return False
            if not self.column():
                return False
            if not self.array_initialization():
                return False
            if not self.array_more():
                return False
            return True

        # 31	<array_more>	→	λ
        elif token == '~':
            return True  # End of array initialization with tilde

        self.error_message = f"Syntax Error: Missing tilde '~' at Line {self.current_line}, Index {self.current_index + 1}"
        return False
    
    def array_lit(self):
        # 32	<array_lit>	→	id_lit
        if self.match('identifier'):
            return True
        
        #33	<array_lit>	→	<lit4> 
        elif self.lit4():
            return True
        
        print(f'Line {self.current_line + 1}, Index {self.current_index + 1} --------------------------')
        return False
    
    def assignment_operator(self):
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
            print({self.current_token()}, "=/ ----------------------------")
            return True
        # 38	<assignment_operator>	→	%=
        elif self.match('%='):
            return True
        
        self.error_message = f"Syntax Error: Invalid Assignment Operator '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False

    def assignment_operand(self):
        # 37	<assignment_operand>	→	id_lit <id_ext> <more_arith>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            if not self.more_arith():
                return False
            return True
        
        # 38	<assignment_operand>	→	<lit3> <more_arith>
        elif self.lit3():
            if not self.more_arith():
                return False
            return True
        
        # 39	<assignment_operand>	→	<arithmetic_operand_2> <arithmetic_operator><arithmetic_operand><more_arith>
        elif self.arithmetic_operand_2():
            if not self.arithmetic_operator():
                return False
            if not self.arithmetic_operand():
                return False
            if not self.more_arith():
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid Assignment Operand '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False

    def logical_exp(self):
        current_pos = self.current_index
        # 40	<logical_exp>	→	<logical_operator1> <logical_operand> <logical_operator> <logical_operator1> <logical_operand> <more_log>
        print("entered logical expression", self.current_token())
        if self.logical_operator1() and self.logical_operand() and self.logical_operator() and self.logical_operator1() and self.logical_operand() and self.more_log():
            return True

        self.current_index = current_pos
        # 41	<logical_exp>	→	! <logical_operand> <more_log>
        if self.match('!') and self.logical_operand() and self.more_log():
            return True
        
        return False
 
    
    def logical_operand(self):
        current_pos = self.current_index
        print("entered logical operand", self.current_token())
        # 42	<logical_operand>	→	id_lit <id_ext> <logical_operand_ext>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            if not self.logical_operand_ext():
                return False
            return True
        
        # 43	<logical_operand>	→	<lit3> <more_arith> <relational_operator> <relational_operand><relational_more>
        elif self.lit3() and  self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more():
            return True
        
        self.current_index = current_pos
        # 44	<logical_operand>	→	scroll_lit <relational_operator> <relational_operand><relational_more>
        if self.match('scroll_lit') and self.relational_operator() and self.relational_operand() and self.relational_more():
            return True
        
        self.current_index = current_pos
        # <logical_operand>	→ rose_lit <relational_operator> <relational_operand><relational_more>
        if self.match('rose_lit') and self.relational_operator() and self.relational_operand() and self.relational_more():
            print()
            return True
        
        self.current_index = current_pos
        # 45	<logical_operand>	→	mirror_lit
        if self.match('mirror_lit'):
            return True
        
        self.current_index = current_pos
        # 46	<logical_operand>	→	<treasures_mirror>
        if self.treasures_mirror():
            return True
        
        self.current_index = current_pos
        # 47	<logical_operand>	→	(<expression>)
        if self.match('('):
            print('enter epxression', self.current_token())
            if not self.expression():
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid Logical Operand '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def expression(self):
        print('entered epxression ----------------------??', self.current_token())
        current_pos = self.current_index

        # 48 <expression>	→	<relational_exp>) <relational_more>
        if self.relational_exp() and self.match(')') and self.relational_more():
            print('passed epxression relational ----------------------??', self.current_token())
            return True
        
        # 49	<expression>	→	<logical_exp>)
        self.current_index = current_pos
        if self.logical_exp() and self.match(')'):
            print('passed epxression logical ----------------------??', self.current_token())
            return True
        
        self.current_index = current_pos
        # <expression>	→	<arithmetic_exp>) <more_arith> <relational_operator> <relational_operand> <relational_more>
        if self.arithmetic_exp() and self.match(')') and self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more():
            return True
        
        return False
    
    
    def logical_operand_ext(self):
        current_pos = self.current_index
        print('enter logical_operand_ext ---------', self.current_token())
        token = self.current_token()
        # 52	<logical_operand_ext>	→	<more_arith> <relational_operator> <relational_operand><relational_more>
        if self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more():
            return True
        
        self.current_index = current_pos
        # 53	<logical_operand_ext>	→	λ
        if token in ['&&', '||', ',' , ')', '~'   ]:
            print('enter null log-op-ext ---------', self.current_token())
            return True

        return False
    

    def logical_operator(self):
        # 54	<logical_operator>	→	&&
        if self.match('&&'):
            return True
        
        # 55	<logical_operator>	→	||
        elif self.match('||'):
            print('matched || ---------', self.current_token())
            return True
        
        return False
    
    def logical_operator1(self):
        token = self.current_token()
        # 56	<logical_operator1>	→	!
        if self.match('!'):
            return True
        
        # 55 <logical_operator1>	→	λ
        elif token in ['identifier','ocean_lit', 'treasures_lit', 'scroll_lit', 'mirror_lit', '1','0', '(']:
            return True
        
        self.error_message = f"Syntax Error: Invalid Logical Operator '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        
        return False
    
    def more_log(self):
        current_pos = self.current_index
        print('enter more log')
        token = self.current_token()
        # 57	<more_log>	→	 <logical_operator> <logical_operator1> <logical_operand> <more_log>
        if self.logical_operator() and self.logical_operator1() and self.logical_operand() and self.more_log():
            return True
        
        self.current_index = self.current_index
        # 58	<more_log>	→	λ
        if token in [',', ')', '~']:
            print('more log null ------------------')
            return True

        return False
    
    def treasures_mirror(self):
        # 61	<treasures_mirror>	→	1
        if self.match('1'):
            return True
        
        # 62	<treasures_mirror>	→	0
        if self.match('0'):
            return True
        
        return False
    
    def arithmetic_exp(self):
        print('entered arith exp---------', self.current_token())
        # 63	<arithmetic_exp>	→	<arithmetic_operand> <arithmetic_operator><arithmetic_operand><more_arith>
        if self.arithmetic_operand() and self.arithmetic_operator() and self.arithmetic_operand() and self.more_arith():
            print('arithmetic exp passed ------------- ', self.current_token())
            return True
        print('arithmetic exp not passed ------------- ', self.current_token())
        return False
    
    def arithmetic_operand_1(self):
        print('entered arith operand---------', self.current_token())
        # 64	<arithmetic_operand_1>	→	id_lit <id_ext>
        if self.match('identifier'):
            print('passed id arith operand---------', self.current_token())
            if not self.id_ext():
                return False
            print('passed id arith operand')
            return True
            
        
        # 65	<arithmetic_operand_1>	→	<lit3>
        elif self.lit3():
            return True
        
        return False
    
    def arithmetic_operand_2(self):
        # 66	<arithmetic_operand_2>	→	(<arithmetic_exp>)
        if self.match('('):
            if not self.arithmetic_exp():
                return False
            if not self.match(')'):
                return False
            return True
        
        return False  # Explicitly return False if no match is found
        
    def arithmetic_operand(self):
        # 67	<arithmetic_operand>	→	<arithmetic_operand_1>
        if self.arithmetic_operand_1():
            return True
        
        # 68	<arithmetic_operand>	→	<arithmetic_operand_2>
        elif self.arithmetic_operand_2():
            return True
        
        self.error_message = (f"Syntax Error: Invalid Operand '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
    
    def arithmetic_operator(self):
        print('entered arith operator---------', self.current_token())
        # 69	<arithmetic_operator>	→	+
        if self.match('+'):
            return True
        
        # 70	<arithmetic_operator>	→	-
        elif self.match('-'):
            return True
        
        # 71	<arithmetic_operator>	→	/
        elif self.match('/'):
            return True
        
        # 72	<arithmetic_operator>	→	*
        elif self.match('*'):
            return True
        
        # 73	<arithmetic_operator>	→	%
        elif self.match('%'):
            return True
        
        # raise SyntaxError(f"Syntax Error: Invalid Arithmetic Operator '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
    
    def more_arith(self):
        print('entered more arith ------------', self.current_token())
        token = self.current_token()
        
        # Rule: <more_arith>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                return False
            return self.more_arith()  # Simplified recursive call
        
        # Rule: <more_arith>	→	λ
        elif token in ['<', '>', '<=', '>=', '==', '!=', '&&', '||', ',' , ')', '~']:
            print('more_arith null')
            return True
        

        return False
    
    def relational_exp(self):
        print('entered relational exp')
        # 76	<relational_exp>	→	<relational_operand> <relational_operator> <relational_operand> <relational_more> 
        if self.relational_operand():
            print('passed relational operand')
            if not self.relational_operator():
                return False
            print('passed relational operator')
            if not self.relational_operand():
                return False
            print('passed relational operand')
            if not self.relational_more():
                return False
            print('passed relational more')
            return True
        print('not pass relational exp', self.current_index)
        return False

    def relational_operand(self):
        print('entered relational operand', self.current_token())
        # 77	<relational_operand_1>	→	id_lit <id_ext> <more_arith>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            if not self.more_arith():
                return False
            return True
        
        # 78	<relational_operand_1>	→	<lit3> <more_arith>
        elif self.lit3():
            print('passed lit3')
            if not self.more_arith():
                return False
            print('passed rel exp more arith')
            return True
        
        # 79	<relational_operand>	→	scroll_lit
        elif self.match('scroll_lit'):
            return True
        
        # <relational_operand>	→	rose_lit
        elif self.match('rose_lit'):
            return True
         
        # 78	<relational_operand>	→	(<expression_2>
        elif self.match('('):
            if not self.expression_2():
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid Operand '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def expression_2(self):
        current_pos = self.current_index
        # content = []
        # current_pos = self.current_index
        # token = self.current_token()
        
        # while token != '~':
        #     token = self.current_token()
        #     content.append(token)
        #     self.advance()
        
        # expr = self.determine_operation_type(content)
        # self.current_index = current_pos

        # 79	<expression_2>	→	<arithmetic_exp> ) <more_arith>
        if self.arithmetic_exp() and self.match(')') and self.more_arith():
            return True
        
        self.current_index = current_pos
        # print("-------------------------------------",self.current_token() )
        # 80	<expression_2>	→	<relational_exp>  )
        if self.relational_exp() and self.match(')'):
            return True
        
        return False
    
    def relational_operator(self):
        print('enter relational operator', self.current_token())
        # 83	<relational_operator>	→	<
        if self.match('<'):
            print('matched <')
            return True
        
        # 84	<relational_operator>	→	>
        elif self.match('>'):
            print('matched <')
            print('passed relational operator')
            return True
        
        # 85	<relational_operator>	→	<=
        elif self.match('<='):
            return True
        
        # 86	<relational_operator>	→	>=
        elif self.match('>='):
            return True
        
        # 87	<relational_operator>	→	==
        elif self.match('=='):
            return True
        
        # 88	<relational_operator>	→	!=
        elif self.match('!='):
            return True
        
        self.error_message = f"Syntax Error: Invalid Relational Operator '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def relational_more(self):
        print('eneter relational more')
        token = self.current_token()
        # 89	<relational_more>	→	<relational_operator> <relational_operand><relational_more>
        if self.relational_operator():
            if not self.relational_operand():
                return False
            if not self.relational_more():
                return False
            return True
        
        # 90	<relational_more>	→	λ
        elif token in ['&&', '||', ',' , ')', '~']:
            print('relational more null -----', self.current_token())
            return True

        return False
    
    def unary(self):
        # 91	<unary>	→	id_lit <unary_operator>
        if self.match('identifier'):
            if not self.unary_operator():
                return False
            return True
        
        return False
    
    def unary_operator(self):
        # 92	<unary_operator>	→	++
        if self.match('++'):
            return True
        
        # 93	<unary_operator>	→	--
        elif self.match('--'):
            return True
        
        self.error_message = f"Syntax Error: Unary Operator '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def string_operand(self):
        # 94	<string_operand>	→	<lit1>
        if self.lit1():
            return True
        
        # 95	<string_operand>	→	id_lit <id_ext>
        elif self.match('identifier'):
            if not self.id_ext():
                return False
            return True
        
        # 96	<string_operand>	→	toscroll(<conver_value>)
        elif self.match('toscroll'):
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid Operand '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    

    def string_more(self):
        token = self.current_token()
        # 97	<string_more>	→	+ <string_operand> <string_more>
        if self.match('+'):
            if not self.string_operand():
                return False
            if not self.string_more():
                return False
            return True
        
        # 98	<string_more>	→	λ
        elif token in [',', ')', '~']:
            return True

        return False
    
    def user_defined_func(self):
        token = self.current_token()
        # 99	<user-defined_func>	→	spell <return_type> id_lit(<param>) {<body><ret_statement>} <user-defined_func>
        if self.match('spell'):
            if not self.return_type():
                return False
            print('passed return type -----------', self.current_token())
            self.advance()
            if not self.match('identifier'):
                return False
            print('passed id ------------------', self.current_token())
            if not self.match('('):
                return False
            if not self.param():
                return False
            if not self.match(')'):
                return False
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.ret_statement():
                return False
            if not self.match('}'):
                return False
            if not self.user_defined_func():
                return False
            
            return True
        
        # 100	<user-defined_func>	→	λ
        elif token in ['castle', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted',  
                        'identifier','spell', 'tale', 'cast', 'forever', 'believe', 'return', '}', 'break', 'continue', 'EOF']:
            return True

        return False
    
    def return_type(self):
        token = self.current_token()
        print('return type -------------')
        # 101	<return_type>	→	<data_type>
        if self.data_type():
            return True
        
        # 102	<return_type>	→	chamber
        elif token == 'chamber':
            return True
        
        self.error_message = f"Syntax Error: Missing return type at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def param(self):
        print('enter param')
        token = self.current_token()
        # 103	<param>	→	<data_type> id_lit <param_more>
        if self.match('treasures') or self.match('ocean') or self.match('scroll') or self.match('rose') or self.match('mirror'): 
            if self.match('identifier') and self.param_more():
                return True
        
        # 104	<param>	→	λ
        elif token in [ ')']:
            return True

        raise SyntaxError(f"Syntax Error: Invalid parameter at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
    
    def param_more(self):
        print('enter param more ++++++++', self.current_token())
        token = self.current_token()
        # 105	<param_more>	→	, <data_type> id_lit <param_more>
        if self.match(','):
            print('passed ,  ++++++++', self.current_token())
            # Correct way to match data types
            data_types = ['treasures', 'ocean', 'scroll', 'rose', 'mirror']
            if not any(self.match(data_type) for data_type in data_types):
                print('failed data type  ++++++++', self.current_token())
                return False
            
            print('passed data type  ++++++++', self.current_token())
            print('passed data type  ++++++++', self.current_token())
            if not self.match('identifier'):
                return False
            if not self.param_more():
                return False
            return True
        
        # 106	<param_more>	→	λ
        elif token in [ ')']:
            return True

        # raise SyntaxError(f"Syntax Error: Invalid parameter at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
    
    def body_1(self):
        token = self.current_token()
        print('enter body 1 -----------------------------')
        # 107	<body_1>	→	<var_dec> <body>

        if token in ['dynasty', 'treasures', 'ocean', 'scroll', 'rose', 'mirror']:
            if not self.var_dec():
                print(self.error_message)
                return False
            return self.body()
        
        # 108	<body_1>	→	<output> <body>
        elif token == 'granted':
            if not self.output():
                return False
            return self.body()
        
        # 109	<body_1>	→	id_lit <body_1_ext> <body>
        elif self.match('identifier'):
            print('enter identifier')
            if not self.body_1_ext():
                return False
            print('passed body id ext')
            return self.body()
        
        # 110	<body_1>	→	<user-defined_func> <body>
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.body()
        
        # 111	<body_1>	→	<for_loop> <body>
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.body()
        
        
        return False
    
    def body_1_ext(self):
        token = self.current_token()
        print('enter body 1 ext---------', self.current_token() )
        # 112	<body_1_ext>	→	(<args>)~
        if self.match('('):
            if not self.args():
                return False
            if not self.match(')'):
                return False
            if not self.match('~'):
                return False
            return True
            
        # 113	<body_1_ext>	→	= <val> ~
        elif self.match('='):
            print('enter = ')
            if not self.val():
                return False
            print('passed = val ---------------')
            if not self.match('~'):
                return False
            return True
        
        # 114	<body_1_ext>	→	<unary_operator> ~ 
        elif self.unary_operator():
            if not self.match('~'):
                return False
            return True
        
        # 115	<body_1_ext>	→	<index> <assignment_operator> <assignment_operand>~ 
        elif self.index() and self.assignment_operator() and self.assignment_operand() and self.match('~'):
            return True
        
        print('----------------------------------- invalid body 1 ext --------------------------------------------')
        raise SyntaxError(f"Syntax Error: Invalid input '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}")
        return False
        
    def body_2(self):
        print('enter body 2 -----------------------------', self.current_token())
        token = self.current_token()
        # 116	<body_2>	→	<condi_statement> <body>
        if token in ['cast', 'forever', 'believe']:
            if not self.condi_statement():
                return False
            return self.body()
        print('not body 2 -----------------------------', self.current_token())
        return False


    def body(self):
        print('enter body -----------------------------')
        token = self.current_token()
        # 117	<body>	→	<body_1>
        if self.body_1():
            print('body part is not null ---------------', self.current_token())
            return True
        
        # 118	<body>	→	<body_2>
        elif self.body_2():
            print('body part is not null ---------------', self.current_token())
            return True
        
        # 119	<body>	→	λ 
        elif token in ['return', '}', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted',  
                        'identifier','spell', 'tale', 'cast', 'forever', 'believe', 'EOF']:
            print('body part is null ---------------', self.current_token())
            return True
        
        if token in ['break', 'continue']:
            raise SyntaxError(f"Syntax Error: Invalid input '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}")
            return False

        return False
    
    def flow_body(self):
        token = self.current_token()
        print('enter body flow -----------------------------', self.current_token())
        # 107	<body_1>	→	<var_dec> <body>

        if token in ['dynasty', 'treasures', 'ocean', 'scroll', 'rose', 'mirror']:
            if not self.var_dec():
                print(self.error_message)
                return False
            return self.flow_body()
        
        # 108	<body_1>	→	<output> <body>
        elif token == 'granted':
            if not self.output():
                return False
            return self.flow_body()
        
        # 109	<body_1>	→	id_lit <body_1_ext> <body>
        elif self.match('identifier'):
            print('enter identifier')
            if not self.body_1_ext():
                return False
            print('passed body id ext')
            return self.flow_body()
        
        # 110	<body_1>	→	<user-defined_func> <body>
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.flow_body()
        
        # 111	<body_1>	→	<for_loop> <body>
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.flow_body()
        
        token = self.current_token()
        # 116	<body_2>	→	<condi_statement> <body>
        if token in ['forever', 'believe']:
            if not self.condi_statement():
                return False
            return self.flow_body()

        elif token == 'cast':
            if not self.if_break():
                return False
            return self.flow_body()
        
        elif token in ['return', '}', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted',  
                        'identifier','spell', 'tale', 'cast', 'forever', 'believe', 'break', 'continue', 'EOF']:
            print('body part is null ---------------', self.current_token())
            return True
        
        return False
        
    
    def ret_statement(self):
        token = self.current_token()
        # 120	<ret_statement>	→	return <val1> ~
        if self.match('return'):
            if not self.val1():
                self.error_message = f"Syntax Error: Invalid return value at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match('~'):
                return False
            return True
        
        # 121	<ret_statement>	→	λ
        elif token in ['}']:
            return True

        self.error_message = f"Syntax Error: Invalid return statement at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def condi_statement(self):
        # 122	<condi_statement>	→	<if>
        if self.if_statement():
            return True
        
        # 123	<condi_statement>	→	<while>
        elif self.while_statement():
            return True

        # 124	<condi_statement>	→	<do_while>
        elif self.do_while():
            return True
        
        return False
    
    def for_loop(self):
        print('entered for_loop ------------------', self.current_token())
        # 125	<for_loop>	→	tale (<loop_var> ~ <relational_exp> ~ <unary>) {<loop_body>}
        if self.match('tale'):
            if not self.match('('):
                return False
            print('matched ( ------------------', self.current_token())
            if not self.loop_var():
                return False
            print('passed loop_var ------------------', self.current_token())
            if not self.match('~'):
                return False
            print('matched ~ ------------------', self.current_token())
            if not self.relational_exp():
                return False
            print('passed relational_exp ------------------', self.current_token())
            if not self.match('~'):
                return False
            print('matched ~ ------------------', self.current_token())
            if not self.unary():
                return False
            
            if not self.match(')'):
                return False
            print('matched ) ------------------', self.current_token())
            if not self.match('{'):
                return False
            print('matched { ------------------', self.current_token())
            if not self.loop_body():
                return False
            if not self.match('}'):
                return False
            print('matched } ------------------', self.current_token())
            return True
        
        return False
    
    def loop_var(self):
        # 126	<loop_var>	→	treasures id_lit = <loop_val>
        if self.match('treasures'):
            if not self.match('identifier'):
                return False
            if not self.match('='):
                self.error_message = f"Syntax Error: Missing variable initialization at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.loop_val():
                self.error_message = f"Syntax Error: Invalid looping variable value at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            return True
        
        # 127	<loop_var>	→	id_lit <loop_init>
        elif self.match('identifier'):
            if not self.loop_init():
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid looping variable at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def loop_init(self):
        token = self.current_token()
        # 128	<loop_init>	→	=  <loop_val>
        if self.match('='):
            if not self.loop_val():
                self.error_message = f"Syntax Error: Invalid looping value '~' at Line {self.current_line}, Index {self.current_index + 1}"
                return False
            return True
        
        # 129	<loop_init>	→	λ
        elif token in ['~']:
            return True
        
        self.error_message = f"Syntax Error: Missing tilde '~' at Line {self.current_line}, Index {self.current_index + 1}"
        return False
    
    def loop_val(self):
        # 130	<loop_val>	→	id_lit
        if self.match('identifier'):
            return True
        
        # 131	<loop_val>	→	treasures_lit
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            return True
        
        return False
    
    def loop_body(self):
        token = self.current_token()
        print('enter loop_body  ---------------------------------------', self.current_token())

        if token in ['dynasty', 'treasures', 'ocean', 'scroll', 'rose', 'mirror']:
            if not self.var_dec():
                return False
            return self.loop_body()
        
        elif token == 'granted':
            if not self.output():
                return False
            return self.loop_body()
        
        elif token == 'identifier':
            print('enter identifier')
            self.match('identifier')
            if not self.body_1_ext():
                return False
            print('passed body id ext')
            return self.loop_body()
        
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.loop_body()
        
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.loop_body()
        
        elif self.if_break():
            return self.loop_body()
        
        elif self.while_statement():
            return self.loop_body()
        
        elif self.do_while():
            return self.loop_body()
        
        # Lambda alternative: if token indicates end of loop body (e.g., '}' or another closing marker), accept empty loop body.
        elif token in ['}']:  # Adjust this set as needed.
            return True

        return False


    
    def if_break(self):
        print('entered if_break ---------------', self.current_token())
        # 136	<if_break>	→	cast (<condition>) {<body><flow_control>} <elif_break> <else_break>
        if self.match('cast'):
            if not self.match('('):
                return False
            print('matched ( ---------------', self.current_token())
            if not self.condition():
                return False
            print('passed condition---------------', self.current_token())
            if not self.match(')'):
                return False
            print('matched ) ---------------', self.current_token())
            if not self.match('{'):
                return False
            print('matched { ---------------', self.current_token())
            if not self.flow_body():
                return False
            print('passed body --------------', self.current_token())
            if not self.flow_control():
                return False
            print('passed flow control')
            if not self.match('}'):
                return False
            if not self.elif_break():
                return False
            if not self.else_break():
                return False
            return True
        
        return False
    

    def elif_break(self):
        token = self.current_token()
        # 137	<elif_break>	→	twist(<condition>) {<body><flow_control>}<elif_break>
        if self.match('twist'):
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            if not self.match('{'):
                return False
            if not self.flow_body():
                return False
            if not self.flow_control():
                return False
            if not self.match('}'):
                return False
            if not self.elif_break():
                return False
            return True

        # 138	<elif_break>	→	λ
        elif token in ['curse', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted',  'id_lit', 'spell', 'tale', 'cast', 'forever', 'believe', '}']:
            return True 

        return False

    def else_break(self):
        token = self.current_token()
        # 139	<else_break>	→	curse {<body><flow_control>}
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.flow_body():
                return False
            if not self.flow_control():
                return False
            if not self.match('}'):
                return False
            return True
        
        # 140	<else_break>	→	λ
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted',  'id_lit', 'spell', 'tale', 'cast', 'forever', 'believe', '}']:
            return True 
        
        return False
    
    def flow_control(self):
        print('entered flow control', self.current_token())
        token = self.current_token()
        # 141	<flow_control>	→	break~
        if self.match('break') and self.match('~'):
             return True

        # 142	<flow_control>	→	continue~
        elif self.match('continue') and self.match('~'):
             return True
        
        # 143	<flow_control>	→	λ
        elif token in ['}']:
            return True

        return False
    
    def do_while(self):
        # 144	<do_while>	→	believe {<loop_body>} forever(<condition>)~
        if self.match('believe'):
            if not self.match('{'):
                return False
            if not self.loop_body():
                return False
            if not self.match('}'):
                return False
            if not self.match('forever'):
                return False
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            if not self.match('~'):
                return False
            return True
        
        return False
    

    def condition(self):
        current_pos = self.current_index
        
        print('entered condition', self.current_token())
        # 145	<condition>	→	<treasures_mirror> <more_log>
        if self.treasures_mirror() and self.more_log():
            return True
        
        self.current_index = current_pos
        # 146	<condition>	→	id_lit <condi_id_ext>
        if self.match('identifier') and  self.condi_id_ext():
            print('passed condi_id_ext')
            return True
        
        self.current_index = current_pos
        # 148	<condition>	→	<logical_operator1> <logical_operand> <more_log>
        if self.logical_operator1() and self.logical_operand() and self.more_log():
            return True
        
        self.current_index = current_pos
        # 148	<condition>	→	mirror_lit <more_log>
        if self.match('mirror_lit') and self.more_log():
            return True
        
        self.current_index = current_pos
        # 149	148	<condition>	→	<lit3> <more_arith> <relational_operator> <relational_operand><relational_more> <more_log>
        if self.lit3() and self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            return True
        
        self.current_index = current_pos
        # 149	<condition>	→	scroll_lit <relational_operator> <relational_operand><relational_more> <more_log>
        if self.match('scroll_lit') and  self.relational_operator() and  self.relational_operand() and self.relational_more() and self.more_log():
            return True
        
        self.current_index = current_pos
        # <condition>	→ rose_lit <relational_operator> <relational_operand><relational_more> <more_log>
        if self.match('rose_lit') and self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            return True

        self.current_index = current_pos
        # 150	<condition>	→	(<expression>
        if self.match('('):
            if not self.expression_3():
                return False
            return True
        
        
        self.error_message = f"Syntax Error: Invalid condition at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    

    def expression_3(self):
        print('entered condition ( ------------------------', self.current_token())
        current_pos = self.current_index
        # 153	<expression_3>	→	<relational_exp>) <relational_more><more_log>
        if self.relational_exp(): 
            print('passed exp3 relational exp', self.current_token())
            if not self.match(')'):
                return False
            print('passed exp3 )')
            if not self.relational_more():
                return False
            if not self.more_log():
                return False
            return True
        
        self.current_index = current_pos
        # 154	<expression_3>	→	<logical_exp>)<more_log>
        if self.logical_exp() and self.match(')') and self.more_log():
            return True
        
        self.current_index = current_pos
        # 155	<expression_3>	→	<arithmetic_exp>) <more_arith> <relational_operator> <relational_operand><relational_more><more_log>
        if self.arithmetic_exp() and self.match(')') and self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            return True
        
        return False

    def condi_id_ext(self):
        print('entered condi_id_ext' , self.current_token())
        token = self.current_token()
        current_pos = self.current_index
        # 154	<condi_id_ext>	→	<mirror_init>
        if self.mirror_init():
            return True
        
        self.current_index = current_pos
        # 155	<condi_id_ext>	→	<id_ext> <other_id_ext>
        if self.id_ext() and self.other_id_ext():
            print('passed # 155	<condi_id_ext>	→	<id_ext> <other_id_ext>')
            return True
        
        # 156	<condi_id_ext>	→	λ
        elif token in [')']:
            return True

        return False
    
    def other_id_ext(self):
        print('entered other_id_ext()---------------')
        token = self.current_token()

        # <other_id_ext>	→	<other_id_ext_1>  <other_id_ext_2> 
        if self.other_id_ext_1() and self.other_id_ext_2():
            return True

        return False
    
    def other_id_ext_1(self):
        print('entered other_id_ext_1   ---------------')
        token = self.current_token()
        # <other_id_ext_1>	→	<more_arith> <relational_operator> <relational_operand><relational_more>
        if self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more():
            return True
        
        # <other_id_ext_1>	→	λ
        elif token in ['&&', '||', ')']:
            return True
        
        return False
    

    def other_id_ext_2(self):
        print('entered other_id_ext_2   ---------------')
        token = self.current_token()
        # 162	162	<other_id_ext_2>	→	<logical_operator> <more_log>
        if self.logical_operator() and self.more_log():
            return True
        
        # <other_id_ext_2>	→	λ
        elif token in [')']:
            return True

        return False
    

    def mirror_init(self):
        token = self.current_token()
        # 160	<mirror_init>	→	== mirror_lit
        if self.match('==') and self.match('mirror_lit'):
            return True
        
        # 161	<mirror_init>	→	!= mirror_lit
        elif self.match('!=') and self.match('mirror_lit'):
            return True
        
        # 162	<mirror_init>	→	λ
        elif token in [')']:
            return True

        return False
    
    def while_statement(self):
        # 163	<while>	→	forever (<condition>) {<loop_body>}
        if self.match('forever'):
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            if not self.match('{'):
                return False
            if not self.loop_body():
                return False
            if not self.match('}'):
                return False
            return True
        
        return False
    
    def if_statement(self):
        # 164	<if>	→	cast (<condition>) {<body>} <elif> <else>
        if self.match('cast'):
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.match('}'):
                return False
            if not self.elif_statement():
                return False
            if not self.else_statement():
                return False
            return True
        
        return False

    def elif_statement(self):
        token = self.current_token()
        # 165	<elif>	→	twist(<condition>) {<body>}<elif>
        if self.match('twist'):
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.match('}'):
                return False
            if not self.elif_statement():
                return False
            return True
        
        # 166	<elif>	→	λ
        elif token in ['curse', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 
                       'granted',  'id_lit', 'spell', 'tale', 'cast', 'forever', 'believe', 'return', '}', 'break', 'continue']:
            return True

        return False
    
    def else_statement(self):
        token = self.current_token()
        # 167	<else>	→	curse {<body>}
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.match('}'):
                return False
            return True
        
        # 168	<else>	→	λ
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 
                       'granted',  'id_lit', 'spell', 'tale', 'cast', 'forever', 'believe', 'return', '}', 'break', 'continue']:
            return True

        return False
    
    def output(self):
        print('enter output')
        # 169	<output>	→	granted(<granted_content> <more_granted>) ~
        if self.match('granted'):
            if not self.match('('):
                return False
            if not self.granted_content():
                return False
            print('passed granted_content')
            if not self.more_granted():
                return False
            print('passed more_granted')
            if not self.match(')'):
                return False
            if not self.match('~'):
                return False
            return True
        
        return False
    
    def granted_content_1(self):
        print('enter granted content 1')
        # 170	<granted_content_1>	→	set_precision
        if self.match('setprecission'):
            return True
        
        # 171	<granted_content_1>	→	id_lit <granted_id_ext>
        elif self.match('identifier'):
            print('matched id')
            if not self.granted_id_ext():
                return False
            print('passed granted_id_ext')
            return True
        
        return False
    
    def granted_content_2(self):
        print('enter granted content 2', self.current_token())
        token = self.current_token()
        # 172	<granted_content_2>	→	phantom
        if self.match('phantom'):
            return True
        
        # 173	<granted_content_2>	→	<conversion_func> (<conversion_value>)
        elif self.conversion_func():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        # 175	<granted_content_2>	→	toscroll (<conversion_value>) <string_more>
        elif self.match('toscroll'):
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            if not self.string_more():
                return False
            return True
        
        
        elif self.match('1') or self.match('0'):
            # 176	<granted_content_2>	→	<treasures_mirror> <more_log>
            if self.more_log():
                return True
            
            # 180	<granted_content_2>	→	<lit3>  <granted_lit3_ext>
            elif self.granted_lit3_ext():
                print('passed granted lit 3 ext --------------------', self.current_token())
                return True
            
        
        # 177	<granted_content_2>	→	mirror_lit <more_log>
        elif self.match('mirror_lit'):
            if not self.more_log():
                return False
            return True
        
        # 177	<granted_content_2>	→	scroll_lit <granted_scroll_ext>
        elif self.match('scroll_lit'):
            if not self.granted_scroll_ext():
                return False
            return True
        
        
        # 178	<granted_content_2>	→	rose_lit <granted_rose_ext>
        elif self.match('rose_lit'):
            if not self.granted_rose_ext():
                return False
            return True
        
        # 179	<granted_content_2>	→	<lit3> <granted_lit3_ext>
        elif token in ['treasures_lit', 'ocean_lit']:
            print('enter lit3 --------------------', self.current_token())
            if self.lit3():
                print('passed lit3 --------------------', self.current_token())
                if not self.granted_lit3_ext():
                    return False
                print('passed granted lit 3 ext --------------------', self.current_token())
                return True
        
        # 180	<granted_content_2>	→	( <granted_open_paren_ext>
        elif self.match('('):
            print('granted_content_2 matched ( -------------------')
            if self.granted_open_paren_ext():
                return True
            
        # <granted_content_2>	→	<logical_operator1> <logical_operand> <more_log> 
        elif self.logical_operator1() and self.logical_operand() and self.more_log():
            return True
        
        return False
    
    def granted_content(self):
        print('entered granted content', self.current_token())
        # 181	<granted_content>	→	<granted_content_1>
        if self.granted_content_1():
            return True
        
        # 182	<granted_content>	→	<granted_content_2>
        if self.granted_content_2():
            return True
        
        self.error_message = f"Syntax Error: Invalid granted content at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def granted_open_paren_ext(self):
        content = []
        current_pos = self.current_index
        print(f'Initial current_pos: {current_pos}, current_index: {self.current_index}')
        
        while self.current_token() != '~':
            print(f'Current token: {self.current_token()}, current_index: {self.current_index}')
            content.append(self.current_token())
            self.advance()
        
        expr = self.determine_operation_type(content)
        print(f'Determined expression type: {expr}, content: {content}')
        
        # Reset to original position
        self.current_index = current_pos
        print(f'Reset current_index: {self.current_index}')

 
        if expr == 'arithmetic':
            # 185	<granted_open_paren_ext>	→	<arithmetic_exp>) <more_arith>
            if self.arithmetic_exp():
                if not self.match(')'):
                    return False
                if not self.more_arith():
                    False
                return True
        
        elif expr == 'logical':
            # 186	<granted_open_paren_ext>	→	<expression> <more_log>
            if self.expression():
                print('passedd expression ------------------')
                if not self.more_log():
                    return True
                print('passeddddddddddddddddd')
                return True
            
        elif expr == 'relational':
            # 187	<granted_open_paren_ext>	→	<expression_2> <relational_more>
            if self.expression_2(): 
                if not self.relational_more():
                    return False
                print('passeddddddddddddddddd')
                return True

        return False
    
    def granted_id_ext(self):
        token = self.current_token()
        # 188	<granted_id_ext>	→	<unary_operator>
        if self.unary_operator():
            return True
        
        # 189	<granted_id_ext>	→	<id_ext> <granted_other_id_ext>
        elif self.id_ext() and self.granted_other_id_ext():
            return True
        
        # 190	<granted_id_ext>	→	λ
        elif token in [',', ')', '~']:
            return True


        return False
    
    def granted_other_id_ext(self):
        print('enter granted_other_ext ---------', self.current_token())
        current_pos = self.current_index

        token = self.current_token()
        
        # 191	<granted_other_id_ext>	→	+ <string_operand> <string_more>
        if self.match('+') and self.string_operand() and self.string_more():
                return True
        
        self.current_index = current_pos
         # 192	<granted_other_id_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
        if self.arithmetic_operator() and self.arithmetic_operand() and self.more_arith():
                return True
        
        self.current_index = current_pos
        # 207	193	<granted_other_id_ext>	→	<more_arith> <relational_operator> <relational_operand> <relational_more> 
        if self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more():
                return True
        
        # self.current_index = current_pos
        # 197	<granted_other_id_ext>	→	<logical_operand_ext> <logical_operator> <more_log>
        if self.logical_operand_ext() and self.logical_operator() and self.more_log():
                return True
        
        # 195	<granted_other_id_ext>	→	λ
        if token in [',', ')', '~']:
            return True

        return False
    
    def granted_scroll_ext(self):
        token = self.current_token()
        # 191	<granted_scroll_ext>	→	+ <string_operand> <string_more>
        if self.match('+'):
            if not self.string_operand():
                return False
            if not self.string_more():
                return False
            return True
        
        # 192	<granted_scroll_ext>	→	<relational_operator> <relational_operand><relational_more> <more_log>
        elif self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            print('passed_more_log')
            return True
        
        # 193	<granted_scroll_ext>	→	λ
        elif token in [',', ')', '~']:
            return True

        return False
    
    def granted_rose_ext(self):
        token = self.current_token()
        # 194	<granted_rose_ext>	→	+ <string_operand> <string_more>
        if self.match('+'):
            if not self.string_operand():
                return False 
            if not self.string_more():
                return False
            return True
        # <granted_rose_ext>	→ <relational_operator> <relational_operand><relational_more> <more_log>
        elif self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            return True

        # 195	<granted_rose_ext>	→	λ
        elif token in [',', ')', '~']:
            return True

        return False
    
    def granted_lit3_ext(self):
        print('enter granted lit3 ext --------------------', self.current_token())
        token = self.current_token()
        current_pos = self.current_index

        # 203	<granted_lit3_ext>	→	<more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
        if self.more_arith() and self.relational_operator() and self.relational_operand() and self.relational_more() and self.more_log():
            return True

        self.current_index = current_pos
        # 202	<granted_lit3_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
        if self.arithmetic_operator() and self.arithmetic_operand() and self.more_arith():
            return True
    
        
        # 204	<granted_lit3_ext>	→	λ
        elif token in [',', ')', '~']:
            print('enter null --------------------', self.current_token())
            return True

        return False
    
    def more_granted(self):
        token = self.current_token()
        # 210	<more_granted>	→	, <granted_content> <more_granted>
        if self.match(','):
            if not self.granted_content():
                return False
            if not self.more_granted():
                return False
            return True
        
        # 211	<more_granted>	→	λ
        elif token in [')']:
            return True

        return False
    
    def data_type(self):
        print('enter data type--------------------', self.current_token())
        token = self.current_token()
        # 212	<data_type>	→	scroll
        # 213	<data_type>	→	treasures
        # 214	<data_type>	→	mirror
        # 215	<data_type>	→	ocean
        # 216	<data_type>	→	rose
        if token in {'scroll', 'treasures', 'mirror', 'ocean', 'rose'}:
            print('passed data type --------------------', self.current_token())
            return True
        
        return False
    
    def val(self):
        token = self.current_token()
        print('enter val -------', self.current_token())
        # 218	<val>	→	id_lit <granted_id_ext>
        if self.match('identifier') and self.granted_id_ext():
            return True
        
        # 219	<val>	→	<input>
        elif self.input():
            return True
        
        # 217	<val>	→	<granted_content_2>
        elif self.granted_content_2():
            print('passed granted_content_2 --------------------', self.current_token())
            return True
        

        return False
    
    def val1(self):

        # 221	<val1>	→	id_lit <val1_ext>
        if self.match('identifier'):
            if not self.val1_ext():
                return False
            return True

        # 220	<val1>	→	<granted_content_2>
        elif self.granted_content_2():
            return True
    
        
        return False
    
    def val1_ext(self):
        token = self.current_token()
        # 222	<val1_ext>	→	<id_ext> <val1_id_ext>
        if self.id_ext():
            if not self.val1_id_ext():
                return False
            return True
        
        # 223	<val1_ext>	→	<unary_operator>
        elif self.unary_operator():
            return True
        
        # 224	<val1_ext>	→	λ
        elif token in ['~']:
            return True
        
        return False
    
    def val1_id_ext(self):
        token = self.current_token()
        # 225	<val1_id_ext>	→	<granted_other_id_ext>
        if self.granted_other_id_ext():
            return True
        
        # 226	<val1_id_ext>	→	<assignment_operator> <assignment_operand>
        elif self.assignment_operator():
            if not self.assignment_operand():
                return False
            return True
        
        # 227	<val1_id_ext>	→	λ
        elif token in ['~']:
            return True

        return False
    
    
    def conversion_func(self):
        # 229	<conversion_func_2>	→	torose
        if self.match('torose'):
            return True
        
        # 230	<conversion_func_2>	→	totreasures
        if self.match('totreasures'):
            return True
        
        # 231	<conversion_func_2>	→	toocean
        if self.match('toocean'):
            return True
        
        # 232	<conversion_func_2>	→	tomirror
        if self.match('tomirror'):
            return True
        
        return False
    
    
    def conversion_value(self):
        # 235	<conversion_value>	→	<lit4>
        if self.lit4():
            return True
        
        # 236	<conversion_value>	→	id_lit <id_ext> 
        elif self.match('identifier'):
            if not self.id_ext():
                return False
            return True
        
        self.error_message = f"Syntax Error: Invalid conversion value at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def index(self):
        print('enter index +++++++++++++++', self.current_token())
        token = self.current_token()
        # 237	<index>	→	[<array_size>] <column1>
        if self.match('['):
            if not self.array_size():
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(']'):
                return False
            if not self.column1():
                return False
            return True
        
        # 238	<index>	→	λ
        elif token in ['&&', '||', ',' , ')', '~', '+', '-', '/', '*', '%', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=']:
            return True

        return False
            
    def column1(self):
        print('enter column1 +++++++++++++++', self.current_token())
        token = self.current_token()
        # 239	<column1>	→	[<array_size>]
        if self.match('['):
            if not self.array_size():
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(']'):
                return False
            return True

        # 240	<column1>	→	λ
        elif token in ['&&', '||', ',' , ')', '~', '+', '-', '/', '*', '%', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=']:
            return True

        return False
    
    def input(self):
        # 241	<input>	→	wish (scroll_lit)
        if self.match('wish'):
            if not self.match('('):
                return False
            if not self.match('scroll_lit'):
                self.error_message = f"Syntax Error: Invalid scroll literal '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(')'):
                return False
            return True
        
        return False

    def lit1(self):
        # 242	<lit1>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        
        # 243	<lit1>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        
        return False
    

    def lit2(self):
        # 244	<lit2>	→	mirror_lit
        if self.match('mirror_lit'):
            return True
        
        return False

    def lit3(self):
        # 245	<lit3>	→	ocean_lit
        if self.match('ocean_lit'):
            return True
        
        # 246	<lit3>	→	treasures_lit
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            print('enter treasures_lit --------------------', self.current_token())
            return True
        
        return False

    def lit4(self):
        # 247	<lit4>	→	<lit1>
        if self.lit1():
            return True
        
        # 248	<lit4>	→	<lit2>
        elif self.lit2():
            return True
        
        # 249	<lit4>	→	<lit3>
        elif self.lit3():
            return True

        return False

    def func_call(self):
        # 250	<func_call>	→	(<args>)
        if self.match('('):
            if not self.args():
                return False
            if not self.match(')'):
                return False
            return True
        
    def args(self):
        print('enter args +++++++++++++++', self.current_token())
        token = self.current_token()
        # 251	<args>	→	<args_val> <args_more>
        if self.args_val():
            if not self.args_more():
                return False
            return True
        
        # 252	<args>	→	λ
        elif token in [')']:
            return True
        
        self.error_message = f"Syntax Error: Invalid argument '{repr(self.tokens[self.current_line][self.current_index][1])}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def args_val(self):
        print('enter args val +++++++++++++++', self.current_token())
        # 253	<args_val>	→	id_lit <id_ext>
        if self.match('identifier'):
            print('enter args  id+++++++++++++++', self.current_token())
            if not self.id_ext():
                return False
            print('enter not id +++++++++++++++', self.current_token())
            return True
        
        # 254	<args_val>	→	<lit4>
        elif self.lit4():
            return True
        
        return False
    
    def args_more(self):
        token = self.current_token()

        # 255	<args_more>	→	, <args_val> <args_more>
        if self.match(','):
            if not self.args_val():
                return False
            if not self.args_more():
                return False
            return True
        
        # 256	<args_more>	→	λ
        elif token in [')']:
            return True

        return False
    
    def array_element(self):
        print('enter array element +++++++++++++++', self.current_token())
        # 257	<array_element>	→	<index>
        if self.index():
            return True
        
        return False
    
    def id_ext(self):
        print('entered id_ext', self.current_token())
        token = self.current_token()
        # 258	<id_ext>	→	<func_call>
        if self.func_call():
            return True
        
        
        # 259	<id_ext>	→	<array_element>
        elif self.array_element():
            return True
        
        # 260	<id_ext>	→	λ
        elif token in ['&&', '||', ',' , ')', '~', '+', '-', '/', '*', '%', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=']:
            print('id ext null')
            return True
        
        return False

    def array_size(self):
        

        # 261	<array_size>	→	id_lit
        if self.match("identifier"):
            return True
        # 262	<array_size>	→	positive_treasures_lit
        size = int(self.tokens[self.current_line][self.current_index][1])
        if size >=0 :
            self.advance()
            return True
    
        return False
    
     
    def determine_operation_type(self, content):
        """
        Analyze the content to determine operation type with complex combination rules.
        
        Args:
            content (list): A list of tokens to analyze
        
        Returns:
            str: The type of operation
        """
        # Remove closing parentheses and '~' if present
        content = [token for token in content if token not in [')', '~']]
        
        # Define operator types
        relational_ops = ['>', '<', '>=', '<=', '==', '!=']
        arithmetic_ops = ['+', '-', '*', '/', '%']
        logical_ops = ['&&', '||', 'and', 'or']
        
        # Check for the presence of each operator type
        has_relational = any(op in content for op in relational_ops)
        has_arithmetic = any(op in content for op in arithmetic_ops)
        has_logical = any(op in content for op in logical_ops)
        
        # Determine operation type based on rules
        if has_logical:
            return 'logical'
        
        if has_relational:
            return 'relational'
        
        if not has_relational and not has_logical and has_arithmetic:
            return 'arithmetic'
        
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
            # print({self.current_token()}, self.error_message)

    def get_parsing_result(self):
        """Return parsing result."""
        return self.parsing_result
    