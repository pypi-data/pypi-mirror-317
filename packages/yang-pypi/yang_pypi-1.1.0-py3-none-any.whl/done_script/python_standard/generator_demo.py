
"""
生成器：
    1. 属于特殊的迭代器，使用next() 或 __next__() 迭代
    2. 自定义生成器内部的 yield 会返回当前的表达式的值，然后等待下一次的next。
    3. send：有next()的功能且使用send()可以向生成器发送一个值，此值会改变 yield 表达式的值，然后继续执行到下一个yield
"""

def my_generator():
    a = yield 0
    print('a', a)
    b = yield 1
    print('b', b)
    c = yield 2
    print('c', c)

if __name__ == '__main__':
    gene = my_generator()
    print(type(gene), gene)
    print('*'*20)
    print(gene.__next__())
    print(gene.send('hello'))  # 设置生成器当前暂停位置yield表达式的返回值，然后继续执行 到下一个yield
    pass