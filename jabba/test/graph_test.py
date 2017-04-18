
import unittest
import abc
import os

class GraphTest(unittest.TestCase):

    def run_test_for_file(self, main_file):
        '''
        Unfolds main_file, renders it. Finds ref graph for it and compares generated graph with ref graph
        If ref graph is not found, generate it
        '''

        self.clean(main_file)

        self.setUpYamlUnfolder(main_file)

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


    def clean(self, main_file):
        try:
            os.remove(self.test_data + main_file + self.ext)
            os.remove(self.test_data + main_file + self.ext + '.svg')
        except OSError:
            # Files were not created yet
            pass

    @abc.abstractmethod
    def setUpYamlUnfolder(self, main_file):
        pass
