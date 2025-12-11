# ngx_http_core_module 模块

**Translator:** cfsego  
**Revision:** 13  
**Language:** cn


## 指令 {#directives}



    on |
    off |
    sendfile
off
http
server
location
0.8.11


在FreeBSD和Linux操作系统上启用或者禁用异步文件I/O(AIO)。



从FreeBSD 4.3版本开始，可以使用AIO。AIO既可以静态链接到内核中：

options VFS_AIO

又可以作为内核模块动态加载：

kldload aio




在FreeBSD第5版和第6版，静态启动AIO，或者在系统启动时动态加载AIO，都会触发网络子系统使用一把大锁，进而对整个系统的性能造成负面影响。
这个限制在2009年发布的FreeBSD 6.4稳定版和FreeBSD 7中被消除。
虽然如此，仍有方法在5.3及以上版本的FreeBSD中开启AIO而不触发网络子系统的大锁，那就是在内核启动以后加载AIO模块。
使用这种时，/var/log/messages中会出现下面信息，

WARNING: Network stack Giant-free, but aio requires Giant.
Consider adding 'options NET_WITH_GIANT' or setting debug.mpsafenet=0

但可以安全的忽略它。

使用AIO大锁的是FreeBSD套接字上的aio_read和aio_write异步操作。但是nginx仅仅在磁盘I/O使用AIO，所以不会出现问题。




为了让AIO工作，需要关闭：

location /video/ {
    sendfile       off;
    aio            on;
    output_buffers 1 64k;
}




不过，从FreeBSD 5.2.1版和nginx 0.8.12版开始，AIO也可以为sendfile预读数据：

location /video/ {
    sendfile       on;
    tcp_nopush     on;
    aio            sendfile;
}


这个配置使nginx在调用sendfile时带SF_NODISKIO参数，
那么sendfile在数据没有读入内存的时候，就不会阻塞在磁盘I/O上，而是直接返回报告；接着nginx就读这个一字节报告，然后初始化异步数据。
FreeBSD内核接着会读取文件的开始128K字节到内存，而后续的读取只会以16K的单位来进行。
这个性质可以使用指令来调节。



从Linux内核2.6.22版开始，也可以使用AIO。但必须同时开启，否则读取将是阻塞的：

location /video/ {
    aio            on;
    directio       512;
    output_buffers 1 128k;
}




在Linux上，只在读取的块的边界对齐512字节（在XFS上是4K字节）时才有用。在读取文件尾部时，
如果没有对齐，AIO读取还是阻塞的。同样的情况(如果数据的开始或者结尾未对齐时，读取也是阻塞的)
也发生在含有byte range头的请求中，或者发生在不是从头开始的FLV请求中。
没有必要手动关闭，因为如果使用了，它就会自动关闭。




path

location


定义指定路径的替换路径。比如下面配置

location /i/ {
    alias /data/w3/images/;
}

“/i/top.gif”将由/data/w3/images/top.gif文件来响应。



path的值可以包含变量，但不能使用$document_root和$realpath_root这两个变量。



如果在定义了正则表达式的路径中使用了alias，那么正则表达式中应该含有匹配组，
并且alias应该引用这些匹配组(0.7.40版)来组成一个完整的文件路径，比如：

location ~ ^/users/(.+\.(?:gif|jpe?g|png))$ {
    alias /data/w3/images/$1;
}




如果路径对应指令path值的最后一部分：

location /images/ {
    alias /data/w3/images/;
}

最好换用指令：

location /images/ {
    root /data/w3;
}





on | off
on
http
server
location


允许关闭HTTP/1.1中的分块传输编码。在客户端软件不支持分块传输编码的时候，这条指令才有用。





size
8k|16k
http
server
location


设置读取客户端请求正文的缓冲容量。如果请求正文大于缓冲容量，整个正文或者正文的一部分将写入临时文件。
缓冲大小默认等于两块内存页的大小，在x86平台、其他32位平台和x86-64平台，这个值是8K。在其他64位平台，这个值一般是16K。





    on |
    clean |
    off
off
http
server
location


决定nginx是否将客户端请求正文整个写入文件。这条指令在调试时，或者使用$request_body_file变量时，
或者使用ngx_http_perl_module模块的
$r->request_body_file方法时都可以使用。



当指令值设置为on时，请求处理结束后不会删除临时文件。



当指令值设置为clean时，请求处理结束后会删除临时文件。




on | off
off
http
server
location


决定nginx将整个客户端请求正文保存在一块缓冲中。
这条指令推荐在使用$request_body变量时使用，可以节省引入的拷贝操作。





    path
    [level1
    [level2
    [level3]]]
client_body_temp
http
server
location


定义存储客户端请求正文的临时文件的目录。
支持在指定目录下多达3层的子目录结构。比如下面配置

client_body_temp_path /spool/nginx/client_temp 1 2;

存储临时文件的路径是

/spool/nginx/client_temp/7/45/00000123457





time
60s
http
server
location


定义读取客户端请求正文的超时。超时是指相邻两次读操作之间的最大时间间隔，而不是整个请求正文完成传输的最大时间。
如果客户端在这段时间内没有传输任何数据，nginx将返回错误到客户端。




size
1k
http
server


