
import graphviz as gv

import collections

from graph import Graph

'''
All visual settings we want to specify for include graph
'''
graph_settings = {
    'edges': {
        'include_color': 'green',
        'include_raw_color': 'red',
        'default_color': 'black'
    }
}

# path - path that is passed to !include or !include_raw
# settings - settings of the edge (label, color)
IncludeEdge = collections.namedtuple('IncludeEdge', ['path', 'settings'])

class IncludeGraph(Graph):

    def __init__(self, rank_dir='left-right'):
        super(self.__class__, self).__init__(rank_dir)

        self.graph = gv.Digraph(format='svg')

        if self.rank_dir == 'left-right':
            self.graph.body.extend(['rankdir=LR'])

        self.graph.body.extend(['size="8,5"'])

        self.active = False

        self.include_list = []

        # Internal graph
        # Represented as hashmap (path -> edges) where edges is list of IncludeEdge objects
        self._graph = {}

    def add_node(self, name):
        if not self.active:
            return

        if name not in self._graph:
            self._graph[name] = []

    def add_edge(self, node_from, node_to, label, color):
        if not self.active:
            return

        self.add_node(node_from)
        self.add_node(node_to)

        if self.has_edge(node_from, node_to):
            return

        edges = self._graph[node_from]

        if color == 'include_color':
            color = graph_settings['edges']['include_color']
        elif color == 'include_raw_color':
            color = graph_settings['edges']['include_raw_color']
        else:
            color = graph_settings['edges']['default_color']

        edges.append(IncludeEdge(path=node_to, settings = {
            'label': label,
            'color': color
        }))

    def has_edge(self, from_node, to_node):
        if not self.active:
            return False

        if not from_node in self._graph:
            return False

        edges = self._graph[from_node]

        for edge in edges:
            if edge.path == to_node:
                return True

        return False

    def add_edge_from_last_node(self, text, label, color):
        if not self.active:
            return

        self.add_edge(self.include_list[-1], text, label=label, color=color)

    def add_to_list(self, v):
        if self.active:
            self.include_list.append(v)

    def pop_from_list(self):
        if not self.active:
            return

        return self.include_list.pop()

    def render(self, file_to):
        if not self.active:
            return

        super(self.__class__, self).render()

        for path in self._graph.keys():
            self.graph.node(path)

            for edge in self._graph[path]:
                self.graph.edge(path, edge.path, label=edge.settings['label'], color=edge.settings['color'])

        self.graph.render(file_to)

