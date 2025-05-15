from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters

castle_grammar = r"""
// Fantasy Programming Language Grammar in Lark Format

start: program

program: "crown~" global_dec user_defined_func "castle" "treasures" IDENTIFIER "(" ")" "{" body "}" "return" "0" "~" "}" "reign~"

global_dec: var_dec global_dec | 

var_dec: dynasty data_type IDENTIFIER vardec_def

dynasty: "dynasty" | 

vardec_def: variable_def | array_def

variable_def: initialization vardec_more "~"

array_def: "[" array_size "]" column array_initialization array_more "~"

initialization: "=" val | 

vardec_more: vardec_more_list | 

vardec_more_list: "," IDENTIFIER initialization vardec_more

column: "[" array_size "]" | 

array_initialization: "=" array_list | 

array_list: "{" array_content "}"

array_content: simple_array_content | nested_array_content | id_array_content

simple_array_content: array_lit lit_more

nested_array_content: "{" array_row "}" row_more

id_array_content: IDENTIFIER row_more

array_row: array_lit lit_more

row_more: row_more_ext | 

row_more_ext: "," row_more_content row_more

row_more_content: "{" array_row "}" | IDENTIFIER 

lit_more: lit_more_ext | 

lit_more_ext: "," array_lit lit_more

array_more: array_more_ext | 

array_more_ext: "," IDENTIFIER "[" array_size "]" column array_initialization array_more

array_lit: lit4 | IDENTIFIER 

assignment_operator: "+=" | "-=" | "*=" | "/=" | "%="

assignment_operand: assignment_operand_id | assignment_operand_lit | assignment_operand_arith

assignment_operand_id: IDENTIFIER id_ext more_arith

assignment_operand_lit: lit3 more_arith

assignment_operand_arith: arithmetic_operand_2 arithmetic_operator arithmetic_operand more_arith

logical_exp: logical_exp_binary | logical_exp_not

logical_exp_binary: logical_operator1 logical_operand logical_operator logical_operator1 logical_operand more_log

logical_exp_not: "!" logical_operand more_log

logical_operand: logical_operand_id | logical_operand_lit3 | logical_operand_scroll | logical_operand_rose | logical_operand_mirror | logical_operand_treasures | logical_operand_paren

logical_operand_id: IDENTIFIER id_ext logical_operand_ext

logical_operand_lit3: lit3 more_arith relational_operator relational_operand relational_more

logical_operand_scroll: SCROLL_LIT relational_operator relational_operand relational_more

logical_operand_rose: ROSE_LIT relational_operator relational_operand relational_more

logical_operand_mirror: MIRROR_LIT relational_more

logical_operand_treasures: treasures_mirror relational_more

logical_operand_paren: "(" expression

expression: expression_rel | expression_log | expression_arith

expression_rel: relational_exp ")" relational_more

expression_log: logical_exp ")"

expression_arith: arithmetic_exp ")" more_arith relational_operator relational_operand relational_more

logical_operand_ext: logical_operand_ext_rel | 

logical_operand_ext_rel: more_arith relational_operator relational_operand relational_more

logical_operator: "&&" | "||"

logical_operator1: "!" | 

more_log: more_log_ext | 

more_log_ext: logical_operator logical_operator1 logical_operand more_log

treasures_mirror: "1" | "0"

arithmetic_exp: arithmetic_operand arithmetic_operator arithmetic_operand more_arith

arithmetic_operand_1: arithmetic_operand_1_id | arithmetic_operand_1_lit

arithmetic_operand_1_id: IDENTIFIER id_ext

arithmetic_operand_1_lit: lit3

arithmetic_operand_2: "(" arithmetic_exp ")"

arithmetic_operand: arithmetic_operand_1 | arithmetic_operand_2

arithmetic_operator: "+" | "-" | "/" | "*" | "%"

more_arith: more_arith_ext | 

more_arith_ext: arithmetic_operator arithmetic_operand more_arith

relational_exp: relational_operand relational_operator relational_operand relational_more

relational_operand: relational_operand_id | relational_operand_lit3 | relational_operand_scroll | relational_operand_rose | relational_operand_mirror | relational_operand_treasures | relational_operand_paren

relational_operand_id: IDENTIFIER id_ext more_arith

relational_operand_lit3: lit3 more_arith

relational_operand_scroll: SCROLL_LIT

relational_operand_rose: ROSE_LIT

relational_operand_mirror: MIRROR_LIT

relational_operand_treasures: treasures_mirror

relational_operand_paren: "(" expression_2

expression_2: expression_2_arith | expression_2_rel

expression_2_arith: arithmetic_exp ")" more_arith

expression_2_rel: relational_exp ")"

relational_operator: "<" | ">" | "<=" | ">=" | "==" | "!="

relational_more: relational_more_ext | 

relational_more_ext: relational_operator relational_operand relational_more

unary: IDENTIFIER unary_operator

unary_operator: "++" | "--"

string_operand: string_operand_lit | string_operand_id | string_operand_conv

string_operand_lit: lit1

string_operand_id: IDENTIFIER id_ext

string_operand_conv: "toscroll" "(" conversion_value ")"

string_more: string_more_ext | 

string_more_ext: "+" string_operand string_more

user_defined_func: user_defined_func_def | 

user_defined_func_def: "spell" return_type IDENTIFIER "(" param ")" "{" body ret_statement "}" user_defined_func

return_type: data_type | "chamber"

param: param_list | 

param_list: data_type IDENTIFIER param_more

param_more: param_more_ext | 

param_more_ext: "," data_type IDENTIFIER param_more

body_1: body_var_dec | body_output | body_id | body_func | body_for

body_var_dec: var_dec body

body_output: output body

body_id: IDENTIFIER body_1_ext body

body_func: user_defined_func body

body_for: for_loop body

body_1_ext: body_1_ext_func | body_1_ext_assign | body_1_ext_unary | body_1_ext_complex_assign

body_1_ext_func: "(" args ")" "~"

body_1_ext_assign: index "=" val "~"

body_1_ext_unary: unary_operator "~"

body_1_ext_complex_assign: index assignment_operator assignment_operand "~"

body_2: condi_statement body

body: body_1 | body_2 | 

ret_statement: ret_statement_val | 

ret_statement_val: "return" val1 "~"

condi_statement: condi_if | condi_while | condi_do_while

condi_if: if

condi_while: while

condi_do_while: do_while

for_loop: "tale" "(" loop_var "~" relational_exp "~" unary ")" "{" loop_body "}"

loop_var: loop_var_treasures | loop_var_id

loop_var_treasures: "treasures" IDENTIFIER "=" loop_val

loop_var_id: IDENTIFIER loop_init

loop_init: loop_init_assign | 

loop_init_assign: "=" loop_val

loop_val: IDENTIFIER | TREASURES_LIT

loop_body: loop_body_basic | loop_body_if_break | loop_body_while | loop_body_do_while | 

loop_body_basic: body_1 loop_body

loop_body_if_break: if_break loop_body

loop_body_while: while loop_body

loop_body_do_while: do_while loop_body

if_break: "cast" "(" condition ")" "{" body flow_control "}" elif_break else_break

elif_break: elif_break_ext | 

elif_break_ext: "twist" "(" condition ")" "{" body flow_control "}" elif_break

else_break: else_break_body | 

else_break_body: "curse" "{" body flow_control "}"

flow_control: flow_control_break | flow_control_continue | 

flow_control_break: "break" "~"

flow_control_continue: "continue" "~"

do_while: "believe" "{" loop_body "}" "forever" "(" condition ")" "~"

condition: condition_treasures | condition_id | condition_logical | condition_mirror | condition_lit3 | condition_scroll | condition_rose | condition_paren

condition_treasures: treasures_mirror more_log

condition_id: IDENTIFIER condi_id_ext

condition_logical: logical_operator1 logical_operand more_log

condition_mirror: MIRROR_LIT relational_more more_log

condition_lit3: lit3 more_arith relational_operator relational_operand relational_more more_log

condition_scroll: SCROLL_LIT relational_operator relational_operand relational_more more_log

condition_rose: ROSE_LIT relational_operator relational_operand relational_more more_log

condition_paren: "(" expression_3

expression_3: expression_3_rel | expression_3_log | expression_3_arith

expression_3_rel: relational_exp ")" relational_more more_log

expression_3_log: logical_exp ")" more_log

expression_3_arith: arithmetic_exp ")" more_arith relational_operator relational_operand relational_more more_log

condi_id_ext: condi_id_mirror | condi_id_ext_other | 

condi_id_mirror: mirror_init

condi_id_ext_other: id_ext other_id_ext

other_id_ext: other_id_ext_1 other_id_ext_2

other_id_ext_1: other_id_ext_1_rel | 

other_id_ext_1_rel: more_arith relational_operator relational_operand relational_more more_log

other_id_ext_2: other_id_ext_2_log | 

other_id_ext_2_log: logical_operator more_log

mirror_init: "==" MIRROR_LIT | "!=" MIRROR_LIT | 

while: "forever" "(" condition ")" "{" loop_body "}"

if: "cast" "(" condition ")" "{" body "}" elif else

elif: elif_ext | 

elif_ext: "twist" "(" condition ")" "{" body "}" elif

else: else_body | 

else_body: "curse" "{" body "}"

output: "granted" "(" granted_content more_granted ")" "~"

granted_content: granted_content_type1 | granted_content_type2

granted_content_type1: granted_content_type1_set | granted_content_type1_id

granted_content_type1_set: "set_precision"

granted_content_type1_id: IDENTIFIER granted_id_ext

granted_content_type2: granted_content_phantom | granted_content_length | granted_content_conv | granted_content_toscroll | granted_content_treasures | granted_content_mirror | granted_content_scroll | granted_content_rose | granted_content_lit3 | granted_content_paren | granted_content_logical

granted_content_phantom: "phantom"

granted_content_length: "lengthof" "(" IDENTIFIER index ")"

granted_content_conv: conversion_func "(" conversion_value ")"

granted_content_toscroll: "toscroll" "(" conversion_value ")" string_more

granted_content_treasures: treasures_mirror more_log

granted_content_mirror: MIRROR_LIT relational_more more_log

granted_content_scroll: SCROLL_LIT granted_scroll_ext

granted_content_rose: ROSE_LIT granted_rose_ext

granted_content_lit3: lit3 granted_lit3_ext

granted_content_paren: "(" granted_open_paren_ext

granted_content_logical: logical_operator1 logical_operand more_log

granted_open_paren_ext: granted_open_paren_arith | granted_open_paren_exp | granted_open_paren_exp2

granted_open_paren_arith: arithmetic_exp ")" more_arith

granted_open_paren_exp: expression more_log

granted_open_paren_exp2: expression_2 relational_more

granted_id_ext: granted_id_ext_unary | granted_id_ext_complex | 

granted_id_ext_unary: unary_operator

granted_id_ext_complex: id_ext granted_other_id_ext

granted_other_id_ext: granted_other_id_ext_string | granted_other_id_ext_arith | granted_other_id_ext_rel | granted_other_id_ext_log | 

granted_other_id_ext_string: "+" string_operand string_more

granted_other_id_ext_arith: arithmetic_operator arithmetic_operand more_arith

granted_other_id_ext_rel: more_arith relational_operator relational_operand relational_more

granted_other_id_ext_log: logical_operand_ext logical_operator more_log

granted_scroll_ext: granted_scroll_ext_string | granted_scroll_ext_rel | 

granted_scroll_ext_string: "+" string_operand string_more

granted_scroll_ext_rel: relational_operator relational_operand relational_more more_log

granted_rose_ext: granted_rose_ext_string | granted_rose_ext_rel | 

granted_rose_ext_string: "+" string_operand string_more

granted_rose_ext_rel: relational_operator relational_operand relational_more more_log

granted_lit3_ext: granted_lit3_ext_arith | granted_lit3_ext_rel | 

granted_lit3_ext_arith: arithmetic_operator arithmetic_operand more_arith

granted_lit3_ext_rel: more_arith relational_operator relational_operand relational_more more_log

more_granted: more_granted_ext | 

more_granted_ext: "," granted_content more_granted

data_type: "scroll" | "treasures" | "mirror" | "ocean" | "rose"

val: val_granted | val_id | val_input

val_granted: granted_content_type2

val_id: IDENTIFIER granted_id_ext

val_input: input

val1: val1_granted | val1_id

val1_granted: granted_content_type2

val1_id: IDENTIFIER val1_ext

val1_ext: val1_ext_id | val1_ext_unary | 

val1_ext_id: id_ext val1_id_ext

val1_ext_unary: unary_operator

val1_id_ext: val1_id_ext_granted | val1_id_ext_assign | 

val1_id_ext_granted: granted_other_id_ext

val1_id_ext_assign: assignment_operator assignment_operand

conversion_func: "torose" | "totreasures" | "toocean" | "tomirror"

conversion_value: conversion_value_lit | conversion_value_id

conversion_value_lit: lit4

conversion_value_id: IDENTIFIER id_ext

index: index_array | 

index_array: "[" array_size "]" column1

column1: column1_array | 

column1_array: "[" array_size "]"

input: "wish" "(" SCROLL_LIT ")"

lit1: SCROLL_LIT | ROSE_LIT

lit2: MIRROR_LIT

lit3: OCEAN_LIT | TREASURES_LIT

lit4: lit4_1 | lit4_2 | lit4_3

lit4_1: lit1
lit4_2: lit2
lit4_3: lit3

func_call: "(" args ")"

args: args_list | 

args_list: args_val args_more

args_val: args_val_id | args_val_lit

args_val_id: IDENTIFIER id_ext

args_val_lit: lit4

args_more: args_more_list | 

args_more_list: "," args_val args_more

array_element: index

id_ext: id_ext_func | id_ext_array | 

id_ext_func: func_call

id_ext_array: array_element

array_size: array_size_id | array_size_lit

array_size_id: IDENTIFIER 

array_size_lit: POSITIVE_TREASURES_LIT

          
COMMENTS: "single_comment" | "multi_comment"

// String literal (scroll_lit)
SCROLL_LIT: ESCAPED_STRING

// Char literal (rose_lit)
ROSE_LIT: /'(\\.|[^\\'])'/

// Boolean literal (mirror_lit)
MIRROR_LIT: "true" | "false" | "1" | "0"

NEGATIVE: /-?/

// Integer literal (treasures_lit)
TREASURES_LIT: /-?[0-9]+/
POSITIVE_TREASURES_LIT: /0|[1-9][0-9]*/

// Float literal (ocean_lit)
OCEAN_LIT: /[0-9]+\.[0-9]+/

// Identifier: starts with a capital letter, then letters/digits/underscores
IDENTIFIER: /[A-Z][A-Za-z0-9_]*/

%import common.WS
%import common.ESCAPED_STRING
%ignore WS
%ignore COMMENTS
"""
parser = Lark(castle_grammar, parser="lalr", start="start")

source_code = '''
crown ~ 
scroll A = B ~
castle treasures MyFunc() { } return 0 ~ } reign ~
'''

tree = parser.parse(source_code)
print(tree.pretty())