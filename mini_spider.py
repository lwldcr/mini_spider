# -*- coding: utf-8 -*-
"""
mini spider
"""

import sys
import Queue
import argparse
import logging
import threading

import seedfile_load
import config_load
import crawl_thread
import spider_conf

reload(sys)
sys.setdefaultencoding('utf-8')

VERSION = '0.0.1'

url_queue = Queue.Queue()

def log_config():
    """log configuration"""
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='spider.log',
                    filemode='a+')


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.0')
    parser.add_argument("-c", "--conf", help="assign config file")
    args, remaining = parser.parse_known_args(sys.argv)
    conf_file = args.conf
    config_info = config_load.load_conf(conf_file)
    thread_count = int(config_info['thread_count'].replace(';', ''))

    log_config()
    logging.info("Mini Spider activated")
    conf = spider_conf.SpiderConf(config_info)

    seedfile_load.load_seedfile(config_info['url_list_file'], url_queue)
    if url_queue.qsize() <= 0:
        logging.error("FATAL: no urls loaded, exit!")
        sys.exit(1)
    history_urls = []
    threads = []
    mutex = threading.Lock()
    for i in range(thread_count):
        crawler = crawl_thread.CrawlerThread(url_queue=url_queue, 
                thread_name="Crawler" + '_' + str(i), conf=conf,
                history_urls=history_urls, mutex=mutex)
        threads.append(crawler)
        crawler.setDaemon(True)
        crawler.start()
    url_queue.join()

    for t in threads:
        if t.isAlive():
            logging.info("%s, waiting to terminate", t.name)
            t.join(1)
    logging.info("Crawler exited")

if __name__ == '__main__':
    main()
