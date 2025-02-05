from lexer import RoyalScriptLexer, Token
from RS_RegDef import Delims, RegDef

class RoyalScriptParser:
    def __init__(self, tokens):
        """Initialize with tokens (list of token types) and syntax rules."""
        self.tokens = tokens  # List of token types for each line
        self.syntax = self.syntax  # Grammar rules
        self.current_line = 0  # Index for current line of tokens
        self.current_index = 0  # Index for the token in the current line
        self.parsing_result = ""  # Variable to store the result of parsing

    def current_token(self):
        """Return the current token type in the current line."""
        if self.current_line < len(self.tokens):
            if self.current_index < len(self.tokens[self.current_line]):
                return self.tokens[self.current_line][self.current_index]
        return None
    
    def previous_token(self):
        """Return the previous token type in the current line."""
        if self.current_index > 0:
            return self.tokens[self.current_line][self.current_index - 1]
        # If there is no previous token in the current line, check the previous line
        if self.current_line > 0 and len(self.tokens[self.current_line - 1]) > 0:
            return self.tokens[self.current_line - 1][-1]  # Last token of the previous line
        return None

    def advance(self):
        """Advance to the next token. If at the end of a line, move to the next line."""
        if self.current_index + 1 < len(self.tokens[self.current_line]):
            self.current_index += 1
        elif self.current_line + 1 < len(self.tokens):
            self.current_line += 1
            self.current_index = 0
        else:
            return None  # End of tokens

    def match(self):
        """Check if current and previous tokens match any syntax rule."""
        token = self.current_token()  # Just token types as strings
        prev_token = self.previous_token()  # Previous token type

        if token is None:
            return False

        # Direct match with token type in syntax rules
        if token in self.syntax:
            expected_tokens = self.syntax[token]
            return expected_tokens

        # Other matching logic for previous tokens or pairs
        if prev_token is not None:
            for key, value in self.syntax.items():
                if isinstance(key, tuple) and key[0] == prev_token and key[1] == token:
                    return value

        # Handle other syntax cases
        for key, value in self.syntax.items():
            if isinstance(key, tuple) and key[0] == token:
                return value

        return None

    def parse(self):
        """Parse the tokens according to the syntax."""
        while self.current_token() is not None:
            token = self.current_token()
            print(f"Current token: {token}, Previous token: {self.previous_token()}")
            
            # Check if we encounter EOF and stop parsing
            if token == 'EOF':
                self.parsing_result = "Parsing complete: EOF reached."
                print(self.parsing_result)
                break

            # Check if the token type matches any rule
            result = self.match()  # Just pass token directly here
            if result:
                print(f"Matching rule: {token} -> {result}")
                self.advance()
            else:
                self.parsing_result = f"No matching rule for token: {token}"
                print(self.parsing_result)
                break

    def get_parsing_result(self):
        """Return the result of the parsing."""
        return self.parsing_result


    
    #syntax:
    syntax = {

    #start 
        'program': ['crown'],
        'crown' : ['~'],
        ('~', 'crown'): ['treasures', 'ocean', 'scroll', 'rose', 'mirror', 'const', 'spell', 'castle','EOF'],
    #variable declaration
        #<const> <data_type> id_lit
        'const': ['treasures', 'ocean', 'scroll', 'rose', 'mirror'],
        ('treasures', 'const'): ['identifier'],
        ('ocean', 'const'): ['identifier'],
        ('scroll', 'const'): ['identifier'],
        ('rose', 'const'): ['identifier'],
        ('mirror', 'const'): ['identifier'],

        #<data_type> id_lit
        'treasures': ['identifier'],
        'ocean': ['identifier'],
        'scroll': ['identifier'],
        'rose': ['identifier'],
        'mirror': ['identifier'],

        # <vardec_def>
        ('identifier', 'treasures') : ['=', ',', '~', '[', ')'],
        ('identifier', 'ocean') : ['=', ',', '~', '[', ')'],
        ('identifier', 'scroll') : ['=', ',', '~', '[', ')'],
        ('identifier', 'rose') : ['=', ',', '~', '[', ')'],
        ('identifier', 'mirror') : ['=', ',', '~', '[', ')'],

        #<intialization> -> = <val>

        ('=', 'identifier'): ['scroll-lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'mirror-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'rose-lit', 'id_lit', 'phantom', 
                            'toscroll', 'wish', 'torose', 'totreasures', 'toocean', '!', 1, 0, '(', 'wish'],

        ('scroll-lit', '='): [',', '~'],
        ('rose-lit', '='): [',', '~'],
        ('neg-treasures-lit', '='): [',', '~'],
        ('pos-treasures-lit', '='): [',', '~'],
        ('mirror-lit', '='): [',', '~'],
        ('neg-ocean-lit', '='): [',', '~'],
        ('pos-ocean-lit', '='): [',', '~'],
        ('id-lit', '='): [',', '~'],
        ('phantom', '='): [',', '~'],


        # array declaration (single) -> [num] 
        ('[', 'identifier'): [RegDef['num']],
        (RegDef['num'], '['): [']'],
        # array declaration -> [num] -> <column>
        (']', RegDef['num']): ['[', '=', ',', '~'],
        ('[', ']'): [RegDef['num']],
        (RegDef['num'], '['): [']'],
        (']', RegDef['num']): ['=', ',' , '~'],

        #array with initialization 
        ('=', ']'): ['{'],
        ('{', '='): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit', '{'],
        ('scroll-lit', '{'): [',', '}'],
        ('rose_lit', '{'): [',', '}'],
        ('neg-treasures-lit', '{'): [',', '}'],
        ('pos-treasures-lit', '{'): [',', '}'],
        ('neg-ocean-lit' , '{'): [',', '}'],
        ('pos-ocean-lit', '{'): [',', '}'],
        ('mirror-lit', '{'): [',', '}'],   

        #multiple element
        (',', 'scroll-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'rose_lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'neg-treasures-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'pos-treasures-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'neg-ocean-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'pos-ocean-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],
        (',', 'mirror-lit'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],

        #single array
        ('}', 'scroll-lit'): ['~', '}', ','], 
        ('}', 'rose_lit'): ['~', '}', ','],
        ('}', 'neg-treasures-lit'): ['~', '}', ','],
        ('}', 'pos-treasures-lit'): ['~', '}', ','],
        ('}', 'neg-ocean-lit'): ['~', '}', ','],
        ('}', 'pos-ocean-lit'): ['~', '}', ','],
        ('}', 'mirror-lit'): ['~', '}', ','],
        
        #single array end 
        (',', '}'): ['{'],
        ('{', ','): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],

        ('~', '}'): [], #add tokens

        #more array
        (', ', '}'): ['{'],
        ('{', ','): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],

        #2d array start
        ('{', '{'): ['scroll-lit', 'rose_lit', 'neg-treasures-lit' , 'pos-treasures-lit', 'neg-ocean-lit' , 'pos-ocean-lit', 'mirror-lit'],

        #2d array end 
        ('}', '}'): ['~'],


        #<vardec_more> -> , id_lit 
        (',', 'identifier'): ['identifier'],

        #<initialization> and <vardec_more> == null
        ('~', 'identifier'): ['EOF'], #add tokens
        
        #user-defined function -> spell <return_type> id_lit(<param>){<body><ret_statement>}<user-defined-func>
        ('spell', '~'): ['chamber', 'treasures', 'ocean', 'scroll', 'rose', 'mirror'],
        ('chamber', 'spell'): ['id_lit'],
        ('treasures', 'spell'): ['id_lit'],
        ('ocean', 'spell'): ['id_lit'],
        ('scroll', 'spell'): ['id_lit'],
        ('rose', 'spell'): ['id_lit'],
        ('mirro', 'spell'): ['id_lit'],
        ('id_lit', 'chamber'): ['('],
        ('id_lit', 'treasures'): ['('],
        ('id_lit', 'ocean'): ['('],
        ('id_lit', 'scroll'): ['('],
        ('id_lit', 'rose'): ['('],
        ('id_lit', 'mirro'): ['('],
        ('(', 'id_lit'): ['treasures', 'ocean', 'scroll', 'rose', 'mirror'],
        ('treasures', '('): ['identifier'],
        ('ocean', '('): ['identifier'],
        ('scroll', '('): ['identifier'],
        ('rose', '('): ['identifier'],
        ('mirror', '('): ['identifier'],



        #main function

    }