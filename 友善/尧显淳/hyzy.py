#!/usr/bin/env python
# -*-coding:utf8-*-

# name__尧显淳
# Student ID__2018213993

import requests, random, re, winsound, time
from multiprocessing import Process
# import mysql
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 加个头。


def headers(domain):
    headers = {'Referer':'http://whois.chinaz.com/'.format(domain),
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    return headers
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 用来保存还已注册的域名及对应的过期时间。


def savedata1(domain, time):
    # 保存到SQL数据库。
    # db = pymysql.connect(host='localhost', user='root', password='52yxc1314', port=3306, db='domain_list')
    # cursor = db.cursor()
    # sql = "INSERT INTO registered(domain , deadline)\
    #             VALUES (%s , %s )"
    # try:
    #     cursor.execute(sql, (domain, time))
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()

    # 保存在本地.txt文本中。
    message = '域名：{}\t\t过期时间：{}'.format(domain, time)
    with open('registered.txt', 'a+') as f:
        f.write('{}\n'.format(message))
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 用来保存还未注册的域名。


def savedata2(domain):
    # 保存到SQL数据库。
    # db = pymysql.connect(host='localhost', user='root', password='52yxc1314', port=3306, db='domain_list')
    # cursor = db.cursor()
    # sql = "INSERT INTO unregistered(domain)\
    #           VALUES (%s)"
    # try:
    #     cursor.execute(sql, domain)
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()

    # 保存在本地.txt文本中。
    message = '域名：{}'.format(domain)
    with open('unregistered.txt', 'a+') as f:
        f.write('{}\n'.format(message))
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 用来保存因为“请求过于频繁”而导致请求失败的域名。


def savedata3(domain):
    # 保存到SQL数据库。
    # db = pymysql.connect(host='localhost', user='root', password='52yxc1314', port=3306, db='domain_list')
    # cursor = db.cursor()
    # sql = "INSERT INTO errors(domain)\
    #               VALUES (%s)"
    # try:
    #     cursor.execute(sql,domain)
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()

    # 保存在本地.txt文本中。
    with open('errors.txt', 'a+') as f:
        f.write('{}\n'.format(domain))
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 用来保存值得"抢注"的域名。


def savedata4(domain):
    # 保存到SQL数据库。
    # db = pymysql.connect(host='localhost', user='root', password='52yxc1314', port=3306, db='domain_list')
    # cursor = db.cursor()
    # sql = "INSERT INTO good_domain(domain)\
    #               VALUES (%s)"
    # try:
    #     cursor.execute(sql, domain)
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()

    # 保存在本地.txt文本中。
    message = '域名：{}'.format(domain)
    with open('good_domain.txt', 'a+') as f:
        f.write('{}\n'.format(message))
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 清空指定文档。


def cleartxt(name):
    with open(name, 'w') as f:
        f.truncate()
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 读取指定文档。


def readtxt(name):
    with open(name, 'r') as f:
        data = []
        for s in f.readlines():
            data.append(s)
    return data
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 调用该函数可获得从'aaaa'-'zzzz'遍历的域名合集。


def getdomain(hz):
    a = list(map(chr, range(ord('a'), ord('z') + 1)))
    words = ['', '', '', '']
    sum = []
    i = 0
    m = 0
    n = 0
    k = 0
    while i < 26:
        words[0] = a[i]
        i += 1
        k = 0
        m = 0
        n = 0
        while k < 26:
            words[1] = a[k]
            k += 1
            m = 0
            n = 0
            while m < 26:
                words[2] = a[m]
                m += 1
                n = 0
                while n < 26:
                    words[3] = a[n]
                    n += 1
                    s = ''.join(words) + hz   # 这里组合成域名。
                    sum.append(s)
    return sum
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 该函数用来设定你想要的域名规则。当前设置为'a()()b'格式，其中()()表示从'aa'-'zz'。


def setdomain(hz):
    a = list(map(chr, range(ord('a'), ord('z') + 1)))
    words = ['', '']
    sum = []
    i = 0
    k = 0
    while i < 26:
        words[0] = a[i]
        i += 1
        k = 0
        while k < 26:
            words[1] = a[k]
            k += 1
            s = 'a'+''.join(words) + 'b' + hz    # 这里组合成域名。
            sum.append(s)
    return sum
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 当遇到牛逼的域名时，该函数可做到提示的作用！牛不牛逼看怎么设置，当前设置为域名中有 重复的字母 时则发出报警声并给出提示。


def ring(domain):
    s = list(domain[:4])    # 得到域名前四位。
    if len(s) != len(set(s)):   # 进行判断看是否有相同的字母，如果有，则提示并返回Ture，否则返回False。
        print('哇！域名"{}"似乎不错，试试抢注吧！'.format(domain))
        winsound.Beep(600, 700)     # 发出声音进行提示。
        return True
    else:
        return False
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# 检查域名状态并进行相应的措施。


def cheakdomain(domain):
    url = 'http://whois.chinaz.com/{}'.format(domain)          # 检查该域名的状态。
    response = requests.get(url, headers=headers(domain)).text             # 得到响应。
    s = re.search('<div\sclass.*?过期时间.*?<span>(.*?)</span>', response, re.S)         # 用正则查询过期时间。
    if s:            # 如果过期时间存在，则说明该域名被注册。
        time = s.group(1)              # 得到过期时间。
        print('域名"{}"已被注册！过期时间：{}'.format(domain, time))      # 给出信息。
        savedata1(domain, time)   # 保存数据。
    else:   # 如果不存在，则有两种情况:1.请求繁忙错误；2.该域名还未注册。
        try:     # 尝试查询是否有错误信息。
            error = re.search('<div.*?tc\sptb10\scol.*?>(.*?)<a', response, re.S).group(1)[:8]    # 用正则检查是否是因为“请求繁忙”。
            if error.find('您的请求') != -1:    # 如果找到了繁忙错误，则给出提示并保存。
                print('当前访问"{}"。您的请求过于频繁，请稍后再试！'.format(domain))
                savedata3(domain)
        except:    # 剩下的情况就是还未注册。
            print('域名"{}"还未注册！'.format(domain))
            q = ring(domain)   # 对域名是否值得“抢注”进行判断，根据情况分别保存在两个文本中。
            if q == True:
                savedata4(domain)
            else:
                savedata2(domain)
# ------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    s = input('请输入想查询的域名后缀(支持".gs"、".com"):')
    if s == '.gs' or s == '.com':    # 对输入值进行判断,如果正确则执行，错误则给出相应提示。
        a = setdomain(s)             # 得到大量域名，'setdomain'可以得到自定义域名，getdomain得到'aaaa'-'zzzz'的遍历域名。
        for i in a:
            p = Process(target=cheakdomain, args=(i,))    # 开起子进程加快工作效率。
            p.start()
            time.sleep(1)            # 限时,防止因为频繁访问导致错误。
        for b in range(3):             # 这个循坏用来对由于因“请求繁忙”错误信息而导致访问失败的域名重新进行访问。
            x = readtxt('errors.txt')            # 从相应文档中取得数据。
            cleartxt('errors.txt')                # 清空相应文档中的数据，以供接下来重新保存。
            for c in x:
                d = c[:4] + s                    # 这里得到域名。
                po = Process(target=cheakdomain, args=(d,))
                po.start()
                time.sleep(1)
    else:
        print('错误！请选择".gs"和".com"中的一种！')       # 相应提示。
