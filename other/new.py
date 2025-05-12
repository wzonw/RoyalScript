from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters

from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters

castle_grammar = r"""
start: program
program: "crown" "TILDE" global_dec? user_defined_func* "castle" "treasures" IDENTIFIER "LPAREN" "RPAREN" "LCUR" body return_statement "RCUR" "reign" "TILDE" "EOF"

global_dec: var_dec+

var_dec: dynasty data_type IDENTIFIER vardec_def

dynasty: "dynasty"

vardec_def: initialization vardec_more? "TILDE"
          | "LSQR" array_size "RSQR" column? array_initialization array_more? "TILDE"

initialization: "EQUAL" val

vardec_more: "COMMA" IDENTIFIER initialization vardec_more?

column: "LSQR" array_size "RSQR"

array_initialization: "EQUAL" array_list

array_list: "LCUR" array_content "RCUR"

array_content: lit4 lit_more?
             | "LCUR" array_row "RCUR" row_more?
             | IDENTIFIER array_content_ext1?

array_content_ext1: "COMMA" array_content_ext2

array_content_ext2: row_more_ext
                  | array_lit lit_more?

array_row: array_lit lit_more?

row_more: "COMMA" row_more_ext

row_more_ext: "LCUR" array_row "RCUR" row_more?
            | IDENTIFIER row_more?

lit_more: "COMMA" array_lit lit_more?

array_more: "COMMA" IDENTIFIER "LSQR" array_size "RSQR" column? array_initialization array_more?

array_lit: lit4
         | IDENTIFIER

assignment_operator: "ADD_EQUAL"
                  | "SUB_EQUAL"
                  | "MUL_EQUAL"
                  | "DIV_EQUAL"
                  | "MOD_EQUAL"

assignment_operand: IDENTIFIER id_ext? more_arith?
                  | lit3 more_arith?
                  | arithmetic_operand_2 arithmetic_operator arithmetic_operand more_arith?

logical_exp: logical_operator1? logical_operand logical_operator logical_operator1? logical_operand more_log?

logical_operand: IDENTIFIER id_ext? logical_operand_ext?
               | lit3 more_arith? relational_operator relational_operand relational_more?
               | SCROLL_LIT relational_operator relational_operand relational_more?
               | ROSE_LIT relational_operator relational_operand relational_more?
               | MIRROR_LIT relational_more?
               | treasures_mirror relational_more?
               | "LPAREN" expression

expression: relational_exp "RPAREN" relational_more?
          | logical_exp "RPAREN"
          | arithmetic_exp "RPAREN" more_arith? relational_operator relational_operand relational_more?

logical_operand_ext: more_arith? relational_operator relational_operand relational_more?

logical_operator: "AND"
               | "OR"

logical_operator1: "NOT"

more_log: logical_operator logical_operator1? logical_operand more_log?

treasures_mirror: "1"
                | "0"

arithmetic_exp: arithmetic_operand arithmetic_operator arithmetic_operand more_arith?

arithmetic_operand_1: IDENTIFIER id_ext?
                    | lit3

arithmetic_operand_2: "LPAREN" arithmetic_exp "RPAREN"

arithmetic_operand: arithmetic_operand_1
                 | arithmetic_operand_2

arithmetic_operator: "ADD"
                  | "SUB"
                  | "DIV"
                  | "MUL"
                  | "MOD"

more_arith: arithmetic_operator arithmetic_operand more_arith?

relational_exp: relational_operand relational_operator relational_operand relational_more?

relational_operand: IDENTIFIER id_ext? more_arith?
                  | lit3 more_arith?
                  | SCROLL_LIT
                  | ROSE_LIT
                  | MIRROR_LIT
                  | treasures_mirror
                  | "LPAREN" expression_2

expression_2: arithmetic_exp "RPAREN" more_arith?
            | relational_exp "RPAREN"

relational_operator: "LESS"
                  | "GREATER"
                  | "LESS_EQUAL"
                  | "GREATER_EQUAL"
                  | "EQUAL_EQUAL"
                  | "NOT_EQUAL"

relational_more: relational_operator relational_operand relational_more?

unary: IDENTIFIER unary_operator

unary_operator: "INC"
              | "DEC"

string_operand: lit1
              | IDENTIFIER id_ext?
              | "toscroll" "LPAREN" conversion_value "RPAREN"

string_more: "ADD" string_operand string_more?

user_defined_func: "spell" return_type IDENTIFIER "LPAREN" param? "RPAREN" "LCUR" body ret_statement "RCUR"

ret_statement: "return" val1 "TILDE"

return_type: data_type
           | "chamber"

param: data_type IDENTIFIER param_more?

param_more: "COMMA" data_type IDENTIFIER param_more?

body_1: var_dec body?
      | output body?
      | IDENTIFIER body_1_ext body?
      | user_defined_func body?
      | for_loop body?

body_1_ext: "LPAREN" args? "RPAREN" "TILDE"
          | index "EQUAL" val "TILDE"
          | unary_operator "TILDE"
          | index assignment_operator assignment_operand "TILDE"

body_2: condi_statement body?

body: body_1
    | body_2

return_statement: "return" val1 "TILDE"

condi_statement: if
               | while
               | do_while

for_loop: "tale" "LPAREN" loop_var "TILDE" relational_exp "TILDE" unary "RPAREN" "LCUR" loop_body? "RCUR"

loop_var: "treasures" IDENTIFIER "EQUAL" loop_val
        | IDENTIFIER loop_init

loop_init: "EQUAL" loop_val

loop_val: IDENTIFIER
        | TREASURES_LIT
        | "1"
        | "0"

loop_body: body_1 loop_body?
         | if_break loop_body?
         | while loop_body?
         | do_while loop_body?

if_break: "cast" "LPAREN" condition "RPAREN" "LCUR" body flow_control "RCUR" elif_break? else_break?

elif_break: "twist" "LPAREN" condition "RPAREN" "LCUR" body flow_control "RCUR" elif_break?

else_break: "curse" "LCUR" body flow_control "RCUR"

flow_control: "break" "TILDE"
            | "continue" "TILDE"

do_while: "believe" "LCUR" loop_body? "RCUR" "forever" "LPAREN" condition "RPAREN" "TILDE"

condition: treasures_mirror more_log?
         | IDENTIFIER condi_id_ext?
         | logical_operator1 logical_operand more_log?
         | MIRROR_LIT relational_more? more_log?
         | lit3 more_arith? relational_operator relational_operand relational_more? more_log?
         | SCROLL_LIT relational_operator relational_operand relational_more? more_log?
         | ROSE_LIT relational_operator relational_operand relational_more? more_log?
         | "LPAREN" expression_3

expression_3: relational_exp "RPAREN" relational_more? more_log?
            | logical_exp "RPAREN" more_log?
            | arithmetic_exp "RPAREN" more_arith? relational_operator relational_operand relational_more? more_log?

condi_id_ext: mirror_init
            | id_ext? other_id_ext?

other_id_ext: other_id_ext_1 other_id_ext_2?

other_id_ext_1: more_arith? relational_operator relational_operand relational_more? more_log?

other_id_ext_2: logical_operand more_log?

mirror_init: "EQUAL_EQUAL" MIRROR_LIT
           | "NOT_EQUAL" MIRROR_LIT

while: "forever" "LPAREN" condition "RPAREN" "LCUR" loop_body? "RCUR"

if: "cast" "LPAREN" condition "RPAREN" "LCUR" body "RCUR" elif? else?

elif: "twist" "LPAREN" condition "RPAREN" "LCUR" body "RCUR" elif?

else: "curse" "LCUR" body "RCUR"

output: "granted" "LPAREN" granted_content more_granted? "RPAREN" "TILDE"

granted_content_1: "set_precision"
                 | IDENTIFIER granted_id_ext?

granted_content_2: "phantom"
                 | "lengthof" "LPAREN" IDENTIFIER index? "RPAREN"
                 | conversion_func "LPAREN" conversion_value "RPAREN"
                 | "toscroll" "LPAREN" conversion_value "RPAREN" string_more?
                 | treasures_mirror more_log?
                 | MIRROR_LIT relational_more? more_log?
                 | SCROLL_LIT granted_scroll_ext?
                 | ROSE_LIT granted_rose_ext?
                 | lit3 granted_lit3_ext?
                 | "LPAREN" granted_open_paren_ext
                 | logical_operator1 logical_operand more_log?

granted_content: granted_content_1
               | granted_content_2

granted_open_paren_ext: arithmetic_exp "RPAREN" more_arith?
                      | expression more_log?
                      | expression_2 relational_more?

granted_id_ext: unary_operator
              | id_ext? granted_other_id_ext?

granted_other_id_ext: "ADD" string_operand string_more?
                    | arithmetic_operator arithmetic_operand more_arith?
                    | more_arith? relational_operator relational_operand relational_more?
                    | logical_operand_ext? more_log?

granted_scroll_ext: "ADD" string_operand string_more?
                  | relational_operator relational_operand relational_more? more_log?

granted_rose_ext: "ADD" string_operand string_more?
                | relational_operator relational_operand relational_more? more_log?

granted_lit3_ext: arithmetic_operator arithmetic_operand more_arith?
                | more_arith? relational_operator relational_operand relational_more? more_log?

more_granted: "COMMA" granted_content more_granted?

data_type: "scroll"
         | "treasures"
         | "mirror"
         | "ocean"
         | "rose"

val: granted_content_2
   | IDENTIFIER granted_id_ext?
   | "SUB" IDENTIFIER granted_id_ext?
   | input

val1: granted_content_2
    | IDENTIFIER val1_ext?

val1_ext: id_ext? val1_id_ext?
        | unary_operator

val1_id_ext: granted_other_id_ext?
           | assignment_operator assignment_operand

conversion_func: "torose"
               | "totreasures"
               | "toocean"
               | "tomirror"

conversion_value: lit4
                | IDENTIFIER id_ext?

index: "LSQR" array_size "RSQR" column1?

column1: "LSQR" array_size "RSQR"

input: "wish" "LPAREN" SCROLL_LIT "RPAREN"

lit1: SCROLL_LIT
     | ROSE_LIT

lit2: MIRROR_LIT

lit3: bool_lit
    | int_lit
    | float_lit

lit4: lit1
     | lit2
     | lit3

bool_lit: "1" | "0"
int_lit: TREASURES_LIT
float_lit: OCEAN_LIT

func_call: "LPAREN" args? "RPAREN"

args: args_val args_more?

args_val: IDENTIFIER id_ext?
        | lit4

args_more: "COMMA" args_val args_more?

array_element: index

id_ext: func_call
      | array_element

array_size: IDENTIFIER
          | POS_TREASURES_LIT
          
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
POS_TREASURES_LIT: /0|[1-9][0-9]*/

// Float literal (ocean_lit)
OCEAN_LIT: /[0-9]+\.[0-9]+/

// Identifier: starts with a capital letter, then letters/digits/underscores
IDENTIFIER: /[A-Z][A-Za-z0-9_]*/

%import common.WS
%import common.ESCAPED_STRING
%ignore WS
%ignore COMMENTS
"""


