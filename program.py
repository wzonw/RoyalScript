class CFGProcessor:
    def __init__(self):
        # Complete grammar dictionary with all productions
        self.grammar = {
            'program': ['crown ~ global_dec user-defined_func castle treasures id_lit {body return 0 ~} reign ~'],
            'global_dec': ['var_dec global_dec', ''],
            'var_dec': ['data_type id_lit vardec_def', ''],
            'vardec_def': ['initialization vardec_more ~', '[num] column array_initialization array_more ~'],
            'initialization': ['= val', ''],
            'vardec_more': [', id_lit initialization vardec_more', ''],
            'column': ['[num]', ''],
            'array_initialization': ['= array_list', ''],
            'array_list': ['single', 'multi'],
            'single': ['{array_lit list_more}'],
            'multi': ['{single multi_more}', ''],
            'multi_more': [', single multi_more', ''],
            'list_more': [', array_lit list_more', ''],
            'array_more': [', id_lit [num] column array_initialization', ''],
            'array_lit': ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
            'assignment_exp': ['id_lit assignment_operator assignment_operand ~'],
            'assignment_operator': ['+=', '-=', '*=', '/=', '%='],
            'assignment_operand': ['id_lit', 'treasures_lit', 'ocean_lit', 'array_element', 'arithmetic_exp'],
            'array_element': ['id_lit index'],
            'logical_exp': ['logical_operand logical_operator logical_operand more_log', 
                          'logical_operator1 logical_operand more_log'],
            'logical_operand': ['id_lit', 'mirror_lit', 'treasures_mirror', 'relational_exp', '(relational_exp)', 
                              'func_call', 'array_element'],
            'logical_operator': ['&&', '||'],
            'logical_operator1': ['!'],
            'more_log': ['logical_operator logical_operand more_log', 
                        'logical_operator logical_operator1 logical_operand', ''],
            'func_call': ['id_lit ( args )', ''],
            'args': ['args_val args_more', ''],
            'args_val': ['id_lit', 'scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
            'args_more': [', args args_more', ''],
            'treasures_mirror': ['1', '0'],
            'arithmetic_exp': ['arithmetic_operand arithmetic_operator arithmetic_operand more_arith'],
            'arithmetic_operand': ['id_lit', 'ocean_lit', 'treasures_lit', 'arithmetic_exp', 
                                 '( arithmetic_exp )', 'func_call', 'array_element'],
            'arithmetic_operator': ['+', '-', '/', '*', '%'],
            'more_arith': ['arithmetic_operator arithmetic_operand', ''],
            'relational_exp': ['relational_operand relational_operator relational_operand relational_more'],
            'relational_operand': ['id_lit', 'scroll_lit', 'treasures_lit', 'ocean_lit', '(arithmetic_exp)',
                                 'arithmetic_exp', 'func_call', 'array_element'],
            'relational_operator': ['relational_operator1', 'relational_operator2'],
            'relational_operator1': ['<', '>', '<=', '>='],
            'relational_operator2': ['==', '!='],
            'relational_more': ['relational_operator1 relational_operand', ''],
            'unary': ['id_lit unary_operator'],
            'unary_operator': ['++', '--'],
            'concat': ['string_operand + string_operand string_more'],
            'string_operand': ['scroll_lit', 'id_lit', 'rose_lit', 'array_element', 'toscroll(conver_value)'],
            'string_more': ['+ string_operand string_more', ''],
            'user-defined_func': ['spell return_type id_lit (param) { body ret_statement } user-defined_func', ''],
            'return_type': ['data_type', 'chamber'],
            'param': ['datatype id_lit param_more', ''],
            'param_more': [', datatype id_lit param_more', ''],
            'body': ['var_dec body', 'output body', 'func_call body', 'user-defined_func body',
                    'condi_statement body', 'for_loop body', 'coronation body', 'unary body',
                    'assignment_exp body', 'comments body', ''],
            'comments': ['single_line', 'multi_line'],
            'single_line': ['? scroll_lit'],
            'multi_line': ['? * scroll_lit * ?'],
            'ret_statement': ['return val1 ~', ''],
            'coronation': ['id_lit = val ~', ''],
            'condi_statement': ['if', 'while', 'do_while', ''],
            'for_loop': ['tale (loop_var ~ relational_exp ~ unary) { loop_body }', ''],
            'loop_var': ['treasures id_lit = loop_val', 'id_lit = loop_val', 'id_lit'],
            'loop_val': ['id_lit', 'treasures_lit'],
            'loop_body': ['body', 'if_break'],
            'if_break': ['cast ( if-elif_condition ) { body flow_control } elif_break else_break'],
            'elif_break': ['twist ( if-elif_condition ) { body flow_control }', ''],
            'else_break': ['curse { body flow_control }', ''],
            'flow_control': ['break ~', 'continue ~', ''],
            'do_while': ['believe { loop_body } forever (if-elif_condition) ~'],
            'if-elif_condition': ['id_lit', 'treasures_mirror', 'id_lit mirror_init', 'relational_exp',
                                'logical_exp', 'logical_operator1 ( if-elif_condition )'],
            'mirror_init': ['relational_operator2 mirror_lit', ''],
            'while': ['forever ( if-elif_condition ) { loop_body }'],
            'if': ['cast ( if-elif_condition ) { body } elif else'],
            'elif': ['twist( if-elif_condition ) { body } elif', ''],
            'else': ['curse { body }', ''],
            'output': ['granted( queen more_queen ) ~'],
            'queen': ['id_lit', 'scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit',
                     'phantom', 'set_precision', 'conversion_func ( conver_value )', 'concat',
                     'relational_exp', 'logical_exp', 'unary', 'arithmetic_exp', 'array_element'],
            'set_precision': ['" % . [ treasures_lit ] f "'],
            'more_queen': [', queen more_queen', ''],
            'data_type': ['scroll', 'treasures', 'mirror', 'ocean', 'rose'],
            'val': ['scroll_lit', 'treasures_lit', 'mirror_lit', 'ocean_lit', 'rose_lit', 'id_lit',
                   'phantom', 'concat', 'arithmetic_exp', 'input', 'type_conversion',
                   'relational_exp', 'logical_exp', 'treasures_mirror'],
            'val1': ['val', 'unary', 'assignment_exp'],
            'type_conversion': ['conversion_func ( conver_value )'],
            'conversion_func': ['toscroll', 'torose', 'totreasures', 'toocean'],
            'conver_value': ['scroll_lit', 'rose_lit', 'ocean_lit', 'treasures_lit', 'id_lit index'],
            'index': ['[ treasures_lit ] column1', ''],
            'column1': ['[ treasures_lit ]', ''],
            'input': ['wish ( scroll_lit )']
        }
        
        # Initialize sets
        self.first_sets = {}
        self.follow_sets = {}
        self.predict_sets = {}
        
        # Track terminals and non-terminals
        self.non_terminals = set(self.grammar.keys())
        self.terminals = self._get_terminals()

    # Rest of the class implementation remains the same as in previous artifact
    def _get_terminals(self):
        """Extract terminals from the grammar"""
        terminals = set()
        for productions in self.grammar.values():
            for prod in productions:
                if prod:  # Skip empty productions
                    symbols = prod.split()
                    for symbol in symbols:
                        if symbol not in self.non_terminals and symbol not in ['~', '{', '}', '[', ']', '(', ')', ',', '"', '*', '?', '+', '=']:
                            terminals.add(symbol)
        return terminals

    def compute_first_sets(self):
        """Compute FIRST sets for all non-terminals"""
        # Initialize FIRST sets
        self.first_sets = {nt: set() for nt in self.non_terminals}
        
        while True:
            updated = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    if not production:  # Empty production
                        if '' not in self.first_sets[nt]:
                            self.first_sets[nt].add('')
                            updated = True
                        continue
                    
                    symbols = production.split()
                    first_symbol = symbols[0]
                    
                    if first_symbol in self.terminals or first_symbol in ['~', '{', '}', '[', ']', '(', ')', ',', '"', '*', '?', '+', '=']:
                        if first_symbol not in self.first_sets[nt]:
                            self.first_sets[nt].add(first_symbol)
                            updated = True
                    elif first_symbol in self.non_terminals:
                        for symbol in self.first_sets[first_symbol]:
                            if symbol not in self.first_sets[nt]:
                                self.first_sets[nt].add(symbol)
                                updated = True
            
            if not updated:
                break

    def compute_follow_sets(self):
        """Compute FOLLOW sets for all non-terminals"""
        # Initialize FOLLOW sets
        self.follow_sets = {nt: set() for nt in self.non_terminals}
        self.follow_sets['program'].add('$')  # Add $ to start symbol
        
        while True:
            updated = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    if not production:
                        continue
                        
                    symbols = production.split()
                    for i, symbol in enumerate(symbols):
                        if symbol in self.non_terminals:
                            # Get remaining symbols after current symbol
                            remaining = symbols[i + 1:]
                            
                            if not remaining:  # Nothing follows
                                for follow_symbol in self.follow_sets[nt]:
                                    if follow_symbol not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(follow_symbol)
                                        updated = True
                            else:
                                first_of_remaining = self._compute_first_of_string(remaining)
                                for first_symbol in first_of_remaining:
                                    if first_symbol != '' and first_symbol not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(first_symbol)
                                        updated = True
                                
                                if '' in first_of_remaining:
                                    for follow_symbol in self.follow_sets[nt]:
                                        if follow_symbol not in self.follow_sets[symbol]:
                                            self.follow_sets[symbol].add(follow_symbol)
                                            updated = True
            
            if not updated:
                break

    def _compute_first_of_string(self, symbols):
        """Compute FIRST set for a string of symbols"""
        if not symbols:
            return {''}
            
        first_set = set()
        all_nullable = True
        
        for symbol in symbols:
            if symbol in self.terminals or symbol in ['~', '{', '}', '[', ']', '(', ')', ',', '"', '*', '?', '+', '=']:
                first_set.add(symbol)
                all_nullable = False
                break
            elif symbol in self.non_terminals:
                symbol_first = self.first_sets[symbol]
                first_set.update(s for s in symbol_first if s != '')
                if '' not in symbol_first:
                    all_nullable = False
                    break
        
        if all_nullable:
            first_set.add('')
            
        return first_set

    def compute_predict_sets(self):
        """Compute PREDICT sets for all productions"""
        self.predict_sets = {}
        
        for nt in self.non_terminals:
            for production in self.grammar[nt]:
                key = (nt, production)
                self.predict_sets[key] = set()
                
                if not production:  # Empty production
                    self.predict_sets[key].update(self.follow_sets[nt])
                else:
                    first_of_prod = self._compute_first_of_string(production.split())
                    self.predict_sets[key].update(s for s in first_of_prod if s != '')
                    if '' in first_of_prod:
                        self.predict_sets[key].update(self.follow_sets[nt])

    def generate_sets(self):
        """Generate all sets and return them"""
        self.compute_first_sets()
        self.compute_follow_sets()
        self.compute_predict_sets()
        return {
            'FIRST': self.first_sets,
            'FOLLOW': self.follow_sets,
            'PREDICT': self.predict_sets
        }

def main():
    cfg_processor = CFGProcessor()
    sets = cfg_processor.generate_sets()
    
    # Print FIRST sets
    print("\nFIRST Sets:")
    for nt, first_set in sorted(sets['FIRST'].items()):
        print(f"FIRST({nt}) = {first_set}")
    
    # Print FOLLOW sets
    print("\nFOLLOW Sets:")
    for nt, follow_set in sorted(sets['FOLLOW'].items()):
        print(f"FOLLOW({nt}) = {follow_set}")
    
    # Print PREDICT sets
    print("\nPREDICT Sets:")
    for (nt, production), predict_set in sorted(sets['PREDICT'].items()):
        prod_str = production if production else "ε"
        print(f"PREDICT({nt} -> {prod_str}) = {predict_set}")

if __name__ == "__main__":
    main()