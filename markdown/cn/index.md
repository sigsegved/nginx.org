# nginx

**Revision:** 3  
**Language:** cn


nginx [engine x]是[Igor Sysoev](http://sysoev.ru/en/)编写的一个HTTP和反向代理服务器，另外它也可以作为邮件代理服务器。
它已经在众多流量很大的俄罗斯网站上使用了很长时间，这些网站包括[Yandex](http://www.yandex.ru)、[Mail.Ru](http://www.mail.ru)、[VKontakte](http://www.vkontakte.ru)，以及[Rambler](http://www.rambler.ru)。据Netcraft统计，在2012年8月份，[世界上最繁忙的网站中有11.48%](http://news.netcraft.com/archives/2012/08/02/august-2012-web-server-survey.html)使用Nginx作为其服务器或者代理服务器。部分成功案例请见：
[Netflix](https://signup.netflix.com/openconnect/software)，
[Wordpress.com](http://barry.wordpress.com/2008/04/28/load-balancer-update/)，
[FastMail.FM](http://blog.fastmail.fm/2007/01/04/webimappop-frontend-proxies-changed-to-nginx/)。

Nginx的源码使用的许可为[两条款类BSD协议](http://nginx.org/LICENSE)。

## 基本的HTTP服务器特性 {#basic_http_features}

- 处理静态文件，[索引](docs/http/ngx_http_index_module.html)文件以及[自动索引](docs/http/ngx_http_autoindex_module.html)；[打开文件描述符缓存](docs/http/ngx_http_core_module.xml#open_file_cache)；
- [使用缓存加速反向代理](docs/http/ngx_http_proxy_module.html)；[简单负载均衡以及容错](docs/http/ngx_http_upstream_module.html)；
- 远程[FastCGI](docs/http/ngx_http_fastcgi_module.html)，uwsgi，SCGI，和[memcached](docs/http/ngx_http_memcached_module.html)服务的缓存加速支持；[简单的负载均衡以及容错](docs/http/ngx_http_upstream_module.html)；
- 模块化的架构。过滤器包括[gzip压缩](docs/http/ngx_http_gzip_module.html)、ranges支持、chunked响应、[XSLT](docs/http/ngx_http_xslt_module.html)，[SSI](docs/http/ngx_http_ssi_module.html)以及[图像缩放](docs/http/ngx_http_image_filter_module.html)。在SSI 过滤器中，一个包含多个SSI的页面，如果经由FastCGI或反向代理处理，可被并行处理；
- [支持SSL，TLS SNI](docs/http/ngx_http_ssl_module.html)。

## 其他的HTTP服务器特性 {#other_http_features}

- 基于名字和IP的[虚拟主机](docs/http/request_processing.html)；
- [Keep-alive](docs/http/ngx_http_core_module.xml#keepalive_timeout)和pipelined连接支持；
- 灵活的配置；
- [重新加载配置](docs/control.xml#reconfiguration)以及[在线升级](docs/control.xml#upgrade)时，不需要中断正在处理的请求；
- [自定义访问日志格式](docs/http/ngx_http_log_module.xml#log_format)，[带缓存的日志写操作](docs/http/ngx_http_log_module.xml#access_log)以及[快速日志轮转](docs/control.xml#logs)；
- 3xx-5xx错误代码[重定向](docs/http/ngx_http_core_module.xml#error_page)；
- 重写（rewrite）模块：[使用正则表达式改变URI](docs/http/ngx_http_rewrite_module.html)；
- 根据[客户端地址](docs/http/ngx_http_geo_module.html)[执行不同的功能](docs/http/ngx_http_rewrite_module.xml#if)；
- 基于[客户端IP地址](docs/http/ngx_http_access_module.html)和[HTTP基本认证机制](docs/http/ngx_http_auth_basic_module.html)的访问控制；
- 支持验证[HTTP referer](docs/http/ngx_http_referer_module.html)；
- 支持[PUT、DELETE、MKCOL、COPY以及MOVE](docs/http/ngx_http_dav_module.html)方法；
- 支持[FLV流](docs/http/ngx_http_flv_module.html)和[MP4流](docs/http/ngx_http_mp4_module.html)；
- [速度限制](docs/http/ngx_http_core_module.xml#limit_rate)；
- 来自同一地址的同时[连接数](docs/http/ngx_http_limit_conn_module.html)或[请求数](docs/http/ngx_http_limit_req_module.html)限制；
- [嵌入Perl语言](docs/http/ngx_http_perl_module.html)。

## 邮件代理服务器特性 {#mail_proxy_server_features}

- 使用外部HTTP[认证](docs/mail/ngx_mail_auth_http_module.html)服务器重定向用户到[IMAP](docs/mail/ngx_mail_imap_module.html)/[POP3](docs/mail/ngx_mail_pop3_module.html)后端；
- 使用外部HTTP[认证](docs/mail/ngx_mail_auth_http_module.html)服务器认证用户后重定向连接到内部[SMTP](docs/mail/ngx_mail_smtp_module.html)后端；
- 支持的认证方式：


- [POP3](docs/mail/ngx_mail_pop3_module.xml#pop3_auth): USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
- [IMAP](docs/mail/ngx_mail_imap_module.xml#imap_auth): LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
- [SMTP](docs/mail/ngx_mail_smtp_module.xml#smtp_auth): AUTH LOGIN/PLAIN/CRAM-MD5;
- [SSL](docs/mail/ngx_mail_ssl_module.html)支持；
- [STARTTLS和STLS](docs/mail/ngx_mail_ssl_module.xml#starttls)支持。

## 架构和扩展性 {#architecture_and_scalability}

- 一个主进程和多个工作进程，工作进程以非特权用户运行；
- [支持](docs/events.html)的事件机制：kqueue（FreeBSD 4.1+）、epoll（Linux 2.6+）、rt signals（Linux 2.2.19+）、/dev/poll（Solaris 7 11/99+）、event ports（Solaris 10）、select以及poll；
- 众多支持的kqueue特性包括EV_CLEAR、EV_DISABLE（临时禁止事件）、NOTE_LOWAT、EV_EOF，可用数据的数量，错误代码；
- 支持sendfile（FreeBSD 3.1+, Linux 2.2+, Mac OS X 10.5+）、sendfile64（Linux 2.4.21+）和sendfilev（Solaris 8 7/01+）；
- [文件AIO](docs/http/ngx_http_core_module.xml#aio)（FreeBSD 4.3+, Linux 2.6.22+）；
- [DIRECTIO](docs/http/ngx_http_core_module.xml#directio)
(FreeBSD 4.4+, Linux 2.4+, Solaris 2.6+, Mac OS X);
- [支持](docs/http/ngx_http_core_module.xml#listen)Accept-filters（FreeBSD 4.1+, NetBSD 5.0+）和 TCP_DEFER_ACCEPT（Linux 2.4+）；
- 10000个非活跃的HTTP keep-alive连接仅占用约2.5M内存；
- 尽可能避免数据拷贝操作。

## 测试过的操作系统和平台 {#tested_os_and_platforms}

- FreeBSD 3 — 10 / i386; FreeBSD 5 — 10 / amd64;
- Linux 2.2 — 3 / i386; Linux 2.6 — 3 / amd64;
- Solaris 9 / i386, sun4u; Solaris 10 / i386, amd64, sun4v;
- AIX 7.1 / powerpc;
- HP-UX 11.31 / ia64;
- MacOS X / ppc, i386;
- Windows XP, Windows Server 2003.
