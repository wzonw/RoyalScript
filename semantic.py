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
        self.dynasty_dval = False
        self.other_dval = "phantom"
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
        if (any(token[1] in s for s in self.dynasty_id.values()) or 
            any(token[1] in s for s in self.other_id.values()) or 
            any(token[1] in s for s in self.other_array_id.values()) or 
            any(token[1] in s for s in self.dynasty_array_id.values())):
            self.errors.append(f"{token[1]} is already declared")
            return

        
        if self.isDynasty:
            # Add the identifier to the set for the given data type.
            self.dynasty_id[self.datatype].add(token[1])
            # Store its associated value separately, if needed.
            self.dynasty_values[(self.datatype, token[1])] = self.dynasty_dval
        else:
            self.other_id[self.datatype].add(token[1])
            self.other_values[(self.datatype, token[1])] = self.other_dval
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
        self.advance()
        token = self.current()
        is_valid, error_message = self.is_value_compatible_with_type(token[1], datatype, token[0])

        if not is_valid:
            self.errors.append(error_message)
            return

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
        self.dynasty_dval = False
        self.other_dval = "phantom"
        self.name = None

        if (any(token[1] in s for s in self.dynasty_id.values()) or 
            any(token[1] in s for s in self.other_id.values()) or 
            any(token[1] in s for s in self.other_array_id.values()) or 
            any(token[1] in s for s in self.dynasty_array_id.values())):
            self.errors.append(f"{token[1]} is already declared")
            return
        
        if self.isDynasty:
            # Add the identifier to the set for the given data type.
            self.dynasty_id[self.datatype].add(token[1])
            # Store its associated value separately, if needed.
            self.dynasty_values[(self.datatype, token[1])] = self.dynasty_dval
        else:
            self.other_id[self.datatype].add(token[1])
            self.other_values[(self.datatype, token[1])] = self.other_dval
        self.name = token[1]
        self.advance()


        token = self.current()
        if token[0] == '=':
            self.init(datatype, self.name, isDynasty)
        
        elif token[0] == ',':
            self.var_more(datatype, isDynasty)
        
        elif token[0] == '~':
            return

    def is_value_compatible_with_type(self, value: str, data_type: str, token_type) -> tuple[bool, str]:
        """
        Returns (is_valid, error_message) indicating if 'value' is valid
        for the given 'data_type'. If invalid, 'error_message' describes why.
        """
        self.isArray = False

        if any (value in s for s in self.dynasty_array_id.values()) or any (value in s for s in self.other_array_id.values()):
            self.isArray = True
        token = self.current()
        print(self.isArray)

        print("Dynasty ID contents:")
        for dtype, id_dict in self.dynasty_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        print("Other ID contents:")
        for dtype, id_dict in self.other_id.items():
            print(f"  {dtype}: {list(id_dict)}")

        if token_type == 'identifier':
                # First check if we have a next token at all
            peeked_token = self.peek()

            if peeked_token is None:
                return self.check_identifier_type(value, data_type)
            
            if self.isArray:
                token = self.current()
                # Now check if the next token is a bracket for array access
                if peeked_token[0] == '[':  # Compare with the token type, not value
                    # Check if array exists in our tracking structures
                    print("Array access detected for:", value)
                    is_one_dim = value in self.one_dim
                    is_two_dim = value in self.two_dim
                    
                    if not (is_one_dim or is_two_dim):
                        return (False, f"Array '{value}' is not defined.")
                    
                    # Check if the identifier is valid for the given data type
                    if not self.check_identifier_type(value, data_type):
                        return (False, f"Type mismatch for array '{value}'.")
                    
                    # Move to the opening bracket
                    self.advance()
                    token = self.current()
                    
                    # Handle 1D array indexing
                    if is_one_dim:
                        expected_size = self.one_dim[value][0]  # Get the size from [size]
                        print(f"1D array access for {value} with max index {expected_size-1}")
                        
                        # Parse the single `[index]`
                        if token[0] == '[':
                            self.advance()
                            token = self.current()
                            
                            # if token[0] != 'number':
                            #     return (False, f"Expected numeric index, got '{token[0]}'.")
                            
                            index = int(token[1])
                            print(f"Checking index {index} against max {expected_size-1}")
                            if index < 0 or index >= expected_size:
                                return (False, f"Array index {index} out of bounds; max is {expected_size - 1}.")
                            
                            # Move past the index
                            self.advance()
                            token = self.current()
                            
                            if token[0] == ']':
                                # self.advance()  # Move past the closing bracket
                                return (True, "")
                            else:
                                return (False, f"Expected ']' after array index, got '{token[0]}'.")
                        
                        
                    # Handle 2D array indexing
                    elif is_two_dim:
                        (expected_rows, expected_cols) = self.two_dim[value]
                        print(f"2D array access for {value} with max indices [{expected_rows-1}][{expected_cols-1}]")
                        
                        # Parse the first `[row_index]`
                        if token[0] == '[':
                            self.advance()
                            token = self.current()
                            
                            # if token[0] != 'number':
                            #     return (False, f"Expected numeric row index, got '{token[0]}'.")
                            
                            row_index = int(token[1])
                            print(f"Checking row index {row_index} against max {expected_rows-1}")
                            if row_index < 0 or row_index >= expected_rows:
                                return (False, f"Row index {row_index} out of bounds; max is {expected_rows - 1}.")
                            
                            # Move past the row index
                            self.advance()
                            token = self.current()
                            
                            if token[0] == ']':
                                # self.advance()  # Move past the closing bracket
                                token = self.current()
                            else:
                                return (False, f"Expected ']' after row index, got '{token[0]}'.")
                            
                            # Parse the second `[col_index]`
                            if token[0] == '[':
                                self.advance()
                                token = self.current()
                                
                                # if token[0] != 'number':
                                #     return (False, f"Expected numeric column index, got '{token[0]}'.")
                                
                                col_index = int(token[1])
                                print(f"Checking col index {col_index} against max {expected_cols-1}")
                                if col_index < 0 or col_index >= expected_cols:
                                    return (False, f"Column index {col_index} out of bounds; max is {expected_cols - 1}.")
                                
                                # Move past the column index
                                self.advance()
                                token = self.current()
                                
                                if token[0] == ']':
                                    # self.advance()  # Move past the closing bracket
                                    return (True, "")
                                else:
                                    return (False, f"Expected ']' after column index, got '{token[0]}'.")
                            else:
                                return (False, f"Expected '[' for column index, got '{token[0]}'.")
                        else:
                            return (False, f"Expected '[' for row index, got '{token[0]}'.")
                
                elif peeked_token[0] == '~':
                    # Not an array access, just check the identifier
                    return (False, f"{token[1]} is an array and must have an index.")

            elif (any(token[1] in s for s in self.dynasty_id.values()) or any(token[1] in s for s in self.other_id.values()) or any(token[1] in s for s in self.other_array_id.values())):
                return self.check_identifier_type(value, data_type)
            else:
                return (False, f"Undefined identifier: '{value}'")
            

        else:
            if data_type == "treasures":
                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    return (True, "")
                elif value == 'phantom':
                    return (True, "")
                elif value == 'lengthof':
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()
                        
                    if token[0] == 'identifier':
                        return self.check_identifier_type(token[1], "scroll")
                    self.advance()
                    token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    
                elif value == "wish":
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()

                    if token[0] == 'scroll_lit':
                        self.advance()
                        token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    
                elif value == 'totreasures':
                    self.advance()
                    token = self.current()
                    if token[0] == '(':
                        self.advance()
                        token = self.current()
                        if token[0] == 'identifier':
                            self.datatype = None
                            self.actual_value = None
                            self.isDynasty = False
                        
                            for dtype, identifiers in self.dynasty_id.items():
                                if token[1] in identifiers:
                                    self.datatype = dtype
                                    self.isDynasty = True
                                    break
                            if not self.datatype:
                                for dtype, identifiers in self.other_id.items():
                                    if token[1] in identifiers:
                                        self.datatype = dtype
                                        self.isDynasty = False
                                        break

                            if not self.datatype:
                                return (False, f"Undefined identifier: '{token[1]}'")
                            
                            if self.isDynasty:
                                self.actual_value = self.dynasty_values[(self.datatype, token[1])]
                            else:
                                self.actual_value = self.other_values[(self.datatype, token[1])]
                        
                            # Check if the value can be converted to treasures
                            if self.datatype == "treasures":
                                # Already a treasures value
                                return (True, "")
                            elif self.datatype == "ocean":
                                # Can convert ocean to treasures
                                return (True, "")
                            elif self.datatype == "scroll":
                                # Check if string is numeric
                                if self.actual_value is None:  # phantom
                                    return (False, "Cannot convert phantom scroll to treasures")
                                string_value = self.actual_value.strip('"')
                                if string_value.isdigit() or (string_value.startswith('-') and string_value[1:].isdigit()):
                                    return (True, "")
                                else:
                                    return (False, f"Cannot convert non-numeric scroll '{string_value}' to treasures")
                            elif self.datatype == "rose":
                                # Check if string is numeric
                                if self.actual_value is None:  # phantom
                                    return (False, "Cannot convert phantom scroll to treasures")
                                string_value = self.actual_value.strip("'")
                                if string_value.isdigit():
                                    return (True, "")
                                else:
                                    return (False, f"Cannot convert non-numeric rose '{string_value}' to treasures")
                            elif self.datatype == "mirror":
                                # Can convert boolean to 0/1
                                return (True, "")
                            else:
                                return (False, f"Cannot convert {self.datatype} to treasures")

                            
                        elif token[0] == 'treasures_lit':
                            return (True, "")
                        elif token[0] in  ['1', '0']:
                            return (True, "")
                        elif token[0] == 'ocean_lit':
                            return (True, "")
                        elif token[0] == 'scroll_lit':
                            # Check if string is numeric
                            if token[1] is None:  # phantom
                                return (False, "Cannot convert phantom scroll to treasures")
                            string_value= token[1].strip('"')
                            if string_value.isdigit() or (string_value.startswith('-') and string_value[1:].isdigit()):
                                return (True, "")
                            else:
                                return (False, f"Cannot convert non-numeric scroll '{string_value}' to treasures")
                        elif token[0] == 'rose_lit':
                            if token[1] is None:  # phantom
                                return (False, "Cannot convert phantom scroll to treasures")
                            string_value= token[1].strip("'")
                            if string_value.isdigit():
                                return (True, "")
                            else:
                                return (False, f"Cannot convert non-numeric rose '{string_value}' to treasures")
                        elif token[0] == ['mirror_lit']:
                            # if token[1].isdigit():
                            return (True, "")

                else:
                    return (False, f"'{value}' is not a valid integer (treasures).")

            elif data_type == "ocean":
                # 1) Phantom is always valid for ocean
                if value == 'phantom':
                    return (True, "")

                elif value == "wish":
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()

                    if token[0] == 'scroll_lit':
                        self.advance()
                        token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    

                # 2) If user wrote "toocean"
                if value == 'toocean':
                    # Advance tokens to parse what's inside (...).
                    self.advance()
                    token = self.current()

                    if token[0] != '(':
                        return (False, f"Expected '(' after 'toocean', got '{token[0]}' instead.")
                    self.advance()
                    token = self.current()

                    # (A) If it's an identifier
                    if token[0] == 'identifier':
                        self.datatype = None
                        self.actual_value = None
                        self.isDynasty = False

                        # Check dynasty IDs
                        for dtype, identifiers in self.dynasty_id.items():
                            if token[1] in identifiers:
                                self.datatype = dtype
                                self.isDynasty = True
                                break
                        # If not found in dynasty, check other IDs
                        if not self.datatype:
                            for dtype, identifiers in self.other_id.items():
                                if token[1] in identifiers:
                                    self.datatype = dtype
                                    self.isDynasty = False
                                    break

                        if not self.datatype:
                            return (False, f"Undefined identifier: '{token[1]}'")

                        # Retrieve the actual value from whichever set it belongs to
                        if self.isDynasty:
                            self.actual_value = self.dynasty_values[(self.datatype, token[1])]
                        else:
                            self.actual_value = self.other_values[(self.datatype, token[1])]

                        # Now decide if we can convert self.datatype -> ocean.
                        if self.datatype == "ocean":
                            # Already ocean
                            return (True, "")
                        elif self.datatype == "treasures":
                            # For example, interpret integer treasures as a float by appending .0
                            return (True, "")
                        elif self.datatype == "scroll":
                             # Check if string is numeric
                            if self.actual_value is None:  # phantom
                                return (False, "Cannot convert phantom scroll to treasures")
                            string_value = self.actual_value.strip('"')
                            if string_value.isdigit() or (string_value.startswith('-') and string_value[1:].isdigit()):
                                return (True, "")
                            else:
                                return (False, f"Cannot convert non-numeric scroll '{string_value}' to ocean")
                        elif self.datatype == "rose":
                            # Check if string is numeric
                            if self.actual_value is None:  # phantom
                                return (False, "Cannot convert phantom scroll to treasures")
                            string_value = self.actual_value.strip("'")
                            if string_value.isdigit():
                                return (True, "")
                            else:
                                return (False, f"Cannot convert non-numeric rose '{string_value}' to treasures")
                        elif self.datatype == "mirror":
                            # Could treat mirror (true/false) as 1.0 or 0.0
                            return (True, "")
                        else:
                            return (False, f"Cannot convert {self.datatype} to ocean.")

                    # (B) If it's a literal token
                    elif token[0] == 'treasures_lit':
                        # Possibly treat numeric literal as float by appending .0
                        return (True, "")
                    elif token[0] in ['1', '0']:
                        # Mirror-likes => ocean? Sure, treat as "1.0" or "0.0"
                        return (True, "")
                    elif token[0] == 'ocean_lit':
                        # Already ocean
                        return (True, "")
                    elif token[0] == 'scroll_lit':
                        # Check if string is numeric
                        if token[1] is None:  # phantom
                            return (False, "Cannot convert phantom scroll to treasures")
                        string_value= token[1].strip('"')
                        try:
                            float(string_value)
                            if '.' in string_value:
                                return (True, "")
                            return (False, f"'{string_value}' lacks a decimal point required for ocean type.")
                        except ValueError:
                                return (False, f"Cannot convert non-numeric scroll '{string_value}' to ocean")
                    elif token[0] == 'rose_lit':
                        if token[1] is None:  # phantom
                            return (False, "Cannot convert phantom scroll to treasures")
                        string_value= token[1].strip("'")
                        try:
                            float(string_value)
                            if '.' in string_value:
                                return (True, "")
                            return (False, f"'{string_value}' lacks a decimal point required for ocean type.")
                        except ValueError:
                                return (False, f"Cannot convert non-numeric rose '{string_value}' to ocean")
                    elif token[0] == 'mirror_lit':
                        # e.g. "true"/"false" => "1.0" / "0.0"
                        return (True, "")
                    else:
                        return (False, f"Unexpected token '{token[0]}' when converting to ocean.")

                # 3) Otherwise, do the normal "ocean" validation (float + decimal point).
                else:
                    try:
                        float(value)
                        if '.' in value:
                            return (True, "")
                        return (False, f"'{value}' lacks a decimal point required for ocean type.")
                    except ValueError:
                        return (False, f"'{value}' is not a valid float (ocean).")


            elif data_type == "scroll":
                if value.startswith('\"') and value.endswith('\"'):
                    return (True, "")
                elif value == 'phantom':
                    return (True, "")
                
                elif value == "wish":
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()

                    if token[0] == 'scroll_lit':
                        self.advance()
                        token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    

                elif value == 'toscroll':
                    self.advance()
                    token = self.current()
                    if token[0] == '(':
                        self.advance()
                        token = self.current()
                        if token[0] == 'identifier':
                            self.datatype = None
                            self.actual_value = None
                            self.isDynasty = False
                        
                            for dtype, identifiers in self.dynasty_id.items():
                                if token[1] in identifiers:
                                    self.datatype = dtype
                                    self.isDynasty = True
                                    break
                            if not self.datatype:
                                for dtype, identifiers in self.other_id.items():
                                    if token[1] in identifiers:
                                        self.datatype = dtype
                                        self.isDynasty = False
                                        break

                            if not self.datatype:
                                return (False, f"Undefined identifier: '{token[1]}'")
                            
                            if self.isDynasty:
                                self.actual_value = self.dynasty_values[(self.datatype, token[1])]
                            else:
                                self.actual_value = self.other_values[(self.datatype, token[1])]
                        
                            # Check if the value can be converted to treasures
                            if self.datatype == "treasures":
                                # Already a treasures value
                                return (True, "")
                            elif self.datatype == "ocean":
                                # Can convert ocean to treasures
                                return (True, "")
                            elif self.datatype == "scroll":
                                return (True, "")
                            elif self.datatype == "rose":
                                return (True, "")
                            elif self.datatype == "mirror":
                                # Can convert boolean to 0/1
                                return (True, "")
                            else:
                                return (False, f"Cannot convert {self.datatype} to scroll")

                            
                        elif token[0] == 'treasures_lit':
                            return (True, "")
                        elif token[0] in  ['1', '0']:
                            return (True, "")
                        elif token[0] == 'ocean_lit':
                            return (True, "")
                        elif token[0] == 'scroll_lit':
                            return (True, "")
                        elif token[0] == 'rose_lit':
                            return (True, "")
                        elif token[0] == 'mirror_lit':
                            return (True, "")
                        else:
                            return (False, f"Unexpected token '{token[0]}' when converting to scroll.")
                else:
                    return (False, f"'{value}' is not properly quoted for scroll strings.")

            elif data_type == "rose":
                if len(value) == 3 and value.startswith("'") and value.endswith("'"):
                    return (True, "")
                elif value == 'phantom':
                    return (True, "")
                
                elif value == "wish":
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()

                    if token[0] == 'scroll_lit':
                        self.advance()
                        token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    

                elif value == 'torose':
                    self.advance()
                    token = self.current()
                    if token[0] == '(':
                        self.advance()
                        token = self.current()
                        if token[0] == 'identifier':
                            self.datatype = None
                            self.actual_value = None
                            self.isDynasty = False
                        
                            for dtype, identifiers in self.dynasty_id.items():
                                if token[1] in identifiers:
                                    self.datatype = dtype
                                    self.isDynasty = True
                                    break
                            if not self.datatype:
                                for dtype, identifiers in self.other_id.items():
                                    if token[1] in identifiers:
                                        self.datatype = dtype
                                        self.isDynasty = False
                                        break

                            if not self.datatype:
                                return (False, f"Undefined identifier: '{token[1]}'")
                            
                            if self.isDynasty:
                                self.actual_value = self.dynasty_values[(self.datatype, token[1])]
                            else:
                                self.actual_value = self.other_values[(self.datatype, token[1])]
                        
                            # Check if the value can be converted to rose
                            if self.datatype in ['treasures', 'ocean', 'scroll', 'mirror']:
                                val_str = self.actual_value.strip('"').strip("'")
                                # Now check if it’s exactly one character
                                if len(val_str) == 1:
                                    return (True, "")
                                else:
                                    return (False, f"Invalid length of '{val_str}' for rose value")

                            elif self.datatype == "rose":
                                return (True, "")
                            else:
                                return (False, f"Cannot convert {self.datatype} to rose")

                            

                        
                        elif token[0] in ['treasures_lit', 'ocean_lit', 'scroll_lit', 'mirror_lit']:
                            val_str = token[1].strip('"').strip("'")
                            # Now check if it’s exactly one character
                            if len(val_str) == 1:
                                return (True, "")
                            else:
                                return (False, f"Invalid length of '{val_str}' for rose value")
                        elif token[0] in  ['1', '0']:
                            return (True, "")
                        elif token[0] == 'rose_lit':
                            return (True, "")
                        else:
                            return (False, f"Unexpected token '{token[0]}' when converting to rose.")
                else:
                    return (False, f"'{value}' is not a valid single-character (rose).")

            elif data_type == "mirror":
                if value.lower() in ["true", "false", "0", "1"]:
                    return (True, "")
                
                elif value == "wish":
                    self.advance()
                    token = self.current()

                    if token[0] == '(':
                        self.advance()
                        token = self.current()

                    if token[0] == 'scroll_lit':
                        self.advance()
                        token = self.current()

                    if token[0] == ')':
                        return (True, "")
                    

                elif value == 'tomirror':
                    self.advance()
                    token = self.current()
                    if token[0] == '(':
                        self.advance()
                        token = self.current()
                        if token[0] == 'identifier':
                            self.datatype = None
                            self.actual_value = None
                            self.isDynasty = False
                        
                            for dtype, identifiers in self.dynasty_id.items():
                                if token[1] in identifiers:
                                    self.datatype = dtype
                                    self.isDynasty = True
                                    break
                            if not self.datatype:
                                for dtype, identifiers in self.other_id.items():
                                    if token[1] in identifiers:
                                        self.datatype = dtype
                                        self.isDynasty = False
                                        break

                            if not self.datatype:
                                return (False, f"Undefined identifier: '{token[1]}'")
                            
                            if self.isDynasty:
                                self.actual_value = self.dynasty_values[(self.datatype, token[1])]
                            else:
                                self.actual_value = self.other_values[(self.datatype, token[1])]
                        
                            # Check if the value can be converted to treasures
                            if self.datatype in ["treasures", "ocean"]:
                                val_str = self.actual_value.strip('"').strip("'")
                                if val_str in ["1", "0"]:
                                    return (True, "")
                                return (False, f"'{value}' is not a valid boolean (mirror).")
                            elif self.datatype == "scroll":
                                val_str = self.actual_value.strip('"').strip("'")
                                if val_str in ["1", "0", "true", "false"]:
                                    return (True, "")
                                return (False, f"'{value}' is not a valid boolean (mirror).")
                            elif self.datatype == "rose":
                                val_str = self.actual_value.strip('"').strip("'")
                                if val_str in ["1", "0"]:
                                    return (True, "")
                                return (False, f"'{value}' is not a valid boolean (mirror).")
                            elif self.datatype == "mirror":
                                # Can convert boolean to 0/1
                                return (True, "")
                            else:
                                return (False, f"Cannot convert {self.datatype} to scroll")

                            
                        elif token[0] in ['treasures_lit', 'ocean_lit']:
                            val_str = token[1].strip('"').strip("'")
                            if val_str in ["1", "0"]:
                                return (True, "")
                            return (False, f"'{value}' is not a valid boolean (mirror).")
                        elif token[0] in  ['1', '0']:
                            return (True, "")
                        elif token[0] == 'scroll_lit':
                            val_str = token[1].strip('"').strip("'")
                            if val_str in ["1", "0", "true", "false"]:
                                return (True, "")
                            return (False, f"'{value}' is not a valid boolean (mirror).")
                        elif token[0] == 'rose_lit':
                            val_str = token[1].strip('"').strip("'")
                            if val_str in ["1", "0"]:
                                return (True, "")
                            return (False, f"'{value}' is not a valid boolean (mirror).")
                        elif token[0] == 'mirror_lit':
                            return (True, "")
                        else:
                            return (False, f"Unexpected token '{token[0]}' when converting to scroll.")
                else:
                    return (False, f"'{value}' is not a valid boolean (mirror).")

            # else:
            #     # Unknown data type
            #     return (False, f"Unknown data type '{data_type}'.")
    def check_identifier_type(self, identifier: str, expected_type: str) -> tuple[bool, str]:
        """
        Checks if an identifier exists and has the expected data type.
        Returns (is_valid, error_message) tuple.
        """
        # Check if identifier exists in dynasty_id dictionaries
        for data_type, identifiers in self.dynasty_id.items():
            if identifier in identifiers:
                if data_type == expected_type:
                    return (True, "")
                else:
                    return (False, f"Type mismatch: '{identifier}' is '{data_type}', not '{expected_type}'")
        
        # Check if identifier exists in other_id dictionaries
        for data_type, identifiers in self.other_id.items():
            if identifier in identifiers:
                if data_type == expected_type:
                    return (True, "")
                else:
                    return (False, f"Type mismatch: '{identifier}' is '{data_type}', not '{expected_type}'")
        
        # Identifier not found in any dictionary
        return (False, f"Undefined identifier: '{identifier}'")
    

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
        self.dynasty_dval = False
        self.other_dval = "phantom"
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
                    is_valid, error_message = self.is_value_compatible_with_type(token[1], datatype, token[0])
                    if not is_valid:
                        self.errors.append(error_message)
                        return
                    self.row_num += 1

                    self.advance()  # consume this element
                    token = self.current()

                # Now we expect '}'
                if token and token[0] == '}':
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
                    is_valid, error_msg = self.is_value_compatible_with_type(token[1], datatype, token[0])
                    if not is_valid:
                        self.errors.append(
                            f"Initializer error at row {actual_rows}, col {parsed_cols}: {error_msg}"
                        )
                        return
                    parsed_cols += 1
                    self.advance()
                    token = self.current()

                # We should have ended on '}' that closes the row
                if token and token[0] == '}':
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