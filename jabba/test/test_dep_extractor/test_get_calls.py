
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba import FileIndex, DepExtractor

test_data = 'test/test_call_graph/test_data/'

class TestGetCalls(unittest.TestCase):

    def setUp(self):
        self.file_index = FileIndex(test_data)
        self.file_index.load_files(test_data)

        self.dep_extractor = DepExtractor(self.file_index)

    def testEmpty(self):
        calls = self.dep_extractor.get_calls('empty')

        self.assertEqual(len(calls), 0)

    def testSingleCall(self):
        calls = self.dep_extractor.get_calls('single')

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].to, 'empty')

    def testMultipleCalls(self):
        calls = self.dep_extractor.get_calls('multiple')

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].to, 'empty')
        self.assertEqual(calls[1].to, 'empty_2')

if __name__ == "__main__":
    unittest.main()
