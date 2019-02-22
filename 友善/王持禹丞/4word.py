f=open("4word.txt",'a')
chars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for a in range(0,26):
    ch0=chars[a]
    for b in range(0,26):
        ch1=chars[b]
        for c in range(0,26):
            ch2=chars[c]
            for d in range(0,26):
                ch3=chars[d]
                f.write(ch0+ch1+ch2+ch3+'\n')
f.close()