设置读取客户端请求头部的缓冲容量。
对于大多数请求，1K的缓冲足矣。
但如果请求中含有的cookie很长，或者请求来自WAP的客户端，可能请求头不能放在1K的缓冲中。
如果从请求行，或者某个请求头开始不能完整的放在这块空间中，那么nginx将按照
指令的配置分配更多更大的缓冲来存放。
directive.




time
60s
http
server


定义读取客户端请求头部的超时。如果客户端在这段时间内没有传送完整的头部到nginx，
nginx将返回错误到客户端。




size
1m
http
server
location


设置允许客户端请求正文的最大长度。请求的长度由Content-Length请求头指定。
如果请求的长度超过设定值，nginx将返回错误到客户端。
请注意浏览器不能正确显示这个错误。
将size设置成0可以使nginx不检查客户端请求正文的长度。




size
256
http
server


允许微调为每个连接分配的内存。这条指令对nginx的性能影响非常小，一般不应该使用。




mime-type
text/plain
http
server
location


定义响应的默认MIME类型。设置文件扩展名和响应的MIME类型的映射表则使用指令。




size | off
off
http
server
location
0.7.7


当读入长度大于等于指定size的文件时，开启DirectIO功能。
具体的做法是，
在FreeBSD或Linux系统开启使用O_DIRECT标志，
在Mac OS X系统开启使用F_NOCACHE标志，
在Solaris系统开启使用directio功能。
这条指令自动关闭(0.7.15版)。
它在处理大文件时

directio 4m;

或者在Linux系统使用时比较有用。




size
512
http
server
location
0.8.11


为设置文件偏移量对齐。大多数情况下，按512字节对齐足矣，
但在Linux系统下使用XFS，需要将值扩大到4K。




off

    on |
    if_not_owner
    [from=part]
off
http
server
location
1.1.15


决定nginx打开文件时如何处理符号链接：


off

默认行为，允许路径中出现符号链接，不做检查。


on

如果文件路径中任何组成部分中含有符号链接，拒绝访问该文件。


if_not_owner

如果文件路径中任何组成部分中含有符号链接，且符号链接和链接目标的所有者不同，拒绝访问该文件。


from=part

当nginx进行符号链接检查时(参数on和参数if_not_owner)，路径中所有部分默认都会被检查。
而使用from=part参数可以避免对路径开始部分进行符号链接检查，而只检查后面的部分路径。
如果某路径不是以指定值开始，整个路径将被检查，就如同没有指定这个参数一样。
如果某路径与指定值完全匹配，将不做检查。
这个参数的值可以包含变量。






比如：

disable_symlinks on from=$document_root;




这条指令只在有openat和fstatat接口的系统上可用。
当然，现在的FreeBSD、Linux和Solaris都支持这些接口。



参数on和if_not_owner会带来处理开销。

只在那些不支持打开目录查找文件的系统中，使用这些参数需要工作进程有这些被检查目录的读权限。





ngx_http_autoindex_module模块，
ngx_http_random_index_module模块
和ngx_http_dav_module模块目前忽略这条指令。






    code ...
    [=[response]]
    uri

http
server
location
if in location


为指令错误定义显示的URI。当前配置级别没有error_page指令时，将从上层配置继承。
uri可以包含变量。



比如：

error_page 404             /404.html;
error_page 500 502 503 504 /50x.html;




而且，可以使用“=response语法改变响应状态码。比如：

error_page 404 =200 /empty.gif;




如果URI将被发送到一个被代理的服务器处理，或者发送到一个FastCGI服务器处理，
这些后端服务器又返回了不同的响应状态码（比如200、302、401或404），那么这些返回的状态码也可以由本指令处理：

error_page 404 = /404.php;




当然，也可以使用本指令对错误处理进行重定向：

error_page 403      http://example.com/forbidden.html;
error_page 404 =301 http://example.com/notfound.html;

对于例子中的第一行，nginx将向客户端发送302响应状态码。这种用法能使用的状态码只有301、302、303和307。



如果内部跳转时无需改变URI，可以将错误处理转到一个命名路径：

location / {
    error_page 404 = @fallback;
}

location @fallback {
    proxy_pass http://backend;
}





如果处理uri产生了错误，那么nginx将最后一次出错的HTTP响应状态码返回给客户端。





on | off
on
http
server
location
1.3.3


开启或关闭为静态文件自动计算ETag响应头。






main

为HTTP服务器提供配置上下文。




    off |
    exact |
    before
exact
http
server
location
0.7.24


指定响应的修改时间和If-Modified-Since请求头的比较方法：



off

忽略If-Modified-Since请求头(0.7.34)；


exact

精确匹配；


before

响应的修改时间小于等于If-Modified-Since请求头指定的时间。







on | off
on
http
server


控制是否忽略非法的请求头字段名。
合法的名字是由英文字母、数字和连字符组成，当然也可以包含下划线(由指令控制)。



本指令可以在默认虚拟主机的配置层级中定义一次，那么这个值在监听在相同地址和端口的所有虚拟主机上都生效。






location


指定一个路径是否只能用于内部访问。如果是外部访问，客户端将收到错误。
下列请求是内部请求：




由指令、指令、
指令
和指令引起的重定向请求；



由后端服务器返回的X-Accel-Redirect响应头引起的重定向请求；



