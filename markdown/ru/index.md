# nginx

**Revision:** 169  
**Language:** ru

nginx (" *engine x* ")—это HTTP-сервер, обратный прокси сервер с поддержкой кеширования и балансировки нагрузки, TCP/UDP прокси-сервер, а также почтовый прокси-сервер. Изначально разработан [Игорем Сысоевым](http://sysoev.ru) и распространяется под [лицензией BSD из 2 пунктов](../LICENSE) .

nginx известен своей исключительной гибкостью, высокой производительностью и минимальным потреблением ресурсов. Он также:

- самый популярный веб-сервер в мире
[ [Netcraft](https://news.netcraft.com/archives/category/web-server-survey/) ];
- один из самых востребованных [Docker-образов](https://hub.docker.com/search?q=nginx) [ [DataDog](https://www.datadoghq.com/docker-adoption/#six) ];
- активно используется в [Ingress-контроллерах
для Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) ,
включая [наш собственный](https://github.com/nginxinc/kubernetes-ingress) .

Корпоративное распространение, коммерческая поддержка и тренинги осуществляются компанией [F5, Inc.](../ru/enterprise.xml)

# Основная функциональность HTTP-сервера {#basic_http_features}

- Обслуживание статических запросов, [индексных
файлов](docs/http/ngx_http_index_module.xml) , [автоматическое
создание списка файлов](docs/http/ngx_http_autoindex_module.xml) , [кэш дескрипторов открытых файлов](docs/http/ngx_http_core_module.xml#open_file_cache) ;
- [Акселерированное
обратное проксирование с кэшированием](docs/http/ngx_http_proxy_module.xml) , [распределение нагрузки
и отказоустойчивость](docs/http/ngx_http_upstream_module.xml) ;
- Акселерированная поддержка [FastCGI](docs/http/ngx_http_fastcgi_module.xml) , [uwsgi](docs/http/ngx_http_uwsgi_module.xml) , [SCGI](docs/http/ngx_http_scgi_module.xml) и [memcached](docs/http/ngx_http_memcached_module.xml) серверов с кэшированием, [распределение нагрузки
и отказоустойчивость](docs/http/ngx_http_upstream_module.xml) ;
- Модульность, фильтры, в том числе [сжатие (gzip)](docs/http/ngx_http_gzip_module.xml) ,
byte-ranges (докачка),
chunked ответы, [XSLT-фильтр](docs/http/ngx_http_xslt_module.xml) , [SSI-фильтр](docs/http/ngx_http_ssi_module.xml) , [преобразование
изображений](docs/http/ngx_http_image_filter_module.xml) ;
несколько подзапросов на одной странице, обрабатываемые в SSI-фильтре
через прокси или FastCGI/uwsgi/SCGI, выполняются параллельно;
- [Поддержка SSL и
расширения TLS SNI](docs/http/ngx_http_ssl_module.xml) ;
- Поддержка [HTTP/2](docs/http/ngx_http_v2_module.xml) с приоритизацией на основе весов и зависимостей;
- Поддержка [HTTP/3](docs/http/ngx_http_v3_module.xml) .

# Другие возможности HTTP-сервера {#other_http_features}

- [Виртуальные серверы](docs/http/request_processing.xml) ,
определяемые по IP-адресу и имени;
- Поддержка [keep-alive](docs/http/ngx_http_core_module.xml#keepalive_timeout) и pipelined соединений;
- [Настройка
форматов логов](docs/http/ngx_http_log_module.xml#log_format) , [буферизованная
запись в лог](docs/http/ngx_http_log_module.xml#access_log) , [быстрая ротация логов](docs/control.xml#logs) , [запись в syslog](docs/syslog.xml) ;
- [Специальные
страницы](docs/http/ngx_http_core_module.xml#error_page) для ошибок 3xx-5xx;
- rewrite-модуль: [изменение URI
с помощью регулярных выражений](docs/http/ngx_http_rewrite_module.xml) ;
- [Выполнение
разных функций](docs/http/ngx_http_rewrite_module.xml#if) в зависимости от [адреса клиента](docs/http/ngx_http_geo_module.xml) ;
- Ограничение доступа в зависимости от [адреса клиента](docs/http/ngx_http_access_module.xml) , [по паролю
(HTTP Basic аутентификация)](docs/http/ngx_http_auth_basic_module.xml) и по [результату
подзапроса](docs/http/ngx_http_auth_request_module.xml) ;
- Проверка [HTTP referer](docs/http/ngx_http_referer_module.xml) ;
- [Методы
PUT, DELETE, MKCOL, COPY и MOVE](docs/http/ngx_http_dav_module.xml) ;
- [FLV](docs/http/ngx_http_flv_module.xml) и [MP4](docs/http/ngx_http_mp4_module.xml) стриминг;
- [Ограничение скорости отдачи ответов](docs/http/ngx_http_core_module.xml#limit_rate) ;
- Ограничение числа одновременных [соединений](docs/http/ngx_http_limit_conn_module.xml) и [запросов](docs/http/ngx_http_limit_req_module.xml) с одного адреса;
- [Геолокация по IP-адресу](docs/http/ngx_http_geoip_module.xml) ;
- [A/B-тестирование](docs/http/ngx_http_split_clients_module.xml) ;
- [Зеркалирование запросов](docs/http/ngx_http_mirror_module.xml) ;
- Встроенный [Perl](docs/http/ngx_http_perl_module.xml) ;
- сценарный язык [njs](docs/njs/index.xml) .

# Функциональность почтового прокси-сервера {#mail_proxy_server_features}

- Перенаправление пользователя на [IMAP](docs/mail/ngx_mail_imap_module.xml) -
или [POP3](docs/mail/ngx_mail_pop3_module.xml) -сервер
с использованием внешнего HTTP-сервера [аутентификации](docs/mail/ngx_mail_auth_http_module.xml) ;
- Проверка пользователя с помощью внешнего HTTP-сервера [аутентификации](docs/mail/ngx_mail_auth_http_module.xml) и перенаправление соединения на внутренний [SMTP](docs/mail/ngx_mail_smtp_module.xml) -сервер;
- Методы аутентификации:
  - [POP3](docs/mail/ngx_mail_pop3_module.xml#pop3_auth) :
USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
  - [IMAP](docs/mail/ngx_mail_imap_module.xml#imap_auth) :
LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
  - [SMTP](docs/mail/ngx_mail_smtp_module.xml#smtp_auth) :
AUTH LOGIN/PLAIN/CRAM-MD5;
  
- Поддержка [SSL](docs/mail/ngx_mail_ssl_module.xml) ;
- Поддержка [STARTTLS
и STLS](docs/mail/ngx_mail_ssl_module.xml#starttls) .

# Функциональность TCP/UDP прокси-сервера {#generic_proxy_server_features}

- [Проксирование
TCP и UDP;](docs/stream/ngx_stream_proxy_module.xml)
- Поддержка [SSL](docs/stream/ngx_stream_ssl_module.xml) и
расширения TLS [SNI](docs/stream/ngx_stream_ssl_preread_module.xml) для TCP;
- [Распределение нагрузки
и отказоустойчивость](docs/stream/ngx_stream_upstream_module.xml) ;
- Ограничение доступа в зависимости от [адреса клиента](docs/stream/ngx_stream_access_module.xml) ;
- Выполнение разных функций в зависимости от [адреса клиента](docs/http/ngx_http_geo_module.xml) ;
- Ограничение числа одновременных [соединений](docs/stream/ngx_stream_limit_conn_module.xml) с одного адреса;
- [Настройка
форматов логов](docs/stream/ngx_stream_log_module.xml#log_format) , [буферизованная
запись в лог](docs/stream/ngx_stream_log_module.xml#access_log) , [быстрая ротация логов](docs/control.xml#logs) , [запись в syslog](docs/syslog.xml) ;
- [Геолокация по IP-адресу](docs/stream/ngx_stream_geoip_module.xml) ;
- [A/B-тестирование](docs/stream/ngx_stream_split_clients_module.xml) ;
- сценарный язык [njs](docs/njs/index.xml) .

# Архитектура и масштабируемость {#architecture_and_scalability}

- Один главный и несколько рабочих процессов, рабочие процессы работают под
непривилегированным пользователем;
- [Гибкость конфигурации](docs/example.xml) ;
- [Изменение настроек](docs/control.xml#reconfiguration) и [обновление
исполняемого файла](docs/control.xml#upgrade) без перерыва в обслуживании клиентов;
- [Поддержка](docs/events.xml) kqueue (FreeBSD 4.1+),
epoll (Linux 2.6+),
/dev/poll (Solaris 7 11/99+), event ports (Solaris 10), select и poll;
- Использование возможностей, предоставляемых kqueue, таких как
 EV_CLEAR, EV_DISABLE (для временного выключения события),
NOTE_LOWAT, EV_EOF, число доступных данных, коды ошибок;
- Использование возможностей, предоставляемых epoll, таких как
EPOLLRDHUP (Linux 2.6.17+, glibc 2.8+) и
EPOLLEXCLUSIVE (Linux 4.5+, glibc 2.24+);
- Поддержка sendfile (FreeBSD 3.1+, Linux 2.2+, macOS 10.5+),
sendfile64 (Linux 2.4.21+) и sendfilev (Solaris 8 7/01+);
- Поддержка [файлового
AIO](docs/http/ngx_http_core_module.xml#aio) (FreeBSD 4.3+, Linux 2.6.22+);
- Поддержка [DIRECTIO](docs/http/ngx_http_core_module.xml#directio) (FreeBSD 4.4+, Linux 2.4+, Solaris 2.6+, macOS);
- [Поддержка](docs/http/ngx_http_core_module.xml#listen) accept-фильтров (FreeBSD 4.1+, NetBSD 5.0+) и TCP_DEFER_ACCEPT (Linux 2.4+);
- На 10 000 неактивных HTTP keep-alive соединений расходуется
около 2.5M памяти;
- Минимум операций копирования данных.

# Протестированные ОС и платформы {#tested_os_and_platforms}

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

