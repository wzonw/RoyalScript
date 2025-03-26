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

        # Store tokens of the current statement (we store full token tuples)
        self.current_statement_tokens = []  

        # Store finalized statements with their labels
        self.final_statements_list = []

    def current_token(self):
        """Return the current token type (a string) in the current line, skipping empty lines."""
        while self.current_line < len(self.tokens):
            if self.tokens[self.current_line]:  # Ensure line is not empty
                if self.current_index < len(self.tokens[self.current_line]):
                    # Return only the token type (the first element of the tuple)
                    return self.tokens[self.current_line][self.current_index][0]
            self.current_line += 1
            self.current_index = 0
        return None  # End of tokens

    def current_token_tuple(self):
        """Return the entire token tuple (type, value) of the current token (if any)."""
        if self.current_line < len(self.tokens) and self.current_index < len(self.tokens[self.current_line]):
            return self.tokens[self.current_line][self.current_index]
        return None

    def peek_next_token(self):
        """Peek at the next token type without advancing the position."""
        if self.current_line < len(self.tokens):
            temp_line, temp_index = self.current_line, self.current_index
            if temp_index + 1 < len(self.tokens[temp_line]):  # Next token in same line
                return self.tokens[temp_line][temp_index + 1][0]
            elif temp_line + 1 < len(self.tokens) and self.tokens[temp_line + 1]:
                return self.tokens[temp_line + 1][0][0]
        return None  # No more tokens

    def advance(self):
        """Move to the next token, automatically skipping comments and empty lines."""
        token_tuple = self.current_token_tuple()  # Get the full (type, value) tuple.
        if token_tuple:
            self.current_statement_tokens.append(token_tuple)  # Store full tuple.
        while True:
            if self.current_index + 1 < len(self.tokens[self.current_line]):
                self.current_index += 1
            elif self.current_line + 1 < len(self.tokens):
                self.current_line += 1
                self.current_index = 0
                while self.current_line < len(self.tokens) and not self.tokens[self.current_line]:
                    self.current_line += 1
            else:
                return None  # End of tokens
            # Automatically skip comment tokens
            if self.current_token() not in ["single_comment", "multi_comment"]:
                break

    def set_error(self, message, expected=None):
        """Helper to set a detailed error message using the current token tuple."""
        token_detail = self.current_token_tuple()
        token_str = repr(token_detail) if token_detail is not None else "None"
        if expected:
            self.error_message = (f"Syntax Error: {message} - Expected {expected}, but got {token_str} "
                                  f"at Line {self.current_line + 1}, Index {self.current_index + 1}")
        else:
            self.error_message = (f"Syntax Error: {message} at Line {self.current_line + 1}, "
                                  f"Index {self.current_index + 1}")

    def store_completed_statement(self, statement_type):
        """Store the completed statement with its type and reset tracking.
        Filters out specific special tokens before storing and prints debug info."""
        if self.current_statement_tokens:
            filtered_tokens = []
            i = 0
            while i < len(self.current_statement_tokens):
                current_token = self.current_statement_tokens[i]
                # Remove special tokens such as crown~, reign~, and EOF.
                if (i + 1 < len(self.current_statement_tokens) and 
                    isinstance(current_token, tuple) and len(current_token) >= 2 and 
                    current_token[0] == "crown" and current_token[1] == "crown" and
                    isinstance(self.current_statement_tokens[i+1], tuple) and 
                    self.current_statement_tokens[i+1][0] == "~" and self.current_statement_tokens[i+1][1] == "~"):
                    i += 2  # Skip both tokens
                    continue
                if (i + 1 < len(self.current_statement_tokens) and 
                    isinstance(current_token, tuple) and len(current_token) >= 2 and 
                    current_token[0] == "reign" and current_token[1] == "reign" and
                    isinstance(self.current_statement_tokens[i+1], tuple) and 
                    self.current_statement_tokens[i+1][0] == "~" and self.current_statement_tokens[i+1][1] == "~"):
                    i += 2  # Skip both tokens
                    continue
                if (isinstance(current_token, tuple) and 
                    ((len(current_token) == 1 and current_token[0] == "EOF") or 
                     (len(current_token) >= 2 and current_token[0] == "EOF" and current_token[1] == "EOF"))):
                    i += 1  # Skip this token
                    continue
                filtered_tokens.append(current_token)
                i += 1
            labeled_statement = [statement_type] + filtered_tokens
            print(f"[DEBUG] Original tokens: {self.current_statement_tokens}")
            print(f"[DEBUG] Filtered tokens: {filtered_tokens}")
            print(f"[DEBUG] Final labeled statement: {labeled_statement}")
            self.final_statements_list.append(labeled_statement)
            self.current_statement_tokens = []
            print(f"[DEBUG] Stored statement: {statement_type} with {len(filtered_tokens)} tokens (removed special tokens)")

    # -------------------------------
    # Parser methods (all error assignments now call set_error)
    # -------------------------------

    def match(self, expected):
        """Match the current token type against the expected value while ignoring comments."""
        while self.current_token() in ["single_comment", "multi_comment"]:
            self.advance()
        token = self.current_token()
        if token == expected:
            self.advance()
            return True
        full_token = self.current_token_tuple()
        if token is None:
            self.set_error("Unexpected end of input")
        else:
            if expected == 'crown':
                self.set_error("Program must start with 'crown'", expected)
            elif expected == '~':
                self.set_error("Missing tilde '~'", expected)
            elif expected == 'castle':
                self.set_error("Program must have a main function starting with 'castle'", expected)
            elif expected == 'treasures':
                self.set_error("Expected treasures", expected)
            elif expected == 'identifier':
                self.set_error("Missing identifier", expected)
            elif expected == ')':
                self.set_error("Unclosed (", expected)
            elif expected == ']':
                self.set_error("Unclosed ]", expected)
            elif expected == 'return':
                self.set_error("Missing return statement", expected)
            elif expected == '0':
                self.set_error("Expected 0", expected)
            elif expected == 'reign':
                self.set_error("Program must end with 'reign'", expected)
            elif expected == 'scroll_lit':
                self.set_error("Expected scroll literal", expected)
            elif expected == 'treasures_lit':
                self.set_error("Expected treasures literal", expected)
        print(f"Matching expected: {repr(expected)} | Current token: {self.current_token_tuple()}")
        return False

    def program(self):
        # <program> → crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~
        self.error_message = ""
        while self.current_token() in ["single_comment", "multi_comment"]:
            self.advance()
        if not self.match("crown") or not self.match("~"):
            return False
        if not self.global_dec():
            return False
        if not self.user_defined_func():
            return False
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
        return self.match("EOF")

    def global_dec(self):
        if self.var_dec():
            token = self.current_token()
            if token in ['dynasty', 'scroll', 'mirror', 'ocean', 'treasures', 'rose']:
                return self.global_dec()
            return True
        token = self.current_token()
        return token in ['castle', 'spell', 'reign']

    def var_dec(self):
        if not self.dynasty():
            return False
        if not self.data_type():
            self.set_error("Missing data type", "data_type")
            return False
        self.advance()
        if not self.match('identifier'):
            self.set_error("Missing variable name", "identifier")
            return False
        return self.vardec_def()

    def dynasty(self):
        if self.match('dynasty'):
            return True
        elif self.data_type():
            return True
        else:
            self.set_error("Missing data type", "data_type")
            return False

    def vardec_def(self):
        if self.initialization():
            if not self.vardec_more():
                return False
            if not self.match("~"):
                return False
            self.store_completed_statement("VARIABLE_DECLARATION")
            return True
        elif self.match('['):
            if not (self.match('treasures_lit') or self.match('1')):
                self.set_error("Invalid array size", "treasures_lit or 1")
                return False
            if not self.match(']'):
                return False
            if not self.column():
                return False
            if not self.array_initialization():
                return False
            if not self.array_more():
                return False
            if not self.match('~'):
                return False
            self.store_completed_statement("ARRAY_DECLARATION")
            return True
        self.set_error("Invalid input", "valid vardec_def start")
        return False

    def initialization(self):
        if self.match('='):
            return self.val()
        return self.current_token() in ['~', ',']

    def vardec_more(self):
        if self.match(','):
            if not self.match('identifier') or not self.initialization():
                self.set_error("Missing variable name", "identifier")
                return False
            return self.vardec_more()
        return self.current_token() == '~'
    
    def column(self):
        token = self.current_token()
        if self.match('['):
            if not (self.match('treasures_lit') or self.match('1')):
                self.set_error("Expected treasures literal", "treasures_lit or 1")
                return False
            if not self.match(']'):
                return False
            return True
        elif token in ['=', ',', '~']:
            return True  
        else:
            self.set_error("Invalid input", self.current_token())
            return False 

    def array_initialization(self):
        token = self.current_token()
        if self.match('='):
            if not self.array_list():
                self.set_error("Invalid array list", "array_list")
                return False
            return True
        elif token in [',', '~']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def array_list(self):
        if not self.match('{'):
            return False
        if not self.array_content():
            return False
        if not self.match('}'):
            return False
        return True

    def array_content(self):
        if self.array_lit():
            if not self.lit_more():
                return False
            return True
        elif self.match('{'):
            if not self.array_row():
                return False
            if not self.match('}'):
                return False
            if not self.row_more():
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def array_row(self):
        if not self.array_lit():
            return False
        if not self.lit_more():
            return False
        return True

    def row_more(self):
        token = self.current_token()
        if self.match(','):
            if not self.match('{'):
                return False
            if not self.array_row():
                return False
            if not self.match('}'):
                return False
            if not self.row_more():
                return False
            return True
        elif token == '}':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def lit_more(self):
        token = self.current_token()
        if self.match(','):
            if not self.array_lit():
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.lit_more():
                return False
            return True
        elif token == '}':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def array_more(self):
        token = self.current_token()
        if self.match(','):
            if not self.match('identifier'):
                self.set_error("Missing variable name", "identifier")
                return False
            if not self.match('['):
                return False
            if not (self.match('treasures_lit') or self.match('1')):
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
        elif token == '~':
            return True  
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def array_lit(self):
        if self.match('scroll_lit'):
            return True
        elif self.match('rose_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.match('ocean_lit'):
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.match('identifier'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def assignment_exp(self):
        print("Entering assignment_exp")
        if not self.match('identifier'):
            self.set_error("Missing variable name", "identifier")
            return False
        print(f"Passed ID match: {repr(self.current_token())}")
        if not self.index():
            self.set_error("Invalid array index", self.current_token())
            return False
        if not self.assignment_operator():
            self.set_error("Invalid assignment operator", self.current_token())
            return False
        if not self.assignment_operand():
            self.set_error("Invalid assignment operand", self.current_token())
            return False
        self.store_completed_statement("ASSIGNMENT_EXP")
        return True

    def assignment_operator(self):
        token = self.current_token()
        print(f"Current token in assignment_operator: {token}")
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
            self.set_error("Invalid input", token)
            return False

    def assignment_operand(self):
        next_token = self.peek_next_token()
        token = self.current_token()
        if token == 'identifier':
            next_token = self.peek_next_token()
            print(f"Next token after identifier: {next_token}")
            if next_token == '(':
                start_pos = self.current_index
                if self.func_call():
                    print("Function call detected and parsed.")
                    next_token = self.current_token()
                    if next_token in ['+', '-', '*', '/', '*']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_token == '~':
                        return True
            elif next_token == '[':
                start_pos = self.current_index
                self.advance()
                if self.index():
                    print("Index detected and parsed.")
                    next_token = self.current_token()
                    if next_token in ['+', '-', '*', '/', '*']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_token == '~':
                        return True
            else:
                return self.match('identifier')
        elif token in ['treasures_lit', '1', '0']:
            if next_token in ['+', '-', '/', '*', '%']:
                if not self.arithmetic_exp():
                    return False
                return True
            else:
                return self.match(token)
        elif token == 'ocean_lit':
            if next_token in ['+', '-', '/', '*', '%']:
                if not self.arithmetic_exp():
                    return False
                return True
            else:
                return self.match('ocean_lit')
        elif self.match('('):
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
            self.set_error("Invalid input", self.current_token())
            return False

    def array_element(self):
        if not self.match('identifier'):
            self.set_error("Missing variable name", "identifier")
            return False
        if not self.index():
            self.set_error("Invalid array index", self.current_token())
            return False
        self.store_completed_statement("ARRAY_ELEMENT")
        return True

    def logical_exp(self):
        token = self.current_token()
        print(f"enter log_exp {token}")
        if self.logical_operand():
            print(f"passed log_operand {token}")
            if not self.logical_operator():
                self.set_error("Invalid logical operator", self.current_token())
                return False
            print(f"passed log_operator {token}")
            if not self.logical_operand():
                self.set_error("Invalid logical operand", self.current_token())
                return False
            print(f"passed log_operand {token}")
            if not self.more_log():
                return False
            self.store_completed_statement("LOGICAL_EXP")
            return True
        elif self.logical_operator1():
            if not self.logical_operand():
                self.set_error("Invalid logical operand", self.current_token())
                return False
            if not self.more_log():
                return False
            self.store_completed_statement("LOGICAL_EXP")
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def logical_operand(self):
        token = self.current_token()
        print(f"Checking logical operand: {token}")
        if token == 'identifier':
            next_token = self.peek_next_token()
            print(f"Next token after identifier: {next_token}")
            if next_token == '(':
                if self.func_call():
                    print("Function call detected and parsed.")
                    return True
            elif next_token == '[':
                self.advance()
                if self.index():
                    print("Array element detected and parsed.")
                    return True
            else:
                return self.match('identifier')
        elif self.match('treasures_mirror'):
            return True
        elif self.match('!'):
            if not self.logical_operand():
                return False
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.treasures_mirror():
            return True
        elif self.current_token() == '(':
            print("parenthesis detected")
            saved_position = self.current_index
            self.advance()
            if self.relational_operand():
                print("rel_operand detected")
                if (self.match('<') or self.match('>') or self.match('<=') or 
                    self.match('>=') or self.match('==') or self.match('!=')):
                    print("rel_operator detected")
                    if self.relational_operand() and self.relational_more() and self.match(')'):
                        print("close_paren detected")
                        return True
            self.current_index = saved_position
            self.advance()
            if self.logical_operand():
                print(f"passed logical operand: {self.current_token()}")
                if self.logical_operator():
                    print(f"passed logical operator: {self.current_token()}")
                    if self.logical_operand() and self.more_log() and self.match(')'):
                        print("close_paren detected")
                        return True
            self.current_index = saved_position
            self.advance()
            if self.logical_operator1():
                print("Logical NOT operator detected")
                if self.logical_operand() and self.more_log() and self.match(')'):
                    print("close_paren detected")
                    return True
            self.current_index = saved_position
            return False
        elif self.relational_exp():
            return True
        elif self.func_call():
            return True
        elif self.array_element():
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def logical_operator(self):
        if self.match('&&'):
            return True
        elif self.match('||'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def logical_operator1(self):
        if self.match('!'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def more_log(self):
        token = self.current_token()
        if self.logical_operator():
            print("Logical operator detected, continuing more_log_ext...")
            if not self.more_log_ext():
                return False
            return True
        elif token in [',', '~', ')']:
            print(f"End of logical expression detected: {token}")
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def more_log_ext(self):
        if self.logical_operand():
            if not self.more_log():
                return False
            return True
        elif self.logical_operator1():
            if not self.logical_operand():
                return False
            if not self.more_log():
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def func_call(self):
        if not self.match('identifier'):
            self.set_error("Missing variable name", "identifier")
            return False
        if not self.match('('):
            return False
        if not self.args():
            self.set_error("Invalid argument", self.current_token())
            return False
        if not self.match(')'):
            return False
        print("pass func_call")
        self.store_completed_statement("FUNC_CALL")
        return True
    
    def args(self):
        token = self.current_token()
        if self.args_val():
            if token == ')':
                return True
            if not self.args_more():
                return False
            return True
        elif token == ')':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def args_val(self):
        if self.match('identifier'):
            return True
        elif self.match('scroll_lit'):
            return True
        elif self.match('rose_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.match('ocean_lit'):
            return True
        elif self.match('mirror_lit'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def args_more(self):
        token = self.current_token()
        if token == ',':
            self.advance()
            if not self.args():
                return False
            return self.args_more()
        elif token in [')', '+', '-', '*', '/', '%', '~']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def treasures_mirror(self):
        if self.match('1'):
            return True
        elif self.match('0'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def arithmetic_exp(self):
        token = self.current_token()
        print(f"Enter Arith_exp {token}")
        if not self.arithmetic_operand():
            self.set_error("Invalid arithmetic operand", self.current_token())
            return False
        token = self.current_token()
        print(f"Enter Arith_operand success {token} ")
        if not self.arithmetic_operator():
            self.set_error("Invalid arithmetic operator", self.current_token())
            return False
        token = self.current_token()
        print(f"Enter Arith_operator success {token}")
        if not self.arithmetic_operand():
            self.set_error("Invalid arithmetic operand", self.current_token())
            return False
        token = self.current_token()
        print(f"Enter Arith_operand success {token}")
        if not self.more_arith():
            return False
        self.store_completed_statement("ARITHMETIC_EXP")
        return True
    
    def arithmetic_operand(self):
        token = self.current_token()
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':
                if not self.func_call():
                    return False
                return True
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
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.match('('):
            if not self.arithmetic_operand():
                self.set_error("Invalid arithmetic operand", self.current_token())
                return False
            if not (self.match('+') or self.match('-') or self.match('/') or self.match('*') or self.match('%')):
                self.set_error("Invalid arithmetic operator", self.current_token())
                print("Invalid operand")
                return False
            if not self.arithmetic_operand():
                self.set_error("Invalid arithmetic operand", self.current_token())
                return False
            if not self.more_arith():
                return False
            if not self.match(')'):
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
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
        elif self.match('&&'):
            return True
        elif self.match('||'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def more_arith(self):
        token = self.current_token()
        print(f"more_arith {token}")
        if self.arithmetic_operator():
            if not self.arithmetic_operand():
                self.set_error("Expected operand", self.current_token())
                return False
            print("more_arith_operand")
            return self.more_arith()
        elif token in [')', '~', ',', '<', '>', '<=', '>=', '==', '!=']:
            return True  
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def relational_exp(self):
       if not self.relational_operand():
            self.set_error("Invalid relational operand", self.current_token())
            return False
       if not self.relational_operator():
            self.set_error("Invalid relational operator", self.current_token())
            return False
       if not self.relational_operand():
            self.set_error("Invalid relational operand", self.current_token())
            return False
       if not self.relational_more():
            return False
       self.store_completed_statement("RELATIONAL_EXP")
       return True
    
    def relational_operand(self):
        token = self.current_token()
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':
                if not self.func_call(): 
                    return False
                return True  
            elif next_token == '[':
                self.advance()
                if not self.index():
                    return False
                return True
            else:
                return self.match(token)
        elif self.match('scroll_lit'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.match('ocean_lit'):
            return True
        elif self.match('('):
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
            self.set_error("Invalid input", self.current_token())
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
        elif self.match('&&'):
            return True
        elif self.match('||'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def relational_more(self):
        token = self.current_token()
        if self.relational_operator():
            if not self.relational_operand():
                self.set_error("Invalid relational operand", self.current_token())
                return False
            if not self.relational_more():
                return False
            return True
        elif token in [')', '', '', '~', '&&', '||']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def unary(self):
        token = self.current_token()
        print("Unary")
        if not self.match('identifier'):
            self.set_error("Missing variable name", "identifier")
            return False
        print(f"This is {token}")
        if not self.unary_operator():
            self.set_error("Invalid unary operator", self.current_token())
            return False
        self.store_completed_statement("UNARY_EXP")
        return True
    
    def unary_operator(self):
        if self.match('++'):
            return True
        elif self.match('--'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def concat(self):
        token = self.current_token()
        print(f"Enter concat Line {token}")
        if not self.string_operand():
            self.set_error("Invalid string operand", self.current_token())
            return False
        if not self.match('+'):
            return False
        if not self.string_operand():
            self.set_error("Invalid string operand", self.current_token())
            return False
        if not self.string_more():
            return False
        self.store_completed_statement("CONCATENATION")
        return True

    def string_operand(self):
        token = self.current_token()
        if token == 'identifier':
            next_token = self.peek_next_token()
            if next_token == '(':
                if not self.func_call():
                    return False
                return True
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
            self.set_error("Invalid input", self.current_token())
            return False

    def string_more(self):
        if self.match('+'):
            if not self.string_operand():
                self.set_error("Invalid string operand", self.current_token())
                return False
            return self.string_more()
        return True

    def user_defined_func(self):
        token = self.current_token()
        if self.match('spell'):
            if not self.return_type():
                return False
            if not self.match('identifier'):
                self.set_error("Missing function name", "identifier")
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
            if not self.user_defined_func():
                return False
            self.store_completed_statement("CONCATENATION")
            return True
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'single_comment', 'multi_comment', 'continue', '}', 'return', 'break', 'castle']:
            return True
        else: 
            self.set_error("Invalid input", self.current_token())
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
            self.set_error("Invalid return type", self.current_token())
            return False
        
    def param(self):
        token = self.current_token()
        print("enter param")
        if self.data_type():
            self.advance()
            if not self.match('identifier'):
                self.set_error("Missing variable name", "identifier")
                return False
            if not self.param_more():
                return False
            return True
        elif token == ')':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def param_more(self):
        token = self.current_token()
        if self.match(','):
            if not self.data_type():
                self.set_error("Missing data type", "data_type")
                return False
            self.advance()
            if not self.match('identifier'):
                self.set_error("Missing variable name", "identifier")
                return False
            if not self.param_more():
                return False
            return True
        elif token == ')':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def body(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        if token in ['return', '}', 'break', 'continue']:
            return True
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
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    print("passed")
                    next_token = self.current_token()
                    if next_token in ['+=', '-=', '*=', '/=', '%=']:
                        self.current_index = start_pos
                        if not self.assignment_exp():
                            return False
                        if not self.match('~'):
                            return False
                        return self.body()
                    elif next_token == '=':
                        self.current_index = start_pos
                        if not self.var_reassign():
                            return False
                        return self.body()
                    return False
                return False
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'rose', 'ocean']:
            if not self.var_dec():
                return False
            return self.body()
        elif token in ['believe', 'forever', 'cast']:
            if not self.condi_statement():
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
        elif token == 'tale':
            if not self.for_loop():
                return False
            return self.body()
        elif token in ["single_comment", "multi_comment"]:
            self.advance()
            return self.body()
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def ret_statement(self):
        token = self.current_token()
        print(f"This is {token}")
        if self.match('return'):
            print('passed return')
            if not self.val1():
                return False
            print('val1')
            if not self.match('~'):
                return False
            return True
        elif token == '}':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def var_reassign(self):
        if not self.match('identifier'):
            self.set_error("Invalid variable name", "identifier")
            return False
        if not self.match('='):
            return False
        if not self.val():
            return False
        if not self.match('~'):
            return False
        self.store_completed_statement("VAR_REASSIGN")
        return True
    
    def condi_statement(self):
        token = self.current_token()
        if token == 'cast':
            return self.if_statement()
        elif token == 'forever':
            return self.while_statement()
        elif token == 'believe':
            return self.do_while_statement()
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def for_loop(self):
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
        self.store_completed_statement("FOR_LOOP")
        return True

    def loop_var(self):
        if self.match('treasures'):
            if not self.match('identifier'):
                self.set_error("Missing variable name", "identifier")
                return False
            if not self.match('='):
                return False
            if not self.loop_val():
                return False
            return True
        elif self.match('identifier'):
            if not self.loop_init():
                return False
            return True
    
    def loop_init(self):
        token = self.current_token()
        if self.match('='):
            if not self.loop_val():
                return False
            return True
        elif token == '~':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def loop_val(self):
        if self.match('identifier'):
            return True
        elif self.match('treasures_lit'):
            return True
        elif self.match('0'):
            return True
        elif self.match('1'):
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def loop_body(self):
        token = self.current_token()
        next_token = self.peek_next_token()     
        if token is None:
            return True
        if token in ['return', '}', 'break', 'continue']:
            return True
        elif token == 'identifier':
            if next_token is None:
                return False
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
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    print("passed")
                    next_token = self.current_token()
                    if next_token in ['+=', '-=', '*=', '/=', '%=']:
                        self.current_index = start_pos
                        if not self.assignment_exp():
                            return False
                        if not self.match('~'):
                            return False
                        return self.loop_body()
                    elif next_token == '=':
                        self.current_index = start_pos
                        if not self.var_reassign():
                            return False
                        return self.loop_body()
                    self.set_error("Invalid input", self.current_token()) 
                    return False
                self.set_error("Invalid input", self.current_token())
                return False
        elif token in ['dynasty', 'scroll', 'treasures', 'mirror', 'rose', 'ocean']:
            if not self.var_dec():
                return False
            return self.loop_body()
        elif token in ['believe', 'forever']:
            if not self.condi_statement():
                return False
            return self.loop_body()
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
            self.advance()
            return self.loop_body()
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def if_break(self):
        if not self.match('cast'):
            self.set_error("Invalid input", self.current_token())
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
        self.store_completed_statement("IF_BREAK")
        return True
    
    def elif_break(self):
        token = self.current_token()
        if self.match('twist'):
            if not self.match('('):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.condition():
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.match(')'):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.match('{'):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.body():
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.flow_control():
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.match('}'):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.elif_break():
                self.set_error("Invalid input", self.current_token())
                return False
            self.store_completed_statement("ELIF_BREAK")
            return True
        elif token in ['curse', '}']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def else_break(self):
        token = self.current_token()
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.flow_control():
                return False
            if not self.match('}'):
                return False
            self.store_completed_statement("ELSE_BREAK")
            return True
        elif token == '}':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def flow_control(self):
        token = self.current_token()
        if self.match('break'):
            if not self.match('~'):
                return False
            return True
        elif self.match('continue'):
            if not self.match('~'):
                return False
            return True
        elif token == '}':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def do_while_statement(self):
        if not self.match('believe'):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match('{'):
            return False
        if not self.loop_body():
            return False
        if not self.match('}'):
            return False
        if not self.match('forever'):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match('('):
            return False
        if not self.condition():
            return False
        if not self.match(')'):
            return False
        if not self.match('~'):
            return False
        self.store_completed_statement("DO_WHILE")
        return True
    
    def condition(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        if token == 'identifier':
            if next_token == '(':
                start_pos = self.current_index
                if self.func_call():
                    next_after_func = self.current_token()
                    if next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    elif next_token in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    elif next_token in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    return True
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            else:
                return self.match(token)
        elif self.match('!'):
            print(f"Current Token: {self.current_token()}, Next Token: {self.peek_next_token()}")
            if not self.match('('):
                return False
            if not self.condition():
                return False
            if not self.match(')'):
                return False
            return True
        elif self.func_call():
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.relational_exp():
            return True
        elif self.logical_exp():
            return True
        elif self.treasures_mirror():
            return True
        else:
            self.set_error("Invalid condition", self.current_token())
            return False
    
    def mirror_init(self):
        token = self.current_token()
        if self.match('=='):
            if not (self.match('mirror_lit') or self.match('0') or self.match('1')):
                self.set_error("Invalid input", self.current_token())
                return False
            return True
        elif self.match('!='):
            if not (self.match('mirror_lit') or self.match('0') or self.match('1')):
                self.set_error("Invalid input", self.current_token())
                return False
            return True
        elif token == ')':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def while_statement(self):
        token = self.current_token()
        if not self.match('forever'):
            return False
        print(f"passed forever {token}")
        if not self.match('('):
            return False
        print(f"passed ( {token}")
        if not self.condition():
            return False
        print(f"passed condition {token}")
        if not self.match(')'):
            return False
        print(f"passed ) {token}")
        if not self.match('{'):
            return False
        print(f"passed open curly {token}")
        if not self.loop_body():
            return False
        print(f"passed loop body {token}")
        if not self.match('}'):
            return False
        print(f"passed close curly {token}")
        self.store_completed_statement("WHILE_STATEMENT")
        return True
        
    def if_statement(self):
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
        self.store_completed_statement("IF_STATEMENT")
        return True
    
    def elif_statement(self):
        token = self.current_token()
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
            self.store_completed_statement("ELIF_STATEMENT")
            return True
        elif token in ['curse', 'scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', '?', 'return']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def else_statement(self):
        token = self.current_token()
        if self.match('curse'):
            if not self.match('{'):
                return False
            if not self.body():
                return False
            if not self.match('}'):
                return False
            self.store_completed_statement("ELSE_STATEMENT")
            return True
        elif token in ['scroll', 'treasures', 'mirror', 'ocean', 'rose', 'dynasty', 'granted', 'identifier', 'spell', 'cast', 'forever', 'believe', 'tale', 'single_comment', 'multi_comment', 'return', 'break', 'continue']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def output(self):
        if not self.match('granted'):
            return False
        if not self.match('('):
            return False
        if not self.granted_content():
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.more_granted():
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match(')'):
            return False
        if not self.match('~'):
            return False
        self.store_completed_statement("ELSE_STATEMENT")
        return True
    
    def granted_content(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        if token == 'identifier':
            if next_token == '(':
                start_pos = self.current_index
                if self.func_call():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
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
        elif token in ['treasures_lit', '1', '0']:
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
            paren_count = 1
            content = []
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:
                    self.set_error("Missing closing parenthesis")
                    return False
                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)
            if next_after_paren == '~':
                self.advance()
                self.advance()
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    self.set_error("Invalid input", self.current_token())
                    return False
            else:
                self.current_index = start_pos
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren in ['relational', 'logical']:
                        return self.logical_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                else:
                    self.set_error("Invalid input", self.current_token())
                    return False
        elif self.match('setprecission'):
            return True
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose', 'tomirror']:
            start_pos = self.current_index
            self.advance()
            paren_count = 1
            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()
                cur_token = self.current_token()
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                self.set_error("Invalid input", self.current_token())
                return False
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos
            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == ')' :
                return self.type_conversion()
            else:
                print("Invalid string operations")
                self.set_error("Invalid input", self.current_token())
                return False
        elif self.match('lengthof'):
            if not self.match('('):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.match('identifier'):
                self.set_error("Invalid input", self.current_token())
                return False
            if not self.match(')'):
                self.set_error("Invalid input", self.current_token())
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def set_precision(self):
        if not self.match('%'):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match('.'):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match('['):
            self.set_error("Invalid input", self.current_token())
            return False
        if not (self.match('treasures_lit') or self.match('1') or self.match('0')):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match(']'):
            self.set_error("Invalid input", self.current_token())
            return False
        if not self.match('f'):
            self.set_error("Invalid input", self.current_token())
            return False
        return True

    def more_granted(self):
        token = self.current_token()
        if self.match(','):
            if not self.granted_content():
                return False
            if not self.more_granted():
                return False
            return True
        elif token == ')':
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False

    def data_type(self):
        token = self.current_token()
        if token in {'scroll', 'treasures', 'mirror', 'ocean', 'rose'}:
            return True
        self.set_error("Invalid input", self.current_token())
        return False

    def val(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        if token == 'identifier':
            if next_token == '(':
                start_pos = self.current_index
                if self.func_call():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True 
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['&&', '||']:
                        self.current_index = start_pos
                        return self.logical_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
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
        elif token in ['treasures_lit', '1', '0']:
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
            paren_count = 1
            content = []
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:
                    self.set_error("Missing closing parenthesis", f"Line {self.current_line}, Index {self.current_index}")
                    return False
                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)
            if next_after_paren == '~':
                self.advance()
                self.advance()
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    self.set_error("Invalid input", self.current_token())
                    return False
            else:
                self.current_index = start_pos
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren == 'relational':
                        return self.logical_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                else:
                    self.set_error("Invalid input", self.current_token())
                    return False
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose', 'tomirror']:
            start_pos = self.current_index
            self.advance()
            paren_count = 1
            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()
                cur_token = self.current_token()
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                self.set_error("Invalid input", self.current_token())
                return False
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos
            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == '~':
                return self.type_conversion()
            else:
                print("Invalid string operations")
                self.set_error("Invalid input", self.current_token())
                return False
        elif token == 'wish': 
            return self.input() 
        elif self.match('lengthof'):
            if not self.match('('):
                return False
            if not self.match('identifier'):
                return False
            if not self.match(')'):
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def val1(self):
        token = self.current_token()
        next_token = self.peek_next_token()
        print("Entered Val1")
        if token == 'identifier':
            if next_token == '(':
                start_pos = self.current_index
                if self.func_call():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['+=', '-=', '/=', '*=', '%=']:
                        self.current_index = start_pos
                        return self.assignment_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token == '[':
                start_pos = self.current_index 
                self.advance()
                if self.index():
                    next_after_func = self.current_token()
                    if next_after_func in ['+', '-', '*', '/', '%']:
                        self.current_index = start_pos
                        return self.arithmetic_exp()
                    elif next_after_func in ['>', '<', '>=', '<=', '==', '!=']:
                        self.current_index = start_pos
                        return self.relational_exp()
                    elif next_after_func in ['+=', '-=', '/=', '%=', '*=']:
                        self.current_index = start_pos
                        return self.assignment_exp()
                    return True  
                self.set_error("Invalid input", self.current_token())
                return False
            elif next_token in ['+', '-', '*', '/', '%']:
                return self.arithmetic_exp()
            elif next_token in ['>', '<', '>=', '<=', '==', '!=']:
                return self.relational_exp()
            elif next_token in ['&&', '||']:
                return self.logical_exp()
            elif next_token in ['+=', '-=', '/=', '*=', '%=']:
                return self.assignment_exp()
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
        elif token in ['treasures_lit', '1', '0']:
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
            paren_count = 1
            content = []
            while paren_count > 0:
                self.advance()
                cur_token = self.current_token()
                if cur_token is None:
                    self.set_error("Missing closing parenthesis", f"Line {self.current_line}, Index {self.current_index}")
                    return False
                content.append(cur_token)
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            next_after_paren = self.peek_next_token()
            operator_in_paren = self.determine_operation_type(content)
            if next_after_paren == '~':
                self.advance()
                self.advance()
                if operator_in_paren == 'arithmetic':
                    return self.arithmetic_exp()
                elif operator_in_paren == 'relational':
                    return self.relational_exp()
                elif operator_in_paren == 'logical':
                    return self.logical_exp()
                elif operator_in_paren == 'Not Valid':
                    self.set_error("Invalid input", self.current_token())
                    return False
            else:
                self.current_index = start_pos
                if next_after_paren in ['+', '-', '*', '/', '%']:
                    if operator_in_paren == 'arithmetic':
                        return self.arithmetic_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['>', '<', '>=', '<=', '==', '!=']:
                    if operator_in_paren == 'arithmetic':
                        return self.relational_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                elif next_after_paren in ['&&', '||']:
                    if operator_in_paren == 'relational':
                        return self.logical_exp()
                    self.set_error("Invalid input", self.current_token())
                    return False
                else:
                    self.set_error("Invalid input", self.current_token())
                    return False
        elif token in ['toscroll', 'toocean', 'totreasures', 'torose', 'tomirror']:
            start_pos = self.current_index
            self.advance()
            paren_count = 1
            while paren_count > 0 and self.current_index < len(self.tokens):
                self.advance()
                cur_token = self.current_token()
                if cur_token == '(':
                    paren_count += 1
                elif cur_token == ')':
                    paren_count -= 1
            if paren_count > 0:
                print("Syntax Error: Unmatched parenthesis")
                self.set_error("Invalid input", self.current_token())
                return False
            next_after_paren = self.peek_next_token()
            self.current_index = start_pos
            if next_after_paren == '+':
                return self.concat()
            elif next_after_paren == '~':
                return self.type_conversion()
            else:
                print("Invalid string operations")
                self.set_error("Invalid input", self.current_token())
                return False
        elif token == 'wish': 
            return self.input() 
        elif self.match('lengthof'):
            if not self.match('('):
                return False
            if not self.match('identifier'):
                return False
            if not self.match(')'):
                return False
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
    
    def type_conversion(self):
        if not self.conversion_func():
            return False
        if not self.match('('):
            return False
        if not self.conversion_value():
            return False
        if not self.match(')'):
            return False
        return True
    
    def conversion_func(self):
        if self.match('toscroll'):
            return True
        elif self.match('totreasures'):
            return True
        elif self.match('tomirror'):
            return True
        elif self.match('toocean'):
            return True
        elif self.match('torose'):
            return True
        else:
            self.set_error("Invalid conversion function", self.current_token())
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
        elif self.match('1'):
            return True
        elif self.match('0'):
            return True
        elif self.match('mirror_lit'):
            return True
        elif self.match('identifier'):
            if not self.index():
                return False
            return True
        elif self.func_call():
            return True
        else:
            self.set_error("Invalid conversion value", self.current_token())
            return False

    def index(self):
        token = self.current_token()
        if self.match('['):
            if not (self.match('treasures_lit') or self.match('1') or self.match('0')):
                self.set_error("Invalid array index", self.current_token())
                return False
            if not self.match(']'):
               return False
            print("index-done")
            if not self.column1():
                return False
            print("column1")
            return True
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{', '+=', '-=', '*=', '/=', '%=']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
            
    def column1(self): 
        token = self.current_token()
        if self.match('['):
            if not (self.match('treasures_lit') or self.match('1') or self.match('0')):
                self.set_error("Invalid array index", self.current_token())
                return False
            if not self.match(']'):
                return False
            return True
        elif token in ['&&', '||' , ',' , '~', ')', '+', '-', '/', '*', '%', ')', '<', '>', '<=', '>=', '==', '!=', '{', '+=', '-=', '*=', '/=', '%=']:
            return True
        else:
            self.set_error("Invalid input", self.current_token())
            return False
        
    def input(self):
        if not self.match('wish'):
            return False
        if not self.match('('):
            return False
        if not self.match('scroll_lit'):
            return False
        if not self.match(')'):
            return False
        return True
    
    def determine_operation_type(self, content):
        if content and content[-1] == ')':
            content.pop()
        content_str = ' '.join(str(token) for token in content).lower()
        if any(op in content_str for op in ['+', '-', '*', '/', '%']):
            return 'arithmetic'
        elif any(op in content_str for op in ['>', '<', '>=', '<=', '==', '!=']):
            return 'relational'
        elif any(op in content_str for op in ['and', 'or', '&&', '||']):
            return 'logical'
        return 'Not Valid'

    def parse(self):
        if self.program():
            self.parsing_result = "Parsing successful."
            return True
        else:
            raise SyntaxError(self.error_message)

    def get_parsing_result(self):
        return self.parsing_result
