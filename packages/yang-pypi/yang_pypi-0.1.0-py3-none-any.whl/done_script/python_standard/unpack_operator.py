
"""
拆包：
    1. 直接拆包 *my_class，运行的是__iter__()方法，过程是生成一个迭代器，然后进行遍历。
"""


class MyClass:

    def __init__(self, hobby:list):
        self.hobby_list = hobby
        self.person_info_dict = {0:'张三', 1:18, 2:'男'}

    def __iter__(self):
        print(11111111111)
        return iter(self.hobby_list)

    def __getitem__(self, item):
        print(item)
        print(22222222222)
        return self.person_info_dict[item]

if __name__ == '__main__':
    my_class = MyClass(['a','b','c'])
    print(*my_class)
    pass
