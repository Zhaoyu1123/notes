# coding: utf8


# 插入排序
def insert_sort(lists):
    # 插入排序 假设第一个元素是排好的序列，第二个元素以后是待插入序列，循环待插入序列
    for i in range(1, len(lists)):
        key = lists[i]             # 取待插入序列的每个元素
        j = i - 1
        while j >= 0:              # 与排好的序列每个元素比较
            if lists[j] > key:
                lists[j + 1], lists[j] = lists[j], lists[j + 1]
            j -= 1
    return lists


# 冒泡排序
def short_bubble_sort(a_list):
    exchanges = False
    pass_num = len(a_list) - 1                   # 外层循环次数
    while pass_num > 0 and not exchanges:
        exchanges = True
        for i in range(pass_num):
            if a_list[i] > a_list[i + 1]:           # 只要有一个元素没排好序，exchanges = False
                exchanges = False
                a_list[i],a_list[i+1] = a_list[i+1], a_list[i]
        pass_num = pass_num - 1


# 选择排序, 假设第一个元素是最大的，循环剩余的元素余值比较，大则交换位置，找出最大的元素
# 外层循环为倒叙，一次是最大的元素需要插入的位置。
def selection_sort(a_list):
    for fill_slot in range(len(a_list) - 1, 0, -1):
        pos_of_max = 0
        for location in range(1, fill_slot + 1):
            if a_list[location] > a_list[pos_of_max]:
                pos_of_max = location
        a_list[fill_slot],a_list[pos_of_max]=a_list[pos_of_max],a_list[fill_slot]


# 快速排序,选第一个数作为基准数，小的放在左边，大的放在右边。
def qsort(seq):
    if seq==[]:
        return []
    else:
        pivot=seq[0]
        lesser=qsort([x for x in seq[1:] if x<pivot])
        greater=qsort([x for x in seq[1:] if x>=pivot])
        return qsort(lesser)+[pivot]+qsort(greater)


# 二分查找
def binarySearch(l, t):
    low, high = 0, len(l) - 1
    while low < high:
        mid = (low + high) / 2
        if l[mid] > t:
            high = mid
        elif l[mid] < t:
            low = mid + 1
        else:
            return mid
    return low if l[low] == t else False     # 此时 low == high


# 栈的实现, 先进先出
class Stack:
    def __init__(self):
       self.items = []
    def is_empty(self):
       return self.items == []
    def push(self, item):
       self.items.append(item)
    def pop(self):
       return self.items.pop()
    def peek(self):                #查看栈的顶部的对象
       return self.items[len(self.items)-1]
    def size(self):
       return len(self.items)


# 队列的实现, 先进后出
class Queue:
   def __init__(self):
      self.items = []
   def is_empty(self):
      return self.items == []
   def enqueue(self, item):
      self.items.insert(0,item)
   def dequeue(self):
      return self.items.pop()
   def size(self):
      return len(self.items)


# 二叉树的实现
class BinaryTree:
    def __init__(self, root):
        self.key = root
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if self.left_child == None:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if self.right_child == None:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

# 堆是一种完全二叉树，堆排序是一种树形选择排序，利用了大顶堆堆顶元素最大的特点，不断取出最大元素，并调整使剩下的元素还是大顶堆，依次取出最大元素就是排好序的列表。


def recur_fibo(n):
   """
   递归函数
   输出斐波那契数列
   """
   if n <= 1:
       return n
   else:
       return recur_fibo(n-1) + recur_fibo(n-2)


# 汉诺塔递归（压栈出栈）
def move(n, a, buffer, c):
    if n == 1:
        print(a, "->", c)
        return
    move(n-1, a, c, buffer)      # 把n-1个盘子由 a 移动到 b 借助 C       buffer 表示 b
    move(1, a, buffer, c)           # 把最后一个盘子由 a 移动到 C
    move(n-1, buffer, a, c)      # 把n-1个盘子由 b 移动到 c 借助 a


# 合并两个有序列表
# 第归
def _recursion_merge_sort2(l1, l2, tmp):
    if len(l1) == 0 or len(l2) == 0:
        tmp.extend(l1)
        tmp.extend(l2)
        return tmp
    else:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
        return _recursion_merge_sort2(l1, l2, tmp)


# 循环算法
def loop_merge_sort(l1, l2):
    tmp = []
    while len(l1) > 0 and len(l2) > 0:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
    tmp.extend(l1)
    tmp.extend(l2)
    return tmp
