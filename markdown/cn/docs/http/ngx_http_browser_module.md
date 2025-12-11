# ngx_http_browser_module模块

**Translator:** litianqing  
**Revision:** 1  
**Language:** cn


模块`ngx_http_browser_module`创建变量，它们的值取决于
请求头中**User-Agent**的值：

***$modern_browser***  
  如果浏览器被为识别为新式浏览器，该值等于指令设置的值；
***$ancient_browser***  
  如果浏览器被识别为旧式浏览器，该值等于指令设置的值；
***$msie***  
  如果浏览器被识别为任何版本的MSIE，该值等于“1”。

## 配置示例 {#example}

选择一个默认页:

```
modern_browser_value "modern.";

modern_browser msie      5.5;
modern_browser gecko     1.0.0;
modern_browser opera     9.0;
modern_browser safari    413;
modern_browser konqueror 3.0;

index index.${modern_browser}html index.html;
```

旧式浏览器的重定向：

```
modern_browser msie      5.0;
modern_browser gecko     0.9.1;
modern_browser opera     8.0;
modern_browser safari    413;
modern_browser konqueror 3.0;

modern_browser unlisted;

ancient_browser Links Lynx netscape4;

if ($ancient_browser) {
    rewrite ^ /ancient.html;
}
```

## 指令 {#directives}


string ...

http
server
location


如果任一指定的子串在请求头的User-Agent域中被发现，浏览器将被认定为旧式浏览器。
特殊字符串“netscape4” 相当于正则表达式“^Mozilla/[1-4]”。




string
1
http
server
location


设定变量$ancient_browser的值。




browser version
unlisted

http
server
location


指定一个版本，此版本及后续版本的浏览器都被认定为新式浏览器。
浏览器可以是下列之一： msie,
gecko (基于Mozilla),
opera，safari,
或者 konqueror。



版本可被指定为以下形式：X, X.X, X.X.X, 或 X.X.X.X。
每一形式的最大值分别是4000, 4000.99, 4000.99.99, 和 4000.99.99.99。



浏览器既没有在modern_browser中列出，又没有在中
列出时，如果配置了特殊值unlisted，那么浏览器将被认定为新式浏览器，否则
认定为旧式浏览器。
如果请求头中没有User-Agent域，浏览器以没有列出对待。




string
1
http
server
location


设定变量$modern_browser的值。


