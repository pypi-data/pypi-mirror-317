
"""
导入模块与包：
    1. python在导入模块时会执行该模块下的语句，声明(加载)该模块的类和函数
    2. __init__.py，如果一个目录下存在这个文件，Python 将其视为包，尽管它什么内容都没有。（python 3.3+ 没有该文件的文件夹也可以作为包被导入）
    3. __init__.py中的__all__=[‘’]，指明了哪些内容是可以通过 import * 导入
    4. __init__.py，在进行导包的时候，__init__.py模块下的代码会被执行
"""


# from done_script.python_standard.my_package.demo_1 import DemoName, DemoAge
#
# __all__ = ['DemoName', 'DemoAge']
#
#
# print('哎呀！我被导入啦！')