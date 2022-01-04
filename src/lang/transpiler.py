from .token import Token, TokenType
from typing import List
from inspect import cleandoc
import textwrap
import itertools
from yattag import indent

class ThymineToHTMLTranspiler:
    def __init__(self):
        self.tokens: List[List[Token]] = []

    def tokens_to_html(self, tokens: List[List[Token]], template: str = None) -> str:
        self.tokens = tokens
        body: str = ""
        metadata_loaded: bool = False
        metadata: dict[str, str] = {}
        bulletpoint_level: int = 0
        bulletpoint_start: bool = False

        for line_num, line in enumerate(self.tokens):
            for idx, tok in enumerate(line):
                # close bulletpoint ul tags (god no)

                if tok.type == TokenType.Header:
                    assert idx != len(line) - 1, "Empty Header!"
                    head_level: int = tok.value.count("#")
                    body += f"<h{head_level}>{self.tokens_to_html([line[1:]])}</h{head_level}>"
                    for child_tok in line[idx+1:]:
                        child_tok.parent = tok

                if tok.type == TokenType.MetadataTag and not metadata_loaded:
                    metadata, metadata_tokens = self._collect_metadata(self.tokens[line_num+1:])
                    metadata_loaded = True

                    for md_tok in metadata_tokens:
                        md_tok.parent = tok

                if tok.type == TokenType.MetadataAssignment and tok.parent == None:
                    body += f"<text>{tok.value}</text>"

                if tok.type == TokenType.QuoteBlock:
                    body += f"<quote-block>{self.tokens_to_html([line[idx+1:]])}</quote-block>"
                    for child_tok in line[idx+1:]:
                        child_tok.parent = tok

                if bulletpoint_start:
                    if (not tok.parent and tok.type != TokenType.BulletPoint) or (self._is_last_token(tok) and tok.parent and tok.parent.type == TokenType.BulletPoint):
                        bulletpoint_start = False
                        body += "</ul>" * bulletpoint_level

                if tok.type == TokenType.BulletPoint:
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

                if tok.type == TokenType.InlineCode and not tok.parent:
                    code_text = ""
                    for next_tok_idx, next_tok in enumerate(line[idx+1:]):
                        next_tok.parent = tok
                        if next_tok.type == TokenType.InlineCode:
                            break 
                        code_text += next_tok.value
                    body += f"<code>{code_text}</code>"

                if tok.type == TokenType.Link and not tok.parent:
                    for i in range(1, 4): # Take ownership of URL, TITLE and closing tag
                        line[idx + i].parent = tok
                    body += f"<a href=\"{line[idx+1].value}\">{line[idx+2].value}</a>"

                if tok.type == TokenType.LineBreak:
                    body += f"<br>"

                if tok.type == TokenType.StringText and tok.parent == None:
                    body += f"<text>{tok.value}</text>"

        if not template:
            return body
        
        final_html: str = self._format_template(template, metadata, body)
        return self._prettify_html(final_html)


    def _is_last_token(self, token: Token):
        return self.tokens[-1][-1] == token

    def _format_template(self, template: str, metadata: dict, body: str):
        template = template.replace("$THYMINE_BODY", body) #TODO: proper indentation
        for key, val in metadata.items():
            template = template.replace("$THYMINE_META." + key, val)
        return template

    def _prettify_html(self, text: str):
        return indent(text, indentation=" "*4, newline="\n", indent_text=False)

    def _collect_metadata(self, tokens):
        md: List[Token] = self._filter_metadata(tokens)
        assert md != None, "No closing metadata tag found!"

        md_dict: dict[str, str] = {}

        for idx, tok in enumerate(md):
            if tok.type == TokenType.MetadataAssignment:
                assert idx != 0 and idx != len(md) - 1, "Invalid metadata assignment syntax with \":\""
                key, val = md[idx-1], md[idx+1]
                assert key.type == TokenType.StringText and val.type == TokenType.StringText, "Metadata assignment only accepts strings"
                md_dict[key.value.strip()] = val.value.strip()

        return md_dict, md

    def _filter_metadata(self, tokens: List[List[Token]]) -> List[Token]:
        metadata: List[Token] = []

        for line in tokens:
            for tok in line:
                if tok.type == TokenType.MetadataTag:
                    return metadata
                metadata.append(tok)