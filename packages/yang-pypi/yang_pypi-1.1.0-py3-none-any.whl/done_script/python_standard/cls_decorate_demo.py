"""
用装饰器来装饰类：
    1. 定义添加类或成员属性的装饰器时，仅需一层即可。
        与函数装饰器的不同：
            a.当装饰器装饰一个函数时把函数作为参数，且需要在内部调用该函数后再返回一个新的函数，故需要两层(内层作为新函数被返回)
            b.当装饰器装饰一个类时把类作为参数，不需要在内部调用该类，修改或添加后，直接返回该类即可
"""

def add_attributes(cls):
    # 添加类属性
    cls.class_attribute = "This is a class attribute"

    # 保存原始的 __init__ 方法
    original_init = cls.__init__

    # 定义新的 __init__ 方法
    def new_init(self, *args, **kwargs):
        # 调用原始的 __init__ 方法
        original_init(self, *args, **kwargs)
        # 添加实例属性
        self.instance_attribute = "This is an instance attribute"

    # 替换 __init__ 方法
    cls.__init__ = new_init
    return cls  # 返回修改后的类


@add_attributes
class MyClass:
    def __init__(self, value):
        self.value = value

    def show_value(self):
        print(f"Value: {self.value}")

# 使用修饰后的类
obj = MyClass(10)
obj.show_value()            # 输出: Value: 10
print(obj.instance_attribute)  # 输出: This is an instance attribute
print(MyClass.class_attribute)  # 输出: This is a class attribute