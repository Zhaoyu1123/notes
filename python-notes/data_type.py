S.lower()   #小写
S.upper()   #大写
S.swapcase()   #大小写互换
S.capitalize()   #首字母大写
String.capwords(S)   
#这是模块中的方法。它把S用split()函数分开，然后用capitalize()把首字母变成大写，最后用join()合并到一起
S.title()    #只有首字母大写，其余为小写，模块中没有这个方法
字符串在输出时的对齐：
S.ljust(width,[fillchar])   
S.rjust(width,[fillchar])    #右对齐
S.center(width, [fillchar])    #中间对齐
S.zfill(width)   #把S变成width长，并在右对齐，不足部分用0补足
字符串中的搜索和替换：
S.find(substr, [start, [end]])   
#返回S中出现substr的第一个字母的标号，如果S中没有substr则返回-1。start和end作用就相当于在S[start:end]中搜索
S.index(substr, [start, [end]])   
#与find()相同，只是在S中没有substr时，会返回一个运行时错误
S.rfind(substr, [start, [end]])   
#返回S中最后出现的substr的第一个字母的标号，如果S中没有substr则返回-1，也就是说从右边算起的第一次出现的substr的首字母标号
S.rindex(substr, [start, [end]])
S.count(substr, [start, [end]])    #计算substr在S中出现的次数
S.replace(oldstr, newstr, [count])    
#把S中的oldstar替换为newstr，count为替换次数。这是替换的通用形式，还有一些函数进行特殊字符的替换
S.strip([chars])
#把S中前后chars中有的字符全部去掉，可以理解为把S前后chars替换为None
S.lstrip([chars])
S.rstrip([chars])
S.expandtabs([tabsize])   
#把S中的tab字符替换没空格，每个tab替换为tabsize个空格，默认是8个
字符串的分割和组合：
S.split([sep, [maxsplit]]) 
#以sep为分隔符，把S分成一个list。maxsplit表示分割的次数。默认的分割符为空白字符
S.rsplit([sep, [maxsplit]])
S.splitlines([keepends])
#把S按照行分割符分为一个list，keepends是一个bool值，如果为真每行后而会保留行分割符。
S.join(seq) #把seq代表的序列──字符串序列，用S连接起来
S.startwith(prefix[,start[,end]]) 
#是否以prefix开头
S.endwith(suffix[,start[,end]]) 
#以suffix结尾
S.isalnum() 
#是否全是字母和数字，并至少有一个字符
S.isalpha() #是否全是字母，并至少有一个字符
S.isdigit() #是否全是数字，并至少有一个字符
S.isspace() #是否全是空白字符，并至少有一个字符
S.islower() #S中的字母是否全是小写
S.isupper() #S中的字母是否便是大写
S.istitle() #S是否是首字母大写的



列表操作包含以下函数:
1、cmp(list1, list2)：比较两个列表的元素 
2、len(list)：列表元素个数 
3、max(list)：返回列表元素最大值 
4、min(list)：返回列表元素最小值 
5、list(seq)：将元组转换为列表 
列表操作包含以下方法:
1、list.append(obj)：在列表末尾添加新的对象
2、list.count(obj)：统计某个元素在列表中出现的次数
3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
5、list.insert(index, obj)：将对象插入列表
6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
7、list.remove(obj)：移除列表中某个值的第一个匹配项
8、list.reverse()：反向列表中元素
9、list.sort([func])：对原列表进行排序



Python字典包含了以下内置函数：
1、cmp(dict1, dict2)：比较两个字典元素。
2、len(dict)：计算字典元素个数，即键的总数。
Python字典包含了以下内置方法：
1、radiansdict.clear()：删除字典内所有元素
2、radiansdict.copy()：返回一个字典的浅复制
3、radiansdict.fromkeys()：创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值
4、radiansdict.get(key, default=None)：返回指定键的值，如果值不在字典中返回default值
5、radiansdict.has_key(key)：如果键在字典dict里返回true，否则返回false
6、radiansdict.items()：以列表返回可遍历的(键, 值) 元组数组
7、radiansdict.keys()：以列表返回一个字典所有的键
8、radiansdict.setdefault(key, default=None)：和get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为default
9、radiansdict.update(dict2)：把字典dict2的键/值对更新到dict里
10、radiansdict.values()：以列表返回字典中的所有值