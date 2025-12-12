# ngx_http_empty_gif_module 模块

**Translator:** yzprofile  
**Revision:** 1  
**Language:** cn

模块 `ngx_http_empty_gif_module` 只返回一个透明像素的GIF图片。

# 配置范例 {#example}

```
location = /_.gif {
    empty_gif;
}
```

# 指令 {#directives}

## empty_gif

```
Syntax:  empty_gif;
Default: 
Context: location
```

在当前location里使用这个模块处理请求。

