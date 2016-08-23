# -*- coding: utf-8 -*-
"""
Crawl_thread单测
"""

import os
import sys
import unittest
import Queue
import threading

BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)
import crawl_thread

class TestCrawlThread(unittest.TestCase):
    """testcases"""
    def setUp(self):
        self.config = {}
        self.q = Queue.Queue()
        self.name = 'crawler'

    def testInitThread(self):
        """test init thread"""
        self.crawler = crawl_thread.CrawlerThread(self.q, self.name, self.config)
        self.assertIsInstance(self.crawler, threading.Thread)
        self.assertEqual(self.crawler.name, self.name)

    def tearDown(self):
        pass


def suite():
    """return test suite"""
    tests = [
            'testInitThread'
            ]
    return unittest.TestSuite(map(TestCrawlThread, tests))

if __name__ == '__main__':
    unittest.main()
