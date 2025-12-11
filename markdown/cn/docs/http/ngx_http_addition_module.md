# ngx_http_addition_module模块

**Translator:** Weibin Yao  
**Revision:** 1  
**Language:** cn


`ngx_http_addition_module` 是一个过滤模块，它可以在回复正文前后加上内容。
这个模块默认不会编译进去，若要开启需加上编译选项：`--with-http_addition_module`。

## 配置示例 {#example}

```
location / {
    add_before_body /before_action;
    add_after_body  /after_action;
}
```

## 指令 {#directives}


uri

location


在回复正文之前加入一段文字，nginx会发起一个子请求去获取这些文字。




uri

location


在回复正文之后加入一段文字，nginx会发起一个子请求去获取这些文字。




mime-type ...
text/html
http
server
location
0.7.9


指定生效的回复MIME类型，默认始终包含“text/html”。
如果设置类型为“*”，就会匹配任何类型的回复(0.8.29)。


