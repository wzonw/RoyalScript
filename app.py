from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os
import threading
import queue
import time
import json
from io import StringIO

# Import your existing components
# Update these imports to match your actual file structure
from lexer2 import RoyalScriptLexer, Token
from parser import RoyalScriptParser
from ast_builder import RoyalScriptASTBuilder, ASTBuildingException
from semantic import SemanticAnalyzer, SemanticError
from coder import RoyalScriptToPythonTranslator
from test_ast import print_ast

app = Flask(__name__)

# Global dictionary to store active processes
active_processes = {}

class ProcessHandler:
    """Class to handle running Python subprocesses"""
    def __init__(self, session_id):
        self.session_id = session_id
        self.process = None
        self.output_queue = queue.Queue()
        self.is_waiting_for_input = False
        self.is_running = False
        
    def start_process(self, python_code):
        """Start a subprocess to run the Python code"""
        # Terminate any existing process first
        self.terminate_process()
        
        # Add special wrapper code to make input detection more reliable
        modified_code = """
import sys
import builtins

# Override the built-in input function to add markers
original_input = builtins.input
def marked_input(prompt=""):
    # Print a special marker that our process handler will detect
    print("INPUT_REQUIRED_MARKER", flush=True)
    # Print the actual prompt
    if prompt:
        print(prompt, end="", flush=True)
    # Get the input using the original function
    return original_input()

# Replace the built-in input function with our marked version
builtins.input = marked_input

# Original code starts here
{}
""".format(python_code)
        
        # Save the code to a temporary file
        filename = f"output_{self.session_id}.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(modified_code)
        
        # Start the process with unbuffered I/O
        self.process = subprocess.Popen(
            ["python", "-u", filename],  # -u ensures unbuffered output
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            text=True
        )
        
        self.is_running = True
        
        # Start threads to monitor output
        self.stdout_thread = threading.Thread(target=self._read_output, args=(self.process.stdout, "stdout"))
        self.stderr_thread = threading.Thread(target=self._read_output, args=(self.process.stderr, "stderr"))
        
        self.stdout_thread.daemon = True
        self.stderr_thread.daemon = True
        
        self.stdout_thread.start()
        self.stderr_thread.start()
        
    def _read_output(self, pipe, pipe_name):
        """Read output from the process pipe"""
        while self.is_running and self.process and self.process.poll() is None:
            try:
                line = pipe.readline()
                if not line:
                    time.sleep(0.1)  # Avoid busy waiting
                    continue
                    
                # Check for our special input marker
                if "INPUT_REQUIRED_MARKER" in line:
                    self.is_waiting_for_input = True
                    self.output_queue.put({
                        "type": "input_prompt",
                        "content": "Input required:"
                    })
                    continue  # Skip the marker line itself
                
                # For regular output
                self.output_queue.put({
                    "type": "output" if pipe_name == "stdout" else "error",
                    "content": line.rstrip()
                })
            except Exception as e:
                self.output_queue.put({
                    "type": "error",
                    "content": f"Error reading output: {str(e)}"
                })
                
        # If process has finished, put a termination message
        if not self.is_running or (self.process and self.process.poll() is not None):
            if self.is_waiting_for_input:
                # Process ended while waiting for input - this is unexpected
                self.output_queue.put({
                    "type": "error",
                    "content": "[Process terminated unexpectedly while waiting for input]"
                })
            else:
                self.output_queue.put({
                    "type": "system",
                    "content": "[Process completed]"
                })
            self.is_running = False
            
    def send_input(self, input_text):
        """Send input to the process"""
        if self.process and self.process.poll() is None:
            try:
                # Add the input to the queue so it's shown in the terminal
                self.output_queue.put({
                    "type": "user_input",
                    "content": input_text
                })
                
                # Send to process with newline
                self.process.stdin.write(input_text + "\n")
                self.process.stdin.flush()
                
                # Reset input flag
                self.is_waiting_for_input = False
                return True
            except Exception as e:
                self.output_queue.put({
                    "type": "error",
                    "content": f"Error sending input: {str(e)}"
                })
                return False
        return False
        
    def get_output(self):
        """Get accumulated output from the queue"""
        output = []
        try:
            while not self.output_queue.empty():
                output.append(self.output_queue.get_nowait())
        except:
            pass  # Handle any queue errors
        return output
        
    def terminate_process(self):
        """Terminate the process if it's running"""
        if self.process and self.process.poll() is None:
            try:
                self.is_running = False
                self.is_waiting_for_input = False
                
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
                    
                # Clean up any temporary files
                filename = f"output_{self.session_id}.py"
                if os.path.exists(filename):
                    try:
                        os.remove(filename)
                    except:
                        pass
                        
                return True
            except Exception as e:
                print(f"Error terminating process: {str(e)}")
                return False
        return True

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze_lexical', methods=['POST'])
def analyze_lexical():
    """Handle lexical analysis request"""
    try:
        code = request.json.get('code', '')
        lexer = RoyalScriptLexer(code)
        
        # Perform lexical analysis
        token_lines = lexer.get_tokens() or []
        
        # Process results
        result = {
            "success": True,
            "tokens": [],
            "errors": lexer.errors,
            "message": "Lexical analysis completed successfully!" if not lexer.errors else "Lexical errors detected"
        }
        
        # Format tokens for display
        for line_idx, line_tokens in enumerate(token_lines):
            line_result = []
            for token in line_tokens:
                if isinstance(token, Token) and hasattr(token, 'token_type'):
                    line_result.append({
                        "line": line_idx + 1,
                        "value": token.value,
                        "type": token.token_type
                    })
            result["tokens"].extend(line_result)
        
        return jsonify(result)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return jsonify({
            "success": False,
            "errors": [str(e)],
            "traceback": error_traceback,
            "message": f"Error during lexical analysis: {str(e)}"
        })