由ngx_http_ssi_module模块
和ngx_http_addition_module模块
的“include virtual”指令产生的子请求；



用指令对请求进行修改。






举例：

error_page 404 /404.html;

location /404.html {
    internal;
}


nginx限制每个请求只能最多进行10次内部重定向，以防配置错误引起请求处理出现问题。
如果内部重定向次数已达到10次，nginx将返回错误。
同时，错误日志中将有“rewrite or internal redirection cycle”的信息。





none | browser ...
msie6
http
server
location


针对行为异常的浏览器关闭长连接功能。
browser参数指定那些浏览器会受到影响。
值为msie6表示在遇到POST请求时，关闭与老版MSIE浏览器建立长连接。
值为safari表示在遇到Mac OS X和类Mac OS X操作系统下的Safari浏览器和类Safari浏览器时，不与浏览器建立长连接。
值为none表示为所有浏览器开启长连接功能。

在nginx 1.1.18版本及以前，safari将匹配所有操作系统上的Safari和类Safari浏览器，并默认不与这些浏览器建立长连接。





number
100
http
server
location
0.8.0


设置通过一个长连接可以处理的最大请求数。
请求数超过此值，长连接将关闭。





    timeout
    [header_timeout]
75s
http
server
location


第一个参数设置客户端的长连接在服务器端保持的最长时间（在此时间客户端未发起新请求，则长连接关闭）。
第二个参数为可选项，设置Keep-Alive: timeout=time响应头的值。
可以为这两个参数设置不同的值。



Keep-Alive: timeout=time响应头可以被Mozilla和Konqueror浏览器识别和处理。
MSIE浏览器在大约60秒后会关闭长连接。




number size
4 8k
http
server


设置读取客户端请求超大请求的缓冲最大number(数量)和每块缓冲的size(容量)。
HTTP请求行的长度不能超过一块缓冲的容量，否则nginx返回错误到客户端。
每个请求头的长度也不能超过一块缓冲的容量，否则nginx返回错误到客户端。
缓冲仅在必需是才分配，默认每块的容量是8K字节。
即使nginx处理完请求后与客户端保持入长连接，nginx也会释放这些缓冲。




method ...

location


允许按请求的HTTP方法限制对某路径的请求。method用于指定不由这些限制条件进行过滤的HTTP方法，可选值有
GET、
HEAD、
POST、
PUT、
DELETE、
MKCOL、
COPY、
MOVE、
OPTIONS、
PROPFIND、
PROPPATCH、
LOCK、
UNLOCK
或者
PATCH。
指定method为GET方法的同时，nginx会自动添加HEAD方法。
那么其他HTTP方法的请求就会由指令引导的配置块中的ngx_http_access_module
模块和ngx_http_auth_basic_module模块的指令来限制访问。如：

limit_except GET {
    allow 192.168.1.0/32;
    deny  all;
}

请留意上面的例子将对除GET和HEAD方法以外的所有HTTP方法的请求进行访问限制。




rate
0
http
server
location
if in location


限制向客户端传送响应的速率限制。参数rate的单位是字节/秒，设置为0将关闭限速。

nginx按连接限速，所以如果某个客户端同时开启了两个连接，那么客户端的整体速率是这条指令设置值的2倍。



也可以利用$limit_rate变量设置流量限制。如果想在特定条件下限制响应传输速率，可以使用这个功能：

server {

    if ($slow) {
        set $limit_rate 4k;
    }

    ...
}




此外，也可以通过X-Accel-Limit-Rate响应头来完成速率限制。
这种机制可以用指令和
指令关闭。




size
0
http
server
location
if in location
0.8.0


设置不限速传输的响应大小。当传输量大于此值时，超出部分将限速传送。



比如:

location /flv/ {
    flv;
    limit_rate_after 500k;
    limit_rate       50k;
}






    off |
    on |
    always
on
http
server
location
1.1.0
1.0.6


控制nginx如何关闭客户端连接。



默认值“on”指示nginx在完成关闭连接前等待和
处理客户端发来的额外数据。但只有在预测客户端可能发送更多数据的情况才会做此处理。



“always”指示nginx无条件等待和处理客户端的额外数据。



“off”指示nginx立即关闭连接，而绝不等待客户端传送额外数据。
这样做破坏了协议，所以正常条件下不应使用。




time
30s
http
server
location


生效时，这条指令定义nginx处理(读取但忽略)客户端额外数据的最长时间。
超过这段时间后，nginx将关闭连接，不论是否还有更多数据待处理。




time
5s
http
server
location


生效时，这条指令定义nginx等待客户端更多数据到来的最长时间。
如果在这段时间内，nginx没有接收到数据，nginx将关闭连接。否则，nginx将接收数据，忽略它，然后再等待更多数据。
这个“等待——接收——忽略”的循环一直重复，但总时间不会超过指令定义的时间。





    address[:port]
    [default_server]
    [setfib=number]
    [backlog=number]
    [rcvbuf=size]
    [sndbuf=size]
    [accept_filter=filter]
    [deferred]
    [bind]
    [ipv6only=on|off]
    [ssl]
    [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]]

    port
    [default_server]
    [setfib=number]
    [backlog=number]
    [rcvbuf=size]
    [sndbuf=size]
    [accept_filter=filter]
    [deferred]
    [bind]
    [ipv6only=on|off]
    [ssl]
    [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]]

    unix:path
    [default_server]
    [backlog=number]
    [rcvbuf=size]
    [sndbuf=size]
    [accept_filter=filter]
    [deferred]
    [bind]
    [ssl]
    [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]]
