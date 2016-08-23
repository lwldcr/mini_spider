# -*- coding: utf-8 -*-
"""
spider_conf单测
"""

import os
import sys
import Queue
import unittest

BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)

import spider_conf

class TestSpiderConf(unittest.TestCase):
    """testcases"""
    def setUp(self):
        self.conf = {
                'max_depth': '5;',
                'output_directory': 'out;',
                'target_url': 'http://www.baidu.com;',
                'crawl_timeout': '10;',
                'crawl_interval': '2;',
                }

    def testSpiderConfDefault(self):
        """test SpiderConf"""
        conf = spider_conf.SpiderConf()
        self.assertIsInstance(conf, spider_conf.SpiderConf)
        self.assertEqual(conf.max_depth, 2)
        self.assertEqual(conf.output_directory, '.')
        self.assertEqual(conf.target_url, '')
        self.assertEqual(conf.timeout, 10)
        self.assertEqual(conf.interval, 1)

    def testSpiderConfAssigned(self):
        """test SpiderConf"""
        conf = spider_conf.SpiderConf(self.conf)
        self.assertIsInstance(conf, spider_conf.SpiderConf)
        self.assertEqual(conf.max_depth, 5)
        self.assertEqual(conf.output_directory, 'out')
        self.assertEqual(conf.target_url, 'http://www.baidu.com')
        self.assertEqual(conf.timeout, 10)
        self.assertEqual(conf.interval, 2)


def suite():
    """return test suite"""
    tests = [
            'testSpiderConfDefault',
            'testSpiderConfAssigned',
            ]
    return unittest.TestSuite(map(TestSpiderConf, tests))


if __name__ == '__main__':
    unittest.main()
