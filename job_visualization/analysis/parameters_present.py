
import collections

from .result import Result

Error = collections.namedtuple('Error', ['caller', 'edge', 'parameter'])

def parameters_present(options, **kwargs):
    synonyms = options['synonyms']
    call_graph = options['call_graph']

    result = _Result()

    for node, edges in call_graph._graph.items():
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
        self.errors.append(Error(caller=node, edge=edge, parameter=parameter))

    def __str__(self):
        ret = "Parameters present test\n---------\n"

        if len(self.errors) == 0:
            ret += "OK"
            return ret

        for error in self.errors:
            caller = error.caller
            edge = error.edge
            parameter = error.parameter
            ret += "{} calls {} without the required parameter {} (or synonyms)\n".format(caller, edge.call_config['project'], parameter)

        return ret