*:80 | *:8000
server


设置nginx监听地址，nginx从这里接受请求。对于IP协议，这个地址就是address和port；对于UNIX域套接字协议，这个地址就是path。
一条listen指令只能指定一个address或者port。
address也可以是主机名。
比如：

listen 127.0.0.1:8000;
listen 127.0.0.1;
listen 8000;
listen *:8000;
listen localhost:8000;

IPv6地址(0.7.36版)用方括号来表示：

listen [::]:8000;
listen [fe80::1];

UNIX域套接字(0.8.21版)则使用“unix:”前缀：

listen unix:/var/run/nginx.sock;




如果只定义了address，nginx将使用80端口。



在没有定义listen指令的情况下，如果以超级用户权限运行nginx，它将监听*:80，否则他将监听*:8000。



如果listen指令携带default_server参数，当前虚拟主机将成为指定address:port的默认虚拟主机。
如果任何listen指令都没有携带default_server参数，那么第一个监听address:port的虚拟主机将被作为这个地址的默认虚拟主机。

0.8.21版以前，这个参数的名称是default。




可以为listen指令定义若干额外的参数，这些参数用于套接字相关的系统调用。
这些参数可以在任何listen指令中指定，但是对于每个address:port，只能定义一次。

0.8.21版以前，只有为listen指令定义了default参数，才能定义这些额外的参数。




setfib=number


这个参数(0.8.44)为监听套接字设置关联路由表FIB(SO_SETFIB选项)。
当前这个参数仅工作在FreeBSD上。



backlog=number


为系统调用listen设置backlog参数，用以限制未接受(Accept)连接的队列的最大长度。
FreeBSD和Mac OS X下，backlog的默认值是-1，在其他系统中，默认值是511。




rcvbuf=size


为监听套接字设置接收缓冲区大小(SO_RCVBUF参数)。



sndbuf=size


为监听套接字设置发送缓冲区大小(SO_SNDBUF参数)。



accept_filter=filter


为监听套接字设置接受过滤器的名称(SO_ACCEPTFILTER选项)。
对每个到来的连接，接受过滤器先进行过滤，然后才将它们呈现给accept。
本特性仅工作在FreeBSD系统和NetBSD 5.0+系统下。
可接受的值是
dataready
和
httpready。



deferred


指示在Linux系统使用延迟的accept(TCP_DEFER_ACCEPT选项)。



bind


指示nginx为设置的address:port单独调用一次bind。
这是因为当有多条listen指令监听不同地址下的相同端口，
而其中一条listen指令监听了这个端口的所有地址(*:port)时，
nginx只会为*:port调用一次bind绑定套接字。
需要留意的是，这种情况下，nginx会调用getsockname系统调用来确定接受请求的套接字地址。
如果为某个address:port定义了参数backlog、rcvbuf、
sndbuf、accept_filter、deferred或者so_keepalive，
nginx总会为这个地址单独调用一次bind绑定套接字。



ipv6only=on|off


这个参数(0.7.42)(通过IPV6_V6ONLY选项)决定监听在通配地址[::]上的IPv6套接字是只支持IPv6连接，还是同时支持IPv6和IPv4连接。
这个参数默认打开，并且只能在nginx启动时设置。

在1.3.4版以前，如果省略此参数，那么操作系统的套接字设置将生效。




ssl


本参数(0.7.14)与套接字相关的系统调用无关，但是它可以指定从这个端口接受的连接应该以SSL模式工作。
本参数在某服务器同时处理HTTP和HTTPS请求时，可以使配置更为紧凑。

listen 80;
listen 443 ssl;




so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]


这个参数(1.1.11)为监听套接字配置“TCP keepalive”行为。
如果省略此参数，操作系统默认的设置将对此端口生效。
如果参数值设置为“on”，监听套接字的SO_KEEPALIVE属性将被开启。
如果参数值设置为“off”，监听套接字的SO_KEEPALIVE属性将被关闭。
有些操作系统支持为每个连接调整TCP长连接的参数。调整参数可以使用套接字选项TCP_KEEPIDLE，TCP_KEEPINTVL和TCP_KEEPCNT。
在这些操作系统上(当前就是Linux 2.4+，嬀NetBSD 5+FreeBSD 9.0-STABLE)，可以使用keepidle，keepintvl和keepcnt参数来配置。
省略一到两个参数的话，对应套接字属性的系统默认设置将生效。
比如，
so_keepalive=30m::10将
设置空闲超时(TCP_KEEPIDLE)为30分钟，
设置探测次数(TCP_KEEPCNT)为10次，
保留探测时间间隔(TCP_KEEPINTVL)为系统默认值。






举例：

listen 127.0.0.1 default_server accept_filter=dataready backlog=1024;





[
    = |
    ~ |
    ~* |
    ^~
    ] uri
@name

server
location


为某个请求URI（路径）建立配置。



