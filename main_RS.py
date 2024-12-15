import tkinter as tk
from tkinter import scrolledtext
import re
import RS_regdef

#Lagay tayo sound kahit magical intro lang

#Regular Definitions
#Number
zero = '0'
num = '123456789'
number = zero + num
period = '.'

#Alphabet Letters
alpha_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
less_equal = '<='
greater_equal = '>='
relational_op = not_equal + dual_equal + greater_than +less_than + less_equal + greater_equal

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
escape_seq = newline + tab + backslash
double_quote = '"'

#Others
terminator = '~'
true = 'true'
false = 'false'
space = 'space'
dynasty = 'const' #Unsure, no constant data-type for python
phantom = 'NULL' #double check
chamber = 'void' #Same with dynasty
# return = return hawhahwhawh delete i guess\\
spell = 'declaration' #Same with dynasty
concatenat = '+'

#Literals
#scroll_lit = ''

escape_delim = alphanum + escape_seq + '"'
control_flow = space + escape_seq

#Symbols Delim
arithmetic_op_delim = alphanum + '(' + ')' #Double check with the ()
plus_delim = alphanum + '(' + '"'
logical_op_delim = alphanum + '('
not_op_delim = alphanum + "'" + '"' + '('
witch_delim = '{'
assign_op_delim = '(' + alphanum
equal_delim = alphanum + '"' + "'" + '[' + '('
unary_op_delim = alphanum + '~' +  ')'
relational_op_delim = '(' + "'" + '"' + alphanum
open_par_delim = unary_op + alphanum
close_par_delim = arithmetic_op + logical_op + relational_op + '(' + '{' + '~'
open_curl_delim = '(' + unary_op + alphanum + newline
close_curl_delim = alpha_lower
open_square_delim = '"' + '"' + ']' + alphanum
close_square_delim = '~' +'[' + '='
comma_delim = alphanum + '-' + '"' + "'"

id_delim = '(' + ')' + '~' + arithmetic_op + assignment_op + relational_op + unary_op

#Literals Delim
book_delim = '~' +  ')' + '+'
number_delim = ')' + '}' + ']' + '~' + unary_op + relational_op + logical_op + assignment_op + arithmetic_op

#Other Delimiter
genie_delim = '('
gate_delim = '~'

#Comments Delim
single_delim = newline
# multi_delim = 

#RESERVE WORDS
BELIEVE = 'believe'

#Error definition
class Error:
    def __init__ (self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln +1}'
        return result
    
    class IllegalChar_Error():
        def __init__ (self, pos_start, pos_end, details):
            super().__init__(pos_start, pos_end, 'Illegal Character', details)
    
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln =ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance (self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln+=1
            self.col = 0

        return self
class Token:
    def __init__ (self, token, value=None):
        self.token = token
        self.value = value
    def _repar_(self):
        if self.value: return f'{self.value}: {self.token}'
        return f'{self.token}'


class RoyalScriptLexer:
    def __init__(self, text, fn):
        self. text = text
        self.fn = fn
        self.pos = Position (-1,0,-1,fn,text)
        self.current_char = self.text[self.pos.idx] if len(self.text) > 0 else None  # Initialize current_char

    def peek (self):
        next_idx = self.post.idx + 1
        return self.text[next_idx] if next_idx < len(self.text) else None
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx <= len(self.text)-1 else None
    def make_tokens(self):
        tokens = []
        errors = []
        string = ""
        

        while self.current_char is not None:
            """ if self.current_char in special_chars:
                errors.extend([f"Invalid symbol: {self.current_char}"])
                self.advance() """
            if self.current_char in '\t':
                tokens.append(Token(NEWTAB, "\\t"))
                self.advance()
            elif self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n"))
                self.advance()
            elif self.current_char  == '>':
                tokens.append(Token(greater_than, ">"))
                self.advance()
            elif self.current_char  == '<':
                tokens.append(Token(less_than, "<"))
                self.advance()
            elif self.current_char.isspace():
                # Handle spaces explicitly
                while self.current_char is not None and self.current_char.isspace():
                    if self.current_char == " ":
                        tokens.append(Token(SPACE, "\" \""))
                    self.advance()
            elif self.current_char in alpha:
                result, error = self.make_word()
                
                if error:
                    errors.extend(error)  
                tokens.append(result)
            else:
                errors.append(f"Illegal character '{self.current_char}' at position {self.pos.idx}")
                self.advance()

        return tokens, errors

    def make_word(self):
        ident = ""
        ident_count = 0
        errors = []

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            ident += self.current_char
            self.advance()

            if self.current_char == "b": 
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "e":
                    ident += self.current_char
                    elf.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "v":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "e":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1

                                        if self.current_char == None:
                                            errors.extend([f'Invalid delimiter for belive! Cause: {self.current_char}. Expected: ('])
                                            return [], errors
                                        if self.current_char in '(':
                                            return Token(BELIEVE, "believe"), errors
                                        elif self.current_char in alpha_num: #double check this
                                            continue
                                        else:
                                            errors.extend([f'Invalid delimiter for add! Cause: {self.current_char}. Expected: ('])
                                            return [], errors
            if ident:
                result, error = self.make_ident(ident)
                if error:
                    errors.append(error)
                    return [], errors
                elif result:
                    return Token(IDENTIFIER, result), errors

    def make_ident(self, ident):
        """
        Validates whether the given word is a valid identifier or reserved word.
        """
        errors = []

        # Ensure the first letter is uppercase
        if not ident[0].isupper():
            return None, f"Invalid identifier start: '{ident[0]}'. Cause: '{ident}'. Identifier must start with an uppercase letter."

        # Ensure no invalid characters are present

        return ident, None


            




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
        code = self.input_text.get("1.0", tk.END).strip()
        lexer = RoyalScriptLexer("<input>",code)

        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.errors_listbox.delete(0, tk.END)


        tokens, errors = lexer.make_tokens()
            
        row_number = 1    # Show only the words in the output text
        for token in tokens:
            
           if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                    # Check for spaces as errors
                if token.token == "SPACE":
                    self.error_output.insert(tk.END, f"Error: Unexpected whitespace at line {row_number}\n")
                    # Check for newlines as tokens
                elif token.token == "NEWLINE":
                    lexeme = "\\n"  # Display as "\n" in the table for clarity
                self.token_listbox.insert(tk.END, f"{token.token}")
                self.output_listbox.insert(tk.END, f"{code}")

                row_number += 1

        if errors:
            self.errors_listbox.insert(tk.END, "\n".join(errors) + "\n")
        else:
            self.errors_listbox.insert(tk.END, "No errors found.\n")

        
    def clear_input(self):
        """Clear the code input box"""
        self.code_input.delete("1.0", tk.END)

    def undo_input(self):
        """Undo the last action in the code input box"""
        current_text = self.code_input.get("1.0", tk.END)
        if len(current_text) > 1:  # Check if there's any text to undo
            self.code_input.delete("1.0", tk.END)
            self.code_input.insert("1.0", current_text[:-2])

if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()