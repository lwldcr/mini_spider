# -*- coding: utf-8 -*-
"""
载入配置文件
"""

import os
import configparser
BaseDir = os.path.dirname(__file__)

def load_conf(conf=None):
    """load configuration"""
    if not conf or not os.path.isfile(conf):
        conf = os.path.join(BaseDir, 'spider.conf')
    conf_parser = configparser.ConfigParser()
    config = {}
    try:
        conf_parser.read(conf)
        for sec in conf_parser.sections():
            config[sec] = dict(conf_parser.items(sec))
    except configparser.ParsingError:
        config['spider'] = {}
    return config['spider']

if __name__ == '__main__':
    config = load_conf()
    print config
