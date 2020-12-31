#多线程的2种模式

import threading
from time import sleep, time
 
loops = [4, 2]
 
def loop(nloop, nsec, lock):
    print('start loop %s at: %s' % (nloop, time()))
    sleep(nsec)
    print('loop %s done at: %s' % (nloop, time()))
    # 每个线程都会被分配一个事先已经获得的锁，在 sleep()的时间到了之后就释放 相应的锁以通知主线程，这个线程已经结束了。
 
 
def main():
    print('starting at:', time())
    threads = []
    nloops = range(len(loops))
 
    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)
 
    for i in nloops:
        # start threads
        threads[i].start()
 
    for i in nloops:
        # wait for all
        # join()会等到线程结束，或者在给了 timeout 参数的时候，等到超时为止。
        # 使用 join()看上去 会比使用一个等待锁释放的无限循环清楚一些(这种锁也被称为"spinlock")
        threads[i].join()  # threads to finish

    print('all DONE at:', time())
 
if __name__ == '__main__':
    main()
#>>>=====================================================================


from threading import Thread
from time import sleep, time
 
 
loops = [4, 2]
 
 
class MyThread(Thread):
 
    def __init__(self, func, args, name=""):
        super(MyThread, self).__init__()
        self.name = name
        self.func = func
        self.args = args
 
    def getResult(self):
        return self.res
 
    def run(self):
        # 创建新线程的时候，Thread 对象会调用我们的 ThreadFunc 对象，这时会用到一个特殊函数 __call__()。
        print 'starting', self.name, 'at:', time()
        self.res = self.func(*self.args)
        print self.name, 'finished at:', time()
 
 
def loop(nloop, nsec):
    print('start loop %s at: %s' % (nloop, time()))
    sleep(nsec)
    print('loop %s done at: %s' % (nloop, time()))
 

def main():
    print('starting at:', time())
    threads = []
    nloops = range(len(loops))
 
    for i in nloops:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        # start threads
        threads[i].start()
 
    for i in nloops:
        # wait for all
        # join()会等到线程结束，或者在给了 timeout 参数的时候，等到超时为止。
        # 使用 join()看上去 会比使用一个等待锁释放的无限循环清楚一些(这种锁也被称为"spinlock")
        threads[i].join()  # threads to finish
 
    print('all DONE at:', time())
 
 
if __name__ == '__main__':
    main()
