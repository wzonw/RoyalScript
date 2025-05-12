import sys
import traceback
import re
import linecache
from io import StringIO

class SourceMap:
    """Maps Python line numbers to RoyalScript line numbers."""
    def __init__(self):
        self.py_to_royal = {}  # Python line number -> (RoyalScript filename, line number)
        self.royal_to_py = {}  # (RoyalScript filename, line number) -> Python line number

    def add_mapping(self, py_line, royal_file, royal_line):
        """Add a mapping from Python line to RoyalScript line."""
        self.py_to_royal[py_line] = (royal_file, royal_line)
        self.royal_to_py[(royal_file, royal_line)] = py_line

    def get_royal_location(self, py_line):
        """Get RoyalScript location for a Python line."""
        return self.py_to_royal.get(py_line, (None, None))

    def get_python_line(self, royal_file, royal_line):
        """Get Python line for a RoyalScript location."""
        return self.royal_to_py.get((royal_file, royal_line), None)

class RoyalScriptError:
    """Custom error class for RoyalScript errors."""
    
    # Mapping of Python error types to RoyalScript error types
    ERROR_TYPE_MAP = {
        'SyntaxError': 'RoyalSyntaxError',
        'NameError': 'UndeclaredIdentifierError',
        'TypeError': 'TypeMismatchError',
        'IndexError': 'ArrayBoundsError',
        'ZeroDivisionError': 'DivideByZeroError',
        'ValueError': 'ValueError',
        'AttributeError': 'AttributeError',
        'KeyError': 'KeyError',
        'RuntimeError': 'RuntimeError',
        'OverflowError': 'OverflowError',
        'ImportError': 'ImportError'
    }
    
    # Mapping of Python terms to RoyalScript terms
    TERM_MAP = {
        'list': 'array',
        'index out of range': 'array bounds exceeded',
        'not subscriptable': 'is not an array',
        'integer': 'treasures',
        'float': 'ocean',
        'string': 'scroll',
        'character': 'rose',
        'boolean': 'mirror',
        'None': 'phantom',
        'True': 'truth',
        'False': 'falsity',
        'int': 'treasures',
        'str': 'scroll',
        'bool': 'mirror',
        'list': 'array'
    }
    
    def __init__(self, original_error, source_map, original_code=None, royal_filename="royal_script.rs"):
        """
        Initialize with the Python error and source map.
        
        Args:
            original_error: The original Python exception
            source_map: SourceMap object mapping Python lines to RoyalScript lines
            original_code: The original RoyalScript code (if available)
            royal_filename: The filename of the original RoyalScript file
        """
        self.original_error = original_error
        self.source_map = source_map
        self.original_code = original_code
        self.royal_filename = royal_filename
        self.error_type = self._map_error_type()
        self.message = self._customize_message()
        self.traceback = self._translate_traceback()
    
    def _map_error_type(self):
        """Map Python error type to RoyalScript error type."""
        error_class = self.original_error.__class__.__name__
        
        for py_error, royal_error in self.ERROR_TYPE_MAP.items():
            if error_class == py_error:
                return royal_error
        
        # If no specific mapping exists, use a default prefix
        return f"Royal{error_class}"
    
    def _customize_message(self):
        """Customize the error message to use RoyalScript terminology."""
        msg = str(self.original_error)
        
        # Replace Python terms with RoyalScript terms
        for py_term, royal_term in self.TERM_MAP.items():
            # Use word boundaries to avoid partial replacements
            msg = re.sub(fr'\b{py_term}\b', royal_term, msg)
        
        # Additional message customizations based on error type
        error_class = self.original_error.__class__.__name__
        
        if error_class == 'NameError' and "name" in msg and "is not defined" in msg:
            # Extract the variable name
            match = re.search(r"name '(.+)' is not defined", msg)
            if match:
                var_name = match.group(1)
                return f"The identifier '{var_name}' has not been declared in this scope"
                
        elif error_class == 'IndexError' and "list index out of range" in msg:
            return "Array bounds exceeded"
            
        elif error_class == 'TypeError':
            # Customize type error messages
            if "unsupported operand type(s)" in msg:
                msg = msg.replace("unsupported operand type(s)", "incompatible types")
                
            if "object is not subscriptable" in msg:
                match = re.search(r"'(.+)' object is not subscriptable", msg)
                if match:
                    type_name = match.group(1)
                    royal_type = self.TERM_MAP.get(type_name, type_name)
                    return f"{royal_type} is not an array and cannot be indexed"
        
        return msg
    
    def _translate_traceback(self):
        """Translate Python traceback to reference RoyalScript source files and line numbers."""
        tb_entries = []
        tb = self.original_error.__traceback__
        
        while tb:
            frame = tb.tb_frame
            py_line = tb.tb_lineno
            py_file = frame.f_code.co_filename
            
            # Try to map this Python location to RoyalScript location
            royal_file, royal_line = self.source_map.get_royal_location(py_line)
            
            if royal_file and royal_line:
                # If we have original code, show the actual line
                code_line = ""
                if self.original_code:
                    lines = self.original_code.splitlines()
                    if 0 <= royal_line - 1 < len(lines):
                        code_line = lines[royal_line - 1].strip()
                        if code_line:
                            code_line = f"\n    | {code_line}"
                
                tb_entries.append(f"  at {royal_file}:{royal_line}{code_line}")
            else:
                # If no mapping exists but it's user code (not in standard lib)
                if "<" not in py_file:
                    line_content = linecache.getline(py_file, py_line).strip()
                    if line_content:
                        tb_entries.append(f"  at <internal>:{py_line}\n    | {line_content}")
            
            tb = tb.tb_next
        
        return "\n".join(tb_entries)
    
    def __str__(self):
        """Format the error as a string in RoyalScript style."""
        return f"RoyalScript {self.error_type}: {self.message}\n{self.traceback}"


