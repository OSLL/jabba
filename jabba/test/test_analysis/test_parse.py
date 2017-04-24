
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from jabba.analysis import parse_analyzer_arguments as parse

class TestParseAnalyzerArguments(unittest.TestCase):

    def testEmptyInput(self):
        self.assertEqual(len(parse([])), 0) 

    def testSimpleInput(self):
        args = parse(["func"])

        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].function, "func")
        self.assertEqual(args[0].arguments, {})

    def testComplexInput(self):

        args = parse(["func1:arg1=True:arg2=False", "func2:arg1:arg2=10:arg3=hello"])

        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].function, "func1")
        self.assertEqual(args[1].function, "func2")

        self.assertEqual(args[0].arguments['arg1'], True)
        self.assertEqual(args[0].arguments['arg2'], False)

        self.assertEqual(args[1].arguments['arg1'], True)
        self.assertEqual(args[1].arguments['arg2'], 10)
        self.assertEqual(args[1].arguments['arg3'], 'hello')
 
