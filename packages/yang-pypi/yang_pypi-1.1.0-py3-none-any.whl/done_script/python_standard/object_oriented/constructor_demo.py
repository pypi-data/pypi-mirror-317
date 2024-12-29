"""
Python的构造函数：
    1. 执行顺序是  __new__() ---> __init__()
    2. 执行原理：通过类方法__new__调用super创建该类的实例，然后传递到__init__方法中进行初始化参数
    3. 在__new__中的形参不需要传入到super中，Python会自动将其传递给__init__方法
"""

class MyClass:
    def __init__(self, name):
        print('__init__执行了', self, name)
        self.name = name
        pass

    def __new__(cls, *args, **kwargs):
        print('__new__执行了', cls, *args, **kwargs)
        return super().__new__(cls)


if __name__ == '__main__':
    obj = MyClass('test')
    pass