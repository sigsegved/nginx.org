# ngx_http_flv_module 模块

**Translator:** litianqing  
**Revision:** 1  
**Language:** cn

模块 `ngx_http_flv_module` 为Flash Video(FLV)文件 提供服务端伪流媒体支持

通过返回以请求偏移位置开始的文件内容，该模块专门处理 在查询串中有 `start` 参数的请求, 和有预先设置到FLV头部的请求。

这个模块并不是默认构建的，必须通过配置参数 `--with-http_flv_module` 来启用。

# 配置范例 {#example}

```
location ~ \.flv$ {
    flv;
}
```

# 指令 {#directives}

## flv

```
Syntax:  flv;
Default: 
Context: location
```

在当前location里使用这个模块处理请求。

