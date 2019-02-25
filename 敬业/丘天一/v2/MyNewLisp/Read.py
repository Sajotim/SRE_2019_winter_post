def tokenize(inp_str):
    # 读取输入内容，分割字符串
    return inp_str.replace('(', ' ( ').replace(')', ' ) ').split()


class READ:
    # 返回输入需要处理的位置，处理完指向下一位置
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position

    def now(self):
        return self.tokens[self.position]

    def next(self):
        self.position += 1
        return None


def read_atom(tokens):
    # 读取输入的atom
    import re
    token = tokens.now()
    if re.match('^-?[1-9]\\d*$', r'' + token):
        tokens.next()
        return int(token)
    elif re.match('^(-?\\d+)(\\.\\d+)?$', r'' + token):
        tokens.next()
        return float(token)
    elif token == "nil":
        tokens.next()
        return None
    elif token == "true":
        tokens.next()
        return True
    elif token == "false":
        tokens.next()
        return False
    else:
        tokens.next()
        return str(token)


def read_list(tokens):
    # 读取输入的list
    li = []
    tokens.next()
    while tokens.now() != ')':
        li.append(read_tokens(tokens))
    tokens.next()
    return li


def read_tokens(tokens):
    # 读取输入的表达式
    token = tokens.now()
    if token == '(':
        return read_list(tokens)
    elif token == ')':
        raise SyntaxError('Error: ')
    else:
        return read_atom(tokens)


def read(inp_str):
    inp = tokenize(inp_str)
    tokens = READ(inp)
    return read_tokens(tokens)
