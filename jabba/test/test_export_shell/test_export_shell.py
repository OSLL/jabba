
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba.yaml_unfolder import YamlUnfolder
from jabba import FileIndex
from jabba import export_shell

class TestExportShell(unittest.TestCase):
    def setUp(self):
        self.test_data = 'test/test_export_shell/test_data'
        self.exported_shell = 'test/test_export_shell/exported_shell'

        self.yaml_unfolder = YamlUnfolder(root=self.test_data)

    def testExportShell(self):
        file_index = FileIndex(self.test_data)

        export_shell(file_index, to_dir=self.exported_shell)

        with open("{}/{}".format(self.exported_shell, "test-test_export_shell-test_data-job.sh"), "r") as f:
            self.assertEquals(f.read(), "echo test\necho second line\n")
