# ngx_http_rewrite_module模块

**Translator:** cfsego  
**Revision:** 2  
**Language:** cn


`ngx_http_rewrite_module`模块允许正则替换URI，返回页面重定向，和按条件选择配置。

`ngx_http_rewrite_module`模块指令按以下顺序处理：

- 处理在[](ngx_http_core_module.xml#server)级别中定义的模块指令；
- 为请求查找location；
- 处理在选中的[](ngx_http_core_module.xml#location)中定义的模块指令。如果指令改变了URI，按新的URI查找location。这个循环至多重复[10次](ngx_http_core_module.xml#internal)，之后nginx返回错误500 Internal Server Error。

## 指令 {#directives}




server
location
if


停止处理当前这一轮的ngx_http_rewrite_module指令集。



举例：

if ($slow) {
    limit_rate 10k;
    break;
}





(condition)

server
location


计算指定的condition的值。如果为真，执行定义在大括号中的rewrite模块指令，并将if指令中的配置指定给请求。if指令会从上一层配置中继承配置。



条件可以是下列任意一种：



变量名；如果变量值为空或者是以“0”开始的字符串，则条件为假；



使用“=”和“!=”运算符比较变量和字符串；



使用“~”（大小写敏感）和“~*”（大小写不敏感）运算符匹配变量和正则表达式。正则表达式可以包含匹配组，匹配结果后续可以使用变量$1..$9引用。如果正则表达式中包含字符“}”或者“;”，整个表达式应该被包含在单引号或双引号的引用中。



使用“-f”和“!-f”运算符检查文件是否存在；



使用“-d”和“!-d”运算符检查目录是否存在；



使用“-e”和“!-e”运算符检查文件、目录或符号链接是否存在；



使用“-x”和“!-x”运算符检查可执行文件；






举例：

if ($http_user_agent ~ MSIE) {
    rewrite ^(.*)$ /msie/$1 break;
}

if ($http_cookie ~* "id=([^;]+)(?:;|$)") {
    set $id $1;
}

if ($request_method = POST) {
    return 405;
}

if ($slow) {
    limit_rate 10k;
}

if ($invalid_referer) {
    return 403;
}


内嵌变量$invalid_referer的值是通过指令设置的。





code [text]
code URL
URL

server
location
if


停止处理并返回指定code给客户端。返回非标准的状态码444可以直接关闭连接而不返回响应头。



从0.8.42版开始，可以在指令中指定重定向的URL（状态码为301、302、303和307），或者指定响应体文本（状态码为其它值）。响应体文本或重定向URL中可以包含变量。作为一种特殊情况，重定向URL可以简化为当前server的本地URI，那么完整的重定向URL将按照请求协议（$scheme）、指令和指令的配置进行补全。



另外，状态码为302的临时重定向使用的URL可以作为指令的唯一参数。该参数应该以“http://”、“https://”或者“https://”开始。URL中可以包含变量。




0.7.51版本以前只能返回下面状态码：
204、400、402 — 406、408、410、411、413、416 和 500 — 504。



直到1.1.16和1.0.13版，状态码307才被认为是一种重定向。






    regex
    replacement
    [flag]

server
location
if


如果指定的正则表达式能匹配URI，此URI将被replacement参数定义的字符串改写。rewrite指令按其在配置文件中出现的顺序执行。flag可以终止后续指令的执行。如果replacement的字符串以“http://”或“https://”开头，nginx将结束执行过程，并返回给客户端一个重定向。



可选的flag参数可以是其中之一：


last

停止执行当前这一轮的ngx_http_rewrite_module指令集，然后查找匹配改变后URI的新location；


break

停止执行当前这一轮的ngx_http_rewrite_module指令集；


redirect

在replacement字符串未以“http://”或“https://”开头时，使用返回状态码为302的临时重定向；


permanent

返回状态码为301的永久重定向。



完整的重定向URL将按照请求协议（$scheme）、指令和指令的配置进行补全。



举例：

server {
    ...
    rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 last;
    rewrite ^(/download/.*)/audio/(.*)\..*$ $1/mp3/$2.ra  last;
    return  403;
    ...
}




但是当上述指令写在“/download/”的location中时，应使用标志break代替last，否则nginx会重复10轮循环，然后返回错误500：

location /download/ {
    rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 break;
    rewrite ^(/download/.*)/audio/(.*)\..*$ $1/mp3/$2.ra  break;
    return  403;
}




如果replacement字符串包括新的请求参数，以往的请求参数会添加到新参数后面。如果不希望这样，在replacement字符串末尾加一个问号“？”，就可以避免，比如：

rewrite ^/users/(.*)$ /show?user=$1? last;




如果正则表达式中包含字符“}”或者“;”，整个表达式应该被包含在单引号或双引号的引用中。




on | off
off
http
server
location
if


开启或者关闭将ngx_http_rewrite_module模块指令的处理日志以notice级别记录到错误日志中。




variable value

server
location
if


为指定变量variable设置变量值value。value可以包含文本、变量或者它们的组合。




on | off
on
http
server
location
if


控制是否记录变量未初始化的警告到日志。



## 内部实现 {#internals}

`ngx_http_rewrite_module`模块的指令在解析配置阶段被编译成nginx内部指令。这些内部指令在处理请求时被解释执行。而解释器是一个简单的堆栈机器。

比如，下面指令

```
location /download/ {
    if ($forbidden) {
        return 403;
    }

    if ($slow) {
        limit_rate 10k;
    }

    rewrite ^/(download/.*)/media/(.*)\..*$ /$1/mp3/$2.mp3 break;
}
```

将被翻译成下面这些指令：

```
variable $forbidden
check against zero
    return 403
    end of code
variable $slow
check against zero
match of regular expression
copy "/"
copy $1
copy "/mp3/"
copy $2
copy ".mp3"
end of regular expression
end of code
```

请注意没有对应上面的[](ngx_http_core_module.xml#limit_rate)指令的内部指令，因为这个指令与`ngx_http_rewrite_module`模块无关。nginx会为这个块单独创建一个配置，包含`limit_rate`等于10k。如果条件为真，nginx将把这个配置指派给请求。

指令

```
rewrite ^/(download/.*)/media/(.*)\..*$ /$1/mp3/$2.mp3 break;
```

可以通过将正则表达式中的第一个斜线“/”放入圆括号，来实现节约一个内部指令：

```
rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 break;
```

对应的内部指令将会是这样：

```
match of regular expression
copy $1
copy "/mp3/"
copy $2
copy ".mp3"
end of regular expression
end of code
```
