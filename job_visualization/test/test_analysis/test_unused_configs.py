
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization import Analyzer
from job_visualization import FileIndex
from job_visualization import SynonymSet
from job_visualization.yaml_unfolder import YamlUnfolder

class TestUnusedConfigs(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_analysis/unused_configs/'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testUnusedConfigs(self):

        arguments = ["unused_configs"]

        analyzer = Analyzer(root=self.test_data, arguments=arguments, file_index=self.yaml_unfolder.file_index, dep_extractor=self.yaml_unfolder.dep_extractor)
        analyzer.run()

        result = analyzer.results[0]

        self.assertEquals(len(result.errors), 2)

        self.assertEquals(result.errors[0], 'test/test_analysis/unused_configs/unused_1.yaml')
        self.assertEquals(result.errors[1], 'test/test_analysis/unused_configs/unused_2.yml')
