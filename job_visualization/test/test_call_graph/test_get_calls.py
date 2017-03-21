
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder

test_data = 'test/test_call_graph/test_data/'

class TestGetCalls(unittest.TestCase):

    def setUp(self):
        yaml_root = test_data
        self.yaml_unfolder = YamlUnfolder(root=yaml_root)

    def testEmpty(self):
        calls = self.yaml_unfolder.get_calls(test_data + 'empty.yml')

        print(calls)

        self.assertEqual(len(calls), 0)

    def testSingleCall(self):
        calls = self.yaml_unfolder.get_calls(test_data + 'single_call.yml')

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].project_name, 'empty')

    def testMultipleCalls(self):
        calls = self.yaml_unfolder.get_calls(test_data + 'multiple_calls.yml')

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].project_name, 'empty')
        self.assertEqual(calls[1].project_name, 'empty_2')

if __name__ == "__main__":
    unittest.main()
