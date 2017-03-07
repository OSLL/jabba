
import unittest

class GraphTest(unittest.TestCase):

    def run_test_for_file(self, main_file):
        '''
        Unfolds main_file, renders it. Finds ref graph for it and compares generated graph with ref graph
        If ref graph is not found, generate it
        '''

        export_name = self.yaml_root + main_file + self.ext

        if self.type == 'include_graph':
            unfolded_yaml = self.yaml_unfolder.unfold_yaml(self.test_data + main_file, is_root=True)
            self.yaml_unfolder.include_graph.render(export_name)
        elif self.type == 'call_graph':
            self.yaml_unfolder.call_graph.unfold_file(self.test_data + main_file)
            self.yaml_unfolder.call_graph.render(export_name)
        else:
            raise Exception("Unknown graph type {}".format(self.type))

        with open(self.test_data + main_file + self.ext, 'r') as test_file:

            try:
                with open(self.test_refs + main_file + self.ext, 'r') as ref_file:
                    ref_graph = ref_file.read()
                    test_graph = test_file.read()

                    self.assertEquals(ref_graph, test_graph)
            except IOError:
                print('Generating new ref graph for ' + self.test_data + main_file)

                with open(self.test_refs + main_file + self.ext, 'w+') as ref_file:
                    test_graph = test_file.read()
                    ref_file.write(test_graph)

                    self.assertTrue(True)


