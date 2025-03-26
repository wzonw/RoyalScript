from lexer import RoyalScriptLexer
from lexer import Token
from RS_RegDef  import Delims
from RS_RegDef  import RegDef


class RoyalScriptParser:
    def __init__(self, tokens, syntax):
        """Initialize with tokens and syntax rules."""
        self.tokens = tokens  # List of token lists (nested format)
        self.syntax = syntax  # Grammar rules
        self.current_line = 0  # Index for current line of tokens
        self.current_index = 0  # Index for the token in the current line

    def current_token(self):
        """Return the current token in the current line."""
        if self.current_line < len(self.tokens):
            if self.current_index < len(self.tokens[self.current_line]):
                return self.tokens[self.current_line][self.current_index]
        return None

    def previous_token(self):
        """Return the previous token in the current line."""
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
        token = self.current_token()
        prev_token = self.previous_token()

        if token is None:
            return False

        # Check if current token matches a direct key in the syntax
        if token in self.syntax:
            expected_tokens = self.syntax[token]
            return expected_tokens

        # Check if the current token and previous token match a tuple key (like ('~', 'crown'))
        if prev_token is not None:
            for key, value in self.syntax.items():
                if isinstance(key, tuple) and key[0] == prev_token and key[1] == token:
                    return value

        # Check if current token is part of a tuple key (like ('=', 'identifier'))
        for key, value in self.syntax.items():
            if isinstance(key, tuple) and key[0] == token:
                return value

        return None
    
    def parse(self):
        """Parse the tokens according to the syntax."""
        while self.current_token() is not None:
            token = self.current_token()
            print(f"Current token: {token}, Previous token: {self.previous_token()}")

            # Check if the token matches any rule
            result = self.match()
            if result:
                print(f"Matching rule: {token} -> {result}")
                # Handle rule based on result
                # If the rule indicates a list of tokens, we advance to the next token
                self.advance()
            else:
                print(f"No matching rule for token: {token}")
                break
    
    #syntax:
    syntax = {

    #start 
        'program': ['crown'],
        'crown' : ['~'],
        ('~', 'crown'): ['treasures', 'ocean', 'scroll', 'rose', 'mirror', 'const', 'spell', 'castle'],

    #variable declaration
        #<const> <data_type> id_lit
        'const': ['treasures', 'ocean', 'scroll', 'rose', 'mirror'],
        ('treasures', 'const'): ['identifier'],
        ('ocean', 'const'): ['identifier'],
        ('scroll', 'const'): ['identifier'],
        ('rose', 'const'): ['identifier'],

        #<data_type> id_lit
        'treasures': ['identifier'],
        'ocean': ['identifier'],
        'scroll': ['identifier'],
        'rose': ['identifier'],

        # <vardec_def>
        ('identifier', 'treasures') : ['=', ',', '~', '['],
        ('identifier', 'ocean') : ['=', ',', '~', '['],
        ('identifier', 'scroll') : ['=', ',', '~', '['],
        ('identifier', 'rose') : ['=', ',', '~', '['],

        #<intialization> -> = <val>

        ('=', 'identifier'): ['scroll_lit', 'treasures_lit', 'mirror_lit', 'ocean_lit', 'rose_lit', 'id_lit', 'phantom', 
                            'toscroll', 'wish', 'torose', 'totreasures', 'toocean', '!', 1, 0, '(', 'wish'],

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
        ('{', '='): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit', '{'],
        ('scroll_lit', '{'): [',', '}'],
        ('rose_lit', '{'): [',', '}'],
        ('treasures_lit', '{'): [',', '}'],
        ('ocean_lit', '{'): [',', '}'],
        ('mirror_lit', '{'): [',', '}'],    
        #multiple element
        (',', 'scroll_lit'): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
        (',', 'rose_lit'): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
        (',', 'treasures_lit'): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
        (',', 'ocean_lit'): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
        (',', 'mirror_lit'): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],
        #single array
        ('}', 'scroll_lit'): ['~'], #[',', '~']
        ('}', 'rose_lit'): ['~'],
        ('}', 'treasures_lit'): ['~'],
        ('}', 'ocean_lit'): ['~'],
        ('}', 'mirror_lit'): ['~'],
        
        #2d array
        (',', '}'): ['{'],
        ('{', ','): ['scroll_lit', 'rose_lit', 'treasures_lit', 'ocean_lit', 'mirror_lit'],

        ('~', '}'): [], #add tokens

        #<vardec_more> -> , id_lit 
        (',', 'identifier'): ['identifier'],

        #<initialization> and <vardec_more> == null
        ('~', 'identifier'): [], #add tokens
        
        #user-defined function

        #main function


    }