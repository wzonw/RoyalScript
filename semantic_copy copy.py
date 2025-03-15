from semantic_functions import *


class RoyalScriptSemanticAnalyzer:
    def __init__(self, statements):
        self.statements = statements
        self.errors = []

        self.dynasty_id = {
            "treasures": set(),  # use a set to store identifiers
            "ocean": set(),
            "scroll": set(),
            "rose": set(),
            "mirror": set()
        }

        self.other_id = {
            "treasures": set(),
            "ocean": set(),
            "scroll": set(),
            "rose": set(),
            "mirror": set(),
            "chamber": set()
        }


        self.dynasty_array_id = {
            "treasures": set(),  # For integers (constants)
            "ocean": set(),      # For floating points (constants)
            "scroll": set(),     # For strings (constants)
            "rose": set(),       # For char (constants)
            "mirror": set()     # For booleans (constants)
        }

        self.other_array_id = {
            "treasures": set(),  # For integers (variables)
            "ocean": set(),
            "scroll": set(),
            "rose": set(),
            "mirror": set(),
            # "chamber": {}     # For functions with no return value
        }

        #array dimensions
        self.one_dim= {} 
        self.two_dim= {} 
        # Add dictionaries to store values
        self.dynasty_values = {}

        self.other_values = {}

        self.dynasty_array_values = {}

        self.other_array_values = {}

        # Pointer variables for traversing tokens in the current statement
        self.current_statement = []
        self.current_token_idx = 0
        self.current_statement_idx = 0
        self.current_token = None
        

    # ------------------------------------------------------------------
    # Pointer / Utility Methods
    # ------------------------------------------------------------------

    def current(self):
        """Return the current token tuple or None if at the end of the statement."""
        if self.current_token_idx < len(self.current_statement):
            token = self.current_statement[self.current_token_idx]
            print(f"[DEBUG] current() at index {self.current_token_idx}: {token}")
            return token
        print(f"[DEBUG] current() at index {self.current_token_idx}: None")
        return None

    def advance(self):
        """Advance to the next token in the current statement or to the next statement if needed."""
        self.current_token_idx += 1

        if self.current_token_idx < len(self.current_statement):
            self.current_token = self.current_statement[self.current_token_idx]
            print(f"[DEBUG] advance() => {self.current_token}")
            return self.current_token

        # If we reached the end of the current statement, we should return None
        # but NOT automatically move to the next statement
        # The main analyze loop will handle moving to the next statement
        print(f"[DEBUG] advance() => end of current statement")
        self.current_token = None
        return None

    def peek(self, offset=1):
        """Return the token at current_token_idx + offset without advancing the pointer."""
        idx = self.current_token_idx + offset
        if idx < len(self.current_statement):
            token = self.current_statement[idx]
            print(f"[DEBUG] peek({offset}) at index {idx}: {token}")
            return token
        print(f"[DEBUG] peek({offset}) out of range.")
        return None

    def filter_special_tokens(self, tokens):
        """Remove crown~, reign~, and EOF tokens from the token list."""
        filtered_tokens = []
        i = 0
        
        while i < len(tokens):
            current_token = tokens[i]
            
            # Skip crown~ pattern
            if (i + 1 < len(tokens) and 
                isinstance(current_token, tuple) and len(current_token) >= 2 and 
                current_token[0] == "crown" and current_token[1] == "crown" and
                isinstance(tokens[i+1], tuple) and tokens[i+1][0] == "~"):
                i += 2
                continue
                
            # Skip reign~ pattern
            if (i + 1 < len(tokens) and 
                isinstance(current_token, tuple) and len(current_token) >= 2 and 
                current_token[0] == "reign" and current_token[1] == "reign" and
                isinstance(tokens[i+1], tuple) and tokens[i+1][0] == "~"):
                i += 2
                continue
                
            # Skip EOF token
            if isinstance(current_token, tuple) and current_token[0] == "EOF":
                i += 1
                continue
                
            filtered_tokens.append(current_token)
            i += 1
            
        return filtered_tokens

    def setup_statement(self, statement_tokens):
        """Process a statement, removing special tokens and setting up pointers."""
        # Filter out special tokens
        filtered_tokens = self.filter_special_tokens(statement_tokens)
        
        # Set up pointer variables for this statement
        self.current_statement = filtered_tokens
        self.current_token_idx = 0
        self.current_token = filtered_tokens[0] if filtered_tokens else None
        
        return len(filtered_tokens) > 0

    # ------------------------------------------------------------------
    # Main Analysis Method
    # ------------------------------------------------------------------

    def analyze(self):
        """Perform semantic analysis on each statement in self.statements."""
        print("[DEBUG] Starting semantic analysis...")

        # We iterate over each statement in a loop
        self.current_statement_idx = 0
        while self.current_statement_idx < len(self.statements):
            statement = self.statements[self.current_statement_idx]
            
            if not statement:
                # Skip empty statements
                self.current_statement_idx += 1
                continue
                
            # Extract the statement type from the first token
            statement_type = statement[0]
            statement_type_str = statement_type[0] if isinstance(statement_type, tuple) else statement_type
            
            # Set up the statement for processing (skip the statement type)
            if self.setup_statement(statement[1:]):
                print(f"[DEBUG] Analyzing statement {self.current_statement_idx} with label '{statement_type_str}'")
                
                # Dispatch to the appropriate checker based on statement type
                if statement_type_str == "VARIABLE_DECLARATION":
                    self.check_variable_declaration()
                elif statement_type_str == "ARRAY_DECLARATION":
                    self.check_array_declaration()
                elif statement_type_str == "ASSIGNMENT_EXP":
                    self.check_assignment()
                elif statement_type_str == "FUNC_CALL":
                    self.check_function_call()
                elif statement_type_str == "IF_STATEMENT":
                    self.check_if_statement()
                elif statement_type_str == "FOR_LOOP":
                    self.check_for_loop()
                elif statement_type_str == "WHILE_STATEMENT":
                    self.check_while_statement()
                else:
                    err = f"Unknown statement type: {statement_type_str}"
                    print(f"[DEBUG] {err}")
                    self.errors.append(err)
            
            # Move on to the next statement
            self.current_statement_idx += 1
            print(f"[DEBUG] Moving to next statement. Current index: {self.current_statement_idx}")

        print("Dynasty Name:")
        for dtype, id_dict in self.dynasty_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        print("Other Name:")
        for dtype, id_dict in self.other_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        print("Dynasty Array Name:")
        for dtype, id_dict in self.dynasty_array_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        print("Other Array Name:")
        for dtype, id_dict in self.other_array_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        print("1D ARRAY CONTENTS:")
        for array_name, elements in self.one_dim.items():
            print(f"  {array_name}: {elements}")

        print("2D ARRAY CONTENTS:")
        for array_name, rows in self.two_dim.items():
            print(f"  {array_name}:")
            for row_index, row in enumerate(rows):
                print(f"    Row {row_index}: {row}")

        print("Dynasty VALUES:")
        for (dtype, var_name), value in self.dynasty_values.items():
            print(f"  ({dtype}, {var_name}): {value} (Type: {type(value).__name__})")

        print("Other VALUES:")
        for (dtype, var_name), value in self.other_values.items():
            print(f"  ({dtype}, {var_name}): {value} (Type: {type(value).__name__})")

        # After processing all statements, report errors
        if self.errors:
            print(f"[DEBUG] Semantic analysis completed with errors: {self.errors}")
        else:
            print("[DEBUG] Semantic analysis completed with no errors.")

        return not self.errors

    # ------------------------------------------------------------------
    # Checker Methods
    # ------------------------------------------------------------------

    def check_variable_declaration(self):
        """Check a variable declaration statement for semantic correctness."""
        print("[DEBUG] check_variable_declaration()")
        
        # Check for dynasty/variable keyword
        token = self.current()
        self.datatype = None
        self.isDynasty = False
        self.name = None

        #constant 
        if token[0] == 'dynasty':
            self.isDynasty = True
            self.advance()
            token = self.current()
            if token[0] in ['treasures', 'ocean', 'scroll', 'rose', 'mirror']:
                self.datatype = token[0]
                self.advance()
        
        #variables
        elif token[0] in ['treasures', 'ocean', 'scroll', 'rose', 'mirror']:
            self.isDynasty = False
            self.datatype = token[0]
            self.advance()

        
        token = self.current()
        # check if the name exist
        self.check_if_exist(token[1])

        peeked_token = self.peek()
        #check if may initialization if wala default val then record yung name
        if peeked_token:
            self.check_var_init(peeked_token[0], token[1], self.datatype, self.isDynasty)
        
        self.name = token[1]
        self.advance()
        token = self.current()
        if token[0] == '=':
            self.init(self.datatype, self.name, self.isDynasty)
        
        elif token[0] == ',':
            self.var_more(self.datatype, self.isDynasty)
        
        elif token[0] == '~':
            return
    
    def init(self, datatype, name, isDynasty):
        print("this is data=tye", datatype)
        self.advance()
        token = self.current()
        self.current_datatype = token[0]
        is_valid, error_message= self.is_value_compatible_with_type(token[1], datatype, token[0], name, isDynasty)

        if not is_valid:
            self.errors.append(error_message)
            return
        
        print(token[1], name, "----------------------------------")
        
        if self.current_datatype != "identifier" and self.current_datatype != "lengthof":
            if isDynasty:
                self.dynasty_values[(datatype, name)] = token[1]
                
            else:
                self.other_values[(datatype, name)] = token[1]

        self.advance()
        token = self.current()
        if token[0] == ',':
            self.var_more(datatype, isDynasty)
        
        elif token[0] == '~':
            return
    
    def var_more(self, datatype, isDynasty):
        self.advance()
        token = self.current()
        self.name = None

        # check if the name exist
        self.check_if_exist(token[1])

        peeked_token = self.peek()
        #check if may initialization if wala default val then record yung name
        if peeked_token:
            self.check_var_init(peeked_token[0], token[1], datatype, isDynasty)
        
        self.name = token[1]
        self.advance()
        token = self.current()
        if token[0] == '=':
            self.init(datatype, self.name, isDynasty)
        
        elif token[0] == ',':
            self.var_more(datatype, isDynasty)
        
        elif token[0] == '~':
            return
    
    # Placeholder for other checker methods
    #--------------------------------------------------------------------------------
    # ARRAY DECLARATION
    #--------------------------------------------------------------------------------

    def check_array_declaration(self):
        """Check a variable declaration statement for semantic correctness."""
        print("[DEBUG] check_array_declaration()")

        # Check for dynasty/variable keyword
        token = self.current()
        self.datatype = None
        self.isDynasty = False
        self.row = None
        self.name = None

        # 1) Check if it's 'dynasty' or a normal variable
        if token[0] == 'dynasty':
            self.isDynasty = True
            self.advance()
            token = self.current()
            if token[0] in ['treasures', 'ocean', 'scroll', 'rose', 'mirror']:
                self.datatype = token[0]
                self.advance()
        elif token[0] in ['treasures', 'ocean', 'scroll', 'rose', 'mirror']:
            self.isDynasty = False
            self.datatype = token[0]
            self.advance()
        else:
            self.errors.append(f"Invalid data type '{token[0]}' in array declaration.")
            return

        # 2) Get the identifier name, check if it's already declared
        token = self.current()
        if (any(token[1] in s for s in self.dynasty_id.values()) or 
            any(token[1] in s for s in self.other_id.values()) or 
            any(token[1] in s for s in self.other_array_id.values()) or 
            any(token[1] in s for s in self.dynasty_array_id.values())):
            self.errors.append(f"{token[1]} is already declared")
            return
        else:
            # Insert into the correct "array" table
            if self.isDynasty:
                # Add the identifier to the set for the given data type.
                self.dynasty_array_id[self.datatype].add(token[1])
                # Store its associated value separately, if needed.
                self.dynasty_array_values[(self.datatype, token[1])] = self.dynasty_dval
            else:
                self.other_array_id[self.datatype].add(token[1])
                self.other_array_values[(self.datatype, token[1])] = self.other_dval
            self.name = token[1]
            self.advance()


        # 3) Check for the first '[' dimension
        token = self.current()
        if token and token[0] == '[':
            self.advance()  # skip '['
            size_token = self.current()
            try:
                row_size = int(size_token[1])
                if row_size <= 0:
                    self.errors.append(f"Invalid array size {row_size}")
                    return
            except ValueError:
                self.errors.append(f"Array size '{size_token[1]}' is not an integer.")
                return

            self.row = row_size
            self.advance()  # move past the size token

            # We expect a ']'
            token = self.current()
            if token and token[0] == ']':
                self.advance()  # skip ']'
            else:
                self.errors.append("Expected ']' after first dimension.")
                return
        else:
            # If your language requires at least one dimension, raise an error.
            # Or if you allow single variable (no array?), handle that logic here.
            self.errors.append("Expected '[' for array dimension.")
            return

        # 4) Check if there's a second dimension, or an initializer, or more...
        token = self.current()
        if token and token[0] == '[':
            # We have a second dimension => 2D array
            self.column(self.datatype, self.name, self.isDynasty, self.row)
        elif token and token[0] == '=':
            # 1D array with initializer
            self.one_dim[self.name] = [self.row]  # store [4] for example
            self.array_init(self.datatype, self.name, self.isDynasty)
        elif token and token[0] == ',':
            # Another array declared in the same statement
            self.one_dim[self.name] = [self.row]
            self.array_more(self.datatype, self.isDynasty)
        elif token and token[0] == '~':
            # End of statement
            self.one_dim[self.name] = [self.row]
            return
        else:
            self.errors.append(f"Unexpected token '{token[0]}' after dimension.")


    def column(self, datatype, name, isDynasty, row):
        """
        Parse the second dimension for a 2D array and store (row, col) in self.two_dim[name].
        Then proceed to initializer or next steps.
        """
        self.advance()  # skip '['
        token = self.current()

        try:
            col_size = int(token[1])
            if col_size <= 0:
                self.errors.append(f"Invalid array size {col_size}")
                return
        except ValueError:
            self.errors.append(f"Array size '{token[1]}' is not an integer.")
            return

        self.advance()  # move past the size token
        token = self.current()
        if token and token[0] == ']':
            self.advance()  # skip ']'
        else:
            self.errors.append("Expected ']' after second dimension.")
            return

        # Now we store the 2D dimension as a tuple (row, col).
        self.two_dim[name] = (row, col_size)

        token = self.current()
        if token and token[0] == '=':
            self.array_init(datatype, name, isDynasty)
        elif token and token[0] == ',':
            self.array_more(datatype, isDynasty)
        elif token and token[0] == '~':
            return
        else:
            # Potentially another check or error
            pass


    
    def array_init(self, datatype, name, isDynasty):
        """
        Handles array initialization after encountering '='.
        This version differentiates 1D vs 2D by checking if `name` is in `self.one_dim` or `self.two_dim`.
        """
        # Skip the '='
        self.advance()
        token = self.current()

        self.row_num = 0
        self.column_num = 0
        self.row_elements = []
        self.column_elements = []

        # ---------------------------------------------------------
        # 1) 1D array initialization
        # ---------------------------------------------------------
        if name in self.one_dim:
            declared_size = int(self.one_dim[name][0])  # e.g. if we stored [10], then 10 is the declared size

            # Expect '{'
            if token and token[0] == '{':
                self.advance()  # skip '{'
                token = self.current()

                while token and token[0] != '}':
                    if token[0] == ',':
                        # Skip commas between elements
                        self.advance()
                        token = self.current()
                        continue

                    elif token[0] == '{':
                        self.errors.append("Expected one dimensional array but got two dimensional array.")
                        return

                    # Otherwise, it should be an element
                    is_valid, error_message, _ = self.is_value_compatible_with_type(token[1], datatype, token[0])
                    if not is_valid:
                        self.errors.append(error_message)
                        return
                    self.row_num += 1
                    self.row_elements.append(token[1])
                    self.advance()  # consume this element
                    token = self.current()

                # Now we expect '}'
                if token and token[0] == '}':
                    self.one_dim[name] = self.row_elements
                    self.advance()  # skip '}'
                else:
                    self.errors.append("Expected '}' at the end of 1D array initializer.")
                    return

                # Finally, compare how many elements we got
                if self.row_num != declared_size:
                    self.errors.append(
                        f"Array size mismatch -> The declared array dimension(s) expect {declared_size} "
                        f"elements, but the initializer contains {self.row_num} elements."
                    )
                    return
            else:
                self.errors.append("Expected '{' for 1D array initializer.")
                return

        # ---------------------------------------------------------
        # 2) 2D array initialization
        # ---------------------------------------------------------
        elif name in self.two_dim:
            (rows_str, cols_str) = self.two_dim[name]  # e.g. ('4', '5')
            expected_rows = int(rows_str)
            expected_cols = int(cols_str)

            actual_rows = 0

            # Expect '{'
            if token and token[0] == '{':
                self.advance()  # skip '{'
                token = self.current()
            else:
                self.errors.append("Expected '{' to begin 2D array initializer.")
                return

            # Outer loop: read row sublists until we see '}'
            while token and token[0] != '}':
                if token[0] == ',':
                    # Skip commas between row sub-lists
                    self.advance()
                    token = self.current()
                    continue

                # Each row should begin with '{'
                elif token[0] != '{':
                    self.errors.append("Expected '{' to begin a row sub-list in 2D initializer.")
                    return

                # Parse one row
                self.advance()  # skip the '{'
                token = self.current()

                parsed_cols = 0
                while token and token[0] != '}':
                    if token[0] == ',':
                        # Skip commas between elements in the row
                        self.advance()
                        token = self.current()
                        continue

                    # Otherwise, it should be an element
                    is_valid, error_msg, _ = self.is_value_compatible_with_type(token[1], datatype, token[0])
                    if not is_valid:
                        self.errors.append(
                            f"Initializer error at row {actual_rows}, col {parsed_cols}: {error_msg}"
                        )
                        return
                    self.column_elements.append(self.row_elements.copy())
                    parsed_cols += 1
                    self.advance()
                    token = self.current()

                # We should have ended on '}' that closes the row
                if token and token[0] == '}':
                    self.two_dim[name] = self.column_elements
                    self.advance()  # skip '}'
                    token = self.current()
                else:
                    self.errors.append(f"Expected '}}' at end of row {actual_rows} in 2D initializer.")
                    return

                # Check columns
                if parsed_cols != expected_cols:
                    self.errors.append(
                        f"Array size mismatch -> For row {actual_rows}, declared {expected_cols} columns, "
                        f"but got {parsed_cols} elements."
                    )
                    return

                actual_rows += 1

            # Now we should be on '}' that closes the entire 2D array
            if token and token[0] == '}':
                self.advance()  # skip '}'
            else:
                self.errors.append("Expected '}' to close the entire 2D array initializer.")
                return

            # Finally, check total rows
            if actual_rows != expected_rows:
                self.errors.append(
                    f"Array size mismatch -> Declared {expected_rows} rows, but initializer has {actual_rows} rows."
                )
                return

        # ---------------------------------------------------------
        # 3) If it's not in one_dim or two_dim, we do nothing or raise error
        # ---------------------------------------------------------
        else:
            # Possibly do nothing, or raise an error if you expected arrays to be in one_dim or two_dim
            self.errors.append(f"'{name}' is not recognized as 1D or 2D array.")
            return

        # ---------------------------------------------------------
        # 4) Check for trailing , or ~
        # ---------------------------------------------------------
        token = self.current()
        if token and token[0] == ',':
            self.var_more(datatype, isDynasty)
        elif token and token[0] == '~':
            return
        # else: handle other grammar possibilities if needed

    
    def array_more(self, datatype, isDynasty):
        self.advance()
        token = self.current()
        self.dynasty_dval = "false"
        self.other_dval = "phantom"
        self.name = None
        self.row = None

        # 2) Get the identifier name, check if it's already declared
        token = self.current()
        if (any(token[1] in s for s in self.dynasty_id.values()) or 
            any(token[1] in s for s in self.other_id.values()) or 
            any(token[1] in s for s in self.other_array_id.values()) or 
            any(token[1] in s for s in self.dynasty_array_id.values())):
            self.errors.append(f"{token[1]} is already declared")
            return
        else:
            # Insert into the correct "array" table
            if self.isDynasty:
                # Add the identifier to the set for the given data type.
                self.dynasty_array_id[self.datatype].add(token[1])
                # Store its associated value separately, if needed.
                self.dynasty_array_values[(self.datatype, token[1])] = self.dynasty_dval
            else:
                self.other_array_id[self.datatype].add(token[1])
                self.other_array_values[(self.datatype, token[1])] = self.other_dval
            self.name = token[1]
            self.advance()


        # 3) Check for the first '[' dimension
        token = self.current()
        if token and token[0] == '[':
            self.advance()  # skip '['
            size_token = self.current()
            try:
                row_size = int(size_token[1])
                if row_size <= 0:
                    self.errors.append(f"Invalid array size {row_size}")
                    return
            except ValueError:
                self.errors.append(f"Array size '{size_token[1]}' is not an integer.")
                return

            self.row = row_size
            self.advance()  # move past the size token

            # We expect a ']'
            token = self.current()
            if token and token[0] == ']':
                self.advance()  # skip ']'
            else:
                self.errors.append("Expected ']' after first dimension.")
                return
        else:
            # If your language requires at least one dimension, raise an error.
            # Or if you allow single variable (no array?), handle that logic here.
            self.errors.append("Expected '[' for array dimension.")
            return

        # 4) Check if there's a second dimension, or an initializer, or more...
        token = self.current()
        if token and token[0] == '[':
            # We have a second dimension => 2D array
            self.column(datatype, self.name, isDynasty, self.row)
        elif token and token[0] == '=':
            # 1D array with initializer
            self.one_dim[self.name] = [self.row]  # store [4] for example
            self.array_init(datatype, self.name, isDynasty)
        elif token and token[0] == ',':
            # Another array declared in the same statement
            self.one_dim[self.name] = [self.row]
            self.array_more(datatype, isDynasty)
        elif token and token[0] == '~':
            # End of statement
            self.one_dim[self.name] = [self.row]
            return
        else:
            self.errors.append(f"Unexpected token '{token[0]}' after dimension.")

    def check_assignment(self):
        print("[DEBUG] check_assignment() - Not implemented yet")
        pass

    def check_function_call(self):
        print("[DEBUG] check_function_call() - Not implemented yet")
        pass

    def check_if_statement(self):
        print("[DEBUG] check_if_statement() - Not implemented yet")
        pass

    def check_for_loop(self):
        print("[DEBUG] check_for_loop() - Not implemented yet")
        pass

    def check_while_statement(self):
        print("[DEBUG] check_while_statement() - Not implemented yet")
        pass




























    #-------------------------------------------------------------------------
    # FUNCTIONS
    #-------------------------------------------------------------------------


    

