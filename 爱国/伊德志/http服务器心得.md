## http服务器心得

1.用C语言写一个http服务器

在Windows中使用

```c
# include <winsock2.h>

#pragma comment(lib, "ws2_32.lib") 
```

在Linux中使用

```c
#include <sys/socket.h>
#include <sys/types.h>
...
```

运用socket方法

2.

先在网上查找许多c语言写HTTPsever的代码和思路

也把《图解http》看了一遍  了解一点HTTP协议

在网上看到一个最简单的python写的sever只有几行代码：

```python
import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("severing at port", PORT)
    httpd.serve_forever()
```

我找到的C语言写的最少也有100多行。。。

方法是创建一个socket，用bind()绑定端口，然后开始监听listen()，等待客户端的请求accept()

 3.

困难：最困难的事就是该怎么写，在网上找了好几份不同的代码，但是我能直接通过编译的只有1，2份。我也不能就认为其他代码有问题，所幸，大部分思路还是相似的。其中一篇更是对socket方法的各个函数做了注解，特别感谢作者。在读代码过程中，遇到过如memset(),atoi()之类的陌生函数，还有对有无符号的int型进行typedef的写法，size_t,ssize_t。遇到很多新东西，只能一个一个去百度，但过程还是很充实。不停的修改，不停的增减内容。

心得：之所以选择C语言，也是想能复习一下C。如果选择python，代码应该会简单很多。在准备作业的过程中，看了一遍《图解http》，对HTTP协议有了更深的了解。在找代码和写代码过程中也让我体会到了不一样的C，让从以前只能用C做做C题库的我，对C有了其他认识，它其实能做更多的事情。在遇到问题时，有了搜索引擎真的能有效率的解决大部分问题。

遗憾：程序在Linux中虽然成功通过了编译并运行，但在运行过程中会出现**段错误（核心已转储）**字样，导致程序运行中途就会断掉，但是还是能作为服务器使用，虽然在https://blog.csdn.net/youngys123/article/details/79804840中解释了原因和提供了处理方法，但是我还是没能解决掉这个问题。所以这次作业没完全达到心理预期。



主要参考：

https://blog.csdn.net/HES_C/article/details/82862521

https://blog.csdn.net/u012662731/article/details/53025046