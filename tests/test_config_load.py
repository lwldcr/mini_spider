# -*- coding: utf-8 -*-
"""
载入配置文件 单测
"""

import os
import sys
import unittest

BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)

import config_load

class TestConfigLoad(unittest.TestCase):
    """testcases"""
    def setUp(self):
        self.default_keys = [
            'crawl_interval',
            'crawl_timeout',
            'max_depth',
            'output_directory',
            'target_url',
            'thread_count',
            'url_list_file'
            ]

    def testLoadConfNotExist(self):
        """test load_conf when file doesnot exist"""
        config = config_load.load_conf('not_exist')
        self.assertEqual(type(config), dict)
        sorted_keys = sorted(config.keys())
        self.assertEqual(sorted_keys, self.default_keys)

    def testLoadConfNone(self):
        """test load_conf when file not given"""
        config = config_load.load_conf()
        self.assertEqual(type(config), dict)
        sorted_keys = sorted(config.keys())
        self.assertEqual(sorted_keys, self.default_keys)

    def testLoadConfDefault(self):
        """test load_conf:default conf"""
        config_file = os.path.join('..', 'spider.conf')
        config = config_load.load_conf(config_file)
        self.assertEqual(type(config), dict)
        sorted_keys = sorted(config.keys())
        self.assertEqual(sorted_keys, self.default_keys)

    def tearDown(self):
        pass


def suite():
    """return test suite"""
    tests = [
            'testLoadConfNotExist',
            'testLoadConfNone',
            'testLoadConfDefault',
            ]
    return unittest.TestSuite(map(TestConfigLoad, tests))

if __name__ == '__main__':
    unittest.main()
