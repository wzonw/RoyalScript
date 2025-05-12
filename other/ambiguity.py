import re
from collections import defaultdict
from itertools import product

EPSILON = 'λ'

grammar_text = """
<program> -> crown ~ <global_dec> <user-defined_func> castle treasures id_lit () { <body> return 0 ~ } reign ~
<global_dec> -> <var_dec> <global_dec>
<global_dec> -> λ
<var_dec> -> <dynasty> <data_type> id_lit <vardec_def>
<dynasty> -> dynasty
<dynasty> -> λ
<vardec_def> -> <initialization> <vardec_more> ~
<vardec_def> -> [ <array_size> ] <column> <array_initialization> <array_more> ~
<initialization> -> = <val>
<initialization> -> λ
<vardec_more> -> , id_lit <initialization> <vardec_more>
<vardec_more> -> λ
<column> -> [ <array_size> ]
<column> -> λ
<array_initialization> -> = <array_list>
<array_initialization> -> λ
<array_list> -> { <array_content> }
<array_content> -> <array_lit> <lit_more>
<array_content> -> { <array_row> } <row_more>
<array_content> -> id_lit <row_more>
<array_row> -> <array_lit> <lit_more>
<row_more> -> , <row_more_ext>
<row_more> -> λ
<row_more_ext> -> { <array_row> } <row_more>
<row_more_ext> -> id_lit <row_more>
<lit_more> -> , <array_lit> <lit_more>
<lit_more> -> λ
<array_more> -> , id_lit [ <array_size> ] <column> <array_initialization> <array_more>
<array_more> -> λ
<array_lit> -> <lit4>
<array_lit> -> id_lit
<assignment_operator> -> +=
<assignment_operator> -> -=
<assignment_operator> -> *=
<assignment_operator> -> /=
<assignment_operator> -> %=
<assignment_operand> -> id_lit <id_ext> <more_arith>
<assignment_operand> -> <lit3> <more_arith>
<assignment_operand> -> <arithmetic_operand_2> <arithmetic_operator> <arithmetic_operand> <more_arith>
<logical_exp> -> <logical_operator1> <logical_operand> <logical_operator> <logical_operator1> <logical_operand> <more_log>
<logical_exp> -> ! <logical_operand> <more_log>
<logical_operand> -> id_lit <id_ext> <logical_operand_ext>
<logical_operand> -> <lit3> <more_arith> <relational_operator> <relational_operand> <relational_more>
<logical_operand> -> scroll_lit <relational_operator> <relational_operand> <relational_more>
<logical_operand> -> rose_lit <relational_operator> <relational_operand> <relational_more>
<logical_operand> -> mirror_lit <relational_more>
<logical_operand> -> <treasures_mirror> <relational_more>
<logical_operand> -> ( <expression>
<expression> -> <relational_exp> ) <relational_more>
<expression> -> <logical_exp> )
<expression> -> <arithmetic_exp> ) <more_arith> <relational_operator> <relational_operand> <relational_more>
<logical_operand_ext> -> <more_arith> <relational_operator> <relational_operand> <relational_more>
<logical_operand_ext> -> λ
<logical_operator> -> &&
<logical_operator> -> ||
<logical_operator1> -> !
<logical_operator1> -> λ
<more_log> -> <logical_operator> <logical_operator1> <logical_operand> <more_log>
<more_log> -> λ
<treasures_mirror> -> 1
<treasures_mirror> -> 0
<arithmetic_exp> -> <arithmetic_operand> <arithmetic_operator> <arithmetic_operand> <more_arith>
<arithmetic_operand_1> -> id_lit <id_ext>
<arithmetic_operand_1> -> <lit3>
<arithmetic_operand_2> -> ( <arithmetic_exp> )
<arithmetic_operand> -> <arithmetic_operand_1>
<arithmetic_operand> -> <arithmetic_operand_2>
<arithmetic_operator> -> +
<arithmetic_operator> -> -
<arithmetic_operator> -> /
<arithmetic_operator> -> *
<arithmetic_operator> -> %
<more_arith> -> <arithmetic_operator> <arithmetic_operand> <more_arith>
<more_arith> -> λ
<relational_exp> -> <relational_operand> <relational_operator> <relational_operand> <relational_more>
<relational_operand> -> id_lit <id_ext> <more_arith>
<relational_operand> -> <lit3> <more_arith>
<relational_operand> -> scroll_lit
<relational_operand> -> rose_lit
<relational_operand> -> mirror_lit
<relational_operand> -> treasures_mirror
<relational_operand> -> ( <expression_2>
<expression_2> -> <arithmetic_exp> ) <more_arith>
<expression_2> -> <relational_exp>  )
<relational_operator> -> <
<relational_operator> -> >
<relational_operator> -> <=
<relational_operator> -> >=
<relational_operator> -> ==
<relational_operator> -> !=
<relational_more> -> <relational_operator> <relational_operand> <relational_more>
<relational_more> -> λ
<unary> -> id_lit <unary_operator>
<unary_operator> -> ++
<unary_operator> -> --
<string_operand> -> <lit1>
<string_operand> -> id_lit <id_ext>
<string_operand> -> toscroll ( <conver_value> )
<string_more> -> + <string_operand> <string_more>
<string_more> -> λ
<user-defined_func> -> spell <return_type> id_lit ( <param> ) { <body> <ret_statement> } <user-defined_func>
<user-defined_func> -> λ
<return_type> -> <data_type>
<return_type> -> chamber
<param> -> <data_type> id_lit <param_more>
<param> -> λ
<param_more> -> , <data_type> id_lit <param_more>
<param_more> -> λ
<body_1> -> <var_dec> <body>
<body_1> -> <output> <body>
<body_1> -> id_lit <body_1_ext> <body>
<body_1> -> <user-defined_func> <body>
<body_1> -> <for_loop> <body>
<body_1_ext> -> ( <args> ) ~
<body_1_ext> -> <index> = <val> ~
<body_1_ext> -> <unary_operator> ~
<body_1_ext> -> <index> <assignment_operator> <assignment_operand> ~
<body_2> -> <condi_statement> <body>
<body> -> <body_1>
<body> -> <body_2>
<body> -> λ
<ret_statement> -> return <val1> ~
<ret_statement> -> λ
<condi_statement> -> <if>
<condi_statement> -> <while>
<condi_statement> -> <do_while>
<for_loop> -> tale ( <loop_var> ~ <relational_exp> ~ <unary> ) { <loop_body> }
<loop_var> -> treasures id_lit = <loop_val>
<loop_var> -> id_lit <loop_init>
<loop_init> -> = <loop_val>
<loop_init> -> λ
<loop_val> -> id_lit
<loop_val> -> treasures_lit
<loop_body> -> <body_1> <loop_body>
<loop_body> -> <if_break> <loop_body>
<loop_body> -> <while> <loop_body>
<loop_body> -> <do_while> <loop_body>
<loop_body> -> λ
<if_break> -> cast ( <condition> ) { <body> <flow_control> } <elif_break> <else_break>
<elif_break> -> twist ( <condition> ) { <body><flow_control> } <elif_break>
<elif_break> -> λ
<else_break> -> curse { <body> <flow_control> }
<else_break> -> λ
<flow_control> -> break ~
<flow_control> -> continue ~
<flow_control> -> λ
<do_while> -> believe { <loop_body> } forever ( <condition> ) ~
<condition> -> <treasures_mirror> <more_log>
<condition> -> id_lit <condi_id_ext>
<condition> -> <logical_operator1> <logical_operand> <more_log>
<condition> -> mirror_lit <relational_more> <more_log>
<condition> -> <lit3> <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<condition> -> scroll_lit <relational_operator> <relational_operand> <relational_more> <more_log>
<condition> -> rose_lit <relational_operator> <relational_operand> <relational_more> <more_log>
<condition> -> ( <expression_3>
<expression_3> -> <relational_exp> ) <relational_more> <more_log>
<expression_3> -> <logical_exp> ) <more_log>
<expression_3> -> <arithmetic_exp> ) <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<condi_id_ext> -> <mirror_init>
<condi_id_ext> -> <id_ext> <other_id_ext>
<condi_id_ext> -> λ
<other_id_ext> -> <other_id_ext_1> <other_id_ext_2>
<other_id_ext_1> -> <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<other_id_ext_1> -> λ
<other_id_ext_2> -> <logical_operator> <more_log>
<other_id_ext_2> -> λ
<mirror_init> -> == mirror_lit
<mirror_init> -> != mirror_lit
<mirror_init> -> λ
<while> -> forever ( <condition> ) { <loop_body> }
<if> -> cast ( <condition> ) { <body> } <elif> <else>
<elif> -> twist( <condition> ) { <body> } <elif>
<elif> -> λ
<else> -> curse { <body> }
<else> -> λ
<output> -> granted ( <granted_content> <more_granted> ) ~
<granted_content_1> -> set_precision
<granted_content_1> -> id_lit <granted_id_ext>
<granted_content_2> -> phantom
<granted_content_2> -> lengthof ( id_lit <index> )
<granted_content_2> -> <conversion_func> ( <conversion_value> )
<granted_content_2> -> toscroll ( <conversion_value> ) <string_more>
<granted_content_2> -> <treasures_mirror> <more_log>
<granted_content_2> -> mirror_lit <relational_more> <more_log>
<granted_content_2> -> scroll_lit <granted_scroll_ext>
<granted_content_2> -> rose_lit <granted_rose_ext>
<granted_content_2> -> <lit3>  <granted_lit3_ext>
<granted_content_2> -> ( <granted_open_paren_ext>
<granted_content_2> -> <logical_operator1> <logical_operand> <more_log>
<granted_content> -> <granted_content_1>
<granted_content> -> <granted_content_2>
<granted_open_paren_ext> -> <arithmetic_exp> ) <more_arith>
<granted_open_paren_ext> -> <expression> <more_log>
<granted_open_paren_ext> -> <expression_2> <relational_more>
<granted_id_ext> -> <unary_operator>
<granted_id_ext> -> <id_ext> <granted_other_id_ext>
<granted_id_ext> -> λ
<granted_other_id_ext> -> + <string_operand> <string_more>
<granted_other_id_ext> -> <arithmetic_operator> <arithmetic_operand> <more_arith>
<granted_other_id_ext> -> <more_arith> <relational_operator> <relational_operand> <relational_more>
<granted_other_id_ext> -> <logical_operand_ext> <logical_operator> <more_log>
<granted_other_id_ext> -> λ
<granted_scroll_ext> -> + <string_operand> <string_more>
<granted_scroll_ext> -> <relational_operator> <relational_operand> <relational_more> <more_log>
<granted_scroll_ext> -> λ
<granted_rose_ext> -> + <string_operand> <string_more>
<granted_rose_ext> -> <relational_operator> <relational_operand> <relational_more> <more_log>
<granted_rose_ext> -> λ
<granted_lit3_ext> -> <arithmetic_operator> <arithmetic_operand> <more_arith>
<granted_lit3_ext> -> <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<granted_lit3_ext> -> λ
<more_granted> -> , <granted_content> <more_granted>
<more_granted> -> λ
<data_type> -> scroll
<data_type> -> treasures
<data_type> -> mirror
<data_type> -> ocean
<data_type> -> rose
<val> -> <granted_content_2>
<val> -> id_lit <granted_id_ext>
<val> -> <input>
<val1> -> <granted_content_2>
<val1> -> id_lit <val1_ext>
<val1_ext> -> <id_ext> <val1_id_ext>
<val1_ext> -> <unary_operator>
<val1_ext> -> λ
<val1_id_ext> -> <granted_other_id_ext>
<val1_id_ext> -> <assignment_operator> <assignment_operand>
<val1_id_ext> -> λ
<conversion_func> -> torose
<conversion_func> -> totreasures
<conversion_func> -> toocean
<conversion_func> -> tomirror
<conversion_value> -> <lit4>
<conversion_value> -> id_lit <id_ext>
<index> -> [ <array_size> ] <column1>
<index> -> λ
<column1> -> [ <array_size> ]
<column1> -> λ
<input> -> wish ( scroll_lit )
<lit1> -> scroll_lit
<lit1> -> rose_lit
<lit2> -> mirror_lit
<lit3> -> ocean_lit
<lit3> -> treasures_lit
<lit4> -> <lit1>
<lit4> -> <lit2>
<lit4> -> <lit3>
<func_call> -> ( <args> )
<args> -> <args_val> <args_more>
<args> -> λ
<args_val> -> id_lit <id_ext>
<args_val> -> <lit4>
<args_more> -> , <args_val> <args_more>
<args_more> -> λ
<array_element> -> <index>
<id_ext> -> <func_call>
<id_ext> -> <array_element>
<id_ext> -> λ
<array_size> -> id_lit
<array_size> -> positive_treasures_lit
"""

