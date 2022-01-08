import os
import shutil
import json
from pathlib import Path

class Template:
    def __init__(self, config: dict, out_path: str):
        self.config = config
        self.out_path = out_path

    def get_main_template_path(self):
        return self.config["main_template"]

    def get_output_path(self, file_path: str):
        filename_no_ext: str = Path(file_path).stem
        return os.path.join(self.out_path, filename_no_ext + ".html")    

    def create_build_folder(self):
        try:
            os.makedirs(self.out_path)
        except FileExistsError:
            # directory already exists
            pass

    def copy_files(self):
        if "extras" not in self.config.keys():
            return

        for file_path in self.config["extras"]:
            _, file_name = os.path.split(file_path)
            shutil.copy(file_path, os.path.join(self.out_path, file_name))

def get_templates(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)


