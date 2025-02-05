# # # class CFGProcessor:
# # #     def __init__(self):
# # #         self.grammar = {
# # #             '<program>': [
# # #                 ['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'id_lit', '{', '<body>', 'return', '0', '~', '}', 'reign', '~']
# # #             ],
# # #             '<global_dec>': [
# # #                 ['<var_dec>', '<global_dec>'],
# # #                 []
# # #             ],
# # #             '<var_dec>': [
# # #                 ['<data_type>', 'id_lit', '<vardec_def>'],
# # #                 []
# # #             ],
# # #             '<vardec_def>': [
# # #                 ['<initialization>', '<vardec_more>', '~'],
# # #                 ['[', 'num', ']', '<column>', '<array_initialization>', '<array_more>', '~']
# # #             ],
# # #             '<initialization>': [
# # #                 ['=', '<val>'],
# # #                 []
# # #             ],
# # #             '<vardec_more>': [
# # #                 [',', 'id_lit', '<initialization>', '<vardec_more>'],
# # #                 []
# # #             ],
# # #             '<column>': [
# # #                 ['[', 'num', ']'],
# # #                 []
# # #             ],
# # #             '<array_initialization>': [
# # #                 ['=', '<array_list>'],
# # #                 []
# # #             ],
# # #             '<array_list>': [
# # #                 ['<single>'],
# # #                 ['<multi>']
# # #             ],
# # #             '<single>': [
# # #                 ['{', '<array_lit>', '<list_more>', '}']
# # #             ],
# # #             '<multi>': [
# # #                 ['{', '<single>', '<multi_more>', '}'],
# # #                 []
# # #             ],
# # #             '<multi_more>': [
# # #                 [',', '<single>', '<multi_more>'],
# # #                 []
# # #             ],
# # #             '<list_more>': [
# # #                 [',', '<array_lit>', '<list_more>'],
# # #                 []
# # #             ],
# # #             '<array_more>': [
# # #                 [',', 'id_lit', '[', 'num', ']', '<column>', '<array_initialization>'],
# # #                 []
# # #             ],
# # #             '<array_lit>': [
# # #                 ['scroll_lit'], ['rose_lit'], ['treasures_lit'], ['ocean_lit'], ['mirror_lit']
# # #             ],
# # #             '<assignment_exp>': [
# # #                 ['id_lit', '<assignment_operator>', '<assignment_operand>', '~']
# # #             ],
# # #             '<assignment_operator>': [
# # #                 ['+='], ['-='], ['*='], ['/='], ['%=']
# # #             ],
# # #             '<assignment_operand>': [
# # #                 ['id_lit'], ['treasures_lit'], ['ocean_lit'], ['<array_element>'], ['<arithmetic_exp>']
# # #             ],
# # #             '<array_element>': [
# # #                 ['id_lit', '<index>']
# # #             ],
# # #             '<logical_exp>': [
# # #                 ['<logical_operand>', '<logical_operator>', '<logical_operand>', '<more_log>'],
# # #                 ['<logical_operator1>', '<logical_operand>', '<more_log>']
# # #             ],
# # #             '<logical_operand>': [
# # #                 ['id_lit'], ['mirror_lit'], ['<treasures_mirror>'], ['<relational_exp>'],
# # #                 ['(', '<relational_exp>', ')'], ['<func_call>'], ['<array_element>']
# # #             ],
# # #             '<logical_operator>': [
# # #                 ['&&'], ['||']
# # #             ],
# # #             '<logical_operator1>': [
# # #                 ['!']
# # #             ],
# # #             '<more_log>': [
# # #                 ['<logical_operator>', '<logical_operand>', '<more_log>'],
# # #                 ['<logical_operator>', '<logical_operator1>', '<logical_operand>'],
# # #                 []
# # #             ],
# # #             '<func_call>': [
# # #                 ['id_lit', '(', '<args>', ')'],
# # #                 []
# # #             ],
# # #             '<args>': [
# # #                 ['<args_val>', '<args_more>'],
# # #                 []
# # #             ],
# # #             '<args_val>': [
# # #                 ['id_lit'], ['scroll_lit'], ['rose_lit'], ['treasures_lit'], 
# # #                 ['ocean_lit'], ['mirror_lit']
# # #             ],
# # #             '<args_more>': [
# # #                 [',', '<args>', '<args_more>'],
# # #                 []
# # #             ],
# # #             '<treasures_mirror>': [
# # #                 ['1'], ['0']
# # #             ],
# # #             '<arithmetic_exp>': [
# # #                 ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>']
# # #             ],
# # #             '<arithmetic_operand>': [
# # #                 ['id_lit'], ['ocean_lit'], ['treasures_lit'], ['<arithmetic_exp>'],
# # #                 ['(', '<arithmetic_exp>', ')'], ['<func_call>'], ['<array_element>']
# # #             ],
# # #             '<arithmetic_operator>': [
# # #                 ['+'], ['-'], ['/'], ['*'], ['%']
# # #             ],
# # #             '<more_arith>': [
# # #                 ['<arithmetic_operator>', '<arithmetic_operand>'],
# # #                 []
# # #             ],
# # #             '<relational_exp>': [
# # #                 ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>']
# # #             ],
# # #             '<relational_operand>': [
# # #                 ['id_lit'], ['scroll_lit'], ['treasures_lit'], ['ocean_lit'],
# # #                 ['(', '<arithmetic_exp>', ')'], ['<arithmetic_exp>'], 
# # #                 ['<func_call>'], ['<array_element>']
# # #             ],
# # #             '<relational_operator>': [
# # #                 ['<relational_operator1>'], ['<relational_operator2>']
# # #             ],
# # #             '<relational_operator1>': [
# # #                 ['<'], ['>'], ['<='], ['>=']
# # #             ],
# # #             '<relational_operator2>': [
# # #                 ['=='], ['!=']
# # #             ],
# # #             '<relational_more>': [
# # #                 ['<relational_operator1>', '<relational_operand>'],
# # #                 []
# # #             ],
# # #             '<unary>': [
# # #                 ['id_lit', '<unary_operator>']
# # #             ],
# # #             '<unary_operator>': [
# # #                 ['++'], ['--']
# # #             ],
# # #             '<concat>': [
# # #                 ['<string_operand>', '+', '<string_operand>', '<string_more>']
# # #             ],
# # #             '<string_operand>': [
# # #                 ['scroll_lit'], ['id_lit'], ['rose_lit'], ['<array_element>'],
# # #                 ['toscroll', '(', '<conver_value>', ')']
# # #             ],
# # #             '<string_more>': [
# # #                 ['+', '<string_operand>', '<string_more>'],
# # #                 []
# # #             ],
# # #             '<user-defined_func>': [
# # #                 ['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>'],
# # #                 []
# # #             ],
# # #             '<return_type>': [
# # #                 ['<data_type>'], ['chamber']
# # #             ],
# # #             '<param>': [
# # #                 ['<datatype>', 'id_lit', '<param_more>'],
# # #                 []
# # #             ],
# # #             '<param_more>': [
# # #                 [',', '<datatype>', 'id_lit', '<param_more>'],
# # #                 []
# # #             ],
# # #             '<body>': [
# # #                 ['<var_dec>', '<body>'], ['<output>', '<body>'], ['<func1_call>', '<body>'],
# # #                 ['<user-defined_func>', '<body>'], ['<condi_statement>', '<body>'],
# # #                 ['<for_loop>', '<body>'], ['<coronation>', '<body>'], ['<unary>', '<body>'],
# # #                 ['<assignment_exp>', '<body>'], ['<comments>', '<body>'],
# # #                 []
# # #             ],
# # #             '<func1_call>': [
# # #                 ['id_lit', '(', '<args>', ')', '~']
# # #             ],
# # #             '<comments>': [
# # #                 ['<single_line>'], ['<multi_line>']
# # #             ],
# # #             '<single_line>': [
# # #                 ['?', 'scroll_lit']
# # #             ],
# # #             '<multi_line>': [
# # #                 ['?', '*', 'scroll_lit', '*', '?']
# # #             ],
# # #             '<ret_statement>': [
# # #                 ['return', '<val1>', '~'],
# # #                 []
# # #             ],
# # #             '<coronation>': [
# # #                 ['id_lit', '=', '<val>', '~']
# # #             ],
# # #             '<condi_statement>': [
# # #                 ['<if>'], ['<while>'], ['<do_while>'],
# # #                 []
# # #             ],
# # #             '<for_loop>': [
# # #                 ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}']
# # #             ],
# # #             '<loop_var>': [
# # #                 ['treasures', 'id_lit', '=', '<loop_val>'],
# # #                 ['id_lit', '=', '<loop_val>'],
# # #                 ['id_lit']
# # #             ],
# # #             '<loop_val>': [
# # #                 ['id_lit'], ['treasures_lit']
# # #             ],
# # #             '<loop_body>': [
# # #                 ['<body>'], ['<if_break>']
# # #             ],
# # #             '<if_break>': [
# # #                 ['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>', '<else_break>']
# # #             ],
# # #             '<elif_break>': [
# # #                 ['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}'],
# # #                 []
# # #             ],
# # #             '<else_break>': [
# # #                 ['curse', '{', '<body>', '<flow_control>', '}'],
# # #                 []
# # #             ],
# # #             '<flow_control>': [
# # #                 ['break', '~'], ['continue', '~'],
# # #                 []
# # #             ],
# # #             '<do_while>': [
# # #                 ['believe', '{', '<loop_body>', '}', 'forever', '(', '<if-elif_condition>', ')', '~']
# # #             ],
# # #             '<if-elif_condition>': [
# # #                 ['id_lit'], ['<treasures_mirror>'], ['id_lit', '<mirror_init>'],
# # #                 ['<relational_exp>'], ['<logical_exp>'],
# # #                 ['<logical_operator1>', '(', '<if-elif_condition>', ')']
# # #             ],
# # #             '<mirror_init>': [
# # #                 ['<relational_operator2>', 'mirror_lit'],
# # #                 []
# # #             ],
# # #             '<while>': [
# # #                 ['forever', '(', '<if-elif_condition>', ')', '{', '<loop_body>', '}']
# # #             ],
# # #             '<if>': [
# # #                 ['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>', '<else>']
# # #             ],
# # #             '<elif>': [
# # #                 ['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>'],
# # #                 []
# # #             ],
# # #             '<else>': [
# # #                 ['curse', '{', '<body>', '}'],
# # #                 []
# # #             ],
# # #             '<output>': [
# # #                 ['granted', '(', '<queen>', '<more_queen>', ')', '~']
# # #             ],
# # #             '<queen>': [
# # #                 ['id_lit'], ['scroll_lit'], ['rose_lit'], ['treasures_lit'], ['ocean_lit'],
# # #                 ['mirror_lit'], ['phantom'], ['<set_precision>'],
# # #                 ['conversion_func', '(', '<conver_value>', ')'], ['<concat>'],
# # #                 ['<relational_exp>'], ['<logical_exp>'], ['<unary>'],
# # #                 ['<arithmetic_exp>'], ['<array_element>']
# # #             ],
# # #             '<set_precision>': [
# # #                 ['"', '%', '.', '[', 'treasures_lit', ']', 'f', '"']
# # #             ],
# # #             '<more_queen>': [
# # #                 [',', '<queen>', '<more_queen>'],
# # #                 []
# # #             ],
# # #             '<data_type>': [
# # #                 ['scroll'], ['treasures'], ['mirror'], ['ocean'], ['rose']
# # #             ],
# # #             '<val>': [
# # #                 ['scroll_lit'], ['treasures_lit'], ['mirror_lit'], ['ocean_lit'],
# # #                 ['rose_lit'], ['id_lit'], ['phantom'], ['<concat>'],
# # #                 ['<arithmetic_exp>'], ['<input>'], ['<type_conversion>'],
# # #                 ['<relational_exp>'], ['<logical_exp>'], ['<treasures_mirror>']
# # #             ],
# # #             '<val1>': [
# # #                 ['<val>'], ['<unary>'], ['<assignment_exp>']
# # #             ],
# # #             '<type_conversion>': [
# # #                 ['<conversion_func>', '(', '<conver_value>', ')']
# # #             ],
# # #             '<conversion_func>': [
# # #                 ['toscroll'], ['torose'], ['totreasures'], ['toocean']
# # #             ],
# # #             '<conver_value>': [
# # #                 ['scroll_lit'], ['rose_lit'], ['ocean_lit'], ['treasures_lit'],
# # #                 ['id_lit', '<index>']
# # #             ],
# # #             '<index>': [
# # #                 ['[', 'treasures_lit', ']', '<column1>'],
# # #                 []
# # #             ],
# # #             '<column1>': [
# # #                 ['[', 'treasures_lit', ']'],
# # #                 []
# # #             ],
# # #             '<input>': [
# # #                 ['wish', '(', 'scroll_lit', ')']
# # #             ]
# # #         }
        
