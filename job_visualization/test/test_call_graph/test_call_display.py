
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from test_call_graph import TestCallGraph

class TestCallDisplay(TestCallGraph):

    def setUp(self):
        super(TestCallDisplay, self).setUp()

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

if __name__ == "__main__":
    unittest.main()
