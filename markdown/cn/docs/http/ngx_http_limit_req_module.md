# ngx_http_limit_req_module 模块

**Translator:** Weibin Yao  
**Revision:** 1  
**Language:** cn

`ngx_http_limit_req_module` 模块(0.7.21)可以通过定义的 键值来限制请求处理的频率。特别的，它可以限制来自单个IP地址的请求处理频率。 限制的方法是通过一种“漏桶”的方法——固定每秒处理的请求数，推迟过多的请求处理。

# 配置示例 {#example}

```
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    ...

    server {

        ...

        location /search/ {
            limit_req zone=one burst=5;
        }
```

# 指令 {#directives}

## limit_req

```
Syntax:  limit_req zone=name [burst=number] [nodelay];
Default: 
Context: location, http, server
```

设置对应的共享内存限制域和允许被处理的最大请求数阈值。 如果请求的频率超过了限制域配置的值，请求处理会被延迟，所以 所有的请求都是以定义的频率被处理的。 超过频率限制的请求会被延迟，直到被延迟的请求数超过了定义的阈值 这时，这个请求会被终止，并返回 503 Service Temporarily Unavailable 错误。这个阈值的默认值等于0。 比如这些指令：

```
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

server {
    location /search/ {
        limit_req zone=one burst=5;
    }
```

限制平均每秒不超过一个请求，同时允许超过频率限制的请求数不多于5个。

如果不希望超过的请求被延迟，可以用 `nodelay` 参数：

```
limit_req zone=one burst=5 nodelay;
```

## limit_req_log_level

```
Syntax:  limit_req_log_level info | notice | warn | error;
Default: error
Context: location, http, server
```

*This directive appeared in version 0.8.18.*

设置你所希望的日志级别，当服务器因为频率过高拒绝或者延迟处理请求时可以记下相应级别的日志。 延迟记录的日志级别比拒绝的低一个级别；比如， 如果设置“ `limit_req_log_level notice` ”， 延迟的日志就是 `info` 级别。

## limit_req_zone

```
Syntax:  limit_req_zone $variable zone=name:size rate=rate;
Default: 
Context: http
```

设置一块共享内存限制域的参数，它可以用来保存键值的状态。 它特别保存了当前超出请求的数量。 键的值就是指定的变量（空值不会被计算）。 示例用法：

```
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
```

这里，状态被存在名为“one”，最大10M字节的共享内存里面。对于这个限制域来说 平均处理的请求频率不能超过每秒一次。

键值是客户端的IP地址。 如果不使用 `$remote_addr` 变量，而用 `$binary_remote_addr` 变量， 可以将每条状态记录的大小减少到64个字节，这样1M的内存可以保存大约1万6千个64字节的记录。 如果限制域的存储空间耗尽了，对于后续所有请求，服务器都会返回 503 Service Temporarily Unavailable 错误。

请求频率可以设置为每秒几次（r/s）。如果请求的频率不到每秒一次， 你可以设置每分钟几次(r/m)。比如每秒半次就是30r/m。

