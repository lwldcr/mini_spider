# -*- coding:utf-8 -*-
"""
载入url列表文件
"""

import os
import Queue

def load_seedfile(seed, q):
    """ load seedfile to queue"""
    if not os.path.isfile(seed):
        seed = './urls'
    try:
        with open(seed) as s:
            urls = s.readlines()
    except IOError:
        urls = []

    for url in urls:
        q.put((url.strip(), 0))

if __name__ == '__main__':
    url_queue = load_seedfile('./urls')
    print url_queue.qsize()