def check_if_exist(self, name):
    if (any(name in s for s in self.dynasty_id.values()) or 
            any(name in s for s in self.other_id.values()) or 
            any(name in s for s in self.other_array_id.values()) or 
            any(name in s for s in self.dynasty_array_id.values())):
            self.errors.append(f"{name} is already declared")
            return
    
# Fixed check_var_init function
def check_var_init(self, token_value, var_name, datatype, isDynasty):
        if token_value != '=':
            if isDynasty:
                # Add the identifier to the set for the given data type.
                self.dynasty_id[datatype].add(var_name)
                # Store its associated value separately, if needed.
                if datatype == "mirror":
                    self.dynasty_values[(datatype, var_name)] = "false"
                else:
                    self.dynasty_values[(datatype, var_name)] = "phantom"
            else:
                self.other_id[datatype].add(var_name)
                if datatype == "mirror":
                    self.other_values[(datatype, var_name)] = "false"
                else:
                    self.other_values[(datatype, var_name)] = "phantom"
            return var_name

        elif token_value == '=':
            if isDynasty:
                # Add the identifier to the set for the given data type.
                self.dynasty_id[datatype].add(var_name)
            else:
                self.other_id[datatype].add(var_name)
                return var_name
        

def is_value_compatible_with_type(self, value: str, data_type: str, token_type, name, isDynasty) -> tuple[bool, str]:
        self.isArray = False
        self.isOneDim = value in self.one_dim
        
        if value in (any(name in s for s in self.other_array_id.values()) or any(name in s for s in self.dynasty_array_id.values())):
            self.isArray = True


        if data_type == "treasures":
            print("treasures")
            print(token_type)
            if token_type in ['treasures_lit', '1', '0']:
                return check_literals_compatibility("treasures", value)
            elif token_type == 'identifier':
                is_valid, str = self.check_identifier_type(value, data_type, name)
                if self.isArray:
                    if is_valid:
                        array_element(self, value, self.isOneDim)
                    else:
                        return(False, str)
                elif not self.isArray:
                    pass
                else:
                    return self.check_identifier_type(value, data_type, name)
            elif token_type == "phantom":
                 return (True, "")
            elif token_type == 'wish':
                 return (True, "")
            elif token_type == 'lengthof':
                 return (True, "")
            elif token_type == 'totreasures':
                 return (True, "")
            else:
                return (False, f"'{value}' is not a valid integer (treasures).")
        elif data_type == "ocean":
            print("ocean")
            print(token_type)
            if token_type == 'ocean_lit':
                return check_literals_compatibility("ocean", value)
            elif token_type == 'identifier':
                return (True, "")
            elif token_type == "phantom":
                return (True, "")
            elif token_type == 'wish':
                return (True, "")
            elif token_type == 'toocean':
                return (True, "")
            else:
                return (False, f"'{value}' is not a valid float (ocean).")
        elif data_type == "scroll":
            if token_type == 'scroll_lit':
                return check_literals_compatibility("scroll", value)
            elif token_type == 'identifier':
                 return (True, "")
            elif token_type == "phantom":
                 return (True, "")
            elif token_type == 'wish':
                 return (True, "")
            elif token_type == 'toscroll':
                 return (True, "")
            else:
                return (False, f"'{value}' is not a valid string (scroll).")
        elif data_type == "rose":
            if token_type == 'rose_lit':
                return check_literals_compatibility("rose", value)
            elif token_type == 'identifier':
                 return (True, "")
            elif token_type == "phantom":
                 return (True, "")
            elif token_type == 'wish':
                 return (True, "")
            elif token_type == 'torose':
                 return (True, "")
            else:
                return (False, f"'{value}' is not a valid char (rose).")
        elif data_type == "mirror":
            if token_type in ['mirror_lit', '1', '0']:
                return (True, "")
            elif token_type == 'identifier':
                 return (True, "")
            elif token_type == 'wish':
                 return (True, "")
            else:
                return (False, f"'{value}' is not a valid boolean (mirror).")
        
        # Default case if data_type doesn't match any
        return (False, f"Unknown data type: {data_type}")

