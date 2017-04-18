
import os

from . import yaml_unfolder
from . import synonym_parser

class ConfigParser(yaml_unfolder.YamlUnfolder):
    default_config = '.jjv_config.yml'

    def __init__(self, config, verbose=0):
        yaml_unfolder.YamlUnfolder.__init__(self, root='.', verbose=0)
        #super(self.__class__, self).__init__(root='.')

        self.verbose = verbose

        self.include_graph.active = False
        self.call_graph.active = False

        if os.path.exists(config):
            if self.verbose == 2:
                print("Using config {}".format(config))

            v = self.unfold_yaml(config)
            self.args = self.unfold_yaml(config)['config']
        else:
            if config != ConfigParser.default_config:
                raise IOError("No such file {}".format(config))

            self.args = {}

    def merge_args(self, args):
        for arg, value in self.args.items():
            if arg == 'synonyms':
                value = synonym_parser.parse_from_array(value)

            setattr(args, arg, value)

        return args
