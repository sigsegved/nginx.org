# Module ngx_http_realip_module

**Revision:** 8  
**Language:** en


The `ngx_http_realip_module` module is used
to change the client address and optional port
to those sent in the specified header field.

This module is not built by default, it should be enabled with the
`--with-http_realip_module`
configuration parameter.

## Example Configuration {#example}

```
set_real_ip_from  192.168.1.0/24;
set_real_ip_from  192.168.2.1;
set_real_ip_from  2001:0db8::/32;
real_ip_header    X-Forwarded-For;
real_ip_recursive on;
```

## Directives {#directives}



    address |
    CIDR |
    unix:

http
server
location


Defines trusted addresses that are known to send correct
replacement addresses.
If the special value unix: is specified,
all UNIX-domain sockets will be trusted.
Trusted addresses may also be specified using a hostname (1.13.1).

IPv6 addresses are supported starting from versions 1.3.0 and 1.2.1.






    field |
    X-Real-IP |
    X-Forwarded-For |
    proxy_protocol
X-Real-IP
http
server
location


Defines the request header field
whose value will be used to replace the client address.



The request header field value that contains an optional port
is also used to replace the client port (1.11.0).
The address and port should be specified according to
RFC 3986.



The proxy_protocol parameter (1.5.12) changes
the client address to the one from the PROXY protocol header.
The PROXY protocol must be previously enabled by setting the
proxy_protocol parameter
in the  directive.




on | off
off
http
server
location
1.3.0
1.2.1


If recursive search is disabled, the original client address that
matches one of the trusted addresses is replaced by the last
address sent in the request header field defined by the
 directive.
If recursive search is enabled, the original client address that
matches one of the trusted addresses is replaced by the last
non-trusted address sent in the request header field.



## Embedded Variables {#variables}

***$realip_remote_addr***  
  keeps the original client address (1.9.7)
***$realip_remote_port***  
  keeps the original client port (1.11.0)
