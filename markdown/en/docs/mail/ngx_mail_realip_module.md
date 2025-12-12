# Module ngx_mail_realip_module

**Revision:** 1  
**Language:** en

The `ngx_mail_realip_module` module is used to change the client address and port to the ones sent in the PROXY protocol header (1.19.8). The PROXY protocol must be previously enabled by setting the [proxy_protocol](ngx_mail_core_module.xml#proxy_protocol) parameter in the `listen` directive.

# Example Configuration {#example}

```
listen 110 proxy_protocol;

set_real_ip_from  192.168.1.0/24;
set_real_ip_from  192.168.2.1;
set_real_ip_from  2001:0db8::/32;
```

# Directives {#directives}

## set_real_ip_from

```
Syntax:  set_real_ip_from address | CIDR | unix:;
Default: 
Context: server, mail
```

Defines trusted addresses that are known to send correct replacement addresses. If the special value `unix:` is specified, all UNIX-domain sockets will be trusted.

