
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder

test_data = 'test/test_include_graph/test_data/'
test_refs = 'test/test_include_graph/test_refs/'


class TestIncludeGraph(unittest.TestCase):

    def setUp(self):
        self.yaml_root = os.getcwd() + '/' + test_data
        self.yaml_unfolder = YamlUnfolder(root=self.yaml_root)
        self.yaml_unfolder.include_graph.active = True

    def testExample1(self):
        self.run_test_for_file('test.yml')

    def run_test_for_file(self, main_file):
        '''
        Unfolds main_file, renders it. Finds ref graph for it and compares generated graph with ref graph
        If ref graph is not found, generate it
        '''

        unfolded_yaml = self.yaml_unfolder.unfold_yaml(test_data + main_file, is_root=True)
        export_name = self.yaml_root + main_file + '_include'
        self.yaml_unfolder.include_graph.render(export_name)

        with open(test_data + main_file + '_include', 'r') as test_file:

            try:
                with open(test_refs + main_file + '_include', 'r') as ref_file:
                    ref_graph = ref_file.read()
                    test_graph = test_file.read()

                    self.assertEquals(ref_graph, test_graph)
            except IOError:
                print('Generating new ref graph for ' + test_data + main_file)

                with open(test_refs + main_file + '_include', 'w+') as ref_file:
                    test_graph = test_file.read()
                    ref_file.write(test_graph)

                    self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
