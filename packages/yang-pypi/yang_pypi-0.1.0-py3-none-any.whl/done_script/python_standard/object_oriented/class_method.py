

class Person:
    age = 18

    def __init__(self, name):
        self.name = name
        pass

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        return obj

    @classmethod
    def class_new(cls):
        cls.age = 20
        obj = cls.__new__(cls)
        return obj

if __name__ == '__main__':
    person_1 = Person("Tom")
    print("1", person_1.name, person_1.age, person_1)
    person_2 = Person.class_new()
    print("2", person_2)
    person_2.__init__("jerry")
    print("3", person_2.name, person_2.age, person_2)
    # print(person_2.name, person_2.age, person_2)
    pass
