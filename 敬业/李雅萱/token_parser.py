def parser(tokens):

#把token——list解析成ast（抽象语法树）


    token_array = []

    counter = 0

    break_index = 0

    for i, p in enumerate(tokens):

        e = p.value

        if counter > 0:

            counter -= 1

            continue

        elif e == '[':

            v, break_index = parser(tokens[i+1:])#使用parser的递归来脱去括弧
            #并且根据表达式的优先级从索引小的到索引大的存储起来

            counter = break_index

            token_array.append(v)

        if e not in ',[]':

            token_array.append(p)

        elif e == ']':

            break_index = i + 1

            break

    return token_array, break_index