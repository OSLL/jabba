
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba.yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest


class TestLegend(GraphTest):

    def setUpYamlUnfolder(self, main_file):
        export_name = self.yaml_root + main_file + self.ext

        self.yaml_unfolder.call_graph.unfold_file(self.test_data + main_file)
        self.yaml_unfolder.call_graph.render(export_name)

    def setUp(self):
        self.test_data = 'test/test_graph/test_data/'
        self.test_refs = 'test/test_graph/test_refs/'

        self.yaml_root = self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.yaml_unfolder.call_graph.draw_legend = True

        self.ext = '_call'

    def testLegend(self):
        self.run_test_for_file('test_legend.yml')

if __name__ == "__main__":
    unittest.main()
