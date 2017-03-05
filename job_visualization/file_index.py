
import os

class FileIndex:
    """
    Indexes files for quick search by name or path
    """
    def __init__(self, path, unfold):
        self.unfold = unfold
        self.path = path
        self.files = self.load_files(path)

    def load_files(self, path):
        files = {}
        for filename in os.listdir(path):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                name, file_yaml = self.load_file(path + "/" + filename)

                if name != None:
                    files[name] = file_yaml
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
