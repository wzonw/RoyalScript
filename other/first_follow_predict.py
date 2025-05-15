from collections import defaultdict

class CFG:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set(productions.keys())
        self.terminals = set()
        
        # More thorough identification of terminals
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol != 'λ' and symbol not in self.non_terminals:
                        self.terminals.add(symbol)
        
        print(f"Non-terminals: {len(self.non_terminals)}")
        print(f"Terminals: {len(self.terminals)}")

    def compute_first(self):
        """
        Compute FIRST sets for all symbols in the grammar
        """
        first = defaultdict(set)
        
        # Step 1: Initialize FIRST for terminals
        for terminal in self.terminals:
            first[terminal] = {terminal}
        
        # Step 2: Handle epsilon productions
        for non_terminal, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if not rhs or rhs == ['λ'] or rhs == []:  # Empty production
                    first[non_terminal].add('λ')
        
        # Step 3: Iteratively compute FIRST sets
        changed = True
        while changed:
            changed = False
            for non_terminal, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    if not rhs or rhs == ['λ'] or rhs == []:  # Empty production
                        continue
                    
                    # Calculate first of the RHS
                    k = 0
                    all_can_derive_lambda = True
                    
                    while k < len(rhs) and all_can_derive_lambda:
                        symbol = rhs[k]
                        all_can_derive_lambda = False
                        
                        if symbol in self.terminals:
                            # If symbol is a terminal, add it to FIRST(non_terminal)
                            if symbol not in first[non_terminal]:
                                first[non_terminal].add(symbol)
                                changed = True
                            break
                        elif symbol in self.non_terminals:
                            # Add all non-lambda symbols from FIRST(symbol) to FIRST(non_terminal)
                            before_size = len(first[non_terminal])
                            for s in first[symbol]:
                                if s != 'λ':
                                    first[non_terminal].add(s)
                            
                            if before_size != len(first[non_terminal]):
                                changed = True
                            
                            # Check if symbol can derive lambda
                            if 'λ' in first[symbol]:
                                all_can_derive_lambda = True
                                k += 1
                            else:
                                break
                    
                    # If all symbols in the RHS can derive lambda, add lambda to FIRST(non_terminal)
                    if all_can_derive_lambda and k == len(rhs):
                        if 'λ' not in first[non_terminal]:
                            first[non_terminal].add('λ')
                            changed = True
                            
        return first

    def compute_follow(self, first):
        """
        Compute FOLLOW sets for all non-terminals in the grammar
        """
        follow = defaultdict(set)
        
        # Step 1: Add $ to FOLLOW(start_symbol)
        start_symbol = next(iter(self.productions))
        follow[start_symbol].add('$')
        
        # Step 2: Iteratively compute FOLLOW sets
        changed = True
        iterations = 0  # To track iterations for debugging
        
        while changed:
            changed = False
            iterations += 1
            
            for non_terminal, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    for i, symbol in enumerate(rhs):
                        if symbol in self.non_terminals:
                            # Case 1: A -> αBβ, add FIRST(β) - {λ} to FOLLOW(B)
                            if i < len(rhs) - 1:
                                remaining = rhs[i+1:]
                                first_of_remaining = self.compute_first_of_sequence(remaining, first)
                                
                                # Add everything except lambda
                                for s in first_of_remaining:
                                    if s != 'λ' and s not in follow[symbol]:
                                        follow[symbol].add(s)
                                        changed = True
                                
                                # Case 2: If FIRST(β) contains λ, add FOLLOW(A) to FOLLOW(B)
                                if 'λ' in first_of_remaining:
                                    before_size = len(follow[symbol])
                                    follow[symbol].update(follow[non_terminal])
                                    if before_size != len(follow[symbol]):
                                        changed = True
                            
                            # Case 3: A -> αB or A -> αBβ where β =>* λ, add FOLLOW(A) to FOLLOW(B)
                            else:  # B is at the end of the production
                                before_size = len(follow[symbol])
                                follow[symbol].update(follow[non_terminal])
                                if before_size != len(follow[symbol]):
                                    changed = True
            
            # Safety check to prevent infinite loops
            if iterations > 100:
                print(f"Warning: Exiting after {iterations} iterations")
                break
                
        return follow

    def compute_first_of_sequence(self, sequence, first):
        """
        Compute FIRST set for a sequence of symbols
        """
        if not sequence:
            return {'λ'}
        
        result = set()
        can_derive_lambda = True
        
        for symbol in sequence:
            if symbol in self.terminals:
                result.add(symbol)
                can_derive_lambda = False
                break
            elif symbol in self.non_terminals:
                # Add all non-lambda symbols
                for s in first[symbol]:
                    if s != 'λ':
                        result.add(s)
                
                # If this symbol cannot derive lambda, we're done
                if 'λ' not in first[symbol]:
                    can_derive_lambda = False
                    break
        
        # If all symbols can derive lambda, add lambda to the result
        if can_derive_lambda:
            result.add('λ')
            
        return result

    def compute_predict(self, first, follow):
        """
        Compute PREDICT sets for all productions in the grammar
        """
        predict = {}
        
        for non_terminal, rhs_list in self.productions.items():
            predict[non_terminal] = {}
            
            for rhs in rhs_list:
                if not rhs:  # Handle empty production
                    predict[non_terminal][tuple([])] = set(follow[non_terminal])
                    continue
                    
                first_of_rhs = self.compute_first_of_sequence(rhs, first)
                predict_set = set(s for s in first_of_rhs if s != 'λ')
                
                if 'λ' in first_of_rhs:
                    predict_set.update(follow[non_terminal])
                
                predict[non_terminal][tuple(rhs)] = predict_set
                
        return predict

    def print_sets(self, first, follow, predict):
        """
        Print FIRST, FOLLOW, and PREDICT sets in a more readable format
        """
        # Print FIRST sets
        print("\n===== FIRST SETS =====")
        for nt in sorted(self.non_terminals):
            print(f"FIRST({nt}) = {sorted(first[nt])}")
        
        # Print FOLLOW sets  
        print("\n===== FOLLOW SETS =====")
        for nt in sorted(self.non_terminals):
            print(f"FOLLOW({nt}) = {sorted(follow[nt])}")
        
        # Print PREDICT sets
        print("\n===== PREDICT SETS =====")
        for nt in sorted(self.non_terminals):
            if nt in predict:
                for rhs, p_set in predict[nt].items():
                    rhs_str = ' '.join(rhs) if rhs else 'λ'
                    print(f"PREDICT({nt} -> {rhs_str}) = {sorted(p_set)}")

