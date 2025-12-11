# ngx_http_geoip_module 模块

**Translator:** cfsego  
**Revision:** 1  
**Language:** cn


`ngx_http_geoip_module` 模块（0.8.6+）创建变量，使用预编译的[MaxMind](http://www.maxmind.com)数据库解析客户端IP地址，得到变量值。

nginx默认不编译这个模块，需要开启`--with-http_geoip_module`编译选项。

> **Note:** 模块依赖[MaxMind GeoIP](http://www.maxmind.com/app/c)库。

## 配置示例 {#example}

```
http {
    geoip_country         GeoIP.dat;
    geoip_city            GeoLiteCity.dat;
    geoip_proxy           192.168.100.0/24;
    geoip_proxy           2001:0db8::/32;
    geoip_proxy_recursive on;
    ...
```

## 指令 {#directives}


database

http


指定数据库，用于根据客户端IP地址得到其所在国家。
使用这个数据库时，配置中可用下列变量：


$geoip_country_code

双字符国家代码，比如
“RU”，“US”。


$geoip_country_code3

三字符国家代码，比如
“RUS”，“USA”。


$geoip_country_name

国家名称，比如
“Russian Federation”，“United States”。







database

http


指定数据库，用于根据客户端IP地址得到其所在的国家、行政区和城市。
使用这个数据库时，配置中可用下列变量：


$geoip_city_country_code

双字符国家代码，比如
“RU”，“US”。


$geoip_city_country_code3

三字符国家代码，比如
“RUS”，“USA”。


$geoip_city_country_name

国家名称，比如
“Russian Federation”，“United States”。


$geoip_region

国家行政区名（行政区、直辖区、州、省、联邦管辖区，诸如此类），比如
“Moscow City”，“DC”。


$geoip_city

城市名称，比如
“Moscow”，“Washington”。


$geoip_postal_code

邮编。







address | CIDR

http
1.3.0
1.2.1


定义可信地址。
如果请求来自可信地址，nginx将使用其X-Forwarded-For头来获得地址。




on | off
off
http
1.3.0
1.2.1


如果关闭递归查找，在客户端地址与某个可信地址匹配时，nginx将使用X-Forwarded-For中的最后一个地址来代替原始客户端地址。
如果开启递归查找，在客户端地址与某个可信地址匹配时，nginx将使用X-Forwarded-For中最后一个与所有可信地址都不匹配的地址来代替原始客户端地址。


