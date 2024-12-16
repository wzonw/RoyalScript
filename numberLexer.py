import tkinter as tk
from tkinter import scrolledtext
import re
import RS_regdef as regdef
from RS_regdef import Delims


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
    GRANTED = "INPUT"  # Output
    CAST = "IF"  # If statement
    TWIST = "ELSEIF"  # Else if statement
    CURSE = "ELSE"  # Else statement
    TOROSE = "CONVERSION FUNC"
    TOSCROLL = "CONVERSION FUNC"
    TOOCEAN = "CONVERSION FUNC"
    TOTREASURES = "CONVERSION FUNC"  
    ESCAPE = "ESCAPE"

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
    OPEN_PAREN = "OPEN_PAREN"
    CLOSE_PAREN = "CLOSE_PAREN"
    OPEN_BRACKET = "OPEN_BRACKET"
    CLOSE_BRACKET = "CLOSE_BRACKET"
    TERMINATOR = "TERMINATOR"
    OPEN_CURLY = "OPEN_CURLY"
    CLOSE_CURLY = "CLOSE_CURLY"

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

    #DELIMS haha
    DELIMS = {
    'return': {'0', ' '},
    'data_type': {' ', '~'},
    'dynasty': {' '},
    'mirror': {'|', '&', ']', ',', ' ', '}', ')', '~', '\n'},
    'conditional': {'(', ' '},
    'io': {'(', ' '},
    'castle': {' '},
    'int_float': {',', ' ',('general_operator'), ')', '~', '!', r'&', '|', '>', '<', '='},
    'string': {' ', ')', ',', '&', '}', '~', '!', '='},
    'assign_delim': {('alpha'), ('number'), '{', ' ', '-', '(', '"'},
    'operator_delim': {('alpha'), ('number'), ' ', '-', '(', '{'},
    'logical_delim': {'"', ('alpha'), ('number'), ' ', '-', '(', '{'},
    'string_parts': {'"', ('alpha'), ('number'), ' ', '-', '(', '|', '&'},
    'open_brace': {'{', '}', '(', ('number'), ' ', '"', ('alpha'), '\n', '>', '-'},
    'close_brace': {'{', '}', '.', '~', ' ', ',', ')', '\n', '>', '&', ('general_operator'), '!', '|'},
    'open_parenthesis': {'{', ('number'), ('alpha'), ' ', '-', '\n', '>', '(', ')', '"'},
    'id': {'{', '\n', ' ', '~', ',', '(', ')', '(', ']', '}', ('general_operator'), '!', r'&', '|', '.'},
    'close_parenthesis': {'{', ' ', ('general_operator'), '!', '&', '|', '\n', '~', '>', '.', ',', ')', '(', '(', ']', '}'},
    'open_bracket': {']', ('number'), '-', ('alpha'), '(', ' ', '\n'},
    'double_open_bracket': {' ', '\n', ('alpha'), '>'},
    'close_bracket': {'\n', '(', ' ', '~', ',', ')', '(', ']', '}', ('general_operator'), '!', r'&', '|', '.', '\n'},
    'double_close_bracket': {']',' ', '\n', ('alpha'), '>'},
    'unary': {'|', '~', ')', ('general_operator'), '!', ' ', '\n'},
    'concat': {' ', '"', ('alpha'), ('number'), '(', '{', '\n'},
    'line': {'\n', ' ', ('alpha'), ']'},
    'comma': {('alpha'), ' ', ('number'), '"', '-', '\n', '>', '{'},
    'dot_op': {('alpha'), '[', '(', '\n'},
    'nuww': {' ', '~', ')', '}', ',', '=', '\n', '!', '|', '&'},
    'whitespace': {' ', '\n'},
    'single_line_comment': {'\n'},
    'all': {None}
    }

class RoyalScriptLexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

        # Define all reserved words in RoyalScript dynamically from input
        # self.RESERVED_KEYWORDS = {
        #     'crown': TokenType.CROWN,
        #     'reign': TokenType.REIGN,
        #     'spell': TokenType.SPELL,
        #     'castle': TokenType.CASTLE,
        #     'wish': TokenType.WISH,
        #     'granted': TokenType.GRANTED,
        #     'cast': TokenType.CAST,
        #     'twist': TokenType.TWIST,
        #     'curse': TokenType.CURSE,
        #     'treasures': TokenType.TREASURES,
        #     'ocean': TokenType.OCEAN,
        #     'scroll': TokenType.SCROLL,
        #     'rose': TokenType.ROSE,
        #     'mirror': TokenType.MIRROR,
        #     'chamber': TokenType.CHAMBER,
        #     'dynasty': TokenType.DYNASTY
        # }

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

    def peek_reserved(self, word, token_type):
        """Check if the next part of the code matches a reserved word"""
        match = self.match(r'\b' + re.escape(word) + r'\b')
        if match:
            token = Token(match, token_type, self.position)
            self.tokens.append(token)
            self.position += len(match)
            return True
        return False
    
    def peek_escape_sequence(self):
        """Check if the next part of the code matches an escape sequence and return the corresponding token."""
        
        # Match the escape sequences
        if self.match(r'\\n'):  # Match \n escape sequence
            token = Token(r'\n', TokenType.ESCAPE_NEWLINE, self.position)
            self.tokens.append(token)
            self.position += 2  # Move the position forward by the length of the escape sequence
            return True

        elif self.match(r'\\t'):  # Match \t escape sequence
            token = Token(r'\t', TokenType.ESCAPE_TAB, self.position)
            self.tokens.append(token)
            self.position += 2  # Move position forward
            return True

        elif self.match(r'\\\\'):  # Match \\ escape sequence
            token = Token(r'\\', TokenType.ESCAPE_BACKSLASH, self.position)
            self.tokens.append(token)
            self.position += 2  # Move position forward
            return True

        elif self.match(r'\\"'):  # Match \" escape sequence
            token = Token(r'\"', TokenType.ESCAPE_QUOTE, self.position)
            self.tokens.append(token)
            self.position += 2  # Move position forward
            return True

        return False

    def peek_symbol(self, symbol, token_type):
        # If the symbol is more than one character long, check if the next characters match
        if len(symbol) > 1:
            # Match the multi-character symbol
            if self.match(symbol):
                token = Token(symbol, token_type, self.position)
                self.tokens.append(token)
                self.position += len(symbol)  # Move the position forward by the length of the symbol
                return True
        else:
            # Handle single-character symbols
            if self.match(symbol):  # Match the single character symbol
                token = Token(symbol, token_type, self.position)
                self.tokens.append(token)
                self.position += 1  # Move the position forward by 1 (since it's a single character)
                return True
        return False

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

            # Handle terminator (~)
            if char == '~':
                if char in TokenType.DELIMS:  # Check if it's a delimiter
                    token = Token(char, TokenType.DELIMS, self.position)
                    self.tokens.append(token)
                else:
                    token = Token(char, TokenType.TERMINATOR, self.position)
                    self.tokens.append(token)
                self.advance()
                continue

            if char in ['\n', ' ', '\t']:
                match = self.match(r'\s+')
                if match and self.position < len(self.code) - 1:  # Avoid trailing whitespace
                    token = Token(match, TokenType.WHITESPACE, self.position)
                    self.tokens.append(token)
                self.advance()  # Move to the next character
                continue

            if char == 'b':
                # pos_start = self.position.copy()
                valid, input_str = self.state1()
                if valid:
                    self.tokens.append(Token(input_str, TokenType.BELIEVE, self.position - len(input_str)))
                else:
                    while self.current_char() is not None and self.current_char() not in TokenType.DELIMS['conditional']:
                        char = self.current_char()  # Update char after advancing
                        input_str += char
                        self.advance()

                    raise SyntaxError(
                        f"Expected delimiter '~' or ' ' after 'believe' at position {self.position}"
                    )


        return self.tokens

    def match_literal(self, token_type):
        """Match literals like INT, FLOAT, CHAR, STRING"""
        if token_type == TokenType.FLOAT_LITERAL:
            # Match floats like 3.14, .5, or 10.
            match = self.match(r'\b\d*\.\d+\b|\b\d+\.\b')
            if match:
                token = Token(match, token_type, self.position)
                self.tokens.append(token)
                self.position += len(match)
                return True
        elif token_type == TokenType.INT_LITERAL:
            # Match integers without a dot
            match = self.match(r'\b\d+\b(?!\.)')
            if match:
                token = Token(match, token_type, self.position)
                self.tokens.append(token)
                self.position += len(match)
                return True

        elif token_type == TokenType.CHAR_LITERAL:
            # Match char literals like 'a', '1', '$' (single characters inside single quotes)
            match = self.match(r"'([^'\\])'")
            if match:
                token = Token(match, token_type, self.position)
                self.tokens.append(token)
                self.position += len(match)
                return True
            else:
                # If the match fails, raise an error and display in the error box
                raise SyntaxError(f"Invalid char literal at position {self.position}")

        elif token_type == TokenType.STRING_LITERAL:
            # Match string literals enclosed in double quotes
            match = self.match(r'"([^"\\\n]*(\\.[^"\\\n]*)*)"')
            if match:
                token = Token(match, token_type, self.position)
                self.tokens.append(token)
                self.position += len(match)
                return True


    def match_unary_operator(self):
        """Match post-unary operators (++ and --)"""
        match = self.match(r'\+\+|\-\-')
        if match:
            # Ensure it's treated as post-unary by checking previous token
            if self.tokens and self.tokens[-1].token_type in {TokenType.IDENTIFIER, TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL}:
                token = Token(match, TokenType.UNARY_OPERATOR, self.position)
                self.tokens.append(token)
                self.position += len(match)
                return True
        return False
    
    def match_logical_operator(self):
        # Adjusted regex pattern for logical operators (&&, ||, !)
        match = self.match(r'\&&|\|\||\!(?=([A-Z]|[A-Z][a-zA-Z0-9_]))')
        if match:
            token = Token(match, TokenType.LOGICAL_OPERATOR, self.position)
            self.tokens.append(token)
            self.position += len(match)


    def match_identifier(self):
        """Match identifiers"""
        match = self.match(r'\b[A-Z_][a-zA-Z0-9_]*\b') #Hndi na ccatch if lowercase, insert warning unidentified word
        if match:
            token = Token(match, TokenType.IDENTIFIER, self.position)
            self.tokens.append(token)
            self.position += len(match)

    def match_operator(self):
        """Match operators (<, >, <=,>=,==,!=)"""
        match = self.match(r'\<=|\>=|\==|\!=|<|>')
        if match:
            token = Token(match, TokenType.RELATIONAL_OPERATOR, self.position)
            self.tokens.append(token)
            self.position += len(match)
            
        """Match operators (=,+=, -=, *=, /=, %=)"""
        match = self.match(r'\+=|-=|\*=|/=|%=|=')
        if match:
            token = Token(match, TokenType.ASSIGNMENT_OPERATOR, self.position)
            self.tokens.append(token)
            self.position += len(match)

    def match_Arith_operator(self):
        """Match operators (+, -, *, /, %)"""
        match = self.match(r'[\+|\-|\*|/|%|]')
        if match:
            token = Token(match, TokenType.ARITHMETIC_OPERATOR, self.position)
            self.tokens.append(token)
            self.position += len(match)

    def match_comment(self):
        # Single-line comment matching 
        match = self.match(r'\?(?!\*)[^\n*]*\*?[^\n]*(?=\n)')
        if match:
            token = Token(match, TokenType.SINGLE_COMMENT, self.position)
            self.tokens.append(token)
            self.position += len(match)
            return True

        # Multi-line comment matching (starts with '?*', ends with '*?')
        match = self.match(r'\?\*[\s\S]*?\*\?')
        if match:
            token = Token(match, TokenType.MULTI_COMMENT, self.position)
            self.tokens.append(token)
            self.position += len(match)
            return True
        return False

    def match_symbol(self):
        """Match Terminator"""
        match = self.match(r'[~]')
        if match:
            token = Token(match, TokenType.TERMINATOR, self.position)
            self.tokens.append(token)
            self.position += len(match)


    def state1(self):
        input_str = ""
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state2(input_str)
            # case "r":
            #     return self.state9(input_str)
            case _:
                return False, input_str
                    
    def state2(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "l":
                return self.state3(input_str)
            case _:
                return False, input_str

    def state3(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "i":
                return self.state4(input_str)
            case _:
                return False, input_str 
                    
    def state4(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state5(input_str)
            case _:
                return False, input_str
                    
    def state5(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "v":
                return self.state6(input_str)
            case _:
                return False, input_str
            
    def state6(self, input_str):
        input_str += self.current_char()
        self.advance()

        match self.current_char():
            case "e":
                return self.state7(input_str)
            case _:
                return False, input_str
                    
    def state7(self, input_str):
        input_str += self.current_char()
        self.advance()

        if self.current_char() in TokenType.DELIMS['conditional']:
            return self.state8(input_str)
        else:
            return False, input_str

    #Final State Believe
    def state8(self, input_str):
        return True, input_str



# Create the GUI with Tkinter
class RoyalScriptLexerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("RoyalScript Lexer")
        self.geometry("910x650")

        # Create frames for each section
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.middle_frame = tk.Frame(self)
        self.middle_frame.grid(row=0, column=1, padx=0, pady=5, sticky="nsew")

        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=2, padx=0, pady=5, sticky="nsew")

        # Errors and Program Frame (combined)
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Program Frame: Below the errors frame
        self.program_frame = tk.Frame(self)
        self.program_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Left: Input code with title (larger box)
        self.input_label = tk.Label(self.left_frame, text="Input Code")
        self.input_label.grid(row=0, column=0)
        self.input_text = scrolledtext.ScrolledText(self.left_frame, width=60, height=20, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, padx=0, pady=5)

        # Middle: Lexer output with title (same width as the token box)
        self.output_label = tk.Label(self.middle_frame, text="Lexer")
        self.output_label.grid(row=0, column=0)
        self.output_listbox = tk.Listbox(self.middle_frame, width=30, height=20, justify="center")
        self.output_listbox.grid(row=1, column=0, padx=0, pady=5)

        # Right: Tokens with title (same width as lexer output)
        self.tokens_label = tk.Label(self.right_frame, text="Tokens")
        self.tokens_label.grid(row=0, column=0)
        self.token_listbox = tk.Listbox(self.right_frame, width=30, height=20, justify="center")
        self.token_listbox.grid(row=1, column=0, padx=0, pady=5)

        # Errors Box (left side of the combined frame)
        self.errors_label = tk.Label(self.bottom_frame, text="Errors")
        self.errors_label.grid(row=0, column=0, padx=5)
        self.errors_listbox = tk.Listbox(self.bottom_frame, width=80, height=10, fg="red")
        self.errors_listbox.grid(row=1, column=0, padx=5, pady=5)

        # Program Status Box (right side of the combined frame)
        self.program_label = tk.Label(self.bottom_frame, text="Program Status")
        self.program_label.grid(row=0, column=1, padx=5)
        self.program_listbox = tk.Listbox(self.bottom_frame, width=65, height=10)
        self.program_listbox.grid(row=1, column=1, padx=0, pady=0)

        # Button to trigger lexer analysis
        self.analyze_button = tk.Button(self, text="Analyze Code", command=self.analyze_code)
        self.analyze_button.grid(row=3, column=0, columnspan=3, pady=0)

    def analyze_code(self):
        code = self.input_text.get("1.0", tk.END)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.errors_listbox.delete(0, tk.END)

        try:
            tokens = lexer.get_tokens()
            
            # Show only the words in the output text
            for token in tokens:
                self.output_listbox.insert(tk.END, f"{token.value}\n")  # Just the word (lexeme), centered

                # Handle definition lookup
                if token.token_type in TokenType.__dict__.values():
                    definition = token.token_type.replace("_", "")
                    self.token_listbox.insert(tk.END, f"{definition}")

                


        except SyntaxError as e:
            # Display error messages in the Errors Box
            self.errors_listbox.insert(tk.END, f"{str(e)}\n")
        except Exception as e:
            # Handle any unexpected errors
            self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}\n")


if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()