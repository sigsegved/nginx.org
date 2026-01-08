# Module ngx_mail_proxy_module

**Revision:** 6  
**Language:** en

# Directives {#directives}

## proxy_buffer

```
Syntax:  proxy_buffer size;
Default: 4k|8k
Context: server, mail
```

Sets the size of the buffer used for proxying. By default, the buffer size is equal to one memory page. Depending on a platform, it is either 4K or 8K.

## proxy_pass_error_message

```
Syntax:  proxy_pass_error_message on | off;
Default: off
Context: server, mail
```

Indicates whether to pass the error message obtained during the authentication on the backend to the client.

Usually, if the authentication in nginx is a success, the backend cannot return an error. If it nevertheless returns an error, it means some internal error has occurred. In such case the backend message can contain information that should not be shown to the client. However, responding with an error for the correct password is a normal behavior for some POP3 servers. For example, CommuniGatePro informs a user about [mailbox overflow](http://www.stalker.com/CommuniGatePro/Alerts.html#Quota) or other events by periodically outputting the [authentication error](http://www.stalker.com/CommuniGatePro/POP.html#Alerts) . The directive should be enabled in this case.

## proxy_protocol

```
Syntax:  proxy_protocol on | off;
Default: off
Context: server, mail
```

*This directive appeared in version 1.19.8.*

Enables the [PROXY protocol](http://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) for connections to a backend.

## proxy_smtp_auth

```
Syntax:  proxy_smtp_auth on | off;
Default: off
Context: server, mail
```

*This directive appeared in version 1.19.4.*

Enables or disables user authentication on the SMTP backend using the `AUTH` command.

If [XCLIENT](#xclient) is also enabled, then the `XCLIENT` command will not send the `LOGIN` parameter.

## proxy_timeout

```
Syntax:  proxy_timeout timeout;
Default: 24h
Context: server, mail
```

Sets the `timeout` between two successive read or write operations on client or proxied server connections. If no data is transmitted within this time, the connection is closed.

## xclient

```
Syntax:  xclient on | off;
Default: on
Context: server, mail
```

Enables or disables the passing of the [XCLIENT](http://www.postfix.org/XCLIENT_README.html) command with client parameters when connecting to the SMTP backend.

With `XCLIENT` , the MTA is able to write client information to the log and apply various limitations based on this data.

If `XCLIENT` is enabled then nginx passes the following commands when connecting to the backend:

- `EHLO` with the [server name](ngx_mail_core_module.xml#server_name)
- `XCLIENT`
- `EHLO` or `HELO` ,
as passed by the client

If the name [found](ngx_mail_core_module.xml#resolver) by the client IP address points to the same address, it is passed in the `NAME` parameter of the `XCLIENT` command. If the name could not be found, points to a different address, or [resolver](ngx_mail_core_module.xml#resolver) is not specified, the `[UNAVAILABLE]` is passed in the `NAME` parameter. If an error has occurred in the process of resolving, the `[TEMPUNAVAIL]` value is used.

If `XCLIENT` is disabled then nginx passes the `EHLO` command with the [server name](ngx_mail_core_module.xml#server_name) when connecting to the backend if the client has passed `EHLO` , or `HELO` with the server name, otherwise.

