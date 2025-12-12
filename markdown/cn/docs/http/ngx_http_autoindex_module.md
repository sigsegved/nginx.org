# ngx_http_autoindex_module模块

**Translator:** Weibin Yao  
**Revision:** 1  
**Language:** cn

`ngx_http_autoindex_module` 模块可以列出目录中的文件。 一般当 [ngx_http_index_module](ngx_http_index_module.xml) 模块找不到默认主页的时候，会把请求转给 `ngx_http_autoindex_module` 模块去处理。

# 配置示例 {#example}

```
location / {
    autoindex on;
}
```

# 指令 {#directives}

## autoindex

```
Syntax:  on | off
Default: off
Context: location, http, server
```

开启或者关闭列出目录中文件的功能。

## autoindex_exact_size

```
Syntax:  on | off
Default: on
Context: location, http, server
```

设置目录中列出的文件是显示精确大小，还是对KB，MB，GB进行四舍五入。

## autoindex_localtime

```
Syntax:  on | off
Default: off
Context: location, http, server
```

设置目录中列出文件的时间是本地时间还是UTC时间。

