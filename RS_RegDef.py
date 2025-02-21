
RegDef = {
    'alpha': {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    },
    'alpha_big': {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    },
    'alpha_small': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    },
    'alphanum': {
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    },
    'arithmetic_op': {
        '%', '*', '+', '-', '/'
    },
    'ascii': {
        '!', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=',
        '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
        'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
        'Z', '[', '\\', ']', '^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', '{', '|', '}', '”'
    },
    'assignment_op': {
        '%=', '*=', '+=', '-=', '/='
    },
    'double_quote': {
        '"'
    },
    'equal': {
        '='
    },
    'escape_seq': {
        '\\\\', '\\"', '\\n', '\\t'
    },
    'general_operator': {
        '%', '*', '+', '-', '/', '<', '=', '>'
    },
    'logical_op': {
        '!', '&&', '||'
    },
    'multiline_close': {
        '*?'
    },
    'multiline_open': {
        '?*'
    },
    # 'num': {
    #     '1', '2', '3', '4', '5', '6', '7', '8', '9'
    # },
    'num': ('1', '2', '3', '4', '5', '6', '7', '8', '9'),
    'number': {
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    },
    'period': {
        '.'
    },
    'relational_op': {
        '!=', '<', '<=', '==', '>', '>='
    },
    'single_line': {
        '?'
    },
    'single_quote': {
        "'"
    },
    'special_char': {
        '!', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
        ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '{', '|', '}', '”'
    },
    'unary_op': {
        '++', '--'
    },
    'whitespace': {
        '\t', '\n', ' '
    },
    'zero': {
        '0'
    }
}



Delims = {
 
    # 'gate_delim': {'~', ' '},    

    # 'other_assignment_operator_delim' : {'(', *RegDef['number'], *RegDef['alpha_big'],  ' '},
    
    # 'arithmetic_operator_delim':{'(', ' ', *RegDef['number'], *RegDef['alpha_big']},  

    # 'escape_sequence_delim': { '"', *RegDef['ascii'], *RegDef['escape_seq'], ' ', '"'},
    
    # 'plus_delim' : {'(', *RegDef['alphanum'], '"', "'", ' '},   

    # 'minus_delim' : {'(', ' ', *RegDef['alpha_big']}, 

    # 'logical_operator_delim': {'(', *RegDef['alphanum'], ' '}, 

    # 'not_logical_delim': {'(', '"', "'",  *RegDef['alphanum'], ' '},    
    
    # 'witch_delim': {'{', ' ' },

    # 'equal_delim':{'‘', '“', '( ', '[', *RegDef['alphanum'], ' '}, 

    # 'mirror-lit_delim': {' ', '~', ')'},

    # 'unary_operator_delim': {'~', ')', ' '},    

    # 'relational_operator_delim': {'(', '“', '‘', *RegDef['alphanum'], ' '},     

    # 'open_parentheses_delim':  {*RegDef['alphanum'], ' ', ')', '"', "!"},   

    # 'close_parentheses_delim' : {*RegDef['arithmetic_op'], *RegDef['logical_op'], *RegDef['relational_op'], '{',  '~', ' ', '\n', ')'},

    # 'open_curly_bracket_delim' : {'(',  *RegDef['alphanum'], *RegDef['whitespace'], '{', '-'},    

    # 'close_curly_bracket_delim' : { *RegDef['alphanum'], ' ', "'", '"', *RegDef['whitespace'], ',', '~', '}'},    

    # 'open_square_bracket_delim' : {'‘','”', ']', *RegDef['number'], ' ',  *RegDef['alpha_big']},  

    # 'close_square_bracket_delim' : {'~', '[', '=', ' ', ','},    

    # 'comma_delim' : {*RegDef['alphanum'], '-' , '‘' , '“' , '[',  ' ' ,'}', *RegDef['whitespace']},   

    # 'id_delim' : {'[', '(', ')', '~', ' ', '=' , ']', ',', *RegDef['unary_op'], *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['relational_op']}, 
    
    # 'book_delim' : {'~',')', '+', ' ', ',', },     
    
    # 'number_delim' : {')','}',']','~', '=', *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['logical_op'], *RegDef['relational_op'], *RegDef['unary_op'], ' ', ','},    
    
    # 'genie_delim' : {'(', ' '},    

    # 'gate_delim' : {' ', '~'},    
    
    # 'terminator_delim' : {*RegDef['whitespace'], '?', '}', *RegDef['alpha']},
    
    # 'multi-comment_delim' : {*RegDef['ascii'], *RegDef['whitespace']}


    'arithmetic_operator_delim': {' ', '(', *RegDef['alpha_big'], *RegDef['number']},

    'book_delim': {' ', ')', '+', ',', '~'},

    'close_curly_bracket_delim': {'}', *RegDef['alphanum'], *RegDef['whitespace'], ',', '~'},

    'close_parentheses_delim': {' ', '\n', ')', '{', '~', *RegDef['arithmetic_op'], *RegDef['logical_op'], *RegDef['relational_op']},

    'close_square_bracket_delim': {' ', ',', '=', '[', '~', ')', *RegDef['arithmetic_op']},

    'comma_delim': {'-', '‘', '“', *RegDef['alphanum'], *RegDef['whitespace'], '{'},

    'escape_sequence_delim': {' ', '"', '"', *RegDef['ascii'], *RegDef['escape_seq']},

    'equal_delim': {' ', '(', '[', '‘', '“', *RegDef['alphanum'], '{'},

    'gate_delim': {' ', '~'},

    'genie_delim': {' ', '('},

    'id_delim': {' ', '(', ')', ',', '[', ']', '=', '~', *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['relational_op'], *RegDef['unary_op'], '&', '|'},

    'logical_operator_delim': {' ', '(', *RegDef['alphanum']},

    'mirror-lit_delim': {' ', ')', '~', ','},

    'minus_delim': {' ', '(', *RegDef['alpha_big']},

    'multi-comment_delim': {*RegDef['ascii'], *RegDef['whitespace']},

    'not_logical_delim': {' ', '"', "'", '(', *RegDef['alphanum']},

    'number_delim': {' ', ')', ',', '=', ']', '}', '~', *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['logical_op'], *RegDef['relational_op'], *RegDef['unary_op']},

    'open_curly_bracket_delim': {'{', *RegDef['alphanum'], *RegDef['whitespace'], '-', '('},

    'open_parentheses_delim': {' ', '!', '"', ')', *RegDef['alphanum']},

    'open_square_bracket_delim': {' ', '‘', '”', *RegDef['alpha_big'], *RegDef['number']},

    'other_assignment_operator_delim': {' ', '(', *RegDef['alpha_big'], *RegDef['number']},

    'plus_delim': {' ', '"', "'", '(', *RegDef['alphanum']},

    'relational_operator_delim': {' ', '(', '‘', '“', *RegDef['alphanum']},

    'terminator_delim': {' ', '?', '}', *RegDef['alpha'], *RegDef['whitespace']},

    'unary_operator_delim': {' ', ')', '~'},

    'witch_delim': {' ', '{'},

}


all_delims = set().union(*Delims.values())
