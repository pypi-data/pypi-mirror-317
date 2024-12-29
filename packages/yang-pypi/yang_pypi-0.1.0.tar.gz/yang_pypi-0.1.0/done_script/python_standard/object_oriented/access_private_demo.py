
"""
1. 类中的私有变量（protected，双下划线开头），不能直接访问，因为Python对其重新命名。
    硬要访问应该使用它改后的名字： _className__变量名
2. 类中的受保护变量变量（private，双下划线开头），可以直接访问，但对外一般不可见。
"""
from select import select


class Person:
    def __init__(self, name, age):
        self.name = name
        self._sex = "男" # protected变量
        self.__age = age  # private变量，自动变为_Person__age


class Worker(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        pass


if __name__ == '__main__':
    person_1 = Person('Tom', 18)
    print(person_1._sex)
    print(person_1._Person__age)
    print(person_1.__dict__)

    # 子类对父类的属性访问
    print("#"*10)
    worker_1 = Worker('Jack', 20)
    print(worker_1._sex)
    print(worker_1._Person__age)
    pass