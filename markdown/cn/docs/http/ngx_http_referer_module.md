# ngx_http_referer_module模块

**Translator:** nigelzeng  
**Revision:** 1  
**Language:** cn


`ngx_http_referer_module`模块允许拦截**Referer**请求头中含有非法值的请求，阻止它们访问站点。
需要注意的是伪造一个有效的**Referer**请求头是相当容易的，
因此这个模块的预期目的不在于彻底地阻止这些非法请求，而是为了阻止由正常浏览器发出的大规模此类请求。
还有一点需要注意，即使正常浏览器发送的合法请求，也可能没有**Referer**请求头。

## 配置实例 {#example}

```
valid_referers none blocked server_names
               *.example.com example.* www.example.org/galleries/
               ~\.google\.;

if ($invalid_referer) {
    return 403;
}
```

## 指令 {#directives}


size
64
server
location
1.0.5


设置用来存储有效referer的哈希表的表项长度。
详细的情况参见哈希表设置。




size
2048
server
location
1.0.5


设置用来存储有效referer的哈希表最大桶容量。
详细的情况参见哈希表设置。





    none |
    blocked |
    server_names |
    string
    ...

server
location


Referer请求头为指定值时，内嵌变量$invalid_referer被设置为空字符串，
否则这个变量会被置成“1”。查找匹配时不区分大小写。



该指令的参数可以为下面的内容：


none

缺少Referer请求头；


blocked

Referer 请求头存在，但是它的值被防火墙或者代理服务器删除；
这些值都不以“http://” 或者 “https://”字符串作为开头；


server_names

Referer 请求头包含某个虚拟主机名；


任意字符串

定义一个服务器名和可选的URI前缀。服务器名允许在开头或结尾使用“*”符号。
当nginx检查时，Referer请求头里的服务器端口将被忽略。


正则表达式

必须以“~”符号作为开头。
需要注意的是表达式会从“http://”或者“https://”之后的文本开始匹配。






实例:

valid_referers none blocked server_names
               *.example.com example.* www.example.org/galleries/
               ~\.google\.;



