from urllib import request

import json

import random

import pymysql

def gs():
    url=input('请输入要查询的域名:')

    iplist =['120.25.203.182:7777','180.104.62.69:9000']

    px = request.ProxyHandler({'http':random.choice(iplist)})

    opener = request.build_opener(px)

    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36')]

    req = request.Request('https://www.1198.cn/ajax/SearchAjax.ashx?domain='+url+'&ischina=no&type=more&times=1550040860947')

    res = opener.open(req)

    html = res.read().decode('utf-8')

    j = json.loads(html)

    result = j[0]

    strle = result['result']

    final_result= strle[43:49]

    print(url)

    print(final_result)

    with open ('gs.txt','a') as f:

        f.write(url)

        f.write(' ')

        f.write(final_result)

        f.write('\n')


def data():
    connect = pymysql.Connect(
    host='localhost',
    port=3310,
    user='text',
    passwd='123456',
    db='python',
    charset='utf8'
)
    cursor=connect.cursor()
    sql = "INSERT INTO person (gs,result) VALUES ( url, final_result)"
    cursor.execute(sql)
    connect.commit()
    print('插入成功')
    cursor.close()
    connect.close()
    

print('请确定存在gs.txt文件夹')
print('网站关系每天查询次数有限制所以我用了ullib的代理（但是我不知道检查时ip还能不能用）')
for i in range(1000):
    k=input('输入1开始或继续查询，输入2结束程序:')
    if k=='1':
        gs()
        print('结果以写入文件gs.text')
        q=input('是否储存到数据库中（1=yes,2=no）')
        if q=='1':
            data()           
    else:
        break
    

    




