from .token import Token, TokenType
from typing import List
from inspect import cleandoc
import textwrap
import itertools

class ThymineToHTMLTranspiler:
    def __init__(self):
        pass

    def tokens_to_html(self, tokens: List[List[Token]], template: str) -> str:
        body: str = ""
        metadata_loaded: bool = False
        metadata: dict[str, str] = {}

        for line_num, line in enumerate(tokens):
            for idx, tok in enumerate(line):
                if tok.type == TokenType.Header:
                    assert idx != len(line) - 1, "Empty Header!"
                    head_text_tok: str = line[idx + 1]
                    assert head_text_tok.type == TokenType.StringText, "Header has no text token!"
                    head_text_tok.parent = tok
                    head_level: int = tok.value.count("#")

                    body += f"\n<h{head_level}>{head_text_tok.value}</h{head_level}>\n"

                elif tok.type == TokenType.MetadataTag and not metadata_loaded:
                    metadata, metadata_tokens = self._collect_metadata(tokens[line_num+1:])
                    metadata_loaded = True

                    for md_tok in metadata_tokens:
                        md_tok.parent = tok

                elif tok.type == TokenType.QuoteBlock:
                    if idx == len(line) - 1:
                        text = ""
                    else:
                        text_tok = line[idx + 1]
                        text_tok.parent = tok
                        text = text_tok.value
                    body += f"\n<quote-block>{text}</quote-block>\n"

                elif tok.type == TokenType.StringText and tok.parent == None:
                    body += f"{tok.value}"


        # TODO: make the identation not ugly
        final_html: str = self._format_template(template, metadata, body)

        return self._prettify_html(final_html)

    def _format_template(self, template: str, metadata: dict, body: str):
        template = template.replace("$THYMINE_BODY", body) #TODO: proper indentation
        for key, val in metadata.items():
            template = template.replace("$THYMINE_META." + key, val)
        return template

    def _prettify_html(self, text: str):
        prettified_text: str = ""
        text = cleandoc(text)
        for line in text.split("\n"):
            if line.strip() == "":
                continue
            prettified_text += line + "\n"

        return prettified_text

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