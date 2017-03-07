
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest



class TestIncludeGraph(GraphTest):

    def setUpYamlUnfolder(self, main_file):
        export_name = self.yaml_root + main_file + self.ext

        self.yaml_unfolder.unfold_yaml(self.test_data + main_file, is_root=True)
        self.yaml_unfolder.include_graph.render(export_name)

    def setUp(self):
        self.test_data = 'test/test_include_graph/test_data/'
        self.test_refs = 'test/test_include_graph/test_refs/'

        self.yaml_root = os.getcwd() + '/' + self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.yaml_unfolder.include_graph.active = True
        self.ext = '_include'

    def testExample1(self):
        self.run_test_for_file('test.yml')

    def testExample2(self):
        self.run_test_for_file('example2-test.yml')

if __name__ == "__main__":
    unittest.main()
