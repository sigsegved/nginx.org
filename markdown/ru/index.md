# nginx

**Revision:** 169  
**Language:** ru


nginx ("*engine x*")—это HTTP-сервер, обратный прокси сервер
с поддержкой кеширования и балансировки нагрузки,
TCP/UDP прокси-сервер,
а также почтовый прокси-сервер.
Изначально разработан [Игорем Сысоевым](http://sysoev.ru)
и распространяется под
[лицензией BSD из 2 пунктов](../LICENSE).

nginx известен своей исключительной гибкостью, высокой производительностью
и минимальным потреблением ресурсов.
Он также:


- самый популярный веб-сервер в мире
[[Netcraft](https://news.netcraft.com/archives/category/web-server-survey/)];
- один из самых востребованных
[Docker-образов](https://hub.docker.com/search?q=nginx)
[[DataDog](https://www.datadoghq.com/docker-adoption/#six)];
- активно используется в
[Ingress-контроллерах
для Kubernetes](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/),
включая
[наш собственный](https://github.com/nginxinc/kubernetes-ingress).

Корпоративное распространение, коммерческая поддержка и тренинги
осуществляются компанией [F5, Inc.](../ru/enterprise.html)

## Основная функциональность HTTP-сервера {#basic_http_features}

- Обслуживание статических запросов,
[индексных
файлов](docs/http/ngx_http_index_module.html),
[автоматическое
создание списка файлов](docs/http/ngx_http_autoindex_module.html),
[кэш дескрипторов открытых файлов](docs/http/ngx_http_core_module.xml#open_file_cache);
- [Акселерированное
обратное проксирование с кэшированием](docs/http/ngx_http_proxy_module.html),
[распределение нагрузки
и отказоустойчивость](docs/http/ngx_http_upstream_module.html);
- Акселерированная поддержка
[FastCGI](docs/http/ngx_http_fastcgi_module.html),
[uwsgi](docs/http/ngx_http_uwsgi_module.html),
[SCGI](docs/http/ngx_http_scgi_module.html) и
[memcached](docs/http/ngx_http_memcached_module.html)
серверов с кэшированием,
[распределение нагрузки
и отказоустойчивость](docs/http/ngx_http_upstream_module.html);
- Модульность, фильтры, в том числе
[сжатие (gzip)](docs/http/ngx_http_gzip_module.html),
byte-ranges (докачка),
chunked ответы,
[XSLT-фильтр](docs/http/ngx_http_xslt_module.html),
[SSI-фильтр](docs/http/ngx_http_ssi_module.html),
[преобразование
изображений](docs/http/ngx_http_image_filter_module.html);
несколько подзапросов на одной странице, обрабатываемые в SSI-фильтре
через прокси или FastCGI/uwsgi/SCGI, выполняются параллельно;
- [Поддержка SSL и
расширения TLS SNI](docs/http/ngx_http_ssl_module.html);
- Поддержка [HTTP/2](docs/http/ngx_http_v2_module.html)
с приоритизацией на основе весов и зависимостей;
- Поддержка [HTTP/3](docs/http/ngx_http_v3_module.html).

## Другие возможности HTTP-сервера {#other_http_features}

- [Виртуальные серверы](docs/http/request_processing.html),
определяемые по IP-адресу и имени;
- Поддержка
[keep-alive](docs/http/ngx_http_core_module.xml#keepalive_timeout)
и pipelined соединений;
- [Настройка
форматов логов](docs/http/ngx_http_log_module.xml#log_format),
[буферизованная
запись в лог](docs/http/ngx_http_log_module.xml#access_log),
[быстрая ротация логов](docs/control.xml#logs),
[запись в syslog](docs/syslog.html);
- [Специальные
страницы](docs/http/ngx_http_core_module.xml#error_page) для ошибок 3xx-5xx;
- rewrite-модуль:
[изменение URI
с помощью регулярных выражений](docs/http/ngx_http_rewrite_module.html);
- [Выполнение
разных функций](docs/http/ngx_http_rewrite_module.xml#if) в зависимости от
[адреса клиента](docs/http/ngx_http_geo_module.html);
- Ограничение доступа в зависимости от
[адреса клиента](docs/http/ngx_http_access_module.html),
[по паролю
(HTTP Basic аутентификация)](docs/http/ngx_http_auth_basic_module.html) и по
[результату
подзапроса](docs/http/ngx_http_auth_request_module.html);
- Проверка [HTTP referer](docs/http/ngx_http_referer_module.html);
- [Методы
PUT, DELETE, MKCOL, COPY и MOVE](docs/http/ngx_http_dav_module.html);
- [FLV](docs/http/ngx_http_flv_module.html)
и
[MP4](docs/http/ngx_http_mp4_module.html)
стриминг;
- [Ограничение скорости отдачи ответов](docs/http/ngx_http_core_module.xml#limit_rate);
- Ограничение числа одновременных
[соединений](docs/http/ngx_http_limit_conn_module.html) и
[запросов](docs/http/ngx_http_limit_req_module.html)
с одного адреса;
- [Геолокация по IP-адресу](docs/http/ngx_http_geoip_module.html);
- [A/B-тестирование](docs/http/ngx_http_split_clients_module.html);
- [Зеркалирование запросов](docs/http/ngx_http_mirror_module.html);
- Встроенный [Perl](docs/http/ngx_http_perl_module.html);
- сценарный язык [njs](docs/njs/index.html).

## Функциональность почтового прокси-сервера {#mail_proxy_server_features}

- Перенаправление пользователя на
[IMAP](docs/mail/ngx_mail_imap_module.html)-
или
[POP3](docs/mail/ngx_mail_pop3_module.html)-сервер
с использованием внешнего HTTP-сервера
[аутентификации](docs/mail/ngx_mail_auth_http_module.html);
- Проверка пользователя с помощью внешнего HTTP-сервера
[аутентификации](docs/mail/ngx_mail_auth_http_module.html)
и перенаправление соединения на внутренний
[SMTP](docs/mail/ngx_mail_smtp_module.html)-сервер;
- Методы аутентификации:


- [POP3](docs/mail/ngx_mail_pop3_module.xml#pop3_auth):
USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
- [IMAP](docs/mail/ngx_mail_imap_module.xml#imap_auth):
LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
- [SMTP](docs/mail/ngx_mail_smtp_module.xml#smtp_auth):
AUTH LOGIN/PLAIN/CRAM-MD5;
- Поддержка [SSL](docs/mail/ngx_mail_ssl_module.html);
- Поддержка
[STARTTLS
и STLS](docs/mail/ngx_mail_ssl_module.xml#starttls).

## Функциональность TCP/UDP прокси-сервера {#generic_proxy_server_features}

- [Проксирование
TCP и UDP;](docs/stream/ngx_stream_proxy_module.html)
- Поддержка [SSL](docs/stream/ngx_stream_ssl_module.html) и
расширения TLS
[SNI](docs/stream/ngx_stream_ssl_preread_module.html)
для TCP;
- [Распределение нагрузки
и отказоустойчивость](docs/stream/ngx_stream_upstream_module.html);
- Ограничение доступа в зависимости от
[адреса клиента](docs/stream/ngx_stream_access_module.html);
- Выполнение разных функций в зависимости от
[адреса клиента](docs/http/ngx_http_geo_module.html);
- Ограничение числа одновременных
[соединений](docs/stream/ngx_stream_limit_conn_module.html)
с одного адреса;
- [Настройка
форматов логов](docs/stream/ngx_stream_log_module.xml#log_format),
[буферизованная
запись в лог](docs/stream/ngx_stream_log_module.xml#access_log),
[быстрая ротация логов](docs/control.xml#logs),
[запись в syslog](docs/syslog.html);
- [Геолокация по IP-адресу](docs/stream/ngx_stream_geoip_module.html);
- [A/B-тестирование](docs/stream/ngx_stream_split_clients_module.html);
- сценарный язык [njs](docs/njs/index.html).

## Архитектура и масштабируемость {#architecture_and_scalability}

- Один главный и несколько рабочих процессов, рабочие процессы работают под
непривилегированным пользователем;
- [Гибкость конфигурации](docs/example.html);
- [Изменение настроек](docs/control.xml#reconfiguration)
и [обновление
исполняемого файла](docs/control.xml#upgrade) без перерыва в обслуживании клиентов;
- [Поддержка](docs/events.html)
kqueue (FreeBSD 4.1+),
epoll (Linux 2.6+),
/dev/poll (Solaris 7 11/99+),
event ports (Solaris 10),
select и poll;
- Использование возможностей, предоставляемых kqueue, таких как
 EV_CLEAR, EV_DISABLE (для временного выключения события),
NOTE_LOWAT, EV_EOF, число доступных данных, коды ошибок;
- Использование возможностей, предоставляемых epoll, таких как
EPOLLRDHUP (Linux 2.6.17+, glibc 2.8+) и
EPOLLEXCLUSIVE (Linux 4.5+, glibc 2.24+);
- Поддержка sendfile (FreeBSD 3.1+, Linux 2.2+, macOS 10.5+),
sendfile64 (Linux 2.4.21+) и sendfilev (Solaris 8 7/01+);
- Поддержка
[файлового
AIO](docs/http/ngx_http_core_module.xml#aio) (FreeBSD 4.3+, Linux 2.6.22+);
- Поддержка
[DIRECTIO](docs/http/ngx_http_core_module.xml#directio)
(FreeBSD 4.4+, Linux 2.4+, Solaris 2.6+, macOS);
- [Поддержка](docs/http/ngx_http_core_module.xml#listen)
accept-фильтров (FreeBSD 4.1+, NetBSD 5.0+) и TCP_DEFER_ACCEPT (Linux 2.4+);
- На 10 000 неактивных HTTP keep-alive соединений расходуется
около 2.5M памяти;
- Минимум операций копирования данных.

## Протестированные ОС и платформы {#tested_os_and_platforms}

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
