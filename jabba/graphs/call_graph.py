
import graphviz as gv

import collections
from ..file_data import FileData

from .graph import Graph
from .edge import Edge

from ..util import convert_path

class CallGraph(Graph):
    '''
    Class for manipulating call graph
    Stores all graph with file configs for further analysis
    '''
 
    def __init__(self, dep_extractor, file_index, rank_dir='left-right'):

        super(self.__class__, self).__init__(dep_extractor, file_index, rank_dir)

        self.active = False

        # Graphviz graph
        self.gv_graph = gv.Digraph(format='svg')

        if self.rank_dir == 'left-right':
            self.gv_graph.body.extend(['rankdir=LR'])

        self.gv_graph.body.extend(['size="8,5"'])

        # Internal graph represented as dict mapping node names to the list of its edges
        # Edge is represented as CallEdge
        self.graph = {}
        # Configs for files
        self._configs = {}
        # Roots are the jobs that were passed to `unfold_file` method
        # We need to treat them differently
        self._roots = set()

        # How to display call information
        # none - don't display
        # text - display as plain text above the edge
        # edge - display as node embeded in the edge
        self.call_display = 'text'

        # Which parameters to display on call edges
        self.call_parameters = {}

        self.init_legend()

    def init_legend(self):
        self.legend.add_item('publishers', {'color': 'green'})
        self.legend.add_item('builders', {'color': 'blue'})

    def add_call_object(self, call_object):
        self.add_node(call_object.to, call_object.project_config)
        self.add_edge(call_object.caller_name, call_object.to, call_object.settings)

    def add_node(self, name, project_config, is_root=False):
        if name not in self.graph:
            self.graph[name] = []
            self._configs[name] = project_config
            
        if is_root:
            self._roots.add(name)

    def add_edge(self, from_name, to_name, settings):
        if not self.has_edge(from_name, to_name):
            call_edge = Edge(to=to_name, settings=settings)
            self.graph[from_name].append(call_edge)

    def has_edge(self, from_name, to_name):

        try:
            edges = self.graph[from_name]
        except KeyError:
            return False

        for edge in edges:
            if edge.to == to_name:
                return True
        else:
            return False

    def unfold_file(self, path):
        """
        Adds given file info graph
        """
        yaml_config = self.file_index.unfold_yaml(path)

        self.unfold_config(path, yaml_config)

    def unfold_config(self, path, yaml_config):
        try:
            name = self.file_index.get_job_name(yaml_config)
        except KeyError:
            print("Warning: building call graph for not a job {}".format(yaml_config))
            return

        self.add_node(name, FileData(yaml=yaml_config, path=path), is_root=True)

        # Queue
        q = []

        q.extend(self.dep_extractor.get_calls(name))

        # What is the order of current call in call config
        current_order = 1

        # What is the name of the last caller
        # If the caller is the same, that means we are processing the call from the same caller
        # so we need to increase current_call
        current_caller = ''

        while len(q) != 0:
            call = q.pop(0)

            if call.caller_name != current_caller:
                current_order = 1
                current_caller = call.caller_name
            else:
                current_order += 1

            call.settings['call-order'] = current_order

            self.add_call_object(call)

            calls = self.dep_extractor.get_calls(call.to)

            for c in calls:
                if not self.has_edge(c.caller_name, c.to):
                    q.append(c)

    def render(self, path):
        for node in self._roots:
            self.render_node(node, color='red')

        for node in self.graph.keys():
            if node not in self._roots:
                self.render_node(node)

        # Because of the way GraphViz position clusters
        # we have to draw the base graph after the main graph
        super(self.__class__, self).render()

        self.gv_graph.render(path)


    def render_node(self, name, color='black'):
        self.gv_graph.node(self.get_path_from_name(name), color=color)

        edges = self.graph[name]

        for edge in edges:
            edge_settings = self.get_settings(edge)

            if self.call_display == 'none':
                self.render_simple_edge(name, edge, edge_settings)
            elif self.call_display == 'text':
                self.render_edge_with_label(name, edge, edge_settings)
            elif self.call_display == 'edge':
                self.render_edge_with_node_label(name, edge, edge_settings)
            else:
                raise Exception('Incorrect call display option {}'.format(self.call_display))

    def render_simple_edge(self, name, edge, edge_settings, label="call"):
        """
        Render edge without label
        """
        self.gv_graph.edge(self.get_path_from_name(name), self.get_path_from_name(edge.to), label=label, **edge_settings)

    def render_edge_with_label(self, name, edge, edge_settings):
        """
        Render edge with label as text
        """
        props_to_display = self.extract_props(edge.settings)

        label = '<'

        for prop, value in props_to_display.items():
            label += self.get_label(prop, value)
            label += "<BR/>"

        label += '>'

        self.gv_graph.edge(self.get_path_from_name(name), self.get_path_from_name(edge.to), label=label, **edge_settings)

    def render_edge_with_node_label(self, name, edge, edge_settings):
        """
        Render edge with label as separate node
        """
        props_to_display = self.extract_props(edge.settings)

        label = '<'
        label += "|".join(self.get_label(prop, value) for prop, value in props_to_display.items()) 
        label += '>'

        edge_node_name = "{}-{}".format(name, edge.to)

        self.gv_graph.node(edge_node_name, label=label, shape="record")

        self.gv_graph.edge(self.get_path_from_name(name), edge_node_name, arrowhead="none", **edge_settings)
        self.gv_graph.edge(edge_node_name, self.get_path_from_name(edge.to), **edge_settings)

    def get_label(self, prop, value):
        """
        Format label
        If value is missing, label will be colored red
        """
        if value is None:
            return '{}: <FONT color="red">{}</FONT>'.format(prop, "not set")
        else:
            return "{}:{}".format(prop, value)

    def get_settings(self, edge):
        """
        Get render settings for edge
        """
        if 'section' not in edge.settings:
            return {}

        if edge.settings['section'] == 'publishers':
            return {'color': 'green'}

        if edge.settings['section'] == 'builders':
            return {'color': 'blue'}

        return {}

    def extract_props(self, settings):
        '''
        Extract all valuable properties to be displayed
        '''

        props = {}

        for param in self.call_parameters:
            if param in settings:
                props[param] = settings[param]
            else:
                props[param] = None

        return props

    def should_display_prop(self, prop):
        return prop in self.call_parameters

    def get_path_from_name(self, name):
        path = self._configs[name].path
        return convert_path(path)
