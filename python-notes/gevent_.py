#! -*- coding:utf-8 -*-
import gevent
from gevent import monkey;monkey.patch_all()
import urllib2
def get_body(i):
	print "start",i
	urllib2.urlopen("http://cn.bing.com")
	print "end",i
tasks=[gevent.spawn(get_body, i) for i in range(3)]
gevent.joinall(tasks)


"""输出

start 0
start 1
start 2
end 2
end 0
end 1

说明：从结果上来看，执行get_body的顺序应该先是输出”start”，然后执行到urllib2时碰到IO堵塞，则会自动切换运行下一个程序（继续执行get_body输出start），直到urllib2返回结果，再执行end。也就是说，程序没有等待urllib2请求网站返回结果，而是直接先跳过了，等待执行完毕再回来获取返回值。值得一提的是，在此过程中，只有一个线程在执行，因此这与多线程的概念是不一样的。


monkey可以使一些阻塞的模块变得不阻塞，机制：遇到IO操作则自动切换，手动切换可以用gevent.sleep(0)
gevent.spawn 启动协程，参数为函数名称，参数名称
gevent.joinall  挂起协程

"""

import gevent
from gevent.queue import Queue

products = Queue()
 
def consumer(name):
    while not products.empty():
        print '%s got product %s' % (name, products.get())
        gevent.sleep(0)
 
    print '%s Quit'
 
def producer():
    for i in xrange(1, 10):
        products.put(i)
 
gevent.joinall([
    gevent.spawn(producer),
    gevent.spawn(consumer, 'steve'),
    gevent.spawn(consumer, 'john'),
    gevent.spawn(consumer, 'nancy'),
])

"""
首先，gevent是一个网络库：libevent是一个事件分发引擎，greenlet提供了轻量级线程的支持。所以它不适合处理有长时间阻塞IO的情况。

gevent就是基于这两个东西的一个专门处理网络逻辑的并行库。

1. gevent.spawn启动的所有协程，都是运行在同一个线程之中，所以协程不能跨线程同步数据。

2. gevent.queue.Queue 是协程安全的。

3. gevent启动的并发协程，具体到task function，不能有长时间阻塞的IO操作。因为gevent的协程的特点是，当前协程阻塞了才会切换到别的协程。
如果当前协程长时间阻塞，则不能显示（gevent.sleep(0)，或隐式，由gevent来做）切换到别的协程。导致程序出问题。

4. 如果有长时间阻塞的IO操作，还是用传统的线程模型比较好。

5. 因为gevent的特点总结是：事件驱动+协程+非阻塞IO，事件驱动值得是libvent对epool的封装，来基于事件的方式处理IO。

协程指的是greenlet，非阻塞IO指的是gevent已经patch过的各种库，例如socket和select等等。

6. 使用gevent的协程，最好要用gevent自身的非阻塞的库。如httplib, socket, select等等。

7. gevent适合处理大量无阻塞的任务，如果有实在不能把阻塞的部分变为非阻塞再交给gevent处理，就把阻塞的部分改为异步吧
"""
