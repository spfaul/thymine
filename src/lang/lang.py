from pprint import pprint
from .token import Token, TokenType
from .transpiler import ThymineToHTMLTranspiler
import re

class ThymineInterpreter:
    def __init__(self):
        self.tpiler = ThymineToHTMLTranspiler()

    def feed(self, text: str, output_path: str, template: str):
        """ Parse thymine-lang input """
        tokens = ThymineInterpreter.tokenize(text)
        # pprint(tokens)

        html_str = self.tpiler.tokens_to_html(tokens, template)
        with open(output_path, 'w') as file:
            file.write(html_str)

    def feed_file(self, source_path: str, output_path: str, template_path: str):
        """ Parse a thymine-lang file given its relative/absolute path """
        with open(source_path, 'r') as source:
            with open(template_path, 'r') as template:
                self.feed(source.read(), output_path, template.read())

    @staticmethod
    def tokenize(text: str):
        tokens: list[list[Token]] = []
        for line in text.split("\n"):
            line_toks: list[Token] = []

            # Find tokens at the start of the line (no iteration needed)
            if line.strip() == "-":  # Metadata Tags
                line_toks.append(Token(TokenType.MetadataTag, "-"))
                tokens.append(line_toks)
                continue
            if line.strip().startswith(">"): # Quote Blocks
                line_toks.append(Token(TokenType.QuoteBlock, ">"))
                line = line.replace(">", "", 1)

            header = re.search("#+ ", line)  # Markdown-Style Headers
            if header != None and header.start() == 0:
                line_toks.append(Token(TokenType.Header, header.group(0)))
                line = line.replace(header.group(0), "", 1)

            tok_value: str = ""
            tok_type: TokenType = TokenType.StringText
            old_tok_type: TokenType = None

            for idx, char in enumerate(line):
                tok_value += char

                if char == ":": # 
                    line_toks.append(Token(tok_type, tok_value[:len(tok_value)-1]))
                    tok_type = TokenType.MetadataAssignment
                    line_toks.append(Token(tok_type, tok_value[-1]))
                    tok_value = ""                    
                else:
                    tok_type = TokenType.StringText

                if idx == len(line)-1 and tok_type == TokenType.StringText:
                    line_toks.append(Token(tok_type, tok_value))

            tokens.append(line_toks)

        return tokens


