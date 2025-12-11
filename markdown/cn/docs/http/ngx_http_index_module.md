# ngx_http_index_module模块

**Translator:** litianqing  
**Revision:** 1  
**Language:** cn


模块 `ngx_http_index_module` 处理以斜线字符(‘`/`’)结尾的请求。

## 配置范例 {#example}

```
location / {
    index index.$geo.html index.html;
}
```

## 指令 {#directives}


file ...
index.html
http
server
location


定义将要被作为默认页的文件。
文件 file 的名字可以包含变量。
文件以配置中指定的顺序被nginx检查。
列表中的最后一个元素可以是一个带有绝对路径的文件。
例子：

index index.$geo.html index.0.html /index.html;




需要注意的是，index文件会引发内部重定向，请求可能会被其它location处理。
比如，下面这个例子：

location = / {
    index index.html;
}

location / {
    ...
}

请求“/”实际上将会在第二个location中作为“/index.html”被处理。


