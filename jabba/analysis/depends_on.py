
from .result import Result

from ..graphs.include_graph import IncludeGraph

def depends_on(options, **kwargs):
    include_graph = options['include_graph']

    if 'graph' in kwargs:
        name = kwargs['graph']
        del kwargs['graph']

        dep_graph = build_dependency_graph(include_graph, **kwargs)

        dep_graph.render(name)

        print("Rendered graph at {}".format(name))

        return _Result("Rendered dep graph at {}".format(name))

    else:
        dep_graph = build_dependency_graph(include_graph, **kwargs)

        for node, edges in dep_graph:
            print(node)

    return _Result("")

def build_dependency_graph(include_graph, **kwargs):

    inverted_graph = invert_graph(include_graph)

    depends_on_files = get_files_depend_on(inverted_graph, **kwargs)

    inverted_graph.graph = {node: edges for node, edges in inverted_graph if node in depends_on_files}

    return invert_graph(inverted_graph)

def invert_graph(include_graph):
    """
    TODO: move this to include_graph 
    """

    file_index = include_graph.file_index
    dep_extractor = include_graph.dep_extractor

    inverted_graph = IncludeGraph(file_index, dep_extractor)
    inverted_graph.active = True

    for node, edges in include_graph:
        inverted_graph.add_node(node)

        for edge in edges:
            inverted_graph.add_edge(edge.to, node, edge.settings['type'])

    return inverted_graph

def get_files_depend_on(include_graph, **kwargs):
    files = set()

    for config in kwargs:
        files = files.union(_get_files_depend_on(include_graph, config))

    return files

def _get_files_depend_on(include_graph, config):
    files = {config}

    for edge in include_graph[config]:
        files.add(edge.to)

        files = files.union(_get_files_depend_on(include_graph, edge.to))

    return files

def _Result(Result):
    def __init__(self, mess):
        self.mess = mess
    def __str__(self):
        return mess

