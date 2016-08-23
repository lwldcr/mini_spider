# -*- coding: utf-8 -*-
"""
Test all
"""
import os
import sys
import unittest
BaseDir = os.path.dirname(__file__)
UpperDir = os.path.join('..', BaseDir)
sys.path.append(UpperDir)

import test_config_load
import test_crawl_thread
import test_seedfile_load
import test_spider_conf
import test_webpage

def main():
    """main"""
    suites = []
    suites.append(test_config_load.suite())
    suites.append(test_seedfile_load.suite())
    suites.append(test_crawl_thread.suite())
    suites.append(test_spider_conf.suite())
    suites.append(test_webpage.suite())
    test_suites = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(test_suites)

if __name__ == '__main__':
    main()
