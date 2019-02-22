from apply import apply


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