# ngx_http_gzip_static_module模块

**Translator:** WenMing  
**Revision:** 1  
**Language:** cn

模块 `ngx_http_gzip_static_module` 允许发送以“ `.gz` ”作为文件扩展名的预压缩文件，以替代发送普通文件。

这个模块不是默认编译的，因此需要指定 `--with-http_gzip_static_module` 编译选项。

# 配置范例 {#example}

```
gzip_static  on;
gzip_proxied expired no-cache no-store private auth;
```

# 指令 {#directives}

## gzip_static

```
Syntax:  on | off
Default: off
Context: location, http, server
```

启用或者禁用检查预压缩文件是否存在。 与以下指令共同确定功能开启: [gzip_http_version](ngx_http_gzip_module.xml#gzip_http_version) , [gzip_proxied](ngx_http_gzip_module.xml#gzip_proxied) , [gzip_disable](ngx_http_gzip_module.xml#gzip_disable) , 和 [gzip_vary](ngx_http_gzip_module.xml#gzip_vary) .

文件可以使用 `gzip` 命令来进行压缩，或任何其他兼容的命令。 建议压缩文件和原始文件的修改日期和时间保持一致。

