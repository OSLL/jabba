
from .yaml_unfolder import YamlUnfolder
from . import graphs
from . import analysis
from .analysis import parse_analyzer_arguments
from .util import is_job_config
from .synonym_parser import SynonymSet

class Analyzer(YamlUnfolder):

    def __init__(self, root, arguments, file_index, synonyms=SynonymSet()):
        super(self.__class__, self).__init__(root=root)

        self.arguments = parse_analyzer_arguments(arguments)
        self.synonyms = synonyms
        self.root = root
        self.file_index = file_index

        self.include_graph = graphs.include_graph.IncludeGraph()
        self.include_graph.active = True
        self.call_graph = graphs.call_graph.CallGraph(get_calls=self.get_calls_from_dict, unfold=self.unfold_yaml)

        self.results = []

        self.create_include_graph()
        self.create_call_graph()

    def create_include_graph(self):
        for name, file_data in self.file_index.files.items():
            self.unfold_yaml(file_data.path)
            self.include_graph.reset()

    def create_call_graph(self):
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
            'file_index': self.file_index
        }

        for argument in self.arguments:
            func = None

            try:
                func = getattr(analysis, argument.function)
            except AttributeError:
                raise AttributeError("Cannot find analysis function {}".format(argument.function))

            result = func(options=options, **argument.arguments)
            self.results.append(result)

    def is_ok(self):
        return all(result.is_ok() for result in self.results)

    def print_result(self):
        for result in self.results:
            print(result)
