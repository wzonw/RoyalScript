import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk 
import re
from RS_RegDef  import Delims
from RS_RegDef  import RegDef


# Token class to represent individual tokens
class Token:
    def __init__(self, value, token_type, position):
        self.value = value
        self.token_type = token_type
        self.position = position

    def __repr__(self):
        return f"{self.token_type}({self.value}) "



# Define token types for RoyalScript
class TokenType:
    # Reserved words for RoyalScript
    CROWN = "RESERVE WORDS"
    REIGN = "RESERVE WORDS"
    SPELL = "RESERVE WORDS"  # For function declarations
    CASTLE = "RESERVE WORDS"  # Main function
    WISH = "INPUT"  # Input
    GRANTED = "OUTPUT"  # Output
    CAST = "IF"  # If statement
    TWIST = "ELSEIF"  # Else if statement
    CURSE = "ELSE"  # Else statement
    TOROSE = "CONVERSION FUNC"
    TOSCROLL = "CONVERSION FUNC"
    TOOCEAN = "CONVERSION FUNC"
    TOTREASURES = "CONVERSION FUNC"  
    ESCAPE = "ESCAPE"
    TALE = "FOR LOOP"

    # Flow control
    BELIEVE = "CONDITIONAL"
    FOREVER = "CONDITIONAL"
    BREAK = "FLOW CONTROL"
    CONTINUE = "FLOW CONTROL"
    RETURN = "RETURN"

    # Data types
    TREASURES = "DATA TYPE"  # int
    OCEAN = "DATA TYPE"  # float
    SCROLL = "DATA TYPE"  # string
    ROSE = "DATA TYPE"  # char
    MIRROR = "DATA TYPE"  # boolean
    CHAMBER = "DATA TYPE"  # void
    DYNASTY = "DATA TYPE"  # constant
    PHANTOM = "NULL"

    # Literals
    INT_LITERAL = "INT_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"
    NULL_LITERAL = "NULL_LITERAL"

    # Operatorsi 
    ASSIGNMENT_OPERATOR = "ASSIGNMENT_OPERATOR"
    ARITHMETIC_OPERATOR = "ARITHMETIC OPERATOR"
    RELATIONAL_OPERATOR = "RELATIONAL OPERATOR"
    LOGICAL_OPERATOR = "LOGICAL OPERATOR"
    UNARY_OPERATOR = "UNARY OPERATOR"

    # Symbols
    COMMA = "COMMA"
    DOT = "DOT"
    OPEN_PAREN = "OPEN PARENTHESIS"
    CLOSE_PAREN = "CLOSE PARENTHESIS"
    OPEN_SQUARE = "OPEN SQUARE BRACKET"
    CLOSE_SQUARE = "CLOSE SQUARE BRACKET"
    TERMINATOR = "TERMINATOR"
    OPEN_CURLY = "OPEN CURLY BRACKET"
    CLOSE_CURLY = "CLOSE CURLY BRACKET"

    # Other token types
    IDENTIFIER = "IDENTIFIER"
    WHITESPACE = "WHITESPACE"
    SINGLE_COMMENT = "SINGLE-LINE COMMENT"
    MULTI_COMMENT = "MULTI-LINE COMMENT"
    DOT = "DOT"

    ESCAPE_NEWLINE = "ESCAPE_NEWLINE"
    ESCAPE_TAB = "ESCAPE_TAB"
    ESCAPE_BACKSLASH = "ESCAPE_BACKSLASH"
    ESCAPE_QUOTE = "ESCAPE_QUOTE"

    EQUAL = 'EQUAL SIGN'
    NOT = 'NOT LOGIC'
    ALPHANUM = 'ALPHANUM'


class RoyalScriptLexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def advance(self):
        """Advance to the next character in the input"""
        self.position += 1

    def current_char(self):
        """Return the current character at the position"""
        if self.position < len(self.code):
            return self.code[self.position]
        return None

    def match(self, regex):
        """Try to match a regex pattern at the current position"""
        match = re.match(regex, self.code[self.position:])
        if match:
            return match.group(0)
        return None

    #def match(self, symbol):
       # """Match the input code against the provided symbol using string comparison."""
        # Check if the current position can match the symbol
        #if self.input_code[self.position:self.position + len(symbol)] == symbol:
         #   return True
      #  return False

    def get_tokens(self):
        """Tokenize the entire input code"""
        cursor_advanced = False
        while self.position < len(self.code):
            char = self.current_char()

            # # Handle terminator (~)
            # if char == '~':
            #     if char in TokenType.DELIMS:  # Check if it's a delimiter
            #         token = Token(char, TokenType.DELIMS, self.position)
            #         self.tokens.append(token)
            #     else:
            #         token = Token(char, TokenType.TERMINATOR, self.position)
            #         self.tokens.append(token)
            #     self.advance()
            #     continue

            if char in ['\n', ' ', '\t']:
                match = self.match(r'\s+')
                if match and self.position < len(self.code) - 1:  # Avoid trailing whitespace
                    token = Token(match, TokenType.WHITESPACE, self.position)
                    self.tokens.append(token)
                self.advance()  # Move to the next character
                continue

            if char == 'b':
                pos_start = self.position
                valid, input_str, tokenType= self.state1()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in Delims['conditional'] and self.current_char() not in ['~', ' ']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    # Inside get_tokens method
                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )

                
            if char == 'c':
                pos_start = self.position
                valid, input_str, tokenType= self.state14()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()
                    
                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )

            if char == 'd':
                pos_start = self.position
                valid, input_str, tokenType= self.state47()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == 'f':
                pos_start = self.position
                valid, input_str, tokenType= self.state55()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == 'g':
                pos_start = self.position
                valid, input_str, tokenType= self.state63()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == 'm':
                pos_start = self.position
                valid, input_str, tokenType= self.state71()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )

            if char == 'o':
                pos_start = self.position
                valid, input_str, tokenType= self.state78()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == 'p':
                pos_start = self.position
                valid, input_str, tokenType= self.state84()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '~']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )  

            if char == 'r':
                pos_start = self.position
                valid, input_str, tokenType= self.state92()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '~']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )

            if char == 's':
                pos_start = self.position
                valid, input_str, tokenType= self.state108()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )     

            if char == 't':
                pos_start = self.position
                valid, input_str, tokenType= self.state120()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(', '~']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 


            if char == 'w':
                pos_start = self.position
                valid, input_str, tokenType= self.state168()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )

            if char == '=':
                pos_start = self.position
                valid, input_str, tokenType= self.state173()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )    
            
            if char == '+':
                pos_start = self.position
                valid, input_str, tokenType= self.state177()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 

            if char == '-':
                pos_start = self.position
                valid, input_str, tokenType= self.state183()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 
                
            if char == '*':
                pos_start = self.position
                valid, input_str, tokenType= self.state189()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )  
                
            if char == '/':
                pos_start = self.position
                valid, input_str, tokenType= self.state193()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )  
                
            if char == '%':
                pos_start = self.position
                valid, input_str, tokenType= self.state197()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 

            if char == '!':
                pos_start = self.position
                valid, input_str, tokenType= self.state201()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 
                
            if char == '&':
                pos_start = self.position
                valid, input_str, tokenType= self.state205()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == '|':
                pos_start = self.position
                valid, input_str, tokenType= self.state208()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    ) 

            if char == '>':
                pos_start = self.position
                valid, input_str, tokenType= self.state211()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
            
            if char == '<':
                pos_start = self.position
                valid, input_str, tokenType= self.state215()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )


            if char == '(':
                pos_start = self.position
                valid, input_str, tokenType= self.state219()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == ')':
                pos_start = self.position
                valid, input_str, tokenType= self.state221()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
            
            if char == '{':
                pos_start = self.position
                valid, input_str, tokenType= self.state223()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == '}':
                pos_start = self.position
                valid, input_str, tokenType= self.state225()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == '[':
                pos_start = self.position
                valid, input_str, tokenType= self.state227()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == ']':
                pos_start = self.position
                valid, input_str, tokenType= self.state229()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == '~':
                pos_start = self.position
                valid, input_str, tokenType= self.state231()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
            
            if char == ',':
                pos_start = self.position
                valid, input_str, tokenType= self.state233()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char == '\\':
                pos_start = self.position
                valid, input_str, tokenType= self.state235()

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    while self.current_char() is not None and self.current_char() not in [' ', '(']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            if char in RegDef['alpha_big']:
                pos_start = self.position
                valid, input_str, tokenType = self.state246("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )
                
            if char == '?':
                pos_start = self.position
                valid, input_str, tokenType = self.state249("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )

            if char == '"':
                pos_start = self.position
                valid, input_str, tokenType = self.state257("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )
                
            if char == "'":
                pos_start = self.position
                valid, input_str, tokenType = self.state261("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )
                
            if char in RegDef ['number']:
                pos_start = self.position
                valid, input_str, tokenType = self.state265("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )
                
            if char == ".":
                pos_start = self.position
                valid, input_str, tokenType = self.state266("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['id_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after identifier at position {self.position}"
                    )
                
                
        return self.tokens


    def state1(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state2(input_str)
            case "r":
                return self.state9(input_str)
            case _:
                return False, input_str, None
                    
    def state2(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state3(input_str)
            case _:
                return False, input_str, None

    def state3(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state4(input_str)
            case _:
                return False, input_str, None
                    
    def state4(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state5(input_str)
            case _:
                return False, input_str, None
                    
    def state5(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "v":
                return self.state6(input_str)
            case _:
                return False, input_str, None
            
    def state6(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state7(input_str)
            case _:
                return False, input_str, None
                    
    def state7(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims['witch_delim']:
            return self.state8(input_str)
        else:
            return False, input_str, None

    #Final State Believe
    def state8(self, input_str):
        return True, input_str, TokenType.BELIEVE



    def state9(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state10(input_str)
            case _:
                return False, input_str, None

    def state10(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state11(input_str)
            case _:
                return False, input_str, None 
                    
    def state11(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "k":
                return self.state12(input_str)
            case _:
                return False, input_str, None
            
    def state12(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims['gate_delim']:
            return self.state13(input_str)
        else:
            return False, input_str, None
            
    #Final State Break
    def state13(self, input_str):
        return True, input_str, TokenType.BREAK
    

    def state14(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state15(input_str)
            case "h":
                return self.state22(input_str)
            case "o":
                return self.state29(input_str)
            case "r":
                return self.state37(input_str)
            case "u":
                return self.state42(input_str)
            case _:
                return False, input_str, None
                    
    def state15(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state16(input_str)
            case _:
                return False, input_str, None

    def state16(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state17(input_str)
            case _:
                return False, input_str, None
                
    def state17(self, input_str):
        input_str += self.current_char()
        self.advance()


        if self.current_char() in Delims['gate_delim']:
            return self.state18(input_str)
        elif self.current_char()  == "l":
            return self.state19(input_str)
        else:
            return False, input_str, None

    #Final State Cast
    def state18(self, input_str):
        return True, input_str, TokenType.CAST  
    
    def state19(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state20(input_str)
            case _:
                return False, input_str, None

    def state20(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state21(input_str)
        else:
            return False, input_str, None

    #Final State Castle
    def state21(self, input_str):
        return True, input_str, TokenType.CASTLE  
    
    def state22(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state23(input_str)
            case _:
                return False, input_str, None

    def state23(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "m":
                return self.state24(input_str)
            case _:
                return False, input_str, None
                
    def state24(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "b":
                return self.state25(input_str)
            case _:
                return False, input_str, None
    
    def state25(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state26(input_str)
            case _:
                return False, input_str, None
            
    def state26(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state27(input_str)
            case _:
                return False, input_str, None

    def state27(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state28(input_str)
        else:
            return False, input_str, None

    #Final State Chamber
    def state28(self, input_str):
        return True, input_str, TokenType.CHAMBER

    def state29(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state30(input_str)
            case _:
                return False, input_str, None

    def state30(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state31(input_str)
            case _:
                return False, input_str, None
                
    def state31(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state32(input_str)
            case _:
                return False, input_str, None
    
    def state32(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state33(input_str)
            case _:
                return False, input_str, None
            
    def state33(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "u":
                return self.state34(input_str)
            case _:
                return False, input_str, None
            
    def state34(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state35(input_str)
            case _:
                return False, input_str, None

    def state35(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['gate_delim']:
            return self.state36(input_str)
        else:
            return False, input_str, None

    #Final State Continue
    def state36(self, input_str):
        return True, input_str, TokenType.CONTINUE
    
    
    def state37(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state38(input_str)
            case _:
                return False, input_str, None

    def state38(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "w":
                return self.state39(input_str)
            case _:
                return False, input_str, None
                
    def state39(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state40(input_str)
            case _:
                return False, input_str, None

    def state40(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['gate_delim']:
            return self.state41(input_str)
        else:
            return False, input_str, None

    #Final State Crown
    def state41(self, input_str):
        return True, input_str, TokenType.CROWN
    
    def state42(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state43(input_str)
            case _:
                return False, input_str, None

    def state43(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state44(input_str)
            case _:
                return False, input_str, None
                
    def state44(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state45(input_str)
            case _:
                return False, input_str, None

    def state45(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['witch_delim']:
            return self.state46(input_str)
        else:
            return False, input_str, None

    #Final State Curse
    def state46(self, input_str):
        return True, input_str, TokenType.CURSE
    

    def state47(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "y":
                return self.state48(input_str)
            case _:
                return False, input_str, None

    def state48(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state49(input_str)
            case _:
                return False, input_str, None
                
    def state49(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state50(input_str)
            case _:
                return False, input_str, None


    def state50(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state51(input_str)
            case _:
                return False, input_str, None

    def state51(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state52(input_str)
            case _:
                return False, input_str, None
                
    def state52(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "y":
                return self.state53(input_str)
            case _:
                return False, input_str, None

    def state53(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state54(input_str)
        else:
            return False, input_str, None

    #Final State Dynasty
    def state54(self, input_str):
        return True, input_str, TokenType.DYNASTY
    

    def state55(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state56(input_str)
            case _:
                return False, input_str, None

    def state56(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state57(input_str)
            case _:
                return False, input_str, None
                
    def state57(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state58(input_str)
            case _:
                return False, input_str, None


    def state58(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "v":
                return self.state59(input_str)
            case _:
                return False, input_str, None

    def state59(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state60(input_str)
            case _:
                return False, input_str, None
                
    def state60(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state61(input_str)
            case _:
                return False, input_str, None

    def state61(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state62(input_str)
        else:
            return False, input_str, None

    #Final State Forever
    def state62(self, input_str):
        return True, input_str, TokenType.FOREVER
    

    def state63(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state64(input_str)
            case _:
                return False, input_str, None

    def state64(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state65(input_str)
            case _:
                return False, input_str, None
                
    def state65(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state66(input_str)
            case _:
                return False, input_str, None


    def state66(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state67(input_str)
            case _:
                return False, input_str, None

    def state67(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state68(input_str)
            case _:
                return False, input_str, None
                
    def state68(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "d":
                return self.state69(input_str)
            case _:
                return False, input_str, None

    def state69(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state70(input_str)
        else:
            return False, input_str, None

    #Final State Granted
    def state70(self, input_str):
        return True, input_str, TokenType.GRANTED


    def state71(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state72(input_str)
            case _:
                return False, input_str, None

    def state72(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state73(input_str)
            case _:
                return False, input_str, None
                
    def state73(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state74(input_str)
            case _:
                return False, input_str, None


    def state74(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state75(input_str)
            case _:
                return False, input_str, None

    def state75(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state76(input_str)
            case _:
                return False, input_str, None

    def state76(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state77(input_str)
        else:
            return False, input_str, None

    #Final State Mirror
    def state77(self, input_str):
        return True, input_str, TokenType.MIRROR
    
    def state78(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state79(input_str)
            case _:
                return False, input_str, None

    def state79(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state80(input_str)
            case _:
                return False, input_str, None
                
    def state80(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state81(input_str)
            case _:
                return False, input_str, None


    def state81(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state82(input_str)
            case _:
                return False, input_str, None

    def state82(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state83(input_str)
        else:
            return False, input_str, None
        
    #Final State Ocean
    def state83(self, input_str):
        return True, input_str, TokenType.OCEAN
    
    def state84(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "h":
                return self.state85(input_str)
            case _:
                return False, input_str, None

    def state85(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state86(input_str)
            case _:
                return False, input_str, None
                
    def state86(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state87(input_str)
            case _:
                return False, input_str, None


    def state87(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state88(input_str)
            case _:
                return False, input_str, None
            
    def state88(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state89(input_str)
            case _:
                return False, input_str, None
    
    def state89(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "m":
                return self.state90(input_str)
            case _:
                return False, input_str, None

    def state90(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['gate_delim']:
            return self.state91(input_str)
        else:
            return False, input_str, None
        
        #Final State Phantom
    def state91(self, input_str):
        return True, input_str, TokenType.PHANTOM
    
    
    def state92(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state93(input_str)
            case "o":
                return self.state104(input_str)
            case _:
                return False, input_str, None

    def state93(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state94(input_str)
            case "t":
                return self.state98(input_str)
            case _:
                return False, input_str, None
                
    def state94(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "g":
                return self.state95(input_str)
            case _:
                return False, input_str, None


    def state95(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state96(input_str)
            case _:
                return False, input_str, None

    def state96(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['gate_delim']:
            return self.state97(input_str)
        else:
            return False, input_str, None
        
    #Final State reign
    def state97(self, input_str):
        return True, input_str, TokenType.REIGN
    
    def state98(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "u":
                return self.state99(input_str)
            case _:
                return False, input_str, None


    def state99(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state100(input_str)
            case _:
                return False, input_str, None
            

    def state100(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state101(input_str)
            case _:
                return False, input_str, None

    def state101(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state102(input_str)
        else:
            return False, input_str, None
        
    #Final State return
    def state102(self, input_str):
        return True, input_str, TokenType.RETURN    
    
    def state104(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state105(input_str)
            case _:
                return False, input_str, None


    def state105(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state106(input_str)
            case _:
                return False, input_str, None
            

    def state106(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state107(input_str)
        else:
            return False, input_str, None
        
    #Final State rose
    def state107(self, input_str):
        return True, input_str, TokenType.ROSE    

    def state108(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state109(input_str)
            case "p":
                return self.state115(input_str)
            case _:
                return False, input_str, None   

    def state109(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state110(input_str)
            case _:
                return False, input_str, None
            
    def state110(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state111(input_str)
            case _:
                return False, input_str, None
            
    def state111(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state112(input_str)
            case _:
                return False, input_str, None
    
    def state112(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state113(input_str)
            case _:
                return False, input_str, None
            

    def state113(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state114(input_str)
        else:
            return False, input_str, None
        
    #Final State rose
    def state114(self, input_str):
        return True, input_str, TokenType.ROSE    
    
    
    def state115(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state116(input_str)
            case _:
                return False, input_str, None
            
    def state116(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state117(input_str)
            case _:
                return False, input_str, None
            
    def state117(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state118(input_str)
            case _:
                return False, input_str, None

    def state118(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state119(input_str)
        else:
            return False, input_str, None
        
    #Final State spell
    def state119(self, input_str):
        return True, input_str, TokenType.SPELL  
    
    def state120(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state121(input_str)
            case "o":
                return self.state125(input_str)
            case "r":
                return self.state154(input_str)
            case "w":
                return self.state163(input_str)
            case _:
                return False, input_str, None
            
    def state121(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state122(input_str)
            case _:
                return False, input_str, None
            
    def state122(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state123(input_str)
            case _:
                return False, input_str, None

    def state123(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state124(input_str)
        else:
            return False, input_str, None
        
    #Final State tale
    def state124(self, input_str):
        return True, input_str, TokenType.TALE
    
    def state125(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state126(input_str)
            case "r":
                return self.state132(input_str)
            case "s":
                return self.state137(input_str)
            case "t":
                return self.state144(input_str)
            case _:
                return False, input_str, None
            
    def state126(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state127(input_str)
            case _:
                return False, input_str, None
    
    def state127(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state128(input_str)
            case _:
                return False, input_str, None

    def state128(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state129(input_str)
            case _:
                return False, input_str, None
    
    def state129(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state130(input_str)
            case _:
                return False, input_str, None

    def state130(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state131(input_str)
        else:
            return False, input_str, None
        
    #Final State toocean
    def state131(self, input_str):
        return True, input_str, TokenType.TOOCEAN
    

    def state132(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state133(input_str)
            case _:
                return False, input_str, None
    
    def state133(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state134(input_str)
            case _:
                return False, input_str, None

    def state134(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state135(input_str)
            case _:
                return False, input_str, None

    def state135(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state136(input_str)
        else:
            return False, input_str, None
        
    #Final State torose
    def state136(self, input_str):
        return True, input_str, TokenType.TOROSE
    

    def state137(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state138(input_str)
            case _:
                return False, input_str, None
    
    def state138(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state139(input_str)
            case _:
                return False, input_str, None

    def state139(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state140(input_str)
            case _:
                return False, input_str, None

    def state140(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state141(input_str)
            case _:
                return False, input_str, None
    
    def state141(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state142(input_str)
            case _:
                return False, input_str, None

    def state142(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state143(input_str)
        else:
            return False, input_str, None
        
    #Final State torose
    def state143(self, input_str):
        return True, input_str, TokenType.TOSCROLL
    
    def state144(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state145(input_str)
            case _:
                return False, input_str, None
    
    def state145(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state146(input_str)
            case _:
                return False, input_str, None

    def state146(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state147(input_str)
            case _:
                return False, input_str, None

    def state147(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state148(input_str)
            case _:
                return False, input_str, None
    
    def state148(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "u":
                return self.state149(input_str)
            case _:
                return False, input_str, None
            
    def state149(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state150(input_str)
            case _:
                return False, input_str, None

    def state150(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state151(input_str)
            case _:
                return False, input_str, None
    
    def state151(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state152(input_str)
            case _:
                return False, input_str, None

    def state152(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state153(input_str)
        else:
            return False, input_str, None
        
    #Final State torose
    def state153(self, input_str):
        return True, input_str, TokenType.TOSCROLL
    
    def state154(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state155(input_str)
            case _:
                return False, input_str, None
    
    def state155(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state156(input_str)
            case _:
                return False, input_str, None
    
    def state156(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state157(input_str)
            case _:
                return False, input_str, None
    
    def state157(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "u":
                return self.state158(input_str)
            case _:
                return False, input_str, None
    
    def state158(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state159(input_str)
            case _:
                return False, input_str, None
    
    def state159(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state160(input_str)
            case _:
                return False, input_str, None
            
    def state160(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state161(input_str)
            case _:
                return False, input_str, None

    def state161(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state162(input_str)
        else:
            return False, input_str, None
        
    #Final State treasures
    def state162(self, input_str):
        return True, input_str, TokenType.TREASURES
    
    def state163(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state164(input_str)
            case _:
                return False, input_str, None
            
    def state164(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state165(input_str)
            case _:
                return False, input_str, None
    
    def state165(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state166(input_str)
            case _:
                return False, input_str, None

    def state166(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state167(input_str)
        else:
            return False, input_str, None
        
    #Final State twist
    def state167(self, input_str):
        return True, input_str, TokenType.TWIST
    
    def state168(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state169(input_str)
            case _:
                return False, input_str, None
    
    def state169(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state170(input_str)
            case _:
                return False, input_str, None
            
    def state170(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "h":
                return self.state171(input_str)
            case _:
                return False, input_str, None
            

    def state171(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state172(input_str)
        else:
            return False, input_str, None
        
    #Final State wish
    def state172(self, input_str):
        return True, input_str, TokenType.WISH

#Symbols

    def state173(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['equal_delim']:
            return self.state174(input_str)
        elif self.current_char() == "=":
            return self.state175(input_str)
        else:
            return False, input_str, None
    
    #Final State equal
    def state174(self, input_str):
        return True, input_str, TokenType.EQUAL
    
    def state175(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state176(input_str)
        else:
            return False, input_str, None

    #Final State relational ==
    def state176(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state177(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['plus_delim']:
            return self.state178(input_str)
        elif self.current_char() == "+":
            return self.state179(input_str)
        elif self.current_char() == "=":
            return self.state181(input_str)
        else:
            return False, input_str, None

            
    #Final State arithmetic operator +
    def state178(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state179(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['unary_operator_delim']:
            return self.state180(input_str)
        else:
            return False, input_str, None
        
        
    #Final State unary ++
    def state180(self, input_str):
        return True, input_str, TokenType.UNARY_OPERATOR
    
    def state181(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state182(input_str)
        else:
            return False, input_str, None
    
     #Final State assignment +=
    def state182(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state183(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim'] and self.current_char() not in RegDef ['number']:
            return self.state184(input_str)
        elif self.current_char() == "-":
            return self.state185(input_str)
        elif self.current_char() == "=":
            return self.state187(input_str)
        elif self.current_char() in RegDef ['number']:
            return self.state265(input_str)
        elif self.current_char() == ".":
            return self.state266(input_str)
        else:
            return False, input_str, None
            
    #Final State arithmetic operator -
    def state184(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state185(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['unary_operator_delim']:
            return self.state186(input_str)
        else:
            return False, input_str, None
        
    #Final State unary --
    def state186(self, input_str):
        return True, input_str, TokenType.UNARY_OPERATOR
    
    def state187(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state188(input_str)
        else:
            return False, input_str, None
        
     #Final State assignment -=
    def state188(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
            
    def state189(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state190(input_str)
        elif self.current_char() == "=":
            return self.state191(input_str)
        else:
            return False, input_str, None
    
    #Final State arithmetic operator * 
    def state190(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state191(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state192(input_str)
        else:
            return False, input_str, None

    #Final State assignment operator *=
    def state192(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    

    def state193(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state194(input_str)
        elif self.current_char() == "=":
            return self.state195(input_str)
        else:
            return False, input_str, None

    #Final State arithmetic operator / 
    def state194(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state195(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state196(input_str)
        else:
            return False, input_str, None

    #Final State assignment operator /=
    def state196(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state197(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state198(input_str)
        elif self.current_char() == "=":
            return self.state199(input_str)
        else:
            return False, input_str, None
    
    #Final State arithmetic operator %
    def state198(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state199(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state200(input_str)
        else:
            return False, input_str, None

    #Final State assignment operator %=
    def state200(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state201(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['not_logical_delim']:
            return self.state202(input_str)
        elif self.current_char() == "=":
            return self.state203(input_str)
        else:
            return False, input_str, None
    
    #Final State arithmetic operator !
    def state202(self, input_str):
        return True, input_str, TokenType.NOT
    
    def state203(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state204(input_str)
        else:
            return False, input_str, None

    #Final State assignment operator !=
    def state204(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state205(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "&":
                return self.state206(input_str)
            case _:
                return False, input_str, None
            
    def state206(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['rlogical_operator_delim']:
            return self.state207(input_str)
        else:
            return False, input_str, None
    
    #Final State logical operator &&
    def state207(self, input_str):
        return True, input_str, TokenType.LOGICAL_OPERATOR
    
    def state208(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "|":
                return self.state209(input_str)
            case _:
                return False, input_str, None
            
    def state209(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['rlogical_operator_delim']:
            return self.state210(input_str)
        else:
            return False, input_str, None
    
    #Final State logical operator ||
    def state210(self, input_str):
        return True, input_str, TokenType.LOGICAL_OPERATOR
    

    def state211(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state212(input_str)
        elif self.current_char() == "=":
            return self.state213(input_str)
        else:
            return False, input_str, None

    #Final State relational operator >
    def state212(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
            
    def state213(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state214(input_str)
        else:
            return False, input_str, None
    
    #Final State relational operator >=
    def state214(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state215(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state216(input_str)
        elif self.current_char() == "=":
            return self.state217(input_str)
        else:
            return False, input_str, None

            
    #Final State relational operator <
    def state216(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
            
    def state217(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state218(input_str)
        else:
            return False, input_str, None
    
    #Final State relational operator <=
    def state218(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    
    def state219(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_parentheses_delim']:
            return self.state220(input_str)
        else:
            return False, input_str, None
            
    #Final State Open Parenthesis
    def state220(self, input_str):
        return True, input_str, TokenType.OPEN_PAREN
    

    def state221(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_parentheses_delim']:
            return self.state222(input_str)
        else:
            return False, input_str, None

            
    #Final State Close Parenthesis
    def state222(self, input_str):
        return True, input_str, TokenType.CLOSE_PAREN
    
    def state223(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_curly_bracket_delim']:
            return self.state224(input_str)
        else:
            return False, input_str, None

            
    #Final State Open Curly Bracket
    def state224(self, input_str):
        return True, input_str, TokenType.OPEN_CURLY
    
    def state225(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_curly_bracket_delim']:
            return self.state226(input_str)
        else:
            return False, input_str, None

            
    #Final State Close Curly Bracket
    def state226(self, input_str):
        return True, input_str, TokenType.CLOSE_CURLY
    

    def state227(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_square_bracket_delim']:
            return self.state228(input_str)
        else:
            return False, input_str, None

    #Final State Open Square Bracket
    def state228(self, input_str):
        return True, input_str, TokenType.OPEN_SQUARE
    
    def state229(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_square_bracket_delim']:
            return self.state230(input_str)
        else:
            return False, input_str, None

            
    #Final State Close Square Bracket
    def state230(self, input_str):
        return True, input_str, TokenType.CLOSE_SQUARE
    
    def state231(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['terminator_delim']:
            return self.state232(input_str)
        else:
            return False, input_str, None
            
    #Final State Terminator ~
    def state232(self, input_str):
        return True, input_str, TokenType.TERMINATOR
    

    def state233(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['comma_delim']:
            return self.state234(input_str)
        else:
            return False, input_str, None
        
    #Final State Comma , 
    def state234(self, input_str):
        return True, input_str, TokenType.COMMA
    
    def state235(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state236(input_str)
            case "t":
                return self.state238(input_str)
            case "\\":
                return self.state240(input_str)
            case '"':
                return self.state244(input_str)
            case _:
                return False, input_str, None
    
    def state236(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state237(input_str)
        else:
            return False, input_str, None
            
    #Final State escape sequence \n 
    def state237(self, input_str):
        return True, input_str, TokenType.ESCAPE_NEWLINE
    
    def state238(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state239(input_str)
        else:
            return False, input_str, None

            
    #Final State escape sequence \t 
    def state239(self, input_str):
        return True, input_str, TokenType.ESCAPE_TAB
    
    def state240(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state241(input_str)
        else:
            return False, input_str, None

            
    #Final State escape sequence \n 
    def state241(self, input_str):
        return True, input_str, TokenType.ESCAPE_BACKSLASH
    
    def state244(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state245(input_str)
        else:
            return False, input_str, None

            
    #Final State escape sequence \n 
    def state245(self, input_str):
        return True, input_str, TokenType.ESCAPE_QUOTE
    

    def state246(self, input_str):
        """Initial state for identifiers."""
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['alphanum'] | {'_'}:
            return self.state247(input_str)  # Transition to state247
        elif self.current_char() in Delims['id_delim']:
            return self.state248(input_str)  # Transition to final state
        else:
            return False, input_str, None

    def state247(self, input_str):
        """Intermediate state for identifiers."""
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['alphanum'] | {'_'}:
            return self.state247(input_str)  # Stay in state247
        elif self.current_char() in Delims['id_delim']:
            return self.state248(input_str)  # Transition to final state
        else:
            return False, input_str, None

    def state248(self, input_str):
        """Final state for identifiers."""
        return True, input_str, TokenType.IDENTIFIER
    
    # General alphanum state (e.g., for '1' following '\n')
    def state_alphanum(self, input_str):
        while self.current_char() and self.current_char().isalnum():
            input_str += self.current_char()
            self.advance()
        return True, input_str, TokenType.ALPHANUM
    

    def state249(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() == ' ' and self.current_char() != '*':
            return self.state250(input_str)   
        elif self.current_char() == '\n':
            return self.state251(input_str)  
        elif self.current_char() == '*':
            return self.state252(input_str) 
        else:
            return False, input_str, None

    def state250(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() in ['\t', ' '] and self.current_char() != '*':
            return self.state250(input_str) 
        elif self.current_char() == '\n':
            return self.state251(input_str) 
        else:
            return False, input_str, None

    def state251(self, input_str):
        return True, input_str, TokenType.SINGLE_COMMENT
    
    def state252(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() in ['\t', ' ', '\n'] and self.current_char() != '*':
            return self.state253(input_str) 
        elif self.current_char() == '*':
            return self.state254(input_str) 
        else:
            return False, input_str, None

    def state253(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() in ['\t', ' ', '\n'] and self.current_char() != '*':
            return self.state253(input_str) 
        elif self.current_char() == '*':
            return self.state254(input_str) 
        else:
            return False, input_str, None
        
    def state254(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() == '?':
            return self.state255(input_str) 
        else:
            return False, input_str, None
        
    def state255(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['multi-comment_delim']:
            return self.state256(input_str) 
        else:
            return False, input_str, None
        
    def state256(self, input_str):
        return True, input_str, TokenType.MULTI_COMMENT

    def state257(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() in RegDef['escape_seq'] or self.current_char() in ['\t', ' ']  and self.current_char() not in ['"', '\n']:
            return self.state258(input_str)   
        else:
            return False, input_str, None

    def state258(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() in RegDef['escape_seq'] or self.current_char() in ['\t', ' ']  and self.current_char() not in ['\n']:
            return self.state258(input_str)   
        elif self.current_char() == '"':
            return self.state259(input_str) 
        else:
            return False, input_str, None

    def state259(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['book_delim']:
            return self.state260(input_str)   
        else:
            return False, input_str, None
        
    def state260(self, input_str):
        return True, input_str, TokenType.STRING_LITERAL

    def state261(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['ascii'] or self.current_char() == ' '  and self.current_char() not in ["'"]:
            return self.state262(input_str)   
        else:
            return False, input_str, None

    def state262(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() == "'":
            return self.state263(input_str) 
        else:
            return False, input_str, None

    def state263(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['book_delim']:
            return self.state264(input_str)   
        else:
            return False, input_str, None
        
    def state264(self, input_str):
        return True, input_str, TokenType.CHAR_LITERAL


    def state265(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['number']  and self.current_char() not in ["."]:
            return self.state265(input_str) 
        elif self.current_char() == ".":
            return self.state266(input_str)  
        elif self.current_char() in Delims['number_delim']:
            return self.state267(input_str) 
        else:
            return False, input_str, None

    def state266(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() in RegDef['number']:
            return self.state266(input_str) 
        elif self.current_char() in Delims['number_delim']:
            return self.state268(input_str)
        else:
            return False, input_str, None
        
    def state267(self, input_str):
        normalized = self.normalize_integer(input_str)
        return True, normalized, TokenType.INT_LITERAL
    
    def state268(self, input_str):
        normalized = self.normalize_float(input_str)
        return True, normalized, TokenType.FLOAT_LITERAL

    def normalize_integer(self, input_str):
        """Removes leading zeros from an integer literal, ensuring '0' is preserved."""
        normalized = input_str.lstrip('0')
        return normalized if normalized else '0'

    def normalize_float(self, input_str):
        """Removes trailing zeros from a float literal and the decimal point if necessary."""
        if '.' in input_str:
            integer_part, fractional_part = input_str.split('.', 1)
            fractional_part = fractional_part.rstrip('0')
            if fractional_part:
                normalized_integer = integer_part.lstrip('0') or '0'
                return f"{normalized_integer}.{fractional_part}"
            else:
                # All fractional digits were zeros; return integer part only
                return self.normalize_integer(integer_part)
        return self.normalize_integer(input_str)


class RoyalScriptLexerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("RoyalScript Lexer")
        self.geometry("945x700")

        # Load the image and set it as the background
        self.bg_image = Image.open("3.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((945, 700), Image.Resampling.LANCZOS)  # Resize to fit window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label to place the image as background
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Create frames for each section without background color
        self.left_frame = tk.Frame(self, bg="#ff87d1")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.middle_frame = tk.Frame(self, bg="#ff87d1")
        self.middle_frame.grid(row=0, column=1, padx=0, pady=20, sticky="nsew")

        self.right_frame = tk.Frame(self, bg="#ff87d1")
        self.right_frame.grid(row=0, column=2, padx=0, pady=20, sticky="nsew")

        # Errors and Program Frame (combined)
        self.bottom_frame = tk.Frame(self, bg="#ff87d1")
        self.bottom_frame.grid(row=1, column=0, columnspan=3, padx=21, pady=5, sticky="nsew")

        # Program Frame: Below the errors frame
        self.program_frame = tk.Frame(self, bg="#ff87d1")
        self.program_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Left: Input code with title (larger box)
        self.input_label = tk.Label(self.left_frame, text="Input Code", fg="white", font=("Arial", 14, "bold"), bg="#ff87d1")
        self.input_label.grid(row=0, column=0)
        self.input_text = scrolledtext.ScrolledText(self.left_frame, width=60, height=20, wrap=tk.WORD, fg="#d60083")
        self.input_text.grid(row=1, column=0, padx=0, pady=5)

        # Middle: Lexer output with title (same width as the token box)
        self.output_label = tk.Label(self.middle_frame, text="Lexer", fg="white", font=("Arial", 14, "bold"), bg="#ff87d1")
        self.output_label.grid(row=0, column=0)
        self.output_listbox = tk.Listbox(self.middle_frame, width=30, height=20, justify="center", fg="#d60083")
        self.output_listbox.grid(row=1, column=0, padx=0, pady=5)

        # Right: Tokens with title (same width as lexer output)
        self.tokens_label = tk.Label(self.right_frame, text="Tokens", fg="white", font=("Arial", 14, "bold"), bg="#ff87d1")
        self.tokens_label.grid(row=0, column=0)
        self.token_listbox = tk.Listbox(self.right_frame, width=30, height=20, justify="center", fg="#d60083")
        self.token_listbox.grid(row=1, column=0, padx=0, pady=5)

        # Errors Box (left side of the combined frame)
        self.errors_label = tk.Label(self.bottom_frame, text="Errors", fg="white", font=("Arial", 14, "bold"), bg="#ff87d1")
        self.errors_label.grid(row=0, column=0, padx=5)
        self.errors_listbox = tk.Listbox(self.bottom_frame, width=145, height=10, fg="red")
        self.errors_listbox.grid(row=1, column=0, padx=5, pady=5)

      
        # Create a Canvas to simulate the multi-colored button
        self.analyze_button = tk.Canvas(self, height=50, width=200, highlightthickness=0, relief="raised", bg="#f7e1d3")  # Canvas widget as a button
        self.analyze_button.grid(row=3, column=0, columnspan=3, pady=0)

        # Add multi-colored text to the Canvas with proper spacing
        self.analyze_button.create_text(20, 25, text="✨", font=("Arial", 14, "bold"), fill="#efbf04")
        self.analyze_button.create_text(100, 25, text="Analyze Code", font=("Arial", 14, "bold"), fill="#d60083")  # Adjusted x position for spacing
        self.analyze_button.create_text(180, 25, text="✨", font=("Arial", 14, "bold"), fill="#efbf04")

        # Bind the Canvas click event to the analyze_code function
        self.analyze_button.bind("<Button-1>", self.analyze_code)

        # Add hover effect (when mouse enters)
        self.analyze_button.bind("<Enter>", self.on_hover)
        self.analyze_button.bind("<Leave>", self.on_leave)

    def analyze_code(self, event=None):
        """Method to analyze the code provided in the input_text area."""
        # Getting the code from the text widget
        code = self.input_text.get("1.0", tk.END)
        
        # Create the lexer object
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.errors_listbox.delete(0, tk.END)

        try:
            # Tokenize the input code
            tokens = lexer.get_tokens()
            
            # Show tokens with color-coding
            for token in tokens:
                self.output_listbox.insert(tk.END, f"{token.value}\n")
                
                # Optionally, assign colors based on token type
                if token.token_type == TokenType.WHITESPACE:
                    color = "grey"
                elif token.token_type in [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL]:
                    color = "blue"
                elif token.token_type in [TokenType.STRING_LITERAL, TokenType.CHAR_LITERAL]:
                    color = "green"
                elif token.token_type in [TokenType.BOOL_LITERAL, TokenType.NULL_LITERAL]:
                    color = "purple"
                elif token.token_type == TokenType.IDENTIFIER:
                    color = "black"
                elif token.token_type == "ERROR":
                    color = "red"
                else:
                    color = "orange"
                
                # Insert into token listbox with color (requires using a Text widget instead of Listbox)
                # For simplicity, we continue using Listbox without color-coding
                if token.token_type in TokenType.__dict__.values():
                    definition = token.token_type.replace("_", "")
                    self.token_listbox.insert(tk.END, f"{definition}")

        except SyntaxError as e:
            # Display error messages in the Errors Box
            self.errors_listbox.insert(tk.END, f"{str(e)}\n")
        except Exception as e:
            # Handle any unexpected errors
            self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}\n")

    # Change the button's appearance when hovered
    def on_hover(self, event):
        self.analyze_button.config(bg="#f0a6ca")  # Change background on hover

    # Change the button's appearance when mouse leaves
    def on_leave(self, event):
        self.analyze_button.config(bg="#f7e1d3")  # Reset the background when mouse leaves


if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()