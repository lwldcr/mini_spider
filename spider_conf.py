#-*- coding: utf-8 -*-

"""配置文件定义"""

import logging

class SpiderConf(object):
    """配置文件"""
    def __init__(self, conf=None):
        if not conf:
            conf = {}
        self.max_depth = 2
        self.output_directory = '.'
        self.target_url = ''
        self.timeout = 10
        self.interval = 1
        try:
            self.max_depth = int(conf.get('max_depth', '2').replace(';', ''))
            self.output_directory = conf.get('output_directory', '.').replace(';', '')
            self.target_url = conf.get('target_url').replace(';', '')
            self.timeout = float(conf.get('crawl_timeout', '10').replace(';', ''))
            self.interval = float(conf.get('crawl_interval', '1').replace(';', ''))
            logging.info("config loaded successfully")
        except AttributeError:
            logging.error("loading config failed: %s, using default values", conf)
