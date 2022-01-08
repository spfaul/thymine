import argparse
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

def main():
    description = """
        Generate CSS for Syntax Highlighted Code based on popular color schemes.

        Examples:
            [python3 css-code-highlight-gen.py --list]
            [python3 css-code-highlight-gen.py --scheme monokai]
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--scheme", dest="COLOR_SCHEME", metavar="COLOR_SCHEME", help="Color Scheme Name")
    parser.add_argument("--list", action="store_true", dest="LIST", help="List All Available Color Schemes")

    args = parser.parse_args()

    if args.LIST:
        print("\n".join(get_all_styles()))
        return

    formatter = HtmlFormatter(style=args.COLOR_SCHEME)
    print(formatter.get_style_defs())

if __name__ == '__main__':
    main()