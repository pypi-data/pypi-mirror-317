import functools

# @ 语法糖会执行一次调用操作
"""
用类实现装饰器（构造方法绑定函数）：
    1. 在类做实例化调用时传入func，实现装饰器
    2. 依据__call__()方法实现被装饰后的调用操作
"""
class DecoratorOne:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


"""
用类实现装饰器（__call__()绑定函数）：
    1. 在装饰时，将类先实例化出来，可以传入必要的参数
    2. 依据__call__()方法实现装饰器功能
"""
class DecoratorAnother:

    def __init__(self, extra_params):
        self.extra_params = extra_params
        pass

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


@DecoratorOne
def test_decorator_one(text):
    print(text)


@DecoratorAnother
def test_decorator_another(text):
    print(text)


"""
两层嵌套的带参数装饰器：
    1.可以实现，但是失去了语法糖的特性了
    2.省下了一层嵌套哦
"""
def decorator_params(func, status):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('status', status)
        return func(*args, **kwargs)
    return wrapper


def test_decorator_params(text):
    print(text)


test_decorator_params = decorator_params(test_decorator_params, 'ON')


if __name__ == '__main__':
    print(test_decorator_one('hello'))
    pass