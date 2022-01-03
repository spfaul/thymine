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
        pprint(tokens)

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

            # Empty Lines
            if line.strip() == "":
                tokens.append([Token(TokenType.LineBreak, "\n")])

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

            elif line.strip().startswith("o"): # Bullet points
                whitespace_len: int = ThymineInterpreter._get_ws_level(line.split("o")[0])
                tok: Token = Token(TokenType.BulletPoint, "o", level=whitespace_len + 1)
                line_toks.append(tok)
                line = line.lstrip().replace("o", "", 1)

            tok = Token(TokenType.StringText, "")
            for idx, char in enumerate(line):
                tok.value += char

                if char == ":" and context and context.type == TokenType.MetadataTag:
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.StringText and tok.value.strip():
                        line_toks.append(tok)
                    line_toks.append(Token(TokenType.MetadataAssignment, ":"))
                    tok = Token(TokenType.StringText, "")

                if char == "`" and ((not context and line[idx+1:].count("`") > 0) or (context and context.type == TokenType.InlineCode)):
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.StringText and tok.value.strip():
                        line_toks.append(tok)
                    tok = Token(TokenType.InlineCode, "`")
                    line_toks.append(tok)
                    if not context:
                        context = tok
                    else:
                        context = None
                    tok = Token(TokenType.StringText, "")

                if char == "@" and ((not context and line[idx+1:].count("@") > 0) or (context and context.type == TokenType.Link)):
                    tok.value = tok.value[:-1]
                    tmp = Token(TokenType.Link, "@")
                    if tok.type == TokenType.StringText and tok.value.strip():
                        if context:
                            context = None
                            assert tok.value.count(" ") > 0, "Link does not have a title!"
                            line_toks.extend([Token(TokenType.StringText, val) for val in tok.value.split(" ", 1)])
                        else:
                            line_toks.append(tok)
                            context = tmp
                    line_toks.append(tmp)
                    tok = Token(TokenType.StringText, "")

                # elif char == "^":
                #     occur_idxs = [idx for idx, c in enumerate(tok.value) if char == "^"] # Bold Text
                #     if occur_idxs > 1:
                #         decorated_text: str = line[idx : occur_idxs[-1] - 1]
                #         line_toks += ThymineInterpreter.tokenize_decorated_text(decorated_text)

                if idx == len(line)-1 and tok.type == TokenType.StringText and tok.value.strip() != "":
                    line_toks.append(tok)

            if len(line_toks) > 0:
                tokens.append(line_toks)
        return tokens

    def _get_ws_level(text: str) -> int:
        """ rank amount of whitespace by \"level\", useful for sub-bulletpoints """
        return int(ThymineInterpreter._len_tabs_to_spaces(text, 2) / 2)

    def _len_tabs_to_spaces(text: str, tabwidth: int) -> int:
        return len(text.replace('\t', ' ' * tabwidth))

