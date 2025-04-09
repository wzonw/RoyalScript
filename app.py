import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import sys
import traceback

current_process = None

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from lexer2 import RoyalScriptLexer, Token
    from parser import RoyalScriptParser
    from ast_builder import RoyalScriptASTBuilder, ASTBuildingException
    from semantic import SemanticAnalyzer, SemanticError
    from coder import RoyalScriptToPythonTranslator
    from test_ast import print_ast
except ImportError as e:
    print(f"Error importing modules: {e}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_interactive', methods=['GET'])
def run_interactive():
    import subprocess

    output_file = "output.py"
    if not os.path.exists(output_file):
        return "output.py not found", 404

    def generate():
        global current_process
        try:
            current_process = subprocess.Popen(
                [sys.executable, "-u", output_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            line_buffer = ""
            while True:
                char = current_process.stdout.read(1)
                if not char:
                    break

                line_buffer += char

                if line_buffer.endswith(': ') or line_buffer.endswith('? ') or char == '\n':
                    yield f"data: {line_buffer.rstrip()}\n\n"
                    line_buffer = ""

            current_process.stdout.close()
            current_process = None
        except Exception as e:
            yield f"data: ❌ Server error: {str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/send_input', methods=['POST'])
def send_input():
    global current_process
    user_input = request.form.get('input', '')
    if current_process and current_process.stdin:
        current_process.stdin.write(user_input + '\n')
        current_process.stdin.flush()
    return '', 204

@app.route('/analyze_lexical', methods=['POST'])
def analyze_lexical():
    code = request.form.get('code', '')
    
    try:
        lexer = RoyalScriptLexer(code)
        token_lines = lexer.get_tokens() or []
        
        if not token_lines:
            return jsonify({
                'success': False,
                'message': 'Lexer Error: No tokens detected',
                'output': [],
                'tokens': []
            })
        
        # Process the tokens
        lexemes = []
        token_types = []
        all_tokens = []
        line_numbers = []
        
        for line_num, line_tokens in enumerate(token_lines, 1):
            tokens_for_line = []
            
            if not line_tokens:
                lexemes.append(" ")
                token_types.append(" ")
            else:
                for token in line_tokens:
                    if isinstance(token, Token):
                        lexemes.append(token.value)
                        
                        if hasattr(token, 'token_type'):
                            token_types.append(token.token_type)
                            tokens_for_line.append((token.token_type, token.value))
                            line_numbers.append(str(line_num))
            
            all_tokens.append(tokens_for_line)
        
        # Check for lexer errors
        errors = []
        if lexer.errors:
            for error in lexer.errors:
                errors.append(f"❌ Lexical Error: {error}")
            success = False
        else:
            errors.append("✅ Lexical Analysis Successful.")
            success = True
            
        return jsonify({
            'success': success,
            'message': '\n'.join(errors),
            'lexemes': lexemes,
            'tokens': token_types,
            'line_numbers': line_numbers,
            'all_tokens': all_tokens  # Save for subsequent steps
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Unexpected Error: {str(e)}\n{traceback.format_exc()}",
            'lexemes': [],
            'tokens': []
        })

@app.route('/analyze_syntax', methods=['POST'])
def analyze_syntax():
    code = request.form.get('code', '')
    
    try:
        # First perform lexical analysis
        lexer = RoyalScriptLexer(code)
        token_lines = lexer.get_tokens() or []
        
        if not token_lines:
            return jsonify({
                'success': False,
                'message': 'Lexer Error: No tokens detected',
                'lexemes': [],
                'tokens': []
            })
        
        # Process the tokens like in analyze_lexical
        lexemes = []
        token_types = []
        all_tokens = []
        line_numbers = []
        
        for line_num, line_tokens in enumerate(token_lines, 1):
            tokens_for_line = []
            
            if not line_tokens:
                lexemes.append(" ")
                token_types.append(" ")
            else:
                for token in line_tokens:
                    if isinstance(token, Token):
                        lexemes.append(token.value)
                        
                        if hasattr(token, 'token_type'):
                            token_types.append(token.token_type)
                            tokens_for_line.append((token.token_type, token.value))
                            line_numbers.append(str(line_num))
            
            all_tokens.append(tokens_for_line)
        
        # Initialize messages list
        messages = []
        
        # Check for lexer errors first
        if lexer.errors:
            for error in lexer.errors:
                messages.append(f"❌ Lexical Error: {error}")
            return jsonify({
                'success': False,
                'message': '\n'.join(messages),
                'lexemes': lexemes,
                'tokens': token_types,
                'line_numbers': line_numbers
            })
        
        messages.append("✅ Lexical Analysis Successful.")
        
        # Now run syntax analysis
        parser = RoyalScriptParser(all_tokens)
        try:
            syntax_result = parser.parse()
            
            if syntax_result:
                messages.append("✅ Syntax Analysis Successful!")
                
                try:
                    ast_builder = RoyalScriptASTBuilder(all_tokens)
                    ast = ast_builder.build_ast()
                    ast_string = print_ast_to_string(ast)
                    messages.append("✅ AST Building Successful!")
                    
                    return jsonify({
                        'success': True,
                        'message': '\n'.join(messages),
                        'lexemes': lexemes,
                        'tokens': token_types,
                        'line_numbers': line_numbers,
                        'ast': ast_string
                    })
                    
                except ASTBuildingException as e:
                    messages.append(f"❌ AST Building Failed: {e}")
                    return jsonify({
                        'success': False,
                        'message': '\n'.join(messages),
                        'lexemes': lexemes,
                        'tokens': token_types,
                        'line_numbers': line_numbers
                    })
                    
                except Exception as e:
                    messages.append(f"❌ Unexpected Error in AST Building: {str(e)}")
                    return jsonify({
                        'success': False,
                        'message': '\n'.join(messages),
                        'lexemes': lexemes,
                        'tokens': token_types,
                        'line_numbers': line_numbers
                    })
            else:
                messages.append("❌ Syntax Analysis Failed.")
                return jsonify({
                    'success': False,
                    'message': '\n'.join(messages),
                    'lexemes': lexemes,
                    'tokens': token_types,
                    'line_numbers': line_numbers
                })
                
        except SyntaxError as e:
            messages.append(f"❌ {str(e)}")
            return jsonify({
                'success': False,
                'message': '\n'.join(messages),
                'lexemes': lexemes,
                'tokens': token_types,
                'line_numbers': line_numbers
            })
            
        except Exception as e:
            messages.append(f"❌ Unexpected Error in Syntax Analysis: {str(e)}")
            return jsonify({
                'success': False,
                'message': '\n'.join(messages),
                'lexemes': lexemes,
                'tokens': token_types,
                'line_numbers': line_numbers
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Unexpected Error: {str(e)}\n{traceback.format_exc()}",
            'lexemes': [],
            'tokens': []
        })

@app.route('/analyze_semantic', methods=['POST'])
def analyze_semantic():
    code = request.form.get('code', '')
    try:
        lexer = RoyalScriptLexer(code)
        token_lines = lexer.get_tokens() or []

        if not token_lines:
            return jsonify({
                'success': False,
                'message': 'Lexer Error: No tokens detected',
                'lexemes': [],
                'tokens': []
            })

        lexemes = []
        token_types = []
        all_tokens = []
        line_numbers = []

        for line_num, line_tokens in enumerate(token_lines, 1):
            tokens_for_line = []
            if not line_tokens:
                lexemes.append(" ")
                token_types.append(" ")
            else:
                for token in line_tokens:
                    if isinstance(token, Token):
                        lexemes.append(token.value)
                        if hasattr(token, 'token_type'):
                            token_types.append(token.token_type)
                            tokens_for_line.append((token.token_type, token.value))
                            line_numbers.append(str(line_num))
            all_tokens.append(tokens_for_line)

        messages = []
        if lexer.errors:
            for error in lexer.errors:
                messages.append(f"❌ Lexical Error: {error}")
            return jsonify({
                'success': False,
                'message': '\n'.join(messages),
                'lexemes': lexemes,
                'tokens': token_types,
                'line_numbers': line_numbers
            })

        messages.append("✅ Lexical Analysis Successful.")

        parser = RoyalScriptParser(all_tokens)
        try:
            syntax_result = parser.parse()
            if syntax_result:
                messages.append("✅ Syntax Analysis Successful!")
                try:
                    ast_builder = RoyalScriptASTBuilder(all_tokens)
                    ast = ast_builder.build_ast()
                    messages.append("✅ AST Building Successful!")
                    semantic_analyzer = SemanticAnalyzer()
                    semantic_errors = semantic_analyzer.analyze(ast)

                    if semantic_errors:
                        messages.append("❌ Semantic Analysis Detected Errors:")
                        for error in semantic_errors:
                            messages.append(str(error))
                        return jsonify({
                            'success': False,
                            'message': '\n'.join(messages),
                            'lexemes': lexemes,
                            'tokens': token_types,
                            'line_numbers': line_numbers
                        })

                    messages.append("✅ Semantic Analysis Successful!")
                    translator = RoyalScriptToPythonTranslator()
                    python_code = translator.translate(ast)
                    output_file = "output.py"

                    if isinstance(python_code, list):
                        python_code = "\n".join(python_code)
                    if not python_code.endswith("\n"):
                        python_code += "\n"

                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(python_code)

                    messages.append("▶️ Ready to execute in terminal...")
                    return jsonify({
                        'success': True,
                        'message': '\n'.join(messages),
                        'lexemes': lexemes,
                        'tokens': token_types,
                        'line_numbers': line_numbers,
                        'python_code': python_code,
                        'ready_to_run': True
                    })
                except ASTBuildingException as e:
                    messages.append(f"❌ AST Building Failed: {e}")
                    return jsonify({
                        'success': False,
                        'message': '\n'.join(messages),
                        'lexemes': lexemes,
                        'tokens': token_types,
                        'line_numbers': line_numbers
                    })
            else:
                messages.append("❌ Syntax Analysis Failed.")
                return jsonify({
                    'success': False,
                    'message': '\n'.join(messages),
                    'lexemes': lexemes,
                    'tokens': token_types,
                    'line_numbers': line_numbers
                })
        except SyntaxError as e:
            messages.append(f"❌ {str(e)}")
            return jsonify({
                'success': False,
                'message': '\n'.join(messages),
                'lexemes': lexemes,
                'tokens': token_types,
                'line_numbers': line_numbers
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Unexpected Error: {str(e)}\n{traceback.format_exc()}",
            'lexemes': [],
            'tokens': []
        })

def print_ast_to_string(ast):
    from io import StringIO
    import sys

    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout

    print_ast(ast)

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
