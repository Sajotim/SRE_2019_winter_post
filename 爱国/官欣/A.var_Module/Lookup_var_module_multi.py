"""
get info from whois server directly.
"""
from time import sleep
from whois import whois
from multiprocessing import Process
in_file='list.txt'
out1,out2='existed.txt','raw.txt'

#标记出行首对应索引
def _filter(flag,part):
    for v in part:
        a=v[:2]
        flag[transform_26(a)]=True

#根据给定字符串返回可索引的唯一值（26进制，hash?）
def transform_26(string):
    n,s=len(string)-1,0
    for i in string:
        s+=((int(i,36)-10)*26**n)
        n-=1
    return s


tplt='{}{{"reg": "{}", "open_time": "{}"}}'
f = open(out1, 'a')
fraw = open(out2, 'a')
def query(dm):
    print(dm)
    try:
        raw = whois(dm)
        print(raw, file=fraw)
        if raw['registrar'] == None:
            print(dm + ':' + 'available')
        else:
            key = tplt.format(dm + ':', raw['registrar'], raw['expiration_date'].strftime('%Y-%m-%d'))
            print(key, file=f)
    except:
        print('error on query')

if __name__ =='__main__':

    with open(in_file,'r') as fo:
        origin=fo.readlines()
    flag = [False] * len(origin)

    #第一次运行时不存在out1
    try:
        with open(out1,'r') as fe: #1st time?
            existed=fe.readlines()
        _filter(flag,existed)

    finally:
        pass

    #逆序剔除掉已处理域名
    for i in range(675, -1, -1):
        if flag[i]: origin.pop(i)

    for dm in origin:
        dm=dm[:-1]
        sleep(0.4)
        p = Process(target=query, args=(dm,))
        p.start()
    f.close()
    fraw.close()
