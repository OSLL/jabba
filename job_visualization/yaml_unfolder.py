import collections
from collections import OrderedDict


import graphviz as gv
import os

from . import graphs
from .file_index import FileIndex
from .file_data import FileData
from .dep_extractor import DepExtractor

  
class YamlUnfolder(object):

    def __init__(self, root, rank_dir=None):

        self.initing = True

        self.root = root
        self.rank_dir = rank_dir

        self.init_file_index()

        self.dep_extractor = DepExtractor(self.file_index)

        self.init_include_graph()

        self.init_call_graph()

        self.initing = False

    def init_file_index(self):
        self.file_index = FileIndex(path=self.root)
        self.file_index.load_files(self.root)

    def init_include_graph(self):
        # Each graph should be able to have its own default rank_dir parameter
        if self.rank_dir is None:
            self.include_graph = graphs.include_graph.IncludeGraph(dep_extractor=self.dep_extractor, file_index=self.file_index)
        else:
            self.include_graph = graphs.include_graph.IncludeGraph(dep_extractor=self.dep_extractor, file_index=self.file_index, rank_dir=self.rank_dir)

    def init_call_graph(self):
        if self.rank_dir is None:
            self.call_graph = graphs.call_graph.CallGraph(dep_extractor=self.dep_extractor, file_index=self.file_index)
        else:
            self.call_graph = graphs.call_graph.CallGraph(rank_dir=self.rank_dir, dep_extractor=self.dep_extractor, file_index=self.file_index)

    def unfold_yaml(self, path):
        return self.file_index.unfold_yaml(path)

    def get_calls(self, path):
        return self.dep_extractor.get_calls(path)

    def get_includes(self, path):
        return self.dep_extractor.get_includes(path)

