
import collections

from .result import Result

Error = collections.namedtuple('Error', ['caller', 'edge', 'parameter'])

class Error:
    def __init__(self, caller, edge, parameter):
        self.caller = caller
        self.edge = edge
        self.parameter = parameter

    def __str__(self):
        return "{} calls {} without the required parameter {} (or synonyms)\n".format(self.caller, self.edge.settings['project'], self.parameter)

def parameters_present(options, **kwargs):
    """
    Analysis function
    Check whether all calls contain a given parameters or their synonyms
    """
    synonyms = options['synonyms']
    call_graph = options['call_graph']

    result = _Result()

    for node, edges in call_graph:
        for edge in edges:
            call_config = edge.settings

            for req_param, req_value in kwargs.items():
                found = False

                for param, value in call_config.items():
                    if synonyms.are_synonyms(param, req_param):
                        found = True
                        break

                if not found:
                    result.add(node, edge, req_param)

    return result

class _Result(Result):
    def add(self, node, edge, parameter):
        self.results.append(Error(caller=node, edge=edge, parameter=parameter))
        self.header = "Parameters present test"

    def __str__(self):
        ret = self.format_header()

        if len(self.results) == 0:
            ret += "OK"
            return ret

        for error in self.results:
            ret += str(error)

        return ret
