
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from yaml_unfolder import YamlUnfolder
from yaml_unfolder import convert_path

class TestConvertPath(unittest.TestCase):

    def testThrowsForAbsPath(self):
        with self.assertRaises(Exception) as context:
            convert_path('/abs/path')

        self.assertTrue('Cannot include' in str(context.exception))

    def testKeepsFileIfAlreadyCorrect(self):
        self.assertEquals('file.yml', convert_path('file.yml'))
        self.assertEquals('dir/file.yml', convert_path('dir/file.yml'))

    def testConvertsRelativePath(self):
        self.assertEquals('file.yml', convert_path('./file.yml'))
        self.assertEquals('dir/file.yml', convert_path('./dir/file.yml'))
