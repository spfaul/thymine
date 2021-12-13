import os
from src.lang import ThymineInterpreter
from src.template import Template, get_templates



def main():
    possible_templates = get_templates(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates.json"))
    
    template = Template(possible_templates["debug"], "tests/build/")
    template.copy_files()

    intpr: ThymineInterpreter = ThymineInterpreter()
    intpr.feed_file("tests/test.tym", template.get_output_path("tests/test.tym"), template.get_main_template_path())




if __name__ == '__main__':
    main()