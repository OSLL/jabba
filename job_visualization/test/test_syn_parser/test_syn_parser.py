
import unittest
import sys
import os

sys.path.append("../")
sys.path.append("../../")

from job_visualization.synonym_parser import *

class TestSynonymParser(unittest.TestCase):

    def testAreSynonyms(self):
        s = SynonymSet()

        s.add_set({'a', 'b'})

        self.assertTrue(s.are_synonyms('a', 'b'))
        self.assertFalse(s.are_synonyms('a', 'c'))
        self.assertFalse(s.are_synonyms('b', 'c'))
        

    def testParseFromArgs(self):

        syns = parse_from_args(['{node-parameters, ', 'same-node}'])

        self.assertTrue(syns.are_synonyms('node-parameters', 'same-node'))

        syns = parse_from_args(['{node-parameters, ', 'same-node}', '{a,', ' b,', 'c}'])

        self.assertTrue(syns.are_synonyms('node-parameters', 'same-node'))
        self.assertTrue(syns.are_synonyms('a', 'b'))
        self.assertTrue(syns.are_synonyms('b', 'c'))
        self.assertTrue(syns.are_synonyms('c', 'a'))

        self.assertFalse(syns.are_synonyms('same-node', 'a'))
        self.assertFalse(syns.are_synonyms('same-node', 'b'))
        self.assertFalse(syns.are_synonyms('same-node', 'c'))

    def testParseFromArray(self):
        syns = parse_from_array([['node-parameters', 'same-node']])

        self.assertTrue(syns.are_synonyms('node-parameters', 'same-node'))

        syns = parse_from_array([['node-parameters', 'same-node'], ['a', 'b', 'c']])

        self.assertTrue(syns.are_synonyms('node-parameters', 'same-node'))
        self.assertTrue(syns.are_synonyms('a', 'b'))
        self.assertTrue(syns.are_synonyms('b', 'c'))
        self.assertTrue(syns.are_synonyms('c', 'a'))

        self.assertFalse(syns.are_synonyms('same-node', 'a'))
        self.assertFalse(syns.are_synonyms('same-node', 'b'))
        self.assertFalse(syns.are_synonyms('same-node', 'c'))


