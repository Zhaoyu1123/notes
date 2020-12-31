#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ssl
import json
import urllib
import urllib2
import hashlib
import threading
from Queue import Queue
from multiprocessing.dummy import Pool as ThreadPool

import redis
from concurrent.futures import ThreadPoolExecutor
# 标准库为我们提供了concurrent.futures模块，它提供了ThreadPoolExecutor和ProcessPoolExecutor两个类，实现了对threading和multiprocessing的更高级的抽象，对编写线程池/进程池提供了直接的支持。

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


pool = ThreadPool(10)
results_json = pool.map(self.dataice.get_data, info_list)
pool.close()
pool.join()



class Operator(object):
    login_url = 'https://api.100credit.cn/bankServer2/user/login.action'
    query_url = 'https://api.100credit.cn/bankServer2/data/terData.action'
    haina_api_url = 'http://192.168.22.27:8081/HainaApi/data/getData.action'

    def __init__(self, name, passwd, apicode):
        self.name = name
        self.passwd = passwd
        self.apicode = apicode
        self.tid = None
        self.tmd5 = None

    @staticmethod
    def post(url, data):
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        resp = opener.open(req, data)
        res = resp.read()
        opener.close()
        return json.loads(res)

    def login(self):
        res = self.post(self.login_url, {'userName': self.name,
                                         'password': self.passwd,
                                         'apiCode': self.apicode})

        if res['code'] != '00':
            return False, res['code']

        self.tid = res['tokenid']
        self.tmd5 = hashlib.md5(self.apicode + res['tokenid']).hexdigest()
        return True, '00'

    def get_one(self, data, modal):
        if modal in ['TelCheck', 'IdPhoto', 'TelPeriod', 'TelStatus']:
            data = json.loads(data)
            api_data = {
                'meal': data['meal'],
                'cell': data['cell'][0],
                'id': data['id'],
                'name': data['name'],
            }
            api_data = json.dumps(api_data, ensure_ascii=False)

            res = self.post(self.haina_api_url, {'tokenid': self.tid,
                                                 'apiCode': self.apicode,
                                                 'jsonData': api_data,
                                                 'checkCode': hashlib.md5(api_data + self.tmd5).hexdigest()})
        else:
            res = self.post(self.query_url, {'tokenid': self.tid,
                                             'interCommand': '1000',
                                             'apiCode': self.apicode,
                                             'jsonData': data,
                                             'checkCode': hashlib.md5(data + self.tmd5).hexdigest()})
        return res


RDS = redis.StrictRedis()


def mapping1():

    fd = open('results.txt', 'wb')

    def process_line(line):
        pass

    executor = ThreadPoolExecutor(max_workers=4)

    while RDS.exists('key'):
        llen = RDS.llen('key')
        tmp_lines = [RDS.lpop('key') for _ in xrange(10000 if llen > 10000 else llen)]
        results = executor.map(process_line, tmp_lines)

        for line in results:
            # ...
            fd.write(line)

    executor.shutdown()
    fd.close()
    return


class MappingWorker(threading.Thread):
    def __init__(self, func, rds, key, o_queue):
        super(MappingWorker, self).__init__()
        self.setDaemon(1)
        self._func = func
        self._rds = rds
        self._key = key
        self._o_queue = o_queue

    def run(self):
        while self._rds.exists(self._key):
            line = self._rds.lpop(self._key)
            res = self._func(line)
            self._o_queue.put(res)


def build_worker_pool(func, redis_data_key, queue, size=4):
    workers = []
    for _ in xrange(size):
        worker = MappingWorker(func, RDS, redis_data_key, queue)
        worker.start()
        workers.append(worker)
    return workers


class WriteFileWorker(threading.Thread):
    def __init__(self, fn, queue):
        super(WriteFileWorker, self).__init__()
        self.setDaemon(1)
        self._fn = fn
        self._queue = queue

    def run(self):
        fd = open(self._fn, 'wb')
        while True:
            content = self._queue.get()
            if content == 'quit':
                break

            fd.write(content)

        fd.close()

    def join(self, timeout=None):
        self._queue.put('quit')
        super(WriteFileWorker, self).join(timeout=timeout)


def mapping2():

    def process_line(line):
        pass

    out_queue = Queue()
    workers = build_worker_pool(process_line, 'redis_data_key', out_queue)

    out_worker = WriteFileWorker('filename', out_queue)
    out_worker.start()

    for worker in workers:
        worker.join()

    out_worker.join()


def group_generator(fd, chunksize):
    chunk = []
    for d in fd:
        line = d.strip('\n').split('\t')
        info = {'code': line[0], 'cell': line[1], 'id': line[2]}
        chunk.append(info)
        if len(chunk) >= chunksize:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def mapping():

    fd = open('results.txt', 'wb')

    sf = open('work1.txt','r')

    executor = ThreadPoolExecutor(max_workers=20)

    for chunk in group_generator(fd, 10000):
        obj = Operator('dts_cs', 'dts_cs', '111123')
        obj.login()
        results = executor.map(obj.get_one, chunk)
        for line in results:
            fd.write(line)

    executor.shutdown()
    sf.close()
    fd.close()
    return