# # #         self.first_sets = {}
# # #         self.follow_sets = {}
# # #         self.predict_sets = {}
# # #         self.non_terminals = set(self.grammar.keys())
# # #         self.terminals = self._get_terminals()
        
# # #     def _get_terminals(self):
# # #         terminals = set()
# # #         for productions in self.grammar.values():
# # #             for prod in productions:
# # #                 for symbol in prod:
# # #                     if (not isinstance(symbol, str) or 
# # #                         not symbol.startswith('<') and 
# # #                         not symbol.endswith('>') and 
# # #                         symbol not in ['~', '{', '}', '[', ']', '(', ')', ',', '"', '*', '?', '+', '=']):
# # #                         terminals.add(symbol)
# # #         return terminals

# # #     def compute_first_sets(self):
# # #         """Compute FIRST sets for all non-terminals"""
# # #         # Initialize FIRST sets
# # #         self.first_sets = {nt: set() for nt in self.non_terminals}
        
# # #         changed = True
# # #         while changed:
# # #             changed = False
            
# # #             for non_terminal in self.non_terminals:
# # #                 # For each production of the non-terminal
# # #                 for production in self.grammar[non_terminal]:
# # #                     if not production:  # Empty production
# # #                         if '' not in self.first_sets[non_terminal]:
# # #                             self.first_sets[non_terminal].add('')
# # #                             changed = True
# # #                         continue

