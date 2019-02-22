from token import Token

from token_type import Type

#把字符串解析成token_list



def string_end(code, index):

    """

    code = "abc"

    index = 1

    """

    s = ''

    offset = index

    while offset < len(code):

        c = code[offset]

        if c == '"':

            # 找到字符串的结尾

            # s = code[index:offset]

            return s, offset

        elif c == '\\':

            # 处理转义符, 现在只支持 \"

            if code[offset+1] == '"':

                s += '"'

                offset += 2

            else:

                # 非法转义符

                pass

        else:

            s += c

            offset += 1

    # 程序出错, 没有找到反引号 "

    pass





def vars_end(code, offset):

    """

    接收 code, 直到空格跳出

    """

    code = code[offset:].strip()

    c = ''

    index = 0

    for i, e in enumerate(code):

        if e == ']' or e == ' ':

            break

        else:

            c += e

            index += 1

    return c, index
#返回变量名和变量的所在位置




def keyword_end(code, index):

    c = code[index:]

    keyword_list = ['function', 'if', 'log', 'yes', 'no', 'set', 'default']

    max_element = sorted(keyword_list, key=len)#按照关键字的长度进行排序

    for i in range(len(max_element[-1])):#range默认从1开始到最大长度关键字的长度结束

        if c[:i+1] in keyword_list:

            return c[:i+1], i





def _keyword(code, index):



    keyword_list = ['function', 'if', 'log', 'yes', 'no', 'set', 'default']

    max_element = sorted(keyword_list, key=len)

    for i in range(len(max_element[-1])):

        if code[index-1: index+i] in keyword_list:

            return True

        else:

            continue

    return False





def _vars(code, i):

    """

    如果前四位是 set, 就说明是变量

    """

    return code[i-5:i-2] == 'set'





def tokenizer(code):
#本文件中的关键函数
#处理变量 关键字 字符串 数字 空格 运算符
    length = len(code)

    tokens = []

    spaces = '\n\t\r '

    digits = '1234567890'

    # 当前下标，初始化下标，从0开始进行检索

    i = 0

    while i < length:

        # 当前应该处理的元素

        c = code[i]

        i += 1

        if c in spaces:

            # 空白符号要跳过, space tab return

            continue

        elif c in '+-*/%[]><=!':

            # 处理 6 种单个符号

            t = Token(Type.auto, c)#前一个参数是类型，后一个参数是值

            tokens.append(t)#处理后添加进解析成果的列表中

        elif c == '"':

            # 处理字符串

            s, offset = string_end(code, i)

            i = offset + 1#驱动继续检索

            t = Token(Type.string, s)

            tokens.append(t)

        elif c in digits:

            # 处理数字, 现在不支持小数和负数

            end = 0

            for offset, char in enumerate(code[i:]):

                if char not in digits:

                    end = offset

                    break

            n = code[i-1:i+end]

            i += end

            t = Token(Type.number, n)

            tokens.append(t)

        elif c == ';':

            # 处理注释

            if '\n' not in code[i:]:

                # 说明是单表达式时的注释

                break

            index = code[i:].index('\n')

            i += index

        # 这一步应该直接判断

        elif _keyword(code, i):

            # 处理关键字

            k, offset = keyword_end(code, i-1)

            i += offset

            t = Token(Type.keyword, k)

            tokens.append(t)

        elif _vars(code, i) or c.isalpha():

            # 说明是变量, 目前对变量名做首字母要求

            var, index = vars_end(code, i-1)

            t = Token(Type.vars, var)

            tokens.append(t)

            i += index - 1

        else:

            pass

    return tokens