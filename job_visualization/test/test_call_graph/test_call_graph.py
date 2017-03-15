
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest

class TestCallGraph(GraphTest):

    def setUpYamlUnfolder(self, main_file):
        export_name = self.yaml_root + main_file + self.ext

        self.yaml_unfolder.call_graph.unfold_file(self.test_data + main_file)
        self.yaml_unfolder.call_graph.render(export_name)

    def setUp(self):
        self.test_data = 'test/test_call_graph/test_data/'
        self.test_refs = 'test/test_call_graph/test_refs/'

        self.yaml_root = self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.yaml_unfolder.include_graph.active = True
        self.ext = '_call'

    def testExample1(self):
        self.run_test_for_file('multiple_calls.yml')

if __name__ == "__main__":
    unittest.main()
