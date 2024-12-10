import tkinter as tk
from tkinter import scrolledtext
import re


# Token class to represent individual tokens
class Token:
    def __init__(self, value, token_type, position):
        self.value = value
        self.token_type = token_type
        self.position = position


# Define token types for RoyalScript (no fixed values like CAST = "CAST")
class TokenType:
    LITERALS = ["INT_LITERAL", "FLOAT_LITERAL", "STRING_LITERAL", "CHAR_LITERAL", "BOOL_LITERAL", "NULL_LITERAL"]
    OPERATORS = ["ASSIGNMENT_OPERATOR", "ARITHMETIC_OPERATOR", "RELATIONAL_OPERATOR", "LOGICAL_OPERATOR", "UNARY_OPERATOR"]
    SYMBOLS = ["COMMA", "DOT", "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACE", "CLOSE_BRACE", "OPEN_BRACKET", "CLOSE_BRACKET", "TERMINATOR"]
    OTHERS = ["IDENTIFIER", "WHITESPACE", "SINGLE_COMMENT", "MULTI_COMMENT"]

    # Custom token types
    CROWN = "RESERVE WORD"
    CURSE = "CONDITIONAL"
    CAST = "CONDITIONAL"
    CASTLE = "MAIN FUNC"
    CHAMBER = "VOID"
    BELIEVE = "DO"
    CONTINUE = "CONTINUE"


class RoyalScriptLexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def peek_reserved(self, word):
        """Check if the next part of the code matches a reserved word and dynamically assign the token type."""
        match = self.match(r'\b' + re.escape(word) + r'\b')
        
        if match:
            # Dynamically determine the token type when needed (no predefined mappings)
            token_type = self.get_token_type(word.lower())
            
            if token_type:
                token = Token(match, token_type, self.position)
                self.tokens.append(token)
                self.position += len(match)
                
                # Output the token type dynamically (e.g., 'CAST', 'CASTLE')
                print(f"Matched token: {token_type}")  # Print token type
                return True
        
        return False

    def get_token_type(self, keyword):
        """Dynamically assign a token type when needed based on the keyword."""
        if keyword == "cast":
            return TokenType.CAST
        elif keyword == "castle":
            return TokenType.CASTLE
        elif keyword == "chamber":
            return TokenType.CHAMBER
        elif keyword == "crown":
            return TokenType.CROWN
        elif keyword == "continue":
            return TokenType.CONTINUE
        elif keyword == "curse":
            return TokenType.CURSE
        elif keyword == "believe":
            return TokenType.BELIEVE
        # Add more dynamic assignments as needed
        return None  # Return None if no match is found

    def get_tokens(self):
        """Tokenize the entire input code."""
        while self.position < len(self.code):
            char = self.current_char()

            # Skip whitespace and continue to next character
            if char in ['\n', ' ', '\t']:
                match = self.match(r'\s+')
                if match:
                    token = Token(match, TokenType.OTHERS[1], self.position)  # WHITESPACE
                    self.tokens.append(token)
                    self.position += len(match)
                continue

            # Match reserved words starting with 'c'
            if char == 'c':
                if self.peek_reserved('cast'):
                    continue
                elif self.peek_reserved('castle'):
                    continue
                elif self.peek_reserved('chamber'):
                    continue
                elif self.peek_reserved('crown'):
                    continue
                elif self.peek_reserved('continue'):
                    continue
                elif self.peek_reserved('curse'):
                    continue

            # Match reserved words starting with 'b'
            if char == 'b':
                if self.peek_reserved('believe'):
                    continue

            raise SyntaxError(f"Unexpected character: {char} at position {self.position}")

        return self.tokens

    def match(self, pattern):
        """Helper function to match patterns in the code."""
        match = re.match(pattern, self.code[self.position:])
        if match:
            return match.group(0)
        return None

    def current_char(self):
        """Helper function to get the current character in the code."""
        return self.code[self.position] if self.position < len(self.code) else None


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

                if token.token_type in TokenType.OTHERS:
                    self.token_listbox.insert(tk.END, f"{token.token_type.capitalize()}")

        except SyntaxError as e:
            # Display error messages in the Errors Box
            self.errors_listbox.insert(tk.END, f"{str(e)}")


# Running the GUI
if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()
