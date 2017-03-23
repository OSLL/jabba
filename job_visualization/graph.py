
import graphviz as gv

from legend import Legend

class Graph(object):
    """
    Abstract class for render graphs
    """

    def __init__(self):
        self.legend = Legend()

        self.draw_legend = False

    def render(self):
        if self.draw_legend:
            legend = self.legend.render()
            self.graph.subgraph(legend)
