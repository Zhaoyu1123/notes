# coding: utf8

import os, time, random, string
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def worker(tup):
    print 'Run task %s (%s)...' % (tup[0], os.getpid())
    start = time.time()
    tp = ThreadPool(10)
    res = tp.map_async(task, tup[1], callback=w_back)
    tp.close()
    tp.join()
    end = time.time()
    for j in res:
        print j
    print 'Task %s runs %0.2f seconds.' % (tup[0], (end - start))


def task(line):
    print line, "task"
    return line


def w_back(lines):
    print lines, "w_back"
    with open("thread.txt", 'a+') as f:
        f.writelines(lines)


if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool()

    p.map_async(worker,
                enumerate([[random.choice(string.letters) for _ in range(100)] for _ in range(5)]))
    p.close()
    print 'Waiting for all subprocesses done...'

    for i in range(10):
        print i

    p.join()
    print 'All subprocesses done.'