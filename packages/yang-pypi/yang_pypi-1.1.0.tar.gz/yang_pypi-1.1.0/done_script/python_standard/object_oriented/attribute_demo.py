
"""
类属性与实例属性：
    1. 类属性仅仅在定义类时创建一次，且在类中保存，为一般实例所共有。故此，当使用可变类型作为类属性时，一旦其有所改变则所有实例都会受影响。
    2. 实例属性与类属性同名时，实例属性会在实例中覆盖类属性，而不是在类中覆盖类属性
"""



def init_friends():
    print("init_friends 执行了")
    return ["jerry"]

class Person:
    name = 'Tom'
    friends= init_friends()

    def __init__(self):
        pass

if __name__ == '__main__':
    p1 = Person()
    print("p1's friends", p1.friends)
    p2 = Person()
    print("p2's friends", p2.friends)

    # p1修改类属性，类属性改变，p2也会受影响
    p1.friends.append("spike")
    print("p2's friends", p2.friends)
    pass
