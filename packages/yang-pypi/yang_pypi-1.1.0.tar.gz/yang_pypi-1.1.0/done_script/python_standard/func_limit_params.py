

# 1. 限制在 / 前的参数必须是位置参数
def func_args(a, /, b, c=5):
    return a + b + c


# 2. 限制在 * 后的参数必须是关键字参数
def func_kwargs(a, *, b, c=5):
    return a + b + c

"""
可变的函数参数:
    1. *args：可动态传递多个位置参数，在函数内部将 args解析成元组
    2. **kwargs：可动态传递多个关键字参数，在函数内部将 kwargs解析成字典
"""
def func_vary_args(*args, **kwargs):
    print("函数内的args", args)
    print("函数内的kwargs", kwargs)


if __name__ == '__main__':
    func_vary_args(1, 2, a=None)
    ...