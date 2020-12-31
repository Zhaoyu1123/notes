#多进程处理文件

# 多进程写入文件
import multiprocessing

def write_file(result):
    f = open('')
    f.write(result)

def process(args):
    '''
    work
    '''
    return result

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 100)
    for t in tasks:
        pool.apply_async(process, (t, ),callback=write_file)
    pool.close()
    pool.join()


# 读取文件方式
# 1. 一个进程读取到队列中，多进程或多线程处理队列
# 2. 将文件分块，多进程或多线程处理每块