# # #                     # Process each symbol in the production
# # #                     nullable = True
# # #                     for symbol in production:
# # #                         # If it's a terminal or special symbol
# # #                         if symbol not in self.non_terminals:
# # #                             self.first_sets[non_terminal].add(symbol)
# # #                             nullable = False
# # #                             break
                        
# # #                         # If it's a non-terminal
# # #                         first_set = self.first_sets[symbol]
# # #                         self.first_sets[non_terminal].update(
# # #                             x for x in first_set if x != ''
# # #                         )
                        
# # #                         if '' not in first_set:
# # #                             nullable = False
# # #                             break
                    
# # #                     if nullable and '' not in self.first_sets[non_terminal]:
# # #                         self.first_sets[non_terminal].add('')
# # #                         changed = True

# # #     def compute_follow_sets(self):
# # #         """Compute FOLLOW sets for all non-terminals"""
# # #         # Initialize FOLLOW sets
# # #         self.follow_sets = {nt: set() for nt in self.non_terminals}
# # #         self.follow_sets['<program>'].add('$')  # Add end marker to start symbol
        
# # #         changed = True
# # #         while changed:
# # #             changed = False
            
# # #             for non_terminal in self.non_terminals:
# # #                 for production_nt in self.non_terminals:
# # #                     for production in self.grammar[production_nt]:
# # #                         if not production:  # Skip empty productions
# # #                             continue
                            
# # #                         # Find all occurrences of non_terminal in production
# # #                         for i, symbol in enumerate(production):
# # #                             if symbol == non_terminal:
# # #                                 # Get the rest of the production after non_terminal
# # #                                 rest = production[i + 1:]
                                
# # #                                 if not rest:  # Nothing follows
# # #                                     # Add FOLLOW(production_nt) to FOLLOW(non_terminal)
# # #                                     for follow_symbol in self.follow_sets[production_nt]:
# # #                                         if follow_symbol not in self.follow_sets[non_terminal]:
# # #                                             self.follow_sets[non_terminal].add(follow_symbol)
# # #                                             changed = True
# # #                                 else:
# # #                                     # Compute FIRST of the rest of the production
# # #                                     first_of_rest = self._compute_first_of_string(rest)
                                    
# # #                                     # Add all non-empty symbols from FIRST(rest)
# # #                                     for first_symbol in first_of_rest:
# # #                                         if first_symbol != '' and first_symbol not in self.follow_sets[non_terminal]:
# # #                                             self.follow_sets[non_terminal].add(first_symbol)
# # #                                             changed = True
                                    
# # #                                     # If rest can derive empty, add FOLLOW(production_nt)
# # #                                     if '' in first_of_rest:
# # #                                         for follow_symbol in self.follow_sets[production_nt]:
# # #                                             if follow_symbol not in self.follow_sets[non_terminal]:
# # #                                                 self.follow_sets[non_terminal].add(follow_symbol)
# # #                                                 changed = True

# # #     def _compute_first_of_string(self, symbols):
# # #         """Compute FIRST set for a sequence of symbols"""
# # #         if not symbols:
# # #             return {''}
        
# # #         first_set = set()
        
# # #         # Check if the entire sequence can derive empty
# # #         all_nullable = True
        
# # #         for symbol in symbols:
# # #             # If it's a terminal or special symbol
# # #             if symbol not in self.non_terminals:
# # #                 first_set.add(symbol)
# # #                 all_nullable = False
# # #                 break
            
# # #             # If it's a non-terminal
# # #             symbol_first = self.first_sets[symbol]
# # #             first_set.update(x for x in symbol_first if x != '')
            
# # #             if '' not in symbol_first:
# # #                 all_nullable = False
# # #                 break
        
# # #         if all_nullable:
# # #             first_set.add('')
        
# # #         return first_set

# # #     def compute_predict_sets(self):
# # #         """Compute PREDICT sets for all productions"""
# # #         self.predict_sets = {}
        
# # #         for non_terminal in self.non_terminals:
# # #             for production in self.grammar[non_terminal]:
# # #                 key = (non_terminal, tuple(production))
                
# # #                 if not production:  # Empty production
# # #                     # PREDICT(A → ε) = FOLLOW(A)
# # #                     self.predict_sets[key] = self.follow_sets[non_terminal].copy()
# # #                 else:
# # #                     # PREDICT(A → α) = FIRST(α)
# # #                     first_of_prod = self._compute_first_of_string(production)
# # #                     self.predict_sets[key] = set(s for s in first_of_prod if s != '')
                    
# # #                     # If α can derive empty, add FOLLOW(A)
# # #                     if '' in first_of_prod:
# # #                         self.predict_sets[key].update(self.follow_sets[non_terminal])

# # #     def generate_sets(self):
# # #         """Generate and return all sets"""
# # #         self.compute_first_sets()
# # #         self.compute_follow_sets()
# # #         self.compute_predict_sets()
        
# # #         # Format the sets for better readability
# # #         formatted_sets = {
# # #             'FIRST': {k: sorted(v) for k, v in self.first_sets.items()},
# # #             'FOLLOW': {k: sorted(v) for k, v in self.follow_sets.items()},
# # #             'PREDICT': {str(k): sorted(v) for k, v in self.predict_sets.items()}
# # #         }
        
# # #         return formatted_sets

# # # def format_production(prod):
# # #     """Format a production rule for display"""
# # #     if not prod:
# # #         return "ε"
# # #     return " ".join(str(symbol) for symbol in prod)

# # # def main():
# # #     cfg_processor = CFGProcessor()
# # #     sets = cfg_processor.generate_sets()
    
# # #     # Print results in a structured format
# # #     print("\nFIRST Sets:")
# # #     for nt in sorted(sets['FIRST'].keys()):
# # #         print(f"FIRST({nt}) = {{{', '.join(sorted(sets['FIRST'][nt]))}}}")
    
