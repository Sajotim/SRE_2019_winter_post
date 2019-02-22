from tool import log


from token import Token

from token_type import Type



from token_tokenizer import tokenizer

from token_parser import parser









def reduce(fn, array, basic, vars):
#fn = apply_dic[key]

    array = [basic] + array

    if len(array) == 2:

        x, y = array

        if isinstance(y, list):

            y = apply_op(y, vars)#计算列表中两个操作数的值，并返回，递归
#对两个数的处理
        return fn(int(x), int(y))

    else:

        x, y, *ls = array

        t = fn(int(x), int(y))

        return reduce(fn, ls, t, vars)#递归，对列表中多个数字的处理





def format_expression(ls, vars):

    expression = []

    for i, e in enumerate(ls):

        if isinstance(e, list):

            return interpreter([e], vars)[0]

        elif isinstance(e, Token):

            if e.type == Type.number:

                expression.append(int(e))

            elif e.type == Type.vars:

                v = vars.get(e.value, Type.error)

                if v == Type.error:

                    raise ValueError

                expression.append(v)

            else:

                expression.append(e)

        else:

            pass

    return expression





def apply_op(tokens, vars):

    from operator import add, sub, mul, truediv, mod

    op_dic = {

        '+': add,

        '-': sub,

        '*': mul,

        '/': truediv,

        '%': mod,

    }
    #计算器的作用，还没有计算，只是进行了匹配
    #op匹配运算函数名称，exprssion是一个操作数列表，basic第一个元素

    op, *expression = tokens

    expression = format_expression(expression, vars)

    basic = expression[0]

    expression = expression[1:]

    return reduce(op_dic[op.value], expression, basic, vars)





def apply_compare(tokens, vars):



    if isinstance(tokens, Token):

        # 说明是关键字

        return tokens

    elif isinstance(tokens, list):

        from operator import eq, ne, gt, lt

        op_dic = {

            '>': gt,

            '<': lt,

            '!': ne,

            '=': eq,

        }

        op, *expression = tokens


        v1, v2 = format_expression(expression, vars)

        v1 = int(v1)

        v2 = int(v2)

        # v1, v2 都有可能是 Token 类型, 所以添加 __gt__ 等魔法方法

        ans = op_dic[op.value](v1, v2)

        if ans:

            return Token(Type.keyword, 'yes')

        return Token(Type.keyword, 'no')

    else:

        pass





def apply_if(tokens, vars):

    boolean = apply_compare(tokens[1], vars)

    index = 2

    # 新增魔法方法 __eq__

    if boolean == 'no':

        index = 3

    t = tokens[index]

    if isinstance(t, Token):

        if t.type == Type.number:

            return int(t.value)

        return t

    elif isinstance(t, list):

        pass

    token = interpreter([t], vars)

    return token





def apply_log(tokens, vars):

    value = tokens[1]

    console = value

    if isinstance(value, list):

        console = interpreter([value], vars)

    elif isinstance(value, Token):

        if value.type == Type.string:

            console = value.value

        elif value.type == Type.vars:

            error = Type.error

            # vars 中存的数组

            console, *_ = vars.get(value.value, error)

        else:

            pass

    else:

        pass

    print('>>> {}'.format(console))





def apply_set(tokens, vars):
#实现变量的赋值操作
    _, k, v = tokens

    if isinstance(v, list):

        v = interpreter([v], vars)

    elif isinstance(v, Token):

        if v.type == Type.vars:#如果所赋值是另一个变量，则查找该变量的值（在变量字典中）

            v = vars.get(v.value)

        elif v.type == Type.number:

            v = int(v.value)

        else:

            print('set error')

    vars[k.value] = v
#向变量字典中添加新元素




def apply_function(tokens, vars):

    _, define, *(body, *_) = tokens

    function_name, *arg = define

    vars[function_name.value] = (arg, body)





def replace_args(default, arg):

    inner_vars = {}

    for i in range(len(default)):

        # 需要给 Token 加上 __hash__ and __eq__

        k = default[i]

        v = arg[i]

        inner_vars[k] = v

    return inner_vars





def apply_call(tokens, vars):
#计算带有形参的函数
    define, *arg = tokens

    default_arg, *body = vars[define.value]

    if isinstance(arg[0], Token):

        inner_vars = replace_args(default_arg, arg)

        vars.update(inner_vars)
        #将内部变量合并到全局变量
        value = interpreter(body, vars)

        return value[0]

    else:

        value = interpreter([tokens], vars)

        log('\n')

        return value





def interpreter(tree, vars):

    """

    tree 是一个形如 [表达式 1, [表达式 2, ... 表达式 n]]


    """

    output = []

    apply_dic = {

        'op': apply_op,

        'compare': apply_compare,

        'if': apply_if,

        'log': apply_log,

        'set': apply_set,

        'function': apply_function,

        'call': apply_call,

    }

    for i in tree:#这里的i是指token类

        key = key_from_token(i, vars)

        fn = apply_dic[key]#fn泛指函数名称

        output.append(fn(i, vars))

    return output





def key_from_token(array, vars):

    op, *_ = array

    # log('array', array)
#标识映射了相应的功能键，而相应的功能键对应相应的功能函数
    v = op.value

    keyword_list = ['function', 'if', 'log', 'yes', 'no', 'set', 'default']

    if v in '+-*/%':

        return 'op'

    elif v in '><=!':

        return 'compare'

    elif v in keyword_list:

        return v

    elif v in vars:

        if isinstance(vars[v], tuple):

            return 'call'

    else:

        return 'function'





def apply(code):

    # 全局 vars 来装载变量
    #tree是语义解释器

    vars = {}

    tokens = tokenizer(code)

    tree, _ = parser(tokens)

    console = interpreter(tree, vars)

    return console
#返回输出列表




def test():

    print('run main')

    c = """

    [set a [+ 1 5]]

    [log a]



    [function [plus a b] [+ a b]]



    [set b [plus 0 6]]

    [log b]



    [function [compare x] [if [< x 1] [log "小于1"] [log "大于或等于1"]]]

    [compare 0]
    
        """

    console = apply(c)





def main():

    test()





if __name__ == '__main__':

    main()