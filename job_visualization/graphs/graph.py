
import graphviz as gv

from .legend import Legend

class Graph(object):
    """
    Abstract class for render graphs
    """

    def __init__(self, dep_extractor, file_index, rank_dir):

        self.dep_extractor = dep_extractor
        self.file_index = file_index
        self.rank_dir = rank_dir

        self.legend = Legend()

        self.draw_legend = False

        self.graph = {}

    def render(self):
        if self.draw_legend:
            legend = self.legend.render()
            self.gv_graph.subgraph(legend)

    def __iter__(self):
        for node, edge in self.graph.items():
            yield node, edge

    def __getitem__(self, index):
        return self.graph[index]
