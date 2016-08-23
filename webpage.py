# -*- coding: utf-8 -*-

"""
处理webpage,包括解析和保存
"""

import re
import os
import time
import Queue
import urllib
import urlparse
import multiprocessing
import random
import logging
import HTMLParser


class HrefParser(HTMLParser.HTMLParser):
    """HTML解析"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                for k, v in attrs:
                    if k == 'href':
                        self.links.append(v)

    def clear(self):
        """clear links"""
        self.links = []


class WebpageParser(object):
    """Webpage Parser"""
    def __init__(self, max_depth, out_path='.', pattern='', 
            url_queue=None, crawler_name='Crawler', interval=0.5, history_urls=None, mutex=None):
        self.max_depth = max_depth
        self.url_sets = []
        self.html = ''
        self.parser = HrefParser()
        self.out_path = out_path
        self.base_url = ''
        self.fetched_urls = []
        self.url_queue = url_queue
        self.pattern = pattern
        self.crawler_name = crawler_name
        self.interval = interval
        self.history_urls = history_urls
        self.mutex = mutex

        if not os.path.exists(self.out_path):
            try:
                os.mkdir(self.out_path)
            except OSError as e:
                logging.warning("%s mkdir %s failed: %s, use current dir by default",
                                self.crawler_name, self.out_path, e)
                self.out_path = '.'

    def start(self, auto_terminate=False):
        """start parse"""
        logging.info("%s called start(), queue len:%s ", 
                self.crawler_name, self.url_queue.qsize())
        count = 0
        while True:
            if auto_terminate:
                if count > 10:
                    return
                if self.url_queue.qsize() <= 0:
                    time.sleep(0.1)
                    count += 1
                    continue
            url, depth = self.url_queue.get()
            if url not in self.history_urls:
                try:
                    self.mutex.acquire()
                    logging.info('%s, acquired lock', self.crawler_name)
                    self.history_urls.append(url)
                except Exception as e:
                    logging.error('%s, acquire lock failed, %s', self.crawler_name, e)
                    continue

                try:
                    self.mutex.release()
                    logging.info('%s, release lock', self.crawler_name)
                except threading.ThreadError as e:
                    logging.error('%s, try release unacquired lock', self.crawler_name)
                    return

            self.base_url = url
            self.parse(url, depth)
            self.url_queue.task_done()
            time.sleep(self.interval)
        logging.info('%s job finished', self.crawler_name)

    def parse(self, url, depth):
        """Parse url"""
        if depth > self.max_depth:
            return
        try:
            url = urllib.quote(url.encode('utf-8'), ':/')
            self.html = urllib.urlopen(url).read()
        except IOError as err:
            logging.error('err: %s, %s', err, url)
            return
        except UnicodeError as err:
            logging.error('err: %s, %s', err, url)
            return

        self.decode(url)
        try:
            self.html = self.parser.unescape(self.html)
            self.parser.feed(self.html)
        except UnicodeDecodeError as err:
            logging.warning("parse url: %s failed, %s", url, err)
            return
        self.parser.close()
        self.url_sets += [urlparse.urljoin(self.base_url, suffix) for suffix in self.parser.links]
        self.parser.clear()
        for u in self.url_sets:
            if depth + 1 <= self.max_depth:
                self.url_queue.put((u, depth + 1))
        self.save(url)

    def save(self, url):
        """save page to file"""
        if re.match(self.pattern, url) and url not in self.fetched_urls:
            self.fetched_urls.append(url)
            out_file_name = os.sep.join([self.out_path, url.replace('://', '_').replace('/', '_')])
            logging.info('%s, saving %s,to: %s', self.crawler_name, url, out_file_name)
            with open(out_file_name, 'w') as f:
                f.write(self.html)

    def decode(self, url):
        """decode webpage"""
        charset_pattern = r'charset=\"?(.*?)\"'
        default_charset = 'utf-8'
        try:
            charset = re.findall(charset_pattern, self.html)[0].lower()
        except IndexError:
            logging.warning("no charset found for url: %s, use utf-8 by default", url)
            charset = default_charset

        if charset != 'utf-8':
            try:
                self.html = str(self.html).decode(charset)
            except:
                logging.error("decoding html failed: %s, with charset: %s", url, charset)


if __name__ == '__main__':
    q = Queue.Queue()
    q.put(('http://pycm.baidu.com:8081/', 0))
    parser = WebpageParser(2, out_path='./output', 
            pattern='.*\.(htm|html)$', url_queue=q, crawler_name='test')
    parser.start()
    print 'done'
