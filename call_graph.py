
import graphviz as gv

import collections

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

    def add_call_object(self, call_object):
        self.add_node(call_object.project_name, call_object.project_config)
        self.add_edge(call_object.caller_name, call_object.project_name, call_object.call_config)

    def add_node(self, name, project_config):
        if name not in self._graph:
            self._graph[name] = []
            self._configs[name] = project_config

    def add_edge(self, from_name, to_name, call_config):
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

        self.add_node(name, yaml_config)

        # Queue
        q = []

        q.extend(self.get_calls(yaml_config, name))

        while len(q) != 0:
            call = q.pop(0)

            self.add_call_object(call)

            calls = self.get_calls(call.project_config, call.project_name)

            for c in calls:
                if not self.has_edge(c.caller_name, c.project_name):
                    q.append(c)

    def render(self, path):
        for node in self._graph:
            for edge in self._graph[node]:
                print("{} --> {}".format(node, edge.project_name))
