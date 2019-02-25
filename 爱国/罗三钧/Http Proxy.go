package main

import (
	"bytes"
	"fmt"
	"io"//io.Reader
	"log"//日志
	"net"//I/O接口
	"net/url"//url的操作
	"strings" //判断头信息
)

func main() {
	//Go的log包 自带时间戳 fmt.Println也可以
	log.SetFlags(log.LstdFlags|log.Lshortfile)//时间+文件名+源代码所在行
	//net包监听 在8080口上监听
	l, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Panic(err)
	}
	//Listener接口的Accept方法 阻塞等待
	for {
		client, err := l.Accept()
		if err != nil {
			log.Panic(err)
		}

		//接收到的数据交hcr处理
		go handleClientRequest(client)
	}
}
//hcr设定
func handleClientRequest(client net.Conn) {
	if client == nil {
		return
	}
	defer client.Close()
//解析http头信息
	var b [1024]byte
	n, err := client.Read(b[:])//自带的解析方法
	if err != nil {
		log.Println(err)
		return
	}
	var method, host, address string
	_, _ = fmt.Sscanf(string(b[:bytes.IndexByte(b[:], '\n')]), "%s%s", &method, &host)
	hostPortURL, err := url.Parse(host)
	if err != nil {
		log.Println(err)
		return
	}
//远程服务器信息
	if hostPortURL.Opaque == "443" { //https
		address = hostPortURL.Scheme + ":443"
	} else { //http
		if strings.Index(hostPortURL.Host, ":") == -1 { //host默认80
			address = hostPortURL.Host + ":80"
		} else {
			address = hostPortURL.Host
		}
	}
/*Maybe
ip:port
hostname:port
domainname:port
 */

	//代理服务器与目标服务器建立tcp连接
	server, err := net.Dial("tcp", address)
	if err != nil {
		log.Println(err)
		return
	}
	//确认
	if method == "CONNECT" {
		_, _ = fmt.Fprint(client, "HTTP/1.1 200 Connection Established\r\n\r\n")//双r双n（Attention！
	} else {
		_, _ = server.Write(b[:n])
	}
	//转发
	go io.Copy(server, client)
	_, _ = io.Copy(client, server)
}
