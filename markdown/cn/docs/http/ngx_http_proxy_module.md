# ngx_http_proxy_module 模块

**Translator:** cfsego  
**Revision:** 1  
**Language:** cn

`ngx_http_proxy_module` 模块允许传送请求到其它服务器。

# 配置示例 {#example}

```
location / {
    proxy_pass       http://localhost:8000;
    proxy_set_header Host      $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

# 指令 {#directives}

## proxy_buffer_size

```
Syntax:  proxy_buffer_size size;
Default: 4k|8k
Context: location, http, server
```

设置缓冲区的大小为 `size` 。nginx从被代理的服务器读取响应时，使用该缓冲区保存响应的开始部分。这部分通常包含着一个小小的响应头。该缓冲区大小默认等于 [proxy_buffers](#proxy_buffers) 指令设置的一块缓冲区的大小，但它也可以被设置得更小。

## proxy_buffering

```
Syntax:  proxy_buffering on | off;
Default: on
Context: location, http, server
```

代理的时候，开启或关闭缓冲后端服务器的响应。

当开启缓冲时，nginx尽可能快地从被代理的服务器接收响应，再将它存入 [proxy_buffer_size](#proxy_buffer_size) 和 [proxy_buffers](#proxy_buffers) 指令设置的缓冲区中。如果响应无法整个纳入内存，那么其中一部分将存入磁盘上的 [临时文件](#proxy_temp_path) 。 [proxy_max_temp_file_size](#proxy_max_temp_file_size) 和 [proxy_temp_file_write_size](#proxy_temp_file_write_size) 指令可以控制临时文件的写入。

当关闭缓冲时，收到响应后，nginx立即将其同步传给客户端。nginx不会尝试从被代理的服务器读取整个请求，而是将 [proxy_buffer_size](#proxy_buffer_size) 指令设定的大小作为一次读取的最大长度。

响应头 `X-Accel-Buffering` 传递“ `yes` ”或“ `no` ”可以动态地开启或关闭代理的缓冲功能。 这个能力可以通过 [proxy_ignore_headers](ngx_http_proxy_module.xml#proxy_ignore_headers) 指令关闭。

## proxy_buffers

```
Syntax:  proxy_buffers number size;
Default: 8 4k|8k
Context: location, http, server
```

为每个连接设置缓冲区的数量为 `number` ，每块缓冲区的大小为 `size` 。这些缓冲区用于保存从被代理的服务器读取的响应。每块缓冲区默认等于一个内存页的大小。这个值是4K还是8K，取决于平台。

## proxy_busy_buffers_size

```
Syntax:  proxy_busy_buffers_size size;
Default: 8k|16k
Context: location, http, server
```

当开启 [缓冲](#proxy_buffering) 响应的功能以后，在没有读到全部响应的情况下，写缓冲到达一定 `大小` 时，nginx一定会向客户端发送响应，直到缓冲小于此值。这条指令用来设置此值。 同时，剩余的缓冲区可以用于接收响应，如果需要，一部分内容将缓冲到临时文件。该 `大小` 默认是 [proxy_buffer_size](#proxy_buffer_size) 和 [proxy_buffers](#proxy_buffers) 指令设置单块缓冲大小的两倍。

## proxy_cache

```
Syntax:  proxy_cache zone | off;
Default: off
Context: location, http, server
```

指定用于页面缓存的共享内存。同一块共享内存可以在多个地方使用。 `off` 参数可以屏蔽从上层配置继承的缓存功能。

## proxy_cache_bypass

```
Syntax:  proxy_cache_bypass string ...;
Default: 
Context: location, http, server
```

定义nginx不从缓存取响应的条件。如果至少一个字符串条件非空而且非“0”，nginx就不会从缓存中去取响应：

```
proxy_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
proxy_cache_bypass $http_pragma    $http_authorization;
```

本指令可和与 [proxy_no_cache](#proxy_no_cache) 一起使用。

## proxy_cache_key

```
Syntax:  proxy_cache_key string;
Default: $scheme$proxy_host$request_uri
Context: location, http, server
```

定义如何生成缓存的键，比如

```
proxy_cache_key "$host$request_uri $cookie_user";
```

这条指令的默认值类似于下面字符串

```
proxy_cache_key $scheme$proxy_host$uri$is_args$args;
```

## proxy_cache_lock

```
Syntax:  proxy_cache_lock on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

