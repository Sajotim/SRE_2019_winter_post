#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <sys/stat.h>

#define MAX_CLIENT_COUNT 10
#define BUF_SIZE 512
#define FILE_SIZE 256

void reuseaddr(int socketFd){
    //解决bind时 端口被占用错误，SO_REUSEADDR以便端口马上重用
    int on = 1;
    int ret = setsockopt(socketFd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
    if(ret == -1){
        printf("fail to setsocketopt");
        exit(1);
    }
}

int startsocket(int portNum){
    //创建套接字
    int httpsocket = socket(AF_INET, SOCK_STREAM, 0);
    if(httpsocket == -1){
        fprintf(stderr, "Error: can't create socket, errno is %d\n", errno);
        exit(1);
    }
    //bind
    struct sockaddr_in sockAddr;
    memset(&sockAddr, 0, sizeof(sockAddr));
    sockAddr.sin_family = AF_INET;
    sockAddr.sin_port = htons(portNum);
    sockAddr.sin_addr.s_addr = 0;//0.0.0.0表示本机
    reuseaddr(httpsocket);
    if(bind(httpsocket, (const struct sockaddr*)&sockAddr, sizeof(sockAddr)) == -1){
        printf("can't bind port %d\n", portNum);
        exit(1);
    }
    //listen
    if(listen(httpsocket, MAX_CLIENT_COUNT) == -1){
        fprintf(stderr, "can't listen port %d, error is %d\n", portNum, errno);
        exit(1);
    }

    return httpsocket;
}
int getbuf(int socketFd, char* buf, int buflen){
    //读取每一行socketFd，以\r\n结尾
	int byte = 0;
    char tmpchar;
    memset(buf, 0, buflen);
    while(read(socketFd, &tmpchar, 1) && byte < buflen){
        if(tmpchar == '\r'){
            if(recv(socketFd, &tmpchar, 1, MSG_PEEK) == -1){
                printf("Error: fail to recv char after \\r\n");
                exit(1);
            }
            if(tmpchar == '\n' && byte < buflen){
                read(socketFd, &tmpchar, 1);
                buf[byte++] = '\n';
                break;
            }
            buf[byte++] = '\r';
        }else
            buf[byte++] = tmpchar;
    }
    return byte;
}
void responsefile(int socketFd, int returnNum, char* filepath,
                 char* contenttype){
    //发送静态文件
    char sendbuf[BUF_SIZE] = {0};
    if(strcmp(filepath, "./") == 0) filepath = "./index.html";
    if(contenttype==NULL){
        int tppath = strlen(filepath) - 1;
        while(tppath > 0){
            if(filepath[tppath]!='.') --tppath;
            else break;
        }
        if(tppath){
            if(strcmp(filepath+tppath+1,"html")==0){
                contenttype = "text/html";
            }else if(strcmp(filepath+tppath+1,"txt")==0){
                contenttype = "text/plain";
            }else if(strcmp(filepath+tppath+1,"css")==0){
                contenttype = "text/css";
            }else if(strcmp(filepath+tppath+1,"js")==0){
                contenttype = "text/javascript";
            }else if(strcmp(filepath+tppath+1,"png")==0){
                contenttype = "image/png";
            }else if(strcmp(filepath+tppath+1,"gif")==0){
                contenttype = "image/gif";
            }else if(strcmp(filepath+tppath+1,"jpeg")==0){
                contenttype = "image/jpeg";
            }else if(strcmp(filepath+tppath+1,"bmp")==0){
                contenttype = "image/bmp";
            }else if(strcmp(filepath+tppath+1,"pdf")==0){
                contenttype = "application/pdf";
        	}
        }
    }
    FILE* pfile = fopen(filepath, "r");
    printf("%d %p : %s\n", returnNum, pfile, filepath);
    if(pfile==NULL){
        returnNum = 404;
        filepath = "./err404.html";
        contenttype = "text/html";
        pfile = fopen(filepath,"r");
    }
    switch(returnNum){
        case 200:
            sprintf(sendbuf,"HTTP/1.0 200 OK\r\n");
            break;
        case 400:
            sprintf(sendbuf,"HTTP/1.0 400 BAD REQUEST\r\n");
            break;
        case 404:
            sprintf(sendbuf,"HTTP/1.0 404 NOT FOUND\r\n");
            break;
        case 501:
            sprintf(sendbuf,"HTTP/1.0 501 Method Not Implemented\r\n");
            break;
        default:
            sprintf(sendbuf,"HTTP/1.0 %d Undefined Return Number\r\n",returnNum);
            break;
    }
    write(socketFd, sendbuf, strlen(sendbuf));

    sprintf(sendbuf, "Content-Type: %s\r\n", contenttype);
    write(socketFd, sendbuf, strlen(sendbuf));
    write(socketFd, "\r\n", strlen("\r\n"));

    int readdatalen = 0;
    while((readdatalen = fread(sendbuf, 1, BUF_SIZE, pfile))!=0){
            write(socketFd, sendbuf, readdatalen);
            sendbuf[readdatalen] = 0;
        }
    fclose(pfile);
}
void execCGI(int socketFd,char* requestFilePath,char* requestQueryString){//获取动态页面
    int pipefd[2];
    printf("###%s\n",requestQueryString);
    if(pipe(pipefd)==-1){
        fprintf(stderr, "ERROR : 创建匿名管道失败，失败号 %d\n", errno);
        return;
    }
    //先发送 http 协议信息头
    write(socketFd,"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n", strlen("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"));

    int pid = fork();
    if(pid==0){
        // 子进程执行 将输出重定位到管道的写
        dup2(pipefd[1],1);
        // execl的参数可变，但最好设置最后一个参数为NULL,作为哨兵,否则会有警告
        execl(requestFilePath, requestFilePath, requestQueryString, NULL);
    }else{
        // 父进程执行 对于管道只读不写
        char sendData[BUF_SIZE] = {0};
        int readLength = 0;
        do{
            readLength = read(pipefd[0], sendData, BUF_SIZE);
            if(readLength==0)break;
            write(socketFd, sendData, readLength);
        }while(readLength==BUF_SIZE);
        waitpid(pid,NULL,0);
    }
}
void recv_socket(int socketFd){
	int brosocket = socketFd;
    char recvbuf[BUF_SIZE + 1] = {0};
    int contentlen = 0;
    enum method{REQUEST_GET, REQUEST_POST, REQUEST_UNDEFINED};
    enum method requesttype = REQUEST_UNDEFINED;

    #define FILE_PATH_LEN 128// 定义存放请求文件名的内存块
    #define QUERY_STRING_LEN 128// 定义存放查询参数字符串的内存库
    char requestfp[FILE_PATH_LEN] = {0};
    char requestquery[QUERY_STRING_LEN] = {0};
    int isXfile = 0;
    while(getbuf(brosocket, recvbuf, BUF_SIZE)){
        if(strcmp(recvbuf, "\n") == 0) {break;}
        if(requesttype == REQUEST_UNDEFINED){
            int pfilename = 0;
            int pquerystring = 0;
            int precvbuf = 0;

            if(strncmp(recvbuf, "GET", 3) == 0){
                requesttype = REQUEST_GET;
                precvbuf = 4;
            }else if(strncmp(recvbuf, "POST", 4) == 0){
                requesttype = REQUEST_POST;
                precvbuf = 5;
            }
            if(precvbuf){
                requestfp[pfilename++] = '.';
                while(pfilename<FILE_PATH_LEN && recvbuf[precvbuf]
                      && recvbuf[precvbuf]!=' ' && recvbuf[precvbuf]!='?'){
                    requestfp[pfilename++] = recvbuf[precvbuf++];
                }
                if(pfilename<FILE_PATH_LEN && recvbuf[precvbuf]=='?'){
                    ++precvbuf;
                    while(pquerystring<QUERY_STRING_LEN &&
                          recvbuf[precvbuf] && recvbuf[precvbuf]!=' '){
                        requestquery[pquerystring++] = recvbuf[precvbuf++];
                    }
                }
            }else if(requesttype==REQUEST_POST){
                if(strncmp(recvbuf, "Content-Length:", 15) == 0) contentlen = atoi(recvbuf+15);
            }
        }
    }
    //如果是REQUEST_POST类型,在读取contentlen长度的数据
    if(requesttype==REQUEST_POST && contentlen){
        if(contentlen > QUERY_STRING_LEN){
            fprintf(stderr, "Query string buffer is smaller than content length\n");
            contentlen = QUERY_STRING_LEN;
        }
        read(brosocket, requestquery, contentlen);
    }
    // 判断请求的文件是否是文件夹
    struct stat fileInfo;
    stat(requestfp,&fileInfo);
    if(S_ISDIR(fileInfo.st_mode)){}//是文件夹的情况
    else if(access(requestfp,X_OK)==0){
    isXfile = 1;//非文件夹的情况 判断请求的文件是否是可执行文件
	}
    switch(requesttype){
        case REQUEST_GET:
            if(isXfile==0) responsefile(brosocket,200,requestfp,NULL);
            else execCGI(brosocket,requestfp,requestquery);
            break;
        case REQUEST_POST:
            if(contentlen==0){
                    responsefile(brosocket,400,"./err400.html","text/html");
                    break;
                }else execCGI(brosocket,requestfp,requestquery);
            break;
        case REQUEST_UNDEFINED:
            responsefile(brosocket, 501, "./err501.html","text/html");
            break;
        default:
            break;
    }

    close(brosocket);
}
int main(int argc, char* argv[]){
    int portNum = 2080;
    int httpsocket = startsocket(portNum);

    while(1){
        struct sockaddr_in broAddr; //browser socket addr
        int broLen = sizeof(broAddr);
        int brosocket = accept(httpsocket, (struct sockaddr*)&broAddr, &broLen);
        if(brosocket == -1){
            fprintf(stderr, "fail to accept, error is %d", errno);
            exit(1);
        }
        printf("%s:%d linked!\n", inet_ntoa(broAddr.sin_addr), broAddr.sin_port);
        //inet_ntoa()将二进制ip转换位十进制ip
		recv_socket(brosocket);
    }
    close(httpsocket);
    return 0;
}

