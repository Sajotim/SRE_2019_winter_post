import itertools as its
def DictCreator(fname,n=2,domain='gs'):
    alphabet='abcdefghijklmnopqrstuvwxyz'
    list_str=[]
    listobj=its.product(alphabet,repeat=n)
    for i in listobj:
        raw =("".join(i)+'.'+domain+'\n')
        list_str.append(raw)
    #print(list)
    out="".join(list_str)
    #print(out)
    with open(fname,'w') as fo:
        fo.write(out)
def main():
    fname='list.txt'
    DictCreator(fname)
main()
