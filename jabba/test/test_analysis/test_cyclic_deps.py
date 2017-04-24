
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba import Analyzer
from jabba.yaml_unfolder import YamlUnfolder

class TestParametersPresent(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_analysis/cyclic_deps/'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testFindCycle(self):

        arguments = ['cyclic_deps']

        analyzer = Analyzer(root=self.test_data, arguments=arguments, file_index=self.yaml_unfolder.file_index, dep_extractor=self.yaml_unfolder.dep_extractor)
        analyzer.run()

        self.assertEqual(len(analyzer.results), 1)

        self.assertEqual(analyzer.results[0].errors[0], ['job3', 'job1', 'job2', 'job3'])

