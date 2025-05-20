import tkinter as tk
import subprocess
import sys
import threading
from tkinter import PhotoImage, scrolledtext
from PIL import Image, ImageTk, ImageSequence
from lexer import RoyalScriptLexer
from lexer import Token
from pygame import mixer
from parser import  RoyalScriptParser
from ast_builder import RoyalScriptASTBuilder
from semantic import SemanticAnalyzer
from translator import RoyalScriptToPythonTranslator
import time 
import traceback
from ast_display import print_ast

class InteractiveTerminal:
    """Class to handle interactive I/O with subprocesses"""
    def __init__(self, output_widget):
        self.output_widget = output_widget
        self.process = None
        self.is_waiting_for_input = False
        self.stdout_thread = None
        self.stderr_thread = None
        
    def start_process(self, command):
        """Start a subprocess to run output.py"""
        # Terminate any existing process first
        self.terminate_process()
        
        # Create process with pipes for stdin, stdout, stderr
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start threads to monitor output
        self.stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, "stdout"))
        self.stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, "stderr"))
        
        self.stdout_thread.daemon = True
        self.stderr_thread.daemon = True
        
        self.stdout_thread.start()
        self.stderr_thread.start()

    def _read_output(self, pipe, pipe_name):
        """Read the output from the process and handle interactive input"""
        while True:
            line = pipe.readline()
            if not line:
                break

            # Check for input request but don't duplicate the prompt that input() will show
            if "INPUT_REQUEST:" in line:
                prompt = line.strip().replace("INPUT_REQUEST:", "").strip()
                self.is_waiting_for_input = True
                self._display_input_prompt(prompt)  # Display input prompt immediately
            else:
                # For regular output, just display it in real-time
                cleaned_line = line
                is_err = (pipe_name == "stderr")
                self.output_widget.after(0, self._update_output, cleaned_line, is_err)

    def _display_input_prompt(self, prompt):
        """Display input prompt immediately and wait for input"""
        self._set_waiting_for_input()
        self.output_widget.config(state=tk.NORMAL)
        self.output_widget.insert(tk.END, prompt + " ", "input_prompt")
        self.output_widget.see(tk.END)
        self.output_widget.config(state=tk.DISABLED)
        sys.stdout.flush()  # Flush output immediately after displaying prompt

    def send_input(self, text):
        """Send input to the process only if not empty"""
        if not text.strip():
            # Don't send empty input
            return False
            
        if self.process and self.process.poll() is None:  # If process is running
            try:
                # Display the input in the terminal
                self.output_widget.config(state=tk.NORMAL)
                self.output_widget.insert(tk.END, text + "\n", "user_input")
                self.output_widget.see(tk.END)
                self.output_widget.config(state=tk.DISABLED)

                # Send to process
                self.process.stdin.write(text + '\n')
                self.process.stdin.flush()
                
                # Clear waiting flag
                self.is_waiting_for_input = False
                return True
            except Exception as e:
                self.output_widget.config(state=tk.NORMAL)
                self.output_widget.insert(tk.END, f"Error sending input: {str(e)}\n", "error")
                self.output_widget.see(tk.END)
                self.output_widget.config(state=tk.DISABLED)
                return False
        return False

    def is_running(self):
        """Check if process is still running"""
        return self.process is not None and self.process.poll() is None
        
    def terminate_process(self):
        """Terminate the current process if it exists and is running"""
        if self.process and self.process.poll() is None:
            try:
                # Try to terminate gracefully first
                self.process.terminate()
                
                # Give it a moment to terminate
                timeout = 0.5
                start_time = time.time()
                while self.process.poll() is None and time.time() - start_time < timeout:
                    time.sleep(0.1)
                    
                # If still running after timeout, force kill
                if self.process.poll() is None:
                    self.process.kill()
                
                # Reset flags
                self.is_waiting_for_input = False
            except Exception as e:
                self.output_widget.config(state=tk.NORMAL)
                self.output_widget.insert(tk.END, f"\nError terminating process: {str(e)}\n", "error")
                self.output_widget.see(tk.END)
                self.output_widget.config(state=tk.DISABLED)

    def _set_waiting_for_input(self):
        """Set flag indicating process is waiting for input"""
        self.is_waiting_for_input = True
    
    def _clear_waiting_for_input(self):
        """Clear flag indicating process is waiting for input"""
        self.is_waiting_for_input = False
    
    def _update_output(self, text, is_error=False):
        """Update the output widget with text from subprocess"""
        self.output_widget.config(state=tk.NORMAL)
        if is_error:
            self.output_widget.insert(tk.END, text, "error")
        else:
            self.output_widget.insert(tk.END, text)
        self.output_widget.see(tk.END)
        self.output_widget.config(state=tk.DISABLED)