路径匹配在URI规范化以后进行。所谓规范化，就是先将URI中形如“%XX”的编码字符进行解码，
再解析URI中的相对路径“.”和“..”部分，
另外还可能会压缩相邻的两个或多个斜线成为一个斜线。



可以使用前缀字符串或者正则表达式定义路径。使用正则表达式需要在路径开始添加“~*”前缀
(不区分大小写)，或者“~”前缀(区分大小写)。为了根据请求URI查找路径，nginx先检查前缀字符串定义的路径
(前缀路径)，在这些路径中找到能最精确匹配请求URI的路径。然后nginx按在配置文件中的出现顺序检查正则表达式路径，
匹配上某个路径后即停止匹配并使用该路径的配置，否则使用最大前缀匹配的路径的配置。



路径可以嵌套，但有例外，后面将提到。



在不区分大小写的操作系统（诸如Mac OS X和Cygwin）上，前缀匹配忽略大小写(0.7.7)。但是，比较仅限于单字节的编码区域(one-byte locale)。



正则表达式中可以包含匹配组(0.7.40)，结果可以被后面的其他指令使用。



如果最大前缀匹配的路径以“^~”开始，那么nginx不再检查正则表达式。



而且，使用“=”前缀可以定义URI和路径的精确匹配。如果发现匹配，则终止路径查找。
比如，如果请求“/”出现频繁，定义“location = /”可以提高这些请求的处理速度，
因为查找过程在第一次比较以后即结束。这样的路径明显不可能包含嵌套路径。




在0.7.1到0.8.41的所有nginx中，如果请求匹配的前缀字符串路径并没有“=”或“^~”前缀，
路径查找过程仍然会停止，而不进行正则表达式匹配。




让我们用一个例子解释上面的说法：

location = / {
    [ configuration A ]
}

location / {
    [ configuration B ]
}

location /documents/ {
    [ configuration C ]
}

location ^~ /images/ {
    [ configuration D ]
}

location ~* \.(gif|jpg|jpeg)$ {
    [ configuration E ]
}

请求“/”匹配配置A，
请求“/index.html”匹配配置B，
请求“/documents/document.html”匹配配置C，
请求“/images/1.gif”匹配配置D，
请求“/documents/1.jpg”匹配配置E。



前缀“@”定义了命名路径。这种路径不在一般的请求处理中使用，
而是用在请求重定向中。这些路径不能嵌套，也不能包含嵌套路径。






on | off
on
http
server
location


开启或者关闭在中记录文件不存在的错误。




on | off
off
http
server
location


开启或者关闭在中记录子请求的访问日志。




number

http
server
location
1.1.2


如果请求中含有字节范围的请求头，这条指令可以限制此范围允许的最大值。如果请求头的值超过此限制，将按请求未携带此请求头的情况处理。
默认nginx对此不做限制。设置为0将使nginx完全不支持HTTP字节范围特性。




on | off
on
http
server


开启或者关闭将请求URI中相邻两个或更多斜线合并成一个的功能。



注意压缩URI对于前缀匹配和正则匹配的正确性是很重要的。没有开启这个功能时，请求“//scripts/one.php”将不能匹配

location /scripts/ {
    ...
}

而被按静态文件的流程处理，所以将它变换成“/scripts/one.php”。



如果URI中包含base64编码的内容，必须将斜线压缩调整成off，因为base64编码本身会使用“/”字符。
然而。出于安全方面的考虑，最好还是不要关闭压缩。



这条指令可以指定在默认虚拟主机的配置级别。这样的话，这个配置可以覆盖监听同一地址和端口的所有虚拟主机。




on | off
on
http
server
location


在响应状态码大于等于400时，在响应正文中添加一段注释，使响应正文达到512字节。
本指令可以为MSIE客户端开启或关闭这个功能。




on | off
off
http
server
location


为MSIE客户端开启或者关闭用页面刷新取代页面重定向的功能。




off

max=N
[inactive=time]
off
http
server
location


用于配置文件缓存，可缓存：



打开文件的描述符，大小和修改时间；



目录查找结果；



文件查找时的错误结果，诸如“file not found”(文件不存在)、“no read permission”(无读权限)等等。

应单独使用指令开启缓存错误结果的功能。







指令有下列参数：



max


设置缓存中元素的最大数量，当缓存溢出时，使用LRU(最近最少使用)算法删除缓存中的元素；



inactive


设置超时，在这段时间内缓存元素如果没有被访问，将从缓存中删除。
默认超时是60秒；



off


关闭缓存。






举例：

open_file_cache          max=1000 inactive=20s;
open_file_cache_valid    30s;
open_file_cache_min_uses 2;
open_file_cache_errors   on;





on | off
off
http
server
location


开启或者关闭缓存文件查找的错误结果。




number
1
http
server
location


设置在由指令的inactive参数配置的超时时间内，
文件应该被访问的最小number(次数)。如果访问次数大于等于此值，文件描述符会保留在缓存中，否则从缓存中删除。




time
60s
http
server
location


设置检查缓存的元素的时间间隔。





on | off
off
http
server


这条指令已经被废弃，请使用指令。






on | off
on
http
server
location


开启或关闭nginx发起重定向时指定端口。



重定向中首要主机名的使用由指令控制。




size
1460
http
server
location


如果可能，到客户端的数据将被推迟发送，直到nginx需要发送的数据至少有size字节。
设置为0将关闭推迟发送的功能。




