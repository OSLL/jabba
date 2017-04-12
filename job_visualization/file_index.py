
import os

from collections import OrderedDict
from collections import namedtuple

import yaml
from yaml import load, Loader, dump

import collections
from .file_data import FileData
from .util import is_job_config, convert_path

from .analysis.cyclic_deps import format_cycle
from .dep_extractor import IncludeInfo, include_flag

def ordered_constructor(loader, node):
    loader.flatten_mapping(node)
    pairs = loader.construct_pairs(node)
    return OrderedDict(pairs)

class FileIndex:
    """
    Indexes files for quick search by name or path
    """
    def __init__(self, path):
        self.path = path

        # name -> config for quick look up by job name
        self.jobs = {}

        # Dict: name -> (path, yaml)
        self.files = {}

        self.init_yaml_loader()

        # Jobs that were unfolded while unfolding the  file
        # Prevents goind into infinite recursion
        self.seen = set()

    def init_yaml_loader(self):
        Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, ordered_constructor)
        Loader.add_constructor('!include:', self.include_constructor)
        Loader.add_constructor('!include-raw:', self.include_raw_constructor)
        Loader.add_constructor('!include', self.include_constructor)


    def load_files(self, path):
        for filename in os.listdir(path):

            file_path = path + "/" + filename

            if os.path.isdir(file_path):
                self.load_files(file_path)
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                self.unfold_yaml(file_path)

    def add_file(self, path, yaml):
        if is_job_config(yaml):
            name = self.get_job_name(yaml)

            file_data = FileData(path=path, yaml=yaml)
            self.files[path] = file_data
            self.jobs[name] = file_data
        else:
            self.files[path] = FileData(path=path, yaml=yaml)


    def get_job_name(self, file_config):
        # Job is represented as list
        name = file_config['config']['job']['name']

        return name

    def get_by_name(self, name):
        try:
            return self.jobs[name]
        except KeyError:
            raise KeyError("No job with name {} found in {}".format(name, self.path))

    def get_by_path(self, path):

        path = convert_path(path)

        try:
            return self.files[path]
        except KeyError:
            raise KeyError("No file {} found in {}".format(path, self.path))


    def __contains__(self, key):
        return key in self.files

    def unfold_yaml(self, path):
        '''
        Unfolds file by given name

        Also adds all included files as nodes to include graph. To disable this,
        set include_graph.active = False before calling
        '''

        self.unfolding_stack = []

        return self._unfold_yaml(path)

    def _unfold_yaml(self, path):

        path = convert_path(path)

        try:
            file_data = self.get_by_path(path)

            config = file_data.yaml

            return config
        except KeyError:
            # Maybe we haven't unfolded it yet
            pass

        # Found cycle
        if path in self.unfolding_stack:
            cyclic_call = self.unfolding_stack[-1]

            cycle = self.unfolding_stack[self.unfolding_stack.index(cyclic_call):]

            cycle = [path] + cycle + [path]

            raise Exception("Cyclic include found. {}".format(format_cycle(cycle)))

        self.unfolding_stack.append(path)

        with open(path, 'r') as f:
            config = load(f)

            config = self.inject_include_info(path, config, include_type='include')

            self.add_file(path, config)

            self.unfolding_stack.pop()

            return config

    def inject_include_info(self, path, config, include_type):
        if isinstance(config, list):
            config = config[0]

        ret = OrderedDict()

        ret[include_flag] = IncludeInfo(type=include_type, path=path)
        ret['config'] = config

        return ret

    def include_constructor(self, loader, node):
        v = self._unfold_yaml(node.value)

        return v

    def include_raw_constructor(self, loader, node):

        path = convert_path(node.value)

        with open(path, 'r') as f:
            config = f.read()

            config = self.inject_include_info(path, config, include_type='include-raw')

            self.add_file(path, config)

            return config

    def default_load(self, name, config):
        pass