开启此功能时，对于相同的请求，同时只允许一个请求发往后端，并根据 [proxy_cache_key](#proxy_cache_key) 指令的设置在缓存中植入一个新条目。 其他请求相同条目的请求将一直等待，直到缓存中出现相应的内容，或者锁在 [proxy_cache_lock_timeout](#proxy_cache_lock_timeout) 指令设置的超时后被释放。

## proxy_cache_lock_timeout

```
Syntax:  proxy_cache_lock_timeout time;
Default: 5s
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

为 [proxy_cache_lock](#proxy_cache_lock) 指令设置锁的超时。

## proxy_cache_min_uses

```
Syntax:  proxy_cache_min_uses number;
Default: 1
Context: location, http, server
```

设置响应被缓存的最小请求 `次数` 。

## proxy_cache_path

```
Syntax:  proxy_cache_path path [levels=levels] keys_zone=name:size [inactive=time] [max_size=size] [loader_files=number] [loader_sleep=time] [loader_threshold=time];
Default: 
Context: http
```

设置缓存的路径和其他参数。缓存数据是保存在文件中的，缓存的键和文件名都是在代理URL上执行MD5的结果。 `levels` 参数定义了缓存的层次结构。比如，下面配置

```
proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=one:10m;
```

缓存中文件名看起来是这样的：

```
/data/nginx/cache/c/29/b7f54b2df7773722d382f4809d65029c
```

被缓存的响应首先写入一个临时文件，然后进行重命名。从0.8.9版本开始，临时文件和缓存可以放在不同的文件系统。但请注意，这将导致文件在这两个文件系统中进行拷贝，而不是廉价的重命名操作。因此，针对任何路径，都建议将缓存和 [proxy_temp_path](#proxy_temp_path) 指令设置的临时文件目录放在同一文件系统。

此外，所有活动的键和缓存数据相关的信息都被存放在共享内存中。共享内存通过 `keys_zone` 参数的 `name` 和 `size` 来定义。被缓存的数据如果在 `inactive` 参数指定的时间内未被访问，就会被从缓存中移除，不论它是否是刚产生的。 `inactive` 的默认值是10分钟。

特殊进程“cache manager”监控缓存的条目数量，如果超过 `max_size` 参数设置的最大值，使用LRU算法移除缓存数据。

nginx新启动后不就，特殊进程“cache loader”就被启动。该进程将文件系统上保存的过去缓存的数据的相关信息重新加载到共享内存。加载过程分多次迭代完成，每次迭代，进程只加载不多于 `loader_files` 参数指定的文件数量（默认值为100）。此外，每次迭代过程的持续时间不能超过 `loader_threshold` 参数的值（默认200毫秒）。每次迭代之间，nginx的暂停时间由 `loader_sleep` 参数指定（默认50毫秒）。

## proxy_cache_use_stale

```
Syntax:  proxy_cache_use_stale error | timeout | invalid_header | updating | http_500 | http_502 | http_503 | http_504 | http_404 | off ...;
Default: off
Context: location, http, server
```

如果后端服务器出现状况，nginx是可以使用过期的响应缓存的。这条指令就是定义何种条件下允许开启此机制。这条指令的参数与 [proxy_next_upstream](#proxy_next_upstream) 指令的参数相同。

此外， `updating` 参数允许nginx在正在更新缓存的情况下使用过期的缓存作为响应。这样做可以使更新缓存数据时，访问源服务器的次数最少。

在植入新的缓存条目时，如果想使访问源服务器的次数最少，可以使用 [proxy_cache_lock](#proxy_cache_lock) 指令。

## proxy_cache_valid

```
Syntax:  proxy_cache_valid [code ...] time;
Default: 
Context: location, http, server
```

为不同的响应状态码设置不同的缓存时间。比如，下面指令

```
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404      1m;
```

设置状态码为200和302的响应的缓存时间为10分钟，状态码为404的响应的缓存时间为1分钟。

如果仅仅指定了 `time` ，

```
proxy_cache_valid 5m;
```

那么只有状态码为200、300和302的响应会被缓存。

如果使用了 `any` 参数，那么就可以缓存任何响应：

```
proxy_cache_valid 200 302 10m;
proxy_cache_valid 301      1h;
proxy_cache_valid any      1m;
```

缓存参数也可以直接在响应头中设定。这种方式的优先级高于使用这条指令设置缓存时间。 `X-Accel-Expires` 响应头可以以秒为单位设置响应的缓存时间，如果值为0，表示禁止缓存响应，如果值以 `@` 开始，表示自1970年1月1日以来的秒数，响应一直会被缓存到这个绝对时间点。 如果不含 `X-Accel-Expires` 响应头，缓存参数仍可能被 `Expires` 或者 `Cache-Control` 响应头设置。 如果响应头含有 `Set-Cookie` ，响应将不能被缓存。 这些头的处理过程可以使用指令 [proxy_ignore_headers](#proxy_ignore_headers) 忽略。

## proxy_connect_timeout

```
Syntax:  proxy_connect_timeout time;
Default: 60s
Context: location, http, server
```

设置与后端服务器建立连接的超时时间。应该注意这个超时一般不可能大于75秒。

## proxy_cookie_domain

```
Syntax:  proxy_cookie_domain domain replacement;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.15.*

设置 `Set-Cookie` 响应头中的 `domain` 属性的替换文本。 假设后端服务器返回的 `Set-Cookie` 响应头含有属性“ `domain=localhost` ”，那么指令

```
proxy_cookie_domain localhost example.org;
```

将这个属性改写为“ `domain=example.org` ”。

`domain` 和 `replacement` 配置字符串，以及 `domain` 属性中起始的点将被忽略。 匹配过程大小写不敏感。

`domain` 和 `replacement` 配置字符串中可以包含变量：

```
proxy_cookie_domain www.$host $host;
```

这条指令同样可以使用正则表达式。这时， `domain` 应以“ `~` ”标志开始，且可以使用命名匹配组和位置匹配组，而 `replacement` 可以引用这些匹配组：

```
proxy_cookie_domain ~\.(?P<sl_domain>[-0-9a-z]+\.[a-z]+)$ $sl_domain;
```

可以同时定义多条 `proxy_cookie_domain` 指令：

```
proxy_cookie_domain localhost example.org;
proxy_cookie_domain ~\.([a-z]+\.[a-z]+)$ $1;
```

`off` 参数可以取消当前配置级别的所有 `proxy_cookie_domain` 指令：

```
proxy_cookie_domain off;
proxy_cookie_domain localhost example.org;
proxy_cookie_domain www.example.org example.org;
```

## proxy_cookie_path

```
Syntax:  proxy_cookie_path path replacement;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.15.*

设置 `Set-Cookie` 响应头中的 `path` 属性的替换文本。 假设后端服务器返回的 `Set-Cookie` 响应头含有属性“ `path=/two/some/uri/` ”，那么指令

```
proxy_cookie_path /two/ /;
```

将这个属性改写为“ `path=/some/uri/` ”。

`path` 和 `replacement` 配置字符串可以包含变量：

```
proxy_cookie_path $uri /some$uri;
```

这条指令同样可以使用正则表达式。如果使用大小写敏感的匹配， `path` 应以“ `~` ”标志开始，如果使用大小写不敏感的匹配， `path` 应以“ `~*` ”标志开始。 `path` 可以使用命名匹配组和位置匹配组， `replacement` 可以引用这些匹配组：

```
proxy_cookie_path ~*^/user/([^/]+) /u/$1;
```

可以同时定义多条 `proxy_cookie_path` 指令：

```
proxy_cookie_path /one/ /;
proxy_cookie_path / /two/;
```

`off` 参数可以取消当前配置级别的所有 `proxy_cookie_path` 指令：

```
proxy_cookie_path off;
proxy_cookie_path /two/ /;
proxy_cookie_path ~*^/user/([^/]+) /u/$1;
```

## proxy_hide_header

```
Syntax:  proxy_hide_header field;
Default: 
Context: location, http, server
```

nginx默认不会将 `Date` 、 `Server` 、 `X-Pad` ，和 `X-Accel-...` 响应头发送给客户端。 `proxy_hide_header` 指令则可以设置额外的响应头，这些响应头也不会发送给客户端。相反的，如果希望允许传递某些响应头给客户端，可以使用 [proxy_pass_header](#proxy_pass_header) 指令。

## proxy_http_version

```
Syntax:  proxy_http_version 1.0 | 1.1;
Default: 1.0
Context: location, http, server
```

*This directive appeared in version 1.1.4.*

设置代理使用的HTTP协议版本。默认使用的版本是1.0，而1.1版本则推荐在使用 [keepalive](ngx_http_upstream_module.xml#keepalive) 连接时一起使用。

## proxy_ignore_client_abort

```
Syntax:  proxy_ignore_client_abort on | off;
Default: off
Context: location, http, server
```

决定当客户端在响应传输完成前就关闭连接时，nginx是否应关闭后端连接。

## proxy_ignore_headers

```
Syntax:  proxy_ignore_headers field ...;
Default: 
Context: location, http, server
```

不处理后端服务器返回的指定响应头。下面的响应头可以被设置： `X-Accel-Redirect` ， `X-Accel-Expires` ， `X-Accel-Limit-Rate` (1.1.6)， `X-Accel-Buffering` (1.1.6)， `X-Accel-Charset` (1.1.6)， `Expires` ， `Cache-Control` ，和 `Set-Cookie` (0.8.44)。

如果不被取消，这些头部的处理可能产生下面结果：

- `X-Accel-Expires` ， `Expires` ， `Cache-Control` ，和 `Set-Cookie` 设置响应 [缓存](#proxy_cache_valid) 的参数；
- `X-Accel-Redirect` 执行到指定URI的 [内部跳转](ngx_http_core_module.xml#internal) ；
- `X-Accel-Limit-Rate` 设置响应到客户端的传输 [速率限制](ngx_http_core_module.xml#limit_rate) ；
- `X-Accel-Buffering` 启动或者关闭响应 [缓冲](#proxy_buffering) ；
- `X-Accel-Charset` 设置响应所需的 [字符集](ngx_http_charset_module.xml#charset) 。

## proxy_intercept_errors

```
Syntax:  proxy_intercept_errors on | off;
Default: off
Context: location, http, server
```

当后端服务器的响应状态码大于等于400时，决定是否直接将响应发送给客户端，亦或将响应转发给nginx由 [error_page](ngx_http_core_module.xml#error_page) 指令来处理。

## proxy_max_temp_file_size

```
Syntax:  proxy_max_temp_file_size size;
Default: 1024m
Context: location, http, server
```

打开响应 [缓冲](#proxy_buffering) 以后，如果整个响应不能存放在 [proxy_buffer_size](#proxy_buffer_size) 和 [proxy_buffers](#proxy_buffers) 指令设置的缓冲区内，部分响应可以存放在临时文件中。 这条指令可以设置临时文件的最大 `容量` 。而每次写入临时文件的数据量则由 [proxy_temp_file_write_size](#proxy_temp_file_write_size) 指令定义。

将此值设置为0将禁止响应写入临时文件。

## proxy_next_upstream

```
Syntax:  proxy_next_upstream error | timeout | invalid_header | http_500 | http_502 | http_503 | http_504 | http_404 | off ...;
Default: error timeout
Context: location, http, server
```

指定在何种情况下一个失败的请求应该被发送到下一台后端服务器：

**`error`**  
  和后端服务器建立连接时，或者向后端服务器发送请求时，或者从后端服务器接收响应头时，出现错误；

**`timeout`**  
  和后端服务器建立连接时，或者向后端服务器发送请求时，或者从后端服务器接收响应头时，出现超时；

**`invalid_header`**  
  后端服务器返回空响应或者非法响应头；

**`http_500`**  
  后端服务器返回的响应状态码为500；

**`http_502`**  
  后端服务器返回的响应状态码为502；

**`http_503`**  
  后端服务器返回的响应状态码为503；

**`http_504`**  
  后端服务器返回的响应状态码为504；

**`http_404`**  
  后端服务器返回的响应状态码为404；

**`off`**  
  停止将请求发送给下一台后端服务器。

需要理解一点的是，只有在没有向客户端发送任何数据以前，将请求转给下一台后端服务器才是可行的。也就是说，如果在传输响应到客户端时出现错误或者超时，这类错误是不可能恢复的。

## proxy_no_cache

```
Syntax:  proxy_no_cache string ...;
Default: 
Context: location, http, server
```

定义nginx不将响应写入缓存的条件。如果至少一个字符串条件非空而且非“0”，nginx就不将响应存入缓存：

```
proxy_no_cache $cookie_nocache $arg_nocache$arg_comment;
proxy_no_cache $http_pragma    $http_authorization;
```

这条指令可以和 [proxy_cache_bypass](#proxy_cache_bypass) 指令一起使用。

## proxy_pass

```
Syntax:  proxy_pass URL;
Default: 
Context: limit_except, location, if in location
```

设置后端服务器的协议和地址，还可以设置可选的URI以定义本地路径和后端服务器的映射关系。 这条指令可以设置的协议是“ `http` ”或者“ `https` ”，而地址既可以使用域名或者IP地址加端口（可选）的形式来定义：

```
proxy_pass http://localhost:8000/uri/;
```

又可以使用UNIX域套接字路径来定义。该路径接在“ `unix` ”字符串后面，两端由冒号所包围，比如：

```
proxy_pass http://unix:/tmp/backend.socket:/uri/;
```

如果解析一个域名得到多个地址，所有的地址都会以轮转的方式被使用。当然，也可以使用 [服务器组](ngx_http_upstream_module.xml) 来定义地址。

请求URI按下面规则传送给后端服务器：

- 如果 `proxy_pass` 使用了URI，当传送请求到后端服务器时， [规范化](ngx_http_core_module.xml#location) 以后的请求路径与配置中的路径的匹配部分将被替换为指令中定义的URI：
  ```
location /name/ {
    proxy_pass http://127.0.0.1/remote/;
}
```

- 如果 `proxy_pass` 没有使用URI，传送到后端服务器的请求URI一般客户端发起的原始URI，如果nginx改变了请求URI，则传送的URI是nginx改变以后完整的规范化URI：
  ```
location /some/path/ {
    proxy_pass http://127.0.0.1;
}
```

  > **Note:** 在1.1.12版以前，如果 `proxy_pass` 没有使用URI，某些情况下，nginx改变URI以后，会错误地将原始URI而不是改变以后的URI发送到后端服务器。

某些情况下，无法确定请求URI中应该被替换的部分：

- 使用正则表达式定义路径。
  这种情况下，指令不应该使用URI。

- 在需要代理的路径中，使用 [rewrite](ngx_http_rewrite_module.xml#rewrite) 指令改变了URI，但仍使用相同配置处理请求( `break` )：
  ```
location /name/ {
    rewrite    /name/([^/]+) /users?name=$1 break;
    proxy_pass http://127.0.0.1;
}
```

  这种情况下，本指令设置的URI会被忽略，改变后的URI将被发送给后端服务器。

后端服务器的地址，端口和URI中都可以使用变量：

```
proxy_pass http://$host$uri;
```

甚至像这样：

```
proxy_pass $request;
```

这种情况下，后端服务器的地址将会在定义的 [服务器组](ngx_http_upstream_module.xml) 中查找。如果查找不到，nginx使用 [resolver](ngx_http_core_module.xml#resolver) 来查找该地址。

## proxy_pass_header

```
Syntax:  proxy_pass_header field;
Default: 
Context: location, http, server
```

允许传送 [被屏蔽](#proxy_hide_header) 的后端服务器响应头到客户端。

## proxy_read_timeout

```
Syntax:  proxy_read_timeout time;
Default: 60s
Context: location, http, server
```

定义从后端服务器读取响应的超时。此超时是指相邻两次读操作之间的最长时间间隔，而不是整个响应传输完成的最长时间。如果后端服务器在超时时间段内没有传输任何数据，连接将被关闭。

## proxy_redirect

```
Syntax:  proxy_redirect redirect replacement;
Default: default
Context: location, http, server
```

设置后端服务器 `Location` 响应头和 `Refresh` 响应头的替换文本。 假设后端服务器返回的响应头是 “ `Location: http://localhost:8000/two/some/uri/` ”，那么指令

```
proxy_redirect http://localhost:8000/two/ http://frontend/one/;
```

将把字符串改写为 “ `Location: http://frontend/one/some/uri/` ”。

`replacement` 字符串可以省略服务器名：

```
proxy_redirect http://localhost:8000/two/ /;
```

此时将使用代理服务器的主域名和端口号来替换。如果端口是80，可以不加。

用 `default` 参数指定的默认替换使用了 [location](ngx_http_core_module.xml#location) 和 [proxy_pass](#proxy_pass) 指令的参数。因此，下面两例配置等价：

```
location /one/ {
    proxy_pass     http://upstream:port/two/;
    proxy_redirect default;
```

```
location /one/ {
    proxy_pass     http://upstream:port/two/;
    proxy_redirect http://upstream:port/two/ /one/;
```

而且因为同样的原因， [proxy_pass](#proxy_pass) 指令使用变量时，不允许本指令使用 `default` 参数。

`replacement` 字符串可以包含变量：

```
proxy_redirect http://localhost:8000/ http://$host:$server_port/;
```

而 `redirect` 字符串从1.1.11版本开始也可以包含变量：

```
proxy_redirect http://$proxy_host:8000/ /;
```

同时，从1.1.11版本开始，指令支持正则表达式。使用正则表达式的话，如果是大小写敏感的匹配， `redirect` 以“ `~` ”作为开始，如果是大小写不敏感的匹配， `redirect` 以“ `~*` ”作为开始。而且 `redirect` 的正则表达式中可以包含命名匹配组和位置匹配组，而在 `replacement` 中可以引用这些匹配组的值：

```
proxy_redirect ~^(http://[^:]+):\d+(/.+)$ $1$2;
proxy_redirect ~*/user/([^/]+)/(.+)$      http://$1.example.com/$2;
```

除此以外，可以同时定义多个 `proxy_redirect` 指令：

```
proxy_redirect default;
proxy_redirect http://localhost:8000/  /;
proxy_redirect http://www.example.com/ /;
```

另外， `off` 参数可以使所有相同配置级别的 `proxy_redirect` 指令无效：

```
proxy_redirect off;
proxy_redirect default;
proxy_redirect http://localhost:8000/  /;
proxy_redirect http://www.example.com/ /;
```

最后，使用这条指令也可以为地址为相对地址的重定向添加域名：

```
proxy_redirect / /;
```

## proxy_send_timeout

```
Syntax:  proxy_send_timeout time;
Default: 60s
Context: location, http, server
```

定义向后端服务器传输请求的超时。此超时是指相邻两次写操作之间的最长时间间隔，而不是整个请求传输完成的最长时间。如果后端服务器在超时时间段内没有接收到任何数据，连接将被关闭。

## proxy_set_header

```
Syntax:  proxy_set_header field value;
Default: Connection close
Context: location, http, server
```

允许重新定义或者添加发往后端服务器的请求头。 `value` 可以包含文本、变量或者它们的组合。 当且仅当当前配置级别中没有定义 `proxy_set_header` 指令时，会从上面的级别继承配置。 默认情况下，只有两个请求头会被重新定义：

```
proxy_set_header Host       $proxy_host;
proxy_set_header Connection close;
```

如果不想改变请求头 `Host` 的值，可以这样来设置：

```
proxy_set_header Host       $http_host;
```

但是，如果客户端请求头中没有携带这个头部，那么传递到后端服务器的请求也不含这个头部。 这种情况下，更好的方式是使用 `$host` 变量——它的值在请求包含 `Host` 请求头时为 `Host` 字段的值，在请求未携带 `Host` 请求头时为虚拟主机的主域名：

```
proxy_set_header Host       $host;
```

此外，服务器名可以和后端服务器的端口一起传送：

```
proxy_set_header Host       $host:$proxy_port;
```

如果某个请求头的值为空，那么这个请求头将不会传送给后端服务器：

```
proxy_set_header Accept-Encoding "";
```

## proxy_ssl_session_reuse

```
Syntax:  proxy_ssl_session_reuse on | off;
Default: on
Context: location, http, server
```

决定是否重用与后端服务器的SSL会话。如果日志中出现“ `SSL3_GET_FINISHED:digest check failed` ”错误，请尝试关闭会话重用。

## proxy_store

```
Syntax:  proxy_store on | off | string;
Default: off
Context: location, http, server
```

开启将文件保存到磁盘上的功能。如果设置为 `on` ，nginx将文件保存在 [alias](ngx_http_core_module.xml#alias) 指令或 [root](ngx_http_core_module.xml#root) 指令设置的路径中。如果设置为 `off` ，nginx将关闭文件保存的功能。此外，保存的文件名也可以使用含变量的 `string` 参数来指定：

```
proxy_store /data/www$original_uri;
```

保存文件的修改时间根据接收到的 `Last-Modified` 响应头来设置。响应都是先写到临时文件，然后进行重命名来生成的。从0.8.9版本开始，临时文件和持久化存储可以放在不同的文件系统，但是需要注意这时文件执行的是在两个文件系统间拷贝操作，而不是廉价的重命名操作。因此建议保存文件的路径和 [proxy_temp_path](#proxy_temp_path) 指令设置的临时文件的路径在同一个文件系统中。

这条指令可以用于创建静态无更改文件的本地拷贝，比如：

```
location /images/ {
    root                   /data/www;
    open_file_cache_errors off;
    error_page             404 = /fetch$uri;
}

location /fetch/ {
    internal;

    proxy_pass             http://backend/;
    proxy_store            on;
    proxy_store_access     user:rw group:rw all:r;
    proxy_temp_path        /data/temp;

    alias                  /data/www/;
}
```

或者像这样：

```
location /images/ {
    root               /data/www;
    error_page         404 = @fetch;
}

location @fetch {
    internal;

    proxy_pass         http://backend;
    proxy_store        on;
    proxy_store_access user:rw group:rw all:r;
    proxy_temp_path    /data/temp;

    root               /data/www;
}
```

## proxy_store_access

```
Syntax:  proxy_store_access users:permissions ...;
Default: user:rw
Context: location, http, server
```

设置新创建的文件和目录的访问权限，比如：

```
proxy_store_access user:rw group:rw all:r;
```

如果指定了任何 `group` 或者 `all` 的访问权限，那么可以略去 `user` 的访问权限：

```
proxy_store_access group:rw all:r;
```

## proxy_temp_file_write_size

```
Syntax:  proxy_temp_file_write_size size;
Default: 8k|16k
Context: location, http, server
```

在开启缓冲后端服务器响应到临时文件的功能后，设置nginx每次写数据到临时文件的 `size(大小)` 限制。 `size` 的默认值是 [proxy_buffer_size](#proxy_buffer_size) 指令和 [proxy_buffers](#proxy_buffers) 指令定义的每块缓冲区大小的两倍， 而临时文件最大容量由 [proxy_max_temp_file_size](#proxy_max_temp_file_size) 指令设置。

## proxy_temp_path

```
Syntax:  proxy_temp_path path [level1 [level2 [level3]]];
Default: proxy_temp
Context: location, http, server
```

定义从后端服务器接收的临时文件的存放路径，可以为临时文件路径定义至多三层子目录的目录树。 比如，下面配置

```
proxy_temp_path /spool/nginx/proxy_temp 1 2;
```

那么临时文件的路径看起来会是这样：

```
/spool/nginx/proxy_temp/7/45/00000123457
```

# 内嵌变量 {#variables}

`ngx_http_proxy_module` 支持内嵌变量，可以用于在 [proxy_set_header](#proxy_set_header) 指令中构造请求头：

**`$proxy_host`**  
  后端服务器的主机名和端口；

**`$proxy_port`**  
  后端服务器的端口；

**`$proxy_add_x_forwarded_for`**  
  将 `$remote_addr` 变量值添加在客户端 `X-Forwarded-For` 请求头的后面，并以逗号分隔。
如果客户端请求未携带 `X-Forwarded-For` 请求头， `$proxy_add_x_forwarded_for` 变量值将与 `$remote_addr` 变量相同。

