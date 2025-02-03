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
    
    '<global_dec>': [['<var_dec>', '<global_dec>']],
    '<global_dec>': [['λ']],

    '<var_dec>': [['<data_type>', 'id_lit', '<vardec_def>']],
    '<var_dec>': [['λ']],

    '<vardec_def>': [['<initialization>', '<vardec_more>', '~']],
    '<vardec_def>': [['[', 'num', ']', '<column>', '<array_initialization>', '<array_more>', '~']],

    '<initialization>': [['=', '<val>']],
    '<initialization>': [['λ']],

    '<vardec_more>': [[',', 'id_lit', '<initialization>', '<vardec_more>']],
    '<vardec_more>': [['λ']],

    '<column>': [['[', 'num', ']']],
    '<column>': [['λ']],

    '<array_initialization>': [['=', '<array_list>']],
    '<array_initialization>': [['λ']],

    '<array_list>': [['<single>']],
    '<array_list>': [['<multi>']],

    '<single>': [['{', '<array_lit>', '<list_more>', '}']],

    '<multi>': [['{', '<single>', '<multi_more>', '}']],
    '<multi>': [['λ']],

    '<multi_more>': [[',', '<single>', '<multi_more>']],
    '<multi_more>': [['λ']],

    '<list_more>': [[',', '<array_lit>', '<list_more>']],
    '<list_more>': [['λ']],

    '<array_more>': [[',', 'id_lit', '[', 'num', ']', '<column>', '<array_initialization>', '<array_more>']],
    '<array_more>': [['λ']],

    '<array_lit>': [['scroll_lit']],
    '<array_lit>': [['rose_lit']],
    '<array_lit>': [['treasures_lit']],
    '<array_lit>': [['ocean_lit']],
    '<array_lit>': [['mirror_lit']],

    '<assignment_exp>': [['id_lit', '<assignment_operator>', '<assignment_operand>']],

    '<assignment_operator>': [['+=']],
    '<assignment_operator>': [['-=']],
    '<assignment_operator>': [['*=']],
    '<assignment_operator>': [['/=']],
    '<assignment_operator>': [['%=']],
    
    '<assignment_operand>': [['id_lit']],
    '<assignment_operand>': [['treasures_lit']],
    '<assignment_operand>': [['ocean_lit']],
    '<assignment_operand>': [['<array_element>']],
    '<assignment_operand>': [['<arithmetic_exp>']],
    '<assignment_operand>': [['<func_call>']],

    '<array_element>': [['id_lit', '<index>']],

    '<logical_exp>': [['<logical_operand>', '<logical_operator>', '<logical_operand>', '<more_log>']],
    '<logical_exp>': [['<logical_operator1>', '<logical_operand>', '<more_log>']],

    '<logical_operand>': [['id_lit']],
    '<logical_operand>': [['mirror_lit']],
    '<logical_operand>': [['<treasures_mirror>']],
    '<logical_operand>': [['<relational_exp>']],
    '<logical_operand>': [['(', '<relational_exp>', ')']],
    '<logical_operand>': [['<func_call>']],
    '<logical_operand>': [['<array_element>']],

    '<logical_operator>': [['&&']],
    '<logical_operator>': [['||']],

    '<logical_operator1>': [['!']],

    '<more_log>': [['<logical_operator>', '<logical_operand>', '<more_log>']],
    '<more_log>': [['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>']],
    '<more_log>': [['λ']],

    '<func_call>': [['id_lit', '(', '<args>', ')']],

    '<args>': [['<args_val>', '<args_more>']],
    '<args>': [['λ']],

    '<args_val>': [['id_lit']],
    '<args_val>': [['scroll_lit']],
    '<args_val>': [['rose_lit']],
    '<args_val>': [['treasures_lit']],
    '<args_val>': [['ocean_lit']],
    '<args_val>': [['mirror_lit']],

    '<args_more>': [[',', '<args>', '<args_more>']],
    '<args_more>': [['λ']],

    '<treasures_mirror>': [['1']],
    '<treasures_mirror>': [['0']],

    '<arithmetic_exp>': [['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>']],

    '<arithmetic_operand>': [['id_lit']],
    '<arithmetic_operand>': [['ocean_lit']],
    '<arithmetic_operand>': [['treasures_lit']],
    '<arithmetic_operand>': [['<arithmetic_exp>']],
    '<arithmetic_operand>': [['(', '<arithmetic_exp>', ')']],
    '<arithmetic_operand>': [['<func_call>']],
    '<arithmetic_operand>': [['<array_element>']],

    '<arithmetic_operator>': [['+']],
    '<arithmetic_operator>': [['-']],
    '<arithmetic_operator>': [['/']],
    '<arithmetic_operator>': [['*']],
    '<arithmetic_operator>': [['%']],

    '<more_arith>': [['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>']],
    '<more_arith>': [['λ']],

    '<relational_exp>': [['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>']],

    '<relational_operand>': [['id_lit']],
    '<relational_operand>': [['scroll_lit']],
    '<relational_operand>': [['treasures_lit']],
    '<relational_operand>': [['ocean_lit']],
    '<relational_operand>': [['(', '<arithmetic_exp>', ')']],
    '<relational_operand>': [['<arithmetic_exp>']],
    '<relational_operand>': [['<func_call>']],
    '<relational_operand>': [['<array_element>']],

    '<relational_operator>': [['<']],
    '<relational_operator>': [['>']],
    '<relational_operator>': [['<=']],
    '<relational_operator>': [['>=']],
    '<relational_operator>': [['==']],
    '<relational_operator>': [['!=']],

    '<relational_more>': [['<relational_operator>', '<relational_operand>', '<relational_more>']],
    '<relational_more>': [['λ']],

    '<unary>': [['id_lit', '<unary_operator>']],

    '<unary_operator>': [['++']],
    '<unary_operator>': [['--']],

    '<concat>': [['<string_operand>', '+', '<string_operand>', '<string_more>']],

    '<string_operand>': [['scroll_lit']],
    '<string_operand>': [['id_lit']],
    '<string_operand>': [['rose_lit']],
    '<string_operand>': [['<array_element>']],
    '<string_operand>': [['<func_call>']],
    '<string_operand>': [['toscroll', '(', '<conver_value>', ')']],

    '<string_more>': [['+', '<string_operand>', '<string_more>']],
    '<string_more>': [['λ']],

    '<user-defined_func>': [['spell', '<return_type>', 'id_lit', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>']],
    '<user-defined_func>': [['λ']],

    '<return_type>': [['<data_type>']],
    '<return_type>': [['chamber']],

    '<param>': [['<datatype>', 'id_lit', '<param_more>']],
    '<param>': [['λ']],

    '<param_more>': [[',', '<datatype>', 'id_lit', '<param_more>']],
    '<param_more>': [['λ']],

    '<body>': [['<var_dec>', '<body>']],
    '<body>': [['<output>', '<body>']],
    '<body>': [['<func_call>', '~', '<body>']],
    '<body>': [['<user-defined_func>', '<body>']],
    '<body>': [['<condi_statement>', '<body>']],
    '<body>': [['<for_loop>', '<body>']],
    '<body>': [['<coronation>', '<body>']],
    '<body>': [['<unary>', '~', '<body>']],
    '<body>': [['<assignment_exp>', '~', '<body>']],
    '<body>': [['<comments>', '<body>']],
    '<body>': [['λ']],

    '<comments>': [['<single_line>']],
    '<comments>': [['<multi_line>']],

    '<single_line>': [['?', 'scroll_lit']],

    '<multi_line>': [['?', '*', 'scroll_lit', '*', '?']],

    '<ret_statement>': [['return', '<val1>', '~']],
    '<ret_statement>': [['λ']],

    '<coronation>': [['id_lit', '=', '<val>', '~']],
    '<coronation>': [['λ']],

    '<condi_statement>': [['<if>']],
    '<condi_statement>': [['<while>']],
    '<condi_statement>': [['<do_while>']],
    '<condi_statement>': [['λ']],

    '<for_loop>': [['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}']],

    '<loop_var>': [['treasures', 'id_lit', '=', '<loop_val>']],
    '<loop_var>': [['id_lit', '=', '<loop_val>']],
    '<loop_var>': [['id_lit']],

    '<loop_val>': [['id_lit']],
    '<loop_val>': [['treasures_lit']],

    '<loop_body>': [['<body>']],
    '<loop_body>': [['<if_break>']],

    '<if_break>': [['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>', '<else_break>']],

    '<elif_break>': [['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>']],
    '<elif_break>': [['λ']],

    '<else_break>': [['curse', '{', '<body>', '<flow_control>', '}']],
    '<else_break>': [['λ']],

    '<flow_control>': [['break', '~']],
    '<flow_control>': [['continue', '~']],
    '<flow_control>': [['λ']],

    '<do_while>': [['believe', '{', '<loop_body>', '}', 'forever', '(', 'if-elif_condition', ')', '~']],

    '<if-elif_condition>': [['id_lit']],
    '<if-elif_condition>': [['<treasures_mirror>']],
    '<if-elif_condition>': [['id_lit', '<mirror_init>']],
    '<if-elif_condition>': [['<relational_exp>']],
    '<if-elif_condition>': [['<logical_exp>']],
    '<if-elif_condition>': [['<logical_operator1>', '(', '<if-elif_condition>', ')']],
    '<if-elif_condition>': [['<func_call>']],

    '<mirror_init>': [['==', 'mirror_lit']],
    '<mirror_init>': [['!=', 'mirror_lit']],
    '<mirror_init>': [['λ']],

    '<while>': [['forever', '(', 'if-elif_condition', ')', '{', '<loop_body>', '}']],

    '<if>': [['cast', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>', '<else>']],

    '<elif>': [['twist', '(', '<if-elif_condition>', ')', '{', '<body>', '}', '<elif>']],
    '<elif>': [['λ']],

    '<else>': [['curse', '{', '<body>', '}']],
    '<else>': [['λ']],

    '<output>': [['granted', '(', '<queen>', '<more_queen>', ')', '~']],

    '<queen>': [['id_lit']],
    '<queen>': [['scroll_lit']],
    '<queen>': [['rose_lit']],
    '<queen>': [['treasures_lit']],
    '<queen>': [['ocean_lit']],
    '<queen>': [['mirror_lit']],
    '<queen>': [['phantom']],
    '<queen>': [['<set_precision>']],
    '<queen>': [['<conversion_func>', '(', '<conver_value>', ')']],
    '<queen>': [['<concat>']],
    '<queen>': [['<relational_exp>']],
    '<queen>': [['<logical_exp>']],
    '<queen>': [['<unary>']],
    '<queen>': [['<arithmetic_exp>']],
    '<queen>': [['<array_element>']],
    '<queen>': [['<func_call>']],

    '<set_precision>': [['"', '%', '.', '"', '[', 'treasures_lit', ']', 'f']],

    '<more_queen>': [[',', '<queen>', '<more_queen>']],
    '<more_queen>': [['λ']],

    '<data_type>': [['scroll']],
    '<data_type>': [['treasures']],
    '<data_type>': [['mirror']],
    '<data_type>': [['ocean']],
    '<data_type>': [['rose']],

    '<val>': [['scroll_lit']],
    '<val>': [['treasures_lit']],
    '<val>': [['mirror_lit']],
    '<val>': [['ocean_lit']],
    '<val>': [['rose_lit']],
    '<val>': [['id_lit']],
    '<val>': [['phantom']],
    '<val>': [['<concat>']],
    '<val>': [['<arithmetic_exp>']],
    '<val>': [['<input>']],
    '<val>': [['<type_conversion>']],
    '<val>': [['<relational_exp>']],
    '<val>': [['<logical_exp>']],
    '<val>': [['<treasures_mirror>']],
    '<val>': [['<func_call>']],

    '<val1>': [['<val>']],
    '<val1>': [['<unary>']],
    '<val1>': [['<assignment_exp>']],

    '<type_conversion>': [['<conversion_func>', '(', '<conver_value>', ')']],

    '<conversion_func>': [['toscroll']],
    '<conversion_func>': [['torose']],
    '<conversion_func>': [['totreasures']],
    '<conversion_func>': [['toocean']],

    '<conver_value>': [['scroll_lit']],
    '<conver_value>': [['rose_lit']],
    '<conver_value>': [['ocean_lit']],
    '<conver_value>': [['treasures_lit']],
    '<conver_value>': [['id_lit', '<index>']],
    '<conver_value>': [['<func_call>']],

    '<index>': [['[', 'treasures_lit', ']', '<column1>']],
    '<index>': [['λ']],

    '<column1>': [['[', 'treasures_lit', ']']],
    '<column1>': [['λ']],

    '<input>': [['wish', '(', 'scroll_lit', ')']]
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

