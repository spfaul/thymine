import os
from pprint import pprint
from src.lang import ThymineInterpreter
from src.template import Template, get_templates

# temporary until we have a proper CLI
INPUT_PATH = "tests/test.tym"
BUILD_PATH = "tests/build/"
TEMPLATE_NAME = "debug"

def main():
    possible_templates = get_templates(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates.json"))
    
    template = Template(possible_templates[TEMPLATE_NAME], BUILD_PATH)
    template.copy_files()

    intpr: ThymineInterpreter = ThymineInterpreter()
    intpr.feed_file("tests/test.tym", template.get_output_path(INPUT_PATH), template.get_main_template_path())


if __name__ == '__main__':
    main()