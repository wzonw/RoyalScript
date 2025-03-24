# parser.py

import ply.yacc as yacc

# The token names expected by the parser must match those from your lexer.
tokens = [
    'NUMBER',
    '+',
    '-',   # Define as needed (or include others)
    'EOF'
]

# Grammar rule: an expression can be a NUMBER.
def p_expression_number(p):
    "expression : NUMBER"
    p[0] = int(p[1])

# Grammar rule: an expression can be an addition of two expressions.
def p_expression_plus(p):
    "expression : expression '+' term"
    p[0] = p[1] + p[3]

# Grammar rule: a term can be a NUMBER.
def p_term_number(p):
    "term : NUMBER"
    p[0] = int(p[1])

# Grammar rule: an expression can also be a subtraction.
def p_expression_minus(p):
    "expression : expression '-' term"
    p[0] = p[1] - p[3]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} (value: {p.value}) at line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser.
parser = yacc.yacc()
