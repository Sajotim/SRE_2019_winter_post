"""
this is a module for computing the gap between expiration_date and today
it will input an origin file contains one data a line ,end with date
output a sorted list file add gap of days at the begining of line.
"""

from datetime import datetime

in_file,out_file='result.txt','domain.txt'
span=30

def Caltime_now(now,date):
    future = datetime.strptime(date, '%Y-%m-%d')
    gap = future-now    #type:'timedelta'
    return gap.days + 1   #future is count from 00:00:00



def main():
    n = datetime.now()
    n_str=n.strftime('%Y-%m-%d')
    print(n_str)

    with open(in_file,'r') as f:
        raw=f.readlines()

    #hash
    r_span=0    #日期字符串右端字符数
    d={}
    for v in raw:
        if v[-11-r_span:-1-r_span]==' available':
            d[v[:-1]] = -1
        else:
            gap=Caltime_now(n,v[-11-r_span:-1-r_span])
            if 0<=gap<=span: d[v[:-1]] = gap

    sorted_d=sorted(zip(d.values(),d.keys()))

    f=open(out_file,'w')
    print(n_str,file=f)
    for k,v in sorted_d:
        print('%02d'%k+' '+v,file=f)
    f.close()
if __name__ == '__main__':
    main()