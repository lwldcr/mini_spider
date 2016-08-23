# -*- coding: utf-8 -*-
"""
webpage 单测
"""

import os
import sys
import Queue
import unittest
import threading

BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)

import webpage

class TestWebPageParser(unittest.TestCase):
    """testcases"""
    def setUp(self):
        self.q = Queue.Queue()
        self.q.put(('http://pycm.baidu.com:8081/', 0))
        self.mutex = threading.Lock()
        self.history_urls = []

    def testWebpageParser(self):
        """test WebpageParser"""
        parser = webpage.WebpageParser(2, out_path='./out',
            pattern='.*\.(htm|html)$', url_queue=self.q,
            crawler_name='test', mutex=self.mutex,
            history_urls=[])
        self.assertIsInstance(parser, webpage.WebpageParser)
        self.assertEqual(parser.crawler_name, 'test')
        parser.start(auto_terminate=True)
        self.assertTrue(os.path.isdir('./out'))

    def tearDown(self):
        for f in os.listdir('./out'):
            os.remove(os.path.join('./out', f))
        os.rmdir('./out')


def suite():
    """return test suite"""
    tests = ['testWebpageParser']
    return unittest.TestSuite(map(TestWebPageParser, tests))

if __name__ == '__main__':
    unittest.main()
