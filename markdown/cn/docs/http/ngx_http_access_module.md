# ngx_http_access_module模块

**Translator:** WenMing  
**Revision:** 1  
**Language:** cn


模块 `ngx_http_access_module` 允许限制某些IP地址的客户端访问。

也可以通过
[密码](ngx_http_auth_basic_module.html)来限制访问。
使用
 [](ngx_http_core_module.xml#satisfy) 指令就能同时通过IP地址和密码来限制访问。

## 配置范例 {#example}

```
location / {
    deny  192.168.1.1;
    allow 192.168.1.0/24;
    allow 10.1.1.0/16;
    allow 2001:0db8::/32;
    deny  all;
}
```

规则按照顺序依次检测，直到匹配到第一条规则。
在这个例子里，IPv4的网络中只有
`10.1.1.0/16` 和 `192.168.1.0/24`允许访问，但
`192.168.1.1`除外,
对于IPv6的网络，只有`2001:0db8::/32`允许访问。
在规则很多的情况下，使用
[ngx_http_geo_module](ngx_http_geo_module.html)
模块变量更合适。

## 指令 {#directives}



    address |
    CIDR |
    all

http
server
location
limit_except


允许指定的网络地址访问。





    address |
    CIDR |
    all

http
server
location
limit_except


拒绝指定的网络地址访问。