@app.route('/analyze_syntax', methods=['POST'])
def analyze_syntax():
    """Handle syntax analysis request"""
    try:
        code = request.json.get('code', '')
        lexer = RoyalScriptLexer(code)
        
        # First perform lexical analysis
        token_lines = lexer.get_tokens() or []
        
        # Check for lexical errors
        if lexer.errors:
            return jsonify({
                "success": False,
                "stage": "lexical",
                "errors": lexer.errors,
                "message": "Lexical errors detected"
            })
        
        # Process tokens for parser
        all_tokens = []
        formatted_tokens = []
        
        for line_idx, line_tokens in enumerate(token_lines):
            line_result = []
            tokens_for_line = []
            
            for token in line_tokens:
                if isinstance(token, Token) and hasattr(token, 'token_type'):
                    formatted_tokens.append({
                        "line": line_idx + 1,
                        "value": token.value,
                        "type": token.token_type
                    })
                    tokens_for_line.append((token.token_type, token.value))
            
            all_tokens.append(tokens_for_line)
        
        # Run syntax analysis
        parser = RoyalScriptParser(all_tokens)
        syntax_success = parser.parse()
        
        if syntax_success:
            try:
                # If syntax is valid, try to build AST
                ast_builder = RoyalScriptASTBuilder(all_tokens)
                ast = ast_builder.build_ast()
                ast_string = print_ast(ast)
                
                return jsonify({
                    "success": True,
                    "stage": "syntax",
                    "tokens": formatted_tokens,
                    "ast": ast_string,
                    "message": "Syntax analysis completed successfully!"
                })
                
            except Exception as e:
                return jsonify({
                    "success": True,
                    "stage": "syntax",
                    "tokens": formatted_tokens,
                    "message": "Syntax analysis completed successfully!",
                    "ast_error": str(e)
                })
        else:
            return jsonify({
                "success": False,
                "stage": "syntax",
                "tokens": formatted_tokens,
                "message": "Syntax errors detected. Check your code structure."
            })
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return jsonify({
            "success": False,
            "errors": [str(e)],
            "traceback": error_traceback,
            "message": f"Error during syntax analysis: {str(e)}"
        })

@app.route('/analyze_semantic', methods=['POST'])
def analyze_semantic():
    """Handle semantic analysis request"""
    try:
        code = request.json.get('code', '')
        lexer = RoyalScriptLexer(code)
        
        # First perform lexical analysis
        token_lines = lexer.get_tokens() or []
        
        # Check for lexical errors
        if lexer.errors:
            return jsonify({
                "success": False,
                "stage": "lexical",
                "errors": lexer.errors,
                "message": "Lexical errors detected"
            })
            
        # Process tokens for parser and display
        all_tokens = []
        formatted_tokens = []
        
        for line_idx, line_tokens in enumerate(token_lines):
            line_result = []
            tokens_for_line = []
            
            for token in line_tokens:
                if isinstance(token, Token) and hasattr(token, 'token_type'):
                    formatted_tokens.append({
                        "line": line_idx + 1,
                        "value": token.value,
                        "type": token.token_type
                    })
                    tokens_for_line.append((token.token_type, token.value))
            
            all_tokens.append(tokens_for_line)
        
        # Run syntax analysis
        parser = RoyalScriptParser(all_tokens)
        syntax_success = parser.parse()
        
        if not syntax_success:
            return jsonify({
                "success": False,
                "stage": "syntax",
                "tokens": formatted_tokens,
                "message": "Syntax errors detected. Cannot proceed to semantic analysis."
            })
        
        # Try to build AST
        try:
            ast_builder = RoyalScriptASTBuilder(all_tokens)
            ast = ast_builder.build_ast()
            
            # Perform semantic analysis
            semantic_analyzer = SemanticAnalyzer()
            semantic_errors = semantic_analyzer.analyze(ast)
            
            if semantic_errors:
                return jsonify({
                    "success": False,
                    "stage": "semantic",
                    "tokens": formatted_tokens,
                    "errors": semantic_errors,
                    "message": "Semantic errors detected"
                })
            else:
                ast_string = print_ast(ast)
                return jsonify({
                    "success": True,
                    "stage": "semantic",
                    "tokens": formatted_tokens,
                    "ast": ast_string,
                    "message": "Semantic analysis completed successfully!"
                })
                
        except ASTBuildingException as e:
            return jsonify({
                "success": False,
                "stage": "ast",
                "tokens": formatted_tokens,
                "errors": [str(e)],
                "message": f"AST Building Error: {str(e)}"
            })
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return jsonify({
            "success": False,
            "errors": [str(e)],
            "traceback": error_traceback,
            "message": f"Error during semantic analysis: {str(e)}"
        })