# # #     print("\nFOLLOW Sets:")
# # #     for nt in sorted(sets['FOLLOW'].keys()):
# # #         print(f"FOLLOW({nt}) = {{{', '.join(sorted(sets['FOLLOW'][nt]))}}}")
    
# # #     print("\nPREDICT Sets:")
# # #     for production, predict_set in sorted(sets['PREDICT'].items()):
# # #         print(f"PREDICT({production}) = {{{', '.join(sorted(predict_set))}}}")

# # # if __name__ == "__main__":
# # #     main()

from collections import defaultdict

class CFG:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set(productions.keys())
        self.terminals = set()
        for rhs_list in productions.values():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol not in self.non_terminals and symbol != 'λ':
                        self.terminals.add(symbol)

    def compute_first(self):
        first = defaultdict(set)

        # Initialize FIRST for terminals
        for terminal in self.terminals:
            first[terminal].add(terminal)

        # Initialize FIRST for non-terminals
        for non_terminal in self.non_terminals:
            first[non_terminal] = set()

        changed = True
        while changed:
            changed = False
            for non_terminal, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    for symbol in rhs:
                        if symbol in self.terminals:
                            if symbol not in first[non_terminal]:
                                first[non_terminal].add(symbol)
                                changed = True
                            break
                        elif symbol in self.non_terminals:
                            before_size = len(first[non_terminal])
                            first[non_terminal].update(first[symbol] - {'λ'})
                            if before_size != len(first[non_terminal]):
                                changed = True
                            if 'λ' not in first[symbol]:
                                break
                    else:
                        if 'λ' not in first[non_terminal]:
                            first[non_terminal].add('λ')
                            changed = True
        return first

    def compute_follow(self, first):
        follow = defaultdict(set)
        start_symbol = next(iter(self.productions))
        follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for non_terminal, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    for i, symbol in enumerate(rhs):
                        if symbol in self.non_terminals:
                            next_symbols = rhs[i+1:]
                            if not next_symbols:
                                before_size = len(follow[symbol])
                                follow[symbol].update(follow[non_terminal])
                                if before_size != len(follow[symbol]):
                                    changed = True
                            else:
                                first_of_next = self.compute_first_of_sequence(next_symbols, first)
                                if 'λ' in first_of_next:
                                    before_size = len(follow[symbol])
                                    follow[symbol].update(first_of_next - {'λ'})
                                    follow[symbol].update(follow[non_terminal])
                                    if before_size != len(follow[symbol]):
                                        changed = True
                                else:
                                    before_size = len(follow[symbol])
                                    follow[symbol].update(first_of_next)
                                    if before_size != len(follow[symbol]):
                                        changed = True
        return follow

    def compute_first_of_sequence(self, sequence, first):
        result = set()
        for symbol in sequence:
            result.update(first[symbol] - {'λ'})
            if 'λ' not in first[symbol]:
                break
        else:
            result.add('λ')
        return result

    def compute_predict(self, first, follow):
        predict = {}
        for non_terminal, rhs_list in self.productions.items():
            predict[non_terminal] = {}
            for rhs in rhs_list:
                first_of_rhs = self.compute_first_of_sequence(rhs, first)
                predict_set = first_of_rhs - {'λ'}
                if 'λ' in first_of_rhs:
                    predict_set.update(follow[non_terminal])
                predict[non_terminal][tuple(rhs)] = predict_set
        return predict

