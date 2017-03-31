
import os

import collections
from .file_data import FileData
from .util import is_job_config

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

            file_path = path + "/" + filename

            if os.path.isdir(file_path):
                updates = (self.load_files(file_path))
                files.update(updates)

            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                file_config = self.unfold(file_path)

                if is_job_config(file_config):
                    name, file_yaml = self.load_job_file(file_config)

                    file_data = FileData(path=file_path, yaml=file_yaml)
                    files[name] = file_data
                else:
                    files[file_path] = FileData(path=file_path, yaml=file_config)

        return files

    def load_job_file(self, file_config):
        # Job is represented as list
        name = file_config[0]['job']['name']

        return name, file_config

    def get_by_name(self, name):
        try:
            return self.files[name]
        except KeyError:
            raise Exception("No job with name {} found in {}".format(name, self.path))
