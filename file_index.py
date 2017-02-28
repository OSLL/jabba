
import os

class FileIndex:
    """
    Indexes files for quick search by name or path
    """
    def __init__(self, path, unfold):
        self.unfold = unfold
        self.files = self.load_files(path)

    def load_files(self, path):
        files = {}
        for filename in os.listdir(path):
            if filename.endswith(".yaml"):
                name, file_yaml = self.load_file(path + "/" + filename)

                files[name] = file_yaml
        return files

    def load_file(self, path):
        file_yaml = self.unfold(path)
        name = file_yaml[0]['job']['name']

        return name, file_yaml

    def get_by_name(self, name):
        return self.files[name]