# Define your CFG productions
productions = {
    '<program>': [['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'id_lit', '{', '<body>', 'return', '0', '~', '}', 'reign', '~']],
    
    '<global_dec>': [
        ['<var_dec>', '<global_dec>'],
        ['λ']
    ],
    
    '<var_dec>': [
        ['<const>','<data_type>', 'id_lit', '<vardec_def>'],
        ['λ']
    ],
    
    '<vardec_def>': [
        ['<initialization>', '<vardec_more>', '~'],
        ['[', 'num', ']', '<column>', '<array_initialization>', '<array_more>', '~']
    ],
    
    '<initialization>': [
        ['=', '<val>'],
        ['λ']
    ],
    
    '<vardec_more>': [
        [',', 'id_lit', '<initialization>', '<vardec_more>'],
        ['λ']
    ],

    '<const>': [
        ['dynasty'],
        ['λ']
    ],
    
    '<column>': [
        ['[', 'num', ']'],
        ['λ']
    ],
    
    '<array_initialization>': [
        ['=', '<array_list>'],
        ['λ']
    ],
    
    '<array_list>': [
        ['<single>'],
        ['<multi>']
    ],
    
    '<single>': [
        ['{', '<array_lit>', '<list_more>', '}']
    ],
    
    '<multi>': [
        ['{', '<single>', '<multi_more>', '}'],
        ['λ']
    ],
    
    '<multi_more>': [
        [',', '<single>', '<multi_more>'],
        ['λ']
    ],
    
    '<list_more>': [
        [',', '<array_lit>', '<list_more>'],
        ['λ']
    ],
    
    '<array_more>': [
        [',', 'id_lit', '[', 'num', ']', '<column>', '<array_initialization>', '<array_more>'],
        ['λ']
    ],
    
    '<array_lit>': [
        ['scroll_lit'],
        ['rose_lit'],
        ['treasures_lit'],
        ['ocean_lit'],
        ['mirror_lit']
    ],
    
    '<assignment_exp>': [
        ['id_lit', '<assignment_operator>', '<assignment_operand>']
    ],
    
    '<assignment_operator>': [
        ['+='],
        ['-='],
        ['*='],
        ['/='],
        ['%=']
    ],
    
    '<assignment_operand>': [
        ['id_lit'],
        ['treasures_lit'],
        ['ocean_lit'],
        ['<array_element>'],
        ['<arithmetic_exp>'],
        ['<func_call>']
    ],
    
    '<array_element>': [
        ['id_lit', '<index>']
    ],
    
    '<logical_exp>': [
        ['<logical_operand>', '<logical_operator>', '<logical_operand>', '<more_log>'],
        ['<logical_operator1>', '<logical_operand>', '<more_log>']
    ],
    
    '<logical_operand>': [
        ['id_lit'],
        ['mirror_lit'],
        ['<treasures_mirror>'],
        ['<relational_exp>'],
        ['(', '<relational_exp>', ')'],
        ['<func_call>'],
        ['<array_element>']
    ],
    
    '<logical_operator>': [
        ['&&'],
        ['||']
    ],
    
    '<logical_operator1>': [
        ['!']
    ],
    
    '<more_log>': [
        ['<logical_operator>', '<logical_operand>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['λ']
    ],
    
    '<func_call>': [
        ['id_lit', '(', '<args>', ')']
    ],
    
    '<args>': [
        ['<args_val>', '<args_more>'],
        ['λ']
    ],
    
    '<args_val>': [
        ['id_lit'],
        ['scroll_lit'],
        ['rose_lit'],
        ['treasures_lit'],
        ['ocean_lit'],
        ['mirror_lit']
    ],
    
    '<args_more>': [
        [',', '<args>', '<args_more>'],
        ['λ']
    ],
    
    '<treasures_mirror>': [
        ['1'],
        ['0']
    ],
    
    '<arithmetic_exp>' : [
        ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>']
    ],

    '<arithmetic_operator>': [
        ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>']
    ],
    
    '<arithmetic_operand>': [
        ['id_lit'],
        ['ocean_lit'],
        ['treasures_lit'],
        ['<arithmetic_exp>'],
        ['(', '<arithmetic_exp>', ')'],
        ['<func_call>'],
        ['<array_element>']
    ],
    
    '<arithmetic_operator>': [
        ['+'],
        ['-'],
        ['/'],
        ['*'],
        ['%']
    ],
    
    '<more_arith>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
        ['λ']
    ],
    
    '<relational_exp>': [
        ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>']
    ],
    
    '<relational_operand>': [
        ['id_lit'],
        ['scroll_lit'],
        ['treasures_lit'],
        ['ocean_lit'],
        ['(', '<arithmetic_exp>', ')'],
        ['<arithmetic_exp>'],
        ['<func_call>'],
        ['<array_element>']
    ],
    
    '<relational_operator>': [
        ['<'],
        ['>'],
        ['<='],
        ['>='],
        ['=='],
        ['!=']
    ],
    
    '<relational_more>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['λ']
    ],
    
    '<unary>': [
        ['id_lit', '<unary_operator>']
    ],
    
    '<unary_operator>': [
        ['++'],
        ['--']
    ],
    
    '<concat>': [
        ['<string_operand>', '+', '<string_operand>', '<string_more>']
    ],
    
    '<string_operand>': [
        ['scroll_lit'],
        ['id_lit'],
        ['rose_lit'],
        ['<array_element>'],
        ['<func_call>'],
        ['toscroll', '(', '<conver_value>', ')']
    ],
    
    '<string_more>': [
        ['+', '<string_operand>', '<string_more>'],
        ['λ']
    ],
    
    '<user-defined_func>': [
        ['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>'],
        ['λ']
    ],
    
    '<return_type>': [
        ['<data_type>'],
        ['chamber']
    ],
    
    '<param>': [
        ['<data_type>', 'id_lit', '<param_more>'],
        ['λ']
    ],
    
    '<param_more>': [
        [',', '<data_type>', 'id_lit', '<param_more>'],
        ['λ']
    ],
    
    '<body>': [
        ['<var_dec>', '<body>'],
        ['<output>', '<body>'],
        ['<func_call>', '~', '<body>'],
        ['<user-defined_func>', '<body>'],
        ['<condi_statement>', '<body>'],
        ['<for_loop>', '<body>'],
        ['<coronation>', '<body>'],
        ['<unary>', '~', '<body>'],
        ['<assignment_exp>', '~', '<body>'],
        ['<comments>', '<body>'],
        ['λ']
    ],
    
    '<comments>': [
        ['<single_line>'],
        ['<multi_line>']
    ],
    
    '<single_line>': [
        ['?', 'scroll_lit']
    ],
    
    '<multi_line>': [
        ['?', '*', 'scroll_lit', '*', '?']
    ],
    
    '<ret_statement>': [
        ['return', '<val1>', '~'],
        ['λ']
    ],
    
    '<coronation>': [
        ['id_lit', '=', '<val>', '~']
    ],
    
    '<condi_statement>': [
        ['<if>'],
        ['<while>'],
        ['<do_while>'],
        ['λ']
    ],
    
    '<for_loop>': [
        ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}']
    ],
    
    '<loop_var>': [
        ['treasures', 'id_lit', '=', '<loop_val>'],
        ['id_lit', '=', '<loop_val>'],
        ['id_lit']
    ],
    
    '<loop_val>': [
        ['id_lit'],
        ['treasures_lit']
    ],
    
    '<loop_body>': [
        ['<body>'],
        ['<if_break>']
    ],
    
    '<if_break>': [
        ['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>', '<else_break>']
    ],
    
    '<elif_break>': [
        ['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>'],
        ['λ']
    ],
    
    '<else_break>': [
        ['curse', '{', '<body>', '<flow_control>', '}'],
        ['λ']
    ],
    
    '<flow_control>': [
        ['break', '~'],
        ['continue', '~'],
        ['λ']
    ],
    
    '<do_while>': [
        ['believe', '{', '<loop_body>', '}', 'forever', '(', 'if-elif_condition', ')', '~']
    ],
    
    '<if-elif_condition>': [
        ['id_lit'],
        ['<treasures_mirror>'],
        ['id_lit', '<mirror_init>'],
        ['<relational_exp>'],
        ['<logical_exp>'],
        ['<logical_operator1>', '(', '<if--elif_condition>', ')'],
        ['<func_call>']
    ],
    
    '<mirror_init>': [
        ['==', 'mirror_lit'],
        ['!=', 'mirror_lit'],
        ['λ']
    ],
    
    '<while>': [
        ['forever', '(', 'if-elif_condition', ')', '{', '<loop_body>', '}']
    ],
    
    '<if>': [
        ['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>', '<else>']
    ],
    
    '<elif>': [
        ['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>'],
        ['λ']
    ],
    
    '<else>': [
        ['curse', '{', '<body>', '}'],
        ['λ']
    ],
    
    '<output>': [
        ['granted', '(', '<queen>', '<more_queen>', ')', '~']
    ],
    
    '<queen>': [
        ['id_lit'],
        ['scroll_lit'],
        ['rose_lit'],
        ['treasures_lit'],
        ['ocean_lit'],
        ['mirror_lit'],
        ['phantom'],
        ['<set_precision>'],
        ['<conversion_func>', '(', '<conver_value>', ')'],
        ['<concat>'],
        ['<relational_exp>'],
        ['<logical_exp>'],
        ['<unary>'],
        ['<arithmetic_exp>'],
        ['<array_element>'],
        ['<func_call>']
    ],
    
    '<set_precision>': [
        ['"', '%', '.', '"', '[', 'treasures_lit', ']', 'f']
    ],
    
    '<more_queen>': [
        [',', '<queen>', '<more_queen>'],
        ['λ']
    ],
    
    '<data_type>': [
        ['scroll'],
        ['treasures'],
        ['mirror'],
        ['ocean'],
        ['rose']
    ],
    
    '<val>': [
        ['scroll_lit'],
        ['treasures_lit'],
        ['mirror_lit'],
        ['ocean_lit'],
        ['rose_lit'],
        ['id_lit'],
        ['phantom'],
        ['<concat>'],
        ['<arithmetic_exp>'],
        ['<input>'],
        ['<type_conversion>'],
        ['<relational_exp>'],
        ['<logical_exp>'],
        ['<treasures_mirror>'],
        ['<func_call>']
    ],
    
    '<val1>': [
        ['<val>'],
        ['<unary>'],
        ['<assignment_exp>']
    ],
    
    '<type_conversion>': [
        ['<conversion_func>', '(', '<conver_value>', ')']
    ],
    
    '<conversion_func>': [
        ['toscroll'],
        ['torose'],
        ['totreasures'],
        ['toocean']
    ],
    
    '<conver_value>': [
        ['scroll_lit'],
        ['rose_lit'],
        ['ocean_lit'],
        ['treasures_lit'],
        ['id_lit', '<index>'],
        ['<func_call>']
    ],
    
    '<index>': [
        ['[', 'treasures_lit', ']', '<column1>'],
        ['λ']
    ],
    
    '<column1>': [
        ['[', 'treasures_lit', ']'],
        ['λ']
    ],
    
    '<input>': [
        ['wish', '(', 'scroll_lit', ')']
    ]
}

