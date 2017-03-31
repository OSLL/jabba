
def parameters_present(options, **kwargs):
    synonyms = options['synonyms']
    call_graph = options['call_graph']

    result = _Result()

    for node, edges in call_graph._graph.items():
        for edge in edges:
            call_config = edge.call_config

            for req_key, req_value in kwargs.items():
                found = False

                for key, value in call_config.items():
                    if synonyms.are_synonyms(key, req_key):
                        found = True
                        break

                if not found:
                    result.add(node, edge, req_key)

    return result

class _Result:
    def __init__(self):
        self.failures = []

    def add(self, node, edge, key):
        self.failures.append((node, edge, key))

    def __str__(self):
        ret = "Parameters present test\n---------\n"

        if len(self.failures) == 0:
            ret += "OK"
            return ret

        for node, edge, key in self.failures:
            ret += "{} calls {} without the required parameter {} (or synonyms)\n".format(node, edge.call_config['project'], key)

        return ret
