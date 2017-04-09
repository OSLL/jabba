
from .result import Result

def cyclic_deps(options, **kwargs):
    include_graph = options['include_graph']
    call_graph = options['call_graph']

    include_result = _IncludeResult(cyclic_test(include_graph))
    call_result = _CallResult(cyclic_test(call_graph))

    return _Result(include_result, call_result)

def cyclic_test(graph):
    cycles = []

    visited = set()

    for node, edges in graph._graph.items():
        if node not in visited:
            cycle = find_cycle(graph._graph, node, visited)

            if cycle is not None:
                cycles.append(cycle)

    return cycles

# Find one cycle that can be reached from the node
def find_cycle(graph, node, visited):
    current_stack = []

    return _find_cycle(graph, node, visited, current_stack)

# Simple DFS
# Current stack keeps path from the root to the current node
def _find_cycle(graph, node, visited, current_stack):
    if node in current_stack:
        return unwrap_cycle(node, current_stack)

    visited.add(node)

    current_stack.append(node)

    for edge in graph[node]:
        cycle = _find_cycle(graph, edge.to, visited, current_stack)

        if cycle is not None:
            return cycle

    current_stack.pop()

    return None

def unwrap_cycle(node, stack):
    cycle = [node]

    prev_node = stack.pop()

    while prev_node != node:
        cycle.append(prev_node)

        prev_node = stack.pop()

    cycle.append(node)

    cycle = cycle[::-1]

    return cycle

class _IncludeResult(Result):
    def __init__(self, cycles):
        super(self.__class__, self).__init__()

        for cycle in cycles:
            self.add(cycle)

    def __str__(self):
        return str(self.errors)

class _CallResult(Result):
    def __init__(self, cycles):

        super(self.__class__, self).__init__()

        for cycle in cycles:
            self.add(cycle)

    def __str__(self):
        return str(self.errors)


class _Result(Result):
    def __init__(self, include_result, call_result):
        self.include_result = include_result
        self.call_result = call_result

    def is_ok(self):
        return self.include_result.is_ok() and self.call_result.is_ok()

    def __str__(self):
        return "{}\n{}".format(self.include_result, self.call_result)