# Create CFG object
cfg = CFG(productions)

# Compute FIRST, FOLLOW, and PREDICT sets
first = cfg.compute_first()
follow = cfg.compute_follow(first)
predict = cfg.compute_predict(first, follow)

# Print FIRST sets for non-terminals
print("First Sets for Non-Terminals:")
for non_terminal in cfg.non_terminals:
    print(f"FIRST({non_terminal}) = {first[non_terminal]}")

# Print FOLLOW sets for non-terminals
print("\nFollow Sets for Non-Terminals:")
for non_terminal in cfg.non_terminals:
    print(f"FOLLOW({non_terminal}) = {follow[non_terminal]}")

# Print PREDICT sets for non-terminals
print("\nPredict Sets for Non-Terminals:")
for non_terminal in cfg.non_terminals:
    if non_terminal in predict:
        for rhs, predict_set in predict[non_terminal].items():
            print(f"PREDICT({non_terminal} -> {' '.join(rhs)}) = {predict_set}")

# class CFGAnalyzer:
#     def __init__(self):
#         self.grammar = {}
#         self.first_sets = {}
#         self.follow_sets = {}
#         self.predict_sets = {}
#         self.terminals = set()
#         self.non_terminals = set()
#         self.epsilon = 'λ'  # Using λ as epsilon symbol

#     def add_production(self, non_terminal, productions):
#         """Add a production rule to the grammar."""
#         if non_terminal not in self.grammar:
#             self.grammar[non_terminal] = []
#         self.grammar[non_terminal].extend(productions)
#         self.non_terminals.add(non_terminal)
        
#         # Identify terminals and non-terminals
#         for production in productions:
#             for symbol in production:
#                 if symbol.startswith('<') and symbol.endswith('>'):
#                     self.non_terminals.add(symbol)
#                 elif symbol != self.epsilon:
#                     self.terminals.add(symbol)

#     def compute_first_sets(self):
#         """Compute FIRST sets for all symbols in the grammar."""
#         # Initialize FIRST sets
#         for non_terminal in self.non_terminals:
#             self.first_sets[non_terminal] = set()
#         for terminal in self.terminals:
#             self.first_sets[terminal] = {terminal}

#         while True:
#             updated = False
#             for non_terminal, productions in self.grammar.items():
#                 for production in productions:
#                     first_idx = 0
                    
#                     # Handle epsilon productions
#                     if len(production) == 1 and production[0] == self.epsilon:
#                         if self.epsilon not in self.first_sets[non_terminal]:
#                             self.first_sets[non_terminal].add(self.epsilon)
#                             updated = True
#                         continue

#                     # Handle other productions
#                     all_nullable = True
#                     for symbol in production:
#                         if symbol == self.epsilon:
#                             continue
                        
#                         if symbol in self.terminals:
#                             if symbol not in self.first_sets[non_terminal]:
#                                 self.first_sets[non_terminal].add(symbol)
#                                 updated = True
#                             all_nullable = False
#                             break
#                         else:  # non-terminal
#                             symbol_first = self.first_sets[symbol]
#                             new_terminals = symbol_first - {self.epsilon} - self.first_sets[non_terminal]
#                             if new_terminals:
#                                 self.first_sets[non_terminal].update(new_terminals)
#                                 updated = True
#                             if self.epsilon not in symbol_first:
#                                 all_nullable = False
#                                 break
                    
#                     if all_nullable and self.epsilon not in self.first_sets[non_terminal]:
#                         self.first_sets[non_terminal].add(self.epsilon)
#                         updated = True
            
#             if not updated:
#                 break

#     def compute_follow_sets(self):
#         """Compute FOLLOW sets for all non-terminals in the grammar."""
#         # Initialize FOLLOW sets
#         for non_terminal in self.non_terminals:
#             self.follow_sets[non_terminal] = set()
        
#         # Add $ to the start symbol's FOLLOW set
#         start_symbol = list(self.grammar.keys())[0]
#         self.follow_sets[start_symbol].add('$')

#         while True:
#             updated = False
#             for non_terminal, productions in self.grammar.items():
#                 for production in productions:
#                     for i, symbol in enumerate(production):
#                         if symbol in self.non_terminals:
#                             follow = set()
#                             remaining = production[i + 1:]
                            
#                             if not remaining:  # If it's the last symbol
#                                 follow.update(self.follow_sets[non_terminal])
#                             else:
#                                 first_of_remaining = self.get_first_of_string(remaining)
#                                 follow.update(first_of_remaining - {self.epsilon})
#                                 if self.epsilon in first_of_remaining:
#                                     follow.update(self.follow_sets[non_terminal])
                            
#                             if not follow.issubset(self.follow_sets[symbol]):
#                                 self.follow_sets[symbol].update(follow)
#                                 updated = True
            
#             if not updated:
#                 break

#     def get_first_of_string(self, string):
#         """Compute FIRST set for a string of symbols."""
#         if not string or string[0] == self.epsilon:
#             return {self.epsilon}
        
#         result = set()
#         all_nullable = True
        
#         for symbol in string:
#             if symbol == self.epsilon:
#                 continue
                
#             if symbol in self.terminals:
#                 result.add(symbol)
#                 all_nullable = False
#                 break
#             else:
#                 symbol_first = self.first_sets[symbol]
#                 result.update(symbol_first - {self.epsilon})
#                 if self.epsilon not in symbol_first:
#                     all_nullable = False
#                     break
        
#         if all_nullable:
#             result.add(self.epsilon)
        
