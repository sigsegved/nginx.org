# ngx_http_log_module模块

**Translator:** nigelzeng  
**Revision:** 3  
**Language:** cn

`ngx_http_log_module` 模块按指定的格式写访问日志。

请求在处理结束时，会按请求路径的配置上下文记访问日志。 如果在请求处理期间产生了 [内部跳转](ngx_http_core_module.xml#internal) ， 请求结束时的路径可能不同于原始的请求路径。

# 配置实例 {#example}

```
log_format gzip '$remote_addr - $remote_user [$time_local] '
                '"$request" $status $bytes_sent '
                '"$http_referer" "$http_user_agent" "$gzip_ratio"';

access_log /spool/logs/nginx-access.log gzip buffer=32k;
```

# 指令 {#directives}

## access_log

```
Syntax:  access_log off;
Default: logs/access.log combined
Context: limit_except, http, server, location, if in location
```

为访问日志设置路径，格式和缓冲区大小（nginx访问日志支持缓存）。 在同一个配置层级里可以指定多个日志。 特定值 `off` 会取消当前配置层级里的所有 `access_log` 指令。 如果没有指定日志格式则会使用预定义的“ `combined` ”格式。

缓冲区的大小不能超过磁盘文件原子性写入的大小。 对于FreeBSD来说缓冲区大小是无限制的。

日志文件的路径可以包含变量（0.7.6+）， 但此类日志存在一些限制：

- 工作进程使用的 [user](../ngx_core_module.xml#user) 应拥有在目录里创建文件的权限；
- 写缓冲无效；
- 每条日志写入都会打开和关闭文件。然而，频繁使用的文件描述符可以存储在 [缓存](#open_log_file_cache) 中，
在 [open_log_file_cache](#open_log_file_cache) 指令的 `valid` 参数指定的时间里，
写操作能持续写到旧文件。
- 每次日志写入的操作都会检查请求的 [根目录](ngx_http_core_module.xml#root) 是否存在，
如果不存在则日志不会被创建。
因此在一个层级里同时指定 [root](ngx_http_core_module.xml#root) 和 `access_log` 是一个不错的想法：
  ```
server {
    root       /spool/vhost/data/$host;
    access_log /spool/vhost/logs/$host;
    ...
```

## log_format

```
Syntax:  log_format name string ...;
Default: combined "..."
Context: http
```

指定日志的格式。

日志格式允许包含普通变量和只在日志写入时存在的变量：

**`$body_bytes_sent`**  
  发送给客户端的字节数，不包括响应头的大小；
该变量与Apache模块 `mod_log_config` 里的“ `%B` ”参数兼容。

**`$bytes_sent`**  
  发送给客户端的总字节数。

**`$connection`**  
  连接的序列号。

**`$connection_requests`**  
  当前通过一个连接获得的请求数量。

**`$msec`**  
  日志写入时间。单位为秒，精度是毫秒。

**`$pipe`**  
  如果请求是通过HTTP流水线(pipelined)发送，pipe值为“ `p` ”，否则为“ `.` ”。

**`$request_length`**  
  请求的长度（包括请求行，请求头和请求正文）。

**`$request_time`**  
  请求处理时间，单位为秒，精度毫秒；
从读入客户端的第一个字节开始，直到把最后一个字符发送给客户端后进行日志写入为止。

**`$status`**  
  响应状态。

**`$time_iso8601`**  
  ISO8601标准格式下的本地时间。

**`$time_local`**  
  通用日志格式下的本地时间。

发送给客户端的响应头拥有“ `sent_http_` ”前缀。 比如 `$sent_http_content_range` 。

配置始终包含预先定义的“ `combined` ”日志格式：

```
log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```

## open_log_file_cache

```
Syntax:  open_log_file_cache off;
Default: off
Context: location, http, server
```

定义一个缓存，用来存储频繁使用的文件名中包含变量的日志文件描述符。 该指令包含以下参数：

**`max`**  
  设置缓存中描述符的最大数量；如果缓存被占满，最近最少使用（LRU）的描述符将被关闭。

**`inactive`**  
  设置缓存文件描述符在多长时间内没有被访问就关闭；
默认为10秒。

**`min_uses`**  
  设置在 `inactive` 参数指定的时间里，
最少访问多少次才能使文件描述符保留在缓存中；默认为1。

**`valid`**  
  设置一段用于检查超时后文件是否仍以同样名字存在的时间；
默认为60秒。

**`off`**  
  禁用缓存。

使用实例：

```
open_log_file_cache max=1000 inactive=20s valid=1m min_uses=2;
```

