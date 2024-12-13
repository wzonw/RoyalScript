import tkinter as tk
from tkinter import scrolledtext
import re


#Lagay tayo sound kahit magical intro lang

#Regular Definitions
#Number
zero = '0'
num = '123456789'
number = zero + num
period = '.'

#Alphabet Letters
alpa_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
alpha = alpha_capital + alpha_lower

#AlphaNum
alphanum = alpha + number
special_char = "!@#$%^&*()-_=+[]{}\\|:;'”,<>./?"
ascii_type = alphanum + special_char

#Operators
arithmetic_op = '+-*/%'

equal = '='
plus_equal = '+='
minus_equal = '-='
mult_equal = '*='
div_equal = '/='
mod_equal = '%='
assignment_op = equal + plus_equal + minus_equal + mult_equal + div_equal + mod_equal

and_op = '&&'
not_op = '!'
or_op = '||'
logical_op = and_op + not_op + or_op

not_equal =  '!='
dual_equal = '=='
greater_than = '>'
less_than = '<'
less_euqal = '<='
greater_equal '>='
relational_op = not_equal + dual_equal + greater_than +less_than + less_eual + greater_equal

increment = '++'
decrement = '--'
unary_op = increment + decrement

single_line = '?'
multiline_open = '?*'
multiline_close = '*?' # I saw sa iba they seperated them but let's see kung mag eerror HWHAWHA

#Escape Sequence

newline = '\\n'
tab = '\\t'
backslash = '\\\\'
double_quote = '"'

#Others
terminator = '~'
true = 'true'
false = 'false'
space = 'space'
dynasty = 'const' #Unsure, no constant data-type for python
phantom = NULL #double check
chamber = 'void' #Same with dynasty
# return = return hawhahwhawh delete i guess\\
spell = 'declaration' #Same with dynasty
concatenat = '+'






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

                if token.token_type in TokenType.__dict__.values():
                    definition = token.token_type.replace("_", " ")
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