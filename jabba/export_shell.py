
from collections import OrderedDict
from os.path import splitext, exists
from os import makedirs

from .util import extract_from_config

def export_shell(file_index, to_dir):
    if not exists(to_dir):
        makedirs(to_dir)

    for _, file_data in file_index.files.items():
        export_from_file(file_data, to_dir)

def export_from_file(file_data, to_dir):
    shells = extract_shells_from_dict(file_data.yaml)
    path = file_data.path

    if len(shells) == 0:
        return

    for i in range(len(shells)):
        shell = shells[i]

        shell = extract_from_config(shell)

        if len(shells) == 1:
            file_name = "{}/{}.sh".format(to_dir, flatten_path(path))
        else:
            file_name = "{}/{}_{}.sh".format(to_dir, flatten_path(path), i)

        with open(file_name, 'w+') as f:
            f.write(shell)

def extract_shells_from_dict(yaml):
    shells = []

    if type(yaml) == OrderedDict or type(yaml) == dict:
        for key, value in yaml.items():
            if key == 'shell':
                shells.append(value)
            else:
                shells.extend(extract_shells_from_dict(value))

    elif type(yaml) == list:
        for value in yaml:
            shells.extend(extract_shells_from_dict(value))

    return shells

def flatten_path(path):
    path = path.replace('/', '-')

    path = splitext(path)[0]

    return path
