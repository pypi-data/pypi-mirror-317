#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-05 16:12:24
# @Author: Alan
# @File: test_inspect.py
# @Describe: inspect 反射 获取数据

import math
import inspect

"""
inspect.getsource()   获取源码 函数或类
inspect.signature()   获取参数 函数或类
inspect.isclass()   是否是类
inspect.isfunction()   是否是函数
inspect.ismethod()   是否是类方法
"""


class DemoClass:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def show_name(self):
        return self._name

    def show_age(self):
        return self._age

    def play(self, game):
        return 'name: {}, age: {} is playing {}'.format(self._name, self._age, game)


# 获取信息
print(inspect.getsource(DemoClass))   # 源码
print(inspect.signature(DemoClass('Loly', 20).play))  # (game) 获得play函数的参数
print(inspect.signature(DemoClass))   # 获得类的参数 (name,age)  是初始化的参数

# 判断对象的类型
if inspect.isclass(DemoClass):
    print('cool')

if inspect.isfunction(DemoClass('Loly', 20).play):
    # 找的是普通函数
    print('cool1')
else:
    print('dd')

if inspect.ismethod(DemoClass('Loly', 20).play):
    # 找的是类里的方法
    print('cool1')
else:
    print('dd')


# 获取math模块中所有成员
# members = inspect.getmembers(math)
# for name, value in members:
#     print(name, value)


# 获取类成员
class MyClass:
    def __init__(self):
        self.a = 1

    def my_method(self):
        pass


members = inspect.getmembers(MyClass, predicate=inspect.isfunction)
print(members)  # 输出类中所有函数成员


def grandparent():
    parent()


def parent():
    child()


def child():
    for frame_record in inspect.stack():
        caller_frame = frame_record[0]
        info = inspect.getframeinfo(caller_frame)
        print(
            f"Function '{info.function}' called at line {info.lineno} of file {info.filename}")


grandparent()


"""
反射
getattr(object,name)
hasattr(object,name)
setattr(object,name,value)
delattr(object,name)

"""


class MyClass:
    def __init__(self):
        self.name = "Alice"

    def greet(self):
        print(f"Hello, {self.name}!")


obj = MyClass()

# 使用 getattr 获取属性值
name = getattr(obj, "name")
print(name)  # 输出: Alice

# 使用 setattr 设置属性值
setattr(obj, "name", "Bob")
print(obj.name)  # 输出: Bob

# 使用 hasattr 检查属性或方法是否存在
has_greet = hasattr(obj, "greet")
print(has_greet)  # 输出: True

# 使用 delattr 删除属性
delattr(obj, "name")
print(hasattr(obj, "name"))  # 输出: False

# 使用 getattr 调用方法
greet_method = getattr(obj, "greet")
greet_method()  # 输出: Hello, Alice!
