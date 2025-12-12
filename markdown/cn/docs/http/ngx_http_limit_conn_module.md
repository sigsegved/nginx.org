# ngx_http_limit_conn_module 模块

**Translator:** G_will  
**Revision:** 1  
**Language:** cn

`ngx_http_limit_conn_module` 模块可以按照定义的键限定每个键值的连接数。特别的，可以设定单一 IP 来源的连接数。

并不是所有的连接都会被模块计数；只有那些正在被处理的请求（这些请求的头信息已被完全读入）所在的连接才会被计数。

# 配置范例 {#example}

```
http {
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    ...

    server {

        ...

        location /download/ {
            limit_conn addr 1;
        }
```

# 指令 {#directives}

## limit_conn

```
Syntax:  zone number
Default: 
Context: location, http, server
```

指定一块已经设定的共享内存空间，以及每个给定键值的最大连接数。当连接数超过最大连接数时，服务器将会返回 503 Service Temporarily Unavailable 错误。比如，如下配置

```
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    location /download/ {
        limit_conn addr 1;
    }
```

表示，同一 IP 同一时间只允许有一个连接。

当多个 `limit_conn` 指令被配置时，所有的连接数限制都会生效。比如，下面配置不仅会限制单一IP来源的连接数，同时也会限制单一虚拟服务器的总连接数：

```
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;

server {
    ...
    limit_conn perip 10;
    limit_conn perserver 100;
}
```

如果当前配置层级没有 `limit_conn` 指令，将会从更高层级继承连接限制配置。

## limit_conn_log_level

```
Syntax:  info | notice | warn | error
Default: error
Context: location, http, server
```

*This directive appeared in version 0.8.18.*

指定当连接数超过设定的最大连接数，服务器限制连接时的日志等级。

## limit_conn_zone

```
Syntax:  $variable zone=name:size
Default: 
Context: http
```

设定保存各个键的状态的共享内存空间的参数。键的状态中保存了当前连接数。键的值可以是特定变量的任何非空值（空值将不会被考虑）。 使用范例：

```
limit_conn_zone $binary_remote_addr zone=addr:10m;
```

这里，设置客户端的IP地址作为键。注意，这里使用的是 `$binary_remote_addr` 变量，而不是 `$remote_addr` 变量。 `$remote_addr` 变量的长度为7字节到15字节不等，而存储状态在32位平台中占用32字节或64字节，在64位平台中占用64字节。而 `$binary_remote_addr` 变量的长度是固定的4字节，存储状态在32位平台中占用32字节或64字节，在64位平台中占用64字节。一兆字节的共享内存空间可以保存3.2万个32位的状态，1.6万个64位的状态。如果共享内存空间被耗尽，服务器将会对后续所有的请求返回 503 Service Temporarily Unavailable 错误。

## limit_zone

```
Syntax:  name $variable size
Default: 
Context: http
```

这条指令在 1.1.8 版本中已经被废弃，应该使用等效的 [limit_conn_zone](#limit_conn_zone) 指令。该指令的语法也有变化：

> **Note:** `limit_conn_zone` `$variable` `zone` = `name` : `size` ;

