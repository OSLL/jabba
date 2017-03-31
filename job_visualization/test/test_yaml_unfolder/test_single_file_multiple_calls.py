
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization.yaml_unfolder import YamlUnfolder
from job_visualization.yaml_unfolder import convert_path

class TestSingleFileMultipleCalls(unittest.TestCase):

    def setUp(self):
        self.yaml_unfolder = YamlUnfolder('test/test_yaml_unfolder/test_data')

    def testSingleCall(self):
        test_dict = {
                'trigger-builds': [{
                    'project': ['name_1']
                 }]
        }

        calls = self.yaml_unfolder.get_calls_from_dict(test_dict, 'from_name', settings={'section': 'builders'})

        self.assertEquals(len(calls), 1)

    def testMultipleCalls(self):
        test_dict = {
                'trigger-builds': [{
                    'project': ['name_1', 'name_2', 'name_3']
                 }]
        }

        calls = self.yaml_unfolder.get_calls_from_dict(test_dict, 'from_name', settings={'section': 'builders'})

        self.assertEquals(len(calls), 3)

        self.assertEquals(calls[0].project_name, 'name_1')
        self.assertEquals(calls[1].project_name, 'name_2')
        self.assertEquals(calls[2].project_name, 'name_3')
