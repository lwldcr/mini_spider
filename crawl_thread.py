# -*- coding: utf-8 -*-
"""
crawler thread definition
"""

import logging
import socket
import threading
import webpage
import spider_conf

class CrawlerThread(threading.Thread):
    """Crawler thread"""
    def __init__(self, url_queue, thread_name, conf, history_urls=None, mutex=None):
        super(CrawlerThread, self).__init__(name = thread_name)
        self.url_queue = url_queue
        self.conf = conf
        if type(history_urls) != list:
            self.history_urls = []
        else:
            self.history_urls = history_urls
        self.mutex = mutex

    def run(self):
        """run thread"""
        logging.info('%s started', self.name)
        socket.setdefaulttimeout(self.conf.timeout)
        self.parser = webpage.WebpageParser(self.conf.max_depth,
                out_path=self.conf.output_directory,
                pattern=self.conf.target_url,
                url_queue=self.url_queue,
                crawler_name=self.name,
                interval=self.conf.interval,
                history_urls=self.history_urls,
                mutex=self.mutex)
        self.parser.start()
        logging.info('%s finished', self.name)

if __name__ == '__main__':
    config = {u'target_url': u'.*.(htm|html)$;', 
            u'output_directory': u'./output;',
            u'crawl_timeout': u'1;', 
            u'crawl_interval': u'1;', 
            u'url_list_file': u'./urls;', 
            u'max_depth': u'2;'}
    conf = spider_conf.SpiderConf(conf=config)
    import Queue
    q = Queue.Queue()
    q.put(('http://pycm.baidu.com:8081/', 0))
    crawler = CrawlerThread(q, 'crawler', conf)
    crawler.run()
