import collections

import ruamel.yaml
from ruamel.yaml import load, Loader, dump

import graphviz as gv
import os

from include_graph import IncludeGraph
import call_graph
from file_index import FileIndex

import warnings
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)


'''
Tuple for storing calls
project_name is a name of a job that is called
call_config is a config of call file, i.e. trigger-builds
project_config is a config of job that is been called
'''
CallObject = collections.namedtuple('CallObject', ['project_name', 'call_config', 'project_config', 'caller_name'])

def convert_path(path):
    if os.path.isabs(path):
        raise Exception("Cannot include file with absolute path {}. Please use relative path instead".format((path)))

    path = os.path.normpath(path)

    return path
    
class YamlUnfolder(object):

    def __init__(self, root, rank_dir=None):
        Loader.add_constructor('!include:', self.include_constructor)
        Loader.add_constructor('!include-raw:', self.include_raw_constructor)
        Loader.add_constructor('!include', self.include_constructor)

        # Each graph should be able to have its own default rank_dir parameter
        if rank_dir is None:
            self.include_graph = IncludeGraph()
            self.call_graph = call_graph.CallGraph(get_calls=self.get_calls_from_dict, unfold=self.unfold_yaml)
        else:
            self.include_graph = IncludeGraph(rank_dir)
            self.call_graph = call_graph.CallGraph(rank_dir=rank_dir, get_calls=self.get_calls_from_dict, unfold=self.unfold_yaml)

        self.file_index = FileIndex(root, self.unfold_yaml)


    def include_constructor(self, loader, node):
        v = self.unfold_yaml(node.value)

        return v

    def include_raw_constructor(self, loader, node):

        node.value = convert_path(node.value)

        self.include_graph.add_node(node.value)
        self.include_graph.add_edge_from_last_node(node.value, 
                    label='<<B>include-raw</B>>', color='include_raw_color')

        with open(node.value, 'r') as f:
            text = f.read()

            return text

    def unfold_yaml(self, file_name, is_root=False):
        '''
        Unfolds file by given name

        Also adds all included files as nodes to include graph. To disable this,
        set include_graph.active = False before calling
        '''

        file_name = convert_path(file_name)

        self.include_graph.add_node(file_name)
        self.include_graph.add_to_list(file_name)

        with open(file_name, 'r') as f:
            initial_dict = load(f)

            if len(self.include_graph.include_list) >= 2:
                self.include_graph.pop_from_list()
                self.include_graph.add_edge_from_last_node(file_name, 
                        label='<<B>include</B>>', color='include_color')
            return initial_dict


    def get_calls(self, file_name):
        '''
        Reads file by given name and returns CallObject array
        '''
        
        file_dict = self.unfold_yaml(file_name)

        name = file_dict[0]['job']['name']

        calls = self.get_calls_from_dict(file_dict[0], from_name=name)

        return calls

    def get_data_from_name(self, name):
        '''
        Finds .yaml config by given name
        Slow version that will scan all files in the directory for each call
        '''

        return self.file_index.get_by_name(name)

    def get_calls_from_dict(self, file_dict, from_name, settings={}):
        '''
        Processes unfolded yaml object to CallObject array

        settings is a dict of settings for keeping information like
        in what section we are right now (e.g. builders, publishers)
        '''

        calls = []
        call_settings = dict(settings)

        # Include all possible sections
        # The way to draw them is defined in call graph
        special_sections = {'builders', 'publishers', 'wrappers'}

        # Trigger flags
        triggers = {'trigger-builds', 'trigger-parameterized-builds'}

        if type(file_dict) == dict:
            for key in file_dict:

                if key in special_sections:
                    call_settings['section'] = key

                if key in triggers:
                    calls.extend(self.extract_call(file_dict[key], from_name, settings=call_settings))
                else:
                    calls.extend(self.get_calls_from_dict(file_dict[key], from_name, settings=call_settings))
        elif type(file_dict) == list:
            for value in file_dict:
                calls.extend(self.get_calls_from_dict(value, from_name, settings=call_settings))

        return calls


    def extract_call(self, call, from_name, settings):
        '''
        Creates CallObject from call file (i.e. trigger-builds)

        Returns a list of calls
        '''

        call = collections.defaultdict(lambda: None, call[0])

        try:
            call['section'] = settings['section']
        except KeyError:
            call['section'] = ''

        project = call['project']

        # If there is more than one call in a single file
        if type(project) == list:
            calls = []

            for name in project:
                calls.append(self.create_call(name, call, from_name))

            return calls
        else:
            return [self.create_call(project, call, from_name)]

    def create_call(self, project, call, from_name):
        file_data = self.get_data_from_name(project)

        call_object = CallObject(project_name=project, call_config=call, project_config=file_data, caller_name=from_name)
        return call_object

    def reset(self):
        self.include_graph.reset()
