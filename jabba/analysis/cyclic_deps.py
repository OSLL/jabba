from .result import Result

def cyclic_deps(options, **kwargs):
    """
    Analysis function
    Check whether there are any cyclic dependencies in a call graph
    Cyclic dependencies in include graph are prevented at a parsing stage with FileIndex
    """
    call_graph = options['call_graph']

    call_result = _CallResult(cyclic_test(call_graph))
    
    return call_result


def cyclic_test(graph):
    cycles = []

    visited = set()

    for node, edges in graph:
        if node not in visited:

            cycle = find_cycle(graph, node, visited)

            if cycle is not None:
                cycles.append(cycle)

    cycles = remove_repetitions(cycles)

    return cycles

# Find one cycle that can be reached from the node
def find_cycle(graph, node, visited):
    current_stack = []

    return _find_cycle(graph, node, visited, current_stack)

# Simple DFS
# Current stack keeps path from the root to the current node
def _find_cycle(graph, node, visited, current_stack):
    visited.add(node)

    if node in current_stack:
        return unwrap_cycle(node, current_stack)

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

def remove_repetitions(cycles):
    seen = set()

    ret = []

    for cycle in cycles:
        cycle_set = frozenset(cycle)

        if cycle_set not in seen:
            ret.append(cycle)
            seen.add(cycle_set)

    return ret

def format_cycle(cycle):
    return " -> ".join(cycle)

class _CallResult(Result):
    def __init__(self, cycles):

        super(self.__class__, self).__init__()

        for cycle in cycles:
            self.add(cycle)

    def __str__(self):
        ret = "\nCyclic dependencies in call graph test\n-------------\n"

        if self.is_ok():
            ret += "OK"

            return ret

        for error in self.errors:
            ret += "Found cycle {}\n".format(format_cycle(error))

        return ret
