from .token import Token, TokenType
from .parser import ThymineParser
import re
from typing import *


class ThymineLexer:
    HTML_ESCAPES = {
        "<": "&lt;",
        ">": "&gt;"
    }

    def tokenize(self, text: str):
        tokens: list[list[Token]] = []
        context: Union[Token, None] = None

        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            line_toks: list[Token] = []

            # Empty Lines
            if line.strip() == "":
                tokens.append([Token(TokenType.LINE_BREAK, "\n")])
                continue

            # Find tokens at the start of the line (no iteration needed)
            # TODO: set context specifications for each component
            # Metadata Tags
            if line.strip() == "-" and (context and context.type == TokenType.METADATA_TAG or not context and "-" in [line.strip() for line in lines[line_num+1:]]):
                tmp_tok: Token = Token(TokenType.METADATA_TAG, "-")
                tokens.append([tmp_tok])
                if context:
                    tmp_tok.parent = context
                    context = None
                else:
                    context = tmp_tok
                continue

            # Multi-Line Code
            if line.strip() == "~":
                tmp_tok = Token(TokenType.MULTILINE_CODE, "~")
                if context and context.type == TokenType.MULTILINE_CODE:
                    tmp_tok.parent = context
                    context = None
                else:
                    context = tmp_tok
                tokens.append([tmp_tok])
                continue

            # Headers
            header = re.search("#+ ", line)
            if header != None and header.start() == 0 and not context:
                line_toks.append(Token(TokenType.HEADER, header.group(0)))
                line = line.replace(header.group(0), "", 1)

            # Quote Blocks
            elif line.lstrip().startswith(">") and not context: 
                line_toks.append(Token(TokenType.QUOTE_BLOCK, ">"))
                line = line.replace(">", "", 1)

            # Bullet points
            elif line.lstrip().startswith("o"): 
                whitespace_len: int = self._get_ws_level(line.split("o")[0])
                line_toks.append(Token(TokenType.BULLETPOINT, "o", level=whitespace_len + 1))
                line = line.lstrip().replace("o", "", 1)

            tok = Token(TokenType.STRING_TEXT, "")
            ignored_char_idxs = set([])
            for idx, char in enumerate(line):
                if idx in ignored_char_idxs:
                    # Add String Text at end of line if last character is escaped
                    if idx == len(line)-1 and tok.type == TokenType.STRING_TEXT and tok.value.strip() != "":
                        line_toks.append(tok)
                    continue

                if char == "\\" and not context and idx != len(line) - 1:
                    if line[idx + 1] in self.HTML_ESCAPES.keys():
                        tok.value += self.HTML_ESCAPES[line[idx + 1]]
                        ignored_char_idxs.add(idx+1)
                    elif line[idx + 1] in TokenType.values():
                        tok.value += line[idx + 1]
                        ignored_char_idxs.add(idx+1)
                else:
                    tok.value += char

                # Metadata Assignments
                if char == ":" and context and context.type == TokenType.METADATA_TAG:
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.STRING_TEXT and tok.value.strip():
                        line_toks.append(tok)
                    line_toks.append(Token(TokenType.METADATA_ASSIGNMENT, ":"))
                    tok = Token(TokenType.STRING_TEXT, "")

                # Inline code
                if char == "`" and ((not context and line[idx+1:].count("`") > 0) or (context and context.type == TokenType.INLINE_CODE)):
                    tok.value = tok.value[:-1]
                    if tok.type == TokenType.STRING_TEXT and tok.value:
                        line_toks.append(tok)
                    tok = Token(TokenType.INLINE_CODE, "`")
                    line_toks.append(tok)
                    if not context:
                        context = tok
                    else:
                        context = None
                    tok = Token(TokenType.STRING_TEXT, "")

                # Links
                if char == "@" and ((not context and line[idx+1:].count("@") > 0) or (context and context.type == TokenType.LINK)):
                    tok.value = tok.value[:-1]
                    tmp = Token(TokenType.LINK, "@")
                    if context:
                        context = None
                        assert tok.value.count(" ") > 0, "Link does not have a title!"
                        line_toks.extend([Token(TokenType.STRING_TEXT, val) for val in tok.value.split(" ", 1)])
                    else:
                        if tok.value:
                            line_toks.append(tok)
                        context = tmp
                    line_toks.append(tmp)
                    tok = Token(TokenType.STRING_TEXT, "")

                # Images
                if char == "^" and ((not context and line[idx+1:].count("^") > 0) or (context and context.type == TokenType.IMAGE)):
                    tok.value = tok.value[:-1]
                    tmp = Token(TokenType.IMAGE, "@")
                    if context:
                        context = None
                        assert tok.value.count(" ") > 0, "Image does not have alt-text!"
                        line_toks.extend([Token(TokenType.STRING_TEXT, val) for val in tok.value.split(" ", 1)])
                    else:
                        if tok.value:
                            line_toks.append(tok)
                        context = tmp
                    line_toks.append(tmp)
                    tok = Token(TokenType.STRING_TEXT, "")

                # String Text at end of line
                if idx == len(line)-1 and tok.type == TokenType.STRING_TEXT and tok.value.strip() != "":
                    line_toks.append(tok)

            if len(line_toks) > 0:
                tokens.append(line_toks)
        return tokens

    def _get_ws_level(self, text: str) -> int:
        """ rank amount of whitespace by \"level\", useful for sub-bulletpoints """
        return int(self._len_tabs_to_spaces(text, 2) / 2)

    def _len_tabs_to_spaces(self, text: str, tabwidth: int) -> int:
        return len(text.replace('\t', ' ' * tabwidth))