
from collections import namedtuple, defaultdict

from .graphs import Edge

'''
project_name is a name of a job that is called
call_config is a config of call file, i.e. trigger-builds
project_config is a config of job that is been called
'''
class CallEdge(Edge):
    def __init__(self, to, call_config, project_config, caller_name):
        super(self.__class__, self).__init__(to, call_config)

        self.project_config = project_config
        self.caller_name = caller_name

'''
This flags are injected into unfolded configs so we can see that originaly they were included by
!include or !include-raw 
'''
include_flag = '__jenkins_job_builder_analysis_include_flag__'

'''
Info about included file
type is either 'include' or 'include-raw'
path is the original path to the file included
'''
IncludeInfo = namedtuple('IncludeInfo', ['type', 'path'])

 
class DepExtractor(object):

    def __init__(self, file_index, verbose=0):
        self.file_index = file_index
        self.verbose = verbose

    '''
    ==============
    Get calls part
    ==============
    '''

    def get_calls(self, job_name):
        '''
        Reads file by given name and returns CallEdge array
        '''

        config = self.file_index.get_by_name(job_name).yaml

        calls = self.get_calls_from_dict(config, from_name=job_name)

        return calls

    def get_calls_from_dict(self, file_dict, from_name, settings={}):
        '''
        Processes unfolded yaml object to CallEdge array

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

        if isinstance(file_dict, dict):
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
        Creates CallEdge from call file (i.e. trigger-builds)

        Returns a list of calls
        '''

        call = defaultdict(lambda: None, call[0])

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
        file_data = self.file_index.get_by_name(project)

        call_object = CallEdge(to=project, call_config=call, project_config=file_data, caller_name=from_name)
        return call_object

    '''
    =================
    Get includes part
    =================
    '''

    def get_includes(self, path):
        config = self.file_index.unfold_yaml(path)

        return self.get_includes_from_dict(config, extract=True)

    def get_includes_from_dict(self, config, extract=False):
        if extract and isinstance(config, dict) and 'config' in config:
            config = config['config']
        
        includes = []

        if isinstance(config, dict):
            if include_flag in config:
                includes.append(config[include_flag])
            else:
                for key in config:
                    includes.extend(self.get_includes_from_dict(config[key]))
        elif isinstance(config, list):
            for value in config:
                includes.extend(self.get_includes_from_dict(value))

        return includes