class RoyalScriptLexerGUI(tk.Tk):
    
    mixer.init()
    
    # Class method to allow access from Tcl interpreter
    @classmethod
    def _display_output(cls, widget_id, text, is_error=False):
        """Display output in the terminal widget - accessible from other threads"""
        widget = tk._default_root.nametowidget(str(widget_id))
        widget.config(state=tk.NORMAL)
        if is_error:
            widget.insert(tk.END, text, "error")
        else:
            widget.insert(tk.END, text)
        widget.see(tk.END)
        widget.config(state=tk.DISABLED)
    
    def __init__(self):
        super().__init__()
        self.tokens = [] 
        self.terminal = None  # Will be initialized later

        # def intro_music():
        #     mixer.music.load("Gui_elements/fairytale_intro.mp3")
        #     mixer.music.play(-1) 
        # intro_music()
            
        self.title("RoyalScript")
        self.iconphoto(False, PhotoImage(file="Gui_elements/crown_logo2.png")) 
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
        self.setup_interactive_terminal()
        
        self.animate(0)

    def animate(self, frame):
        next_frame = (frame + 1) % len(self.frames)  # Loop through frames
        self.bg_label.config(image=self.frames[next_frame])
        self.after(25, self.animate, next_frame)  # Adjust delay if needed (e.g., 100ms)
    
    def start_typing_effect(self, full_text): #Typing effect in Output box
        """Start the typing animation for parser output."""
        self.typing_text = full_text
        self.current_index = 0
        #self.errors_listbox.insert(tk.END, "")  # Clear any previous content
        self.animate_text()

    def animate_text(self):
        """Animate the text appearing in the listbox letter by letter."""
        if self.current_index < len(self.typing_text):
            # Get current text and append the next character
            current_text = self.terminal_text.get(tk.END)
            #self.errors_listbox.delete(tk.END)  # Remove last entry
            self.terminal_text.insert(tk.END, current_text + self.typing_text[self.current_index])

            self.current_index += 1
            self.after(10, self.animate_text)  # Adjust speed (50ms per letter)
        
    def setup_frames(self):

        # Main frames with consistent padding f883aa
        self.left_frame = tk.Frame(self, bg="#f883aa",bd=3, relief="ridge")
        self.left_frame.grid(row=1, column=0, columnspan=1, padx=(20,10), pady=(0, 5), sticky="nsw")

        # Combined frame for Lexer and Tokens
        self.lr_frame = tk.Frame(self, bg="#f883aa", bd=3, relief="ridge")
        self.lr_frame.grid(row=1, column=1, columnspan=2, padx=(0, 200), pady=(0, 5), sticky="nsw")

        # Terminal frame
        self.bottom_frame = tk.Frame(self, bg="#f883aa", bd=3, relief="ridge")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=(20,0), pady=(10, 30), sticky="sw")

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

        self.line_numbers = tk.Text(
            self.left_frame, width=5, height=25, wrap=tk.NONE,
            fg="white", bg="#E53888", state="disabled", borderwidth=5
        )
        self.line_numbers.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(3,20))
        
        # Main text widget
        self.input_text = tk.Text(
            self.left_frame, width=85, height=25,
            wrap=tk.WORD, fg="#d60083", relief="sunken", bd=5, undo=True, maxundo=-1, autoseparators=True)
        
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
            self.input_text.yview_scroll(-1 * (event.delta // 120), "units")
            return "break"

        for widget in (self.input_text, self.line_numbers):
            widget.bind("<MouseWheel>", scroll_text)
            widget.bind("<Button-4>", prevent_scroll)
            widget.bind("<Button-5>", prevent_scroll)
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
            fg="white", bg="#E53888", state="disabled", borderwidth=5
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
            self.output_listbox.yview_scroll(-1 * (event.delta // 120), "units")
            return "break"

        for widget in (self.output_listbox, self.token_listbox, self.lexer_line_numbers):
            widget.bind("<MouseWheel>", scroll_text)
            widget.bind("<Button-4>", ignore_events)
            widget.bind("<Button-5>", ignore_events)
            widget.bind("<Up>", ignore_events)
            widget.bind("<Down>", ignore_events)
            widget.bind("<Next>", ignore_events)
            widget.bind("<Prior>", ignore_events)

    def setup_interactive_terminal(self):
        """Setup the interactive terminal section with input capabilities"""
        # Terminal label
        self.terminal_label = tk.Label(
            self.bottom_frame, text="Terminal", fg="white",
            font=("Monotype Corsiva", 14, "bold"), bg="#f883aa"
        )
        self.terminal_label.grid(row=0, column=0, pady=5, sticky="w")

        # Terminal frame to contain both output and input areas
        terminal_frame = tk.Frame(self.bottom_frame, bg="#f883aa")
        terminal_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Terminal output text widget (scrolled text for better handling)
        self.terminal_text = scrolledtext.ScrolledText(
            terminal_frame, width=177, height=10, bg="black", fg="#00ff00",
            insertbackground="#00ff00", relief="sunken", bd=5, font=("Consolas", 10)
        )
        self.terminal_text.grid(row=0, column=0, padx=(0, 10), pady=(3, 0), sticky="nsew")
        
        # Configure the text tags
        self.terminal_text.tag_configure("error", foreground="red")
        self.terminal_text.tag_configure("input_prompt", foreground="yellow")
        self.terminal_text.tag_configure("user_input", foreground="cyan")
        
        self.terminal_text.config(state=tk.DISABLED)  # Make read-only initially
        
        # Terminal input frame
        input_frame = tk.Frame(terminal_frame, bg="#f883aa")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        
        # Terminal prompt label
        self.prompt_label = tk.Label(
            input_frame, text="> ", fg="#00ff00", bg="white",
            font=("Consolas", 10, "bold")
        )
        self.prompt_label.grid(row=0, column=0, sticky="w")
        
        # Terminal input entry
        self.terminal_input = tk.Entry(
            input_frame, width=177, bg="black", fg="#00ff00",
            insertbackground="#00ff00", relief="flat", font=("Consolas", 10)
        )
        self.terminal_input.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.terminal_input.bind("<Return>", self.on_terminal_input)
        
        # Create the interactive terminal handler
        self.terminal = InteractiveTerminal(self.terminal_text)
        
        # Configure the terminal frame to expand properly
        terminal_frame.grid_columnconfigure(0, weight=1)
        terminal_frame.grid_rowconfigure(0, weight=1)
        
        # Add a run button
        self.run_button_canvas = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0, relief="raised", bd=3
        )
        self.run_button_canvas.grid(row=3, column=2, sticky="sew", pady=10, padx=30)
        
        self.run_button_canvas.create_text(
            50, 15, text="Run", font=("Century Schoolbook", 8, "bold"), fill="#d60083"
        )
        
        self.run_button_canvas.bind("<Button-1>", self.run_code)
        self.run_button_canvas.bind("<Enter>", self.on_hover_run)
        self.run_button_canvas.bind("<Leave>", self.on_leave_run)

    def on_terminal_input(self, event=None):
        """Handle terminal input submission"""
        input_text = self.terminal_input.get()
        if input_text and self.terminal and self.terminal.is_running():
            # Send input to the process without any additional messages
            self.terminal.send_input(input_text)
            
            # Clear the input field
            self.terminal_input.delete(0, tk.END)
    
        return "break"  # Prevent default Enter behavior
    
    
    def submit_input(self, event=None):
        """Submit input to the running process"""
        # Get input from the input field
        input_text = self.input_field.get()
        
        # Special command to clear the terminal
        if input_text.strip().lower() == "clear":
            self.clear_terminal()
            self.input_field.delete(0, tk.END)
            return
        
        # Check if input is not empty and there's a running process waiting for input
        if hasattr(self, 'terminal') and self.terminal and self.terminal.is_running():
            # The send_input method now checks if the input is empty
            self.terminal.send_input(input_text)
            
        # Clear the input field regardless of whether input was sent
        self.input_field.delete(0, tk.END)

    def clear_terminal(self):
        """Clear the terminal output"""
        if hasattr(self, 'terminal_text'):
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.delete(1.0, tk.END)
            self.terminal_text.config(state=tk.DISABLED)
            
    def run_code(self, event=None):
        """Run the generated Python code with input capabilities"""
        # take the input and store it in code variable para gawing input sa lexical analysis 
        code = self.input_text.get("1.0", tk.END)
        # initialize lexical analyzer (imported lexer)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state=tk.DISABLED)
        all_tokens = []  # Store tokens (type and value) for additional analysis used for ast [[(token.token_type, token.value), (token.token_type, token.value)], [(token.token_type, token.value), (token.token_type, token.value)]]


        ############### lexical ###############
        try:
            # for each tokens per line, store in token_line var, if wala empty
            token_lines = lexer.get_tokens() or [] #[[(token.token_type, token.value, token.line, token.position), (token.token_type, token.value, token.line, token.position)], [(token.token_type, token.value, token.line, token.position), (token.token_type, token.value, token.line, token.position)]]
            
            # check if may naencounte ne errors
            if lexer.errors:
                # if meron idisplay sa terminal
                self.show_terminal_message("❌ Lexical errors detected:")
                for error in lexer.errors:
                    self.show_terminal_message(f"  - {error}")

                for line_idx, line_tokens in enumerate(token_lines):
                    # processes each individual token within a line.
                    for token in line_tokens:
                        # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                        if isinstance(token, Token) and hasattr(token, 'token_type'):
                            # if meron then display the token value (lexeme) and token type
                            self.output_listbox.insert(tk.END, token.value)
                            self.token_listbox.insert(tk.END, token.token_type)

                return
            
            # Display tokens in output_listbox and token_listbox (lexeme and token)
            """The outer loop (for line_idx, line_tokens in enumerate(token_lines)) 
            is going through each line in token_lines, getting both the index and the line's tokens."""
            for line_idx, line_tokens in enumerate(token_lines):
                # processes each individual token within a line.
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        # if meron then display the token value (lexeme) and token type
                        self.output_listbox.insert(tk.END, token.value)
                        self.token_listbox.insert(tk.END, token.token_type)

        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during lexical analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())
                
        # Prepare tokens for ast (ast input)
        """It iterates through each line of tokens in token_lines 
        (each line_tokens is a collection of tokens from a single line of text/code)"""
        for line_tokens in token_lines:
            # For each line, creates an empty list called tokens to store processed token information
            tokens = []
            # loops through each individual token within the current line
            for token in line_tokens:
                # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                if isinstance(token, Token) and hasattr(token, 'token_type'):
                    """If both conditions are met, creates a tuple containing the token's type and value 
                    (token.token_type, token.value) and add its tuple to the tokens list"""
                    tokens.append((token.token_type, token.value))
            # After processing all tokens in the current line, adds the collected tokens list to the all_tokens list
            all_tokens.append(tokens) # per lines pero ang laman lang is tyken_type and token value
        
        # Flatten tokens and collect line/column info
        flat_tokens = [] # [(token.token_type, token.value, token.line, token.position), (token.token_type, token.value, token.line, token.position), (token.token_type, token.value, token.line, token.position)]

        """It iterates through each line of tokens in token_lines 
        (each line_tokens is a collection of tokens from a single line of text/code)"""
        for line_tokens in token_lines:
            # loops through each individual token within the current line
            for token in line_tokens:
                if hasattr(token, 'token_type'):
                    """If token have attribute token_type add its tuple to the tokens list"""
                    flat_tokens.append(token) 

        ############### syntax ###############
        try:
            # initialize parser with argument <'program'> to specify the start of the reading of cfg
            parser = RoyalScriptParser('<program>') 
            # store the result and the error_message from the parser
            tree, error_message = parser.parse(flat_tokens)

            # if tree is true meaning successful yung pag parse
            if tree:

                # then since walang syntax error try to build ast 
                try:

                    # initialize ast builder pass the all_tokens as input
                    ast_builder = RoyalScriptASTBuilder(all_tokens)
                    ast = ast_builder.build_ast()
                except Exception as e:
                    self.show_terminal_message(f"AST building not performed - {str(e)}")
            
            # if may syntax error during parsing then display the errors
            else:
                self.show_terminal_message("❌ Syntax errors detected. Check your code structure.")
                if error_message:
                    self.show_terminal_message(error_message)
                    return

        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during syntax analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

        ############### semantic ###############
        try:        
            # Perform semantic analysis if walang lexical and syntax errors
            # initialize semantic analyzer and past the ast as input for semantic analysis
            semantic_analyzer = SemanticAnalyzer()
            semantic_errors = semantic_analyzer.analyze(ast)
            
            # if may semantic errors then display the erros the terminal
            if semantic_errors:
                self.show_terminal_message("❌ Semantic errors detected:")
                for error in semantic_errors:
                    self.show_terminal_message(f"  - {error}")
                
        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during semantic analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

        # Translate to Python
        try:
            # Initialize the translator object with global variable type information from the semantic analyzer
            translator = RoyalScriptToPythonTranslator(global_variable_types=semantic_analyzer.global_variable_types)
            
            # Translate the Abstract Syntax Tree (AST) into Python code
            python_code = translator.translate(ast)
            
            # Check if the returned Python code is a list of code lines instead of a single string
            # If it's a list, join the lines with newline characters to create a proper Python script
            if isinstance(python_code, list):
                python_code = "\n".join(python_code)
                
            # Define the output file path for the generated Python code
            output_file = "output.py"
            
            # Write the generated Python code to the output file
            # The 'utf-8' encoding ensures proper handling of special characters
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(python_code)
                    
            # Check if the terminal object exists and create it if needed
            # The terminal is used to run the generated Python code and display its output
            if not hasattr(self, 'terminal') or self.terminal is None:
                self.terminal = InteractiveTerminal(self.terminal_text)
            
            # Start the Python interpreter process with the generated code file
            # The "-u" flag enables unbuffered output, which is helpful for real-time display
            self.terminal.start_process(["python", "-u", output_file])

        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during compilation: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

    def show_terminal_message(self, message):
        """Display a message in the terminal"""
        # Enable editing of the terminal text widget temporarily
        self.terminal_text.config(state=tk.NORMAL)
        
        # Add the message to the terminal with a newline character
        self.terminal_text.insert(tk.END, message + "\n")
        
        # Scroll to show the latest message (scrolls to the end)
        self.terminal_text.see(tk.END)
        
        # Disable editing of the terminal text widget to prevent user modification
        self.terminal_text.config(state=tk.DISABLED)

    def on_input_scroll(self, *args):
        """Synchronize input text and line numbers scrolling"""
        # Apply the same scrolling parameters to both the input text editor
        # and the line numbers widget to keep them aligned
        self.input_text.yview(*args)
        self.line_numbers.yview(*args)

    def on_lr_scroll(self, *args):
        """Synchronize lexer and tokens scrolling including line numbers"""
        # Update all components in the lexer/token output area to scroll together
        # This ensures all three components stay aligned when scrolling
        self.output_listbox.yview(*args)
        self.token_listbox.yview(*args)
        self.lexer_line_numbers.yview(*args)

    def sync_lr_scroll(self, *args):
        """Update scrollbar position and sync all components"""
        # Set the scrollbar position based on the provided arguments
        self.lr_scrollbar.set(*args)
        
        # Get the fraction of scrolling (the position as a decimal between 0 and 1)
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components in the lexer/token area
        # This ensures synchronized scrolling when using the scrollbar
        self.output_listbox.yview_moveto(fraction)
        self.token_listbox.yview_moveto(fraction)
        self.lexer_line_numbers.yview_moveto(fraction) 

    def sync_input_scrollbar(self, *args):
        """Update scrollbar position and sync all components"""
        # Set the input area scrollbar position based on the provided arguments
        self.input_scrollbar.set(*args)
        
        # Get the fraction of scrolling (the position as a decimal between 0 and 1)
        fraction = float(args[0])
        
        # Apply the same scroll fraction to all components in the input area
        # This ensures the text editor and line numbers scroll together
        self.input_text.yview_moveto(fraction)
        self.line_numbers.yview_moveto(fraction)

    # updating line numbers in input section
    def update_line_numbers(self, event=None):
        """Update line numbers and reset modified flag"""
        # Reset the modified flag on the text widget to indicate changes have been processed
        self.input_text.edit_modified(False)
        
        # Get the current content of the text editor
        content = self.input_text.get("1.0", "end-1c")
        
        # Count the number of lines in the content (number of newlines plus 1)
        num_lines = content.count('\n') + 1
        
        # Create a string containing line numbers (1, 2, 3, etc.) 
        # Each number is right-justified with width of 3 characters
        numbers = '\n'.join(str(i).rjust(3) for i in range(1, num_lines + 1))
        
        # Store the current scroll position to restore it later
        scroll_position = self.input_text.yview()

        # Make the line numbers text widget editable temporarily
        self.line_numbers.config(state='normal')
        
        # Clear all existing content in the line numbers widget
        self.line_numbers.delete("1.0", "end")
        
        # Insert the newly created line numbers string
        self.line_numbers.insert("1.0", numbers)
        
        # Configure a tag for right-alignment
        self.line_numbers.tag_configure("right", justify="right")
        
        # Apply the right-alignment tag to all content in the line numbers widget
        self.line_numbers.tag_add("right", "1.0", "end")
        
        # Make the line numbers widget non-editable again
        self.line_numbers.config(state='disable')

        # Restore the previous scroll position for both widgets to maintain synchronization
        # This prevents the UI from jumping when line numbers are updated
        self.input_text.yview_moveto(scroll_position[0])
        self.line_numbers.yview_moveto(scroll_position[0])

    def setup_analyze_button(self):
        # Create analyze button using Canvas
        self.analyze_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0, relief="raised", bd=3
        )
        self.analyze_button.grid(row=0, column=2, sticky="sew", pady=10, padx=30)

        # Add button text and sparkles
        self.analyze_button.create_text(
            53, 18, text="Lexical", font=("Century Schoolbook", 8, "bold"), fill="#d60083"
        )

        # Bind button events
        self.analyze_button.bind("<Button-1>", self.analyze_lexical)
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
        self.syntax_button.bind("<Button-1>", self.analyze_syntax)  
        self.syntax_button.bind("<Enter>", self.on_hover_syntax)
        self.syntax_button.bind("<Leave>", self.on_leave_syntax)
    
        # Create semantic button using Canvas
        self.semantic_button = tk.Canvas(
            self.button_frame, height=30, width=100, highlightthickness=0, relief="raised", bd=3
        )
        self.semantic_button.grid(row=2, column=2, sticky="sew", pady=10, padx=30)

        # Add button text and sparkles
        self.semantic_button.create_text(
            50, 15, text="Semantic", font=("Century Schoolbook", 8, "bold"), fill="#d60083", 
        )

        # Bind button events
        self.semantic_button.bind("<Button-1>", self.analyze_semantic)
        self.semantic_button.bind("<Enter>", self.on_hover_semantic)
        self.semantic_button.bind("<Leave>", self.on_leave_semantic)

    def analyze_semantic(self, event=None):
        """Analyze the code and display semantic analysis results"""
        # take the input and store it in code variable para gawing input sa lexical analysis 
        code = self.input_text.get("1.0", tk.END)
        # initialize lexical analyzer (imported lexer)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state=tk.DISABLED)
        all_tokens = []  # Store tokens (type and value) for additional analysis used for ast
        
        try:
            # for each tokens per line, store in token_line var, if wala empty
            token_lines = lexer.get_tokens() or []
            
            # check if may naencounte ne errors
            if lexer.errors:
                # if meron idisplay sa terminal
                self.show_terminal_message("❌ Lexical errors detected:")
                for error in lexer.errors:
                    self.show_terminal_message(f"  - {error}")

                for line_idx, line_tokens in enumerate(token_lines):
                    # processes each individual token within a line.
                    for token in line_tokens:
                        # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                        if isinstance(token, Token) and hasattr(token, 'token_type'):
                            # if meron then display the token value (lexeme) and token type
                            self.output_listbox.insert(tk.END, token.value)
                            self.token_listbox.insert(tk.END, token.token_type)

                return
            else:
                # if wala display yung success message
                self.show_terminal_message("✅ Lexical analysis completed successfully!")
                self.show_terminal_message("No lexical errors found.")
            
            # Display tokens in output_listbox and token_listbox (lexeme and token)
            """The outer loop (for line_idx, line_tokens in enumerate(token_lines)) 
            is going through each line in token_lines, getting both the index and the line's tokens."""
            for line_idx, line_tokens in enumerate(token_lines):
                # processes each individual token within a line.
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        # if meron then display the token value (lexeme) and token type
                        self.output_listbox.insert(tk.END, token.value)
                        self.token_listbox.insert(tk.END, token.token_type)

            # Prepare tokens for ast (ast input)
            """It iterates through each line of tokens in token_lines 
            (each line_tokens is a collection of tokens from a single line of text/code)"""
            for line_tokens in token_lines:
                # For each line, creates an empty list called tokens to store processed token information
                tokens = []
                # loops through each individual token within the current line
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        """If both conditions are met, creates a tuple containing the token's type and value 
                        (token.token_type, token.value) and add its tuple to the tokens list"""
                        tokens.append((token.token_type, token.value))
                # After processing all tokens in the current line, adds the collected tokens list to the all_tokens list
                all_tokens.append(tokens)
           
            
            # Flatten tokens and collect line/column info
            flat_tokens = []

            """It iterates through each line of tokens in token_lines 
            (each line_tokens is a collection of tokens from a single line of text/code)"""
            for line_tokens in token_lines:
                # loops through each individual token within the current line
                for token in line_tokens:
                    if hasattr(token, 'token_type'):
                        """If token have attribute token_type add its tuple to the tokens list"""
                        flat_tokens.append(token) 

            # initialize parser with argument <'program'> to specify the start of the reading of cfg
            parser = RoyalScriptParser('<program>') 
            # store the result and the error_message from the parser
            tree, error_message = parser.parse(flat_tokens)

            # if tree is true meaning successful yung pag parser
            if tree:
                # display the success message
                self.show_terminal_message("✅ Syntax analysis completed successfully!")
                self.show_terminal_message("No syntax errors found.")

                # then since walang syntax error try to build ast 
                try:

                    # initialize ast builder pass the all_tokens as input
                    ast_builder = RoyalScriptASTBuilder(all_tokens)
                    ast = ast_builder.build_ast()
                except Exception as e:
                    self.show_terminal_message(f"AST building not performed - {str(e)}")
            
            # if may syntax error during parsing then display the errors
            else:
                self.show_terminal_message("❌ Syntax errors detected. Check your code structure.")
                if error_message:
                    self.show_terminal_message(error_message)
                    return
                
            try:
                # Perform semantic analysis if walang lexical and syntax errors
                # initialize semantic analyzer and past the ast as input for semantic analysis
                semantic_analyzer = SemanticAnalyzer()
                semantic_errors = semantic_analyzer.analyze(ast)
                
                # if may semantic errors then display the erros the terminal
                if semantic_errors:
                    self.show_terminal_message("❌ Semantic errors detected:")
                    for error in semantic_errors:
                        self.show_terminal_message(f"  - {error}")

                # if wala display success message
                else:
                    self.show_terminal_message("✅ Semantic analysis completed successfully!")
                    self.show_terminal_message("No semantic errors found.")
                    
            except Exception as e:
                import traceback
                self.show_terminal_message(f"❌ Error during semantic analysis: {str(e)}")
                self.show_terminal_message(traceback.format_exc())
                
        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

    def analyze_syntax(self, event=None):
        """Analyze the code and display syntax analysis results"""
        # take the input and store it in code variable para gawing input sa lexical analysis 
        code = self.input_text.get("1.0", tk.END)
        # initialize lexical analyzer (imported lexer)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state=tk.DISABLED)
        all_tokens = []  # Store tokens (type and value) for additional analysis used for ast
        
        try:
            # for each tokens per line, store in token_line var, if wala empty
            token_lines = lexer.get_tokens() or []
            
            # check if may naencounte ne errors
            if lexer.errors:
                # if meron idisplay sa terminal
                self.show_terminal_message("❌ Lexical errors detected:")
                for error in lexer.errors:
                    self.show_terminal_message(f"  - {error}")

                for line_idx, line_tokens in enumerate(token_lines):
                    # processes each individual token within a line.
                    for token in line_tokens:
                        # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                        if isinstance(token, Token) and hasattr(token, 'token_type'):
                            # if meron then display the token value (lexeme) and token type
                            self.output_listbox.insert(tk.END, token.value)
                            self.token_listbox.insert(tk.END, token.token_type)

                return
            else:
                # if wala display yung success message
                self.show_terminal_message("✅ Lexical analysis completed successfully!")
                self.show_terminal_message("No lexical errors found.")
            
            # Display tokens in output_listbox and token_listbox (lexeme and token)
            """The outer loop (for line_idx, line_tokens in enumerate(token_lines)) 
            is going through each line in token_lines, getting both the index and the line's tokens."""
            for line_idx, line_tokens in enumerate(token_lines):
                # processes each individual token within a line.
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        # if meron then display the token value (lexeme) and token type
                        self.output_listbox.insert(tk.END, token.value)
                        self.token_listbox.insert(tk.END, token.token_type)

            # Prepare tokens for ast (ast input)
            """It iterates through each line of tokens in token_lines 
            (each line_tokens is a collection of tokens from a single line of text/code)"""
            for line_tokens in token_lines:
                # For each line, creates an empty list called tokens to store processed token information
                tokens = []
                # loops through each individual token within the current line
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        """If both conditions are met, creates a tuple containing the token's type and value 
                        (token.token_type, token.value) and add its tuple to the tokens list"""
                        tokens.append((token.token_type, token.value))
                # After processing all tokens in the current line, adds the collected tokens list to the all_tokens list
                all_tokens.append(tokens)
           
            
            # Flatten tokens and collect line/column info
            flat_tokens = []

            """It iterates through each line of tokens in token_lines 
            (each line_tokens is a collection of tokens from a single line of text/code)"""
            for line_tokens in token_lines:
                # loops through each individual token within the current line
                for token in line_tokens:
                    if hasattr(token, 'token_type'):
                        """If token have attribute token_type add its tuple to the tokens list"""
                        flat_tokens.append(token) 

            # initialize parser with argument <'program'> to specify the start of the reading of cfg
            parser = RoyalScriptParser('<program>') 
            # store the result and the error_message from the parser
            tree, error_message = parser.parse(flat_tokens)

            # if tree is true meaning successful yung pag parser
            if tree:
                # display the success message
                self.show_terminal_message("✅ Syntax analysis completed successfully!")
                self.show_terminal_message("No syntax errors found.")

                # then since walang syntax error try to build ast 
                try:

                    # initialize ast builder pass the all_tokens as input
                    ast_builder = RoyalScriptASTBuilder(all_tokens)
                    ast = ast_builder.build_ast()
                    self.show_terminal_message("\nAbstract Syntax Tree:")
                    ast_string = print_ast(ast)
                    self.show_terminal_message(ast_string)
                except Exception as e:
                    self.show_terminal_message(f"AST building not performed - {str(e)}")
            
            # if may syntax error during parsing then display the errors
            else:
                self.show_terminal_message("❌ Syntax errors detected. Check your code structure.")
                if error_message:
                    self.show_terminal_message(error_message)
                    return

        except Exception as e:
            import traceback
            self.show_terminal_message(f"❌ Error during syntax analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

    def analyze_lexical(self, event=None):
        """Analyze the code and display lexical analysis results"""
        # take the input and store it in code variable para gawing input sa lexical analysis 
        code = self.input_text.get("1.0", tk.END)
        # initialize lexical analyzer (imported lexer)
        lexer = RoyalScriptLexer(code)
        
        # Clear previous output
        self.output_listbox.delete(0, tk.END)
        self.token_listbox.delete(0, tk.END)
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state=tk.DISABLED)
        
        try:
            # for each tokens per line, store in token_line var, if wala empty
            token_lines = lexer.get_tokens() or []
            
            # check if may naencounter na errors
            if lexer.errors:
                # if meron idisplay sa terminal
                self.show_terminal_message("❌ Lexical errors detected:")
                for error in lexer.errors:
                    self.show_terminal_message(f"  - {error}")
                 # Display tokens in output_listbox and token_listbox (lexeme and token)
                """The outer loop (for line_idx, line_tokens in enumerate(token_lines)) 
                is going through each line in token_lines, getting both the index and the line's tokens."""
                for line_idx, line_tokens in enumerate(token_lines):
                    # processes each individual token within a line.
                    for token in line_tokens:
                        # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                        if isinstance(token, Token) and hasattr(token, 'token_type'):
                            # if meron then display the token value (lexeme) and token type
                            self.output_listbox.insert(tk.END, token.value)
                            self.token_listbox.insert(tk.END, token.token_type)
                return
            else:
                # if wala display yung success message
                self.show_terminal_message("✅ Lexical analysis completed successfully!")
                self.show_terminal_message("No lexical errors found.")
                
            # Display tokens in output_listbox and token_listbox (lexeme and token)
            """The outer loop (for line_idx, line_tokens in enumerate(token_lines)) 
            is going through each line in token_lines, getting both the index and the line's tokens."""
            for line_idx, line_tokens in enumerate(token_lines):
                # processes each individual token within a line.
                for token in line_tokens:
                    # check if the token is an instance of Token class (from lexical analyzer) & check if the token have an attribute called token_type
                    if isinstance(token, Token) and hasattr(token, 'token_type'):
                        # if meron then display the token value (lexeme) and token type
                        self.output_listbox.insert(tk.END, token.value)
                        self.token_listbox.insert(tk.END, token.token_type)
            
        # catch any errors if meron man
        except Exception as e:
            self.show_terminal_message(f"❌ Error during lexical analysis: {str(e)}")
            self.show_terminal_message(traceback.format_exc())

    def on_hover(self, event):
        """Handle hover effect for analyze button"""
        self.analyze_button.config(bg="#fcbad3")
        
    def on_leave(self, event):
        """Handle leave effect for analyze button"""
        self.analyze_button.config(bg="SystemButtonFace")
        
    def on_hover_syntax(self, event):
        """Handle hover effect for syntax button"""
        self.syntax_button.config(bg="#fcbad3")
        
    def on_leave_syntax(self, event):
        """Handle leave effect for syntax button"""
        self.syntax_button.config(bg="SystemButtonFace")
        
    def on_hover_semantic(self, event):
        """Handle hover effect for semantic button"""
        self.semantic_button.config(bg="#fcbad3")
        
    def on_leave_semantic(self, event):
        """Handle leave effect for semantic button"""
        self.semantic_button.config(bg="SystemButtonFace")
        
    def on_hover_run(self, event):
        """Handle hover effect for run button"""
        self.run_button_canvas.config(bg="#fcbad3")
        
    def on_leave_run(self, event):
        """Handle leave effect for run button"""
        self.run_button_canvas.config(bg="SystemButtonFace")


if __name__ == "__main__":
    app = RoyalScriptLexerGUI()
    app.mainloop()