
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba import Analyzer
from jabba import SynonymSet
from jabba.yaml_unfolder import YamlUnfolder

class TestParametersPresent(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_analysis/parameters_present/'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testParametersPresent(self):
        synonyms = SynonymSet()
        synonyms.add_set({'same-node', 'node-parameters'})

        arguments = ["parameters_present:same-node"]

        analyzer = Analyzer(root=self.test_data, synonyms=synonyms, arguments=arguments, file_index=self.yaml_unfolder.file_index, dep_extractor=self.yaml_unfolder.dep_extractor)
        analyzer.run()

        self.assertEqual(len(analyzer.results), 1)

        result = analyzer.results[0]

        self.assertEqual(result.results[0].caller, 'publisher')
        self.assertEqual(result.results[0].edge.to, 'test')
        self.assertEqual(result.results[0].parameter, 'same-node')
