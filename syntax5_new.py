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
        while True:
            if self.current_index + 1 < len(self.tokens[self.current_line]):
                self.current_index += 1
            elif self.current_line + 1 < len(self.tokens):
                self.current_line += 1
                self.current_index = 0
                while self.current_line < len(self.tokens) and not self.tokens[self.current_line]:  # Skip empty lines
                    self.current_line += 1
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
                self.error_message = f"Syntax Error: Expected treasures, but got '{full_token}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'identifier':
                self.error_message = f"Syntax Error: Missing identifier at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == ')':
                self.error_message = f"Syntax Error: Unclosed ( at Line {self.current_line}, Index {self.current_index + 1}"
            elif expected == ']':
                self.error_message = f"Syntax Error: Unclosed ] at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'return':
                self.error_message = f"Syntax Error: Missing return statement at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == '0':
                self.error_message = f"Syntax Error: Expected 0, but got '{full_token}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected == 'reign':
                self.error_message = f"Syntax Error: Program must end with 'reign'"
            elif expected == 'scroll_lit':
                self.error_message = f"Syntax Error: Expected scroll literal, but got '{full_token}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            elif expected in ['treasures_lit', '1', '0']:
                self.error_message = f"Syntax Error: Expected treasures literal, but got '{full_token}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            # else:
            #     self.error_message = f"Syntax Error: Expected {expected}, but got {full_token} at Line {self.current_line + 1}, Index {self.current_index + 1}"
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
        #2	<global_dec>	→	<var_dec> <global_dec>
        if self.var_dec():
            token = self.current_token()
            if token in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
                return self.global_dec()
            return True
        
        # 3	<global_dec>	→	λ
        token = self.current_token()
        return token in ['castle', 'spell']

    def var_dec(self):
        # 4	<var_dec>	→	<dynasty> <data_type> id_lit <vardec_def>
        if not self.dynasty():
            return False
        if not self.data_type():
            self.error_message = f"Syntax Error: Missing data type at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        self.advance()
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Missing variable name at Line {self.current_line + 1}, Index {self.current_index + 1}"
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
            self.error_message = f"Syntax Error: Missing data type at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False


    def vardec_def(self):
        token = self.current_token()
        print({self.current_token()}, "ente vardec_def  -----------------------------", self.current_token())
        # 7	<vardec_def>	→	<initialization> <vardec_more>~
        if self.initialization():
            if not self.vardec_more():
                return False
            if not self.match("~"):
                return False
            return True

        # 8	<vardec_def>	→	[treasures_lit] <column> <array_initialization> <array_more>~
        
        elif self.match('['):
            # Handle the first dimension (e.g., `identifier[2]`)
            print({self.current_token()}, "enter index vardec_def ", self.current_token())
            if not self.array_size() :  
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.current_token())}' at Line {self.current_line + 1}"
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
            if not self.match('~'):
                return False
            
            return True

        # self.error_message = f"Syntax Error: Expected '=', but got '{repr(self.current_token())}' at Line {self.current_line + 1}"
        self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False


    def array_size(self):
        size = int(self.tokens[self.current_line][self.current_index][1])
        # 9	<array_size>	→	id_lit
        if self.match("identifier"):
            return True
        # 10	<array_size>	→	positive_treasures_lit
        elif size >=0 :
            self.advance()
            return True
    
        return False

    def initialization(self):
        # 11	<initialization>	→	= <val>
        print({self.current_token()}, "init ---------------- ")
        if self.match('='):
            return self.val()
        # 12	<initialization>	→	λ 
        return self.current_token() in ['~', ',']

    def vardec_more(self):
        print({self.current_token()}, "vardec more", self.current_token())
        # 13	<vardec_more>	→	, id_lit <initialization> <vardec_more>
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            return self.vardec_more()
        # 14	<vardec_more>	→	λ
        return self.current_token() == '~'

    def column(self):
        # 15	<column>	→	[<array_size>]
        token = self.current_token()
        if self.match('['):
            if not self.array_size() :  
                self.error_message = f"Syntax Error: Invalid array size '{repr(self.current_token())}' at Line {self.current_line + 1}"
                return False
            if not self.match(']'):
                return False
            return True
        
        # 16	<column>	→	λ
        elif token in ['+=', '-=', '*=', '/=', '%=', '=', '&&', '||', ')', '+', '-', '/', '*', '%', '~', '<', '>', '<=', '>=', '==', '!=', '=', ',' , 'identifier', 'ocean_lit', 'treasures_lit', '(', '~']:  # End of the array definition
            return True  
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False 

    def array_initialization(self):
        token = self.current_token()
        # 17	<array_initialization>	→	= <array_list>  
        if self.match('='):
            if not self.array_list():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' must be an array list at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            return True
        # 18	<array_initialization>	→	λ
        elif token in [',', '~', '}']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False


    def array_list(self):
        # 19	<array_list>	→	{<array_content>}
        if not self.match('{'):
            return False

        if not self.array_content():
            return False

        if not self.match('}'):
            return False

        return True


    def array_content(self):
        # 20	<array_content>	→	<array_lit> <lit_more> 
        if self.array_lit():
            if not self.lit_more():
                return False
            return True

        # 21	<array_content>	→	{<array_row>} <row_more>
        elif self.match('{'):
            if not self.array_row():
                return False
            if not self.match('}'):
                return False
            if not self.row_more():
                return False
            return True
        
        # 22	<array_content>	→	id_lit <row_more>
        elif self.match('identifier'):
            if not self.row_more():
                return False
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False


    def array_row(self):
        # 23	<array_row>	→	<array_lit> <lit_more> 

        if not self.array_lit():
            return False

        if not self.lit_more():
            return False

        return True
    
    def row_more(self):
        token = self.current_token()
        # 24	<row_more>	→	, <row_more_ext>
        if self.match(','):
            if not self.row_more_ext():
                return False
            return True
        
        # 25	<row_more>	→	λ
        elif token == '}':
            return True  # If no more rows, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    
    def row_more_ext(self):
        # 25	<row_more_ext>	→	{<array_row>} <row_more>
        if self.match('{'):
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
        
    
    def lit_more(self):
        # 28	<lit_more>	→	, <array_lit> <lit_more>
        token = self.current_token()

        if self.match(','):
            if not self.array_lit():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.lit_more():
                return False
            return True

        # 29	<lit_more>	→	λ
        elif token == '}':
            return True  # If no more literals, end with closing bracket

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def array_more(self):
        # 30	<array_more>	→	, id_lit [<array_size>] <column> <array_initialization> <array_more>
        token = self.current_token()

        if self.match(','):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            print({self.current_token()}, "enter index", self.current_token())
            if not self.match('['):
                return False
            print({self.current_token()}, "enter array size", self.current_token())
            if not self.array_size():
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

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def array_lit(self):
        # 32	<array_lit>	→	id_lit
        if self.match('identifier'):
            return True
        
        #33	<array_lit>	→	<lit3> 
        elif self.lit3():
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
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
        
        else:
            self.error_message = f"Syntax Error: Invalid input // {repr(self.current_token)} at Line {self.current_line + 1}"
            return False

    def assignment_operand_1(self):
        print({self.current_token()}, "assignment_operand 1 ----------------------------")
        # 39	<assignment_operand_1>	→	id_lit <id_ext> <more_arith>
        if self.match('identifier'):
            print({self.current_token()}, "id ----------------------------")
            if not self.id_ext():
                return False
            print({self.current_token()}, "more_arith ----------------------------")
            if not self.more_arith():
                print({self.current_token()}, "more arith true ----------------------------")
                return False
            return True
        
        # 40	<assignment_operand_1>	→	<lit2> <more_arith>
        elif self.lit2():
            if not self.more_arith():
                return False
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input // {repr(self.current_token)} at Line {self.current_line + 1}"
            return False
    
    def assignment_operand_2(self):
        # 41	<assignment_operand_2>	→	<arithmetic_operand_2> <more_arith>
        if self.arithmetic_operand_2():
            if not self.more_arith():
                return False
            return True
        
    def assignment_operand(self):
        # 42	<assignment_operand>	→	<assignment_operand_1>
        if self.assignment_operand_1():
            return True
        # 43	<assignment_operand>	→	<assignment_operand_2>
        elif self.assignment_operand_2():
            return True
        
        return False
    
    def logical_exp(self):
        # 44	<logical_exp>	→	<logical_operand> <logical_operator> <logical_operand> <more_log>
        token = self.current_token()
        print({self.current_token()}, f"enter log_exp {token}")
        if self.logical_operand():
            print({self.current_token()}, f"passed log_operand {token}")
            if not self.logical_operator():
                self.error_message = f"Syntax Error: Invalid logical operator '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            print({self.current_token()}, f"passed log_operator {token}")
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid logical operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            print({self.current_token()}, f"passed log_operand {token}")
            if not self.more_log():
                return False

            return True
        
        # 45	<logical_exp>	→	<logical_operator1> <logical_operand> <more_log> 
        
        elif self.logical_operator1():
            if not self.logical_operand():
                self.error_message = f"Syntax Error: Invalid logical operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.more_log():
                return False
      
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def logical_operand_1(self):
        # 46	<logical_operand_1>	→	id_lit <id_ext> <more_arith> <relational_more>
        if not self.match('identifier'):
            return False
        if not self.id_ext():
            return False
        if not self.more_arith():
            return False
        if not self.relational_more():
            return False
        
        return True
    
    def logical_operand_2(self):
        # 47	<logical_operand_2>	→	<lit2> <more_arith> <relational_more>
        print({self.current_token()}, "logical operand 2 --------------------------")
        if self.lit2():
            if not self.more_arith():
                return False
            if not self.relational_more():
                return False
            return True

        # 48	<logical_operand_2>	→	scroll_lit <relational_more>
        elif self.match('scroll_lit'):
            if not self.relational_more():
                return False
            return True
        
        # 49	<logical_operand_2>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True
        
        # 50	<logical_operand_2>	→	<treasures_mirror>
        elif self.treasures_mirror():
            return True
        
        # 51	<logical_operand_2>	→	(<logical_op2_ext>
        elif self.match('('):
            if not self.logical_op2_ext():
                return False
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    
    def logical_operand(self):
        print({self.current_token()}, "logical operand --------------------")
        # 52	<logical_operand>	→	<logical_operand_1>
        if self.logical_operand_1():
            return True

        # 53	<logical_operand>	→	<logical_operand_2>
        elif self.logical_operand_2():
            return True
        
        return False
    
    def logical_op2_ext(self):
        # 54	<logical_op2_ext>	→	<expression>)
        print({self.current_token()}, "logical_op2_ex -------------- ")
        if self.expression():
            if not self.match(')'):
                return False
            return True

        # 55	<logical_op2_ext>	→	<relational_op2_ext> <relational_more>
        elif self.relational_op2_ext():
            if not self.relational_more():
                 return False
            return True
        
        return False
    
    def expression(self):
        # 56	<expression>	→	<logical_exp>
        if self.logical_exp():
            return True

        # 57	<expression>	→	<relational_exp>
        # elif self.relational_exp():
        #     return True
        
        return False
    
    def logical_operator(self):
        # 58	<logical_operator>	→	&&
        if self.match('&&'):
            print({self.current_token()}, "log operator && ----------------")
            return True
        # 59	<logical_operator>	→	||
        elif self.match('||'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    
    def logical_operator1(self):
        # 60	<logical_operator1>	→	!
        if self.match('!'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def more_log(self):
        token = self.current_token()
        print({self.current_token()}, "more log ------------------------")
        # 61	<more_log>	→	<logical_operator> <more_log_ext>
        if self.logical_operator():
            print({self.current_token()}, "Logical operator detected, continuing more_log_ext...")
            if not self.more_log_ext():
                return False
            return True
        
        # 62	<more_log>	→	λ
        elif token in [')', ',' ,'~', '&&', '||', ')']:
            print({self.current_token()}, f"End of logical expression detected: {token}")
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def more_log_ext(self):
        # 63	<more_log_ext>	→	<logical_operand><more_log>
        print({self.current_token()}, "more_log_ext ----------------")
        if self.logical_operand():
            if not self.more_log():
                return False
            return True

        # 64	<more_log_ext>	→	<logical_operator1> <logical_operand><more_log>
        elif self.logical_operator1():
            if not self.logical_operand():
                return False
            if not self.more_log():
                return False
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def treasures_mirror(self):
        # 65	<treasures_mirror>	→	1
        if self.match('1'):
            return True
        
        # 66	<treasures_mirror>	→	0
        elif self.match('0'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def arithmetic_exp(self):
        token = self.current_token()
        # 67	<arithmetic_exp>	→	<arithmetic_operand> <arithmetic_operator><arithmetic_operand><more_arith>
        print({self.current_token()}, f"Enter Arith_exp {token}")
        if not self.arithmetic_operand():
            self.error_message = f"Syntax Error: Invalid arithmetic operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        token = self.current_token()
        print({self.current_token()}, f"Enter Arith_operand success {token} ")
        if not self.arithmetic_operator():
            self.error_message = f"Syntax Error: Invalid arithmetic operator '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        token = self.current_token()
        print({self.current_token()}, f"Enter Arith_operator success {token}")
        if not self.arithmetic_operand():
            self.error_message = f"Syntax Error: Invalid arithmetic operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        token = self.current_token()
        print({self.current_token()}, f"Enter Arith_operand success {token}")
        if not self.more_arith():
            return False
        

        return True

    def arithmetic_operand_1(self):
        # 68	<arithmetic_operand_1>	→	id_lit <id_ext>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            return True

        # 69	<arithmetic_operand_1>	→	<lit2>
        elif self.lit2():
            return True
        
        return False
        
    def arithmetic_operand_2(self):
        # 70	<arithmetic_operand_2>	→	(<arithmetic_exp>)
        if self.match('('):
            if not self.arithmetic_exp():
                return False
            if not self.match(')'):
                return False
            return True
        
        return False
    
    def arithmetic_operand(self):
        # 71	<arithmetic_operand>	→	<arithmetic_operand_1>
        if self.arithmetic_operand_1():
            return True

        # 72	<arithmetic_operand>	→	<arithmetic_operand_2>
        elif self.arithmetic_operand_2():
            return True
        
        return False
    
    def arithmetic_operator(self):
        # 73	<arithmetic_operator>	→	+
        if self.match('+'):
            return True
        # 74	<arithmetic_operator>	→	-
        elif self.match('-'):
            return True
        # 75	<arithmetic_operator>	→	/
        elif self.match('/'):
            return True
        # 76	<arithmetic_operator>	→	*
        elif self.match('*'):
            return True
        # 77	<arithmetic_operator>	→	%
        elif self.match('%'):
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def more_arith(self):
        token = self.current_token()

        # 78	<more_arith>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
        print({self.current_token()}, f"more_arith {token}")

        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                self.error_message = f"Syntax Error: Expected operand but got '{repr(self.current_token())}' at Line {self.current_line + 1}"
                return False
            print({self.current_token()}, "more_arith_operand")
            return self.more_arith()  # Continue parsing if there's more arithmetic

        # 79	<more_arith>	→	λ
        elif token in ['<', '>', '<=', '>=', '==', '!=', ')', ',' ,'~', '&&', '||']:
            print({self.current_token()}, "more_arith null -------------------")
            return True  

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def relational_exp(self):
       # 80	<relational_exp>	→	<relational_operand> <relational_operator> <relational_operand> <relational_more> 
        print({self.current_token()}, "relational_exp ---------") 
        if not self.relational_operand():
            self.error_message = f"Syntax Error: Invalid relational operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        if not self.relational_operator():
            self.error_message = f"Syntax Error: Invalid relational operator '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        if not self.relational_operand():
            self.error_message = f"Syntax Error: Invalid relational operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        if not self.relational_more():
            return False

        return True
    
    def relational_operand_1(self):
        print({self.current_token()}, "rel op 1 -------------")
        # 81	<relational_operand_1>	→	id_lit <id_ext> <more_arith>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            if not self.more_arith():
                return False
            return True

        # 82	<relational_operand_1>	→	<lit2> <more_arith>
        elif self.lit2():
            if not self.more_arith():
                return False
            return True
        
        return False

    def relational_operand_2(self):
        # 83	<relational_operand_2>	→	scroll_lit
        if self.match('scroll_lit'):
            return True

        # 84	<relational_operand_2>	→	( <relational_op2_ext>
        elif self.match('('):
            if not self.relational_op2_ext():
                return False
            return True
        
        return False
    
    def relational_op2_ext(self):
        print({self.current_token()}, "relational_op2_ext ---------------")
        # 85	<relational_op2_ext>	→	<arithmetic_exp>) <more_arith>
        if self.arithmetic_exp():
            if not self.match(')'):
                return False
            if not self.more_arith():
                return False
            return True

        # 86	<relational_op2_ext>	→	<relational_exp>)
        elif self.relational_exp():
            if not self.match(')'):
                return False
            return True
        
        return False
    
    def relational_operand(self):
        # 87	<relational_operand>	→	<relational_operand_1>
        if self.relational_operand_1():
            return True

        # 88	<relational_operand>	→	<relational_operand_2>
        elif self.relational_operand_2():
            return True

        return False

    def relational_operator(self):
        # 89	<relational_operator>	→	<
        if self.match('<'):
            print({self.current_token()}, "rel operator < --------------------")
            return True 
        # 90	<relational_operator>	→	>
        elif self.match('>'):
            print({self.current_token()}, "rel operator > --------------------")
            return True
        # 91	<relational_operator>	→	<=
        elif self.match('<='):
            return True
        # 92	<relational_operator>	→	>=
        elif self.match('>='):
            return True
        # 93	<relational_operator>	→	==
        elif self.match('=='):
            return True
        # 94	<relational_operator>	→	!=
        elif self.match('!='):
            return True
        
    def relational_more(self):
        # 95	<relational_more>	→	<relational_operator> <relational_operand><relational_more>
        token = self.current_token()

        if self.relational_operator():
            if not self.relational_operand():
                self.error_message = f"Syntax Error: Invalid relational operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.relational_more():
                return False
            return True

        # 96	<relational_more>	→	λ
        elif token in [')', ',' ,'~', '&&', '||']:
            print( "relational_more nul ----------------- ", {self.current_token()})
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def unary(self):
        token = self.current_token()
        # 97	<unary>	→	id_lit <unary_operator>
        print({self.current_token()}, "Unary")
        if not self.match('identifier'):
            self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        print({self.current_token()}, f"This is {token}")
        if not self.unary_operator():
            self.error_message = f"Syntax Error: Invalid unary operator '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

        return True
    
    def unary_operator(self):
        # 98	<unary_operator>	→	++
        if self.match('++'):
            return True
        # 99	<unary_operator>	→	--
        elif self.match('--'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def string_operand2(self):
        # 100	<string_operand2>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        
        # 101	<string_operand2>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        
        # 102	<string_operand2>	→	toscroll(<conver_value>)
        elif self.match('toscroll'):
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        return False
    
    def string_operand(self):
        # 103	<string_operand>	→	id_lit <id_ext>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            return True
        
        # 104	<string_operand>	→	<string_operand2>
        elif self.string_operand2():
            return True
        
        return False
    

    def string_more(self):
        token = self.current_token()
        # 105	<string_more>	→	+ <string_operand> <string_more>
        if self.match('+'):
            if not self.string_operand():
                self.error_message = f"Syntax Error: Invalid string operand '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            return self.string_more()
        
        # 106	<string_more>	→	λ
        elif token in [',' , '~', ')']:
            return True
        
        return False
    
    def user_defined_func(self):

        token = self.current_token()

        # 107	<user-defined_func>	→	spell <return_type> id_lit(<param>) {<body><ret_statement>} <user-defined_func>
        if self.match('spell'):
            if not self.return_type():
                return False
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Missing function name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
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

        # 108	<user-defined_func>	→	λ
        elif token in ['castle', 'dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted', 'tale', 
                       'spell', 'id_lit', 'cast', 'forever', 'believe', 'return', 'break', 'continue', '~']:
            return True
        
        else: 
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def return_type(self):
        # 109	<return_type>	→	<data_type>
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
        
        # 110	<return_type>	→	chamber
        elif self.match('chamber'):
            return True
        
        else: 
            self.error_message = f"Syntax Error: Invalid return type '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def param(self):
        token = self.current_token()
        
        # 111	<param>	→	<data_type> id_lit <param_more>
        print({self.current_token()}, "enter param")
        if self.data_type():
            self.advance()
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.param_more():
                return False
            return True

        # 112	<param>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def param_more(self):
        token = self.current_token()

        # 113	<param_more>	→	, <data_type> id_lit <param_more>
        if self.match(','):
            if not self.data_type():
                self.error_message = f"Syntax Error: Missing data type '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            self.advance()
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.param_more():
                return False
            return True

        # 114	<param_more>	→	λ
        elif token == ')':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def body_1(self):
        token = self.current_token()
        print({self.current_token()}, "body1 ---------------")
        # 115	<body_1>	→	<var_dec> <body>
        if token in ['dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose']:
            if not self.var_dec():
                return False
            return self.body()

        # 116	<body_1>	→	<output> <body>
        elif token == 'granted':
            if not self.output():
                return False
            return self.body()
        
        # 117	<body_1>	→	<user-defined_func> <body>
        elif token == 'spell':
            if not self.user_defined_func():
                return False
            return self.body()
        
        # 118	<body_1>	→	<for_loop> <body>
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.body()
        
        # 119	<body_1>	→	id_lit <body_id_ext> <body>
        elif self.match('identifier'):
            print({self.current_token()}, "id ----------------------------")
            if not self.body_id_ext():
                return False
            return self.body()
        
    def body_id_ext(self):
        # 120	<body_id_ext>	→	(<args>)~
        print({self.current_token()}, "id ext ---------------")
        if self.match('('):
            if not self.args():
                return False
            if not self.match(')'):
                return False
            if not self.match('~'):
                return False
            return True

        # 121	<body_id_ext>	→	<unary_operator>~
        elif self.unary_operator():
            if not self.match('~'):
                return False
            return True

        # 122	<body_id_ext>	→	<index> <index_ext>
        elif self.index():
            print({self.current_token()}, "index ----------------------------")
            if not self.index_ext():
                return False
            return True

        return False
    

    def index_ext(self):
        # 124	<index_ext>	→	 = <val> ~
        print({self.current_token()}, "index ext ---------------")
        if self.match('='):
            if not self.val():
                return False
            if not self.match('~'):
                return False
            return True
        
        # 125	<index_ext>	→	<assignment_operator> <assignment_operand> ~
        elif self.assignment_operator():
            print({self.current_token()}, "assignment_operator ----------------------------")
            if not self.assignment_operand():
                print({self.current_token()}, "assignment_operand ----------------------------")
                return False
            if not self.match('~'):
                return False
            return True
        
        return False
    

    def body_2(self):
        # 124	<body_2>	→	<condi_statement> <body>
        if self.condi_statement():
            return self.body()
        
        return False
    
    def body(self):
        print({self.current_token()}, "body ---------------")
        token = self.current_token()
        # 125	<body>	→	<body_1>
        if self.body_1():
            return True

        # 126	<body>	→	<body_2>
        elif self.body_2():
            return True
        
        # 127	<body>	→	λ
        elif token in ['return', '}', 'break', 'continue']:
            return True
        
        return False

    def ret_statement(self):
        token = self.current_token()
        print({self.current_token()}, f"This is {token}")

        # 128	<ret_statement>	→	return <val4> ~
        if self.match('return'):
            if not self.val4():
                return False
            if not self.match('~'):
                return False
            return True

        # 129	<ret_statement>	→	λ
        elif token == '}':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def condi_statement(self):
        token = self.current_token()
        # 130	<condi_statement>	→	<if>
        if token == 'cast':
            return self.if_statement()

        # 131	<condi_statement>	→	<while>
        elif token == 'forever':
            return self.while_statement()

        # 132	<condi_statement>	→	<do_while>
        elif token == 'believe':
            return self.do_while_statement()
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    
    def for_loop(self):
        # 133	<for_loop>	→	tale (<loop_var> ~ <relational_exp> ~ <unary>) {<loop_body>}
        if not self.match('tale'):
            return False
        if not self.match('('):
            return False
        if not self.loop_var():
            return False
        if not self.match('~'):
            return False
        if not self.relational_exp():
            return False
        if not self.match('~'):
            return False
        if not self.unary():
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

    def loop_var(self):
        # 134	<loop_var>	→	treasures id_lit = <loop_val>
        if self.match('treasures'):
            if not self.match('identifier'):
                self.error_message = f"Syntax Error: Missing variable name '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match('='):
                return False
            if not self.loop_val():
                return False
            return True

        # 135	<loop_var>	→	id_lit <loop_init>
        elif self.match('identifier'):
            if not self.loop_init():
                return False
            return True
    
    def loop_init(self):
        token = self.current_token()

        # 136	<loop_init>	→	=  <loop_val>
        if self.match('='):
            if not self.loop_val():
                return False
            return True

        # 137	<loop_init>	→	λ
        elif token == '~':
            return True
        
        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    def loop_val(self):
        # 138	<loop_val>	→	id_lit
        if self.match('identifier'):
            return True
        # 139	<loop_val>	→	treasures_lit
        elif self.match('treasures_lit') or self.match('0') or self.match('1'):
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False


    def loop_body(self):
        # 140	<loop_body>	→	<body_1>
        if self.body_1():
            return True
        
        # 141	<loop_body>	→	<if_break>
        elif self.if_break():
            return True
        
        # 142	<loop_body>	→	<while>
        elif self.while_statement():
            return True
        
        # 143	<loop_body>	→	<do_while>
        elif self.do_while_statement():
            return True
        
        return False
    

    def if_break(self):
        # 144	<if_break>	→	cast (<condition>) {<body><flow_control>} <elif_break> <else_break>
        if not self.match('cast'):
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
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
        if not self.flow_control():
            return False
        if not self.match('}'):
            return False
        if not self.elif_break():
            return False
        if not self.else_break():
            return False
        return True
    
    def elif_break(self):
        token = self.current_token()

        # 145	<elif_break>	→	twist(<condition>) {<body><flow_control>}<elif_break>
        if self.match('twist'):
            if not self.match('('):
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.condition():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(')'):
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match('{'):
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.body():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.flow_control():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match('}'):
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.elif_break():
                self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            return True

        # 146	<elif_break>	→	λ
        elif token in ['curse', '}']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        
    
    def else_break(self):
        token = self.current_token()

        # 147	<else_break>	→	curse {<body><flow_control>}
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.flow_control():
                return False
            if not self.match('}'):
                return False
            return True

        # 148	<else_break>	→	λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def flow_control(self):
        token = self.current_token()

        # 149	<flow_control>	→	break~
        if self.match('break'):
            if not self.match('~'):
                return False
            return True
        
        # 150	<flow_control>	→	continue~
        elif self.match('continue'):
            if not self.match('~'):
                return False
            return True
        
        # 151	<flow_control>	→	λ
        elif token == '}':
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def do_while_statement(self):
        # 152	<do_while>	→	believe {<loop_body>} forever(<condition>)~
        if not self.match('believe'):
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        if not self.match('{'):
            return False
        if not self.loop_body():
            return False
        if not self.match('}'):
            return False
        if not self.match('forever'):
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
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
    
    def condition(self):
        # 153	<condition>	→	<treasures_mirror>
        if self.treasures_mirror():
            return True

        # 154	<condition>	→	id_lit <condi_ext> <more_log>
        elif self.match('identifier'):
            if not self.condi_ext():
                return False
            if not self.more_log():
                return False
            return True
         
        # 155	<condition>	→	<lit2> <more_arith> <relational_more>
        elif self.lit2():
            if not self.more_arith():
                return False
            if not self.relational_more():
                return False
            
        # 156	<condition>	→	scroll_lit <relational_operator> <relational_operand> <relational_more> 
        elif self.match('scroll_lit'):
            if not self.relational_operator():
                return False
            if not self.relational_operand():
                return False
            if not self.relational_more():
                return False
            return True
        
        # 157	<condition>	→	( <relational_op2_ext> <relational_more>
        elif self.match('('):
            if not self.relational_op2_ext():
                return False
            if not self.relational_more():
                return False
            return True
        
        # 158	<condition>	→	<logical_operand_2> <logical_operator> <logical_operand> <more_log>
        elif self.logical_operand_2():
            if not self.logical_operator():
                return False
            if not self.logical_operand():
                return False
            if not self.more_log():
                return False
            return True
        
        # 159	<condition>	→	<logical_operator1> <logical_operand_2> <more_log> 
        elif self.logical_operator1():
            if not self.logical_operand_2():
                return False
            if not self.more_log():
                return False
            return True
        
        # 160	<condition>	→	<logical_operator1> <log_op1_ext>
        elif self.logical_operator1():
            if not self.log_op1_ext():
                return False
            return True
        
        return False


    def log_op1_ext(self):
        # 162	<log_op1_ext>	→	<logical_operand_2> <more_log> 
        if self.logical_operand_2():
            if not self.more_log():
                return False
            return True
        
        # 163	<log_op1_ext>	→	(<condition>)

        if self.match('('):
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            return True
        
        return False

    def condi_ext(self):
        token = self.current_token()
        # 161	<condi_ext>	→	<mirror_init>
        if self.mirror_init():
            return True
        
        # 162	<condi_ext>	→	<more_arith> <more_log>
        elif self.more_arith():
            if not self.more_log():
                return False
            return True
        
        # 163	<condi_ext>	→	(<args>)
        elif self.match('('):
            if not self.args():
                return False
            if not self.match(')'):
                return False
            return True
        
        # 164	<condi_ext>	→	<index>
        elif self.index():
            return True
        
        # 165	<condi_ext>	→	λ Follow set
        elif token in ['&&', '||', ')']:
            return True

        return False
    
    def mirror_init(self):
        # 166	<mirror_init>	→	== mirror_lit
        if self.match('=='):
            if not self.match('mirror_lit'):
                return False
            return True

        # 167	<mirror_init>	→	!= mirror_lit
        elif self.match('!='):
            if not self.match('mirror_lit'):
                return False
            return True
        
        return False


    def while_statement(self):
        # 168	<while>	→	forever (<condition>) {<loop_body>}
        token = self.current_token()
        if not self.match('forever'):
            return False
        print({self.current_token()}, f"passed forever {token}")
        if not self.match('('):
            return False
        print({self.current_token()}, f"passed ( {token}")
        if not self.condition():
            return False
        print({self.current_token()}, f"passed condition {token}")
        if not self.match(')'):
            return False
        print({self.current_token()}, f"passed ) {token}")
        if not self.match('{'):
            return False
        print({self.current_token()}, f"passed open curly {token}")
        if not self.loop_body():
            return False
        print({self.current_token()}, f"passed loop body {token}")
            
        if not self.match('}'):
            return False
        print({self.current_token()}, f"passed close curly {token}")
        return True
        
    
    def if_statement(self):
        # 169	<if>	→	cast (<condition>) {<body>} <elif> <else>
        if not self.match('cast'):
            return False
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
    
    def elif_statement(self):
        token = self.current_token()

        # 170	<elif>	→	twist(<condition>) {<body>}<elif>
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

        # 171	<elif>	→	λ
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted', 'tale',  
                       'spell', 'id_lit', 'cast', 'forever', 'believe', 'return', 'break', 'continue', '}', 'curse']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def else_statement(self):
        token = self.current_token()

        # 172	<else>	→	curse {<body>}
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.match('}'):
                return False
            return True
        
        # 173	<else>	→	λ
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'granted', 'tale',  
                       'spell', 'id_lit', 'cast', 'forever', 'believe', 'return', 'break', 'continue', '}']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False

    def output(self):
        # 174	<output>	→	granted(<granted_content> <more_granted>) ~
        if not self.match('granted'):
            return False
        if not self.match('('):
            return False
        if not self.granted_content():
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        print({self.current_token()}, "------------------")
        if not self.more_granted():
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
        if not self.match(')'):
            return False
        if not self.match('~'):
            return False
        return True
    
    def granted_content(self):
        token = self.current_token()
        # 176	<granted_content>	→	id_lit <granted_id_ext>
        if self.match('identifier'):
            if not self.granted_id_ext():
                return False
            return True
        
        # 177	<granted_content>	→	scroll_lit <granted_lit_ext_1>
        elif self.match('scroll_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 178	<granted_content>	→	rose_lit <granted_lit_ext_1>
        elif self.match('rose_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 179	<granted_content>	→	treasures_lit <granted_lit_ext_2>
        elif (self.match('treasures_lit') or self.match('1') or self.match('0')):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 180	<granted_content>	→	ocean_lit <granted_lit_ext_2>
        elif self.match('ocean_lit'):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 181	<granted_content>	→	mirror_lit <more_log>
        elif self.match('mirror_lit'):
            if not self.more_log():
                return False
            return True
        
        # 182	<granted_content>	→	phantom
        elif self.match('phantom'):
            return True
        
        # 183	<granted_content>	→	<set_precision>
        elif self.match('setprecission'):
            return True
        
        # 184	<granted_content>	→	<conversion_func_2> (<conversion_value>)
        elif self.conversion_func_2():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        # 185	<granted_content>	→	<conversion_func_1> (<conversion_value>) <string_more>
        elif self.conversion_func_1():
            print({self.current_token()}, "enter coversion func1 -----------------")
            if not self.match('('):
                return False
            print({self.current_token()}, "enter coversion func1 -----------------")
            if not self.conversion_value():
                return False
            print({self.current_token()}, "enter coversion func1 -----------------")
            if not self.match(')'):
                return False
            print({self.current_token()}, "enter coversion func1 -----------------")
            if not self.string_more():
                return False
            return True
        
        # 186	<granted_content>	→	( <granted_content_ext>
        elif self.match('('):
            if not self.granted_content_ext():
                return False
            return True
        
        # 187	<granted_content>	→	<logical_operator1> <logical_operand> <more_log> 
        elif self.logical_operator1():
            if not self.logical_operand():
                return False
            if not self.more_log():
                return False
            return True
        
        # 188	<granted_content>	→	<teasures_mirror> <more_log>
        elif self.treasures_mirror():
            if not self.more_log():
                return False
            return True
        
        return False
    
    def granted_id_ext(self):
        token = self.current_token()
        # 189	<granted_id_ext>	→	<unary_operator>
        if self.unary_operator():
            return True
        
        # 190	<granted_id_ext>	→	<id_ext> <other_ext>
        elif self.id_ext():
            if not self.other_ext():
                return False
            return True
        
        # 191	<granted_id_ext>	→	λ
        elif token in [',', '~']:
            return True

        return False
    
    def other_ext(self):
        token = self.current_token()
        # 192	<other_ext>	→	<string_more>
        if self.string_more():
            return True

        # 193	<other_ext>	→	<more_arith> <relational_more> <more_log>
        elif self.more_arith():
            if not self.relational_more():
                return False
            if not self.more_log():
                return False
            return True
        
        # 194	<other_ext>	→	<more_log>
        elif self.more_log():
            return True
        
        # 195	<other_ext>	→	<relational_more>
        elif self.relational_more():
            return True
        
        # 196	<other_ext>	→	λ
        elif token in [',', '~']:
            return True

        return False

    def granted_content_ext(self):
        # 197	<granted_content_ext>	→	<arithmetic_exp>) <more_arith> <relational_more> <more_log>
        if self.arithmetic_exp():
            if not self.match(')'):
                return False
            if not self.more_arith():
                return False
            if not self.relational_more():
                return False
            if not self.more_log():
                return False
            return True
        
        # 198	<granted_content_ext>	→	<relational_exp>) <more_log>
        elif self.relational_exp():
            if not self.match(')'):
                return False
            if not self.more_log():
                return False
            return True
        
        # 199	<granted_content_ext>	→	<logical_exp>) <more_log>
        elif self.logical_exp():
            if not self.match(')'):
                return False
            if not self.more_log():
                return False
            return True
        
        return False
    
    def granted_lit_ext_1(self):
        token = self.current_token()
        # 200	<granted_lit_ext_1>	→	<string_more>
        if self.string_more():
            return True
        
        # 201	<granted_lit_ext_1>	→	<relational_more>
        elif self.relational_more():
            return True
        
        # 202	<granted_lit_ext_1>	→	λ
        elif token in [',', '~']:
            return True

        return False


    def granted_lit_ext_2(self):
        token = self.current_token()
        # 203	<granted_lit_ext_2>	→	<more_arith> <relational_more> <more_log>
        if self.more_arith():
            if not self.relational_more():
                return False
            if not self.more_log():
                return False
            return True
        
        # 204	<granted_lit_ext_2>	→	<relational_more>
        elif self.relational_more():
            return True
        
        # 205	<granted_lit_ext_2>	→	λ
        elif token in [',', '~']:
            return True
        
        return False
    
    def set_precision(self):
        # 207	<set_precision>	→	%.treasures_litf
        if not self.match('%'):
            return False
        if not self.match('.'):
            return False
        if not (self.match('treasures_lit') or self.match('1') or self.match('0')):
            return False
        if not self.match('f'):
            return False
        
        return True
        

    def more_granted(self):
        token = self.current_token()

        # 198	<more_granted>	→	, <granted_content> <more_granted>
        if token == ',':
            if not self.match(','):
                return False
            if not self.granted_content():
                return False
            if not self.more_granted():
                return False
            return True

        # 199	<more_granted>	→	λ
        elif token == ')':
            print({self.current_token()}, "enter null more granted ---------")
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
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
        self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
        return False
    
    def val(self):
        token = self.current_token()
        # 215	<val>	→	lengthof(<id_lit>)
        if self.match('lengthof'):
            if not self.match('('):
                return False
            if not self.match('identifier'):
                return False
            if not self.match(')'):
                return False
            return True
        
        # 216	<val>	→	scroll_lit <granted_lit_ext_1>
        elif self.match('scroll_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 217	<val>	→	rose_lit <granted_lit_ext_1>
        elif self.match('rose_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 218	<val>	→	mirror_lit <more_log>
        elif self.match('mirror_lit'):
            if not self.more_log():
                return False
            return True
        
        # 219	<val>	→	ocean_lit  <granted_lit_ext_2>
        elif self.match('ocean_lit'):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 220	<val>	→	treasures_lit  <granted_lit_ext_2>
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 221	<val>	→	phantom
        elif self.match('phantom'):
            return True
        
        # 222	<val>	→	<conversion_func_2> (<conversion_value>)
        elif self.conversion_func_2():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        # 223	<val>	→	<conversion_func_1> (<conversion_value>) <string_more>
        elif self.conversion_func_1():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            if not self.string_more():
                return False
            return True
        
        # 224	<val>	→	<input>
        elif token == 'wish':
            if not self.input():
                return False
            return True
        
        # 225	<val>	→	<treasures_mirror> <more_log>
        elif self.treasures_mirror():
            if not self.more_log():
                return  False
            return True
        
        # 226	<val>	→	(<logical_op2_ext> <more_log>
        elif self.match('('):
            print({self.current_token()}, '( --------------------- ')
            if not self.logical_op2_ext():
                return False
            if not self.more_log():
                return False
            return True
        
        # 227	<val>	→	id_lit <granted_id_ext>
        elif self.match('identifier'):
            if not self.granted_id_ext():
                return False
            return True
        
        # 229	<val>	→	<logical_operator1> <logical_operand> <more_log> 

        elif self.logical_operator1():
            if not self.logical_operand():
                return False
            if not self.more_log():
                return False
            return True
        
        return False
    
    def val4(self):
        # 228	<val4>	→	<val>
        token = self.current_token()
        # 215	<val>	→	lengthof(<id_lit>)
        if self.match('lengthof'):
            if not self.match('('):
                return False
            if not self.match('identifier'):
                return False
            if not self.match(')'):
                return False
            return True
        
        # 216	<val>	→	scroll_lit <granted_lit_ext_1>
        elif self.match('scroll_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 217	<val>	→	rose_lit <granted_lit_ext_1>
        elif self.match('rose_lit'):
            if not self.granted_lit_ext_1():
                return False
            return True
        
        # 218	<val>	→	mirror_lit <more_log>
        elif self.match('mirror_lit'):
            if not self.more_log():
                return False
            return True
        
        # 219	<val>	→	ocean_lit  <granted_lit_ext_2>
        elif self.match('ocean_lit'):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 220	<val>	→	treasures_lit  <granted_lit_ext_2>
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            if not self.granted_lit_ext_2():
                return False
            return True
        
        # 221	<val>	→	phantom
        elif self.match('phantom'):
            return True
        
        # 222	<val>	→	<conversion_func_2> (<conversion_value>)
        elif self.conversion_func_2():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            return True
        
        # 223	<val>	→	<conversion_func_1> (<conversion_value>) <string_more>
        elif self.conversion_func_1():
            if not self.match('('):
                return False
            if not self.conversion_value():
                return False
            if not self.match(')'):
                return False
            if not self.string_more():
                return False
            return True
        
        # 224	<val>	→	<input>
        elif token == 'wish':
            if not self.input():
                return False
            return True
        
        # 225	<val>	→	<treasures_mirror> <more_log>
        elif self.treasures_mirror():
            if not self.more_log():
                return  False
            return True
        
        # 226	<val>	→	(<logical_op2_ext>
        elif self.match('('):
            if not self.logical_op2_ext():
                return False
            return True
        
        # 227	<val>	→	id_lit <granted_id_ext> & # 229	<val4>	→	id_lit <val4_ext>
        elif self.match('identifier'):
            if self.granted_id_ext():
                return True
            elif self.val4_ext():
                return True
            return False
        
        return False
        
    def val4_ext(self):
        # 230	<val4_ext>	→	<unary_operator>
        if self.unary_operator():
            return True
        
        # 31	<val4_ext>	→	<index> <assignment_operator> <assignment_operand>
        elif self.index():
            if not self.assignment_operator():
                return False
            if not self.assignment_operand():
                return False
            return True
        
        return False


    # def type_conversion(self):
    #     # 232	<type_conversion>	→	<conversion_func> (<conversion_value>)
    #     if not self.conversion_func():
    #         return False
    #     if not self.match('('):
    #         return False
    #     if not self.conversion_value():
    #         return False
    #     if not self.match(')'):
    #         return False
    #     return True

    def conversion_func_1(self):
        # 233	<conversion_func_1>	→	toscroll
        if self.match('toscroll'):
            return True
        
        # 234	<conversion_func_1>	→	torose
        elif self.match('torose'):
            return True
        
        return False
    

    def conversion_func_2(self):
        # 235	<conversion_func_2>	→	totreasures
        if self.match('totreasures'):
            return True
        
        # 236	<conversion_func_2>	→	toocean
        elif self.match('toocean'):
            return True
        
        # 237	<conversion_func_2>	→	tomirror
        elif self.match('tomirror'):
            return True
        
        return False

    def conversion_func(self):
        # 238	<conversion_func>	→	<conversion_func_1>
        if self.conversion_func_1():
            return True
        
        elif self.conversion_func_2():
            # 239	<conversion_func>	→	<conversion_func_2>
            return True
        
        return False
    
    def conversion_value(self):
        # 240	<conversion_value>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        
        # 241	<conversion_value>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        
        # 242	<conversion_value>	→	ocean_lit
        elif self.match('ocean_lit'):
            return True
        
        # 243	<conversion_value>	→	treasures_lit
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            return True
        
        # 244	<conversion_value>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True
        
        # 245	<conversion_value>	→	id_lit <conversion_val_ext>
        elif self.match('identifier'):
            if not self.id_ext():
                return False
            return True
        
        return False
    
    def index(self):
        token = self.current_token()

        # 246	<index>	→	[<array_size>] <column>
        if self.match('['):
            if not self.array_size():
                self.error_message = f"Syntax Error: Invalid array index '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(']'):
               return False
            print({self.current_token()}, "index-done")
            if not self.column():
                return False
            print({self.current_token()}, "column")
            return True

        # 247	<index>	→	λ
        # elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{', '+=', '-=', '*=', '/=', '%=']:
        elif token in ['+=', '-=', '*=', '/=', '%=', '=', '&&', '||', ')', '+', '-', '/', '*', '%', '~', '<', '>', '<=', '>=', 
                        '==', '!=', '=', ',' , 'identifier', 'ocean_lit', 'treasures_lit', '(']:
            print({self.current_token()}, "index null---------------")
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
            
    def column(self): 
        token = self.current_token()

        # 248	<column>	→	[<array_size>]
        if self.match('['):
            if not self.array_size():
                self.error_message = f"Syntax Error: Invalid array index '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
                return False
            if not self.match(']'):
                return False
            return True

        # 249	<column>	→	λ
        # elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{', '+=', '-=', '*=', '/=', '%=' ]:
        elif token in ['+=', '-=', '*=', '/=', '%=', '=', '&&', '||', ')', '+', '-', '/', '*', '%', '~', '<', '>', '<=', '>=', 
                        '==', '!=', '=', ',' , 'identifier', 'ocean_lit', 'treasures_lit', '(', '~']:
            return True

        else:
            self.error_message = f"Syntax Error: Invalid input '{repr(self.current_token())}' at Line {self.current_line + 1}, Index {self.current_index + 1}"
            return False
    
    def input(self):
        # 250	<input>	→	wish (scroll_lit)
        if not self.match('wish'):
            return False
        if not self.match('('):
            return False
        if not self.match('scroll_lit'):
            return False
        if not self.match(')'):
            return False
        return True
    
    def lit1(self):
        # 251	<lit1>	→	scroll_lit
        if self.match('scroll_lit'):
            return True
        
        # 252	<lit1>	→	rose_lit
        elif self.match('rose_lit'):
            return True
        
        # 253	<lit1>	→	mirror_lit
        elif self.match('mirror_lit'):
            return True

        return False
    
    def lit2(self):
        print({self.current_token()}, "lit 2----------------------------")
        # 254	<lit2>	→	ocean_lit
        if self.match('ocean_lit'):
            return True
        
        #255	<lit2>	→	treasures_lit
        elif self.match('treasures_lit') or self.match('1') or self.match('0'):
            print({self.current_token()}, "treasures_lit ----------------------------")
            return True

        return False
    
    def lit3(self):
        # 256	<lit3>	→	<lit1>      
        if self.lit1():
            return True
        
        # 257	<lit3>	→	<lit2>
        elif self.lit2():
            print({self.current_token()}, "lit2----------------------------")
            return True
        
        return False
    
    def func_call(self):
        # 258	<func_call>	→	(<args>)

        if not self.match('('):
            print({self.current_token()}, "(----------------------------")
            return False
        if not self.args():
            return False
        if not self.match(')'):
            print({self.current_token()}, ")----------------------------")
            return False
        
        return True
    
    def args(self):
        print({self.current_token()}, "args ----------------------------")
        token = self.current_token()
        # 259	<args>	→	<args_val> <args_more>
        if self.args_val():
            print({self.current_token()}, "args val----------------------------")
            if not self.args_more():
                return False
            return True
        
        # 260	<args>	→	λ
        elif token in [')', ',']:
            return True
        
        return False
    
    def args_val(self):
        # 261	<args_val>	→	id_lit <id_ext>
        if self.match('identifier'):
            if not self.id_ext():
                return False
            return True

        # 262	<args_val>	→	<lit3>
        elif self.lit3():
            print({self.current_token()}, "lit 3----------------------------")
            return True
        
        return False
    
    def args_more(self):
        print({self.current_token()}, "args more----------------------------")
        token = self.current_token()
        # 263	<args_more>	→	, <args_val> <args_more>
        if self.match(','):
            if not self.args_val():
                return False
            if not self.args_more():
                print({self.current_token()}, "args more 1----------------------------")
                return False
            return True
        
        # 264	<args_more>	→	λ
        elif token in [')', ',']:
            return True
        
        return False
    
    def array_element(self):
        # 265	<array_element>	→	<index>
        if self.index():
            return True
        
        return False
    
    def id_ext(self):
        token = self.current_token()
        # 266	<id_ext>	→	<func_call>
        if self.func_call():
            print({self.current_token()}, "func call----------------------------")
            return True
        
        # 267	<id_ext>	→	<array_element>
        elif self.array_element():
            return True
        
        # 268	<id_ext>	→	λ
        elif token in ['+', '-', '/', '*', '%', '~', '<', '>', '<=', '>=', '==', '!=', '=', ')', ',' , 
                '&&', '||', 'identifier', 'ocean_lit', 'treasures_lit', '(', ')']:
            return True
        
        return False

     

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
            # print({self.current_token()}, self.error_message)

    def get_parsing_result(self):
        """Return parsing result."""
        return self.parsing_result
    