class RoyalScriptParser:
    def __init__(self, reconstructed_code, token_positions):
        self.reconstructed_code = reconstructed_code
        
        # Map token types to their actual symbols
        self.token_map = {
            "ADD": "+",
            "SUB": "-",
            "MUL": "*",
            "DIV": "/",
            "MOD": "%",
            "EQUAL": "=",
            "COMMA": ",",
            "LPAREN": "(",
            "RPAREN": ")",
            "LCUR": "{",
            "RCUR": "}",
            "LSQR": "[",
            "RSQR": "]",
            "ADD_EQUAL": "+=",
            "SUB_EQUAL": "-=",
            "MUL_EQUAL": "*=",
            "DIV_EQUAL": "/=",
            "MOD_EQUAL": "%=",
            "EQUAL_EQUAL": "==",
            "NOT_EQUAL": "!=",
            "LESS": "<",
            "GREATER": ">",
            "LESS_EQUAL": "<=",
            "GREATER_EQUAL": ">=",
            "AND": "&&",
            "OR": "||",
            "NOT": "!",
            "TILDE": "~",
            "DEC": "++",
            "INC" : "--"
        }

    def _map_token(self, token):
        return self.token_map.get(token, token)

    def _extract_token_at_column(self, line_content, col):
        # Extract the word/token at the error position (space-delimited)
        word_start = col
        while word_start > 0 and not line_content[word_start-1].isspace():
            word_start -= 1
        word_end = col
        while word_end < len(line_content) and not line_content[word_end].isspace():
            word_end += 1
        return line_content[word_start:word_end]

    def _extract_anon_values(self, parser):
        # Extract the actual values of anonymous tokens
        anon_values = {}
        
        # First try accessing terminals directly
        if hasattr(parser, 'terminals'):
            for terminal in parser.terminals:
                if terminal.name.startswith('__ANON_'):
                    # For string literals, the pattern will contain the actual value
                    if hasattr(terminal, 'pattern'):
                        if isinstance(terminal.pattern, str):
                            # Strip quotes for string literals
                            if terminal.pattern.startswith('"') and terminal.pattern.endswith('"'):
                                value = terminal.pattern[1:-1]
                            else:
                                value = terminal.pattern
                            anon_values[terminal.name] = value
        
        # If that didn't work, try to extract directly from the grammar
        if not anon_values and hasattr(parser, 'lexer'):
            if hasattr(parser.lexer, 'terminals'):
                term_defs = parser.lexer.terminals
                for name, (priority, re_pattern, *_) in term_defs.items():
                    if name.startswith('__ANON_'):
                        # Try to extract the value from the pattern
                        try:
                            # For literal strings in the grammar
                            if re_pattern.startswith('"') and re_pattern.endswith('"'):
                                value = re_pattern[1:-1]
                            # For fixed tokens
                            elif not re_pattern.startswith('(') and not re_pattern.startswith('['):
                                value = re_pattern
                            else:
                                value = re_pattern
                            anon_values[name] = value
                        except:
                            pass

        # Direct mapping for common ANON tokens based on grammar inspection
        # These are manually identified from the grammar
        if '__ANON_0' not in anon_values:
            anon_values['__ANON_0'] = 'mirror_lit'
        if '__ANON_1' not in anon_values:
            anon_values['__ANON_1'] = '0'
        if '__ANON_2' not in anon_values:
            anon_values['__ANON_2'] = '1'
        
        print("Anonymous token values:", anon_values)  # Debug print
        return anon_values

    def parse(self):
        parser = Lark(castle_grammar, parser="lalr")
        anon_values = self._extract_anon_values(parser)
        
        try:
            tree = parser.parse(self.reconstructed_code)
            return tree, None
        except UnexpectedToken as e:
            # Extract the full token at the error position
            line_content = self.reconstructed_code.split('\n')[e.line-1] if e.line > 0 else self.reconstructed_code
            col = e.column - 1 if e.column > 0 else 0
            actual_token = self._extract_token_at_column(line_content, col)
            # Map to symbol if possible
            mapped_actual = self._map_token(actual_token)
            actual_token = mapped_actual if mapped_actual != actual_token else actual_token

            line = e.line
            # Map expected token types to their symbols
            expected_values = []
            for token_type in sorted(e.expected):
                if token_type.startswith('__ANON_'):
                    # Use the actual value of the anonymous token if available
                    if token_type in anon_values:
                        expected_values.append(anon_values[token_type])
                    else:
                        expected_values.append(token_type)
                elif token_type.startswith('"') and token_type.endswith('"'):
                    expected_values.append(token_type[1:-1])
                elif token_type in self.token_map:
                    expected_values.append(self.token_map[token_type])
                else:
                    expected_values.append(token_type)
            expected = ', '.join(expected_values)
            msg = (f'Syntax Error: Invalid input "{actual_token}" at Line {line}. '
                   f'Expected one of [{expected}].')
            return None, msg

        except UnexpectedCharacters as e:
            line_content = self.reconstructed_code.split('\n')[e.line-1] if e.line > 0 else self.reconstructed_code
            col = e.column - 1 if e.column > 0 else 0
            actual_token = self._extract_token_at_column(line_content, col)
            if not actual_token:
                actual_token = e.char
            mapped_actual = self._map_token(actual_token)
            actual_token = mapped_actual if mapped_actual != actual_token else actual_token

            line = e.line
            expected_values = []
            if e.allowed:
                for token_type in sorted(e.allowed):
                    if token_type.startswith('__ANON_'):
                        # Use the actual value of the anonymous token if available
                        if token_type in anon_values:
                            expected_values.append(anon_values[token_type])
                        else:
                            expected_values.append(token_type)
                    elif token_type.startswith('"') and token_type.endswith('"'):
                        expected_values.append(token_type[1:-1])
                    elif token_type in self.token_map:
                        expected_values.append(self.token_map[token_type])
                    else:
                        expected_values.append(token_type)
                expected = ', '.join(expected_values)
            else:
                expected = "valid token"
            msg = (f'Syntax Error: Invalid input "{actual_token}" at Line {line}. '
                   f'Expected one of [{expected}].')
            return None, msg

        except UnexpectedInput as e:
            if hasattr(e, 'line') and hasattr(e, 'column'):
                try:
                    line_content = self.reconstructed_code.split('\n')[e.line-1]
                    col = e.column - 1 if e.column > 0 else 0
                    actual_token = self._extract_token_at_column(line_content, col)
                    mapped_actual = self._map_token(actual_token)
                    actual_token = mapped_actual if mapped_actual != actual_token else actual_token
                    msg = f"Syntax Error: Invalid input \"{actual_token}\" at Line {e.line}, Column {e.column}."
                except:
                    msg = f"Syntax Error at Line {e.line}, Column {e.column}."
            else:
                msg = "Syntax Error: Invalid input."
            return None, msg