size
0
http
server
location


设置内核参数，控制文件预读的数量。



在Linux上，因为使用的是posix_fadvise(0, 0, 0, POSIX_FADV_SEQUENTIAL)系统调用，所以size无用。



在FreeBSD上，访问的是fcntl(O_READAHEAD,size)系统调用。
该系统调用在FreeBSD 9.0-CURRENT才被支持，在FreeBSD 7上则需要打补丁。




on | off
off
http
server
location


允许或禁止指令进行多次重定向。
允许的话，重定向次数也有限制。
而禁止此功能时，当访问指令重定向的错误页面出现任何问题时，nginx将直接输出默认错误页面。




size
4k
http
server


允许对每个请求的内存分配进行细调。这条指令对性能影响很小，通常情况下不应使用。




on | off
off
http
server
location


开启或关闭重置超时连接的功能。重置连接是这样执行的：关闭套接字以前，设置SO_LINGER选项的超时值为0，
那么当关闭套接字时，nginx向客户端发送TCP RST，并且释放此套接字占用的所有内存。
这样可以避免某个已关闭的套接字长时间处于FIN_WAIT1状态，并占用内存缓冲区。



应该注意的事，超时的长连接仍然是正常关闭。





address ...
[valid=time]

http
server
location


配置将后端服务器的名字解析成ip地址的名字服务器，比如：

resolver 127.0.0.1 [::1]:5353;

这里地址可以指定域名或者ip地址，可以带端口号(1.3.1，1.2.2)。如果未指定端口，nginx使用53端口。
以轮询方式发送请求到多台名字服务器。

在1.1.7版以前，只允许配置一个名字服务器。而支持使用IPv6地址定义名字服务器则是从1.3.1和1.2.2版本开始。

nginx会缓存名字解析的结果。默认情况下，缓存时间是名字解析响应中的TTL字段的值。也允许通过valid参数覆盖它：

resolver 127.0.0.1 [::1]:5353 valid=30s;


在1.1.9版以前，不可能调节缓存时间，nginx总会将响应缓存5分钟。





time
30s
http
server
location


为名字解析设置超时，比如：

resolver_timeout 5s;





path
html
http
server
location
if in location


为请求设置根目录。比如，如果配置如下

location /i/ {
    root /data/w3;
}

那么nginx将使用文件/data/w3/i/top.gif响应请求“/i/top.gif”。



path的值中可以包含除$document_root和$realpath_root以外的变量。



文件路径的构造仅仅是将URI拼在root指令的值后面。如果需要修改URI，应该使用指令。




all | any
all
http
server
location


nginx进行访问限制的有ngx_http_access_module模块和
ngx_http_auth_basic_module模块。
本指令设置成all时，表示只有当两个模块的所有限制条件(写入配置的)都授权访问时，允许请求访问；
设置成any时，表示如果当任意模块的任意限制条件授权访问时，允许请求访问。



举例：

location / {
    satisfy any;

    allow 192.168.1.0/32;
    deny  all;

    auth_basic           "closed site";
    auth_basic_user_file conf/htpasswd;
}





on | off
off
http
server
location


这条指令已被指令的any参数取代。




size
0
http
server
location


如果设置成非0值，nginx将尝试最小化向客户端发送数据的次数。
这是通过将方法的NOTE_LOWAT标志，
或者将套接字的SO_SNDLOWAT属性设置成指定的size实现的。



这条指令在Linux、Solaris和Windows操作系统无效。




time
60s
http
server
location


设置向客户端传输响应的超时。超时仅指两次相邻写操作之间的时间间隔，而非整个响应的传输时间。
如果客户端在这段时间中没有收到任何数据，连接将关闭。





on | off
off
http
server
location
if in location


开启或关闭使用sendfile调用。





size
0
http
server
location


设置为非0值时，可以限制在一次sendfile调用时传输的数据量。
如果不进行限制，一个快速的连接可能会霸占整个worker进程的所有资源。






http


表示开始设置虚拟主机的配置。
nginx没有明显分隔IP-based(基于IP地址)和name-based(基于Host请求头)这两种类型的虚拟主机，
而是用指令描述虚拟主机接受连接的地址和端口，用指令列出虚拟主机的所有主机名。
在文档“Nginx如何处理一个请求”中提供了示例配置。




name ...
""
server


设置虚拟主机名，比如：

server {
    server_name example.com www.example.com;
}




第一个名字成为虚拟主机的首要主机名。



主机名中可以含有星号(“*”)，以替代名字的开始部分或结尾部分：

server {
    server_name example.com *.example.com www.example.*;
}

上面这些名字称为通配符主机名。



上面例子中的前两个名字可以组合成一个：

server {
    server_name .example.com;
}




也可以在主机名中使用正则表达式，就是在名字前面补一个波浪线(“~”)：

server {
    server_name www.example.com ~^www\d+\.example\.com$;
}




可以在正则表达式中包含匹配组(0.7.40)，后续被其他指令使用：

server {
    server_name ~^(www\.)?(.+)$;

    location / {
        root /sites/$2;
    }
}

server {
    server_name _;

    location / {
        root /sites/default;
    }
}





正则表达式中的命名匹配组可以创建变量(0.8.25)，后续被其他指令使用：

