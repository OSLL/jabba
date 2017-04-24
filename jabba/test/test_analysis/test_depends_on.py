
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba import Analyzer
from jabba.yaml_unfolder import YamlUnfolder

class TestParametersPresent(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_analysis/depends_on/'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testDependsOn(self):
        arguments = ['depends_on:' + self.test_data + "c.yml" + ":" +  self.test_data + "e.yml"]

        analyzer = Analyzer(root=self.test_data, arguments=arguments, file_index=self.yaml_unfolder.file_index, dep_extractor=self.yaml_unfolder.dep_extractor)
        analyzer.run()

        result = analyzer.results[0]

        assert set(result.results) == {
                self.test_data + "a.yml", self.test_data + "b.yml", self.test_data + "d.yml"}
