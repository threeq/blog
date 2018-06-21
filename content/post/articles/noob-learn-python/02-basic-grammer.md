---
title: Python学习 02：python 基础语法初识
date: 2018-06-21
lastmod: 2018-06-21
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Python", "python3"]
categories:
 - python
tags:
 - python
toc: true
comment: true
description: ""


---


由于我们使用的 Jupyter web 交互式环境，所以对于 python 原始的交互式环境和如何在物理机器上运行 python 程序将放到后面介绍。直接进入 python 语法的学习。首先先简单了解 Python 的基础语法。

# python 高层概念

1. 程序由模块组成
2. 模块包含语句
3. 语句包含表达式
4. 表达式创建和操作对象

<!--more-->


# 标识符

* 在 Python 里，标识符由字母、数字、下划线组成。
* 在 Python 中，所有标识符可以包括英文、数字以及下划线(_)，但不能以数字开头。
* Python 中的标识符是区分大小写的。
* 以下划线开头的标识符是有特殊意义的。以单下划线开头 _foo 的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 from xxx import * 而导入；
* 以双下划线开头的 `__foo` 代表类的私有成员；以双下划线开头和结尾的 `__foo__ `代表 Python 里特殊方法专用的标识，如  `__init__()` 代表类的构造函数。

* Python 可以同一行显示多条语句，方法是用分号` ; `分开，
如：


```python
a="a"
_b1="bb"
print("hello, "); print("world!")

a-b = "ccc"  # 这里错误，不能包含 字母、数字、下划线 以外的字符
```

运行结果：

      File "<ipython-input-52-7c067522f272>", line 5
        a/b = "ccc"  # 这里错误，不能包含 字母、数字、下划线 以外的字符
                                                ^
    SyntaxError: can't assign to operator

# 保留字

下面的列表显示了在Python中的保留字。这些保留字不能用作常数或变数，或任何其他标识符名称。

所有 Python 的关键字只包含小写字母。

   a |  b | c   |
---|---|---
and	| exec|	not
assert	| finally	| or
break |	for	| pass
class |	from |	print
continue |	global	 |raise
def	| if |	return
del |	import |	try
elif	| in	 | while
else	| is	| with
except |	lambda	| yield

# 行和缩进

学习 Python 与其他语言最大的区别就是，Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块。

缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量，这个必须严格执行。如下所示：



```python
if True:
  print("True")
else:
  print("False")
```

    True



```python
if True:
    print( "Answer")
    print( "True")
else:
    print( "Answer")
    # 没有严格缩进，在执行时会报错
  print( "False")
```


      File "<ipython-input-6-90ba842299af>", line 7
        print( "False")
                       ^
    IndentationError: unindent does not match any outer indentation level



**IndentationError: unindent does not match any outer indentation level** 错误表明，你使用的缩进方式不一致，有的是 tab 键缩进，有的是空格缩进，改为一致即可。

如果是 IndentationError: unexpected indent 错误, 则 python 编译器是在告诉你"Hi，老兄，你的文件里格式不对了，可能是tab和空格没对齐的问题"，所有 python 对格式要求非常严格。

因此，在 Python 的代码块中必须使用相同数目的行首缩进空格数。

建议你在每个缩进层次使用 单个制表符 或 两个空格 或 四个空格 , 切记不能混用

# 多行语句

Python语句中一般以新行作为语句的结束符。

但是我们可以使用斜杠（ \）将一行的语句分为多行显示，如下所示：


```python
item_one='1'
item_two = '2'
item_three = '3'

total = item_one + \
        item_two + \
        item_three
```

语句中包含 [], {} 或 () 括号就不需要使用多行连接符。如下实例：


```python
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday']
```

# python 引号

Python 可以使用引号( ' )、双引号( " )、三引号( ''' 或 """ ) 来表示字符串，引号的开始与结束必须的相同类型的。

其中三引号可以由多行组成，编写多行文本的快捷语法，常用于文档字符串，在文件的特定地点，被当做注释。



```python
word = 'word'
sentence = "这是一个句子。"
paragraph = """这是一个段落。
包含了多个语句"""
```

# Python 注释

python中单行注释采用 # 开头。注释可以在语句或表达式行末。

python 中多行注释使用三个单引号(''')或三个双引号(""")。



