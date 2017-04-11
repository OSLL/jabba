
import graphviz as gv

import collections

from .graph import Graph
from .edge import Edge

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

class IncludeGraph(Graph):

    def __init__(self, dep_extractor, file_index, rank_dir='left-right'):
        super(self.__class__, self).__init__(dep_extractor, file_index, rank_dir)

        self.graph = gv.Digraph(format='svg')

        if self.rank_dir == 'left-right':
            self.graph.body.extend(['rankdir=LR'])

        self.graph.body.extend(['size="8,5"'])

        self.active = False

        # Internal graph
        # Represented as hashmap (path -> edges) where edges is list of IncludeEdge objects
        self._graph = {}

        self.init_legend()

    def init_legend(self):
        self.legend.add_item('include', {'color': 'green'})
        self.legend.add_item('include-raw', {'color': 'red'})


    def add_node(self, name):
        if not self.active:
            return

        if name not in self._graph:
            self._graph[name] = []

    def add_edge(self, node_from, node_to, type):
        if not self.active:
            return


        self.add_node(node_from)
        self.add_node(node_to)

        if self.has_edge(node_from, node_to):
            return

        edges = self._graph[node_from]

        if type == 'include':
            color = graph_settings['edges']['include_color']
            label='<<B>include</B>>'
        elif type == 'include-raw':
            color = graph_settings['edges']['include_raw_color']
            label='<<B>include-raw</B>>'
        else:
            color = graph_settings['edges']['default_color']
            label=''

        edges.append(Edge(to=node_to, settings = {
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
            if edge.to == to_node:
                return True

        return False

    def unfold_file(self, path):
        yaml_config = self.file_index.unfold_yaml(path)

        self.unfold_config(path, yaml_config)

    def unfold_config(self, path, yaml_config):

        # Queue stores config files and who includes them
        q = [(path, None)]

        # To speed things up
        seen = set()

        while len(q) != 0:
            config_name, included_from = q.pop(0)

            if config_name in seen:
                continue

            seen.add(config_name)

            self.add_node(config_name)
            
            if included_from is not None:
                self.add_edge(included_from['name'], config_name, type=included_from['type'])

            includes = self.dep_extractor.get_includes(config_name)

            for include in includes:
                el = (include.path, {'name': config_name, 'type': include.type})
                q.append(el)

    def render(self, file_to):
        if not self.active:
            return

        for path in self._graph.keys():
            self.graph.node(path)

            for edge in self._graph[path]:
                self.graph.edge(path, edge.to, label=edge.settings['label'], color=edge.settings['color'])

        super(self.__class__, self).render()

        self.graph.render(file_to)
