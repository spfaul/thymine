from .token import Token, TokenType
from typing import List
from inspect import cleandoc
import textwrap

class ThymineToHTMLTranspiler:
    def __init__(self):
        pass

    def tokens_to_html(self, tokens: List[List[Token]]) -> str:
        head: str = cleandoc("""<meta charset="UTF-8" />
                                <meta name="viewport" content="width=device-width,initial-scale=1" />""")
        body: str = ""
        metadata_loaded: bool = False
        metadata: dict[str, str] = {}

        for line_num, line in enumerate(tokens):
            for idx, tok in enumerate(line):
                if tok.type == TokenType.Header:
                    assert idx != len(line) - 1, "Empty Header!"
                    head_text_tok: str = line[idx + 1]
                    head_level: int = tok.value.count("#")

                    assert head_text_tok.type == TokenType.StringText, "Header has no text token!"
                    if body:
                        body += "\n"
                    body += f"<h{head_level}>{head_text_tok.value}<h{head_level}>"

                elif tok.type == TokenType.MetadataTag and not metadata_loaded:
                    metadata = self._collect_metadata(tokens[line_num+1:])
                    metadata_loaded = True
                    print(metadata)
                    if "TITLE" in metadata.keys():
                        head += f"\n<title>{metadata['TITLE']}</title>"


        out: str = f"""
<!DOCTYPE html>
<html lang="en">
<head>
{textwrap.indent(head, 4 * " ")}
</head>
<body>
{textwrap.indent(body, 4 * " ")}
</body>
</html>"""
        return out

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

        return md_dict

    def _filter_metadata(self, tokens: List[List[Token]]) -> List[Token]:
        metadata: List[Token] = []

        for line in tokens:
            for tok in line:
                if tok.type == TokenType.MetadataTag:
                    return metadata
                metadata.append(tok)