import tkinter as tk
from tkinter import PhotoImage, scrolledtext
from PIL import Image, ImageTk 
from lexer2 import RoyalScriptLexer
from lexer2 import Token
from pygame import mixer
from syntax4 import RoyalScriptParser


class RoyalScriptLexerGUI(tk.Tk):
    
    mixer.init()
    def __init__(self):
        super().__init__()
        self.tokens = [] 

        def intro_music():
            mixer.music.load("fairytale_intro.mp3")
            mixer.music.play(-1) 
        intro_music()
            
        self.title("RoyalScript")
        self.iconphoto(False, PhotoImage(file="crown_logo2.png")) 
        self.geometry("1050x700")
        self.resizable(False, False)

        # Load and set background image
        self.bg_image = Image.open("4.png")
        self.bg_image = self.bg_image.resize((1050, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = tk.Label(self, image=self.bg_photo, )
        self.bg_label.place(relwidth=1, relheight=1)

        # Setup GUI components
        self.setup_frames()
        self.setup_input_section()
        self.setup_lexer_tokens_section()
        self.setup_errors_section()
        self.setup_analyze_button()

    def setup_frames(self):

        # Main frames with consistent padding
        self.left_frame = tk.Frame(self, bg="#f99dbc")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Combined frame for Lexer and Tokens
        self.lr_frame = tk.Frame(self, bg="#f99dbc")
        self.lr_frame.grid(row=0, column=1, columnspan=2, padx=(0, 20), pady=20, sticky="nsew")

        # Errors frame
        self.bottom_frame = tk.Frame(self, bg="#f99dbc")
        self.bottom_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=5, sticky="nsew")

        # Program frame
        self.program_frame = tk.Frame(self, bg="#f99dbc")
        self.program_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def setup_input_section(self):
        # Input Code label
        self.input_label = tk.Label(
            self.left_frame, text="Input Code", fg="white",
            font=("Arial", 14, "bold"), bg="#f99dbc"
        )
        self.input_label.grid(row=0, column=0, columnspan=3)

        # Line numbers
        self.line_numbers = tk.Text(
            self.left_frame, width=4, height=20, wrap=tk.NONE,
            fg="#d60083", bg="white", state="disabled"
        )
        self.line_numbers.grid(row=1, column=0, sticky="nsew")

        # Main text widget
        self.input_text = tk.Text(
            self.left_frame, width=65, height=20,
            wrap=tk.WORD, fg="#d60083"
        )
        self.input_text.grid(row=1, column=1, sticky="nsew")

        # Input section scrollbar
        self.input_scrollbar = tk.Scrollbar(self.left_frame, orient="vertical")
        self.input_scrollbar.grid(row=1, column=2, sticky="ns")

        # Configure scrollbar connections
        self.input_scrollbar.config(command=self.on_input_scroll)
        self.input_text.config(yscrollcommand=self.input_scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.input_scrollbar.set)

        # Prevent individual scrolling
        def prevent_scroll(event):
            return "break"

        for widget in (self.input_text, self.line_numbers):
            widget.bind("<MouseWheel>", prevent_scroll)
            widget.bind("<Button-4>", prevent_scroll)
            widget.bind("<Button-5>", prevent_scroll)
            widget.bind("<Key-Up>", prevent_scroll)
            widget.bind("<Key-Down>", prevent_scroll)
            widget.bind("<Key-Prior>", prevent_scroll)
            widget.bind("<Key-Next>", prevent_scroll)

        # Bind text changes for line numbers
        self.input_text.bind('<<Modified>>', self.update_line_numbers)

    def setup_lexer_tokens_section(self):
        # Lexer label
        self.output_label = tk.Label(
            self.lr_frame, text="Lexeme", fg="white",
            font=("Arial", 14, "bold"), bg="#f99dbc"
        )
        self.output_label.grid(row=0, column=0, padx=5)

        # Tokens label
        self.tokens_label = tk.Label(
            self.lr_frame, text="Token", fg="white",
            font=("Arial", 14, "bold"), bg="#f99dbc"
        )
        self.tokens_label.grid(row=0, column=1, padx=5)

        # Create frame for listboxes and scrollbar
        list_frame = tk.Frame(self.lr_frame, bg="#f99dbc")
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Create line numbers frame for lexer
        lexer_frame = tk.Frame(list_frame, bg="#f99dbc")
        lexer_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ns")

        # Line numbers for lexer only
        self.lexer_line_numbers = tk.Text(
            lexer_frame, width=3, height=20, wrap=tk.NONE,
            fg="#d60083", bg="white", state="disabled"
        )
        self.lexer_line_numbers.grid(row=0, column=0, sticky="ns")

        # Lexer listbox
        self.output_listbox = tk.Listbox(
            lexer_frame, width=27, height=20, justify="center", fg="#d60083"
        )
        self.output_listbox.grid(row=0, column=1, sticky="ns")

        # Create frame for tokens (without line numbers)
        token_frame = tk.Frame(list_frame, bg="#f99dbc")
        token_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        # Tokens listbox only (no line numbers)
        self.token_listbox = tk.Listbox(
            token_frame, width=30, height=20, justify="center", fg="#d60083"
        )
        self.token_listbox.grid(row=0, column=0, sticky="ns")

        # Shared scrollbar for both listboxes
        self.lr_scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.lr_scrollbar.grid(row=0, column=2, sticky="ns")

        # Configure scrollbar connections
        self.lr_scrollbar.config(command=self.on_lr_scroll)
        self.output_listbox.config(yscrollcommand=self.sync_lr_scroll)
        self.token_listbox.config(yscrollcommand=self.sync_lr_scroll)
        self.lexer_line_numbers.config(yscrollcommand=self.sync_lr_scroll)

        # Prevent individual scrolling
        def ignore_events(event):
            return "break"

        for widget in (self.output_listbox, self.token_listbox, self.lexer_line_numbers):
            widget.bind("<MouseWheel>", ignore_events)
            widget.bind("<Button-4>", ignore_events)
            widget.bind("<Button-5>", ignore_events)
            widget.bind("<Up>", ignore_events)
            widget.bind("<Down>", ignore_events)
            widget.bind("<Next>", ignore_events)
            widget.bind("<Prior>", ignore_events)

    def setup_errors_section(self):
        # Errors label
        self.errors_label = tk.Label(
            self.bottom_frame, text="Output", fg="white",
            font=("Arial", 14, "bold"), bg="#f99dbc"
        )
        self.errors_label.grid(row=0, column=0)

        # Errors listbox
        self.errors_listbox = tk.Listbox(
            self.bottom_frame, width=162, height=10, fg="red"
        )
        self.errors_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Configure errors frame to expand properly
        self.bottom_frame.grid_columnconfigure(0, weight=1)

    def setup_analyze_button(self):
        # Create analyze button using Canvas
        self.analyze_button = tk.Canvas(
            self, height=50, width=200, highlightthickness=0,
            relief="raised", bg="#fdd9e5"
        )
        self.analyze_button.grid(row=3, column=0, columnspan=3, pady=0)

        # Add button text and sparkles
        self.analyze_button.create_text(
            40, 25, text="⋆✴︎", font=("Arial", 14, "bold"), fill="#efbf04"
        )
        self.analyze_button.create_text(
            100, 25, text="Cast Script", font=("Arial", 14, "bold"), fill="#d60083"
        )
        self.analyze_button.create_text(
            180, 25, text="˚｡⋆", font=("Arial", 14, "bold"), fill="#efbf04"
        )

        # Bind button events
        self.analyze_button.bind("<Button-1>", self.analyze_code)
        self.analyze_button.bind("<Enter>", self.on_hover)
        self.analyze_button.bind("<Leave>", self.on_leave)
        

    def on_input_scroll(self, *args):
        """Synchronize input text and line numbers scrolling"""
        self.input_text.yview(*args)
        self.line_numbers.yview(*args)

    def on_lr_scroll(self, *args):
        """Synchronize lexer and tokens scrolling including line numbers"""
        # Update all components
        self.output_listbox.yview(*args)
        self.token_listbox.yview(*args)
        self.lexer_line_numbers.yview(*args)

    def sync_lr_scroll(self, *args):
        """Update scrollbar position and sync all components"""
        self.lr_scrollbar.set(*args)
        
        # Get the fraction of scrolling
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components
        self.output_listbox.yview_moveto(fraction)
        self.token_listbox.yview_moveto(fraction)
        self.lexer_line_numbers.yview_moveto(fraction)

    def update_line_numbers(self, event=None):
        """Update line numbers and reset modified flag"""
        if event:
            self.input_text.edit_modified(False)
        
        content = self.input_text.get("1.0", "end-1c")
        num_lines = content.count('\n') + 1
        numbers = '\n'.join(str(i).rjust(3) for i in range(1, num_lines + 1))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", numbers)
        self.line_numbers.config(state='disabled')

    def update_lexer_token_line_numbers(self):
        """Update line numbers for lexer section only"""
        numbers = []

        # Ensure each line is accounted for, even if it has no tokens
        for line_idx, line_tokens in enumerate(self.tokens):
            if not line_tokens:
                numbers.append(str(line_idx + 1))  # Line number for empty token line
            else:
                numbers.extend([str(line_idx + 1)] * len(line_tokens))  # Line number for each token

        # Convert numbers to string with newlines
        numbers_str = "\n".join(numbers)

        # Update lexer line numbers only
        self.lexer_line_numbers.config(state='normal')
        self.lexer_line_numbers.delete("1.0", "end")
        self.lexer_line_numbers.insert("1.0", numbers_str)
        self.lexer_line_numbers.tag_configure("right", justify="right")
        self.lexer_line_numbers.tag_add("right", "1.0", "end")
        self.lexer_line_numbers.config(state='disabled')

    # def analyze_code(self, event=None):
    #     """Analyze the code and display results"""
    #     code = self.input_text.get("1.0", tk.END)
    #     lexer = RoyalScriptLexer(code)
        
    #     # Clear previous output
    #     self.output_listbox.delete(0, tk.END)
    #     self.token_listbox.delete(0, tk.END)
    #     self.errors_listbox.delete(0, tk.END)
    #     self.tokens = []  # Reset tokens list

    #     try:
    #         token_lines = lexer.get_tokens() or []
    #         self.tokens = token_lines  # Store the token lines
            
    #         for line_num, line_tokens in enumerate(token_lines, 1):
    #             if not line_tokens:  # If the line has no tokens
    #                 self.output_listbox.insert(tk.END, f" ")
    #                 self.token_listbox.insert(tk.END, " ")
    #             else:
    #                 for token in line_tokens:
    #                     if isinstance(token, Token):
    #                         self.output_listbox.insert(tk.END, f"{token.value}")
                            
    #                         if hasattr(token, 'token_type'):
    #                             definition = token.token_type.replace("_", " ")
    #                             self.token_listbox.insert(tk.END, f"{definition}")
            
    #         # Update line numbers after adding all tokens
    #         self.update_lexer_token_line_numbers()
            
    #         if lexer.errors:
    #             for error in lexer.errors:
    #                 self.errors_listbox.insert(tk.END, error)

    #     except SyntaxError as e:
    #         self.errors_listbox.insert(tk.END, f"Lexical Error: {str(e)}")
    #     except Exception as e:
    #         self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}")
    #         import traceback
    #         self.errors_listbox.insert(tk.END, f"Details: {traceback.format_exc()}")

    #lexer with syntax
    # def analyze_code(self, event=None):
    #     """Analyze the code and display results."""
    #     code = self.input_text.get("1.0", tk.END)
    #     lexer = RoyalScriptLexer(code)

    #     # Clear previous output
    #     self.output_listbox.delete(0, tk.END)
    #     self.token_listbox.delete(0, tk.END)
    #     self.errors_listbox.delete(0, tk.END)

    #     lexer_error = False  # Flag to track lexer errors
    #     all_tokens = []  # Store tokens for syntax analysis

    #     try:
    #         token_lines = lexer.get_tokens()  # Lexer generates tokens (2D array)
            
    #         # 🚨 Check if lexer returned empty or invalid tokens
    #         if not token_lines or any(not isinstance(line, list) for line in token_lines):
    #             lexer_error = True
    #             self.errors_listbox.insert(tk.END, "Lexer Error: No valid tokens detected!")
            
    #         for line_num, line_tokens in enumerate(token_lines, 1):
    #             if line_num > 1:
    #                 self.output_listbox.insert(tk.END, "──────────────")
    #                 self.token_listbox.insert(tk.END, "──────────────")

    #             self.output_listbox.insert(tk.END, f"Line {line_num}:")
    #             self.token_listbox.insert(tk.END, f"Line {line_num}:")

    #             token_types = []  # Store token types for syntax analysis
    #             for token in line_tokens:
    #                 if isinstance(token, Token):  # Ensure it's a valid Token object
    #                     token_type = token.token_type
    #                     self.output_listbox.insert(tk.END, f"{token.value}")
    #                     self.token_listbox.insert(tk.END, token_type.replace("_", " "))
    #                     token_types.append(token_type)
    #                 else:
    #                     lexer_error = True  # Invalid token detected
    #                     self.errors_listbox.insert(tk.END, f"Lexer Error: Invalid token in line {line_num}")

    #             if not token_types:  # 🚨 Empty token list detected (likely a lexer issue)
    #                 lexer_error = True
    #                 self.errors_listbox.insert(tk.END, f"Lexer Error: No valid tokens found in line {line_num}")

    #             all_tokens.append(token_types)  # Store for syntax analysis

    #     except Exception as e:
    #         lexer_error = True  # Ensure lexer errors prevent syntax analysis
    #         self.errors_listbox.insert(tk.END, f"Lexer Error: {str(e)}")

    #     #**Ensure syntax analyzer only runs if lexer succeeds**
    #     if lexer_error:
    #         self.errors_listbox.insert(tk.END, "Syntax analysis skipped due to lexer errors.")
    #     else:
    #         self.run_syntax_analyzer(all_tokens)


    def analyze_code(self, event=None):
        """Analyze the code and display results"""
        code = self.input_text.get("1.0", tk.END)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.errors_listbox.delete(0, tk.END)
        self.tokens = []  # Reset tokens list
        all_tokens = []  # Store token types for additional analysis
        
        try:
            token_lines = lexer.get_tokens() or []
            self.tokens = token_lines  # Store the token lines
            
            # Check if we have valid tokens
            if not token_lines:
                self.errors_listbox.insert(tk.END, "Lexer Error: No tokens detected")
                return
                
            for line_num, line_tokens in enumerate(token_lines, 1):
                # Add separator between lines
                # if line_num > 1:
                
                token_types = []  # Store token types for this line
                
                if not line_tokens:  # If the line has no tokens
                    self.output_listbox.insert(tk.END, f" ")
                    self.token_listbox.insert(tk.END, " ")
                else:
                    for token in line_tokens:
                        if isinstance(token, Token):
                            self.output_listbox.insert(tk.END, f"{token.value}")
                            
                            if hasattr(token, 'token_type'):
                                definition = token.token_type.replace("_", " ")
                                self.token_listbox.insert(tk.END, f"{definition}")
                                token_types.append(token.token_type)  # Store the token type
                
                all_tokens.append(token_types)  # Add this line's token types to all_tokens
            
            # Update line numbers after adding all tokens
            self.update_lexer_token_line_numbers()
            
            if lexer.errors:
                for error in lexer.errors:
                    self.errors_listbox.insert(tk.END, error)
            else:
                # No lexer errors, proceed to syntax analysis with both full tokens and token types
                self.run_syntax_analyzer(all_tokens)

        except SyntaxError as e:
            self.errors_listbox.insert(tk.END, f"Lexical Error: {str(e)}")
        except Exception as e:
            self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}")
            import traceback
            self.errors_listbox.insert(tk.END, f"Details: {traceback.format_exc()}")
                

    def run_syntax_analyzer(self, tokens):
        """Run the syntax analyzer with tokens"""
        parser = RoyalScriptParser(tokens)

        try:
            parser.parse()  # Run the syntax analysis
            # self.errors_listbox.insert(tk.END, "\n─── Parser Output ───")
            self.errors_listbox.insert(tk.END, parser.get_parsing_result())

        except SyntaxError as e:
            # self.errors_listbox.insert(tk.END, "\n─── Parser Error ───")
            self.errors_listbox.insert(tk.END, f"Syntax Error: {str(e)}")
            
        except Exception as e:
            # self.errors_listbox.insert(tk.END, "\n─── Parser Error ───")
            self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}")


    def on_hover(self, event):
        """Change button appearance on hover"""
        self.analyze_button.config(bg="#f0a6ca")

    def on_leave(self, event):
        """Reset button appearance when mouse leaves"""
        self.analyze_button.config(bg="#fdd9e5")

if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()