#         return result

#     def compute_predict_sets(self):
#         """Compute PREDICT sets for all productions in the grammar."""
#         for non_terminal, productions in self.grammar.items():
#             if non_terminal not in self.predict_sets:
#                 self.predict_sets[non_terminal] = []
            
#             for production in productions:
#                 predict = self.get_first_of_string(production)
#                 if self.epsilon in predict:
#                     predict.remove(self.epsilon)
#                     predict.update(self.follow_sets[non_terminal])
#                 self.predict_sets[non_terminal].append(predict)

#     def analyze_grammar(self):
#         """Compute all sets for the grammar."""
#         self.compute_first_sets()
#         self.compute_follow_sets()
#         self.compute_predict_sets()

#     def print_results(self):
#         """Print the computed FIRST, FOLLOW, and PREDICT sets."""
#         print("\nFIRST Sets:")
#         for symbol in sorted(self.non_terminals):
#             print(f"FIRST({symbol}) = {self.first_sets[symbol]}")

#         print("\nFOLLOW Sets:")
#         for non_terminal in sorted(self.non_terminals):
#             print(f"FOLLOW({non_terminal}) = {self.follow_sets[non_terminal]}")

#         print("\nPREDICT Sets:")
#         for non_terminal, productions in self.grammar.items():
#             for i, (production, predict_set) in enumerate(zip(productions, self.predict_sets[non_terminal])):
#                 prod_str = ' '.join(production) if production[0] != self.epsilon else 'λ'
#                 print(f"PREDICT({non_terminal} → {prod_str}) = {predict_set}")

# # Example usage with a subset of your grammar
# def main():
#     analyzer = CFGAnalyzer()
    
#     # Program production
#     analyzer.add_production('program', [['crown','~', 'global_dec', 'user-defined_func', 'castle', 'treasures', 'id_lit', '{', 'body', 'return', '0','~', '}']])

#     # Global declarations
#     analyzer.add_production('global_dec', [['var_dec', 'global_dec'], ['λ']])

#     # Variable declarations
#     analyzer.add_production('var_dec', [['data_type', 'id_lit', 'vardec_def'], ['λ']])
#     analyzer.add_production('vardec_def', [['initialization', 'vardec_more', '~'], ['[','num',']', 'column', 'array_initialization', 'array_more', '~']])
#     analyzer.add_production('initialization', [['=', 'val'], ['λ']])
#     analyzer.add_production('vardec_more', [[',', 'id_lit', 'initialization', 'vardec_more'], ['λ']])

#     # Array related productions
#     analyzer.add_production('column', [['[','num',']'], ['λ']])
#     analyzer.add_production('array_initialization', [['=', 'array_list'], ['λ']])
#     analyzer.add_production('array_list', [['single'], ['multi']])
#     analyzer.add_production('single', [['{', 'array_lit', 'list_more', '}']])
#     analyzer.add_production('multi', [['{', 'single', 'multi_more'], ['λ']])
#     analyzer.add_production('multi_more', [[',', 'single', 'multi_more'], ['λ']])
#     analyzer.add_production('list_more', [[',', 'array_lit', 'list_more'], ['λ']])
#     analyzer.add_production('array_more', [[',', 'id_lit', '[','num',']', 'column', 'array_initialization', 'array_more'], ['λ']])

#     # Array literals
#     analyzer.add_production('array_lit', [['scroll_lit'], ['rose_lit'], ['treasures_lit'], ['ocean_lit'], ['mirror_lit']])

#     # Assignment expressions
#     analyzer.add_production('assignment_exp', [['id_lit', 'assignment_operator', 'assignment_operand']])
#     analyzer.add_production('assignment_operator', [['+='], ['-='], ['*='], ['/='], ['%=']])
#     analyzer.add_production('assignment_operand', [['id_lit'], ['treasures_lit'], ['ocean_lit'], ['array_element'], ['arithmetic_exp'], ['func_call']])

#     # Array elements
#     analyzer.add_production('array_element', [['id_lit', 'index']])

#     # Logical expressions
#     analyzer.add_production('logical_exp', [['logical_operand', 'logical_operator', 'logical_operand', 'more_log'], 
#                                         ['logical_operator1', 'logical_operand', 'more_log']])
#     analyzer.add_production('logical_operand', [['id_lit'], ['mirror_lit'], ['treasures_mirror'], ['relational_exp'], 
#                                             ['(','relational_exp',')'], ['func_call'], ['array_element']])
#     analyzer.add_production('logical_operator', [['&&'], ['||']])
#     analyzer.add_production('logical_operator1', [['!']])
#     analyzer.add_production('more_log', [['logical_operator', 'logical_operand', 'more_log'],
#                                     ['logical_operator', 'logical_operator1', 'logical_operand', 'more_log'],
#                                     ['λ']])

#     # Function calls
#     analyzer.add_production('func_call', [['id_lit', '(', 'args', ')'], ['λ']])
#     analyzer.add_production('args', [['args_val', 'args_more'], ['λ']])
#     analyzer.add_production('args_val', [['id_lit'], ['scroll_lit'], ['rose_lit'], ['treasures_lit'], 
#                                     ['ocean_lit'], ['mirror_lit']])
#     analyzer.add_production('args_more', [[',', 'args', 'args_more'], ['λ']])

#     # Treasures mirror values
#     analyzer.add_production('treasures_mirror', [['1'], ['0']])

#     # Arithmetic expressions
#     analyzer.add_production('arithmetic_exp', [['arithmetic_operand', 'arithmetic_operator', 'arithmetic_operand', 'more_arith']])
#     analyzer.add_production('arithmetic_operand', [['id_lit'], ['ocean_lit'], ['treasures_lit'], ['arithmetic_exp'],
#                                                 ['(arithmetic_exp)'], ['func_call'], ['array_element']])
#     analyzer.add_production('arithmetic_operator', [['+'], ['-'], ['/'], ['*'], ['%']])
#     analyzer.add_production('more_arith', [['arithmetic_operator', 'arithmetic_operand', 'more_arith'], ['λ']])

#     # Relational expressions
#     analyzer.add_production('relational_exp', [['relational_operand', 'relational_operator1', 'relational_operand', 'relational_more', 'optional_eq']])
#     analyzer.add_production('optional_eq', [['relational_operator2', 'relational_operand', 'relational_more'], ['λ']])
#     analyzer.add_production('relational_operand', [['id_lit'], ['scroll_lit'], ['treasures_lit'], ['ocean_lit'], 
#                                                 ['(','arithmetic_exp',')'], ['arithmetic_exp'], ['func_call'], ['array_element']])
#     analyzer.add_production('relational_operator1', [['<'], ['>'], ['<='], ['>=']])
#     analyzer.add_production('relational_operator2', [['=='], ['!=']])
#     analyzer.add_production('relational_more', [['relational_operator1', 'relational_operand', 'relational_more'], ['λ']])

