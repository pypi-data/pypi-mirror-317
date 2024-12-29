from select import select


class MyClass:

    def __init__(self):
        """执行实例属性初始化操作的地方"""
        print("__init__执行了")
        self.name = "虹猫"
        pass

    def __int__(self):
        """
        1. 定义调用int()时的行为，必须返回int类型，否则继续向后传递到__index__()
        2. 直接调用__int__()时，不返回int类型也不报错，但是用内置方法int()就TypeError
        """
        print("__int__执行了")
        return 10

    def __getattribute__(self, item):
        """只要访问属性时就会被触发, 应该调用super来返回属性值，不然怎么找父类中存在的属性呢？"""
        print("__getattribute__执行了", type(item), item)
        return super().__getattribute__(item)

    def __getattr__(self, item):
        """只有访问不存在的属性时才会触发"""
        print("__getattr__执行了", item)

    # def __get__(self, instance, owner):
    #     """只有调用描述符属性时被调用"""
    #     print(instance, owner)
    #     pass


if __name__ == '__main__':
    my_class = MyClass()
    print(my_class.age)  # 执行__getattr__
    # print(my_class.name)  # 执行__getattr__
    pass
