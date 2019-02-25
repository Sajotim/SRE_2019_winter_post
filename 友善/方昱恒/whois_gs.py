import whois
import threading
import pymysql

bit = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
       '7', '8', '9']


def task1(start, end):

    db = pymysql.connect("localhost", "root", "root", "whois", charset="utf8")
    cursor = db.cursor()

    b1 = start
    while b1 < end:
        b2 = 0
        while b2 < 36:
            b3 = 0
            while b3 < 36:
                b4 = -1
                while b4 < 35:
                    try:
                        b4 += 1
                        data = whois.whois(bit[b1] + bit[b2] + bit[b3] + bit[b4] + ".gs")

                        if data.get("status") == "No Object Found":
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b1] + bit[b2] + bit[b3] + bit[b4], 'Unregistered', bit[b1] + bit[b2] + bit[b3] + bit[b4], 'Unregistered')
                        else:
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b1] + bit[b2] + bit[b3] + bit[b4], 'Registered', bit[b1] + bit[b2] + bit[b3] + bit[b4], 'Registered')

                        try:
                            cursor.execute(sql1)
                            db.commit()
                        except:
                            db.rollback()

                        print(data)
                        print(bit[b1] + bit[b2] + bit[b3] + bit[b4] + ".gs" + "\n")
                    except:
                        b4 -= 1

                b3 += 1
            b2 += 1
        b1 += 1


def task2():

    db = pymysql.connect("localhost", "root", "root", "whois", charset="utf8")
    cursor = db.cursor()

    f1 = 0
    f2 = 0
    f3 = 0
    b1 = 0
    while b1 < 36:
        b2 = 0
        while b2 < 36:
            b3 = -1
            while b3 < 35:

                try:
                    if f2 == 1:
                        f3 = 1

                    b3 += 1
                    if f1 == 0 and f2 == 0 and f3 == 0:
                        data = whois.whois(bit[b3] + ".gs")

                        if data.get("status") == "No Object Found":
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b3], 'Unregistered', bit[b3], 'Unregistered')
                        else:
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b3], 'Registered', bit[b3], 'Registered')

                        try:
                            cursor.execute(sql1)
                            db.commit()
                        except:
                            db.rollback()

                        # print(data)
                        # print(bit[b1] + bit[b2] + bit[b3] + bit[b4] + ".gs" + "\n")

                    elif f1 == 0 and f2 != 0 and f3 != 0:
                        data = whois.whois(bit[b2] + bit[b3] + ".gs")

                        if data.get("status") == "No Object Found":
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b2] + bit[b3], 'Unregistered', bit[b2] + bit[b3], 'Unregistered')
                        else:
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b2] + bit[b3], 'Registered', bit[b2] + bit[b3], 'Registered')

                        try:
                            cursor.execute(sql1)
                            db.commit()
                        except:
                            db.rollback()



                    else:
                        data = whois.whois(bit[b1] + bit[b2] + bit[b3] + ".gs")

                        if data.get("status") == "No Object Found":
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b1] + bit[b2] + bit[b3], 'Unregistered', bit[b1] + bit[b2] + bit[b3], 'Unregistered')
                        else:
                            sql1 = """INSERT INTO whois_gs(Domain, WhetherRegistered)
                                   VALUES ('%s.gs', '%s') ON DUPLICATE KEY UPDATE Domain = '%s.gs', 
                                   WhetherRegistered = '%s'""" % (bit[b1] + bit[b2] + bit[b3], 'Registered', bit[b1] + bit[b2] + bit[b3], 'Registered')

                        try:
                            cursor.execute(sql1)
                            db.commit()
                        except:
                            db.rollback()
                except:
                    b3 -= 1

            if f2 != 0:
                b2 += 1
            if b3 == 35 and f2 == 0:
                f2 = 1
        if f1 != 0:
            b1 += 1
        if b2 == 35 and f1 == 0:
            f1 = 1


threads = []
t1 = threading.Thread(target=task1, args=(0, 4,))
threads.append(t1)
t2 = threading.Thread(target=task1, args=(5, 8,))
threads.append(t2)
t3 = threading.Thread(target=task1, args=(9, 12,))
threads.append(t3)
t4 = threading.Thread(target=task1, args=(13, 16,))
threads.append(t4)
t5 = threading.Thread(target=task1, args=(17, 20,))
threads.append(t5)
t6 = threading.Thread(target=task1, args=(21, 24,))
threads.append(t6)
t7 = threading.Thread(target=task1, args=(25, 28,))
threads.append(t7)
t8 = threading.Thread(target=task1, args=(29, 32,))
threads.append(t8)
t9 = threading.Thread(target=task1, args=(33, 36,))
threads.append(t9)
t10 = threading.Thread(target=task2)
threads.append(t10)

if __name__ == '__main__':

    for t in threads:
        t.start()
