# 能自行爱国的Http代理

完成度：Http代理 能自行爱国

参考：https://github.com/snail007/goproxy

因为最近在看go相关的内容 就用go来完成这次的考核

1.go的net包用来作监听很方便 net.Listen

Listener接口的Accept方法来接受客户端的连接数据

交给下面的handleClientRequest来处理

2.然后就是解析请求 获取ip和端口

在计算机网络中 可以学习到HTTP/HTTPS协议的头信息

我们需要的都在头信息的第一行 他们都是用空格隔开

Ex:CONNECT www.google.com:443 HTTP/1.1   

http头信息没有端口号 默认80 多了http://

分析完了就能从http头信息中获取请求的url和method

对url进行解析 获取远程服务器信息

3.建立连接 CONNECT要进行回应

开两个goroutines是因为这里读和写不能在同一个协程中进行 

他们是同步的 双协程的生产者和消费者



Go因为有很多成熟的包写起来不是很难

但是在写的过程中感觉

自己真的是太弟弟了

socks5中解析ipv6地址让我非常自闭 我离自己想要的水平还有很远

我也觉得自己计网没有认真看

希望新的一个学期自己能做到 少水群 多看书

Sajo

2019.2.24



