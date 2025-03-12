class RoyalScriptSemanticAnalyzer:
    def __init__(self, statements):
        self.statements = statements
        self.errors = []

        self.dynasty_id = {
            "treasures": {},  # For integers (constants)
            "ocean": {},      # For floating points (constants)
            "scroll": {},     # For strings (constants)
            "rose": {},       # For char (constants)
            "mirror": {}      # For booleans (constants)
        }

        self.other_id = {
            "treasures": {},  # For integers (variables)
            "ocean": {},
            "scroll": {},
            "rose": {},
            "mirror": {},
            "chamber": {}     # For functions with no return value
        }

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
        if not token or (token[0] != "dynasty" and token[0] != "variable"):
            self.errors.append("Expected 'dynasty' or 'variable' keyword in variable declaration")
            return
            
        is_const = token[0] == "dynasty"
        self.advance()
        
        # Check for type (treasures, ocean, etc.)
        token = self.current()
        if not token or token[0] not in ["treasures", "ocean", "scroll", "rose", "mirror"]:
            self.errors.append(f"Expected type keyword in variable declaration, got {token}")
            return
            
        var_type = token[0]
        self.advance()
        
        # Check for identifier
        token = self.current()
        if not token or token[0] != "identifier":
            self.errors.append(f"Expected identifier in variable declaration, got {token}")
            return
            
        var_name = token[1]
        self.advance()
        
        # Store the variable in the appropriate dictionary
        if is_const:
            if var_name in self.dynasty_id[var_type]:
                self.errors.append(f"Constant '{var_name}' already declared")
            else:
                self.dynasty_id[var_type][var_name] = None
                print(f"[DEBUG] Declared dynasty constant '{var_name}' of type '{var_type}'.")
        else:
            if var_name in self.other_id[var_type]:
                self.errors.append(f"Variable '{var_name}' already declared")
            else:
                self.other_id[var_type][var_name] = None
                print(f"[DEBUG] Declared variable '{var_name}' of type '{var_type}'.")
        
        # Check for initialization (=)
        token = self.current()
        if token and token[0] == "=":
            print(f"[DEBUG] Found '=' for initialization.")
            self.advance()
            
            # Check the value
            token = self.current()
            if not token:
                self.errors.append("Expected value after '=' in variable declaration")
                return
                
            value = token[1] if len(token) > 1 else token[0]
            print(f"[DEBUG] current() at index {self.current_token_idx}: {token}")
            print(f"[DEBUG] Initialized '{var_name}' with value '{value}'.")
            self.advance()
        
        # Check for end of declaration (~)
        token = self.current()
        if token and token[0] == "~":
            print(f"[DEBUG] Found '~', end of declaration.")
            # Don't advance here - let the main loop handle the next statement
            return
        
        # If we get here without finding a ~, it's an error
        if token:
            self.errors.append(f"Expected '~' at end of variable declaration, got {token}")

    def check_array_declaration(self):
        """Check an array declaration statement for semantic correctness."""
        print("[DEBUG] Checking array declaration")
        # Implementation would go here
        
    def check_assignment(self):
        """Check an assignment statement for semantic correctness."""
        print("[DEBUG] Checking assignment")
        # Implementation would go here
        
    def check_function_call(self):
        """Check a function call statement for semantic correctness."""
        print("[DEBUG] Checking function call")
        # Implementation would go here
        
    def check_if_statement(self):
        """Check an if statement for semantic correctness."""
        print("[DEBUG] Checking if statement")
        # Implementation would go here
        
    def check_for_loop(self):
        """Check a for loop statement for semantic correctness."""
        print("[DEBUG] Checking for loop")
        # Implementation would go here
        
    def check_while_statement(self):
        """Check a while loop statement for semantic correctness."""
        print("[DEBUG] Checking while statement")
        # Implementation would go hereclass RoyalScriptSemanticAnalyzer:
    def __init__(self, statements):
        self.statements = statements
        self.errors = []

        self.dynasty_id = {
            "treasures": {},  # For integers (constants)
            "ocean": {},      # For floating points (constants)
            "scroll": {},     # For strings (constants)
            "rose": {},       # For char (constants)
            "mirror": {}      # For booleans (constants)
        }

        self.other_id = {
            "treasures": {},  # For integers (variables)
            "ocean": {},
            "scroll": {},
            "rose": {},
            "mirror": {},
            "chamber": {}     # For functions with no return value
        }

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
        if not token or (token[0] != "dynasty" and token[0] != "variable"):
            self.errors.append("Expected 'dynasty' or 'variable' keyword in variable declaration")
            return
            
        is_const = token[0] == "dynasty"
        self.advance()
        
        # Check for type (treasures, ocean, etc.)
        token = self.current()
        if not token or token[0] not in ["treasures", "ocean", "scroll", "rose", "mirror"]:
            self.errors.append(f"Expected type keyword in variable declaration, got {token}")
            return
            
        var_type = token[0]
        self.advance()
        
        # Check for identifier
        token = self.current()
        if not token or token[0] != "identifier":
            self.errors.append(f"Expected identifier in variable declaration, got {token}")
            return
            
        var_name = token[1]
        self.advance()
        
        # Store the variable in the appropriate dictionary
        if is_const:
            if var_name in self.dynasty_id[var_type]:
                self.errors.append(f"Constant '{var_name}' already declared")
            else:
                self.dynasty_id[var_type][var_name] = None
                print(f"[DEBUG] Declared dynasty constant '{var_name}' of type '{var_type}'.")
        else:
            if var_name in self.other_id[var_type]:
                self.errors.append(f"Variable '{var_name}' already declared")
            else:
                self.other_id[var_type][var_name] = None
                print(f"[DEBUG] Declared variable '{var_name}' of type '{var_type}'.")
        
        # Check for initialization (=)
        token = self.current()
        if token and token[0] == "=":
            print(f"[DEBUG] Found '=' for initialization.")
            self.advance()
            
            # Check the value
            token = self.current()
            if not token:
                self.errors.append("Expected value after '=' in variable declaration")
                return
                
            value = token[1] if len(token) > 1 else token[0]
            print(f"[DEBUG] current() at index {self.current_token_idx}: {token}")
            print(f"[DEBUG] Initialized '{var_name}' with value '{value}'.")
            self.advance()
        
        # Check for end of declaration (~)
        token = self.current()
        if token and token[0] == "~":
            print(f"[DEBUG] Found '~', end of declaration.")
            # Don't advance here - let the main loop handle the next statement
            return
        
        # If we get here without finding a ~, it's an error
        if token:
            self.errors.append(f"Expected '~' at end of variable declaration, got {token}")

    def check_array_declaration(self):
        """Check an array declaration statement for semantic correctness."""
        print("[DEBUG] Checking array declaration")
        # Implementation would go here
        
    def check_assignment(self):
        """Check an assignment statement for semantic correctness."""
        print("[DEBUG] Checking assignment")
        # Implementation would go here
        
    def check_function_call(self):
        """Check a function call statement for semantic correctness."""
        print("[DEBUG] Checking function call")
        # Implementation would go here
        
    def check_if_statement(self):
        """Check an if statement for semantic correctness."""
        print("[DEBUG] Checking if statement")
        # Implementation would go here
        
    def check_for_loop(self):
        """Check a for loop statement for semantic correctness."""
        print("[DEBUG] Checking for loop")
        # Implementation would go here
        
    def check_while_statement(self):
        """Check a while loop statement for semantic correctness."""
        print("[DEBUG] Checking while statement")
        # Implementation would go here