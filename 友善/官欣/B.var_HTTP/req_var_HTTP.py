"""
this is a module for crawling static info var some websites' port:80.
it will store [Domain_name, Registrar, Registry Expiry Date] in a line if acquired,
or it will store [Domain_name, 'Available']
"""

import requests
import bs4
from bs4 import BeautifulSoup
from time import sleep

in_file,out_file='words.txt','result.txt'

def getHTML(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ''
def fillwlist(wlist,HTML):
    soup= BeautifulSoup(HTML,'html.parser')
    ul=soup.find('ul')
    if isinstance(ul,bs4.element.Tag):
        lis=ul('li')
        temp=[]

        for i in range(len(lis)):
            if lis[i].contents[0].string=='域名 : ': temp.append(lis[i].contents[2].string)
            if lis[i].contents[0].string == '注册商 : ': temp.append(lis[i].contents[2].string)
            if lis[i].contents[0].string == '到期日期 : ': temp.append(lis[i].contents[2].string[:10])
        if len(temp)==1: temp.append('available')

        wlist.append(temp)


def storwlist(wlist):
    f=open(out_file,'a')
    for line in wlist:
        print(', '.join(line),file=f)
    f.close()
def query(url,dm):
    dm0='.gs'
    winfo=[]
    print(url+dm+dm0,end='')

    HTML=getHTML(url+dm+dm0)
    fillwlist(winfo,HTML)
    print(winfo)
    storwlist(winfo)
def main():
    url_1 = 'http://www.whoisip.cn/'
    with open(in_file,'r') as f:
        origin=f.readlines()
    for dm in origin:
        dm=dm[:-1]
        sleep(0.4)

        query(url_1,dm)