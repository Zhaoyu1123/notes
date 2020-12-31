# coding: utf8

from multiprocessing import Pool
import os, time


def process_work(l):
    print 'Run task (%s)...' % (os.getpid(), )
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()

    from gevent import monkey, spawn, joinall
    monkey.patch_all()
    import functools
    new_spawn = functools.partial(spawn, work)   # 预传参数
    joinall([new_spawn(line) for line in l])

    """ gevent pool
    from gevent.pool import Pool
    gp = Pool()
    gp.map(work, l)            // gevent 的 map 使用
    gp.join()
    """

    """ gevent pool
    from gevent.pool import Pool
    gp = Pool()
    g = gp.map_async(work, l, callback=xx)            // gevent 的 map_async 使用, 与map一样也是阻塞的, 但可以调用callback
    g.join()                    
    """
    print 'Task runs %0.2f seconds.' % ((end - start), )
    return l


def work(ln):
    return ln


def w_back(line):
    print line, 'back'
    with open('123.txt', 'a+') as rf:
        rf.writelines(line)


if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    import string, random

    res = []
    p = Pool()
    for _ in range(5):
        lines = [random.choice(string.ascii_letters) for _ in range(100)]
        result = p.apply_async(process_work, args=(lines, ), callback=w_back)
        """
            callback 处理的是 apply_async/map_async  的返回值
            apply_async/map_async 异步的，当使用 apply/map 同步是会阻塞直到进程池中所有函数执行完毕,等待该函数的执行结果。
            apply_async/map_async 的传参方式不同， 都支持回调函数
        """
        res.append(result)
    """
    如果使用阻塞方式运行，这段代码会被阻塞，直到池中的所有函数都执行完成。
    如果 max_processes=4 ，加入到线程池中的数量为5，而每个函数需要等待10秒钟，那么当前线程将
    被阻塞20秒钟
        do something
    """
    p.close()
    print 'Waiting for all subprocesses done...'
    p.join()
    for i in res:
        print i.get()   # 获取返回结果
    print 'All subprocesses done.'
    """  map_async
    p = Pool()
    p.map_async(process_work,
                [random.choice(string.ascii_letters+"\n") for _ in range(100)],
                callback=w_back)
    p.close()
    p.join()
    """
