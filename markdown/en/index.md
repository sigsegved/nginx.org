# nginx

**Revision:** 169  
**Language:** en

nginx (" *engine x* ") is an HTTP web server, reverse proxy, content cache, load balancer, TCP/UDP proxy server, and mail proxy server. Originally written by [Igor Sysoev](http://sysoev.ru/en/) and distributed under the [2-clause BSD License](../LICENSE) .

Known for flexibility and high performance with low resource utilization, nginx is:

- the world's most popular web server
[ [Netcraft](https://news.netcraft.com/archives/category/web-server-survey/) ];
- consistently one of the most popular [Docker images](https://hub.docker.com/search?q=nginx) [ [DataDog](https://www.datadoghq.com/docker-adoption/#six) ];
- powering multiple [Ingress
Controllers for Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) ,
including [our own](https://github.com/nginxinc/kubernetes-ingress) .

Enterprise distributions, commercial support and training are [available from F5, Inc.](enterprise.xml)

# Basic HTTP server features {#basic_http_features}

- Serving static and [index](docs/http/ngx_http_index_module.xml) files, [autoindexing](docs/http/ngx_http_autoindex_module.xml) ; [open file descriptor cache](docs/http/ngx_http_core_module.xml#open_file_cache) ;
- [Accelerated
reverse proxying with caching](docs/http/ngx_http_proxy_module.xml) ; [load balancing
and fault tolerance](docs/http/ngx_http_upstream_module.xml) ;
- Accelerated support with caching of [FastCGI](docs/http/ngx_http_fastcgi_module.xml) , [uwsgi](docs/http/ngx_http_uwsgi_module.xml) , [SCGI](docs/http/ngx_http_scgi_module.xml) , and [memcached](docs/http/ngx_http_memcached_module.xml) servers; [load balancing
and fault tolerance](docs/http/ngx_http_upstream_module.xml) ;
- Modular architecture.
Filters include [gzipping](docs/http/ngx_http_gzip_module.xml) ,
byte ranges, chunked responses, [XSLT](docs/http/ngx_http_xslt_module.xml) , [SSI](docs/http/ngx_http_ssi_module.xml) ,
and [image
transformation](docs/http/ngx_http_image_filter_module.xml) filter.
Multiple SSI inclusions within a single page can be processed in
parallel if they are handled by proxied or FastCGI/uwsgi/SCGI servers;
- [SSL and
TLS SNI support](docs/http/ngx_http_ssl_module.xml) ;
- Support for [HTTP/2](docs/http/ngx_http_v2_module.xml) with weighted and dependency-based prioritization;
- Support for [HTTP/3](docs/http/ngx_http_v3_module.xml) .

# Other HTTP server features {#other_http_features}

- Name-based and IP-based [virtual servers](docs/http/request_processing.xml) ;
- [Keep-alive](docs/http/ngx_http_core_module.xml#keepalive_timeout) and pipelined connections support;
- [Access
log formats](docs/http/ngx_http_log_module.xml#log_format) , [buffered
log writing](docs/http/ngx_http_log_module.xml#access_log) , [fast log rotation](docs/control.xml#logs) , and [syslog logging](docs/syslog.xml) ;
- 3xx-5xx error codes [redirection](docs/http/ngx_http_core_module.xml#error_page) ;
- The rewrite module: [URI changing
using regular expressions](docs/http/ngx_http_rewrite_module.xml) ;
- [Executing
different functions](docs/http/ngx_http_rewrite_module.xml#if) depending on the [client address](docs/http/ngx_http_geo_module.xml) ;
- Access control based on [client IP address](docs/http/ngx_http_access_module.xml) , [by password (HTTP
Basic authentication)](docs/http/ngx_http_auth_basic_module.xml) and by the [result of
subrequest](docs/http/ngx_http_auth_request_module.xml) ;
- Validation of [HTTP referer](docs/http/ngx_http_referer_module.xml) ;
- The [PUT, DELETE, MKCOL, COPY,
and MOVE](docs/http/ngx_http_dav_module.xml) methods;
- [FLV](docs/http/ngx_http_flv_module.xml) and [MP4](docs/http/ngx_http_mp4_module.xml) streaming;
- [Response rate limiting](docs/http/ngx_http_core_module.xml#limit_rate) ;
- Limiting the number of simultaneous [connections](docs/http/ngx_http_limit_conn_module.xml) or [requests](docs/http/ngx_http_limit_req_module.xml) coming from one address;
- [IP-based geolocation](docs/http/ngx_http_geoip_module.xml) ;
- [A/B testing](docs/http/ngx_http_split_clients_module.xml) ;
- [Request mirroring](docs/http/ngx_http_mirror_module.xml) ;
- Embedded [Perl](docs/http/ngx_http_perl_module.xml) ;
- [njs](docs/njs/index.xml) scripting language.

# Mail proxy server features {#mail_proxy_server_features}

- User redirection to [IMAP](docs/mail/ngx_mail_imap_module.xml) or [POP3](docs/mail/ngx_mail_pop3_module.xml) server using an external HTTP [authentication](docs/mail/ngx_mail_auth_http_module.xml) server;
- User authentication using an external HTTP [authentication](docs/mail/ngx_mail_auth_http_module.xml) server and connection redirection to an internal [SMTP](docs/mail/ngx_mail_smtp_module.xml) server;
- Authentication methods:
  - [POP3](docs/mail/ngx_mail_pop3_module.xml#pop3_auth) :
USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
  - [IMAP](docs/mail/ngx_mail_imap_module.xml#imap_auth) :
LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
  - [SMTP](docs/mail/ngx_mail_smtp_module.xml#smtp_auth) :
AUTH LOGIN/PLAIN/CRAM-MD5;
  
- [SSL](docs/mail/ngx_mail_ssl_module.xml) support;
- [STARTTLS
and STLS](docs/mail/ngx_mail_ssl_module.xml#starttls) support.

# TCP/UDP proxy server features {#generic_proxy_server_features}

- [Generic proxying](docs/stream/ngx_stream_proxy_module.xml) of TCP and UDP;
- [SSL](docs/stream/ngx_stream_ssl_module.xml) and
TLS [SNI](docs/stream/ngx_stream_ssl_preread_module.xml) support
for TCP;
- [Load balancing
and fault tolerance](docs/stream/ngx_stream_upstream_module.xml) ;
- Access control based on [client address](docs/stream/ngx_stream_access_module.xml) ;
- Executing different functions depending on the [client address](docs/stream/ngx_stream_geo_module.xml) ;
- Limiting the number of simultaneous [connections](docs/stream/ngx_stream_limit_conn_module.xml) coming from one address;
- [Access
log formats](docs/stream/ngx_stream_log_module.xml#log_format) , [buffered
log writing](docs/stream/ngx_stream_log_module.xml#access_log) , [fast log rotation](docs/control.xml#logs) , and [syslog logging](docs/syslog.xml) ;
- [IP-based geolocation](docs/stream/ngx_stream_geoip_module.xml) ;
- [A/B testing](docs/stream/ngx_stream_split_clients_module.xml) ;
- [njs](docs/njs/index.xml) scripting language.

# Architecture and scalability {#architecture_and_scalability}

- One master and several worker processes;
worker processes run under an unprivileged user;
- [Flexible configuration](docs/example.xml) ;
- [Reconfiguration](docs/control.xml#reconfiguration) and [upgrade of an
executable](docs/control.xml#upgrade) without interruption of the client servicing;
- [Support](docs/events.xml) for
kqueue (FreeBSD 4.1+),
epoll (Linux 2.6+),
/dev/poll (Solaris 7 11/99+), event ports (Solaris 10),
select, and poll;
- The support of the various kqueue features including EV_CLEAR, EV_DISABLE
(to temporarily disable events), NOTE_LOWAT, EV_EOF, number of available data,
error codes;
- The support of various epoll features including
EPOLLRDHUP (Linux 2.6.17+, glibc 2.8+) and
EPOLLEXCLUSIVE (Linux 4.5+, glibc 2.24+);
- sendfile (FreeBSD 3.1+, Linux 2.2+, macOS 10.5+), sendfile64 (Linux 2.4.21+),
and sendfilev (Solaris 8 7/01+) support;
- [File AIO](docs/http/ngx_http_core_module.xml#aio) (FreeBSD 4.3+, Linux 2.6.22+);
- [DIRECTIO](docs/http/ngx_http_core_module.xml#directio) (FreeBSD 4.4+, Linux 2.4+, Solaris 2.6+, macOS);
- Accept-filters (FreeBSD 4.1+, NetBSD 5.0+) and TCP_DEFER_ACCEPT (Linux 2.4+) [support](docs/http/ngx_http_core_module.xml#listen) ;
- 10,000 inactive HTTP keep-alive connections take about 2.5M memory;
- Data copy operations are kept to a minimum.

# Tested OS and platforms {#tested_os_and_platforms}

- FreeBSD 3—12 / i386;
FreeBSD 5—12 / amd64;
FreeBSD 11 / ppc;
FreeBSD 12 / ppc64;
- Linux 2.2—4 / i386;
Linux 2.6—5 / amd64;
Linux 3—4 / armv6l, armv7l, aarch64, ppc64le;
Linux 4—5 / s390x;
- Solaris 9 / i386, sun4u;
Solaris 10 / i386, amd64, sun4v;
Solaris 11 / x86;
- AIX 7.1 / powerpc;
- HP-UX 11.31 / ia64;
- macOS / ppc, i386, x86_64;
- Windows XP,
Windows Server 2003,
Windows 7,
Windows 10,
Windows 11.

