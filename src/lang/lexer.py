from .token import Token, TokenType, SpecialChars
from .parser import ThymineParser
import re
from typing import *


class ThymineLexer:
    # TODO: Make use of class members

    def tokenize(self, text: str):
        tokens: list[list[Token]] = []
        context: Union[Token, None] = None

        for line in text.split("\n"):
            line_toks: list[Token] = []

            # Empty Lines
            if line.strip() == "":
                tokens.append([Token(TokenType.LineBreak, "\n")])
                continue

            # Find tokens at the start of the line (no iteration needed)
            # TODO: set context specifications for each component
            # Metadata Tags
            if line.strip() == "-" and (context and context.type == TokenType.MetadataTag or not context):
                tmp_tok: Token = Token(TokenType.MetadataTag, "-")
                tokens.append([tmp_tok])
                if context:
                    context = None
                else:
                    context = tmp_tok
                continue

            # Multi-Line Code
            if line.strip() == "~":
                tmp_tok = Token(TokenType.MultiLineCode, "~")
                if context and context.type == TokenType.MultiLineCode:
                    tmp_tok.parent = context
                    context = None
                else:
                    context = tmp_tok
                tokens.append([tmp_tok])
                continue

            # Headers
            header = re.search("#+ ", line)
            if header != None and header.start() == 0 and not context:
                line_toks.append(Token(TokenType.Header, header.group(0)))
                line = line.replace(header.group(0), "", 1)

            # Quote Blocks
            elif line.lstrip().startswith(">") and not context: 
                line_toks.append(Token(TokenType.QuoteBlock, ">"))
                line = line.replace(">", "", 1)

            # Bullet points
            elif line.lstrip().startswith("o"): 
                whitespace_len: int = self._get_ws_level(line.split("o")[0])
                line_toks.append(Token(TokenType.BulletPoint, "o", level=whitespace_len + 1))
                line = line.lstrip().replace("o", "", 1)

            tok = Token(TokenType.StringText, "")
            ignored_char_idxs = set([])
            for idx, char in enumerate(line):
                if idx in ignored_char_idxs:
                    continue

                if char == "\\" and not context:
                    special_chars = [i.value for i in SpecialChars]
                    if idx != len(line) - 1 and line[idx + 1] in special_chars:
                        # treat escaped char as regular char and ignore it on the next iter
                        tok.value += line[idx + 1]
                        ignored_char_idxs.add(idx+1)
                else:
                    tok.value += char

                # Metadata Assignments
                if char == ":" and context and context.type == TokenType.MetadataTag:
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.StringText and tok.value.strip():
                        line_toks.append(tok)
                    line_toks.append(Token(TokenType.MetadataAssignment, ":"))
                    tok = Token(TokenType.StringText, "")

                # Inline code
                if char == "`" and ((not context and line[idx+1:].count("`") > 0) or (context and context.type == TokenType.InlineCode)):
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.StringText and tok.value:
                        line_toks.append(tok)
                    tok = Token(TokenType.InlineCode, "`")
                    line_toks.append(tok)
                    if not context:
                        context = tok
                    else:
                        context = None
                    tok = Token(TokenType.StringText, "")

                # Links
                if char == "@" and ((not context and line[idx+1:].count("@") > 0) or (context and context.type == TokenType.Link)):
                    tok.value = tok.value[:-1]
                    tmp = Token(TokenType.Link, "@")
                    if context:
                        context = None
                        assert tok.value.count(" ") > 0, "Link does not have a title!"
                        line_toks.extend([Token(TokenType.StringText, val) for val in tok.value.split(" ", 1)])
                    else:
                        if tok.value:
                            line_toks.append(tok)
                        context = tmp
                    line_toks.append(tmp)
                    tok = Token(TokenType.StringText, "")

                # elif char == "^":
                #     occur_idxs = [idx for idx, c in enumerate(tok.value) if char == "^"] # Bold Text
                #     if occur_idxs > 1:
                #         decorated_text: str = line[idx : occur_idxs[-1] - 1]
                #         line_toks += self.tokenize_decorated_text(decorated_text)

                if idx == len(line)-1 and tok.type == TokenType.StringText and tok.value.strip() != "":
                    line_toks.append(tok)

            if len(line_toks) > 0:
                tokens.append(line_toks)
        return tokens

    def _get_ws_level(self, text: str) -> int:
        """ rank amount of whitespace by \"level\", useful for sub-bulletpoints """
        return int(self._len_tabs_to_spaces(text, 2) / 2)

    def _len_tabs_to_spaces(self, text: str, tabwidth: int) -> int:
        return len(text.replace('\t', ' ' * tabwidth))