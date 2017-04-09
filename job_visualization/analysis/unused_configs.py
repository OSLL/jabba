
from .result import Result
from os.path import basename

def unused_configs(options, **kwargs):

    include_graph = options['include_graph']
    call_graph = options['call_graph']

    used_configs = get_used_configs(include_graph, call_graph)

    result = _Result()

    for config, edges in include_graph._graph.items():
        if config not in used_configs and is_not_hidden(config): 
            result.add(config)

    return result

def get_used_configs(include_graph, call_graph):
    # Call graphs contains all the jobs. Assume all the jobs are used
    configs = set()

    for job, edges in call_graph._graph.items():
        path_to_job = call_graph.get_path_from_name(job)
        configs.add(path_to_job)

    for node, edges in include_graph._graph.items():
        for edge in edges:
            configs.add(edge.to)

    return configs

def is_not_hidden(config):
    return not basename(config).startswith('.')

class _Result(Result):

    def __init__(self):
        self.errors = []

    def add(self, config):
        self.errors.append(config)

    def __str__(self):
        ret = "Unused configs test\n---------\n"

        if len(self.errors) == 0:
            ret += "OK"
            return ret

        for config in self.errors:
            ret += "{} is not used\n".format(config)

        return ret


