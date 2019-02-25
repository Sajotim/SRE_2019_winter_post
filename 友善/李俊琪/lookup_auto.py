import threading
import time
import requests
from itertools import chain,product
from queue import Queue

charset='0123456789abcdefghijklmnopqrstuvwxyz'#用来生成所有短域名组合的


def auto_lookup_short_domain_name(INPUT):
    q_auto=Queue(6)#最大8个 省的生成器生成太多列表占内存
    gen_names=bruteforce(charset,4)#包含短域名组合的生成器
    global file_auto
    file_auto=open('auto_check.csv','w')  #打开文件，以供读写用

        
    def producer():#最简单的生产消费者模型，生成域名序列 拿来POST
        while 1:
            name_list=[]
            for i in range(500):     #单个线程一次POST500个域名 有很多timeout
                name_list.append(next(gen_names)+'.gs')
            q_auto.put(name_list)

    def consumer():#消费者 不断尝试获取生成的列表 去POST
        while 1:
            multi_inquiry(q_auto.get())
            time.sleep(4.2)       #休息几秒防止被封。API每分钟请求限制60次
                                  #实际因为网速较慢，这个数值应该可以再改小一点


    t_producer=threading.Thread(target=producer,daemon=True)
    t_producer.start()
    for i in range(6):      #线程池放6个线程来POST
        t_consumer=threading.Thread(target=consumer,daemon=True)
        t_consumer.start() 


def bruteforce(charset, maxlength): #从StackOverflow抄来的密码穷举生成器，拿来生成域名
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))



def multi_inquiry(*args): #POST查询域名，写入csv

    baseurl="https://api.godaddy.com/v1/domains/available"
    header={'accept':'application/json','Authorization':'sso-key e42s1CST1356_Bp5jvuAH2iU5CJeyGWZCiA:Bp7TvXYeCk6YR2XZuAFXzn'}
    while 1:    
        try:
            r=requests.post(baseurl,headers=header,json=args[0],timeout=4)
        except requests.exceptions.Timeout:#超时立即重新提交
            print('Timeout. Will try again.')
        except requests.exceptions.ConnectionError:#断网，等5秒再重新提交
            print('Connection error. Will try again 5 seconds later')
            time.sleep(5)
        else:
            r_obj=r.json()
            if 'domains' in r_obj and r_obj['domains'] !=None: #判断是不是错误消息
                for item0 in r_obj['domains']:
                    file_auto.write("{},availability,{}\n".format(item0['domain'],item0['available']))
                    file_auto.flush()   #这么不断的flush应该很蠢，不过目前不知道怎么做更好
                print('success')    #测试消息
                break
            else:
                print('Unknown error. Will try again')#被发错误消息 休息一下
                time.sleep(3)