@app.route('/run_code', methods=['POST'])
def run_code():
    """Compile and run the RoyalScript code"""
    try:
        code = request.json.get('code', '')
        session_id = request.json.get('session_id', 'default')
        
        # First perform lexical analysis
        lexer = RoyalScriptLexer(code)
        token_lines = lexer.get_tokens() or []
        
        # Check for lexical errors
        if lexer.errors:
            return jsonify({
                "success": False,
                "stage": "lexical",
                "errors": lexer.errors,
                "message": "Lexical errors detected"
            })
            
        # Process tokens for parser
        all_tokens = []
        for line_tokens in token_lines:
            tokens = []
            for token in line_tokens:
                if isinstance(token, Token) and hasattr(token, 'token_type'):
                    tokens.append((token.token_type, token.value))
            all_tokens.append(tokens)
        
        # Run syntax analysis
        parser = RoyalScriptParser(all_tokens)
        if not parser.parse():
            return jsonify({
                "success": False,
                "stage": "syntax",
                "message": "Syntax errors detected. Please fix before running."
            })
            
        # Build AST
        try:
            ast_builder = RoyalScriptASTBuilder(all_tokens)
            ast = ast_builder.build_ast()
            
            # Run semantic analysis
            semantic_analyzer = SemanticAnalyzer()
            semantic_errors = semantic_analyzer.analyze(ast)
            
            if semantic_errors:
                return jsonify({
                    "success": False,
                    "stage": "semantic",
                    "errors": semantic_errors,
                    "message": "Semantic errors detected. Please fix before running."
                })
                
            # Translate to Python
            translator = RoyalScriptToPythonTranslator()
            python_code = translator.translate(ast)
            
            # Ensure python_code is a string with newlines
            if isinstance(python_code, list):
                python_code = "\n".join(python_code)
                
            # Create a process handler for this session
            if session_id not in active_processes:
                active_processes[session_id] = ProcessHandler(session_id)
                
            # Start running the code
            active_processes[session_id].start_process(python_code)
            
            # Return initial success
            return jsonify({
                "success": True,
                "message": "Code is running",
                "python_code": python_code
            })
                
        except ASTBuildingException as e:
            return jsonify({
                "success": False,
                "stage": "ast",
                "errors": [str(e)],
                "message": f"AST Building Error: {str(e)}"
            })
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        return jsonify({
            "success": False,
            "errors": [str(e)],
            "traceback": error_traceback,
            "message": f"Error during code execution: {str(e)}"
        })

@app.route('/process_output', methods=['POST'])
def process_output():
    """Get output from the running process"""
    session_id = request.json.get('session_id', 'default')
    
    if session_id in active_processes:
        handler = active_processes[session_id]
        output = handler.get_output()
        
        return jsonify({
            "output": output,
            "waiting_for_input": handler.is_waiting_for_input,
            "is_running": handler.is_running
        })
    else:
        return jsonify({
            "output": [],
            "waiting_for_input": False,
            "is_running": False
        })

@app.route('/send_input', methods=['POST'])
def send_input():
    """Send input to the running process"""
    session_id = request.json.get('session_id', 'default')
    input_text = request.json.get('input', '')
    
    if session_id in active_processes:
        handler = active_processes[session_id]
        success = handler.send_input(input_text)
        
        return jsonify({
            "success": success,
            "waiting_for_input": handler.is_waiting_for_input,
            "is_running": handler.is_running
        })
    else:
        return jsonify({
            "success": False,
            "message": "No active process found for this session"
        })

@app.route('/terminate_process', methods=['POST'])
def terminate_process():
    """Terminate the running process"""
    session_id = request.json.get('session_id', 'default')
    
    if session_id in active_processes:
        handler = active_processes[session_id]
        success = handler.terminate_process()
        
        return jsonify({
            "success": success,
            "message": "Process terminated successfully" if success else "Failed to terminate process"
        })
    else:
        return jsonify({
            "success": True,
            "message": "No active process found for this session"
        })

@app.route('/generate_session_id', methods=['GET'])
def generate_session_id():
    """Generate a unique session ID for the client"""
    import uuid
    session_id = str(uuid.uuid4())
    return jsonify({"session_id": session_id})

if __name__ == '__main__':
    app.run(debug=True)