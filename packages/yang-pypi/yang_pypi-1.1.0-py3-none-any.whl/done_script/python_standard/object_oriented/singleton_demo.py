
"""
一、new方法实现单例
    思想：使用类属性保存类实例，在类的__new__方法中添加判定，若类属性不为空则返回它。
    1.__new__(cls, *args, **kwargs)方法必须返回cls的实例；
        Note：cls是一个类； *args, **kwargs是传递的参数，默认是直接传递给__init__()方法

    2. __new__(cls, *args, **kwargs)方法使用 super.__new__(cls) 创建cls的实例。
"""

# class Singleton:
#     # 使用类属性保存类的示例
#     __instance = None
#
#     def __init__(self, *args, **kwargs):
#         print("@"*10, args, kwargs)
#         ...
#
#     def __new__(cls, *args, **kwargs):
#         if cls.__instance is None:
#             # instance是cls的实例
#             cls.__instance = super().__new__(cls)
#
#         # __new__()方法必须返回cls实例
#         return cls.__instance


"""
二、装饰器实现单例
"""

class Singleton:

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.a = kwargs['a']
        instance.b = kwargs['b']
        return instance

if __name__ == '__main__':
    singleton_1 = Singleton(1, 2, 3, a=10, b=20)
    singleton_2 = Singleton(2, 3, a=10, b=20)
    print('$'*10, singleton_1.__dict__)
    print(singleton_1==singleton_2)
    print(singleton_1 is singleton_2)
    ...