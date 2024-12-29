

content = """
python的super(class, self).xxx()与super().xxx()区别：

1. super(class, self).xxx()：显示调用父类方法，其中的class是指从哪一个类开始调用其父类的方法，self是class的实例。
    eg：
        A <- B <- C <- D，在 D 中,super(B, self).xxx()，表示从D的父类B开始继续向上调用父类方法(即A.xxx())

2. super().xxx()：默认从当前类开始调用父类的方法
"""


class A:
    def __init__(self):
        print('AAAAAA')

class B(A):
    def __init__(self):
        super().__init__()
        print('BBBBBB')

class C(B):
    def __init__(self):
        super().__init__()
        print('CCCCC')

class D(C, B, A):
    def __init__(self):
        super().__init__()
        print()
        super(B, self).__init__()
        print('DDDDDD')


if __name__ == '__main__':
    D()