from token_type import Type





class Token:
#每一个token类都保存了符号的意义（类型，类型使用整数的索引来表示）和内容
    def __init__(self, token_type, token_value):

        super(Token, self).__init__()

        # 用表驱动法处理 if

        d = {

            '+': Type.add,

            '-': Type.sub,

            '*': Type.mul,

            '/': Type.div,

            '[': Type.bracketLeft,

            ']': Type.bracketRight,

            '%': Type.percent,

            '>': Type.gt,

            '<': Type.lt,

            '=': Type.eq,

            '!': Type.ne,

        }

        if token_type == Type.auto:

            self.type = d[token_value]#通过查表，将输入的符号形式转化成标准形式

        else:

            self.type = token_type

        self.value = token_value



    def __repr__(self):
#返回一个字符串
        return '({})'.format(self.value)
#format是一个非常好用的格式化函数，可以和{}搭配，并且，可以按参数或者索引位置进行输出


    def __eq__(self, other):

        return self.value == other



    def __hash__(self):

        return hash(self.value)



    def __int__(self):

        return int(self.value)



    def __gt__(self, other):

        return self.value > other



    def __lt__(self, other):

        return self.value < other



    def __ne__(self, other):

        return self.value != other