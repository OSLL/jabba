
import unittest
import sys
import os

from argparse import Namespace

sys.path.append("../")
sys.path.append("../../")

from config_parser import ConfigParser

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.test_data = 'test/test_config_parser/test_data/'

    def testLoadFile(self):
        parser = ConfigParser(self.test_data + 'config_1.yml')

        self.assertEquals(parser.args['yaml_root'], 'root-directory')
        self.assertEquals(parser.args['legend'], True)
        self.assertEquals(parser.args['call_parameters'], ['same-node', 'node-parameters'])

    def testMergeArgs(self):
        parser = ConfigParser(self.test_data + 'config_1.yml')

        args = Namespace(
            yaml_root = 'old_dir',
            call_parameters=[],
            call_graph=True
        )

        args = parser.merge_args(args)

        self.assertEquals(args.yaml_root, 'root-directory')
        self.assertEquals(args.legend, True)
        self.assertEquals(args.call_parameters, ['same-node', 'node-parameters'])
        self.assertEquals(args.call_graph, True)