```python
# 第一个注释
print("Hello, Python!")  # 第二个注释


'''
这是多行注释，使用单引号。
这是多行注释，使用单引号。
这是多行注释，使用单引号。
'''

"""
这是多行注释，使用双引号。
这是多行注释，使用双引号。
这是多行注释，使用双引号。
"""
print("没有看到错误就正确了哟！恭喜你")
```

    Hello, Python!
    没有看到错误就正确了哟！恭喜你


# python 空行

函数之间或类的方法之间用空行分隔，表示一段新的代码的开始。类和函数入口之间也用一行空行分隔，以突出函数入口的开始。

空行与代码缩进不同，空行并不是Python语法的一部分。书写时不插入空行，Python解释器运行也不会出错。但是空行的作用在于分隔两段不同功能或含义的代码，便于日后代码的维护或重构。

记住：空行也是程序代码的一部分。



# 数据类型

对于数据类型这里只做简要介绍，随后会详细介绍每种类型。


对象类型 | 实例
---|---
Numbers(数值) | 123, 3.4, 3+4j, Ob111, Decimal(), Fraction()
Strings(字符) | '你好', "spam", b'\x01c', u'sp\xc4m'
Lists(列表) | [1,[2,'three'], 4.5], list(range(10))
Dictionaries (字典) | {'food':'orange', 'taste': 'yum'}, dict(hours=10)
Tuples(元组) | (1,'yellow', 4, 'U'), tuple('spam'), namedtuple
Files(文件) | open('eggs.text'), open('/data/aaa.bin', 'wb')
Sets(集合) | set('abc'), {'a', 'b', 'c'}
Other core types(其他核心类型) | Booleans, types, None
Program unit types(程序单元类型) | Functios, modules, classes
Implementation-related types(实施相关) | 编译的代码(.pyc)，stack tracebacks




## 数值


```python
123
```




    123




```python
123+222
```




    345




```python
1.4*4
```




    5.6




```python
2**200
```




    1606938044258990275541962092341162602522202993782792835301376




```python
# 去数字长度
len(str(2**100000))
```




    30103




```python
3.1415 * 2
```




    6.283




```python
# 使用 print 输出
print(3.1415 * 2)
```

    6.283



```python
# 使用 math 数据模块
import math

math.pi
```




    3.141592653589793




```python
math.sqrt(85)
```




    9.219544457292887




```python
# 随机数
import random as rd

rd.random()
```




    0.9251197304813635




```python
# 随机选择一个元素
rd.choice([1,2,3,4])
```




    2



### 数值格式化输出


```python
print('{:,.2f}'.format(29688.2578))
print('%.2f | %+05d' % (3.1415926, -42))
```

    29,688.26
    3.14 | -0042


## 字符串

字符串是要使用引号引起来，可以使以下三种的其中一种：`''、""、""""""`。其中 `""""""` 可以包含多行文本。并且字符串是不可以改变的。


```python
S = "Yellow"
len(S)  # 获取文本长度
```




    6




```python
# 获取字符串特定位置的字符
print(S[0])
print(S[1])
print(S[-1])  # 可以使用负数，表示从右向左
print(S[-2])
print(S[len(S)-1]) # 这个和 print(S[-1]) 等效
```

    Y
    e
    w
    o
    w



```python
print(S)
# 返回字符串子串
print(S[1:3])
print(S[1:])
print(S)  # 返回字符串不会更改字符串的值

print(S[0:3])
print(S[:-1])
print(S[:])

```

    Yellow
    el
    ellow
    Yellow
    Yel
    Yello
    Yellow



```python
# 拼接两个字符串
print(S + "abc")

# 重复输出 N 遍字符串
print(S*8)
```

    Yellowabc
    YellowYellowYellowYellowYellowYellowYellowYellow


### 不可更改性


```python
print(S)

# 此语句将会报错
S[0] = 'z'
```

    Yellow



    ---------------------------------------------------------------------------
    
    TypeError                                 Traceback (most recent call last)
    
    <ipython-input-20-798812957f79> in <module>()
          2 
          3 # 此语句将会报错
    ----> 4 S[0] = 'z'


    TypeError: 'str' object does not support item assignment



```python
# 但是我们可以使用 子串 和 字符串拼接，形成新的字符串
S = 'z' + S[1:]
print(S)
```

    zellow