class RoyalScriptExecutor:
    """Run translated Python code with RoyalScript error handling."""
    
    def __init__(self, source_map=None, original_code=None, royal_filename="royal_script.rs"):
        """
        Initialize with optional source map and original code.
        
        Args:
            source_map: SourceMap object mapping Python lines to RoyalScript lines
            original_code: The original RoyalScript code (if available)
            royal_filename: The filename of the original RoyalScript file
        """
        self.source_map = source_map or SourceMap()
        self.original_code = original_code
        self.royal_filename = royal_filename
        self.stdout_buffer = None
        self.stderr_buffer = None
        
    def add_line_mapping(self, py_line, royal_line):
        """Add a mapping from Python line to RoyalScript line."""
        self.source_map.add_mapping(py_line, self.royal_filename, royal_line)
    
    def execute(self, python_code, global_vars=None):
        """
        Execute the translated Python code and catch any errors.
        
        Args:
            python_code: The translated Python code to execute
            global_vars: Optional dictionary of global variables
        
        Returns:
            tuple: (success, output, error)
                success: Boolean indicating if execution was successful
                output: Standard output from the execution
                error: Error object if execution failed, None otherwise
        """
        # Save original stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Redirect stdout and stderr to capture output
        self.stdout_buffer = StringIO()
        self.stderr_buffer = StringIO()
        sys.stdout = self.stdout_buffer
        sys.stderr = self.stderr_buffer
        
        # Initialize result variables
        success = False
        output = ""
        error = None
        
        try:
            # Create a namespace for execution
            namespace = global_vars or {}
            
            # Execute the Python code
            exec(python_code, namespace)
            success = True
        except Exception as e:
            # Translate the Python error to RoyalScript error
            error = RoyalScriptError(e, self.source_map, self.original_code, self.royal_filename)
        finally:
            # Restore stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            # Get captured output
            output = self.stdout_buffer.getvalue()
            self.stdout_buffer.close()
            self.stderr_buffer.close()
        
        return success, output, error


class RoyalScriptCompiler:
    """Compiles RoyalScript to Python and manages execution with proper error handling."""
    
    def __init__(self, translator_class):
        """
        Initialize with the translator class.
        
        Args:
            translator_class: The RoyalScriptToPythonTranslator class
        """
        self.translator_class = translator_class
        self.source_map = SourceMap()
        self.original_code = None
        self.python_code = None
        
    def compile(self, royal_code, filename="royal_script.rs", global_variable_types=None):
        """
        Compile RoyalScript code to Python and build a source map.
        
        Args:
            royal_code: The RoyalScript source code
            filename: The filename for the RoyalScript code
            global_variable_types: Dictionary of global variable types
        
        Returns:
            str: The translated Python code
        """
        self.original_code = royal_code
        
        # Create a translator instance
        translator = self.translator_class(global_variable_types)
        
        # Parse the RoyalScript code
        # Note: This assumes your parser returns an AST
        # You'll need to adapt this to your actual parsing process
        ast = self._parse_royal_script(royal_code)
        
        # Build the source map during translation
        # Note: This assumes your translator can track line mappings
        # You'll need to adapt this to your actual translation process
        self.python_code = translator.translate(ast)
        
        # For demonstration purposes, we'll create a simple source map
        # In a real implementation, you would build this during parsing/translation
        self._build_demo_source_map(royal_code, self.python_code)
        
        return self.python_code
    
    def _parse_royal_script(self, royal_code):
        """
        Parse RoyalScript code to AST.
        
        Note: This is a placeholder method. You should replace this with your actual parser.
        """
        # Placeholder for the actual parsing logic
        # In reality, you would call your parser here
        return {'type': 'program', 'body': []}  # Placeholder AST
    
    def _build_demo_source_map(self, royal_code, python_code):
        """
        Build a simple source map from RoyalScript to Python.
        
        Note: This is a placeholder method for demonstration. In a real implementation,
        you would build this map during the parsing/translation process.
        """
        royal_lines = royal_code.splitlines()
        python_lines = python_code.splitlines()
        
        # A very simple mapping - just map line to line
        # In reality, the mapping would be more complex
        for i in range(min(len(royal_lines), len(python_lines))):
            # +1 because line numbers are 1-based
            self.source_map.add_mapping(i+1, "royal_script.rs", i+1)
    
    def run(self, global_vars=None):
        """
        Run the compiled Python code with RoyalScript error handling.
        
        Args:
            global_vars: Optional dictionary of global variables
        
        Returns:
            tuple: (success, output, error)
        """
        if not self.python_code:
            return False, "", "No compiled code to run"
        
        executor = RoyalScriptExecutor(self.source_map, self.original_code)
        return executor.execute(self.python_code, global_vars)


def integrate_with_translator(translator_class):
    """
    Modify the translator class to build a source map during translation.
    
    Args:
        translator_class: The RoyalScriptToPythonTranslator class
        
    Returns:
        translator_class: The modified translator class
    """
    # Store the original translate method
    original_translate = translator_class.translate
    
    def new_translate(self, node):
        """Wrapper for translate method that builds source map."""
        # Initialize source map if not already present
        if not hasattr(self, 'source_map'):
            self.source_map = SourceMap()
            self.royal_line_map = {}
        
        # Call original translate method
        result = original_translate(self, node)
        
        # Extract line numbers from the node if available
        if hasattr(node, 'line'):
            python_line = result.count('\n') + 1
            royal_line = node.line
            self.source_map.add_mapping(python_line, "royal_script.rs", royal_line)
        
        return result
    
    # Replace the translate method
    translator_class.translate = new_translate
    
    return translator_class
