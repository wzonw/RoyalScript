# token_wrapper.py

class LexerWrapper:
    def __init__(self, tokens_by_line):
        self.tokens_by_line = tokens_by_line  # Your 2D list of tokens
        self.line_index = 0
        self.token_index = 0

    def token(self):
        # Iterate through each line's token list until a token is found.
        while self.line_index < len(self.tokens_by_line):
            if self.token_index < len(self.tokens_by_line[self.line_index]):
                tok = self.tokens_by_line[self.line_index][self.token_index]
                self.token_index += 1
                return tok
            else:
                self.line_index += 1
                self.token_index = 0
        return None  # No more tokens