def check_literals_compatibility(self, data_type, value) -> tuple[bool, str]:
        if data_type == "treasures":
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                return (True, "", int(value))
            else:
                return (False, f"'{value}' is not a valid integer (treasures).")
        elif data_type == "ocean":
            try:
                float_value = float(value)
                if '.' in value:
                    return (True, "", float_value)
                return (False, f"'{value}' lacks a decimal point required for ocean type.")
            except ValueError:
                return (False, f"'{value}' is not a valid float (ocean).")
        elif data_type == "scroll":
            if value.startswith('\"') and value.endswith('\"'):
                    return (True, "", value[1:-1])  # Return without quotes
            else:
                return (False, f"'{value}' is not a valid string (scroll).")
        elif data_type == "rose":
            if len(value) == 3 and value.startswith("'") and value.endswith("'"):
                    return (True, "", value[1:-1])  # Return without quotes
            else:
                return (False, f"'{value}' is not a valid single-character (rose).")
        elif data_type == "mirror":
            if value.lower() in ["true", "false", "1", "0"]:
                return (True, "", value.lower() == "true")
            else:
                return (False, f"'{value}' is not a valid boolean (mirror).")
        
        # Default case if data_type doesn't match any
        return (False, f"Unknown data type: {data_type}")

def array_element(self, value, is_one_dim) -> tuple[int, int]:
        self.advance()  # move to '['
        token = self.current()
        if token[0] == '[':
            print("Array access detected for:", value)

            if is_one_dim:
                array_elements = self.one_dim[value]
                expected_size = len(array_elements)  # correct way to get size
                print(f"1D array '{value}' size is {expected_size}")

                if token[0] == '[':
                    self.advance()
                    token = self.current()

                    try:
                        index = int(token[1])
                    except ValueError:
                        self.errors.append(f"Invalid index '{token[1]}'")
                        return (None, None)

                    print(f"Checking index {index} against max {expected_size - 1}")

                    if index < 0 or index >= expected_size:
                        self.errors.append(f"Array index {index} out of bounds; max is {expected_size - 1}.")
                        return (None, None)

                    self.advance()  # move past index
                    token = self.current()

                    if token[0] != ']':
                        self.errors.append(f"Expected ']' after array index, got '{token[0]}'.")
                        return (None, None)

                    return (True, index)

            elif not is_one_dim:
                array_elements = self.two_dim[value]
                expected_rows, expected_cols = len(array_elements), len(array_elements[0])
                print(f"2D array '{value}' size is [{expected_rows}][{expected_cols}]")

                if token[0] == '[':
                    self.advance()
                    token = self.current()

                    try:
                        row_index = int(token[1])
                    except ValueError:
                        self.errors.append(f"Invalid row index '{token[1]}'")
                        return (None, None)

                    print(f"Checking row index {row_index} against max {expected_rows - 1}")
                    if row_index < 0 or row_index >= expected_rows:
                        self.errors.append(f"Row index {row_index} out of bounds; max is {expected_rows - 1}.")
                        return (None, None)

                    self.advance()  # move past row index
                    token = self.current()

                    if token[0] != ']':
                        self.errors.append(f"Expected ']' after row index, got '{token[0]}'.")
                        return (None, None)

                    self.advance()
                    token = self.current()

                    if token[0] == '[':
                        self.advance()
                        token = self.current()

                        try:
                            col_index = int(token[1])
                        except ValueError:
                            self.errors.append(f"Invalid column index '{token[1]}'")
                            return (None, None)

                        print(f"Checking col index {col_index} against max {expected_cols - 1}")
                        if col_index < 0 or col_index >= expected_cols:
                            self.errors.append(f"Column index {col_index} out of bounds; max is {expected_cols - 1}.")
                            return (None, None)

                        self.advance()
                        token = self.current()

                        if token[0] != ']':
                            self.errors.append(f"Expected ']' after column index, got '{token[0]}'.")
                            return (None, None)

                        return (row_index, col_index)

            self.errors.append(f"Invalid array indexing for '{value}'")
            return (None, None)

        elif token[0] == '~':
            self.errors.append(f"{value} is an array and must have an index.")
            return (None, None)

        self.errors.append(f"Unexpected token '{token[0]}'")
        return ( None, None)

def check_identifier_type(self, identifier: str, expected_type: str, name) -> tuple[bool, str]:
        """
        Checks if an identifier exists and has the expected data type.
        Returns (is_valid, error_message) tuple.
        """
        print(f"Checking identifier: {identifier}, expected type: {expected_type}, target name: {name}")
        
        # Try to find identifier in dynasty variables
        for data_type, identifiers in self.dynasty_id.items():
            if identifier in identifiers:
                print(f"Found {identifier} in dynasty {data_type}")
                
                if data_type == expected_type:

                    return (True, "")
                else:
                    return (False, f"Type mismatch: '{identifier}' is '{data_type}', not '{expected_type}'")
        
        # Try to find identifier in regular variables
        for data_type, identifiers in self.other_id.items():
            if identifier in identifiers:
                print(f"Found {identifier} in other {data_type}")
                
                if data_type == expected_type:
                    # Get the actual value using the correct ke
                    
                    return (True, "")
                else:
                    return (False, f"Type mismatch: '{identifier}' is '{data_type}', not '{expected_type}'")
        
        print(f"Identifier {identifier} not found in any variable list")
        return (False, f"Undefined identifier: '{identifier}'")
    
