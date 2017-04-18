
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization.yaml_unfolder import YamlUnfolder
from test.graph_test import GraphTest


class TestRankDir(GraphTest):
    def setUpYamlUnfolder(self, main_file):
        export_name = self.yaml_root + main_file + self.ext

        self.yaml_unfolder.call_graph.unfold_file(self.test_data + main_file)
        self.yaml_unfolder.call_graph.render(export_name)

    def setUp(self):
        self.test_data = 'test/test_graph/test_data/'
        self.test_refs = 'test/test_graph/test_refs/'

        self.yaml_root = self.test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root, rank_dir='up-down')
        self.yaml_unfolder.call_graph.draw_legend = True

        self.ext = '_call'

    def testUpDown(self):
        self.run_test_for_file('test_rank_dir_ud.yml')


