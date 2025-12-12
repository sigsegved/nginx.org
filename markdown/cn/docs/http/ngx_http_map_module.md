# Module ngx_http_map_module

**Translator:** yzprofile  
**Revision:** 1  
**Language:** cn

模块 `ngx_http_map_module` 可以创建一些和另外变量相关联的变量。

# 配置范例 {#example}

```
map $http_host $name {
    hostnames;

    default       0;

    example.com   1;
    *.example.com 1;
    example.org   2;
    *.example.org 2;
    .example.net  3;
    wap.*         4;
}

map $http_user_agent $mobile {
    default       0;
    "~Opera Mini" 1;
}
```

# 指令 {#directives}

## map

```
Syntax:  string $variable
Default: 
Context: http
```

在配置的参数中，第一个是要创建新的变量，它的值取决于后面一个或多个源变量。

> **Note:** 在0.9.0版本之前，这里只支持一个变量。

在 `map` 块里的参数指定了源变量值和结果值的对应关系。

源变量值可以使用字符串或者正则表达式 (0.9.6)。

一个正则表达式如果以 “ `~` ” 开头，这个正则表达式对大小写敏感； 若以 “ `~*` ”开头 (1.0.4)，这个正则表达式对大小写不敏感。 且正则表达式里可以包含命名捕获和位置捕获，这些变量可以跟结果变量一起被其它指令使用。

如果源变量的值正好跟特殊参数同名（看下面），它要以 “ `\` ” 字符作为前缀。

结果变量可以是一个字符串也可以是另外一个变量 (0.9.0)。

这个指令也支持三个特殊参数。

**`default` `value`**  
  如果源变量值没有匹配到任何变量，则设置一个默认值作为结果。
当没有设置 `default` ，将会用一个空的字符串作为默认的结果。

**`hostnames`**  
  允许用前缀或者后缀掩码指定域名作为源变量值，举个例子，

```
*.example.com 1;
example.*     1;
```

  这两条记录

```
example.com   1;
*.example.com 1;
```

  可以被合并为：

```
.example.com  1;
```

  这个参数必须写在值映射列表的最前面。

**`include` `file`**  
  包含一个或者多个存有映射值的文件。

如果源值匹配了多余一个的指定变量，例如掩码和正则同时匹配，那么将会按照下面的顺序进行优先选择：

1. 没有掩码的字符串
2. 最长的带前缀的字符串，例如: “ `*.example.com` ”
3. 最长的带后缀的字符串，例如：“ `mail.*` ”
4. 按顺序第一个先匹配的正则表达式 （在配置文件中体现的顺序）
5. 默认值

## map_hash_bucket_size

```
Syntax:  size
Default: 32|64|128
Context: http
```

为 [map](#map) 的变量哈稀表设置桶大小。 默认值取决于处理器cache line的大小。 可以从这里获取到更多参考信息： [设置哈稀表](../hash.xml) .

## map_hash_max_size

```
Syntax:  size
Default: 2048
Context: http
```

设置 [map](#map) 变量哈稀表 `大小` 的上限。 可以从这里获取到更多参考信息： [设置哈稀表](../hash.xml) .

