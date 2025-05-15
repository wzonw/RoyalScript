import re
from collections import defaultdict

def parse_cfg_line(line):
    # Remove leading/trailing whitespace and ignore empty/comment lines
    line = line.strip()
    if not line or line.startswith('#'):
        return None, None
    # Split on the arrow
    parts = [p.strip() for p in re.split(r'\s*→\s*', line)]
    if len(parts) != 2:
        return None, None
    nonterminal = parts[0]
    production = parts[1]
    prod_list = ['λ'] if production == 'λ' else [x for x in production.split() if x]
    return nonterminal, prod_list

def convert_cfg_table(lines):
    cfg = defaultdict(list)
    for line in lines:
        nonterminal, prod_list = parse_cfg_line(line)
        if nonterminal:
            cfg[nonterminal].append(prod_list)
    return cfg

def format_cfg_dict(cfg):
    out = ["CFG = {"]
    for nonterminal, productions in cfg.items():
        out.append(f"    '{nonterminal}': [")
        for prod in productions:
            prod_str = ', '.join(f"'{x}'" for x in prod)
            out.append(f"        [{prod_str}],")
        out.append("    ],")
    out.append("}")
    return '\n'.join(out)

# Example usage:
input_text = """
<program>	→	crown ~ <global_dec> <user-defined_func> castle treasures id_lit ( ) { <body> return 0 ~ } reign ~
<global_dec>	→	<var_dec> <global_dec>
<global_dec>	→	λ
<var_dec>	→	<dynasty> <data_type> id_lit <vardec_def>
<dynasty>	→	dynasty
<dynasty>	→	λ
<vardec_def>	→	<initialization> <vardec_more> ~
<vardec_def>	→	[ <array_size> ] <column> <array_initialization> <array_more> ~
<initialization>	→	= <val>
<initialization>	→	λ 
<vardec_more>	→	, id_lit <initialization> <vardec_more>
<vardec_more>	→	λ
<column>	→	[ <array_size> ]
<column>	→	λ
<array_initialization>	→	= <array_list>
<array_initialization>	→	λ
<array_list>	→	{ <array_content> }
<array_content>	→	<array_lit> <lit_more> 
<array_content>	→	{ <array_row> } <row_more>
<array_row>	→	<array_lit> <lit_more> 
<row_more>	→	, <row_more_ext>
<row_more>	→	λ
<row_more_ext>	→	{ <array_row> } <row_more>
<row_more_ext>	→	id_lit <row_more>
<lit_more>	→	, <lit_more_ext>
<lit_more>	→	λ
<lit_more_ext>	→	<array_lit> <lit_more>
<lit_more_ext>	→	{ <array_row> } <row_more>
<array_more>	→	, id_lit [ <array_size> ] <column> <array_initialization> <array_more>
<array_more>	→	λ
<array_lit>	→	<lit4>
<array_lit>	→	id_lit
<assignment_operator>	→	+=
<assignment_operator>	→	-=
<assignment_operator>	→	*=
<assignment_operator>	→	/=
<assignment_operator>	→	%=
<assignment_operand>	→	id_lit <id_ext> <more_arith>
<assignment_operand>	→	<lit3> <more_arith>
<assignment_operand>	→	<arithmetic_operand_2> <arithmetic_operator> <arithmetic_operand> <more_arith>
<logical_exp>	→	<logical_operator1> <logical_operand> <logical_operator> <logical_operator1> <logical_operand> <more_log>
<logical_operand>	→	id_lit <id_ext> <logical_operand_ext>
<logical_operand>	→	<lit3> <more_arith> <relational_operator> <relational_operand> <relational_more>
<logical_operand>	→	scroll_lit <relational_operator> <relational_operand> <relational_more>
<logical_operand>	→	rose_lit <relational_operator> <relational_operand> <relational_more>
<logical_operand>	→	mirror_lit <relational_more>
<logical_operand>	→	<treasures_mirror> <relational_more>
<logical_operand>	→	( <logical_operator1> <expression>
<expression>	→	id_lit <id_ext> <expression_ext_1>
<expression>	→	<lit3> <expression_ext_1>
<expression>	→	scroll_lit <expression_ext_2>
<expression>	→	rose_lit <expression_ext_2>
<expression>	→	mirror_lit <expression_ext_2>
<expression>	→	<treasures_mirror> <expression_ext_2>
<expression>	→	( <logical_operator1> <expression> <more_log> ) <logical_operand_ext>
<expression_ext_1>	→	<relational_operator> <relational_operand> <relational_more> <more_log> ) <relational_more>
<expression_ext_1>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log> ) 
<expression_ext_1>	→	<arithmetic_operator> <arithmetic_operand> <more_arith> <relational_more> ) <more_arith> <relational_more>
<expression_ext_2>	→	<relational_operator> <relational_operand> <relational_more> ) <relational_more>
<expression_ext_2>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log> ) 
<logical_operand_ext>	→	<more_arith> <relational_operator> <relational_operand> <relational_more>
<logical_operand_ext>	→	λ
<logical_operator>	→	&&
<logical_operator>	→	||
<logical_operator1>	→	!
<logical_operator1>	→	λ
<more_log>	→	 <logical_operator> <logical_operator1> <logical_operand> <more_log>
<more_log>	→	λ
<treasures_mirror>	→	1
<treasures_mirror>	→	0
<arithmetic_exp>	→	<arithmetic_operand> <arithmetic_operator> <arithmetic_operand> <more_arith>
<arithmetic_operand_1>	→	id_lit <id_ext>
<arithmetic_operand_1>	→	<lit3>
<arithmetic_operand_2>	→	( <arithmetic_exp> )
<arithmetic_operand>	→	<arithmetic_operand_1>
<arithmetic_operand>	→	<arithmetic_operand_2>
<arithmetic_operator>	→	+
<arithmetic_operator>	→	-
<arithmetic_operator>	→	/
<arithmetic_operator>	→	*
<arithmetic_operator>	→	%
<more_arith>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>
<more_arith>	→	λ
<relational_exp>	→	<relational_operand> <relational_operator> <relational_operand> <relational_more> 
<relational_operand>	→	id_lit <id_ext> <more_arith>
<relational_operand>	→	<lit3> <more_arith>
<relational_operand>	→	scroll_lit
<relational_operand>	→	rose_lit
<relational_operand>	→	mirror_lit
<relational_operand>	→	treasures_mirror
<relational_operand>	→	( <expression_2>
<expression_2>	→	id_lit <id_ext> <expression_2_ext>
<expression_2>	→	<lit3> <expression_2_ext>
<expression_2>	→	scroll_lit <relational_operator> <relational_operand> <relational_more> )
<expression_2>	→	rose_lit <relational_operator> <relational_operand> <relational_more> )
<expression_2>	→	mirror_lit  <relational_operator> <relational_operand> <relational_more> )
<expression_2>	→	treasures_mirror <relational_operator> <relational_operand> <relational_more> )
<expression_2>	→	( <expression_2> )
<expression_2_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith> ) <more_arith>
<expression_2_ext>	→	<relational_operator> <relational_operand> <relational_more> )
<relational_operator>	→	<
<relational_operator>	→	>
<relational_operator>	→	<=
<relational_operator>	→	>=
<relational_operator>	→	==
<relational_operator>	→	!=
<relational_more>	→	<relational_operator> <relational_operand> <relational_more>
<relational_more>	→	λ
<unary>	→	id_lit <unary_operator>
<unary_operator>	→	++
<unary_operator>	→	--
<string_operand>	→	<lit1>
<string_operand>	→	id_lit <id_ext>
<string_operand>	→	toscroll ( <conversion_value> )
<string_more>	→	+ <string_operand> <string_more>
<string_more>	→	λ
<user-defined_func>	→	spell <return_type> id_lit ( <param> ) { <body> <ret_statement> } <user-defined_func>
<user-defined_func>	→	λ
<return_type>	→	<data_type>
<return_type>	→	chamber
<param>	→	<data_type> id_lit <param_more>
<param>	→	λ
<param_more>	→	, <data_type> id_lit <param_more>
<param_more>	→	λ
<body>	→	<dynasty> <data_type> id_lit <vardec_def> <body>
<body>	→	granted ( <granted_content> <more_granted> ) ~ <body>
<body>	→	id_lit <body_1_ext> <body>
<body>	→	spell <return_type> id_lit ( <param> ) { <body> <ret_statement> }  <body>
<body>	→	tale ( <loop_var> ~ <relational_exp> ~ <unary> ) { <loop_body> } <body>
<body>	→	cast ( <condition> ) { <body> } <elif> <else> <body>
<body>	→	forever ( <condition> ) { <loop_body> } <body>
<body>	→	believe { <loop_body> } forever ( <condition> ) ~ <body>
<body>	→	λ
<body_1_ext>	→	( <args> ) ~ 
<body_1_ext>	→	 <index> <body_1_other_ext>
<body_1_ext>	→	<unary_operator> ~ 
<body_1_other_ext>	→	= <val> ~
<body_1_other_ext>	→	<assignment_operator> <assignment_operand> ~ 
<ret_statement>	→	return <val1> ~
<ret_statement>	→	λ
<loop_var>	→	treasures id_lit = <loop_val>
<loop_var>	→	id_lit <loop_init>
<loop_init>	→	=  <loop_val>
<loop_init>	→	λ
<loop_val>	→	id_lit 
<loop_val>	→	treasures_lit
<loop_body>	→	<dynasty> <data_type> id_lit <vardec_def> <loop_body>
<loop_body>	→	granted ( <granted_content> <more_granted> ) ~ <loop_body>
<loop_body>	→	id_lit <body_1_ext> <loop_body>
<loop_body>	→	spell <return_type> id_lit ( <param> ) { <body> <ret_statement> }  <loop_body>
<loop_body>	→	tale ( <loop_var> ~ <relational_exp> ~ <unary> ) { <loop_body> } <loop_body>
<loop_body>	→	cast ( <condition> ) {  <loop_body> <flow_control> } <elif_break> <else_break> <loop_body>
<loop_body>	→	forever ( <condition> ) { <loop_body> } <loop_body>
<loop_body>	→	believe { <loop_body> } forever ( <condition> ) ~ <loop_body>
<loop_body>	→	λ
<elif_break>	→	twist ( <condition> ) { <body> <flow_control> } <elif_break>
<elif_break>	→	λ
<else_break>	→	curse { <body> <flow_control> }
<else_break>	→	λ
<flow_control>	→	break ~
<flow_control>	→	continue ~
<flow_control>	→	λ
<condition>	→	<treasures_mirror> <more_log>
<condition>	→	id_lit <condi_id_ext>
<condition>	→	! <logical_operand> <more_log>
<condition>	→	mirror_lit <relational_more> <more_log>
<condition>	→	<lit3> <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<condition>	→	scroll_lit <relational_operator> <relational_operand> <relational_more> <more_log>
<condition>	→	rose_lit <relational_operator> <relational_operand> <relational_more> <more_log>
<condition>	→	( <logical_operator1> <expression> <more_log> 
<condi_id_ext>	→	<func_call> <other_id_ext>
<condi_id_ext>	→	[ <array_size> ] <column1> <other_id_ext>
<condi_id_ext>	→	<other_id_ext>
<other_id_ext>	→	<more_arith> <relational_operator> <relational_operand> <relational_more> <more_log>
<other_id_ext>	→	λ
<elif>	→	twist ( <condition> ) { <body> } <elif>
<elif>	→	λ
<else>	→	curse { <body> }
<else>	→	λ
<granted_content_1>	→	set_precision
<granted_content_1>	→	id_lit <granted_id_ext>
<granted_content_2>	→	phantom
<granted_content_2>	→	lengthof ( id_lit <index> )
<granted_content_2>	→	<conversion_func> ( <conversion_value> )
<granted_content_2>	→	toscroll ( <conversion_value> ) <string_more>
<granted_content_2>	→	<treasures_mirror> <more_log>
<granted_content_2>	→	mirror_lit <relational_more> <more_log>
<granted_content_2>	→	scroll_lit <granted_scroll_ext>
<granted_content_2>	→	rose_lit <granted_rose_ext>
<granted_content_2>	→	<lit3>  <granted_lit3_ext>
<granted_content_2>	→	( <logical_operator1> <granted_open_paren_ext> 
<granted_content_2>	→	!  <logical_operand> <more_log> 
<granted_content>	→	<granted_content_1>
<granted_content>	→	<granted_content_2>
<granted_open_paren_ext>	→	id_lit <id_ext> <idlit3_granted_ext>
<granted_open_paren_ext>	→	<lit3> <idlit3_granted_ext>
<granted_open_paren_ext>	→	scroll_lit <expression_ext_2> <more_log> )
<granted_open_paren_ext>	→	rose_lit <expression_ext_2> <more_log> )
<granted_open_paren_ext>	→	mirror_lit <expression_ext_2> <more_log> )
<granted_open_paren_ext>	→	<treasures_mirror> <expression_ext_2> <more_log> )
<granted_open_paren_ext>	→	( <logical_operator1> <granted_open_paren_ext> ) <close_paren_ext>
<idlit3_granted_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log> ) <relational_more> <more_log>
<idlit3_granted_ext>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log> ) <more_log>
<idlit3_granted_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith> <relational_more> <more_log> ) <more_arith> <open_paren_other_ext>
<open_paren_other_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<open_paren_other_ext>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log>
<open_paren_other_ext>	→	λ
<close_paren_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<close_paren_ext>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log>
<close_paren_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith>  <open_paren_other_ext>
<close_paren_ext>	→	λ
<granted_id_ext>	→	<unary_operator>
<granted_id_ext>	→	<func_call> <granted_other_id_ext>
<granted_id_ext>	→	[ <array_size> ] <column1> <granted_other_id_ext>
<granted_id_ext>	→	 <granted_other_id_ext>
<granted_other_id_ext>	→	+ <plus_ext>
<granted_other_id_ext>	→	- <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<granted_other_id_ext>	→	* <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<granted_other_id_ext>	→	/ <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<granted_other_id_ext>	→	% <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<granted_other_id_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_other_id_ext>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log>
<granted_other_id_ext>	→	λ
<granted_other_id_ext2>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_other_id_ext2>	→	λ
<plus_ext>	→	id_lit <plus_ext_1>
<plus_ext>	→	toscroll ( <conversion_value> ) <string_more> 
<plus_ext>	→	scroll_lit <string_more> 
<plus_ext>	→	rose_lit <string_more> 
<plus_ext>	→	( <arithmetic_exp> ) <more_arith> <granted_other_id_ext2>
<plus_ext>	→	treasures_lit <more_arith> <granted_other_id_ext2> 
<plus_ext>	→	ocean_lit <more_arith> <granted_other_id_ext2> 
<plus_ext_1>	→	 + <plus_ext> 
<plus_ext_1>	→	 - <arithmetic_operand> <more_arith> <granted_other_id_ext2> 
<plus_ext_1>	→	 * <arithmetic_operand> <more_arith> <granted_other_id_ext2> 
<plus_ext_1>	→	 / <arithmetic_operand> <more_arith> <granted_other_id_ext2> 
<plus_ext_1>	→	 % <arithmetic_operand> <more_arith> <granted_other_id_ext2> 
<plus_ext_1>	→	 λ 
<granted_scroll_ext>	→	+ <string_operand> <string_more>
<granted_scroll_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_scroll_ext>	→	λ
<granted_rose_ext>	→	+ <string_operand> <string_more>
<granted_rose_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_rose_ext>	→	λ
<granted_lit3_ext>	→	<arithmetic_operator> <arithmetic_operand> <more_arith> <granted_lit3_ext1>
<granted_lit3_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_lit3_ext>	→	λ
<granted_lit3_ext1>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<granted_lit3_ext1>	→	λ
<more_granted>	→	, <granted_content> <more_granted>
<more_granted>	→	λ
<data_type>	→	scroll
<data_type>	→	treasures
<data_type>	→	mirror
<data_type>	→	ocean
<data_type>	→	rose
<val>	→	<granted_content_2>
<val>	→	id_lit <granted_id_ext>
<val>	→	<input>
<val1>	→	<granted_content_2>
<val1>	→	id_lit <val1_ext>
<val1_ext>	→	<val1_id_ext>
<val1_ext>	→	<func_call> <val1_id_ext>
<val1_ext>	→	[ <array_size> ] <column1> <val1_id_ext>
<val1_ext>	→	<unary_operator>
<val1_ext>	→	+ <plus_ext>
<val1_ext>	→	- <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<val1_ext>	→	* <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<val1_ext>	→	/ <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<val1_ext>	→	% <arithmetic_operand> <more_arith> <granted_other_id_ext2>
<val1_ext>	→	<relational_operator> <relational_operand> <relational_more> <more_log>
<val1_ext>	→	<logical_operator> <logical_operator1> <logical_operand> <more_log>
<val1_id_ext>	→	<assignment_operator> <assignment_operand>
<val1_id_ext>	→	λ
<conversion_func>	→	torose
<conversion_func>	→	totreasures
<conversion_func>	→	toocean
<conversion_func>	→	tomirror
<conversion_value>	→	<lit4>
<conversion_value>	→	id_lit <id_ext>
<index>	→	[ <array_size> ] <column1>
<index>	→	λ
<column1>	→	[ <array_size> ]
<column1>	→	λ
<input>	→	wish ( scroll_lit )
<lit1>	→	scroll_lit
<lit1>	→	rose_lit
<lit2>	→	mirror_lit
<lit3>	→	ocean_lit
<lit3>	→	treasures_lit
<lit4>	→	<lit1>
<lit4>	→	<lit2>
<lit4>	→	<lit3>
<func_call>	→	( <args> )
<args>	→	<args_val> <args_more>
<args>	→	λ
<args_val>	→	id_lit <id_ext>
<args_val>	→	<lit4>
<args_more>	→	, <args_val> <args_more>
<args_more>	→	λ
<id_ext>	→	<func_call>
<id_ext>	→	[ <array_size> ] <column1>
<id_ext>	→	λ
<array_size>	→	id_lit
<array_size>	→	positive_treasures_lit
""" # <-- Replace with your full input

lines = input_text.strip().split('\n')
cfg = convert_cfg_table(lines)
output = format_cfg_dict(cfg)
print(output)