```python
# 或者可以使用 list 进行字符串的修改，但是这个也是形成新的字符串，不会修改原始字符串
a = "abcdefg"
L = list(a)
L
L[1] = 'c'
print(''.join(L))
print(a)
```

    accdefg
    abcdefg


更多关于字符串的知识，后面会详细介绍

### 格式化


```python
print('%s, eggs, and %s' % ('spam', 'SPAM!'))
print('{0}, eggs, and {1}'.format('spam', 'SPAM!'))
print('{}, eggs, and {}'.format('spam', 'SPAM!'))
```

    spam, eggs, and SPAM!
    spam, eggs, and SPAM!
    spam, eggs, and SPAM!


# 列表



```python
L = [123, 'spam', 1.33]
print(L)
print(len(L)) # 获取列表长度
```

    [123, 'spam', 1.33]
    3



```python
# 获取列表值
print(L[0])
print(L[:-1]) # 返回一个子列表
```

    123
    [123, 'spam']



```python
print(L + [4,5,6]) # 列表拼接
print(L*2)         
```

    [123, 'spam', 1.33, 4, 5, 6]
    [123, 'spam', 1.33, 123, 'spam', 1.33]



```python
# 检查边界
print(L)
print(L[1])
print(L[99]) # 这里会报错误
```

    [123, 'spam', 1.33]
    spam



    ---------------------------------------------------------------------------
    
    IndexError                                Traceback (most recent call last)
    
    <ipython-input-31-d40083741a4a> in <module>()
          1 print(L)
          2 print(L[1])
    ----> 3 print(L[99]) # 这里会报错误


    IndexError: list index out of range



```python
L[99] = 1 # 赋值也会报错
```


    ---------------------------------------------------------------------------
    
    IndexError                                Traceback (most recent call last)
    
    <ipython-input-32-a8d940cf9021> in <module>()
    ----> 1 L[99] = 1 # 赋值也会报错


    IndexError: list assignment index out of range


# 元组



```python
(1,2,3)
```




    (1, 2, 3)




```python
a = (1,2,3)
a[2]
```




    3



# 字典


```python
d = {"a":1, "b":2}
print(d)

print(d["a"])

d["a"] = "aaa"
print(d)
```

    {'a': 1, 'b': 2}
    1
    {'a': 'aaa', 'b': 2}


# 获取帮助

在 python 中一切都是对象，他们都有自己特定可操作的方法和属性，可以使用 `dir` 进行查看有哪些可使用的方法或属性。并且可以针对方法或属性使用 `help` 函数获得对应的 doc 文档。


```python
dir("a")
```




    ['__add__',
     '__class__',
     '__contains__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getitem__',
     '__getnewargs__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__iter__',
     '__le__',
     '__len__',
     '__lt__',
     '__mod__',
     '__mul__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__rmod__',
     '__rmul__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     'capitalize',
     'casefold',
     'center',
     'count',
     'encode',
     'endswith',
     'expandtabs',
     'find',
     'format',
     'format_map',
     'index',
     'isalnum',
     'isalpha',
     'isdecimal',
     'isdigit',
     'isidentifier',
     'islower',
     'isnumeric',
     'isprintable',
     'isspace',
     'istitle',
     'isupper',
     'join',
     'ljust',
     'lower',
     'lstrip',
     'maketrans',
     'partition',
     'replace',
     'rfind',
     'rindex',
     'rjust',
     'rpartition',
     'rsplit',
     'rstrip',
     'split',
     'splitlines',
     'startswith',
     'strip',
     'swapcase',
     'title',
     'translate',
     'upper',
     'zfill']

`__add__` 是内部方法，实现了字符串的拼接操作和使用 `+` 运算符效果一样


```python
print("a" + 'NI!')
print("a".__add__('NI!'))
```

    aNI!
    aNI!

`help` 获取帮助文档

```python
help("a".replace)
```

    Help on built-in function replace:
    
    replace(...) method of builtins.str instance
        S.replace(old, new[, count]) -> str
        
        Return a copy of S with all occurrences of substring
        old replaced by new.  If the optional argument count is
        given, only the first count occurrences are replaced.



# 试一试

- [ ] 将元组 `('a', 'bb')` 拼接 `a` ，并输出结果
- [ ] 为字典 `d` 新增字段数据：键 `'c'`，值 `'cc'` 

