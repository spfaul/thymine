from .token import Token, TokenType
from typing import List
from inspect import cleandoc
import textwrap
import itertools
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter, HtmlFormatter

class ThymineParser:
    def tokens_to_html(self, tokens: List[List[Token]], template: str = None) -> str:
        body: str = ""
        metadata: dict[str, str] = {}
        bulletpoint_level: int = 0
        bulletpoint_start: bool = False

        for line_num, line in enumerate(tokens):
            for idx, tok in enumerate(line):
                if tok.type == TokenType.HEADER:
                    assert idx != len(line) - 1, "Empty Header!"
                    head_level: int = tok.value.count("#")
                    body += f"<h{head_level}>{self.tokens_to_html([line[1:]])}</h{head_level}>"
                    for child_tok in line[idx+1:]:
                        child_tok.parent = tok

                if tok.type == TokenType.METADATA_TAG and not tok.parent:
                    metadata_chunk, metadata_tokens = self._collect_metadata(tokens[line_num+1:])
                    metadata.update(metadata_chunk)
                    for md_tok in metadata_tokens:
                        md_tok.parent = tok

                if tok.type == TokenType.QUOTE_BLOCK:
                    body += f"<quote-block>{self.tokens_to_html([line[idx+1:]])}</quote-block>"
                    for child_tok in line[idx+1:]:
                        child_tok.parent = tok

                # TODO: fix this or something
                if bulletpoint_start:
                    if (not tok.parent and tok.type != TokenType.BULLETPOINT) or (self._is_last_token(tokens, tok) and tok.parent and tok.parent.type == TokenType.BULLETPOINT):
                        bulletpoint_start = False
                        body += "</ul>" * bulletpoint_level

                if tok.type == TokenType.BULLETPOINT:
                    assert idx != len(line) - 1, "Empty BulletPoint!"

                    if not bulletpoint_start:
                        bulletpoint_start = True
                        body += "<ul>" * tok.level
                    elif tok.level > bulletpoint_level:
                        body += "<ul>" * (tok.level - bulletpoint_level)
                    elif tok.level < bulletpoint_level:
                        body += "</ul>" * (bulletpoint_level - tok.level)
                    
                    bulletpoint_level = tok.level
                    body += f"<li>{self.tokens_to_html([line[1:]])}</li>"
                    for child_tok in line[1:]:
                        child_tok.parent = tok

                if tok.type == TokenType.INLINE_CODE and not tok.parent:
                    code_text = ""
                    for next_tok_idx, next_tok in enumerate(line[idx+1:]):
                        next_tok.parent = tok
                        if next_tok.type == TokenType.INLINE_CODE:
                            break 
                        code_text += next_tok.value
                    body += f"<code>{code_text}</code>"

                if tok.type == TokenType.MULTILINE_CODE and not tok.parent:
                    code_body, code_toks = self._collect_multiline_code(tokens[line_num+1:])
                    for code_tok in code_toks:
                        code_tok.parent = tok 
                    body += f"{code_body}"

                if tok.type == TokenType.LINK and not tok.parent:
                    for i in range(1, 4): # Take ownership of URL, TITLE and closing tag
                        line[idx + i].parent = tok
                    body += f"<a href=\"{line[idx+1].value}\">{line[idx+2].value}</a>"

                if tok.type == TokenType.IMAGE and not tok.parent:
                    for i in range(1, 4): # Take ownership of URL and Alt-text and closing tag
                        line[idx + i].parent = tok
                    body += f"<img src=\"{line[idx + 1].value}\" alt=\"{line[idx + 2].value}\"></img>"                  

                if tok.type == TokenType.LINE_BREAK:
                    body += f"<br>"

                if tok.type == TokenType.STRING_TEXT and tok.parent == None:
                    body += f"<text>{tok.value}</text>"

        if not template:
            return body
        
        final_html: str = self._format_template(template, metadata, body)
        return final_html

    def _is_last_token(self, tokens, token: Token):
        return tokens[-1][-1] == token

    def _format_template(self, template: str, metadata: dict, body: str):
        # TODO: Indent and format HTML so it's presentable
        for key, val in metadata.items():
            template = template.replace("$THYMINE_META." + key, val)
        template = template.replace("$THYMINE_BODY", body)
        return template

    def _collect_multiline_code(self, tokens):
        code_toks = self._filter_multiline_code(tokens)
        if code_toks == None:
            return "<text>~</text>", []

        code_body = ""
        for tok in code_toks:
            code_body += tok.value
            if tok.type != TokenType.LINE_BREAK:
                code_body += "\n"

        lang = "md"
        header_line = code_body.split("\n")[0].lstrip()
        if header_line.startswith("$"):
            lang = header_line[1:].strip().lower()
            code_body = "\n".join(code_body.split("\n")[1:])
        lexer = get_lexer_by_name(lang)
        formatter = HtmlFormatter(style="monokai")
        return pygments.highlight(code_body, lexer=lexer, formatter=formatter), code_toks

    def _filter_multiline_code(self, tokens):
        code_toks = []
        for line in tokens:
            for tok in line:
                if tok.type == TokenType.MULTILINE_CODE:
                    return code_toks
                code_toks.append(tok)

    def _collect_metadata(self, tokens):
        md: List[Token] = self._filter_metadata(tokens)
        md_dict: dict[str, str] = {}

        assert md != None, "Metadata Tag Not Closed!"

        for idx, tok in enumerate(md):
            if tok.type == TokenType.METADATA_ASSIGNMENT:
                assert idx != 0 and idx != len(md) - 1, "Invalid metadata assignment syntax with \":\""
                key, val = md[idx-1], md[idx+1]
                assert key.type == TokenType.STRING_TEXT and val.type == TokenType.STRING_TEXT, "Metadata assignment only accepts strings"
                md_dict[key.value.strip()] = val.value.strip()

        return md_dict, md

    def _filter_metadata(self, tokens: List[List[Token]]) -> List[Token]:
        metadata: List[Token] = []

        for line in tokens:
            for tok in line:
                if tok.type == TokenType.METADATA_TAG:
                    return metadata
                metadata.append(tok)