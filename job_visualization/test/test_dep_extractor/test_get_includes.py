
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization import FileIndex, DepExtractor

test_data = 'test/test_call_graph/test_data/'

class TestGetIncludes(unittest.TestCase):

    def setUp(self):
        self.file_index = FileIndex(test_data)
        self.file_index.load_files(test_data)

        self.dep_extractor = DepExtractor(self.file_index)

    def testEmpty(self):
        includes = self.dep_extractor.get_includes(test_data + 'empty.yml')

        self.assertEqual(len(includes), 0)

    def testSingleCall(self):
        includes = self.dep_extractor.get_includes(test_data + 'single_call.yml')

        self.assertEqual(len(includes), 1)
        print(includes)


if __name__ == "__main__":
    unittest.main()
