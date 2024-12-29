
from done_script.python_standard.my_package import *

"""
1. 导包时，执行__init__.py文件内的代码
2. __init__.py文件内，__all__ = []，定义import *的内容
3. python3以后，不管有没有__init__.py文件都可以当做包来用，但是创建这个文件也累不死你！
"""

if __name__ == '__main__':
    print('大道至简')
    print(DemoName('小明').get_name())
    print(DemoAge(18).get_age())
    print(DemoSex('男').get_sex())
    pass