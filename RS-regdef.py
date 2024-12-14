
RegDef = {
    # Single digits
    'num': {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
    'zero': {'0'},
    'number': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
    
    # Period
    'period': {'.'},

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
    'arithmetic_operator': {'+', '-', '*', '/', '%'},

    # Assignemnt operators
    'assignment_operator': {'+=', '-=', '*=', '/=', '%='},

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
    'single_quote': {"'"}
}


DELIMS = {
    'end': {'~', ' ', '\n'},
    
    # Data types (e.g., for parsing types like int, float, etc.)
    'data_type': {'[', ',', '(', ')', ' ', '~', '=', '-', '\n'},
    
    # Dono (could be a special keyword or identifier in your language)
    'dono': {'~', ',', '(', ')', ' ', '=', '\n'},
    
    # Class-related delimiters
    'cwass': {'~', '[', '.', ',', '(', ')', ' ', '=', '\n'},
    
    # Boolean operators
    'bool': {'|', '&', ']', ',', ' ', '}', ')', '~', '\n'},
    
    # Conditional statements (e.g., if, while, etc.)
    'conditional': {'[', '(', ' ', '\n'},
    
    # IO operations (possibly input/output operations)
    'io': {'(', ' ', '\n'},
    
    # Main function delimiters
    'mainuwu': {'-', ' ', '\n'},
    
    # Integer/Float delimiters (e.g., for parsing numeric expressions)
    'int_float': {',', ' ', *RegDef['general_operator'], ')', '}', ']', '~', '!', r'&', '|', '>', '<', '=', '\n'},
    
    # String delimiters
    'string': {' ', '|', ')', ',', '&', '}', '[', ']', '~', '!', '=', '\n'},
    
    # Assignment delimiters (e.g., variable assignments)
    'assign_delim': {*RegDef['alpha'], *RegDef['number'], '{', ' ', '-', '(', '"', '\n'},
    
    # General operator delimiters (e.g., for mathematical and logical operators)
    'operator_delim': {*RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '{', '\n'},
    
    # Logical operator delimiters (e.g., AND, OR, etc.)
    'logical_delim': {'"', *RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '{', '\n'},
    
    # String parts (for string manipulations or parsing)
    'string_parts': {'"', *RegDef['alpha'], *RegDef['number'], ' ', '-', '(', '|', '\n', '&'},
    
    # Open brace (used for block definitions or scopes)
    'open_brace': {'{', '}', '(', *RegDef['number'], ' ', '"', *RegDef['alpha'], '\n', '>', '-'},
    
    # Close brace (used for block terminations or scopes)
    'close_brace': {'{', '}', '.', '~', ' ', ',', ')', '\n', '>', '&', *RegDef['general_operator'], '!', '|'},
    
    # Parentheses delimiters (for function calls, expressions, etc.)
    'open_parenthesis': {'{', *RegDef['number'], *RegDef['alpha'], ' ', '-', '\n', '>', '(', ')', '"'},
    'close_parenthesis': {'{', ' ', *RegDef['general_operator'], '!', '&', '|', '\n', '~', '>', '.', ',', ')', '(', '[', ']', '}'},

    # Bracket delimiters (typically for arrays or lists)
    'open_bracket': {']', *RegDef['number'], '-', *RegDef['alpha'], '(', ' ', '\n'},
    'double_open_bracket': {' ', '\n', *RegDef['alpha'], '>'},
    'close_bracket': {'\n', '(', ' ', '~', ',', ')', '[', ']', '}', *RegDef['general_operator'], '!', r'&', '|', '.', '\n'},
    'double_close_bracket': {']', ' ', '\n', *RegDef['alpha'], '>'},
    
    # Unary operation delimiters (e.g., negation or logical NOT)
    'unary': {'|', '~', ')', *RegDef['general_operator'], '!', ' ', '\n'},
    
    # Concatenation delimiters (likely for string concatenation)
    'concat': {' ', '"', *RegDef['alpha'], *RegDef['number'], '(', '{', '\n'},
    
    # Line terminators
    'line': {'\n', ' ', *RegDef['alpha'], ']'},
    
    # Comma delimiter (used for separating elements in a list, parameters, etc.)
    'comma': {*RegDef['alpha'], ' ', *RegDef['number'], '"', '-', '\n', '>', '{'},
    
    # Dot operator delimiter (e.g., object member access)
    'dot_op': {*RegDef['alpha'], '[', '(', '\n'},
    
    # "Nuww" might be a typo or special delimiter for null values
    'nuww': {' ', '~', ')', '}', ',', '=', '\n', '!', '|', '&'},
    
    # Whitespace delimiters (spaces and newlines)
    'whitespace': {' ', '\n'},
    
    # Single-line comment delimiter
    'single_line_comment': {'\n'},
    
    # General case for any other delimiter
    'all': {None}
}
