
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba.yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest

class TestCallDisplay(GraphTest):

    def setUpYamlUnfolder(self, main_file):
        export_name = self.yaml_root + main_file + self.ext

        self.yaml_unfolder.call_graph.unfold_file(self.test_data + main_file)
        self.yaml_unfolder.call_graph.render(export_name)


    def setUp(self):
        self.test_data = 'test/test_call_graph/test_data/'
        self.test_refs = 'test/test_call_graph/test_refs/'

        self.yaml_root = self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.ext = '_call'

        self.yaml_unfolder.call_graph.call_parameters = {'same-node'}

    def testNoneDisplay(self):
        self.yaml_unfolder.call_graph.call_display = 'none'
        self.run_test_for_file('params_call_none.yml')

    def testTextDisplay(self):
        self.yaml_unfolder.call_graph.call_display = 'text'
        self.run_test_for_file('params_call_text.yml')

    def testEdgeDisplay(self):
        self.yaml_unfolder.call_graph.call_display = 'edge'
        self.run_test_for_file('params_call_edge.yml')

    def testNoParametersDisplay(self):
        self.yaml_unfolder.call_graph.call_parameters = {}
        self.run_test_for_file('no_params.yml')

    def testMultipleParamsDisplay(self):
        self.yaml_unfolder.call_graph.call_parameters = {'same-node', 'node-parameters'}
        self.run_test_for_file('multiple_params.yml')

    def testCallOrder(self):
        self.yaml_unfolder.call_graph.call_parameters = {'call-order'}
        self.run_test_for_file('order_call.yml')

if __name__ == "__main__":
    unittest.main()