server {
    server_name ~^(www\.)?(?<domain>.+)$;

    location / {
        root /sites/$domain;
    }
}

server {
    server_name _;

    location / {
        root /sites/default;
    }
}




如果参数值等于“$hostname”(0.9.4)，将使用机器的hostname来替换。



nginx也允许定义空主机名(0.7.11)：

server {
    server_name www.example.com "";
}

这种主机名可以让虚拟主机处理没有Host请求头的请求，而不是让指定“地址:端口”的默认虚拟主机来处理。
这是本指令的默认设置。

在0.8.48版以前，机器的hostname被用作默认设置。




通过名字查找虚拟主机时，如果一个名字可以匹配多个指定的配置，比如同时匹配上通配符和正则表达式，
按下面优先级，使用先匹配上的虚拟主机：



确切的名字；



最长的以星号起始的通配符名字，比如“*.example.com”；



最长的以星号结束的通配符名字，比如“mail.*”；



第一个匹配的正则表达式名字（按在配置文件中出现的顺序）。






另一篇文档“虚拟主机名”对虚拟主机名的有详细的描述。




on | off
off
http
server
location


开启或关闭nginx将指令指定的首要虚拟主机名用于发起的重定向的功能。
关闭此功能时，nginx将使用Host请求头的中的名字，如果没有此请求头，nginx将使用虚拟主机所在的IP地址。



重定向中端口的使用由指令控制。




size
32|64|128
http


设置主机名哈希表的表项长度，其默认值取决于处理器的缓存线长度。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。




size
512
http


设置主机名哈希表的最大size(桶容量)。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。




on | off
on
http
server
location


开启或关闭在错误信息的Server响应头中输出nginx版本号。




on | off
on
http
server
location


开启或关闭nginx使用TCP_NODELAY选项的功能。
这个选项仅在将连接转变为长连接的时候才被启用。（译者注，在upstream发送响应到客户端时也会启用）。




on | off
off
http
server
location


开启或者关闭nginx在FreeBSD上使用TCP_NOPUSH套接字选项，
在Linux上使用TCP_CORK套接字选项。
选项仅在使用的时候才开启。
开启此选项允许



在Linux和FreeBSD 4.*上将响应头和正文的开始部分一起发送；



一次性发送整个文件。







file ... uri
file ... =code

server
location


按指定顺序检查文件是否存在，并且使用第一个找到的文件来处理请求，那么处理过程就是在当前上下文环境中进行的。
文件路径是根据指令和指令，将file参数拼接而成。
可以在名字尾部添加斜线以检查目录是否存在，比如“$uri/”。
如果找不到任何文件，将按最后一个参数指定的uri进行内部跳转。
比如：

location /images/ {
    try_files $uri /images/default.gif;
}

location = /images/default.gif {
    expires 30s;
}

最后一个参数也可以指向一个命名路径，如下面的例子所示。
从0.7.51版开始，最后一个参数也可以是code：

location / {
    try_files $uri $uri/index.html $uri.html =404;
}




下面是代理Mongrel的例子：

location / {
    try_files /system/maintenance.html
              $uri $uri/index.html $uri.html
              @mongrel;
}

location @mongrel {
    proxy_pass http://mongrel;
}




下面是Drupal用FastCGI的例子：

location / {
    try_files $uri $uri/ @drupal;
}

location ~ \.php$ {
    try_files $uri @drupal;

    fastcgi_pass ...;

    fastcgi_param SCRIPT_FILENAME /path/to$fastcgi_script_name;
    fastcgi_param SCRIPT_NAME     $fastcgi_script_name;
    fastcgi_param QUERY_STRING    $args;

    ... other fastcgi_param's
}

location @drupal {
    fastcgi_pass ...;

    fastcgi_param SCRIPT_FILENAME /path/to/index.php;
    fastcgi_param SCRIPT_NAME     /index.php;
    fastcgi_param QUERY_STRING    q=$uri&$args;

    ... other fastcgi_param's
}

而下面的例子中

location / {
    try_files $uri $uri/ @drupal;
}

try_files指令等价于

location / {
    error_page 404 = @drupal;
    log_not_found off;
}

然后是这里，

location ~ \.php$ {
    try_files $uri @drupal;

    fastcgi_pass ...;

    fastcgi_param SCRIPT_FILENAME /path/to$fastcgi_script_name;

    ...
}

try_files在将请求发送到FastCGI服务器以前检查PHP文件是否存在。



下面是Wordpress和Joomla的例子：

location / {
    try_files $uri $uri/ @wordpress;
}

location ~ \.php$ {
    try_files $uri @wordpress;

    fastcgi_pass ...;

    fastcgi_param SCRIPT_FILENAME /path/to$fastcgi_script_name;
    ... other fastcgi_param's
}

location @wordpress {
    fastcgi_pass ...;

    fastcgi_param SCRIPT_FILENAME /path/to/index.php;
    ... other fastcgi_param's
}







    text/html  html;
    image/gif  gif;
    image/jpeg jpg;

http
server
location


设置文件扩展名和响应的MIME类型的映射表。
可以将多个扩展名映射到同一种类型，比如：

types {
    application/octet-stream bin exe dll;
    application/octet-stream deb;
    application/octet-stream dmg;
}




