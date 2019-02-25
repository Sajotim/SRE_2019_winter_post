from time import sleep
from whois import whois
import datetime

    #'''
def _filter(flag,all,part):
    for v in part:
        a=v[:2]
        flag[transform_26(a)]=True

def transform_26(string):
    n,s=len(string)-1,0
    for i in string:
        s+=((int(i,36)-10)*26**n)
        n-=1
    return s

def main():
    tplt='{}{{"reg": "{}", "open_time": "{}"}}'

    with open('list.txt','r') as fo:
        origin=fo.readlines()
    flag = [False] * len(origin)
    try:
        with open('existed.txt','r') as fe: #1st time?
            existed=fe.readlines()
        _filter(flag,origin,existed)

    finally:
        f = open('existed.txt', 'a')
        fraw = open('raw.txt', 'a')
        for i, dm in enumerate(origin):
            dm=dm[:-1]
            sleep(0.5)
            if not flag[i]:
                print(dm)
                try:
                    raw = whois(dm)
                    print(raw, file=fraw)
                    if raw['registrar'] == None:
                        print(dm + ':' + 'available')
                    else:
                        key = tplt.format(dm+':',raw['registrar'], raw['expiration_date'].strftime('%Y-%m-%d'))
                        print(key, file=f)
                except:
                    print('error on query')
        f.close()
        fraw.close()

main()