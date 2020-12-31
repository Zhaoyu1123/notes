# coding: utf-8
import socket
from time import time

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()


class Future:

    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)


class AsyncRequest:
    def __init__(self, host, url, port, timeout=5):
        self.sock = socket.socket()
        self.sock.settimeout(timeout)
        self.sock.setblocking(False)
        self.host = host
        self.url = url
        self.port = port
        self.method = None

    def get(self):
        self.method = 'GET'
        self.request = '{} {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(self.method, self.url, self.host)
        return self

    def process(self):
        if self.method is None:
            self.get()
        try:
            self.sock.connect((self.host, self.port))
        except BlockingIOError:
            pass
        self.f = Future()
        selector.register(self.sock.fileno(), EVENT_WRITE, self.on_connected)
        print(22222)
        yield self.f
        print(44444)
        selector.unregister(self.sock.fileno())

        self.sock.send(self.request.encode('ascii'))

        print("read all")
        chunk = yield from read_all(self.sock)
        print("read all finish")
        return chunk

    def on_connected(self):
        self.f.set_result(None)


def read(sock):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield f  # Read one chunk.
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = []
    # Read whole response.

    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)

    return b''.join(response)


class Task(Future):

    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.next_step(f)

    def next_step(self, future):
        try:
            print(111111)
            next_future = self.coro.send(future.result)
            print(333333, next_future)
            if next_future is None:
                print("next_future is None")
                return
        except StopIteration as exc:
            print("StopIteration as exc")

            self.set_result(exc.value)
            return
        next_future.add_done_callback(self.next_step)


class EventLoop:
    stopped = False
    select_timeout = 5

    def run_until_complete(self, coros):
        for coro in coros:
            Task(coro)
        self.run_forever()

    def run_forever(self):
        while not self.stopped:
            events = selector.select(self.select_timeout)
            if not events:
                continue
            for event_key, event_mask in events:
                print(event_key.data, "event")
                callback = event_key.data
                callback()

    def close(self):
        self.stopped = True


def fetch(url):
    request = AsyncRequest('www.baidu.com', url, 80)
    data = yield from request.process()
    return data


def async_way():
    ev_loop = EventLoop()
    ev_loop.run_until_complete([
        fetch('/s?wd={}'.format(i)) for i in range(1)
    ])


start = time()

async_way()

end = time()
print('Cost {} seconds'.format(end - start))