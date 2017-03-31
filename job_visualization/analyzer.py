
from .yaml_unfolder import YamlUnfolder
from . import graphs
from .analysis import parse_analyzer_arguments

class Analyzer(YamlUnfolder):

    def __init__(self, root, synonyms, arguments):
        super(self.__class__, self).__init__(root=root)

        self.arguments = parse_analyzer_arguments(arguments)
        self.synonyms = synonyms
        self.root = root

        self.include_graph = graphs.include_graph.IncludeGraph()
        self.call_graph = graphs.call_graph.CallGraph(get_calls=self.get_calls_from_dict, unfold=self.unfold_yaml)

    def run(self):
        pass

    def print_result(self):
        pass
