
"""
__mro__多继承时的解析规则：
    1. 使用c3线性化，（同级别的）广度优先搜索
    2. 若继承的类中没有公共的类，则优先按继承顺序深度优先，递归构建mro
    3. 按同级继承顺序查找父类方法。note：如果子类在后，父类在前的方式被继承，报错TypeError

c3线性化：
    1. 子类在 MRO 中出现在父类之前。
    2. 如果有多个父类，它们会按声明顺序从左到右进行搜索。
    3. 每个类只能出现在 MRO 列表中一次。

mro构建规则：
    假设：D继承自C，B
    1. 分别获取C，D的__mro__内容
    2. 根据继承顺序以C为先，对比C，B第一项，若C的mro中第一项是B的mro中第一项的子类，则弹出C的mro第一项到D中，继续遍历C
    3. 若C的mro第一项是B的父类，则弹出B的more第一项到D中
    4. 继续2
"""
import types

from win32ui import types

# class A:
#     def __init__(self):
#         print("A")
#         super().__init__()
#
#
# class B(A):
#     def __init__(self):
#         print("B")
#         super().__init__()
#
#
# class C(B):
#     def __init__(self):
#         print("C")
#         super().__init__()
#
#
# class D():
#     def __init__(self):
#         print("D")
#         super().__init__()
#
#
# if __name__ == '__main__':
#     d = D()
#     print(A.__mro__)
#     print(C.__mro__)
#     print(D.__mro__)
#     pass
...
# class A:
#     def __init__(self):
#         print("A")
#
# class B(A):
#     def __init__(self):
#         print("B")
#         super().__init__()
#
# class C(A):
#     def __init__(self):
#         print("C")
#         super().__init__()
#
# # 另一批
# class Aa(B):
#     def __init__(self):
#         print("Aa")
#         super().__init__()
#
# class Bb(Aa, C):
#     def __init__(self):
#         print("Bb")
#         super().__init__()
#
#
# class Cc(Bb, A):
#     def __init__(self):
#         print("Cc")
#         super().__init__()
#
#
# class Sum(Cc, Aa):
#     def __init__(self):
#         print("Sum")
#         super().__init__()
#
# if __name__ == '__main__':
#      sum = Sum()
#      pass
...
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")
        super().__init__()




# 另一批
class Aa(B):
    def __init__(self):
        print("Aa")
        super().__init__()

class C(Aa, B):
    def __init__(self):
        print("C")
        super().__init__()

class Bb(C, Aa):
    def __init__(self):
        print("Bb")
        super().__init__()


# class Cc(Bb, A):
#     def __init__(self):
#         print("Cc")
#         super().__init__()
#
#
# class Sum(Cc, Aa):
#     def __init__(self):
#         print("Dd")
#         super().__init__()

if __name__ == '__main__':
     sum = Bb()
     print(types.resolve_bases(Bb))
     # print(Cc.__mro__)
     # print(Aa.__mro__)
     pass