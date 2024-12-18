
RegDef = {
    # Single digits
    'num': {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
    'zero': {'0'},
    'number': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
    
    # Period
    'period': {'.'},
    

    'general_operator': {'+', '-', '*', '/', '%', '>', '<', '='},

    # Alphabet letters
    'alpha_small': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
    'alpha_big': {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'},
    'alpha': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    },
    
    # Alphanumeric characters
    'alphanum': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    },

    # Special characters (including punctuation)
    'special_char': {
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '[', ']', '{', '}', '\\', '|', ':', ';', "'", '”', ',', '<', '>', '.', '/', '?'
    },
    
    # Arithmetic operators
    'arithmetic_op': {'+', '-', '*', '/', '%'},

    # Assignemnt operators
    'assignment_op': {'+=', '-=', '*=', '/=', '%='},

    'equal' : {'='},
    
    # Logical operators
    'logical_op': {'&&', '!', '||'},
    
    # Unary operators
    'unary_op': {'++', '--'},
    
    # Relational operators
    'relational_op': {'!=', '==', '>', '<', '>=', '<='},

    # Escape sequences
    'escape_seq': {'\\n', '\\t', '\\', '\\"'},
    
    # Comment symbols
    'single_line': {'?'},
    'multiline_open': {'?*'},
    'multiline_close': {'*?'},
    
    # Period, for floating point numbers
    'period': {'.'},

    # quote
    'double_quote': {'"'},
    'single_quote': {"'"},
    'whitespace': {' ', '\t', '\n'},
    'ascii': { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '[', ']', '{', '}', '\\', '|', ':', ';', "'", '”', ',', '<', '>', '.', '/', '?'
    }
}


Delims = {
    'gate_delim': {'~', ' '},    #'end': {'~', ' ', '\n'},
    
    # Data types (e.g., for parsing types like int, float, etc.)
    'data_type': {' '},
    
    'other_assignment_operator_delim' : {'(', *RegDef['alphanum']},
    # Dono (could be a special keyword or identifier in your language)
    'arithmetic_operator_delim':{'(', ')', ' ', *RegDef['alphanum']},  #'dono': {'~', ',', '(', ')', ' ', '=', '\n'},

    'escape_sequence_delim': {'”', *RegDef['alphanum'], 'escape_sequence_symbol', ' '},
    
    # Class-related delimiters
    'plus_delim' : {'(', *RegDef['alphanum'], '"', ' '},    #'cwass': {'~', '[', '.', ',', '(', ')', ' ', '=', '\n'},
    
    # Boolean operators
    'logical_operator_delim': {'(', *RegDef['alphanum'], ' '}, # same with other assignmen operator  #'bool': {'|', '&', ']', ',', ' ', '}', ')', '~', '\n'},
    
    # Conditional statements (e.g., if, while, etc.)
    'not_logical_delim': {'(', '"', "'",  *RegDef['alphanum']},    #'conditional': {'[', '(', ' ', '\n'},
    
    'witch_delim': {'{', ' ' },

    'equal_delim':{'‘', '“', '( ', '[', *RegDef['alphanum'], ' '}, 

    # IO operations (possibly input/output operations)
    'io': {'(', ' ', '\n'},
    
    # Main function delimiters
    'unary_operator_delim': {'~', ')', *RegDef['alphanum']},    #'mainuwu': {'-', ' ', '\n'},
    
    # Integer/Float delimiters (e.g., for parsing numeric expressions)
    'relational_operator_delim': {'(', '“', '‘', *RegDef['alphanum'], ' '},     #'int_float': {',', ' ', *RegDef['general_operator'], ')', '}', ']', '~', '!', r'&', '|', '>', '<', '=', '\n'},
    
    # String delimiters
        ###### 'string': {' ', '|', ')', ',', '&', '}', '[', ']', '~', '!', '=', '\n'},
    
    # Assignment delimiters (e.g., variable assignments)
    'open_parentheses_delim':  {*RegDef['unary_op'], *RegDef['alphanum'], '"', ' ',')'},   #'assign_delim': {*RegDef['alpha'], *RegDef['number'], '{', ' ', '-', '(', '"', '\n'},
    
    # General operator delimiters (e.g., for mathematical and logical operators)
    'close_parentheses_delim' : {*RegDef['arithmetic_op'], *RegDef['logical_op'], *RegDef['relational_op'],'(', '{',  '~', ' '},    #'operator_delim': {*RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '{', '\n'},
    
    # Logical operator delimiters (e.g., AND, OR, etc.)
    'open_curly_bracket_delim' : {'(',  *RegDef['unary_op'], *RegDef['alphanum'], '\n', ' '},    #'logical_delim': {'"', *RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '{', '\n'},
    
    # String parts (for string manipulations or parsing)
    'close_curly_bracket_delim' : { *RegDef['alpha_small'], ' '},    #'string_parts': {'"', *RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '|', '\n', '&'},
    
    # Open brace (used for block definitions or scopes)
    'open_square_bracket_delim' : {'‘','”', ']', *RegDef['number'], ' '},   #'open_brace': {'{', '}', '(', *RegDef['number'], ' ', '"', *RegDef['alpha'], '\n', '>', '-'},
    
    # Close brace (used for block terminations or scopes)
    'close_square_bracket_delim' : {'~', '[', '=', ' '},    #'close_brace': {'{', '}', '.', '~', ' ', ',', ')', '\n', '>', '&', *RegDef['general_operator'], '!', '|'},
    
    # Unary operation delimiters (e.g., negation or logical NOT)
    'comma_delim' : {*RegDef['alphanum'], '-' , '‘' , '“' , ' '},    #'unary': {'|', '~', ')', *RegDef['general_operator'], '!', ' ', '\n'},
    
    # Concatenation delimiters (likely for string concatenation)
    'id_delim' : {'(', ')', '~', ' ', '=' , *RegDef['unary_op'], *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['relational_op']},  #'concat': {' ', '"', *RegDef['alpha'], *RegDef['number'], '(', '{', '\n'},
    
    # Line terminators
    'book_delim' : {'~',')', '+', ' '},     #'line': {'\n', ' ', *RegDef['alpha'], ']'},
    
    # Comma delimiter (used for separating elements in a list, parameters, etc.)
    'number_delim' : {')','}',']','~', *RegDef['arithmetic_op'], *RegDef['assignment_op'], *RegDef['logical_op'], *RegDef['relational_op'], *RegDef['unary_op'], ' '},    #'comma': {*RegDef['alpha'], ' ', *RegDef['number'], '"', '-', '\n', '>', '{'},
    
    # Dot operator delimiter (e.g., object member access)
    'genie_delim' : {'(', ' '},    #'dot_op': {*RegDef['alpha'], '[', '(', '\n'},
    
    # "Null" might be a typo or special delimiter for null values
    'gate_delim' : {' ', '~'},    #'null': {' ', '~', ')', '}', ',', '=', '\n', '!', '|', '&'},
    
    # Whitespace delimiters (spaces and newlines)
    'whitespace': {' ', '\n'},

    'terminator_delim' : {*RegDef['whitespace'], '?', '}', *RegDef['alpha']},
    
    # Single-line comment delimiterA
    #'single_line_comment': {'\n'},
    
    # General case for any other delimiter
    #'all': {None}

    'multi-comment_delim' : {*RegDef['ascii'], *RegDef['whitespace']}
}

