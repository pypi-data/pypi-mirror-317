from functools import partial

# partial返回的偏函数最终参数的顺序： *it_args, *you_args, {**it_kwargs, **you_kwargs}

def func(a, b, c=4):
    print(a + b + c)
    pass


if __name__ == '__main__':
    my_func = partial(func, c=5)
    my_func(3,2)
    pass
