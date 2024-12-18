import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk 
import re
from RS_RegDef  import Delims
from RS_RegDef  import RegDef
from decimal import Decimal, ROUND_HALF_UP



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
    CROWN = "START"
    REIGN = "END"
    SPELL = "USER DEFINED FUNCTION"  # For function declarations
    CASTLE = "MAIN FUNCTION"  # Main function
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
    BELIEVE = "CONDITIONAL - DO"
    FOREVER = "CONDITIONAL - WHILE"
    BREAK = "FLOW CONTROL"
    CONTINUE = "FLOW CONTROL"
    RETURN = "RETURN"

    # Data types
    TREASURES = "DATA TYPE - INT"  # int
    OCEAN = "DATA TYPE - FLOAT"  # float
    SCROLL = "DATA TYPE - STRING"  # string
    ROSE = "DATA TYPE - CHAR"  # char
    MIRROR = "DATA TYPE - BOOL"  # boolean
    CHAMBER = "DATA TYPE - VOID"  # void
    DYNASTY = "RETURN TYPE - CONSTANT"  # constant
    PHANTOM = "NULL"

    # Literals
    NEG_TREASURES_INT = "NEG-TREASURES LITERAL"
    POS_TREASURES_INT = "POS-REASURES LITERAL"
    NEG_FLOAT_LITERAL = "NEG-FLOAT LITERAL"
    POS_FLOAT_LITERAL = "POS-FLOAT LITERAL"
    STRING_LITERAL = "STRING LITERAL"
    CHAR_LITERAL = "CHAR LITERAL"
    BOOL_LITERAL = "BOOL LITERAL"
    NULL_LITERAL = "NULL LITERAL"

    # Operatorsi 
    ASSIGNMENT_OPERATOR = "ASSIGNMENT OPERATOR"
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

    ESCAPE_NEWLINE = "ESCAPE-NEWLINE"
    ESCAPE_TAB = "ESCAPE-TAB"
    ESCAPE_BACKSLASH = "ESCAPE-BACKSLASH"
    ESCAPE_QUOTE = "ESCAPE-QUOTE"

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

    def get_tokens(self):
        """Tokenize the entire input code"""
        while self.position < len(self.code):
            char = self.current_char()

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

            #RESERVED WORDS
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
                valid, input_str, tokenType= self.state68()

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
                valid, input_str, tokenType= self.state76()

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
                valid, input_str, tokenType= self.state83()

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
                valid, input_str, tokenType= self.state89()

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
                valid, input_str, tokenType= self.state97()

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
                valid, input_str, tokenType= self.state112()

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
                valid, input_str, tokenType= self.state124()

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
                valid, input_str, tokenType= self.state175()

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


            #RESERVED SYMBOL
            if char == '=':
                pos_start = self.position
                valid, input_str, tokenType= self.state180()

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
                valid, input_str, tokenType= self.state184()

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
                valid, input_str, tokenType= self.state190()

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
                valid, input_str, tokenType= self.state196()

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
                valid, input_str, tokenType= self.state200()

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
                valid, input_str, tokenType= self.state204()

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
                
            if char == '&':
                pos_start = self.position
                valid, input_str, tokenType= self.state212()

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

            if char == '>':
                pos_start = self.position
                valid, input_str, tokenType= self.state218()

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
                valid, input_str, tokenType= self.state222()

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
                valid, input_str, tokenType= self.state226()

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
                valid, input_str, tokenType= self.state228()

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
                valid, input_str, tokenType= self.state230()

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
                valid, input_str, tokenType= self.state232()

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
                valid, input_str, tokenType= self.state234()

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
                valid, input_str, tokenType= self.state236()

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
                valid, input_str, tokenType= self.state238()

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
                valid, input_str, tokenType= self.state240()

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
                valid, input_str, tokenType= self.state242()

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


            #IDENTIFIER    
            if char in RegDef['alpha_big']:
                pos_start = self.position
                valid, input_str, tokenType = self.state251("")

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
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
            #COMMENTS
            if char == '?':
                pos_start = self.position
                valid, input_str, tokenType = self.state270("")

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
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )


            #SCROLL LITERALS 
            if char == '"':
                pos_start = self.position
                valid, input_str, tokenType = self.state263("")

                if valid:
                    # Append the recognized token
                    self.tokens.append(Token(input_str, tokenType, pos_start))
                else:
                    # Handle invalid input
                    while self.current_char() is not None and self.current_char() not in Delims['book_delim']:
                        char = self.current_char()
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )


            #ROSE LITERALS    
            if char == "'":
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
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
            

            #TREASURES & FLOAT LITERALS
            if char in RegDef ['number']:
                pos_start = self.position
                valid, input_str, tokenType = self.state255("")

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
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
            
            
            #FLOAT LITERALS STARTING WITH .
            if char == ".":
                pos_start = self.position
                valid, input_str, tokenType = self.state258("")

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
                        f"Expected delimiter after '{input_str}' at position {self.position}"
                    )
                
        return self.tokens


    #==================================================#
    #            STATES => RESERVED WORDS              #
    #==================================================#
    #   STATE 1 - STATE 8 => BELIEVE                   #
    #   STATE 1 & STATE 9-13 => BREAK                  #
    #   STATE 14 - STATE 18 => CAST                    #
    #   STATE 17 & STATE 19-21 => CASTLE               #
    #   STATE 14 & STATE 22-28 => CHAMBER              #
    #   STATE 14 & STATE 29-36 => CONTINUE             #
    #   STATE 14 & STATE 37-41 => CROWN                #
    #   STATE 14 & STATE 42-46 => CURSE                #
    #   STATE 47 - STATE 54 => DYNASTY                 #
    #   STATE 55 - STATE 60 => FALSE                   #
    #   STATE 61 - STATE 67 => FOREVER                 #
    #   STATE 68 - STATE 75 => GRANTED                 #
    #   STATE 76 - STATE 82 => MIRROR                  #
    #   STATE 83 - STATE 88 => OCEAN                   #
    #   STATE 89 - STATE 96 => PHANTOM                 #
    #   STATE 97 - STATE 102 => REIGN                  #
    #   STATE 98 & STATE 103-107 => RETURN             #
    #   STATE 97 & STATE 108-111 => ROSE               #
    #   STATE 112 - STATE 118 => SCROLL                #
    #   STATE 112 & STATE 119-123 => SPELL             #
    #   STATE 124 - STATE 128 => TALE                  #
    #   STATE 124 & STATE 129-135 => TOOCEAN           #
    #   STATE 129 & STATE 136-140 => TOROSE            #
    #   STATE 129 & STATE 141-147 => TOSCROLL          #
    #   STATE 129 & STATE 148-157 => TOTREASURES       #
    #   STATE 124 & STATE 158-166 => TREASURES         #
    #   STATE 158 & STATE 167-169 => TRUE              #
    #   STATE 124 & STATE 170-174 => WISH              #
    #   STATE 175 - STATE 179 => WISH                  #
    #==================================================#

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
    
    #################### FINAL STATE FOR BELIEVE ####################

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
    
    #################### FINAL STATE FOR BREAK ####################
            
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


        if self.current_char() in Delims['genie_delim']:
            return self.state18(input_str)
        elif self.current_char()  == "l":
            return self.state19(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR CAST ####################

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

    #################### FINAL STATE FOR CASTLE ####################

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

    #################### FINAL STATE FOR CHAMBER ####################

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

    #################### FINAL STATE FOR CONTINUE ####################

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

    #################### FINAL STATE FOR CROWN ####################

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

    #################### FINAL STATE FOR CURSE ####################

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

    #################### FINAL STATE FOR DYNASTY ####################

    def state54(self, input_str):
        return True, input_str, TokenType.DYNASTY
    

    def state55(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state56(input_str)
            case "o":
                return self.state61(input_str)
            case _:
                return False, input_str, None

    def state56(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state57(input_str)
            case _:
                return False, input_str, None
                
    def state57(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state58(input_str)
            case _:
                return False, input_str, None


    def state58(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state59(input_str)
            case _:
                return False, input_str, None
            
    def state59(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['mirror-lit_delim']:
            return self.state60(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR FALSE ####################
        
    def state60(self, input_str):
        return True, input_str, TokenType.BOOL_LITERAL
            
    def state61(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state62(input_str)
            case _:
                return False, input_str, None
                
    def state62(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state63(input_str)
            case _:
                return False, input_str, None


    def state63(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "v":
                return self.state64(input_str)
            case _:
                return False, input_str, None

    def state64(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state65(input_str)
            case _:
                return False, input_str, None
                
    def state65(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state66(input_str)
            case _:
                return False, input_str, None

    def state66(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state67(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR FOREVER ####################

    def state67(self, input_str):
        return True, input_str, TokenType.FOREVER
    

    def state68(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state69(input_str)
            case _:
                return False, input_str, None

    def state69(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state70(input_str)
            case _:
                return False, input_str, None
                
    def state70(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state71(input_str)
            case _:
                return False, input_str, None

    def state71(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state72(input_str)
            case _:
                return False, input_str, None

    def state72(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state73(input_str)
            case _:
                return False, input_str, None
                
    def state73(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "d":
                return self.state74(input_str)
            case _:
                return False, input_str, None

    def state74(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state75(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR GRANTED ####################

    def state75(self, input_str):
        return True, input_str, TokenType.GRANTED

    def state76(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state77(input_str)
            case _:
                return False, input_str, None

    def state77(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state78(input_str)
            case _:
                return False, input_str, None
                
    def state78(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state79(input_str)
            case _:
                return False, input_str, None


    def state79(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state80(input_str)
            case _:
                return False, input_str, None

    def state80(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state81(input_str)
            case _:
                return False, input_str, None

    def state81(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state82(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR MIRROR ####################

    def state82(self, input_str):
        return True, input_str, TokenType.MIRROR
    
    def state83(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state84(input_str)
            case _:
                return False, input_str, None

    def state84(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
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

        if self.current_char() in [' ']:
            return self.state88(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR OCEAN ####################

    def state88(self, input_str):
        return True, input_str, TokenType.OCEAN
    
    def state89(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "h":
                return self.state90(input_str)
            case _:
                return False, input_str, None

    def state90(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state91(input_str)
            case _:
                return False, input_str, None
                
    def state91(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state92(input_str)
            case _:
                return False, input_str, None


    def state92(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state93(input_str)
            case _:
                return False, input_str, None
            
    def state93(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state94(input_str)
            case _:
                return False, input_str, None
    
    def state94(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "m":
                return self.state95(input_str)
            case _:
                return False, input_str, None

    def state95(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['gate_delim']:
            return self.state96(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR PHANTOM ####################
    def state96(self, input_str):
        return True, input_str, TokenType.PHANTOM
    
    
    def state97(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state98(input_str)
            case "o":
                return self.state108(input_str)
            case _:
                return False, input_str, None

    def state98(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state99(input_str)
            case "t":
                return self.state103(input_str)
            case _:
                return False, input_str, None
                
    def state99(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "g":
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

        if self.current_char() in Delims ['gate_delim']:
            return self.state102(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR REIGN ####################

    def state102(self, input_str):
        return True, input_str, TokenType.REIGN
    
    def state103(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "u":
                return self.state104(input_str)
            case _:
                return False, input_str, None

    def state104(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state105(input_str)
            case _:
                return False, input_str, None

    def state105(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
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
        
    #################### FINAL STATE FOR RETURN ####################

    def state107(self, input_str):
        return True, input_str, TokenType.RETURN    
    
    def state108(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state109(input_str)
            case _:
                return False, input_str, None


    def state109(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state110(input_str)
            case _:
                return False, input_str, None
            

    def state110(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in [' ']:
            return self.state111(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR ROSE ####################

    def state111(self, input_str):
        return True, input_str, TokenType.ROSE    

    def state112(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state113(input_str)
            case "p":
                return self.state119(input_str)
            case _:
                return False, input_str, None   

    def state113(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state114(input_str)
            case _:
                return False, input_str, None
            
    def state114(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state115(input_str)
            case _:
                return False, input_str, None
            
    def state115(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
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

        if self.current_char() in [' ']:
            return self.state118(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR SCROLL ####################

    def state118(self, input_str):
        return True, input_str, TokenType.SCROLL   
    
    
    def state119(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state120(input_str)
            case _:
                return False, input_str, None
            
    def state120(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state121(input_str)
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

        if self.current_char() in [' ']:
            return self.state123(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR SPELL ####################

    def state123(self, input_str):
        return True, input_str, TokenType.SPELL  
    
    def state124(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state125(input_str)
            case "o":
                return self.state129(input_str)
            case "r":
                return self.state158(input_str)
            case "w":
                return self.state170(input_str)
            case _:
                return False, input_str, None
            
    def state125(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state126(input_str)
            case _:
                return False, input_str, None
            
    def state126(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state127(input_str)
            case _:
                return False, input_str, None

    def state127(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state128(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TALE ####################

    def state128(self, input_str):
        return True, input_str, TokenType.TALE
    
    def state129(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state130(input_str)
            case "r":
                return self.state136(input_str)
            case "s":
                return self.state141(input_str)
            case "t":
                return self.state148(input_str)
            case _:
                return False, input_str, None
            
    def state130(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state131(input_str)
            case _:
                return False, input_str, None
    
    def state131(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state132(input_str)
            case _:
                return False, input_str, None

    def state132(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
                return self.state133(input_str)
            case _:
                return False, input_str, None
    
    def state133(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state134(input_str)
            case _:
                return False, input_str, None

    def state134(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state135(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TOOCEAN ####################

    def state135(self, input_str):
        return True, input_str, TokenType.TOOCEAN
    

    def state136(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state137(input_str)
            case _:
                return False, input_str, None
    
    def state137(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state138(input_str)
            case _:
                return False, input_str, None

    def state138(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state139(input_str)
            case _:
                return False, input_str, None

    def state139(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state140(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TOROSE ####################

    def state140(self, input_str):
        return True, input_str, TokenType.TOROSE
    

    def state141(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "c":
                return self.state142(input_str)
            case _:
                return False, input_str, None
    
    def state142(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state143(input_str)
            case _:
                return False, input_str, None

    def state143(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "o":
                return self.state144(input_str)
            case _:
                return False, input_str, None

    def state144(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state145(input_str)
            case _:
                return False, input_str, None
    
    def state145(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state146(input_str)
            case _:
                return False, input_str, None

    def state146(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state147(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TOSCROLL ####################

    def state147(self, input_str):
        return True, input_str, TokenType.TOSCROLL
    
    def state148(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state149(input_str)
            case _:
                return False, input_str, None
    
    def state149(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state150(input_str)
            case _:
                return False, input_str, None

    def state150(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
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

        match self.current_char():
            case "u":
                return self.state153(input_str)
            case _:
                return False, input_str, None
            
    def state153(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state154(input_str)
            case _:
                return False, input_str, None

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
            case "s":
                return self.state156(input_str)
            case _:
                return False, input_str, None

    def state156(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state157(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TOTREASURES ####################

    def state157(self, input_str):
        return True, input_str, TokenType.TOTREASURES
    
    def state158(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state159(input_str)
            case "u":
                return self.state167(input_str)
            case _:
                return False, input_str, None
    
    def state159(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "a":
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

        match self.current_char():
            case "u":
                return self.state162(input_str)
            case _:
                return False, input_str, None
    
    def state162(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "r":
                return self.state163(input_str)
            case _:
                return False, input_str, None
    
    def state163(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
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

        if self.current_char() in Delims ['genie_delim']:
            return self.state166(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TREASURES ####################

    def state166(self, input_str):
        return True, input_str, TokenType.TREASURES
    
    def state167(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state168(input_str)
            case _:
                return False, input_str, None
            
    def state168(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['mirror-lit_delim']:
            return self.state169(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR TRUE ####################

    def state169(self, input_str):
        return True, input_str, TokenType.BOOL_LITERAL
    
    def state170(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state171(input_str)
            case _:
                return False, input_str, None
            
    def state171(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state172(input_str)
            case _:
                return False, input_str, None
    
    def state172(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "t":
                return self.state173(input_str)
            case _:
                return False, input_str, None

    def state173(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state174(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR TWIST ####################

    def state174(self, input_str):
        return True, input_str, TokenType.TWIST
    
    def state175(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state176(input_str)
            case _:
                return False, input_str, None
    
    def state176(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "s":
                return self.state177(input_str)
            case _:
                return False, input_str, None
            
    def state177(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "h":
                return self.state178(input_str)
            case _:
                return False, input_str, None
            

    def state178(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['genie_delim']:
            return self.state179(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR WISH ####################

    def state179(self, input_str):
        return True, input_str, TokenType.WISH

    #==================================================#
    #               STATES => SYMBOLS                  #
    #==================================================#
    #   STATE 180 - STATE 181 => -                     #
    #   STATE 180 & STATE 182-183 => -=                #
    #   STATE 184 - STATE 185 => +                     #
    #   STATE 184 & STATE 186-187 => ++                #
    #   STATE 184 & STATE 188-189 => +=                #
    #   STATE 190 - STATE 191 => -                     #
    #   STATE 190 & STATE 192-193 => --                #
    #   STATE 190 & STATE 194-195 => -=                #
    #   STATE 196 - STATE 197 => *                     #
    #   STATE 196 & STATE 198-199 => *=                 #
    #   STATE 200 - STATE 201 => /                     #
    #   STATE 200 & STATE 202-203 => /=                #
    #   STATE 204 - STATE 205 => %                     #
    #   STATE 204 & STATE 206-207 => %=                #
    #   STATE 208 - STATE 209 => !                     #
    #   STATE 208 & STATE 210-211 => !=                #
    #   STATE 212 - STATE 214 => &&                    #
    #   STATE 215 - STATE 217 => ||                    #
    #   STATE 218 - STATE 219 => >                     #
    #   STATE 218 & STATE 220-221 => >=                #
    #   STATE 222 - STATE 223 => <                     #
    #   STATE 222 & STATE 224-225 => <=                #
    #   STATE 226 - STATE 227 => (                     #
    #   STATE 228 - STATE 229 => )                     #
    #   STATE 230 - STATE 231 => {                     #
    #   STATE 232 - STATE 233 => }                     #
    #   STATE 234 - STATE 235 => [                     #
    #   STATE 236 - STATE 237 => ]                     #
    #   STATE 238 - STATE 239 => ~                     #
    #   STATE 240 - STATE 241 => ,                     #
    #   STATE 242 - STATE 244 => \n                    #
    #   STATE 242 & STATE 245-246 => \t                #
    #   STATE 242 & STATE 247-248 => \\                #
    #   STATE 242 & STATE 249-250 => \"                #
    #==================================================#

    def state180(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['equal_delim']:
            return self.state181(input_str)
        elif self.current_char() == "=":
            return self.state182(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR EQUAL (=) ####################

    def state181(self, input_str):
        return True, input_str, TokenType.EQUAL
    
    def state182(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state183(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR RELATIONAL (==) ####################
    def state183(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state184(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['plus_delim']:
            return self.state185(input_str)
        elif self.current_char() == "+":
            return self.state186(input_str)
        elif self.current_char() == "=":
            return self.state188(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR ARITHMETIC OPERATOR (+) ####################

    def state185(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state186(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['unary_operator_delim']:
            return self.state187(input_str)
        else:
            return False, input_str, None
        
        
    #################### FINAL STATE FOR UNARY OPERATOR (++) ####################
    def state187(self, input_str):
        return True, input_str, TokenType.UNARY_OPERATOR
    
    def state188(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state189(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR ASSIGNMENT OPERATOR (+=) ####################

    def state189(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state190(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim'] and self.current_char() not in RegDef ['number']:
            return self.state191(input_str)
        elif self.current_char() == "-":
            return self.state192(input_str)
        elif self.current_char() == "=":
            return self.state194(input_str)
        elif self.current_char() in RegDef ['number']:
            return self.state253(input_str)
        elif self.current_char() == ".":
            return self.state257(input_str)
        else:
            return False, input_str, None
            
    #################### FINAL STATE FOR ARITHMETIC OPERATOR (-) ####################

    def state191(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state192(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['unary_operator_delim']:
            return self.state193(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR UNARY OPERATOR (--) ####################

    def state193(self, input_str):
        return True, input_str, TokenType.UNARY_OPERATOR
    
    def state194(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state195(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR ASSIGNMENT OPERATOR (-=) ####################
    def state195(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state196(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state197(input_str)
        elif self.current_char() == "=":
            return self.state198(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR ARITHMETIC OPERATOR (*) ####################
    def state197(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state198(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state199(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR ASSIGNMENT OPERATOR (*=) ####################
    def state199(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    

    def state200(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state201(input_str)
        elif self.current_char() == "=":
            return self.state202(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR ARITHMETIC OPERATOR (/) ####################
    def state201(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state202(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state203(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR ASSIGNMENT OPERATOR (/=) ####################

    def state203(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state204(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['arithmetic_operator_delim']:
            return self.state205(input_str)
        elif self.current_char() == "=":
            return self.state206(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR ARITHMETIC OPERATOR (%) ####################

    def state205(self, input_str):
        return True, input_str, TokenType.ARITHMETIC_OPERATOR
    
    def state206(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['other_assignment_operator_delim']:
            return self.state207(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR ASSIGNMENT OPERATOR (%=) ####################

    def state207(self, input_str):
        return True, input_str, TokenType.ASSIGNMENT_OPERATOR
    
    def state208(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['not_logical_delim']:
            return self.state209(input_str)
        elif self.current_char() == "=":
            return self.state210(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR NOT LOGIC (!) ####################
    def state209(self, input_str):
        return True, input_str, TokenType.NOT
    
    def state210(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state211(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR REALTIONAL OPERATOR (!=) ####################

    def state211(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state212(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "&":
                return self.state213(input_str)
            case _:
                return False, input_str, None
            
    def state213(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['logical_operator_delim']:
            return self.state214(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR LOGICAL OPERATOR (&&) ####################

    def state214(self, input_str):
        return True, input_str, TokenType.LOGICAL_OPERATOR
    
    def state215(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "|":
                return self.state216(input_str)
            case _:
                return False, input_str, None
            
    def state216(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['logical_operator_delim']:
            return self.state217(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR LOGICAL OPERATOR (||) ####################

    def state217(self, input_str):
        return True, input_str, TokenType.LOGICAL_OPERATOR
    

    def state218(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state219(input_str)
        elif self.current_char() == "=":
            return self.state220(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR RELATIONAL OPERATOR (||) ####################

    def state219(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
            
    def state220(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state221(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR RELATIONAL OPERATOR (>=) ####################
    def state221(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    

    def state222(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state223(input_str)
        elif self.current_char() == "=":
            return self.state224(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR RELATIONAL OPERATOR (<) ####################
    def state223(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
            
    def state224(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['relational_operator_delim']:
            return self.state225(input_str)
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR RELATIONAL OPERATOR (<=) ####################
    def state225(self, input_str):
        return True, input_str, TokenType.RELATIONAL_OPERATOR
    
    def state226(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_parentheses_delim']:
            return self.state227(input_str)
        else:
            return False, input_str, None
            
   #################### FINAL STATE FOR OPEN PARENTHESIS ( ####################
    def state227(self, input_str):
        return True, input_str, TokenType.OPEN_PAREN
    

    def state228(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_parentheses_delim']:
            return self.state229(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR CLOSE PARENTHESIS ) ####################
    def state229(self, input_str):
        return True, input_str, TokenType.CLOSE_PAREN
    
    def state230(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_curly_bracket_delim']:
            return self.state231(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR OPEN CURLY BRACKET { ####################
    def state231(self, input_str):
        return True, input_str, TokenType.OPEN_CURLY
    
    def state232(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_curly_bracket_delim']:
            return self.state233(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR CLOSE CURLY BRACKET } ####################
    def state233(self, input_str):
        return True, input_str, TokenType.CLOSE_CURLY
    

    def state234(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['open_square_bracket_delim']:
            return self.state235(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR OPEN SQUARE BRACKET [ ####################
    def state235(self, input_str):
        return True, input_str, TokenType.OPEN_SQUARE
    
    def state236(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['close_square_bracket_delim']:
            return self.state237(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR CLOSE SQUARE BRACKET ] ####################
    def state237(self, input_str):
        return True, input_str, TokenType.CLOSE_SQUARE
    
    def state238(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['terminator_delim']:
            return self.state239(input_str)
        else:
            return False, input_str, None
            
    #################### FINAL STATE FOR TERMINATOR ~ ####################
    def state239(self, input_str):
        return True, input_str, TokenType.TERMINATOR
    

    def state240(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        if self.current_char() in Delims ['comma_delim']:
            return self.state241(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR COMMA ####################
    def state241(self, input_str):
        return True, input_str, TokenType.COMMA
    
    def state242(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "n":
                return self.state243(input_str)
            case "t":
                return self.state245(input_str)
            case "\\":
                return self.state247(input_str)
            case '"':
                return self.state249(input_str)
            case _:
                return False, input_str, None
    
    def state243(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state244(input_str)
        else:
            return False, input_str, None
            
    #################### FINAL STATE FOR ESCAPE SEQUENCE \n ####################

    def state244(self, input_str):
        return True, input_str, TokenType.ESCAPE_NEWLINE
    
    def state245(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state246(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR ESCAPE SEQUENCE \t #################### 
    def state246(self, input_str):
        return True, input_str, TokenType.ESCAPE_TAB
    
    def state247(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state248(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR ESCAPE SEQUENCE \\ #################### 
    def state248(self, input_str):
        return True, input_str, TokenType.ESCAPE_BACKSLASH
    
    def state249(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['escape_sequence_delim']:
            return self.state250(input_str)
        else:
            return False, input_str, None

            
    #################### FINAL STATE FOR ESCAPE SEQUENCE \" ####################
    def state250(self, input_str):
        return True, input_str, TokenType.ESCAPE_QUOTE
    
    #=====================================================#
    #        STATES => IDENTIFIER, COMMENT                #
    #=====================================================#
    #   STATE 251 - STATE 252 => IDENTIFIER               #
    #   STATE 190 & STATE 253-254 => NEGATIVE TREASURES   #
    #   STATE 255 & STATE 256 => POSITIVE TREASURES       #
    #   STATE 190 & 253 & STATE 257-259 => NEGATIVE OCEAN #
    #   STATE 255 & STATE 260-262 => POSITIVE OCEAN       #
    #   STATE 263 - STATE 265 => SCROLL LITERALS          #
    #   STATE 266 - STATE 269 => CHAR LITERALS            #
    #   STATE 270 - STATE 271 => SINGLE-LINE COMMENT      #
    #   STATE 270 & STATE 272-275 => MULTI-LINE COMMENT   #
    #=====================================================#

    def state251(self, input_str):
        """Initial state for identifiers."""
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['alphanum'] | {'_'} and self.current_char() not in Delims['id_delim']:
            return self.state251(input_str)  # Transition to state247
        elif self.current_char() in Delims['id_delim']:
            return self.state252(input_str)  # Transition to final state
        else:
            return False, input_str, None

    #################### FINAL STATE FOR IDENTIFIER ####################

    def state252(self, input_str):
        return True, input_str, TokenType.IDENTIFIER


    
    def state253(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['number']  and self.current_char() not in ["."]:
            return self.state253(input_str) 
        elif self.current_char() in Delims['number_delim']:
            return self.state254(input_str) 
        elif self.current_char() == ".":
            return self.state257(input_str)  
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR NEGATIVE TREASURES LITERALS ####################

    def state254(self, input_str):
        normalized = self.normalize_integer(input_str)
        return True, normalized, TokenType.NEG_TREASURES_INT
    
    def state255(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in RegDef['number']  and self.current_char() not in ["."]:
            return self.state255(input_str) 
        elif self.current_char() in Delims['number_delim']:
            return self.state256(input_str) 
        elif self.current_char() == ".":
            return self.state257(input_str)  
        else:
            return False, input_str, None

    #################### FINAL STATE FOR POSITIVE TREASURES LITERALS ####################

    def state256(self, input_str):
        normalized = self.normalize_integer(input_str)
        return True, normalized, TokenType.POS_TREASURES_INT

    def state257(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() in RegDef['number']:
            return self.state258(input_str) 
        else:
            return False, input_str, None
    

    def state258(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() in RegDef['number']:
            return self.state258(input_str) 
        elif self.current_char() in Delims['number_delim']:
            return self.state259(input_str)
        else:
            return False, input_str, None

    #################### FINAL STATE FOR NEGATIVE OCEAN LITERALS ####################
    
    def state259(self, input_str):
        normalized = self.normalize_float(input_str)
        return True, normalized, TokenType.NEG_FLOAT_LITERAL
    

    def state260(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() in RegDef['number']:
            return self.state261(input_str) 
        else:
            return False, input_str, None
    

    def state261(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() in RegDef['number']:
            return self.state258(input_str) 
        elif self.current_char() in Delims['number_delim']:
            return self.state262(input_str)
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR POSITIVE OCEAN LITERALS ####################
    
    def state262(self, input_str):
        normalized = self.normalize_float(input_str)
        return True, normalized, TokenType.POS_FLOAT_LITERAL
    

    def state263(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() not in ['"', '\n'] and (self.current_char() in RegDef['ascii'] or self.current_char() in RegDef['escape_seq'] or self.current_char() in ['\t', ' ']):
            return self.state263(input_str)   
        elif self.current_char() == '"':
            return self.state264(input_str) 
        else:
            return False, input_str, None

    def state264(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['book_delim']:
            return self.state265(input_str)   
        else:
            return False, input_str, None
        

    #################### FINAL STATE FOR SCROLL LITERALS ####################
        
    def state265(self, input_str):
        return True, input_str, TokenType.STRING_LITERAL

    def state266(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if  self.current_char() not in ["'"] and self.current_char() in RegDef['ascii'] or self.current_char() == ' ':
            return self.state267(input_str)  
        elif self.current_char() == "'":
            return self.state268(input_str)  
        else:
            return False, input_str, None

    def state267(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()
 
        if self.current_char() == "'":
            return self.state268(input_str) 
        else:
            return False, input_str, None

    def state268(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims ['book_delim']:
            return self.state269(input_str)   
        else:
            return False, input_str, None
        
    #################### FINAL STATE FOR rose LITERALS ####################
        
    def state269(self, input_str):
        return True, input_str, TokenType.CHAR_LITERAL
    
    #COMMENT
    def state270(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() not in ['\n', '*'] and self.current_char() in RegDef['ascii'] or self.current_char() in [' ', '\t']:
            return self.state270(input_str)   
        elif self.current_char() == '\n':
            return self.state271(input_str)  
        elif self.current_char() == '*':
            return self.state272(input_str) 
        else:
            return False, input_str, None
    
    #################### FINAL STATE FOR SINGLE-LINE COMMENTS ####################

    def state271(self, input_str):
        return True, input_str, TokenType.SINGLE_COMMENT
    
    def state272(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() != '*' and self.current_char() in RegDef['ascii'] or self.current_char() in ['\t', ' ', '\n']:
            return self.state272(input_str) 
        elif self.current_char() == '*':
            return self.state273(input_str) 
        else:
            return False, input_str, None
        
    def state273(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() == '?':
            return self.state274(input_str) 
        else:
            return False, input_str, None
        
    def state274(self, input_str):
        input_str += self.current_char()  # Append the current character
        self.advance()

        if self.current_char() in Delims['multi-comment_delim']:
            return self.state275(input_str) 
        else:
            return False, input_str, None 
        
    
    #################### FINAL STATE FOR MULTI-LINE COMMENTS ####################
        
    def state275(self, input_str):
        return True, input_str, TokenType.MULTI_COMMENT

    

    def normalize_integer(self, input_str):
        """
        Removes leading zeros from an integer literal.
        If the number is negative, removes zeros after the '-'.
        Ensures that '0' and '-0' are preserved.

        Args:
            input_str (str): The integer literal as a string.

        Returns:
            str: The normalized integer literal.
        """
        if not input_str:
            return '0'  # Default to '0' if input is empty

        # Check if the number is negative
        if input_str[0] == '-':
            # Remove leading zeros after the '-'
            normalized = '-' + input_str[1:].lstrip('0')
            # If all characters were zeros, return '-0'
            return normalized if normalized != '-' else '-0'
        else:
            # Remove leading zeros
            normalized = input_str.lstrip('0')
            # If all characters were zeros, return '0'
            return normalized if normalized else '0'
        
    def normalize_float(self, input_str):
        """
        Normalizes a float literal by:
        - Removing leading zeros from the integer part (after '-' if negative).
        - Removing trailing zeros from the fractional part only after non-zero digits.
        - Preserving the fractional part if it consists solely of zeros.
        - Limiting the fractional part to a maximum of 15 decimal places, rounding if necessary.
        - Ensuring that if the fractional part is empty after the decimal point, an error is raised.
        - Preserving '0' and '-0' appropriately.

        Args:
            input_str (str): The float literal as a string.

        Returns:
            str: The normalized float literal.

        Raises:
            ValueError: If the input format is invalid or fractional part is missing.
        """
        if not input_str:
            raise ValueError("Empty input for float normalization.")

        # Check if the number is negative
        is_negative = False
        if input_str[0] == '-':
            is_negative = True
            input_str = input_str[1:]  # Remove '-' for processing

        if '.' in input_str:
            integer_part, fractional_part = input_str.split('.', 1)

            # **Error Check:** Ensure that there is at least one digit after the decimal point
            if not fractional_part:
                raise ValueError("Invalid float format: fractional part is missing after decimal point.")

            # Normalize integer part by removing leading zeros
            normalized_integer = integer_part.lstrip('0') or '0'

            if all(c == '0' for c in fractional_part):
                # Fractional part consists solely of zeros; preserve it
                normalized_fractional = fractional_part
                normalized = f"{normalized_integer}.{normalized_fractional}"
            else:
                # Remove trailing zeros after the last non-zero digit
                normalized_fractional = fractional_part.rstrip('0')

                # **Error Check:** After stripping, ensure there's at least one digit in the fractional part
                if not normalized_fractional:
                    raise ValueError("Invalid float format: fractional part has only zeros.")

                # Limit to 15 decimal places, rounding if necessary
                if len(normalized_fractional) > 15:
                    # Use Decimal for accurate rounding
                    number = Decimal(f"{normalized_integer}.{normalized_fractional}")
                    # Define the quantize pattern for 15 decimal places
                    quantize_pattern = Decimal('1.' + '0' * 15)
                    # Round the number to 15 decimal places
                    number = number.quantize(quantize_pattern, rounding=ROUND_HALF_UP)
                    normalized = format(number, 'f')  # Convert back to string without scientific notation
                else:
                    normalized = f"{normalized_integer}.{normalized_fractional}"

            # Reapply the negative sign if necessary
            if is_negative:
                normalized = '-' + normalized

            return normalized
        else:
            # No decimal point; treat as integer
            normalized_integer = self.normalize_integer(input_str)
            if is_negative:
                normalized_integer = '-' + normalized_integer
            return normalized_integer




    
# Create the GUI with Tkinter
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
                # elif token.token_type in [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL]:
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
