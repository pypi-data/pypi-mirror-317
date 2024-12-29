import functools

'''
1. 装饰器语法糖等同语法（普通函数）：在函数外定义
    new_func = my_decorator(func)
    new_func()
'''
# if __name__ == '__main__':
#     def my_decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             print(args, kwargs)
#             return func(*args, **kwargs)
#         return wrapper
#
#     def func(a:int, b:int, c:int):
#         return a+b+c
#
#     new_func = my_decorator(func)
#     print(new_func(1,2 ,c=3))
#     ...

pass

'''
2. 装饰器语法糖等同语法（装饰类方法）：在类外定义
    class MyClass:
        def my_method(self):
    
    MyClass.my_method = my_decorator(MyClass.my_method)
'''

# if __name__ == '__main__':
#     def my_decorator(func):
#         @functools.wraps(func)
#         def wrapper(self, *args, **kwargs):
#             return func(self, *args, **kwargs)
#         return wrapper
#
#
#     class MyClass:
#         def my_method(self, x):
#             return x * 2
#
#     MyClass.my_method = my_decorator(MyClass.my_method)
#     print(MyClass().my_method(3))
#     ...

pass

'''
3.装饰器@语法糖执行时机(装饰普通函数):在代码实际执行到 @语法糖 处开始执行装饰操作
'''
# if __name__ == '__main__':
#     def my_decorator(func):
#         print('正在装饰.....')
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             print(args, kwargs)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     print('开始装饰')
#
#     @my_decorator
#     def func(a: int, b: int, c: int):
#         return a + b + c
#
#     print('结束装饰')
#     ...

pass

'''
4.装饰器@语法糖执行时机(装饰类中方法):在类实例化时 @语法糖 开始执行装饰
'''

# if __name__ == '__main__':
#     def my_decorator(func):
#         print('正在装饰...')
#         @functools.wraps(func)
#         def wrapper(self, *args, **kwargs):
#             return func(self, *args, **kwargs)
#         return wrapper
#
#
#     class MyClass:
#         print('开始装饰')
#         @my_decorator
#         def my_method(self, x):
#             return x * 2
#         print('结束装饰')
#
#     my_class = MyClass()
#     ...

pass
