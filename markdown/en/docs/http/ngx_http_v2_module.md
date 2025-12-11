# Module ngx_http_v2_module

**Revision:** 19  
**Language:** en


The `ngx_http_v2_module` module (1.9.5) provides
support for
[HTTP/2](https://datatracker.ietf.org/doc/html/rfc7540).

This module is not built by default, it should be enabled with
the `--with-http_v2_module`
configuration parameter.

## Known Issues {#issues}

Before version 1.9.14,
buffering of a client request body could not be disabled
regardless of
[](ngx_http_proxy_module.xml#proxy_request_buffering),
[](ngx_http_fastcgi_module.xml#fastcgi_request_buffering),
[](ngx_http_uwsgi_module.xml#uwsgi_request_buffering), and
[](ngx_http_scgi_module.xml#scgi_request_buffering)
directive values.

Before version 1.19.1,
the [](ngx_http_core_module.xml#lingering_close) mechanism
was not used to control closing HTTP/2 connections.

## Example Configuration {#example}

```
server {
    listen 443 ssl;

    http2 on;

    ssl_certificate server.crt;
    ssl_certificate_key server.key;
}
```

Note that accepting HTTP/2 connections over TLS requires
the “Application-Layer Protocol Negotiation” (ALPN) TLS extension
support, which is available since
[OpenSSL](http://www.openssl.org) version 1.0.2.

Also note that if the
[](ngx_http_ssl_module.xml#ssl_prefer_server_ciphers) directive
is set to the value “`on`”,
the [ciphers](ngx_http_ssl_module.xml#ssl_ciphers)
should be configured to comply with
[RFC 9113, Appendix A](https://datatracker.ietf.org/doc/html/rfc9113#appendix-A)
black list and supported by clients.

## Directives {#directives}


on | off
off
http
server
1.25.1


Enables
the HTTP/2
protocol.




size
64k
http
server
1.11.0


Sets the size of the buffer per each request
in which the request body may be saved
before it is started to be processed.




size
8k
http
server
location


Sets the maximum size of chunks
into which the response body is sliced.
A too low value results in higher overhead.
A too high value impairs prioritization due to

HOL blocking.




time
3m
http
server



This directive is obsolete since version 1.19.7.
The 
directive should be used instead.




Sets the timeout of inactivity after which the connection is closed.




number
10
http
server
1.13.9



This directive is obsolete since version 1.25.1.




Limits the maximum number of concurrent
push requests in a connection.




number
128
http
server


Sets the maximum number of concurrent HTTP/2 streams
in a connection.




size
4k
http
server



This directive is obsolete since version 1.19.7.
The 
directive should be used instead.




Limits the maximum size of
an HPACK-compressed
request header field.
The limit applies equally to both name and value.
Note that if Huffman encoding is applied,
the actual size of decompressed name and value strings may be larger.
For most requests, the default limit should be enough.




size
16k
http
server



This directive is obsolete since version 1.19.7.
The 
directive should be used instead.




Limits the maximum size of the entire request header list after
HPACK decompression.
For most requests, the default limit should be enough.




number
1000
http
server
1.11.6



This directive is obsolete since version 1.19.7.
The 
directive should be used instead.




Sets the maximum number of requests (including
push requests) that can be served
through one HTTP/2 connection,
after which the next client request will lead to connection closing
and the need of establishing a new connection.



Closing connections periodically is necessary to free
per-connection memory allocations.
Therefore, using too high maximum number of requests
could result in excessive memory usage and not recommended.




uri | off
off
http
server
location
1.13.9



This directive is obsolete since version 1.25.1.
The 
directive can be used instead.




Pre-emptively sends
(pushes)
a request to the specified uri
along with the response to the original request.
Only relative URIs with absolute path will be processed,
for example:

http2_push /static/css/main.css;

The uri value can contain variables.



Several http2_push directives
can be specified on the same configuration level.
The off parameter cancels the effect
of the http2_push directives
inherited from the previous configuration level.




on | off
off
http
server
location
1.13.9



This directive is obsolete since version 1.25.1.




Enables automatic conversion of
preload
links
specified in the Link response header fields into
push
requests.




size
256k
http


Sets the size of the per
worker
input buffer.




time
30s
http
server



This directive is obsolete since version 1.19.7.
The 
directive should be used instead.




Sets the timeout for expecting more data from the client,
after which the connection is closed.



## Embedded Variables {#variables}

The `ngx_http_v2_module` module
supports the following embedded variables:

***$http2***  
  negotiated protocol identifier:
“`h2`” for HTTP/2 over TLS,
“`h2c`” for HTTP/2 over cleartext TCP,
or an empty string otherwise.
