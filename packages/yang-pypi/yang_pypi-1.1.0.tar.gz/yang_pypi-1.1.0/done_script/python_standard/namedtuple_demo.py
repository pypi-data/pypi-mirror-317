
from collections import namedtuple

"""
具名元组的声明语句：namedtuple("类名"， 参数)，其中参数就是具名元组的元素，其形式可以是 [x, y, z] 或 "x, y, z" 或"x y z"
Note:
    1.使用时应该用类名来实例化，实例化必须给参数。
"""

class MyClass:
    def __init__(self):
        self.list_test = ['1', '2', '3']
    pass

if __name__ == '__main__':
    person = namedtuple("Person", 'name age sex content')
    print(person)
    me = person('坐地炮', 18, '男', MyClass())
    print(me.name, me.content)
    pass