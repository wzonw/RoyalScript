import tkinter as tk
from tkinter import PhotoImage, scrolledtext
from PIL import Image, ImageTk, ImageSequence
from lexer2 import RoyalScriptLexer
from lexer2 import Token
from pygame import mixer
from parser import RoyalScriptParser
from ast_builder import RoyalScriptASTBuilder
#from semantic_copy import RoyalScriptSemanticAnalyzer 


class RoyalScriptLexerGUI(tk.Tk):
    
    mixer.init()
    def __init__(self):
        super().__init__()
        self.tokens = [] 

        # def intro_music():
        #     mixer.music.load("fairytale_intro.mp3")
        #     mixer.music.play(-1) 
        # intro_music()
            
        self.title("RoyalScript")
        self.iconphoto(False, PhotoImage(file="crown_logo2.png")) 
        self.state('zoomed')
        self.resizable(False, False)
        

        # Load and set background image
        self.bg_image = Image.open("images/rsbg.gif")
        self.frames = []
        self.durations = []

        # Extract frames and durations
        for frame in ImageSequence.Iterator(self.bg_image):
            self.frames.append(ImageTk.PhotoImage(frame.copy()))
            self.durations.append(frame.info.get('duration', 100))

        self.bg_label = tk.Label(self, image=self.frames[0])
        self.bg_label.place(relwidth=1, relheight=1)

        # Allow frames to expand dynamically
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        #self.grid_rowconfigure(3, weight=0)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Setup GUI components
        self.setup_frames()
        self.setup_analyze_button()
        self.setup_input_section()
        self.setup_lexer_tokens_section()
        self.setup_errors_section()
        
        self.animate(0)

    def animate(self, frame):
        next_frame = (frame + 1) % len(self.frames)  # Loop through frames
        self.bg_label.config(image=self.frames[next_frame])
        self.after(25, self.animate, next_frame)  # Adjust delay if needed (e.g., 100ms)
    
    def start_typing_effect(self, full_text):
        """Start the typing animation for parser output."""
        self.typing_text = full_text
        self.current_index = 0
        self.errors_listbox.insert(tk.END, "")  # Clear any previous content
        self.animate_text()

    def animate_text(self):
        """Animate the text appearing in the listbox letter by letter."""
        if self.current_index < len(self.typing_text):
            # Get current text and append the next character
            current_text = self.errors_listbox.get(tk.END)
            self.errors_listbox.delete(tk.END)  # Remove last entry
            self.errors_listbox.insert(tk.END, current_text + self.typing_text[self.current_index])

            self.current_index += 1
            self.after(10, self.animate_text)  # Adjust speed (50ms per letter)


        
    def setup_frames(self):

        # Main frames with consistent padding f883aa
        self.left_frame = tk.Frame(self, bg="#f883aa",bd=3, relief="ridge")
        self.left_frame.grid(row=1, column=0, columnspan=1, padx=(20,10), pady=(0, 5), sticky="nsw")

        # Combined frame for Lexer and Tokens
        self.lr_frame = tk.Frame(self, bg="#f883aa", bd=3, relief="ridge")
        self.lr_frame.grid(row=1, column=1, columnspan=2, padx=(0, 200), pady=(0, 5), sticky="nsw")

        # Errors frame
        self.bottom_frame = tk.Frame(self, bg="#f883aa", bd=3, relief="ridge")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=(20,0), pady=(10, 30), sticky="sw")

        #self.button_frame = tk.Frame(self, bg="#f883aa")
        #self.button_frame.grid(row=1, column=2, padx=0, pady=0, sticky="sw")

        self.button_frame = tk.Frame(self, bd=5, relief="sunken", highlightthickness=3)
        self.button_frame.grid(row=1, column=2, columnspan=2, rowspan=3, sticky="nw", pady=10, padx=(5,10))

        #button frame imgae
        self.button_image = Image.open("images/cushion.png")
        self.button_image = self.button_image.resize((250,250), Image.Resampling.LANCZOS)
        self.button_image = ImageTk.PhotoImage(self.button_image)
        
        self.button_label = tk.Label(self.button_frame, image=self.button_image)
        self.button_label.place(relwidth=1, relheight=1)   

        self.logo_frame = tk.Frame(self, bg="")
        self.logo_frame.grid(row=2, column=2, sticky="nsew", pady=(0,10), padx=(5,10))

        # Program frame
        #self.program_frame = tk.Frame(self, bg="#f883aa")
        #self.program_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.logo_pic = Image.open("images/RoyalScript_logo.png")
        self.logo_pic = self.logo_pic.resize((200,200), Image.Resampling.LANCZOS)
        self.logo_pic = ImageTk.PhotoImage(self.logo_pic)

        self.logo_label = tk.Label(self.logo_frame, image=self.logo_pic, bg="#E53888")
        self.logo_label.pack(pady=10)  


    def setup_input_section(self):
        # Input Code label

        self.input_label = tk.Label(
            self.left_frame, text="Input Code", fg="white", #Fonts =  Castellar, Edwardian Script, French Script, Monotype Corsiva, Constantia, Century Schoolbook, High Tower Text
            font=("Monotype Corsiva", 14, "bold"), bg="#f883aa"
        )
        self.input_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Left Frame Centered
        #self.left_frame.grid_columnconfigure(0, weight=1)  # Line numbers
        #self.left_frame.grid_columnconfigure(1, weight=3)  # Text input (centered)
        #self.left_frame.grid_columnconfigure(2, weight=0)  # Scrollbar

        self.line_numbers = tk.Text(
            self.left_frame, width=6, height=25, wrap=tk.NONE,
            fg="white", bg="#E53888", state="disabled", borderwidth=5
        )
        self.line_numbers.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(3,20))
        
        # Main text widget
        self.input_text = tk.Text(
            self.left_frame, width=85, height=25,
            wrap=tk.WORD, fg="#d60083", relief="sunken", bd=5
        )
        self.input_text.grid(row=1, column=1, padx=(0, 0), pady=(3,20))

        # Input section scrollbar
        self.input_scrollbar = tk.Scrollbar(self.left_frame, orient="vertical")
        self.input_scrollbar.grid(row=1, column=2, sticky="nsew", padx=(1,10), pady=(3,20))

        # Configure scrollbar connections
        self.input_scrollbar.config(command=self.on_input_scroll)
        self.input_text.config(yscrollcommand=self.sync_input_scrollbar)
        self.line_numbers.config(yscrollcommand=self.sync_input_scrollbar)

        # Prevent individual scrolling
        def prevent_scroll(event):
            return "break"
        
        def scroll_text(event): #make the GUI scrollable with touchpad/scroll
            text_widget.yview_scroll(-1 * (event.delta // 120), "units")

        for widget in (self.input_text, self.line_numbers):
            widget.bind("<MouseWheel>", scroll_text)
            widget.bind("<Button-4>", prevent_scroll)
            widget.bind("<Button-5>", prevent_scroll)
            #widget.bind("<Key-Up>", prevent_scroll)
            #widget.bind("<Key-Down>", prevent_scroll)
            widget.bind("<Key-Prior>", prevent_scroll)
            widget.bind("<Key-Next>", prevent_scroll)

        # Bind text changes for line numbers
        self.input_text.bind('<<Modified>>', self.update_line_numbers)

    def setup_lexer_tokens_section(self):

        # Lexeme Token Frame Centered
        self.lr_frame.grid_columnconfigure(0, weight=1)  
        self.lr_frame.grid_columnconfigure(1, weight=1)  

        # Lexer label
        self.output_label = tk.Label(
            self.lr_frame, text="Lexeme", fg="white",
            font=("Monotype Corsiva", 14, "bold"), bg="#f883aa"
        )
        self.output_label.grid(row=0, column=0, padx=5, pady=(5,0))

        # Tokens label
        self.tokens_label = tk.Label(
            self.lr_frame, text="Token", fg="white",
            font=("Monotype Corsiva", 14, "bold"), bg="#f883aa" #Fonts =  Castellar, Edwardian Script, French Script, Monotype Corsiva
        )
        self.tokens_label.grid(row=0, column=1, padx=5, pady=(5,0))

        # Create frame for listboxes and scrollbar
        list_frame = tk.Frame(self.lr_frame, bg="#f883aa")
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Create line numbers frame for lexer
        lexer_frame = tk.Frame(list_frame, bg="#f883aa")
        lexer_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        # Line numbers for lexer only
        self.lexer_line_numbers = tk.Text(
            lexer_frame, width=3, height=24, wrap=tk.NONE,
            fg="white", bg="#E53888", state="disabled"
        )
        self.lexer_line_numbers.grid(row=0, column=0, sticky="ns", padx=(5, 0), pady=0)

        # Lexer listbox
        self.output_listbox = tk.Listbox(
            lexer_frame, width=33, height=25, justify="center", fg="#d60083", relief="sunken", bd=5
        )
        self.output_listbox.grid(row=0, column=1, sticky="nsew", padx=(0,0), pady=0)

        # Create frame for tokens (without line numbers)
        token_frame = tk.Frame(list_frame, bg="#f883aa")
        token_frame.grid(row=0, column=1, padx=(0,0), pady=10, sticky="nsew")

        # Tokens listbox only (no line numbers)
        self.token_listbox = tk.Listbox(
            token_frame, width=33, height=25, justify="center", fg="#d60083", relief="sunken", bd=5
        )
        self.token_listbox.grid(row=0, column=0, sticky="nsew", padx=(0, 1), pady=0)

        # Shared scrollbar for both listboxes
        self.lr_scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.lr_scrollbar.grid(row=0, column=2, sticky="nsew", padx=(0,10), pady=10)

        # Configure scrollbar connections
        self.lr_scrollbar.config(command=self.on_lr_scroll)
        self.output_listbox.config(yscrollcommand=self.sync_lr_scroll)
        self.token_listbox.config(yscrollcommand=self.sync_lr_scroll)
        self.lexer_line_numbers.config(yscrollcommand=self.sync_lr_scroll)

        # Prevent individual scrolling
        def ignore_events(event):
            return "break"
        
        def scroll_text(event): #make the GUI scrollable with touchpad/scroll
            text_widget.yview_scroll(-1 * (event.delta // 120), "units")

        for widget in (self.output_listbox, self.token_listbox, self.lexer_line_numbers):
            widget.bind("<MouseWheel>", scroll_text)
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
            font=("Monotype Corsiva", 14, "bold"), bg="#f883aa"
        )
        self.errors_label.grid(row=0, column=0, pady=5)

        # Errors listbox
        self.errors_listbox = tk.Listbox(
            self.bottom_frame, width=208, height=12,  relief="sunken", bd=5
        )
        self.errors_listbox.grid(row=2, column=0, padx=(10,0), pady=(3,20), sticky="ew")

        # Configure errors frame to expand properly
        self.bottom_frame.grid_columnconfigure(0, weight=0)
        
        self.error_scrollbar = tk.Scrollbar(self.bottom_frame, orient="vertical")
        self.error_scrollbar.grid(row=2, column=1, sticky="nsew", padx=(1,10), pady=(3,20))

        # Configure scrollbar connections
        self.error_scrollbar.config(command=self.on_error_scroll)
        self.errors_listbox.config(yscrollcommand=self.sync_errors_scroll)

        # Prevent individual scrolling
        def prevent_scroll(event):
            return "break"
        
        def scroll_text(event): #make the GUI scrollable with touchpad/scroll
            text_widget.yview_scroll(-1 * (event.delta // 120), "units")

        for widget in (self.input_text, self.line_numbers):
            widget.bind("<MouseWheel>", scroll_text)
            widget.bind("<Button-4>", prevent_scroll)
            widget.bind("<Button-5>", prevent_scroll)
            #widget.bind("<Key-Up>", prevent_scroll)
            #widget.bind("<Key-Down>", prevent_scroll)
            widget.bind("<Key-Prior>", prevent_scroll)
            widget.bind("<Key-Next>", prevent_scroll)


    def setup_analyze_button(self):
        
        # Create analyze button using Canvas
        self.analyze_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0, relief="raised", bd=3
        )
        self.analyze_button.grid(row=0, column=2, sticky="sew", pady=10, padx=30)

        # Add button text and sparkles
        self.analyze_button.create_text(
            53, 18, text="Cast Script", font=("Century Schoolbook", 8, "bold"), fill="#d60083"
        )

        # Bind button events
        self.analyze_button.bind("<Button-1>", self.analyze_code)
        self.analyze_button.bind("<Enter>", self.on_hover)
        self.analyze_button.bind("<Leave>", self.on_leave)

        # Create syntax button using Canvas
        self.syntax_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0,  relief="raised", bd=3
        )
        self.syntax_button.grid(row=1, column=2, sticky="sew", pady=10, padx=30)

       # Add button text 
        self.syntax_button.create_text(
            50, 15, text="Syntax", font=("Century Schoolbook", 8, "bold"), fill="#d60083"
        )

        # Bind button events
        self.syntax_button.bind("<Button-2>", self.syntax_button)
        self.syntax_button.bind("<Enter>", self.on_hover_syntax)
        self.syntax_button.bind("<Leave>", self.on_leave_syntax)
       

        # Create semantic button using Canvas
        self.semantic_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0,
        )
        self.semantic_button.grid(row=2, column=2, sticky="sew", pady=10, padx=30)

       # Add button text and sparkles
        self.semantic_button.create_text(
            50, 15, text="Semantic", font=("Arial", 8, "bold"), fill="#d60083"
        )

        # Bind button events
        #self.semantic_button.bind("<Button-2>", self.analyze_code)
        #self.semantic_button.bind("<Enter>", self.on_hover)
        #self.semantic_button.bind("<Leave>", self.on_leave)
       
        # Create overall run button using Canvas
        self.run_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0,
        )
        self.run_button.grid(row=3, column=2, sticky="sew", pady=10, padx=30)

       # Add button text and sparkles
        self.run_button.create_text(
            50, 15, text="Run", font=("Arial", 8, "bold"), fill="#d60083"
        )

        # Bind button events
        #self.semantic_button.bind("<Button-2>", self.analyze_code)
        #self.semantic_button.bind("<Enter>", self.on_hover)
        #self.semantic_button.bind("<Leave>", self.on_leave)



    def on_input_scroll(self, *args):
        """Synchronize input text and line numbers scrolling"""
        self.input_text.yview(*args)
        self.line_numbers.yview(*args)
        
    def on_error_scroll(self, *args):
        """Synchronize error_text scrolling"""
        self.error_listbox.yview(*args)

    def on_lr_scroll(self, *args):
        """Synchronize lexer and tokens scrolling including line numbers"""
        # Update all components
        self.output_listbox.yview(*args)
        self.token_listbox.yview(*args)
        self.lexer_line_numbers.yview(*args)
    
    def sync_errors_scroll(self, *args):
        """Update scrollbar position and sync all components"""
        self.error_scrollbar.set(*args)
        
        # Get the fraction of scrolling
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components
        self.errors_listbox.yview_moveto(fraction)

    def sync_lr_scroll(self, *args):
        """Update scrollbar position and sync all components"""
        self.lr_scrollbar.set(*args)
        
        # Get the fraction of scrolling
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components
        self.output_listbox.yview_moveto(fraction)
        self.token_listbox.yview_moveto(fraction)
    
    def sync_input_scrollbar(self, *args):
        """Update scrollbar position and sync all components"""
        self.input_scrollbar.set(*args)
        
        # Get the fraction of scrolling
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components
        self.input_text.yview_moveto(fraction)
        self.line_numbers.yview_moveto(fraction)

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
        self.line_numbers.tag_configure("right", justify="right")
        self.line_numbers.tag_add("right", "1.0", "end")
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
    #            = []  # Reset tokens list

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

    def semantic_button(self, event=None):
        return

    def syntax_button(self, event=None):
        return

    def run_button(self, event=None):
        return

    
    
    def analyze_code(self, event=None):
        """Analyze the code and display results"""
        code = self.input_text.get("1.0", tk.END)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.errors_listbox.delete(0, tk.END)
        self.tokens = []  # Reset tokens list
        all_tokens = []  # Store tokens (type and value) for additional analysis
        
        try:
            token_lines = lexer.get_tokens() or []
            self.tokens = token_lines  # Store the token lines

            # Check if we have valid tokens
            if not token_lines:
                self.errors_listbox.insert(tk.END, "Lexer Error: No tokens detected")
                return
                
            for line_num, line_tokens in enumerate(token_lines, 1):
                tokens = []  # Store tokens for this line (each as a tuple)
                
                if not line_tokens:  # If the line has no tokens
                    self.output_listbox.insert(tk.END, " ")
                    self.token_listbox.insert(tk.END, " ")
                else:
                    for token in line_tokens:
                        if isinstance(token, Token):
                            # Insert token value into the output listbox.
                            self.output_listbox.insert(tk.END, f"{token.value}")
                            
                            # Create a display string for the token type and value.
                            if hasattr(token, 'token_type'):
                                display = f"{token.token_type}"
                                self.token_listbox.insert(tk.END, display)
                                
                                # Append a tuple containing both token_type and value.
                                tokens.append((token.token_type, token.value))
                all_tokens.append(tokens)  # Add this line's tokens to all_tokens
            
            # Update line numbers after adding all tokens (if you have such a function).
            self.update_lexer_token_line_numbers()
            
            # If the lexer found errors, list them
            if lexer.errors:
                for error in lexer.errors:
                    self.errors_listbox.insert(tk.END, f"❌ Lexical Error: {error}")
            
            # Show lexical success message in its own listbox item, AFTER error checking
            else:
                self.errors_listbox.insert(tk.END, "✅ Lexical Analysis Successful.")
                
                # Now run syntax analysis
                self.run_syntax_analyzer(all_tokens)
        
        except SyntaxError as e:
            self.errors_listbox.insert(tk.END, f"Lexical Error: {str(e)}")
        except Exception as e:
            import traceback
            self.errors_listbox.insert(tk.END, f"Unexpected Error: {str(e)}")
            self.errors_listbox.insert(tk.END, f"Details: {traceback.format_exc()}")

    def run_syntax_analyzer(self, tokens):
        """Run the syntax analyzer with tokens."""
        parser = RoyalScriptParser(tokens)

        try:
            syntax_result = parser.parse()  # Run the syntax analysis

            if syntax_result:
                # Insert success message on a new line
                self.errors_listbox.insert(tk.END, "✅ Syntax Analysis Successful!")
            else:
                # Insert failure message on its own line
                self.errors_listbox.insert(tk.END, "❌ Syntax Analysis Failed.")

        except SyntaxError as e:
            # Insert the syntax error message as a separate item
            self.errors_listbox.insert(tk.END, f"❌ {str(e)}")
        except Exception as e:
            self.errors_listbox.insert(tk.END, f" ❌ Unexpected Error in Syntax Analysis: {str(e)}")
        

    # def run_semantic_analyzer(self, final_statements_list):
    #     """Run the semantic analyzer if syntax is correct."""
    #     semantic_analyzer = RoyalScriptSemanticAnalyzer(final_statements_list)

    #     try:
    #         analysis_successful = semantic_analyzer.analyze()  # Returns True if no errors

    #         if analysis_successful:  # ✅ True means successful semantic analysis
    #             self.errors_listbox.insert(tk.END, "✅ Semantic Analysis Successful!")
    #         else:
    #             self.errors_listbox.insert(tk.END, "❌ Semantic Analysis Failed. Errors found:")
    #             for error in semantic_analyzer.errors:
    #                 if error and error.strip():  # ensures error isn't empty or whitespace-only
    #                     self.errors_listbox.insert(tk.END, f"   ➤ {error}")



    def on_hover(self, event):
        """Change button appearance on hover"""
        self.analyze_button.config(bg="#f0a6ca")
    
    def on_hover_syntax(self, event):
        """Change button appearance on hover"""
        self.syntax_button.config(bg="#f0a6ca")

    def on_leave_syntax(self, event):
        """Change button appearance on hover"""
        self.syntax_button.config(bg="#fdd9e5")

    def on_leave(self, event):
        """Reset button appearance when mouse leaves"""
        self.analyze_button.config(bg="#fdd9e5") # white font

if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()