def parse_grammar(grammar_text):
    grammar = defaultdict(list)
    non_terminals = set()
    for line in grammar_text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '->' not in line:
            continue  # Skip lines without '->'
        lhs, rhs = re.split(r'->', line)
        lhs = lhs.strip()
        rhs = rhs.strip()
        production = rhs.split()
        grammar[lhs].append(production)
        non_terminals.add(lhs)
    return grammar, non_terminals

grammar, non_terminals = parse_grammar(grammar_text)
start_symbol = next(iter(grammar))

# Generate all possible strings up to a certain depth
def generate_strings(grammar, symbol, max_depth=4):
    if max_depth == 0:
        return set()
    if symbol not in grammar:
        return {symbol}
    results = set()
    for production in grammar[symbol]:
        if production == [EPSILON]:
            results.add('')
        else:
            sublists = [generate_strings(grammar, sym, max_depth-1) for sym in production]
            for prod in product(*sublists):
                results.add(' '.join([p for p in prod if p]))
    return results

# CYK-like parser for ambiguity detection
def count_parses(grammar, string, start_symbol):
    tokens = string.split()
    n = len(tokens)
    if n == 0:
        return 0
    table = [[defaultdict(int) for _ in range(n)] for _ in range(n)]
    # Fill table for length 1 substrings
    for i, token in enumerate(tokens):
        for lhs, productions in grammar.items():
            for prod in productions:
                if prod == [token]:
                    table[i][i][lhs] += 1
    # Fill table for longer substrings
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            for k in range(i, j):
                for B in table[i][k]:
                    for C in table[k+1][j]:
                        for lhs, productions in grammar.items():
                            for prod in productions:
                                if len(prod) == 2 and prod[0] == B and prod[1] == C:
                                    table[i][j][lhs] += table[i][k][B] * table[k+1][j][C]
    return table[0][n-1][start_symbol]

# Main ambiguity check
def check_ambiguity(grammar, start_symbol, max_depth=4):
    strings = generate_strings(grammar, start_symbol, max_depth)
    ambiguous = []
    for s in strings:
        s_clean = ' '.join(s.split())
        if not s_clean:
            continue
        count = count_parses(grammar, s_clean, start_symbol)
        if count > 1:
            ambiguous.append((s_clean, count))
    return ambiguous

# Run ambiguity check
ambiguous = check_ambiguity(grammar, start_symbol, max_depth=4)
if ambiguous:
    print("Ambiguous strings found:")
    for s, count in ambiguous:
        print(f"'{s}' has {count} parses")
    print("\nTo correct ambiguity, consider rewriting the rules that allow multiple parses for the same string.")
else:
    print("No ambiguity detected for strings up to the given length.")