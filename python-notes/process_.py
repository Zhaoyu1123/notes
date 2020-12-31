# ciding: utf-8

"""
    在利用Python进行系统管理的时候，特别是同时操作多个文件目录，或者远程控制多台主机，并行操作可
    以节约大量的时间。当被操作对象数目不大时，可以直接利用multiprocessing中的Process动态成生多
    个进程，10几个还好，但如果是上百个，上千个目标，手动的去限制进程数量却又太过繁琐，这时候进
    程池Pool发挥作用的时候就到了。
    Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，
    如果池还没有满，那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经
    达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程。
    pool.apply_async()用来向进程池提交目标请求，pool.join()是用来等待进程池中的worker进程执行完毕，
    防止主进程在worker进程结束前结束。但必pool.join()必须使用在pool.close()或者pool.terminate()之后
    。其中close()跟terminate()的区别在于close()会等待池中的worker进程执行结束再关闭pool,
    而terminate()则是直接关闭

    p.map(func, iterable [, chunksize] )
    将可调用对象func应用给iterable中的所有项目，然后以列表的形式返回结果。通过将iterable划分为多块并将工作分派给工作进程，可以并行地执行这项操作。chunksize制定每块中的项目数。
    如果数据量较大，可以增大chunksize的值来提升性能。

    p.map_async( func , iterable [, chunksize [, callback] ] )
    同map()函数，但结果的返回时异步地。如果提供callable参数，当结果变为可用时，它将与结果一起被调用。

    p.imap(func, iterable [, chunksize] )
    map（）函数的版本之一，返回迭代器而非结果列表。

    p.imap_unordered(func, iterable [,chunksize] )
    同imap()函数，但从工作进程接收结果时，返回结果的次序时任意的。

    方法apply_async()和map_async()的返回值是AsyncResult实例。AsyncResult实例具有以下方法。
    a.get( [timeout] )
    返回结果，如果有必要则等待结果到达。timeout是可选的超时。如果结果在制定时间内没有到达，将引发multuprocessing.TimeoutError异常。如果远程操作中引发了异常，它将在调用此方法时再次被引发。

    a.ready()
    如果调用完成，返回True

    a.sucessful()
    如果调用完成且没有引发异常，返回True。如果在结果就绪之前调用此方法，将引发AssertionError异常。

    a.wait( [ timeout] )
    等待结果变为可用。timeout是可选的超时。
"""

import multiprocessing
import time
import os


def func(msg):
    time.sleep(3)
    print "msg:", msg, os.getppid(), os.getpid()
    return "done" + msg


if __name__ == "__main__":
    start = int(time.time())
    pool = multiprocessing.Pool(processes=4)    # cpu_count() 线程池中最多线程数量
    result = []

    """
    向进程池发送请求数据，线程池中最多运行4个线程，当一个线程执行完毕，会获取新的请求数据再执行，
    直到所有请求数据被执行完毕。
    整个for循环与下面的语句等价
    result = pool.map(func, ["hello %d" % (i) for i in xrange(10)])
    """
    for i in xrange(10):
        msg = "hello %d" % i
        result.append(pool.apply_async(func, (msg, )))
    # 理解pool.apply_async(func, (msg, )) 类似于golang 的 go (gorouting)

    pool.close()  # 停止向进程池里面发送数据
    pool.join()
    for res in result:
        print ":::", res.get()
    print "Sub-process(es) done.", int(time.time()) - start

