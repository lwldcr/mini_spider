# -*- coding: utf-8 -*-
"""
seedfile_load单测
"""

import os
import sys
import Queue
import unittest

BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)

import seedfile_load
RootDir = os.path.dirname(seedfile_load.__file__)

class TestSeedFileLoad(unittest.TestCase):
    """testcases"""
    def setUp(self):
        self.default_seed_file = os.path.join(RootDir, 'urls')
        self.q = Queue.Queue()

    def testLoadSeedfile(self):
        """test load_seedfile"""
        seedfile_load.load_seedfile(self.default_seed_file, self.q)
        self.assertTrue(self.q.qsize() > 0)

        url_tuple = self.q.get()
        self.assertEqual(type(url_tuple), tuple)
        self.assertTrue(url_tuple[0].startswith('http'))
        self.assertEqual(type(url_tuple[1]), int)


def suite():
    """return test suites"""
    tests = ['testLoadSeedfile']
    return unittest.TestSuite(map(TestSeedFileLoad, tests))

if __name__ == '__main__':
    unittest.main()
