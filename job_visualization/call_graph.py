
import graphviz as gv

import collections
from file_data import FileData

CallEdge = collections.namedtuple('CallEdge', ['project_name', 'call_confing'])

class CallGraph:
    '''
    Class for manipulating call graph
    Stores all graph with file configs for further analysis
    '''
 
    def __init__(self, get_calls, unfold):
        self.active = False
        self.get_calls = get_calls
        self.unfold = unfold

        # Graphviz graph
        self.graph = gv.Digraph(format='svg')
        self.graph.body.extend(['rankdir=LR', 'size="8,5"'])

        self.call_list = []

        # Internal graph represented as dict mapping node names to the list of its edges
        # Edge is represented as CallEdge
        self._graph = {}
        # Configs for files
        self._configs = {}
        # Roots are the jobs that were passed to `unfold_file` method
        # We need to treat them differently
        self._roots = set()

    def add_call_object(self, call_object):
        self.add_node(call_object.project_name, call_object.project_config)
        self.add_edge(call_object.caller_name, call_object.project_name, call_object.call_config)

    def add_node(self, name, project_config, is_root=False):
        if name not in self._graph:
            self._graph[name] = []
            self._configs[name] = project_config
            
        if is_root:
            self._roots.add(name)

    def add_edge(self, from_name, to_name, call_config):
        if not self.has_edge(from_name, to_name):
            call_edge = CallEdge(to_name, call_config)
            self._graph[from_name].append(call_edge)

    def has_edge(self, from_name, to_name):

        try:
            edges = self._graph[from_name]
        except KeyError:
            return False

        for edge in edges:
            if edge.project_name == to_name:
                return True
        else:
            return False

    def unfold_file(self, path):
        yaml_config = self.unfold(path)
        name = yaml_config[0]['job']['name']

        self.add_node(name, FileData(yaml=yaml_config, path=path), is_root=True)

        # Queue
        q = []

        q.extend(self.get_calls(yaml_config, name))

        while len(q) != 0:
            call = q.pop(0)

            self.add_call_object(call)

            calls = self.get_calls(call.project_config.yaml, call.project_name)

            for c in calls:
                if not self.has_edge(c.caller_name, c.project_name):
                    q.append(c)

    def render(self, path):
        for node in self._roots:
            self.render_node(node, color='red')

        for node in self._graph.keys():
            if node not in self._roots:
                self.render_node(node)

        self.graph.render(path)

    def render_node(self, name, color='black'):
        self.graph.node(self.get_path_from_name(name), color=color)

        edges = self._graph[name]

        for edge in edges:
            self.graph.edge(self.get_path_from_name(name), self.get_path_from_name(edge.project_name), label='call')

    def get_path_from_name(self, name):
        return self._configs[name].path
