import re
from collections import defaultdict

class Parser:
    def __init__(self):
        # Initialize data structures
        self.productions = {}  # Maps non-terminals to their production rules
        self.terminals = set()  # Set of terminal symbols
        self.non_terminals = set()  # Set of non-terminal symbols
        self.first_sets = {}  # Maps grammar symbols to their FIRST sets
        self.follow_sets = {}  # Maps non-terminals to their FOLLOW sets
        self.parsing_table = {}  # LL(1) parsing table
        self.start_symbol = '<program>'  # Starting symbol of the grammar
        
        # Initialize the grammar
        self.initialize_grammar()
        
    def initialize_grammar(self):
        """Initialize the grammar with production rules from the CFG.pdf"""

        self.productions = {}

        # Program Structure
        self.productions['<program>'] = [['crown', '~', '<global_dec>', '<user_defined_func>', 'castle', 'treasures', 'id_lit', '(', ')', '{', '<body>', 'return', 'treasures_lit', '~', '}', 'reign', '~']]
        self.productions['<global_dec>'] = [['<var_dec>', '<global_dec>'], []]

        # Variable Declarations - Left-factored to make identifier context clearer
        self.productions['<var_dec>'] = [['<dynasty_opt>', '<data_type>', 'id_lit', '<vardec_def>']]
        self.productions['<dynasty_opt>'] = [['dynasty'], []]
        self.productions['<vardec_def>'] = [['<basic_vardec>'], ['<array_vardec>']]
        self.productions['<basic_vardec>'] = [['<initialization>', '<vardec_more>', '~']]
        self.productions['<array_vardec>'] = [['[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>', '~']]
        self.productions['<initialization>'] = [['=', '<val>'], []]
        self.productions['<vardec_more>'] = [[',', 'id_lit', '<initialization>', '<vardec_more>'], []]

        # Array Related Rules - Restructured to reduce ambiguity
        self.productions['<column>'] = [['[', '<array_size>', ']'], []]
        self.productions['<array_initialization>'] = [['=', '<array_list>'], []]
        self.productions['<array_list>'] = [['{', '<array_list_content>', '}']]
        self.productions['<array_list_content>'] = [['<single_array_content>'], ['<multi_array_content>']]
        self.productions['<single_array_content>'] = [['<array_lit>', '<lit_more>']]
        self.productions['<multi_array_content>'] = [['{', '<array_row>', '}', '<row_more>']]
        self.productions['<array_row>'] = [['<array_lit>', '<lit_more>']]
        self.productions['<row_more>'] = [[',', '<row_more_content>'], []]
        self.productions['<row_more_content>'] = [['{', '<array_row>', '}', '<row_more>'], ['id_lit', '<row_more>']]
        self.productions['<lit_more>'] = [[',', '<array_lit>', '<lit_more>'], []]
        self.productions['<array_more>'] = [[',', 'id_lit', '[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>'], []]
        self.productions['<array_lit>'] = [['<lit4>'], ['id_lit']]

        # Assignment Operators
        self.productions['<assignment_operator>'] = [['+='], ['-='], ['*='], ['/='], ['%=']]
        self.productions['<assignment_operand>'] = [['<expr>']]

        # Expression Hierarchy - Kept as is but may need different parsing strategy
        self.productions['<expr>'] = [['<logical_expr>']]
        self.productions['<logical_expr>'] = [['<logical_term>', '<logical_expr_tail>']]
        self.productions['<logical_expr_tail>'] = [['||', '<logical_term>', '<logical_expr_tail>'], []]
        self.productions['<logical_term>'] = [['<logical_factor>', '<logical_term_tail>']]
        self.productions['<logical_term_tail>'] = [['&&', '<logical_factor>', '<logical_term_tail>'], []]
        self.productions['<logical_factor>'] = [['!', '<logical_factor>'], ['<relational_expr>']]
        self.productions['<relational_expr>'] = [['<arithmetic_expr>', '<relational_expr_tail>']]
        self.productions['<relational_expr_tail>'] = [['<relational_operator>', '<arithmetic_expr>', '<relational_expr_tail>'], []]
        self.productions['<arithmetic_expr>'] = [['<term>', '<arithmetic_expr_tail>']]
        self.productions['<arithmetic_expr_tail>'] = [['+', '<term>', '<arithmetic_expr_tail>'],
                                                    ['-', '<term>', '<arithmetic_expr_tail>'], []]
        self.productions['<term>'] = [['<factor>', '<term_tail>']]
        self.productions['<term_tail>'] = [['*', '<factor>', '<term_tail>'],
                                        ['/', '<factor>', '<term_tail>'],
                                        ['%', '<factor>', '<term_tail>'], []]
        self.productions['<factor>'] = [['id_lit', '<id_factor_tail>'],
                                        ['<lit3>'],
                                        ['scroll_lit'],
                                        ['rose_lit'],
                                        ['mirror_lit'],
                                        ['<treasures_mirror>'],
                                        ['(', '<expr>', ')']]

        # Modified to clarify id_lit in factor context
        self.productions['<id_factor_tail>'] = [['<func_call>'], ['<index>'], []]

        # Basic Types and Values
        self.productions['<treasures_mirror>'] = [['1'], ['0']]

        # Relational Operators
        self.productions['<relational_operator>'] = [['<'], ['>'], ['<='], ['>='], ['=='], ['!=']]

        # Unary Operations
        self.productions['<unary>'] = [['id_lit', '<unary_operator>']]
        self.productions['<unary_operator>'] = [['++'], ['--']]

        # String Operations
        self.productions['<string_expr>'] = [['<string_operand>', '<string_more>']]
        self.productions['<string_operand>'] = [['<lit1>'], ['id_lit', '<id_string_ext>'], ['toscroll', '(', '<conversion_value>', ')']]
        self.productions['<id_string_ext>'] = [['<func_call>'], ['<index>'], []]
        self.productions['<string_more>'] = [['+', '<string_operand>', '<string_more>'], []]

        # Function Definition - Restructured to make recursive case clearer
        self.productions['<user_defined_func>'] = [['<func_definition>', '<user_defined_func_more>'], []]
        self.productions['<func_definition>'] = [['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}']]
        self.productions['<user_defined_func_more>'] = [['<user_defined_func>'], []]
        self.productions['<return_type>'] = [['<data_type>'], ['chamber']]
        self.productions['<param>'] = [['<data_type>', 'id_lit', '<param_more>'], []]
        self.productions['<param_more>'] = [[',', '<data_type>', 'id_lit', '<param_more>'], []]

        # Statement Body - Modified to reduce ambiguity in recursion
        self.productions['<body>'] = [['<statement>', '<body>'], []]
        self.productions['<statement>'] = [['<var_dec_statement>'],
                                        ['<output_statement>'],
                                        ['<id_statement>'],
                                        ['<control_statement>'],
                                        ['<func_def_statement>']]

        # Restructured statement types for better LL(1) compatibility
        self.productions['<var_dec_statement>'] = [['<var_dec>']]
        self.productions['<output_statement>'] = [['granted', '(', '<granted_content>', '<more_granted>', ')', '~']]
        self.productions['<id_statement>'] = [['id_lit', '<id_statement_type>']]
        self.productions['<id_statement_type>'] = [['<index>', '=', '<expr>', '~'],
                                                ['<index>', '<assignment_operator>', '<expr>', '~'],
                                                ['<unary_operator>', '~'],
                                                ['(', '<args>', ')', '~']]
        self.productions['<control_statement>'] = [['<for_loop>'], ['<condi_statement>']]
        self.productions['<func_def_statement>'] = [['<func_definition>']]

        self.productions['<ret_statement>'] = [['return', '<val1>', '~'], []]

        # Conditional Statements - Modified to reduce ambiguity
        self.productions['<condi_statement>'] = [['<if_statement>'], ['<while_statement>'], ['<do_while_statement>']]
        self.productions['<if_statement>'] = [['<if_then_statement>', '<else_part>']]
        self.productions['<if_then_statement>'] = [['cast', '(', '<condition>', ')', '{', '<body>', '}']]
        self.productions['<else_part>'] = [['<else_if_part>', '<else_optional>']]
        self.productions['<else_if_part>'] = [['twist', '(', '<condition>', ')', '{', '<body>', '}', '<else_if_part>'], []]
        self.productions['<else_optional>'] = [['curse', '{', '<body>', '}'], []]

        # Loop Structures - Restructured for better LL(1) compatibility
        self.productions['<for_loop>'] = [['tale', '(', '<loop_var>', '~', '<relational_expr>', '~', '<unary>', ')', '{', '<loop_body>', '}']]
        self.productions['<loop_var>'] = [['<loop_var_type>']]
        self.productions['<loop_var_type>'] = [['treasures', 'id_lit', '=', '<loop_val>'], ['id_lit', '<loop_init>']]
        self.productions['<loop_init>'] = [['=', '<loop_val>'], []]
        self.productions['<loop_val>'] = [['id_lit'], ['treasures_lit']]
        self.productions['<loop_body>'] = [['<loop_statement>', '<loop_body>'], []]
        self.productions['<loop_statement>'] = [['<regular_loop_statement>'], ['<break_statement>'], ['<continue_statement>'], ['<if_break>']]
        self.productions['<regular_loop_statement>'] = [['<var_dec_statement>'], ['<output_statement>'], ['<id_statement>'], ['<control_statement>'], ['<func_def_statement>']]
        self.productions['<break_statement>'] = [['break', '~']]
        self.productions['<continue_statement>'] = [['continue', '~']]
        self.productions['<if_break>'] = [['<if_break_then>', '<else_break_part>']]
        self.productions['<if_break_then>'] = [['cast', '(', '<condition>', ')', '{', '<body>', '<optional_flow_control>', '}']]
        self.productions['<optional_flow_control>'] = [['<break_statement>'], ['<continue_statement>'], []]
        self.productions['<else_break_part>'] = [['<else_if_break_part>', '<else_break_optional>']]
        self.productions['<else_if_break_part>'] = [['twist', '(', '<condition>', ')', '{', '<body>', '<optional_flow_control>', '}', '<else_if_break_part>'], []]
        self.productions['<else_break_optional>'] = [['curse', '{', '<body>', '<optional_flow_control>', '}'], []]
        self.productions['<do_while_statement>'] = [['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~']]
        self.productions['<while_statement>'] = [['forever', '(', '<condition>', ')', '{', '<loop_body>', '}']]

        # Condition Expression
        self.productions['<condition>'] = [['<expr>']]

        # Output Statement - Modified to reduce ambiguity
        self.productions['<granted_content>'] = [['set_precision'], ['id_lit', '<granted_id_ext>'], ['<granted_expr>']]
        self.productions['<granted_expr>'] = [['<lit3>'], ['scroll_lit'], ['rose_lit'], ['mirror_lit'], ['<treasures_mirror>'], ['(', '<expr>', ')']]
        self.productions['<granted_id_ext>'] = [['<unary_operator>'], ['<func_call>'], ['<index>'], []]
        self.productions['<more_granted>'] = [[',', '<granted_content>', '<more_granted>'], []]

        # Data Types
        self.productions['<data_type>'] = [['scroll'], ['treasures'], ['mirror'], ['ocean'], ['rose']]

        # Values and Literals
        self.productions['<val>'] = [['<expr>'], ['<input>']]
        self.productions['<val1>'] = [['<expr>']]
        self.productions['<conversion_func>'] = [['torose'], ['totreasures'], ['toocean'], ['tomirror']]
        self.productions['<conversion_value>'] = [['<lit4>'], ['id_lit', '<id_conv_ext>']]
        self.productions['<id_conv_ext>'] = [['<func_call>'], ['<index>'], []]

        # Array and Variable Index - Clarified
        self.productions['<index>'] = [['[', '<array_size>', ']', '<column1>'], []]
        self.productions['<column1>'] = [['[', '<array_size>', ']'], []]

        # Input and Literals
        self.productions['<input>'] = [['wish', '(', 'scroll_lit', ')']]
        self.productions['<lit1>'] = [['scroll_lit'], ['rose_lit']]
        self.productions['<lit2>'] = [['mirror_lit']]
        self.productions['<lit3>'] = [['ocean_lit'], ['treasures_lit']]
        self.productions['<lit4>'] = [['<lit1>'], ['<lit2>'], ['<lit3>']]

        # Function Calls and Arguments
        self.productions['<func_call>'] = [['(', '<args>', ')']]
        self.productions['<args>'] = [['<args_list>'], []]
        self.productions['<args_list>'] = [['<expr>', '<args_more>']]
        self.productions['<args_more>'] = [[',', '<expr>', '<args_more>'], []]

        # Array Size
        self.productions['<array_size>'] = [['id_lit'], ['positive_treasures_lit']]

        # Extract terminals and non-terminals
        for lhs, rhs_list in self.productions.items():
            self.non_terminals.add(lhs)
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol.startswith('<') and symbol.endswith('>'):
                        self.non_terminals.add(symbol)
                    elif symbol and symbol != 'λ':
                        self.terminals.add(symbol)
    
    def compute_first_sets(self):
        """Compute FIRST sets for all grammar symbols"""
        # Initialize FIRST sets
        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}
        
        for non_terminal in self.non_terminals:
            self.first_sets[non_terminal] = set()
        
        # Add epsilon to the FIRST set of any non-terminal that has an epsilon production
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if not rhs:  # Empty production (lambda/epsilon)
                    self.first_sets[lhs].add('λ')
        
        # Iteratively compute FIRST sets until no changes
        changed = True
        while changed:
            changed = False
            
            for lhs, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    if not rhs:  # Empty production (lambda/epsilon)
                        continue
                    
                    # Process the first symbol in the production
                    first_symbol = rhs[0]
                    
                    if first_symbol in self.terminals or first_symbol == 'λ':
                        # If the first symbol is a terminal or epsilon, add it to FIRST(lhs)
                        if first_symbol not in self.first_sets[lhs]:
                            self.first_sets[lhs].add(first_symbol)
                            changed = True
                    
                    elif first_symbol in self.non_terminals:
                        # If the first symbol is a non-terminal, add FIRST(first_symbol) - {λ} to FIRST(lhs)
                        for symbol in self.first_sets[first_symbol]:
                            if symbol != 'λ' and symbol not in self.first_sets[lhs]:
                                self.first_sets[lhs].add(symbol)
                                changed = True
                        
                        # If λ is in FIRST(first_symbol), consider the next symbol
                        if 'λ' in self.first_sets[first_symbol]:
                            # Check if we can derive epsilon from the entire RHS
                            all_derive_epsilon = True
                            for symbol in rhs:
                                if symbol not in self.non_terminals or 'λ' not in self.first_sets[symbol]:
                                    all_derive_epsilon = False
                                    break
                            
                            if all_derive_epsilon and 'λ' not in self.first_sets[lhs]:
                                self.first_sets[lhs].add('λ')
                                changed = True
                            
                            # Process subsequent symbols if first_symbol can derive epsilon
                            i = 1
                            while i < len(rhs) and 'λ' in self.first_sets[rhs[i-1]]:
                                symbol = rhs[i]
                                
                                if symbol in self.terminals:
                                    if symbol not in self.first_sets[lhs]:
                                        self.first_sets[lhs].add(symbol)
                                        changed = True
                                    break  # Terminal symbols cannot derive epsilon
                                
                                elif symbol in self.non_terminals:
                                    # Add FIRST(symbol) - {λ} to FIRST(lhs)
                                    for term in self.first_sets[symbol]:
                                        if term != 'λ' and term not in self.first_sets[lhs]:
                                            self.first_sets[lhs].add(term)
                                            changed = True
                                
                                i += 1
        
        return self.first_sets
    
    def compute_follow_sets(self):
        """Compute FOLLOW sets for all non-terminals"""
        # Initialize FOLLOW sets
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()
        
        # Add end marker to FOLLOW of start symbol
        self.follow_sets[self.start_symbol].add('$')
        
        # Iteratively compute FOLLOW sets until no changes
        changed = True
        while changed:
            changed = False
            
            for lhs, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    for i, symbol in enumerate(rhs):
                        if symbol not in self.non_terminals:
                            continue
                        
                        # Compute FIRST of everything after the current symbol
                        first_of_beta = set()
                        all_derive_epsilon = True
                        
                        for j in range(i + 1, len(rhs)):
                            beta_symbol = rhs[j]
                            
                            if beta_symbol in self.terminals:
                                first_of_beta.add(beta_symbol)
                                all_derive_epsilon = False
                                break
                            
                            elif beta_symbol in self.non_terminals:
                                # Add FIRST(beta_symbol) - {λ} to first_of_beta
                                for term in self.first_sets[beta_symbol]:
                                    if term != 'λ':
                                        first_of_beta.add(term)
                                
                                # If beta_symbol cannot derive epsilon, stop
                                if 'λ' not in self.first_sets[beta_symbol]:
                                    all_derive_epsilon = False
                                    break
                        
                        # Add first_of_beta to FOLLOW(symbol)
                        for term in first_of_beta:
                            if term not in self.follow_sets[symbol]:
                                self.follow_sets[symbol].add(term)
                                changed = True
                        
                        # If symbol is at the end or all symbols after it can derive epsilon,
                        # add FOLLOW(lhs) to FOLLOW(symbol)
                        if i == len(rhs) - 1 or all_derive_epsilon:
                            for term in self.follow_sets[lhs]:
                                if term not in self.follow_sets[symbol]:
                                    self.follow_sets[symbol].add(term)
                                    changed = True
        
        return self.follow_sets
    
    def build_parsing_table(self):
        """Build LL(1) parsing table using FIRST and FOLLOW sets"""
        # Initialize parsing table
        for non_terminal in self.non_terminals:
            self.parsing_table[non_terminal] = {}
        
        # For each production rule A → α
        for lhs, rhs_list in self.productions.items():
            for i, rhs in enumerate(rhs_list):
                # If production is A → ε
                if not rhs:
                    # For each terminal b in FOLLOW(A), add A → ε to M[A, b]
                    for terminal in self.follow_sets[lhs]:
                        if terminal in self.parsing_table[lhs]:
                            print(f"Grammar is not LL(1): Conflict for {lhs} with terminal {terminal}")
                        else:
                            self.parsing_table[lhs][terminal] = (i, [])
                else:
                    # Compute FIRST(α)
                    first_of_rhs = self.compute_first_of_string(rhs)
                    
                    # For each terminal a in FIRST(α), add A → α to M[A, a]
                    for terminal in first_of_rhs:
                        if terminal != 'λ':
                            if terminal in self.parsing_table[lhs]:
                                print(f"Grammar is not LL(1): Conflict for {lhs} with terminal {terminal}")
                            else:
                                self.parsing_table[lhs][terminal] = (i, rhs)
                    
                    # If ε is in FIRST(α), for each terminal b in FOLLOW(A), add A → α to M[A, b]
                    if 'λ' in first_of_rhs:
                        for terminal in self.follow_sets[lhs]:
                            if terminal in self.parsing_table[lhs]:
                                print(f"Grammar is not LL(1): Conflict for {lhs} with terminal {terminal}")
                            else:
                                self.parsing_table[lhs][terminal] = (i, rhs)
        
        return self.parsing_table
    
    def compute_first_of_string(self, symbols):
        """Compute FIRST set for a list of grammar symbols"""
        if not symbols:
            return {'λ'}
        
        first_set = set()
        all_can_derive_empty = True
        
        for i, symbol in enumerate(symbols):
            if symbol in self.terminals:
                first_set.add(symbol)
                all_can_derive_empty = False
                break
            
            elif symbol in self.non_terminals:
                # Add FIRST(symbol) - {λ} to first_set
                for term in self.first_sets[symbol]:
                    if term != 'λ':
                        first_set.add(term)
                
                # If symbol cannot derive epsilon, stop here
                if 'λ' not in self.first_sets[symbol]:
                    all_can_derive_empty = False
                    break
            
            else:
                # Unknown symbol, treat as terminal
                first_set.add(symbol)
                all_can_derive_empty = False
                break
        
        # If all symbols can derive lambda, add lambda to first_set
        if all_can_derive_empty:
            first_set.add('λ')
        
        return first_set
    
    def parse(self, tokens):
        """Parse input using LL(1) parsing table"""
        # Add end marker
        tokens.append('$')
        
        # Initialize stack with start symbol and end marker
        stack = ['$', self.start_symbol]
        
        # Initialize parsing steps for visualization
        steps = []
        
        # Input pointer
        i = 0
        
        while stack[-1] != '$':
            top = stack[-1]
            current_token = tokens[i]
            
            steps.append({
                'stack': stack.copy(),
                'input': tokens[i:],
                'action': ''
            })
            
            # If top is a terminal
            if top in self.terminals or top not in self.non_terminals:
                if top == current_token:
                    stack.pop()
                    i += 1
                    steps[-1]['action'] = f"Match {top}"
                else:
                    steps[-1]['action'] = f"Error: Expected {top}, got {current_token}"
                    return False, steps
            
            # If top is a non-terminal
            else:
                if current_token in self.parsing_table[top]:
                    production_index, production = self.parsing_table[top][current_token]
                    stack.pop()
                    
                    # Push production in reverse order
                    for symbol in reversed(production):
                        if symbol != 'λ':  # Don't push epsilon
                            stack.append(symbol)
                    
                    steps[-1]['action'] = f"Apply {top} → {' '.join(production) if production else 'λ'}"
                else:
                    steps[-1]['action'] = f"Error: No production for {top} with token {current_token}"
                    return False, steps
        
        # Check if we've consumed all input
        if i >= len(tokens) - 1:  # Accounting for the added '$'
            steps.append({
                'stack': stack.copy(),
                'input': tokens[i:],
                'action': "Accept"
            })
            return True, steps
        else:
            steps.append({
                'stack': stack.copy(),
                'input': tokens[i:],
                'action': "Error: Input not fully consumed"
            })
            return False, steps
    
    def print_first_sets(self):
        """Print FIRST sets for all grammar symbols"""
        print("FIRST Sets:")
        for symbol in sorted(self.first_sets.keys()):
            print(f"FIRST({symbol}) = {sorted(self.first_sets[symbol])}")
    
    def print_follow_sets(self):
        """Print FOLLOW sets for all non-terminals"""
        print("\nFOLLOW Sets:")
        for symbol in sorted(self.follow_sets.keys()):
            print(f"FOLLOW({symbol}) = {sorted(self.follow_sets[symbol])}")
    
    def print_parsing_table(self):
        """Print LL(1) parsing table"""
        print("\nParsing Table:")
        all_terminals = sorted(list(self.terminals)) + ['$']
        
        # Print header
        header = f"{'Non-Terminal':<30} | " + " | ".join(f"{t:<15}" for t in all_terminals[:10])
        print(header)
        print("-" * len(header))
        
        # Print rows (first 10 columns for readability)
        for nt in sorted(self.non_terminals)[:20]:  # Limiting to first 20 non-terminals for readability
            row = f"{nt:<30} | "
            for t in all_terminals[:10]:  # Limiting to first 10 terminals for readability
                if t in self.parsing_table[nt]:
                    prod_idx, prod = self.parsing_table[nt][t]
                    prod_str = " ".join(prod) if prod else "λ"
                    if len(prod_str) > 15:
                        prod_str = prod_str[:12] + "..."
                    row += f"{prod_str:<15} | "
                else:
                    row += f"{'ERROR':<15} | "
            print(row)
    
    def visualize_parse(self, steps):
        """Visualize parsing steps"""
        print("\nParsing Steps:")
        print(f"{'Stack':<40} | {'Input':<40} | {'Action'}")
        print("-" * 100)
        
        for step in steps:
            stack_str = " ".join(reversed(step['stack']))
            if len(stack_str) > 40:
                stack_str = stack_str[:37] + "..."
            
            input_str = " ".join(step['input'])
            if len(input_str) > 40:
                input_str = input_str[:37] + "..."
            
            action = step['action']
            print(f"{stack_str:<40} | {input_str:<40} | {action}")

