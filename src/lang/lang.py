from pprint import pprint
from .token import Token, TokenType
from .transpiler import ThymineToHTMLTranspiler
import re
from typing import *

class ThymineInterpreter:
    def __init__(self):
        self.tpiler = ThymineToHTMLTranspiler()

    def feed(self, text: str, output_path: str, template: str):
        """ Parse thymine-lang input """
        tokens = ThymineInterpreter.tokenize(text)

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
        context: Union[Token, None] = None

        for line in text.split("\n"):
            line_toks: list[Token] = []

            # Find tokens at the start of the line (no iteration needed)
            if line.strip() == "-":  # Metadata Tags
                tmp_tok: Token = Token(TokenType.MetadataTag, "-")
                if context and context.type == TokenType.MetadataTag:
                    context = None
                else:
                    context = tmp_tok
                tokens.append([tmp_tok])
                continue

            if line.strip().startswith(">") and not context: # Quote Blocks
                line_toks.append(Token(TokenType.QuoteBlock, ">"))
                line = line.replace(">", "", 1)

            header = re.search("#+ ", line)  # Headers
            if header != None and header.start() == 0 and not context:
                line_toks.append(Token(TokenType.Header, header.group(0)))
                line = line.replace(header.group(0), "", 1)

            if line.strip().startswith("-"):
                line_toks.append(Token(TokenType.BulletPoint, "-"))
                line = line.replace("-", "", 1)

            tok = Token(TokenType.StringText, "")
            for idx, char in enumerate(line):
                tok.value += char

                if char == ":" and context and context.type == TokenType.MetadataTag:
                    tok.value = tok.value[:-1]
                    line_toks.append(tok)
                    line_toks.append(Token(TokenType.MetadataAssignment, ":"))
                    tok = Token(TokenType.StringText, "")
                # elif char == "^":
                #     occur_idxs = [idx for idx, c in enumerate(tok.value) if char == "^"] # Bold Text
                #     if occur_idxs > 1:
                #         decorated_text: str = line[idx : occur_idxs[-1] - 1]
                #         line_toks += ThymineInterpreter.tokenize_decorated_text(decorated_text)

                if idx == len(line)-1 and tok.type == TokenType.StringText:
                    line_toks.append(tok)

            tokens.append(line_toks)

        return tokens



