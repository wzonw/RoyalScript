from lexer import RoyalScriptLexer
from lexer import Token
from RS_RegDef  import Delims
from RS_RegDef  import RegDef

class RoyalScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens  # Tokens from the lexer, stored as a 2D list
        self.line_num = 0  # Line number for parsing

        # Define the predict sets for different non-terminals
        self.predict_sets = {
            'Expression': {'ID', 'NUMBER'},  # Example tokens that can start an expression
            'Term': {'ID', 'NUMBER'},
            'Factor': {'ID', 'NUMBER'}
        }

    def current_token(self):
        """Get the current token in the current line"""
        if self.line_num < len(self.tokens):
            return self.tokens[self.line_num]  # Return all tokens in the current line
        return None

    def match(self, token_type, token_list):
        """Check if the current token matches the expected token type"""
        if token_list:
            current_token = token_list[0]  # Check the first token in the line
            if current_token[0] == token_type:  # Token format is (type, value)
                return True
        return False

    def advance(self, token_list):
        """Advance the token list by removing the first token"""
        if token_list:
            return token_list[1:]  # Remove the first token
        return token_list

    def parse_expression(self, token_list):
        """Parse an expression (example: ID PLUS NUMBER)"""
        if self.match('ID', token_list):
            token_list = self.advance(token_list)
            if self.match('PLUS', token_list):
                token_list = self.advance(token_list)
                if self.match('NUMBER', token_list):
                    return True  # Expression is valid
        return False  # Expression is not valid

    def parse(self):
        """Parse the entire code, line by line"""
        while self.line_num < len(self.tokens):
            token_list = self.tokens[self.line_num]  # Get tokens for the current line

            print(f"Parsing Line {self.line_num + 1}: {token_list}")

            # Try to parse the expression in the current line
            if self.parse_expression(token_list):
                print(f"Line {self.line_num + 1}: Expression is valid.")
            else:
                print(f"Line {self.line_num + 1}: Syntax Error!")

            # Move to the next line
            self.line_num += 1



