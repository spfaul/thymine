import os
from pprint import pprint
from src.lang import ThymineTranspiler
from src.template import Template, get_templates
import argparse


# temporary until we have a proper CLI
INPUT_PATH = "examples/test.tym"
BUILD_PATH = "examples/build/"
TEMPLATE_NAME = "debug"

def cli():
    parser = argparse.ArgumentParser(description="The Official Thymine Compiler.")
    parser.add_argument("SOURCE_PATH", metavar="SOURCE_PATH", type=str,
                        help="Absolute/Relative path of TL source file to compile")
    parser.add_argument("BUILD_PATH", metavar="BUILD_FOLDER_PATH", type=str,
                        help="Absolute/Relative path of build folder")
    parser.add_argument("-t", dest='TEMPLATE_NAME', metavar="TEMPLATE_NAME",
                        type=str, default="debug",
                        help="Name of template to use when building.")
    args = parser.parse_args()
    return args

def main(args):
    possible_templates = get_templates(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates.json"))
    
    template = Template(possible_templates[args.TEMPLATE_NAME], args.BUILD_PATH)
    template.create_build_folder()

    tpiler = ThymineTranspiler()
    tpiler.feed_file(args.SOURCE_PATH, template.get_output_path(args.SOURCE_PATH), template.get_main_template_path())
    
    template.copy_files()

if __name__ == '__main__':
    args = cli()
    main(args)