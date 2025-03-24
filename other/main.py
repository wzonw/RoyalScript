# main.py

from lexer2 import RoyalScriptLexer
from token_wrapper import LexerWrapper
from parser import parser

def main():
    # Replace this with your RoyalScript source code.
    code = "123 + 456\n789 - 10"
    
    # Initialize and run your custom lexer.
    lexer = RoyalScriptLexer(code)
    token_lines = lexer.get_tokens()  # token_lines is a 2D list of tokens
    print("Tokens (by line):")
    for line in token_lines:
        print(line)
    
    # Wrap the nested token list for PLY.
    lexer_wrapper = LexerWrapper(token_lines)
    
    # Parse the token stream using PLY.
    result = parser.parse(lexer=lexer_wrapper)
    print("Parse result:", result)

if __name__ == "__main__":
    main()
