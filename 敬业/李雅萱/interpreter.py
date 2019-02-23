from apply import apply


def test():
    print('run main')

    c = """

    [set a [+ 1 51]]

    [log a]



     



    [set b [plus 1 6]]

    [log b]



     
    
        """

    console = apply(c)


def main():
    test()


if __name__ == '__main__':
    main()