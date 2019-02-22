import requests
from bs4 import BeautifulSoup
import time
#查询是否注册
def check(domain):
    url = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=%s"%domain
    html = requests.get(url)
    bsj = BeautifulSoup(html.text,"lxml")
    word = bsj.find("original")
    if word != None:
        num = word.get_text()[:3]
        if num == '210':
            print("%s可以注册"%domain)
        elif num == "211":
            print("%s域名已注册"%domain)
        else:
            print("%s不可注册"%domain)
        return num
    else:
        print("发生未知错误")
        return None

def domainlist(namepart):
    # 获取4位单词列表
    text = []
    with open('4word.txt', 'r') as w:
        words = w.readlines()
    for word in words:
        text.append(word.strip())
    # 生成域名列表
    names = []
    for word in text:
        name = namepart+word
        names.append(name)
    return names

#保存可注册域名
def domain(namepart,houzui):
    sucessfullist = []
    names = domainlist(namepart)
    for name in names:
        domain = name+'.'+houzui
        time.sleep(1)
        num = check(domain)
        if num != None:
            if num == '210':
                sucessfullist.append(domain)
        else:
            break
    with open('sucessfullist.txt','w+') as ok:
        for k in sucessfullist:
            s = k+'\n'
            ok.write(s)
    return sucessfullist

if __name__ == '__main__':
    namepart = input('建议回车跳过，适用于xx.xx.后缀：')
    houzui = input('输入域名后缀: ')
    sucessfullist = domain(namepart,houzui)