
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization import util

class TestConvertPath(unittest.TestCase):

    def testThrowsForAbsPath(self):
        with self.assertRaises(Exception) as context:
            util.convert_path('/abs/path')

        self.assertTrue('Cannot include' in str(context.exception))

    def testKeepsFileIfAlreadyCorrect(self):
        self.assertEquals('file.yml', util.convert_path('file.yml'))
        self.assertEquals('dir/file.yml', util.convert_path('dir/file.yml'))

    def testConvertsRelativePath(self):
        self.assertEquals('file.yml', util.convert_path('./file.yml'))
        self.assertEquals('dir/file.yml', util.convert_path('./dir/file.yml'))

    def testRemoveDuplicateSlashes(self):
        self.assertEquals('dir/file.yml', util.convert_path('dir//file.yml'))
