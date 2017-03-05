
import graphviz as gv
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


class IncludeGraph:

    def __init__(self):
        self.graph = gv.Digraph(format='svg')
        self.graph.body.extend(['rankdir=LR', 'size="8,5"'])

        self.active = False

        self.include_list = []

    def add_node(self, text):
        if self.active:
            self.graph.node(text)

    def add_edge(self, node_from, node_to, label, color):
        if color == 'include_color':
            color = graph_settings['edges']['include_color']
        elif color == 'include_raw_color':
            color = graph_settings['edges']['include_raw_color']
        else:
            color = graph_settings['edges']['default_color']

        self.graph.edge(node_from, node_to, label=label, color=color)

    def add_edge_from_last_node(self, text, label, color):
        if self.active:
            self.add_edge(self.include_list[-1], text, label=label, color=color)

    def add_to_list(self, v):
        if self.active:
            self.include_list.append(v)

    def pop_from_list(self):
        if self.active:
            return self.include_list.pop()

    def render(self, file_to):
        if self.active:
            self.graph.render(file_to)
