import os
from pprint import pprint
from src.lang import ThymineTranspiler
from src.template import Template, get_templates

# temporary until we have a proper CLI
INPUT_PATH = "examples/test.tym"
BUILD_PATH = "examples/build/"
TEMPLATE_NAME = "debug"

def main():
    possible_templates = get_templates(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates.json"))
    
    template = Template(possible_templates[TEMPLATE_NAME], BUILD_PATH)
    template.copy_files()

    tpiler = ThymineTranspiler()
    tpiler.feed_file("examples/test.tym", template.get_output_path(INPUT_PATH), template.get_main_template_path())

if __name__ == '__main__':
    main()