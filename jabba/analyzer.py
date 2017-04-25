
from imp import load_source

from .yaml_unfolder import YamlUnfolder
from . import graphs
from . import analysis
from .analysis import parse_analyzer_arguments
from .util import is_job_config
from .synonym_parser import SynonymSet

def get_analysis_function(argument, export_analysis):
    func = None

    try:
        func = getattr(analysis, argument.function)
    except AttributeError:
        if export_analysis is not None:
            module = load_source('user_analysis', export_analysis)

            func = getattr(module, argument.function)

    if func is None:
        raise AttributeError("Cannot find analysis function {}".format(argument.function))

    return func

def load_module(export_analysis):
    if export_analysis.endswith(".py"):
        return load_source(export_analysis)
    else:
        # Load as module
        pass

class Analyzer(YamlUnfolder):

    def __init__(self, root, arguments, file_index, dep_extractor, export_analysis=None, synonyms=SynonymSet(), verbose=0):
        super(self.__class__, self).__init__(root=root, verbose=0)

        self.verbose = verbose

        self.arguments = parse_analyzer_arguments(arguments)
        self.synonyms = synonyms
        self.root = root
        self.file_index = file_index
        self.export_analysis = export_analysis

        self.include_graph = graphs.include_graph.IncludeGraph(dep_extractor=dep_extractor, file_index=file_index)
        self.include_graph.active = True
        self.call_graph = graphs.call_graph.CallGraph(dep_extractor=dep_extractor, file_index=self.file_index)

        self.results = []

        self.create_include_graph()
        self.create_call_graph()

    def create_include_graph(self):
        if self.verbose == 2:
            print("Creating full include graph for analysis")

        for name, file_data in self.file_index.files.items():
            self.include_graph.unfold_file(file_data.path)

    def create_call_graph(self):
        if self.verbose == 2:
            print("Creating full call graph for analysis")

        for name, file_data in self.file_index.files.items():
            if not is_job_config(file_data.yaml):
                continue

            self.call_graph.unfold_config(file_data.path, file_data.yaml)
        
    def run(self):
        self.results = []

        options = {
            'synonyms': self.synonyms,
            'include_graph': self.include_graph,
            'call_graph': self.call_graph,
            'file_index': self.file_index,
            'dep_extractor': self.dep_extractor
        }

        for argument in self.arguments:
            func = get_analysis_function(argument, self.export_analysis)

            if self.verbose == 2:
                print("Running {} analysis function".format(argument.function))

            result = func(options=options, **argument.arguments)

            self.results.append(result)

    def is_ok(self):
        return all(result.is_ok() for result in self.results)

    def print_result(self):
        for result in self.results:
            print(result)
