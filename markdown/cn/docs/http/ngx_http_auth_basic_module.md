# ngx_http_auth_basic_module模块

**Translator:** WenMing  
**Revision:** 1  
**Language:** cn

模块 `ngx_http_auth_basic_module` 允许使用“HTTP基本认证”协议验证用户名和密码来限制对资源的访问。

也可以通过 [地址](ngx_http_auth_basic_module.xml) 来限制访问。 使用 [satisfy](ngx_http_core_module.xml#satisfy) 指令就能同时通过地址和密码来限制访问。

# 配置范例 {#example}

```
location / {
    auth_basic           "closed site";
    auth_basic_user_file conf/htpasswd;
}
```

# 指令 {#directives}

## auth_basic

```
Syntax:  string | off
Default: off
Context: limit_except, http, server, location
```

开启使用“HTTP基本认证”协议的用户名密码验证。 指定的参数被用作 `域` 。 参数 `off` 可以取消继承自上一个配置等级 `auth_basic` 指令的影响。

## auth_basic_user_file

```
Syntax:  file
Default: 
Context: limit_except, http, server, location
```

指定保存用户名和密码的文件，格式如下：

```
# comment
name1:password1
name2:password2:comment
name3:password3
```

密码应该使用 `crypt()` 函数加密。 可以用Apache发行包中的 `htpasswd` 命令来创建此类文件。

