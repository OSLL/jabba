
import os

import yaml_unfolder

class ConfigParser(yaml_unfolder.YamlUnfolder):
    default_config = '.jjv_config.yml'

    def __init__(self, config):
        super(self.__class__, self).__init__(root='.')

        self.include_graph.active = False
        self.call_graph.active = False

        if os.path.exists(config):
            self.args = self.unfold_yaml(config)
        else:
            if config != ConfigParser.default_config:
                raise IOError("No such file {}".format(config))

            self.args = {}

    def merge_args(self, args):
        for arg, value in self.args.items():
            setattr(args, arg, value)

        return args
