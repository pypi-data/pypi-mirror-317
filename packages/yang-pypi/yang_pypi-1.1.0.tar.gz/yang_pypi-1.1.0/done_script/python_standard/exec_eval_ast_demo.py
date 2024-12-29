"""
1. ast.literal_eval()：将字符串计算成python的标准数据结构的值（字符串、字节串、数字、元组、字典、集合、布尔值、None 和 Ellipsis）

2. exec()：定义执行的字符串代码时，缩进要严格

eval()与exec()的globals，locals参数：
    1. locals 的优先级高于 globals

eval()与exec()的区别：
    1. eval()只执行单个的python表达式，exec()执行一段包含多条语句的代码块
    2. eval()的返回值为表达式的结果, exec()无返回值
"""


if __name__ == '__main__':
    x = 10
    y = 20
    custom_globals = {'x': 100}
    custom_locals = {'x': 1000, 'y': 2000}

    a = """
x = 10
y = 20
print(x+y)
    """
    exec(a)

    # locals 的优先级高于 globals
    result = eval('x + y', custom_globals, custom_locals)
    print(result)  # 输出 3000

