
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest



class TestIncludeGraph(GraphTest):

    def setUp(self):
        self.test_data = 'test/test_include_graph/test_data/'
        self.test_refs = 'test/test_include_graph/test_refs/'

        self.yaml_root = self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.yaml_unfolder.include_graph.active = True
        self.ext = '_include'

        self.type = 'include_graph'

    def testExample1(self):
        self.run_test_for_file('test.yml')

if __name__ == "__main__":
    unittest.main()
