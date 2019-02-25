import whois
import threading
var = ' 1234567890abcdefghijklmnopqrstuvwxyz'

def find2(x):
    a=6*(x-1)+1
    b=6*x+1
    for x in range(a,b):
        for y in range(0,37):
            for z in range(0,37):
                for e in range(0,37):
                    t=var[x]+var[y]+var[z]+var[e]
                    t=t+'.gs'
                    try:
                        print("finding whois information..."+"    "+t)
                        data = whois.whois(t)
                        file = open('D:/1/b.txt', 'a', encoding='utf-8')
                        print(data)
                        try:
                            print(t["whois_server"] + "ssaaff")
                        except:
                            z=t["Domain Name"]
                            file.writelines("\n",z)
                        print("whois query successfully!")  # print data return data except: print "whois query fail!" pass
                    except:
                        print("whois query fail!")
                        pass


threads = []
t1 = threading.Thread(target=find2, args=(1,))
threads.append(t1)
t2 = threading.Thread(target=find2, args=(2,))
threads.append(t2)
t3 = threading.Thread(target=find2, args=(3,))
threads.append(t3)
t4 = threading.Thread(target=find2, args=(4,))
threads.append(t4)
t5 = threading.Thread(target=find2, args=(5,))
threads.append(t5)
t6 = threading.Thread(target=find2, args=(6,))
threads.append(t6)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(False)
        t.start()

