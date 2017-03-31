
import os

import collections
from .file_data import FileData

class FileIndex:
    """
    Indexes files for quick search by name or path
    """
    def __init__(self, path, unfold):
        self.unfold = unfold
        self.path = path

        # Dict: name -> (path, yaml)
        self.files = self.load_files(path)

    def load_files(self, path):
        files = {}
        for filename in os.listdir(path):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                file_path = path + '/' + filename
                name, file_yaml = self.load_file(file_path)

                if name != None:
                    file_data = FileData(path=file_path, yaml=file_yaml)
                    files[name] = file_data
        return files

    def load_file(self, path):
        file_yaml = self.unfold(path)

        # Job is represented as list
        if type(file_yaml) == list:
            name = file_yaml[0]['job']['name']

            return name, file_yaml
        else:
            return None, None

    def get_by_name(self, name):
        try:
            return self.files[name]
        except KeyError:
            raise Exception("No job with name {} found in {}".format(name, self.path))