#     # Unary operations
#     analyzer.add_production('unary', [['id_lit', 'unary_operator']])
#     analyzer.add_production('unary_operator', [['++'], ['--']])

#     # String concatenation
#     analyzer.add_production('concat', [['string_operand', '+', 'string_operand', 'string_more']])
#     analyzer.add_production('string_operand', [['scroll_lit'], ['id_lit'], ['rose_lit'], ['array_element'], 
#                                             ['func_call'], ['toscroll','(','conver_value',')']])
#     analyzer.add_production('string_more', [['+', 'string_operand', 'string_more'], ['λ']])

#     # User-defined functions
#     analyzer.add_production('user-defined_func', [['spell', 'return_type', 'id_lit', '(', 'param', ')', '{', 'body', 'ret_statement', '}', 'user-defined_func'], ['λ']])
#     analyzer.add_production('return_type', [['data_type'], ['chamber']])
#     analyzer.add_production('param', [['datatype', 'id_lit', 'param_more'], ['λ']])
#     analyzer.add_production('param_more', [[',', 'datatype', 'id_lit', 'param_more'], ['λ']])

#     # Function body
#     analyzer.add_production('body', [['var_dec', 'body'], ['output', 'body'], ['func_call','~', 'body'], 
#                                 ['user-defined_func', 'body'], ['condi_statement', 'body'], ['for_loop', 'body'],
#                                 ['coronation', 'body'], ['unary','~', 'body'], ['assignment_exp','~', 'body'],
#                                 ['comments', 'body'], ['λ']])

#     # Comments
#     analyzer.add_production('comments', [['single_line'], ['multi_line']])
#     analyzer.add_production('single_line', [['?', 'scroll_lit']])
#     analyzer.add_production('multi_line', [['?','*', 'scroll_lit', '*','?']])

#     # Return statement and coronation
#     analyzer.add_production('ret_statement', [['return', 'val1', '~'], ['λ']])
#     analyzer.add_production('coronation', [['id_lit', '=', 'val', '~'], ['λ']])

#     # Conditional statements
#     analyzer.add_production('condi_statement', [['if'], ['while'], ['do_while'], ['λ']])
#     analyzer.add_production('for_loop', [['tale', '(', 'loop_var', '~', 'relational_exp', '~', 'unary', ')', '{', 'loop_body', '}'], ['λ']])
#     analyzer.add_production('loop_var', [['treasures', 'id_lit', '=', 'loop_val'], ['id_lit', '=', 'loop_val'], ['id_lit']])
#     analyzer.add_production('loop_val', [['id_lit'], ['treasures_lit']])
#     analyzer.add_production('loop_body', [['body'], ['if_break']])

#     # Break and continue structures
#     analyzer.add_production('if_break', [['cast', '(', 'if-elif_condition', ')', '{', 'body', 'flow_control', '}', 'elif_break', 'else_break']])
#     analyzer.add_production('elif_break', [['twist', '(', 'if-elif_condition', ')', '{', 'body', 'flow_control', '}', 'elif_break'], ['λ']])
#     analyzer.add_production('else_break', [['curse', '{', 'body', 'flow_control', '}'], ['λ']])
#     analyzer.add_production('flow_control', [['break','~'], ['continue','~'], ['λ']])

#     # Loop structures
#     analyzer.add_production('do_while', [['believe', '{', 'loop_body', '}', 'forever', '(', 'if-elif_condition', ')', '~']])
#     analyzer.add_production('if-elif_condition', [['id_lit'], ['treasures_mirror'], ['id_lit', 'mirror_init'], 
#                                                 ['relational_exp'], ['logical_exp'], ['logical_operator1', '(', 'if-elif_condition', ')'],
#                                                 ['func_call']])
#     analyzer.add_production('mirror_init', [['relational_operator2', 'mirror_lit'], ['λ']])
#     analyzer.add_production('while', [['forever', '(', 'if-elif_condition', ')', '{', 'loop_body', '}']])

#     # If-else structures
#     analyzer.add_production('if', [['cast', '(', 'if-elif_condition', ')', '{', 'body', '}', 'elif', 'else']])
#     analyzer.add_production('elif', [['twist', '(', 'if-elif_condition', ')', '{', 'body', '}', 'elif'], ['λ']])
#     analyzer.add_production('else', [['curse', '{', 'body', '}'], ['λ']])

#     # Output
#     analyzer.add_production('output', [['granted', '(', 'queen', 'more_queen', ')', '~']])
#     analyzer.add_production('queen', [['id_lit'], ['scroll_lit'], ['rose_lit'], ['treasures_lit'], ['ocean_lit'],
#                                     ['mirror_lit'], ['phantom'], ['set_precision'], ['conversion_func', '(', 'conver_value', ')'],
#                                     ['concat'], ['relational_exp'], ['logical_exp'], ['unary'], ['arithmetic_exp'],
#                                     ['array_element'], ['func_call']])
#     analyzer.add_production('set_precision', [['"','%','.','[','treasures_lit',']','f','"']])
#     analyzer.add_production('more_queen', [[',', 'queen', 'more_queen'], ['λ']])

#     # Data types and values
#     analyzer.add_production('data_type', [['scroll'], ['treasures'], ['mirror'], ['ocean'], ['rose']])
#     analyzer.add_production('val', [['scroll_lit'], ['treasures_lit'], ['mirror_lit'], ['ocean_lit'], ['rose_lit'],
#                                 ['id_lit'], ['phantom'], ['concat'], ['arithmetic_exp'], ['input'], ['type_conversion'],
#                                 ['relational_exp'], ['logical_exp'], ['treasures_mirror'], ['func_call']])
#     analyzer.add_production('val1', [['val'], ['unary'], ['assignment_exp']])

#     # Type conversion
#     analyzer.add_production('type_conversion', [['conversion_func', '(', 'conver_value', ')']])
#     analyzer.add_production('conversion_func', [['toscroll'], ['torose'], ['totreasures'], ['toocean']])
#     analyzer.add_production('conver_value', [['scroll_lit'], ['rose_lit'], ['ocean_lit'], ['treasures_lit'],
#                                         ['id_lit', 'index'], ['func_call']])

#     # Index and input
#     analyzer.add_production('index', [['[','treasures_lit',']', 'column1'], ['λ']])
#     analyzer.add_production('column1', [['[','treasures_lit',']'], ['λ']])
#     analyzer.add_production('input', [['wish', '(', 'scroll_lit', ')']])
    
#     analyzer.analyze_grammar()
#     analyzer.print_results()

# if __name__ == "__main__":
#     main()