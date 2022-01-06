from pprint import pprint
from .lexer import ThymineLexer
from .parser import ThymineParser

class ThymineTranspiler:
    def __init__(self):
        self.lexer = ThymineLexer()
        self.parser = ThymineParser()

    def feed(self, text: str, output_path: str, template: str):
        """ Parse thymine-lang input """
        tokens = self.lexer.tokenize(text)
        pprint(tokens)

        html_str = self.parser.tokens_to_html(tokens, template)
        with open(output_path, 'w') as file:
            file.write(html_str)

    def feed_file(self, source_path: str, output_path: str, template_path: str):
        """ Parse a thymine-lang file given its relative/absolute path """
        with open(source_path, 'r') as source:
            with open(template_path, 'r') as template:
                self.feed(source.read(), output_path, template.read())

