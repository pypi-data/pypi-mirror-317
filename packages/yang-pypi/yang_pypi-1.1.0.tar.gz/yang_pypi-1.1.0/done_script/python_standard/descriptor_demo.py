
"""
如果实例字典中有与描述符同名的属性，那么：

    1.描述符是数据描述符的话，优先使用数据描述符

    2.描述符是非数据描述符的话，优先使用字典中的属性。
"""


# 数据描述符
class DataDes:
    def __init__(self, default=0):
        self._score = default

    def __set__(self, instance, value):
        self._score = value

    def __get__(self, instance, owner):
        print("访问数据描述符里的 __get__")
        return self._score

# 非数据描述符
class NoDataDes:
    def __init__(self, default=0):
        self._score = default

    def __get__(self, instance, owner):
        print("访问非数据描述符里的 __get__")
        return self._score


class Student:
    math = DataDes(0)
    chinese = NoDataDes(0)

    def __init__(self, name, math, chinese):
        self.name = name
        self.math = math
        self.chinese = chinese

    def __getattribute__(self, item):
        print("调用 __getattribute__")
        return super(Student, self).__getattribute__(item)


if __name__ == '__main__':
    std = Student('xm', 88, 99)
    print('$'*10, '访问math')
    print(std.math)
    print('$' * 10, '访问chinese')
    print(std.chinese)
    pass