# Helper function to tokenize input
def tokenize_input(input_string):
    """Convert input string to tokens"""
    # This is a simplified tokenizer - a real implementation would be more complex
    special_tokens = ['(', ')', '{', '}', '[', ']', ',', ';', '=', '+', '-', '*', '/', '%', '<', '>', '!', '~']
    compound_tokens = ['<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=', '&&', '||']
    
    tokens = []
    i = 0
    while i < len(input_string):
        # Skip whitespace
        if input_string[i].isspace():
            i += 1
            continue
        
        # Check for compound tokens
        if i < len(input_string) - 1:
            possible_compound = input_string[i:i+2]
            if possible_compound in compound_tokens:
                tokens.append(possible_compound)
                i += 2
                continue
        
        # Check for special tokens
        if input_string[i] in special_tokens:
            tokens.append(input_string[i])
            i += 1
            continue
        
        # Handle identifiers and keywords
        if input_string[i].isalpha() or input_string[i] == '_':
            identifier = ''
            while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == '_'):
                identifier += input_string[i]
                i += 1
            
            # Check if it's a keyword or identifier
            if identifier in ['crown', 'castle', 'treasures', 'reign', 'dynasty', 'scroll', 'rose', 'mirror', 'ocean', 'spell', 'chamber', 'return', 'cast', 'twist', 'curse', 'tale', 'believe', 'forever', 'phantom', 'lengthof', 'wish', 'granted', 'toscroll', 'torose', 'totreasures', 'toocean', 'tomirror']:
                tokens.append(identifier)
            else:
                tokens.append('id_lit')  # Simplifying: all identifiers are treated as id_lit
            
            continue
        
        # Handle numeric literals
        if input_string[i].isdigit():
            number = ''
            while i < len(input_string) and (input_string[i].isdigit() or input_string[i] == '.'):
                number += input_string[i]
                i += 1
            
            tokens.append('treasures_lit')  # Simplifying: all numbers are treated as treasures_lit
            continue
        
        # Handle string literals
        if input_string[i] == '"' or input_string[i] == "'":
            quote = input_string[i]
            string_literal = quote
            i += 1
            
            while i < len(input_string) and input_string[i] != quote:
                string_literal += input_string[i]
                i += 1
            
            if i < len(input_string):
                string_literal += input_string[i]  # closing quote
                i += 1
            
            tokens.append('scroll_lit')  # Simplifying: all strings are treated as scroll_lit
            continue
        
        # Skip any other character
        i += 1
    
    return tokens

def main():
    # Create an instance of the parser
    parser = Parser()
    
    # Compute FIRST and FOLLOW sets
    parser.compute_first_sets()
    parser.compute_follow_sets()
    
    # Build the parsing table
    parser.build_parsing_table()
    
    # Print the FIRST and FOLLOW sets
    parser.print_first_sets()
    parser.print_follow_sets()
    
    # Print the parsing table (limited for readability)
    parser.print_parsing_table()
    
    # Test with a simple input
    test_input = """
    crown~
castle treasures Main() {

        treasures N = wish("Enter number of Fibonacci Sequence to be displayed: \n")~

        treasures A = 0, B = 1~
        
        granted("hello")~
    
        
        return 0~
}
reign~

    """
    
    # Tokenize the input
    tokens = tokenize_input(test_input)
    print("\nTokenized input:", tokens)
    
    # Parse the input
    success, steps = parser.parse(tokens)
    
    # Display the result
    if success:
        print("\nParsing successful! The input conforms to the grammar.")
    else:
        print("\nParsing failed. The input does not conform to the grammar.")
    
    # Visualize the parsing steps
    parser.visualize_parse(steps)

if __name__ == "__main__":
    main()