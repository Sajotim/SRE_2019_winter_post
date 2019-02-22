from enum import Enum



#用枚举的方式表示lisp所用到的变量类型

class Type(Enum):

    error = -1          # error

    auto = 0            # +-*/

    bracketLeft = 1     # [

    bracketRight = 2    # ]

    number = 3          # 169

    string = 4          # "name"

    add = 5

    sub = 6

    mul = 7

    div = 8

    percent = 9         # %

    keyword = 10        # 关键字

    gt = 11

    lt = 12

    eq = 13

    ne = 14

    vars = 15           # 变量