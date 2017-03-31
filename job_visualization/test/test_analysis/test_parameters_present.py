
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization import Analyzer
from job_visualization import FileIndex
from job_visualization import SynonymSet
from job_visualization.yaml_unfolder import YamlUnfolder

class TestParametersPresent(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_analysis/parameters_present/'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testParametersPresent(self):
        file_index = FileIndex(self.test_data, unfold=self.yaml_unfolder.unfold_yaml)

        synonyms = SynonymSet()
        synonyms.add_set({'same-node', 'node-parameters'})

        arguments = ["parameters_present:same-node"]

        analyzer = Analyzer(root=self.test_data, synonyms=synonyms, arguments=arguments, file_index=file_index)
        analyzer.run()

        result = analyzer.results[0]

        self.assertEqual(result.errors[0].caller, 'publisher')
        self.assertEqual(result.errors[0].edge.project_name, 'test')
        self.assertEqual(result.errors[0].parameter, 'same-node')
