# coding: utf8


import MySQLdb
import json


def consumer(cur):
    r = ""
    while True:
        n = yield r                    # 消费者将r发送给生产者，并中断程序等待获取生产者send的数据，将值赋给n
        print('[CONSUMER] Consuming %s...' % n)
        r = "xxxxxxxxxxxxx"


def produce(c, cur):
    res_file = open("res.txt", "wb")
    c.next()                   # 运行消费者，当消费者运行到yield的时候停止，切换到该处继续执行当前代码
    f = open("data.txt", 'r')
    for line in f:
        line = line.strip('\n')
        print('[PRODUCER] Producing %s...' % line)
        user_id = c.send(line)    # 生产者接收到消费者yield过来的数据将值赋给user_id，并发送数据给消费者，消费者从yield处接收到数据又开始执行之后的代码
    c.close()
    res_file.close()


if __name__ == '__main__':
    c = consumer("x")
    produce(c, "x")


