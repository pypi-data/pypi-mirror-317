

"""
python的枚举：
    1. 枚举类不能被实例化、且定义后不能被更改

Note：
    1. 枚举类型在Python中，每个成员都是枚举类的实例，而C#、C++等语言的枚举类型，每个成员都是整型常量。
    1. 不同语言的枚举机制取决于它们对类型安全和抽象层次的设计目标。Python和Java等语言为了保持对象化和安全性，
        分别要求通过 .value 或 getter 方法来访问枚举的值。而C#、C++等语言的枚举成员是整型常量，可以直接与数值比较。
"""
import enum
from enum import Enum


# 通过继承Enum类创建枚举
@enum.unique    # 确保枚举值唯一
class Color(Enum):
    RED = 1
    GREEN = enum.auto()
    BLUE = 3

# 枚举类的类型是enum.EnumType， 枚举类的成员类型是枚举类的实例对象
print("step_1：", type(Color), type(Color.GREEN))
# 通过 枚举类名.枚举成员名.value 获取枚举成员的值，对应 _value_ 属性
print("step_2：", Color.GREEN.value, Color.GREEN._value_)
# 通过 枚举类名.枚举成员名.name 获取枚举成员的名称，对应 _name_ 属性
print("step_3：", Color.GREEN.name, Color.GREEN._name_)




if __name__ == '__main__':
    # 通过构造函数创建坐标枚举
    COORDINATE = Enum("COORDINATE", "X_LEFT X_RIGHT Y_TOP Y_BOTTOM", module=__name__)
    print(COORDINATE.X_LEFT)
    # for item in COORDINATE:
    #     print(item)

    pass