# Define your CFG productions
productions =  {
    '<program>': [
        ['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'id_lit', '(', ')', '{', '<body>', 'return', '0', '~', '}', 'reign', '~'],
    ],
    '<global_dec>': [
        ['<var_dec>', '<global_dec>'],
        ['λ'],
    ],
    '<var_dec>': [
        ['<dynasty>', '<data_type>', 'id_lit', '<vardec_def>'],
    ],
    '<dynasty>': [
        ['dynasty'],
        ['λ'],
    ],
    '<vardec_def>': [
        ['<initialization>', '<vardec_more>', '~'],
        ['[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>', '~'],
    ],
    '<initialization>': [
        ['=', '<val>'],
        ['λ'],
    ],
    '<vardec_more>': [
        [',', 'id_lit', '<initialization>', '<vardec_more>'],
        ['λ'],
    ],
    '<column>': [
        ['[', '<array_size>', ']'],
        ['λ'],
    ],
    '<array_initialization>': [
        ['=', '<array_list>'],
        ['λ'],
    ],
    '<array_list>': [
        ['{', '<array_content>', '}'],
    ],
    '<array_content>': [
        ['<array_lit>', '<lit_more>'],
        ['{', '<array_row>', '}', '<row_more>'],
    ],
    '<array_row>': [
        ['<array_lit>', '<lit_more>'],
    ],
    '<row_more>': [
        [',', '<row_more_ext>'],
        ['λ'],
    ],
    '<row_more_ext>': [
        ['{', '<array_row>', '}', '<row_more>'],
        ['id_lit', '<row_more>'],
    ],
    '<lit_more>': [
        [',', '<lit_more_ext>'],
        ['λ'],
    ],
    '<lit_more_ext>': [
        ['<array_lit>', '<lit_more>'],
        ['{', '<array_row>', '}', '<row_more>'],
    ],
    '<array_more>': [
        [',', 'id_lit', '[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>'],
        ['λ'],
    ],
    '<array_lit>': [
        ['<lit4>'],
        ['id_lit'],
    ],
    '<assignment_operator>': [
        ['+='],
        ['-='],
        ['*='],
        ['/='],
        ['%='],
    ],
    '<assignment_operand>': [
        ['id_lit', '<id_ext>', '<more_arith>'],
        ['<lit3>', '<more_arith>'],
        ['<arithmetic_operand_2>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ],
    '<logical_exp>': [
        ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ],
    '<logical_operand>': [
        ['id_lit', '<id_ext>', '<logical_operand_ext>'],
        ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['mirror_lit', '<relational_more>'],
        ['<treasures_mirror>', '<relational_more>'],
        ['(', '<logical_operator1>', '<expression>'],
    ],
    '<expression>': [
        ['id_lit', '<id_ext>', '<expression_ext_1>'],
        ['<lit3>', '<expression_ext_1>'],
        ['scroll_lit', '<expression_ext_2>'],
        ['rose_lit', '<expression_ext_2>'],
        ['mirror_lit', '<expression_ext_2>'],
        ['<treasures_mirror>', '<expression_ext_2>'],
        ['(', '<logical_operator1>', '<expression>', '<more_log>', ')', '<logical_operand_ext>'],
    ],
    '<expression_ext_1>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<relational_more>'],
    ],
    '<expression_ext_2>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', ')', '<relational_more>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    ],
    '<logical_operand_ext>': [
        ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['λ'],
    ],
    '<logical_operator>': [
        ['&&'],
        ['||'],
    ],
    '<logical_operator1>': [
        ['!'],
        ['λ'],
    ],
    '<more_log>': [
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['λ'],
    ],
    '<treasures_mirror>': [
        ['1'],
        ['0'],
    ],
    '<arithmetic_exp>': [
        ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ],
    '<arithmetic_operand_1>': [
        ['id_lit', '<id_ext>'],
        ['<lit3>'],
    ],
    '<arithmetic_operand_2>': [
        ['(', '<arithmetic_exp>', ')'],
    ],
    '<arithmetic_operand>': [
        ['<arithmetic_operand_1>'],
        ['<arithmetic_operand_2>'],
    ],
    '<arithmetic_operator>': [
        ['+'],
        ['-'],
        ['/'],
        ['*'],
        ['%'],
    ],
    '<more_arith>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
        ['λ'],
    ],
    '<relational_exp>': [
        ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ],
    '<relational_operand>': [
        ['id_lit', '<id_ext>', '<more_arith>'],
        ['<lit3>', '<more_arith>'],
        ['scroll_lit'],
        ['rose_lit'],
        ['mirror_lit'],
        ['treasures_mirror'],
        ['(', '<expression_2>'],
    ],
    '<expression_2>': [
        ['id_lit', '<id_ext>', '<expression_2_ext>'],
        ['<lit3>', '<expression_2_ext>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['mirror_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['treasures_mirror', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['(', '<expression_2>', ')'],
    ],
    '<expression_2_ext>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ],
    '<relational_operator>': [
        ['<'],
        ['>'],
        ['<='],
        ['>='],
        ['=='],
        ['!='],
    ],
    '<relational_more>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['λ'],
    ],
    '<unary>': [
        ['id_lit', '<unary_operator>'],
    ],
    '<unary_operator>': [
        ['++'],
        ['--'],
    ],
    '<string_operand>': [
        ['<lit1>'],
        ['id_lit', '<id_ext>'],
        ['toscroll', '(', '<conversion_value>', ')'],
    ],
    '<string_more>': [
        ['+', '<string_operand>', '<string_more>'],
        ['λ'],
    ],
    '<user-defined_func>': [
        ['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>'],
        ['λ'],
    ],
    '<return_type>': [
        ['<data_type>'],
        ['chamber'],
    ],
    '<param>': [
        ['<data_type>', 'id_lit', '<param_more>'],
        ['λ'],
    ],
    '<param_more>': [
        [',', '<data_type>', 'id_lit', '<param_more>'],
        ['λ'],
    ],
    '<body>': [
        ['<dynasty>', '<data_type>', 'id_lit', '<vardec_def>', '<body>'],
        ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<body>'],
        ['id_lit', '<body_1_ext>', '<body>'],
        ['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<body>'],
        ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<body>'],
        ['cast', '(', '<condition>', ')', '{', '<body>', '}', '<elif>', '<else>', '<body>'],
        ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<body>'],
        ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<body>'],
        ['λ'],
    ],
    '<body_1_ext>': [
        ['(', '<args>', ')', '~'],
        ['<index>', '<body_1_other_ext>'],
        ['<unary_operator>', '~'],
    ],
    '<body_1_other_ext>': [
        ['=', '<val>', '~'],
        ['<assignment_operator>', '<assignment_operand>', '~'],
    ],
    '<ret_statement>': [
        ['return', '<val1>', '~'],
        ['λ'],
    ],
    '<loop_var>': [
        ['treasures', 'id_lit', '=', '<loop_val>'],
        ['id_lit', '<loop_init>'],
    ],
    '<loop_init>': [
        ['=', '<loop_val>'],
        ['λ'],
    ],
    '<loop_val>': [
        ['id_lit'],
        ['treasures_lit'],
    ],
    '<loop_body>': [
        ['<dynasty>', '<data_type>', 'id_lit', '<vardec_def>', '<loop_body>'],
        ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<loop_body>'],
        ['id_lit', '<body_1_ext>', '<loop_body>'],
        ['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<loop_body>'],
        ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<loop_body>'],
        ['cast', '(', '<condition>', ')', '{', '<loop_body>', '<flow_control>', '}', '<elif_break>', '<else_break>', '<loop_body>'],
        ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<loop_body>'],
        ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<loop_body>'],
        ['λ'],
    ],
    '<elif_break>': [
        ['twist', '(', '<condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>'],
        ['λ'],
    ],
    '<else_break>': [
        ['curse', '{', '<body>', '<flow_control>', '}'],
        ['λ'],
    ],
    '<flow_control>': [
        ['break', '~'],
        ['continue', '~'],
        ['λ'],
    ],
    '<condition>': [
        ['<treasures_mirror>', '<more_log>'],
        ['id_lit', '<condi_id_ext>'],
        ['!', '<logical_operand>', '<more_log>'],
        ['mirror_lit', '<relational_more>', '<more_log>'],
        ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['(', '<logical_operator1>', '<expression>', '<more_log>'],
    ],
    '<condi_id_ext>': [
        ['<func_call>', '<other_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<other_id_ext>'],
        ['<other_id_ext>'],
    ],
    '<other_id_ext>': [
        ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<elif>': [
        ['twist', '(', '<condition>', ')', '{', '<body>', '}', '<elif>'],
        ['λ'],
    ],
    '<else>': [
        ['curse', '{', '<body>', '}'],
        ['λ'],
    ],
    '<granted_content_1>': [
        ['set_precision'],
        ['id_lit', '<granted_id_ext>'],
    ],
    '<granted_content_2>': [
        ['phantom'],
        ['lengthof', '(', 'id_lit', '<index>', ')'],
        ['<conversion_func>', '(', '<conversion_value>', ')'],
        ['toscroll', '(', '<conversion_value>', ')', '<string_more>'],
        ['<treasures_mirror>', '<more_log>'],
        ['mirror_lit', '<relational_more>', '<more_log>'],
        ['scroll_lit', '<granted_scroll_ext>'],
        ['rose_lit', '<granted_rose_ext>'],
        ['<lit3>', '<granted_lit3_ext>'],
        ['(', '<logical_operator1>', '<granted_open_paren_ext>'],
        ['!', '<logical_operand>', '<more_log>'],
    ],
    '<granted_content>': [
        ['<granted_content_1>'],
        ['<granted_content_2>'],
    ],
    '<granted_open_paren_ext>': [
        ['id_lit', '<id_ext>', '<idlit3_granted_ext>'],
        ['<lit3>', '<idlit3_granted_ext>'],
        ['scroll_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['rose_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['mirror_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['<treasures_mirror>', '<expression_ext_2>', '<more_log>', ')'],
        ['(', '<logical_operator1>', '<granted_open_paren_ext>', ')', '<close_paren_ext>'],
    ],
    '<idlit3_granted_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')', '<more_log>'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ],
    '<open_paren_other_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['λ'],
    ],
    '<close_paren_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
        ['λ'],
    ],
    '<granted_id_ext>': [
        ['<unary_operator>'],
        ['<func_call>', '<granted_other_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<granted_other_id_ext>'],
        ['<granted_other_id_ext>'],
    ],
    '<granted_other_id_ext>': [
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['λ'],
    ],
    '<granted_other_id_ext2>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<plus_ext>': [
        ['id_lit', '<plus_ext_1>'],
        ['toscroll', '(', '<conversion_value>', ')', '<string_more>'],
        ['scroll_lit', '<string_more>'],
        ['rose_lit', '<string_more>'],
        ['(', '<arithmetic_exp>', ')', '<more_arith>', '<granted_other_id_ext2>'],
        ['treasures_lit', '<more_arith>', '<granted_other_id_ext2>'],
        ['ocean_lit', '<more_arith>', '<granted_other_id_ext2>'],
    ],
    '<plus_ext_1>': [
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['λ'],
    ],
    '<granted_scroll_ext>': [
        ['+', '<string_operand>', '<string_more>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<granted_rose_ext>': [
        ['+', '<string_operand>', '<string_more>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<granted_lit3_ext>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<granted_lit3_ext1>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['λ'],
    ],
    '<more_granted>': [
        [',', '<granted_content>', '<more_granted>'],
        ['λ'],
    ],
    '<data_type>': [
        ['scroll'],
        ['treasures'],
        ['mirror'],
        ['ocean'],
        ['rose'],
    ],
    '<val>': [
        ['<granted_content_2>'],
        ['id_lit', '<granted_id_ext>'],
        ['<input>'],
    ],
    '<val1>': [
        ['<granted_content_2>'],
        ['id_lit', '<val1_ext>'],
    ],
    '<val1_ext>': [
        ['<val1_id_ext>'],
        ['<func_call>', '<val1_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<val1_id_ext>'],
        ['<unary_operator>'],
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ],
    '<val1_id_ext>': [
        ['<assignment_operator>', '<assignment_operand>'],
        ['λ'],
    ],
    '<conversion_func>': [
        ['torose'],
        ['totreasures'],
        ['toocean'],
        ['tomirror'],
    ],
    '<conversion_value>': [
        ['<lit4>'],
        ['id_lit', '<id_ext>'],
    ],
    '<index>': [
        ['[', '<array_size>', ']', '<column1>'],
        ['λ'],
    ],
    '<column1>': [
        ['[', '<array_size>', ']'],
        ['λ'],
    ],
    '<input>': [
        ['wish', '(', 'scroll_lit', ')'],
    ],
    '<lit1>': [
        ['scroll_lit'],
        ['rose_lit'],
    ],
    '<lit2>': [
        ['mirror_lit'],
    ],
    '<lit3>': [
        ['ocean_lit'],
        ['treasures_lit'],
    ],
    '<lit4>': [
        ['<lit1>'],
        ['<lit2>'],
        ['<lit3>'],
    ],
    '<func_call>': [
        ['(', '<args>', ')'],
    ],
    '<args>': [
        ['<args_val>', '<args_more>'],
        ['λ'],
    ],
    '<args_val>': [
        ['id_lit', '<id_ext>'],
        ['<lit4>'],
    ],
    '<args_more>': [
        [',', '<args_val>', '<args_more>'],
        ['λ'],
    ],
    '<id_ext>': [
        ['<func_call>'],
        ['[', '<array_size>', ']', '<column1>'],
        ['λ'],
    ],
    '<array_size>': [
        ['id_lit'],
        ['positive_treasures_lit'],
    ],
}
# Create CFG object
cfg = CFG(productions)

# Compute FIRST, FOLLOW, and PREDICT sets
first = cfg.compute_first()
follow = cfg.compute_follow(first)
predict = cfg.compute_predict(first, follow)

print("\n===== FIRST SETS =====")
for nt in cfg.productions:  # preserves the order of appearance
    print(f"FIRST({nt}) = {{{', '.join(first[nt])}}}")

print("\n===== FOLLOW SETS =====")
for nt in cfg.productions:
    print(f"FOLLOW({nt}) = {{{', '.join(follow[nt])}}}")

print("\n===== PREDICT SETS =====")
for nt in cfg.productions:
    if nt in predict:
        for rhs, p_set in predict[nt].items():
            rhs_str = ' '.join(rhs) if rhs else 'λ'
            print(f"PREDICT({nt}) → {rhs_str} → {{{', '.join(p_set)}}}")