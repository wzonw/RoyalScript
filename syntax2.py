from lexer import RoyalScriptLexer, Token
from RS_RegDef import Delims, RegDef

class RoyalScriptParser:
    def __init__(self, tokens):
        """Initialize with tokens and syntax rules."""
        self.tokens = tokens  # List of token types for each line
        self.current_line = 0  # Current line index
        self.current_index = 0  # Current token index
        self.errors = []  # Store syntax errors
        self.parsing_result = ""  # Parsing output
    
    def current_token(self):
        """Return the current token type in the current line, skipping empty tokens."""
        while self.current_line < len(self.tokens):
            if self.current_index < len(self.tokens[self.current_line]):
                token = self.tokens[self.current_line][self.current_index]
                if token is not None:  # Ensure token is valid
                    return token
                self.current_index += 1  # Move to next token in the same line
            else:
                self.current_line += 1  # Move to next line
                self.current_index = 0  # Reset index for new line
        return None  # No more tokens
    
    def advance(self):
        """Move to the next token."""
        if self.current_index + 1 < len(self.tokens[self.current_line]):
            self.current_index += 1
        elif self.current_line + 1 < len(self.tokens):
            self.current_line += 1
            self.current_index = 0
        else:
            return None  # End of tokens

    def match(self, expected):
        """Match the current token against the expected value."""
        if self.current_token() == expected:
            self.advance()
            return True
        self.errors.append(f"Syntax Error: Expected {expected} but got {self.current_token()} at line {self.current_line}")
        return False
    #            ______                                                                            _______
    # <program>: crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~
    def program(self):
        """Parse the entire program according to the CFG rules."""
        
        if not self.match("crown"):  # Check for 'crown'
            self.error("Expected 'crown' at the beginning of the program.")
            return False
        
        if not self.match("~"):  # Ensure '~' follows 'crown'
            self.error("Expected '~' after 'crown'.")
            return False
        
        if not self.statements():  
            return False  
        
        if not self.match("reign"):  # Check for 'reign' before EOF
            self.error("Expected 'reign' before the end of the program.")
            return False
        
        if not self.match("~"):  # Ensure '~' follows 'reign'
            self.error("Expected '~' after 'reign'.")
            return False

        return True  # Parsing successful if all rules followed


    #                                                                                               ______
    # <program>: crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~
    def statements(self):
        """Parses multiple statements between 'crown ~' and 'reign ~'."""
        while not self.peek("reign"):  # Stop parsing when 'reign' is next
            if not self.statement():  # Call to handle each statement
                return False  # If a statement fails, return an error
        return True  # Successfully parsed all statements

    #                   _______________________________________
    # <program>: crown~ <global_dec> <user-defined_func> castle treasures id_lit {<body> return 0~} reign~
    def statement(self):
        """Parse a single statement."""
        token = self.current_token()
        if token in ["treasures", "ocean", "scroll", "rose", "mirror", "dynasty"]:
            return self.var_dec()
        # <user-defined-func>: spell <return_type> id_lit(<param>) {<body><ret_statement>} <user-defined_func> => spell
        elif token == "spell":
            return self.parse_function_declaration()
        # <program>: castle
        elif token == "castle":
            return self.parse_main_function_declaration()
        # elif token == "EOF":
        #     return True  # End of program
        else:
            self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
            return False

    # <vardec>: <const> <datatype> id_lit <vardec_more>
    def var_dec(self):
        """Parse variable declaration based on CFG."""
        token = self.current_token()
        #constant declaration
        if token == "dynasty":
            self.advance()
            token = self.current_token()
            if token in (["treasures", "ocean", "scroll", "rose", "mirror"]):
                self.advance()
                token = self.current_token()
                if token == "identifier":
                    return self.vardec_def()
                else:
                    return False
            else:
                return False
        else:
            self.advance()
            token = self.current_token()
            if token == "identifier":
                return self.vardec_def()
            else:
                return False
            

    def vardec_def(self):
        token = self.current_token()
        self.advance()
        if token == "~":
            self.advance()
            return self.statements()
        elif token == "=":
            return self.initialization()
        elif token == ",":
            return self.vardec_more()
        elif token == "[":
            self.advance()
            token = self.current_token()
            if token == "treasures_lit": #palitan ng pos-treasures-lit
                if int(token) >= 1:
                    self.advance()
                    token = self.current_token()
                    if token == "]":
                        return self.column()
                    else:
                        self.errors.append(f"Missing ] to close the array size at line {self.current_line}")
                        return False
                else:
                    self.errors.append(f"Invalid array size must be at least 1 at line {self.current_line}")
                    return False
            else:
                self.errors.append(f"Invalid array size value must be of tresures data type at line {self.current_line}")
                return False
        elif token is None:
            self.errors.append(f"Missing terminator ~ at line {self.current_line}")
            return False
        else:
            self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
            return False

    def initialization(self):
        self.advance()
        token = self.current_token()
        if token in ["scroll_lit", "treasures_lit", "mirror_lit", "ocean_lit", "rose_lit", "id_lit", "phantom"]: # wala pa mga operations etc.
            self.advance()
            token = self.current_token()
            if token == ",":
                return self.vardec_more()
            elif token == "~":
                self.advance()
                return self.statements()
            elif token is None:
                self.errors.append(f"Missing terminator ~ at line {self.current_line}")
                return False
            else:
                self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
                return False
        else:
            self.errors.append(f"Invalid initialization value '{token}' at line {self.current_line}")
            return False
        
    
    def vardec_more(self):
        self.advance()
        token = self.current_token()
        if token == "identifier":
            return self.vardec_def()
        else:
            self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
            return False
            

    def column(self):
        self.advance
        token = self.current_token()
        if token == "[":
            self.advance()
            token = self.current_token()
            if token == "treasures_lit": #palitan ng pos-treasures-lit
                if int(token) >= 1:
                    self.advance()
                    token = self.current_token()
                    if token == "]":
                        return self.array_initialization()
                    else:
                        self.errors.append(f"Missing ] to close the array size at line {self.current_line}")
                        return False
                else:
                    self.errors.append(f"Invalid array size must be at least 1 at line {self.current_line}")
                    return False
            else:
                self.errors.append(f"Invalid array size value must be of tresures data type at line {self.current_line}")
                return False
            
        elif token == "=":
            return self.array_initialization()
        
        elif token == ",":
            return self.array_more()
        
        elif token == "~":
            self.advance()
            return self.statements()

        elif token is None:
            self.errors.append(f"Missing terminator ~ at line {self.current_line}")
            return False
        
        else:
            self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
            return False
        
    
    def array_initialization(self):
        self.advance()
        token = self.current_token()
        if token == "{":
            self.advance()
            token = self.current_token()
            if token == "{":
                self.advance()
                token = self.current_token()
                if token in ["scroll_lit", "treasures_lit", "mirror_lit", "ocean_lit", "rose_lit"]:
                    self.advance()
                    token = self.current_token()
                    if token == ",":
                        return self.list_more()
                    elif token == "}":
                        self.advance()
                        token = self.current_token()
                        if token == "}":
                            self.advance()
                            token = self.current_token()
                            if token == "~":
                                self.advance()
                                return self.statements()
                            elif token is None:
                                self.errors.append(f"Missing terminator ~ at line {self.current_line}")
                                return False
                            else:
                                self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
                                return False
                        # elif token == ",":
                            
                        else:
                            self.errors.append(f"Invalid token {token} at line {self.current_line}")
                            return False
                    else:
                        self.errors.append(f"Invalid token {token} at line {self.current_line}")
                        return False
                else:
                    self.errors.append(f"Invalid value for an array element at line {self.current_line}")
                    return False
            elif token in ["scroll_lit", "treasures_lit", "mirror_lit", "ocean_lit", "rose_lit"]:
                self.advance()
                token = self.current_token()
                if token == ",":
                    return self.list_more()
                elif token == "}":
                    self.advance()
                    token = self.current_token()
                    if token == "~":
                        self.advance()
                        return self.statements()
                    elif token is None:
                                self.errors.append(f"Missing terminator ~ at line {self.current_line}")
                                return False
                    else:
                        self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
                        return False
                else:
                    self.errors.append(f"Invalid token {token} at line {self.current_line}")
                    return False
            else:
                self.errors.append(f"Invalid value for an array element at line {self.current_line}")
                return False
        else:
            self.errors.append(f"Missing '{{' for array initialization at line {self.current_line}")
            return False
            
        
    def list_more(self):
        self.advance()
        token = self.current_token()
        if token in ["scroll_lit", "treasures_lit", "mirror_lit", "ocean_lit", "rose_lit"]:
            self.advance()
            token = self.current_token()
            if token == ",":
                return self.list_more()
            elif token == "}":
                self.advance()
                token = self.current_token()
                if token == "}":
                    self.advance()
                    token = self.current_token()
                    if token == "~":
                        self.advance()
                        return self.statements()
                    elif token is None:
                        self.errors.append(f"Missing terminator ~ at line {self.current_line}")
                        return False
                    else:
                        self.errors.append(f"Unexpected token '{token}' at line {self.current_line}")
                        return False
                else:
                    self.errors.append(f"Invalid token {token} at line {self.current_line}")
                    return False
            else:
                self.errors.append(f"Invalid token {token} at line {self.current_line}")
                return False 
        else:
            self.errors.append(f"Invalid value for an array element at line {self.current_line}")
            return False
        
            



    

    


  


























    # def parse_variable_optional(self):
    #     """Handle optional initialization or array declaration."""
    #     token = self.current_token()
    #     if token == "=":
    #         self.advance()
    #         return self.parse_expression()
    #     elif token == "[":
    #         return self.parse_array_declaration()
    #     return True  # If neither, assume valid declaration

    # def parse_array_declaration(self):
    #     """Parse array declaration."""
    #     if not self.match("["):
    #         return False
    #     if not self.match(RegDef["num"]):
    #         return False
    #     if not self.match("]"):
    #         return False
    #     return self.parse_variable_optional()

    # def parse_expression(self):
    #     """Parse an expression (values, identifiers, or operations)."""
    #     token = self.current_token()
    #     if token in ["scroll-lit", "rose-lit", "neg-treasures-lit", "pos-treasures-lit", 
    #                  "neg-ocean-lit", "pos-ocean-lit", "mirror-lit", "identifier", "phantom"]:
    #         self.advance()
    #         return True
    #     self.errors.append(f"Invalid expression at line {self.current_line}")
    #     return False

    # def parse_function_declaration(self):
    #     """Parse a function declaration."""
    #     if not self.match("spell"):
    #         return False
    #     if not self.match(["chamber", "treasures", "ocean", "scroll", "rose", "mirror"]):
    #         return False
    #     if not self.match("identifier"):
    #         return False
    #     if not self.match("("):
    #         return False
    #     self.parse_parameters()
    #     if not self.match(")"):
    #         return False
    #     return self.parse_function_body()

    # def parse_parameters(self):
    #     """Parse function parameters."""
    #     token = self.current_token()
    #     if token in ["treasures", "ocean", "scroll", "rose", "mirror"]:
    #         self.advance()
    #         self.match("identifier")
    #         while self.current_token() == ",":
    #             self.advance()
    #             self.match(["treasures", "ocean", "scroll", "rose", "mirror"])
    #             self.match("identifier")

    # def parse_function_body(self):
    #     """Parse function body inside curly braces."""
    #     if not self.match("{"):
    #         return False
    #     while self.current_token() and self.current_token() != "}":
    #         if not self.parse_statement():
    #             return False
    #     return self.match("}")

    def parse(self):
        """Parse the program starting from the 'crown' keyword."""
        if self.parse_program():
            self.parsing_result = "Parsing successful."
        else:
            self.parsing_result = "Parsing failed."
            for error in self.errors:
                print(error)
    
    def get_parsing_result(self):
        """Return parsing result."""
        return self.parsing_result
