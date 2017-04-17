
import os

import collections
from .file_data import FileData
from .util import is_job_config

class FileIndex:
    """
    Indexes files for quick search by name or path
    """
    def __init__(self, path, unfold, load_files=True):
        self.unfold = unfold
        self.path = path

        if load_files:
            # Dict: name -> (path, yaml)
            self.files = self.load_files(path)
        else:
            self.files = {}

    def load_files(self, path):
        files = {}

        for filename in os.listdir(path):

            file_path = path + "/" + filename

            if os.path.isdir(file_path):
                updates = self.load_files(file_path)
                files.update(updates)

            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                file_config = self.unfold(file_path)

                self.add_file(file_path, file_config, files=files)

        return files

    def add_file(self, file_path, yaml, files=None):
        if files is None:
            files = self.files

        if is_job_config(yaml):
            name, file_yaml = self.load_job_file(yaml)

            file_data = FileData(path=file_path, yaml=file_yaml)
            files[name] = file_data
        else:
            files[file_path] = FileData(path=file_path, yaml=yaml)


    def load_job_file(self, file_config):
        # Job is represented as list
        name = file_config[0]['job']['name']

        return name, file_config

    def get_by_name(self, name):
        try:
            return self.files[name]
        except KeyError:
            raise Exception("No job with name {} found in {}".format(name, self.path))

    def __contains__(self, key):
        return key in self.files