随nginx发行的conf/mime.types文件中包含了足够全面的映射表。



为了是为某个路径的所有请求生成MIME类型“application/octet-stream”，
可以使用下面配置：

location /download/ {
    types        { }
    default_type application/octet-stream;
}





size
32|64|128
http
server
location


设置MIME类型哈希表的表项长度，其默认值取决于处理器的缓存线长度。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。




size
1024
http
server
location


设置MIME类型哈希表的最大size(桶容量)。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。




on | off
off
http
server


允许或禁止在客户端请求头中使用下划线。
如果禁止，含有下划线的请求头将被标志为非法请求头并接受指令的处理。



可以在默认主机的配置级别定义此命令。这样，指令设置将覆盖监听同一地址和端口的所有虚拟主机。




size
64
http


设置变量哈希表的表项长度，其默认值取决于处理器的缓存线长度。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。




size
512
http


设置变量哈希表的最大size(桶容量)。
另一篇文档“设置哈希表”详细介绍了如何设置哈希表。



## 内嵌变量 {#variables}

`ngx_http_core_module`模块支持内嵌变量，变量名与Apache服务器对应。
首先，这些变量可以表示客户端的请求头字段，诸如*$http_user_agent*、*$http_cookie*等等。
nginx也支持其他变量：

***$arg_**name***  
  请求行中的*name*参数。
***$args***  
  请求行中参数字符串。
***$binary_remote_addr***  
  客户端IP地址的二进制形式，值的长度总是4字节。
***$body_bytes_sent***  
  nginx返回给客户端的字节数，不含响应头。
***$bytes_sent***  
  nginx返回给客户端的字节数(1.3.8, 1.2.5)。
***$connection***  
  连接的序列号(1.3.8, 1.2.5)。
***$content_length***  
  **Content-Length**请求头的值。
***$content_type***  
  **Content-Type**请求头的值。
***$cookie_**name***  
  名为*name*的cookie。
***$document_root***  
  当前请求的指令或指令的配置值。
***$document_uri***  
  与*$uri*相同。
***$host***  
  **Host**请求头的值，如果没有该请求头，则为与请求对应的虚拟主机的首要主机名。
***$hostname***  
  机器名称。
***$http_**name***  
  任意请求头的值；变量名的后半部为转化为小写并且用下划线替代横线后的请求头名称。
***$https***  
  如果连接是SSL模块，返回“`on`”，否则返回空字符串。
***$is_args***  
  如果请求行带有参数，返回“`?`”，否则返回空字符串。
***$limit_rate***  
  允许设置此值来限制连接的传输速率。
***$msec***  
  当前时间，单位是秒，精度是毫秒。(1.3.9, 1.2.6)
***$nginx_version***  
  nginx版本号。
***$pid***  
  worker进程的PID。
***$query_string***  
  与*$args*相同。
***$realpath_root***  
  按指令或指令算出的当前请求的绝对路径。其中的符号链接都会解析成真是文件路径。
***$remote_addr***  
  客户端IP地址。
***$remote_port***  
  客户端端口。
***$remote_user***  
  为基本用户认证提供的用户名。
***$request***  
  完整的原始请求行。
***$request_body***  
  请求正文。

在由指令和
指令处理的路径中，
这个变量值可用。
***$request_body_file***  
  请求正文的临时文件名。

处理完成时，临时文件将被删除。
如果希望总是将请求正文写入文件，需要开启。
如果在被代理的请求或FastCGI请求中传递临时文件名，就应该禁止传递请求正文本身。
使用proxy_pass_request_body off指令
和fastcgi_pass_request_body off指令
分别禁止在代理和FastCGI中传递请求正文。
***$request_completion***  
  请求完成时返回“`OK`”，否则返回空字符串。
***$request_filename***  
  基于指令或指令，以及请求URI，得到的当前请求的文件路径。
***$request_method***  
  HTTP方法，通常为“`GET`”或者“`POST`”。
***$request_time***  
  请求处理的时间，单位为秒，精度是毫秒(1.3.9, 1.2.6)；请求处理时间从由客户端接收到第一个字节开始计算。
***$request_uri***  
  完整的原始请求行（带参数）。
***$scheme***  
  请求协议类型，为“`http`”或“`https`”。
***$sent_http_**name***  
  任意的响应头字段的值。
变量名的后半部为转化为小写并且用下划线替代横线后的响应头名称。
***$server_addr***  
  接受请求的服务器地址。

为计算这个值，通常需要进行一次系统调用。为了避免系统调用，必须指定指令
的地址，并且使用bind参数。
***$server_name***  
  接受请求的虚拟主机的首要主机名。
***$server_port***  
  接受请求的虚拟主机的端口。
***$server_protocol***  
  请求协议，通常为“`HTTP/1.0`”或“`HTTP/1.1`”。
***$status***  
  响应状态码。
***$tcpinfo_rtt*,
*$tcpinfo_rttvar*,
*$tcpinfo_snd_cwnd*,
*$tcpinfo_rcv_space***  
  客户端TCP连接的信息，在支持套接字选项TCP_INFO的系统中可用。
***$uri***  
  当前请求规范化以后的URI。

变量$uri的值可能随请求的处理过程而改变。
比如，当进行内部跳转时，或者使用默认页文件。
