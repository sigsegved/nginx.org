# nginx Windows版使用说明

**Revision:** 1  
**Language:** cn


nginx的Windows版本使用原生Win32 API（非Cygwin模拟层）。当前nginx/Windows只使用*select*作为通知方法，所以不要期待它有很高的性能和扩展性。鉴于这点和一些已知问题，nginx/Windows目前还处于*beta*阶段。nginx/Windows和Unix版本相比，功能几乎已经齐全，除了XSLT过滤器、图像过滤器、GeoIP模块和嵌入Perl语言支持以外。

安装nginx/Windows，需要[下载](../download.html)最新的开发版本，因为开发分支上包含了所有已知的问题修复，尤其是针对Windows版本的问题修复。解压缩下载得到的zip文件，进入nginx-目录，运行nginx。下面给出一个在C盘根目录下安装的例子：


```
cd c:\
unzip nginx-.zip
cd nginx-
start nginx
```


可以在命令行运行`tasklist`命令来查看nginx进程：


```
C:\nginx->tasklist /fi "imagename eq nginx.exe"

Image Name           PID Session Name     Session#    Mem Usage
=============== ======== ============== ========== ============
nginx.exe            652 Console                 0      2 780 K
nginx.exe           1332 Console                 0      3 112 K
```


其中一个是主进程，另一个是工作进程。如果nginx没有启动，请查看`logs\error.log`文件以寻找失败原因。如果日志文件不存在，那失败原因会记录在Windows事件日志中。如果某次请求没有展示预想的页面，而是展示了错误页面，也请查看`logs\error.log`文件。

nginx/Windows使用工作目录作为前缀将配置文件中设置的相对目录补齐。就上面安装的例子而言，工作目录应该是`C:\nginx-\`（工作目录基本上与运行文件所在的目录相同）。配置文件中的目录请使用“/”，而不是“\”做目录分隔：


```
access_log   logs/site.log;
root         C:/web/html;
```

nginx/Windows作为标准控制台应用运行，而不是系统服务。可以用下面的命令控制：


| nginx -s stop | 快速退出 |
| --- | --- |
| nginx -s quit | 优雅退出 |
| nginx -s reload | 更换配置，启动新的工作进程，优雅的关闭以往的工作进程 |
| nginx -s reopen | 重新打开日志文件 |

## 已知问题 {#known_issues}

- 虽然可以启动若干工作进程运行，实际上只有一个进程在处理请求所有请求。
- 一个工作进程只能处理不超过1024个并发连接。
- 缓存和其他需要共享内存支持的模块在Windows Vista及后续版本的操作系统中无法工作，因为在这些操作系统中，地址空间的布局是随机的。

## 日后可能加强的功能 {#possible_future_enhancements}

- 作为系统服务运行。
- 使用“I/O完成端口”作为事件模型。
- 使用单工作进程多线程的模型。
