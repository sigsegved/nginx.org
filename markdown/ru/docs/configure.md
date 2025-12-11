# Сборка nginx из исходных файлов

**Revision:** 25  
**Language:** ru


Сборка настраивается командой `configure`.
Она определяет особенности системы и, в частности, методы, которые nginx
может использовать для обработки соединений.
В конце концов она создаёт `Makefile`.

Команда `configure` поддерживает следующие параметры:

**`--help`**  
  печатает справочное сообщение.

**`--prefix=путь`**  
  задаёт каталог, в котором будут находиться файлы сервера.
Этот же каталог будет использоваться для всех относительных путей,
задаваемых `configure` (кроме путей к исходным текстам
библиотек) и в конфигурационном файле `nginx.conf`.
По умолчанию—каталог `/usr/local/nginx`.
**`--sbin-path=путь`**  
  задаёт имя исполняемого файла nginx.
Это имя используется только на стадии установки.
По умолчанию файл называется
`префикс/sbin/nginx`.
**`--modules-path=путь`**  
  задаёт каталог, в который будут устанавливаться динамические модули.
По умолчанию используется каталог `префикс/modules`.
**`--conf-path=путь`**  
  задаёт имя конфигурационного файла `nginx.conf`.
При желании nginx можно всегда запустить с другим конфигурационным файлом,
указав его в параметре командной строки
-c файл.
По умолчанию файл называется
`префикс/conf/nginx.conf`.
**`--error-log-path=путь`**  
  задаёт имя основного файла ошибок, предупреждений и диагностики.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](ngx_core_module.xml#error_log).
По умолчанию имя
файла—`префикс/logs/error.log`.
**`--pid-path=путь`**  
  задаёт имя файла `nginx.pid`,
в котором будет храниться номер главного процесса.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](ngx_core_module.xml#pid).
По умолчанию имя
файла—`префикс/logs/nginx.pid`.
**`--lock-path=путь`**  
  задаёт префикс имён файлов блокировок.
После установки значение можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](ngx_core_module.xml#lock_file).
По умолчанию используется значение
`префикс/logs/nginx.lock`.

**`--user=имя`**  
  задаёт имя непривилегированного пользователя, с правами которого будут
выполняться рабочие процессы.
После установки это имя можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](ngx_core_module.xml#user).
По умолчанию имя пользователя nobody.
**`--group=имя`**  
  задаёт имя группы, с правами которой будут выполняться рабочие процессы.
После установки это имя можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](ngx_core_module.xml#user).
По умолчанию группа совпадает с именем непривилегированного пользователя.

**`--build=имя`**  
  задаёт необязательное имя сборки nginx.
**`--builddir=путь`**  
  задаёт каталог для сборки.

**`--with-select_module`  

`--without-select_module`**  
  разрешает или запрещает сборку модуля для работы сервера
с помощью метода select.
Этот модуль собирается автоматически, если на платформе не обнаружено
более подходящего метода—kqueue, epoll или /dev/poll.
**`--with-poll_module`  

`--without-poll_module`**  
  разрешает или запрещает сборку модуля для работы сервера
с помощью метода poll.
Этот модуль собирается автоматически, если на платформе не обнаружено
более подходящего метода—kqueue, epoll или /dev/poll.
**`--with-threads`**  
  разрешает использование
[пулов потоков](ngx_core_module.xml#thread_pool).
**`--with-file-aio`**  
  разрешает использование
[файлового асинхронного
ввода-вывода](http/ngx_http_core_module.xml#aio) (AIO) во FreeBSD и Linux.

**`--with-http_ssl_module`**  
  разрешает сборку модуля для работы HTTP-сервера по
[протоколу HTTPS](http/ngx_http_ssl_module.html).
По умолчанию модуль не собирается.
Для сборки и работы этого модуля нужна библиотека OpenSSL.
**`--with-http_v2_module`**  
  разрешает сборку модуля для работы HTTP-сервера по протоколу
[HTTP/2](http/ngx_http_v2_module.html).
По умолчанию модуль не собирается.
**`--with-http_v3_module`**  
  разрешает сборку модуля для работы HTTP-сервера по протоколу
[HTTP/3](http/ngx_http_v3_module.html).
По умолчанию модуль не собирается.
Для сборки и работы этого модуля
нужна библиотека OpenSSL с поддержкой HTTP/3.
**`--with-http_realip_module`**  
  разрешает сборку модуля
[ngx_http_realip_module](http/ngx_http_realip_module.html),
позволяющего менять адрес клиента на переданный в указанном поле заголовка.
По умолчанию модуль не собирается.
**`--with-http_addition_module`**  
  разрешает сборку модуля
[ngx_http_addition_module](http/ngx_http_addition_module.html),
позволяющего добавлять текст до и после ответа.
По умолчанию модуль не собирается.
**`--with-http_xslt_module`  

`--with-http_xslt_module=dynamic`**  
  разрешает сборку модуля
[ngx_http_xslt_module](http/ngx_http_xslt_module.html),
позволяющего преобразовывать XML-ответ с помощью XSLT-шаблонов.
По умолчанию модуль не собирается.
Для сборки и работы этого модуля нужны библиотеки
[libxml2](http://xmlsoft.org) и
[libxslt](http://xmlsoft.org/XSLT/).
**`--with-http_image_filter_module`  

`--with-http_image_filter_module=dynamic`**  
  разрешает сборку модуля
[ngx_http_image_filter_module](http/ngx_http_image_filter_module.html),
позволяющего преобразовывать изображения в форматах JPEG, GIF, PNG и WebP.
По умолчанию модуль не собирается.
**`--with-http_geoip_module`  

`--with-http_geoip_module=dynamic`**  
  разрешает сборку модуля
[ngx_http_geoip_module](http/ngx_http_geoip_module.html),
создающего переменные, значения которых зависят от IP-адреса клиента,
используя готовые базы данных
[MaxMind](http://www.maxmind.com).
По умолчанию модуль не собирается.
**`--with-http_sub_module`**  
  разрешает сборку модуля
[ngx_http_sub_module](http/ngx_http_sub_module.html),
позволяющего изменять в ответе одну заданную строку на другую.
По умолчанию модуль не собирается.
**`--with-http_dav_module`**  
  разрешает сборку модуля
[ngx_http_dav_module](http/ngx_http_dav_module.html),
предназначенного для автоматизации задач управления файлами на сервере
по протоколу WebDAV.
По умолчанию модуль не собирается.
**`--with-http_flv_module`**  
  разрешает сборку модуля
[ngx_http_flv_module](http/ngx_http_flv_module.html),
обеспечивающего серверную поддержку псевдо-стриминга
для файлов Flash Video (FLV).
По умолчанию модуль не собирается.
**`--with-http_mp4_module`**  
  разрешает сборку модуля
[ngx_http_mp4_module](http/ngx_http_mp4_module.html),
обеспечивающего серверную поддержку псевдо-стриминга
для файлов в формате MP4.
По умолчанию модуль не собирается.
**`--with-http_gunzip_module`**  
  разрешает сборку модуля
[ngx_http_gunzip_module](http/ngx_http_gunzip_module.html),
позволяющего распаковывать ответы с “`Content-Encoding: gzip`”
для тех клиентов, которые не поддерживают метод сжатия “gzip”.
По умолчанию модуль не собирается.
**`--with-http_gzip_static_module`**  
  разрешает сборку модуля
[ngx_http_gzip_static_module](http/ngx_http_gzip_static_module.html),
позволяющего отдавать вместо обычного файла предварительно сжатый файл
с таким же именем и с расширением “`.gz`”.
По умолчанию модуль не собирается.
**`--with-http_auth_request_module`**  
  разрешает сборку модуля
[ngx_http_auth_request_module](http/ngx_http_auth_request_module.html),
предоставляющего возможность авторизации клиента,
основанной на результате подзапроса.
По умолчанию модуль не собирается.
**`--with-http_random_index_module`**  
  разрешает сборку модуля
[ngx_http_random_index_module](http/ngx_http_random_index_module.html),
обслуживающего запросы, оканчивающиеся слэшом (‘`/`’),
и выдающего случайный файл в качестве индексного файла каталога.
По умолчанию модуль не собирается.
**`--with-http_secure_link_module`**  
  разрешает сборку модуля
[ngx_http_secure_link_module](http/ngx_http_secure_link_module.html).
По умолчанию модуль не собирается.
**`--with-http_degradation_module`**  
  разрешает сборку модуля
`ngx_http_degradation_module`.
По умолчанию модуль не собирается.
**`--with-http_slice_module`**  
  разрешает сборку модуля
[ngx_http_slice_module](http/ngx_http_slice_module.html),
позволяющего разбить запрос на подзапросы,
каждый из которых возвращает определённый диапазон ответа.
Модуль обеспечивает более эффективное кэширование больших ответов.
По умолчанию модуль не собирается.
**`--with-http_stub_status_module`**  
  разрешает сборку модуля
[ngx_http_stub_status_module](http/ngx_http_stub_status_module.html),
предоставляющего доступ к базовой информации о состоянии сервера.
По умолчанию модуль не собирается.

**`--without-http_charset_module`**  
  запрещает сборку модуля
[ngx_http_charset_module](http/ngx_http_charset_module.html),
позволяющего добавлять указанную кодировку в
поле **Content-Type** заголовка ответа
и перекодировать данные из одной кодировки в другую.
**`--without-http_gzip_module`**  
  запрещает сборку модуля
[сжатия ответов](http/ngx_http_gzip_module.html) HTTP-сервера.
Для сборки и работы этого модуля нужна библиотека zlib.
**`--without-http_ssi_module`**  
  запрещает сборку модуля
[ngx_http_ssi_module](http/ngx_http_ssi_module.html),
обрабатывающего команды SSI (Server Side Includes)
в проходящих через него ответах.
**`--without-http_userid_module`**  
  запрещает сборку модуля
[ngx_http_userid_module](http/ngx_http_userid_module.html),
выдающего куки для идентификации клиентов.
**`--without-http_access_module`**  
  запрещает сборку модуля
[ngx_http_access_module](http/ngx_http_access_module.html),
позволяющего ограничить доступ для определённых адресов клиентов.
**`--without-http_auth_basic_module`**  
  запрещает сборку модуля
[ngx_http_auth_basic_module](http/ngx_http_auth_basic_module.html),
позволяющего ограничить доступ к ресурсам с проверкой имени
и пароля пользователя по протоколу “HTTP Basic Authentication”.
**`--without-http_mirror_module`**  
  запрещает сборку модуля
[ngx_http_mirror_module](http/ngx_http_mirror_module.html),
позволяющего зеркалировать исходный запрос при помощи создания фоновых
зеркалирующих подзапросов.
**`--without-http_autoindex_module`**  
  запрещает сборку модуля
[ngx_http_autoindex_module](http/ngx_http_autoindex_module.html),
обслуживающего запросы, оканчивающиеся слэшом (‘`/`’),
и выдающего листинг каталога, когда модуль
[ngx_http_index_module](http/ngx_http_index_module.html)
не нашёл индексный файл.
**`--without-http_geo_module`**  
  запрещает сборку модуля
[ngx_http_geo_module](http/ngx_http_geo_module.html),
позволяющего создавать переменные,
значения которых зависят от IP-адреса клиента.
**`--without-http_map_module`**  
  запрещает сборку модуля
[ngx_http_map_module](http/ngx_http_map_module.html),
позволяющего создавать переменные,
значения которых зависят от значений других переменных.
**`--without-http_split_clients_module`**  
  запрещает сборку модуля
[ngx_http_split_clients_module](http/ngx_http_split_clients_module.html),
позволяющего создавать переменные для A/B тестирования.
**`--without-http_referer_module`**  
  запрещает сборку модуля
[ngx_http_referer_module](http/ngx_http_referer_module.html),
позволяющего блокировать доступ к сайту для запросов с неверными значениями
поля **Referer** в заголовке.
**`--without-http_rewrite_module`**  
  запрещает сборку модуля HTTP-сервера, позволяющего
[делать
перенаправления и менять URI запросов](http/ngx_http_rewrite_module.html).
Для сборки и работы этого модуля нужна библиотека PCRE.
**`--without-http_proxy_module`**  
  запрещает сборку
[проксирующего модуля](http/ngx_http_proxy_module.html)
HTTP-сервера.
**`--without-http_fastcgi_module`**  
  запрещает сборку модуля
[ngx_http_fastcgi_module](http/ngx_http_fastcgi_module.html),
позволяющего передавать запросы FastCGI-серверу.
**`--without-http_uwsgi_module`**  
  запрещает сборку модуля
[ngx_http_uwsgi_module](http/ngx_http_uwsgi_module.html),
позволяющего передавать запросы uwsgi-серверу.
**`--without-http_scgi_module`**  
  запрещает сборку модуля
[ngx_http_scgi_module](http/ngx_http_scgi_module.html),
позволяющего передавать запросы SCGI-серверу.
**`--without-http_grpc_module`**  
  запрещает сборку модуля
[ngx_http_grpc_module](http/ngx_http_grpc_module.html),
позволяющего передавать запросы gRPC-серверу.
**`--without-http_memcached_module`**  
  запрещает сборку модуля
[ngx_http_memcached_module](http/ngx_http_memcached_module.html),
позволяющего получать ответы из сервера memcached.
**`--without-http_limit_conn_module`**  
  запрещает сборку модуля
[ngx_http_limit_conn_module](http/ngx_http_limit_conn_module.html),
позволяющего ограничить число соединений по заданному ключу,
в частности, число соединений с одного IP-адреса.
**`--without-http_limit_req_module`**  
  запрещает сборку модуля
[ngx_http_limit_req_module](http/ngx_http_limit_req_module.html),
позволяющего ограничить скорость обработки запросов по заданному ключу или,
как частный случай, скорость обработки запросов, поступающих с одного IP-адреса.
**`--without-http_empty_gif_module`**  
  запрещает сборку модуля,
[выдающего однопиксельный
прозрачный GIF](http/ngx_http_empty_gif_module.html).
**`--without-http_browser_module`**  
  запрещает сборку модуля
[ngx_http_browser_module](http/ngx_http_browser_module.html),
создающего переменные, значения которых зависят от значения
поля **User-Agent** в заголовке запроса.
**`--without-http_upstream_hash_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](http/ngx_http_upstream_module.xml#hash).
**`--without-http_upstream_ip_hash_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](http/ngx_http_upstream_module.xml#ip_hash).
**`--without-http_upstream_least_conn_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](http/ngx_http_upstream_module.xml#least_conn).
**`--without-http_upstream_random_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](http/ngx_http_upstream_module.xml#random).
**`--without-http_upstream_keepalive_module`**  
  запрещает сборку модуля, реализующего
[кэширование
соединений](http/ngx_http_upstream_module.xml#keepalive) к вышестоящим серверам.
**`--without-http_upstream_zone_module`**  
  запрещает сборку модуля, позволяющего сохранять рабочее состояние группы
вышестоящих серверов в
[разделяемой
памяти](http/ngx_http_upstream_module.xml#zone).

**`--with-http_perl_module`  

`--with-http_perl_module=dynamic`**  
  разрешает сборку модуля, добавляющего
[встроенный Perl](http/ngx_http_perl_module.html).
По умолчанию модуль не собирается.
**`--with-perl_modules_path=путь`**  
  задаёт каталог, в котором будут находиться файлы модулей Perl.
**`--with-perl=путь`**  
  задаёт имя исполняемого файла Perl.

**`--http-log-path=путь`**  
  задаёт имя основного файла регистрации запросов HTTP-сервера.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_log_module.xml#access_log).
По умолчанию имя
файла—`префикс/logs/access.log`.
**`--http-client-body-temp-path=путь`**  
  задаёт каталог для хранения временных файлов
с телами запросов клиентов.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_core_module.xml#client_body_temp_path).
По умолчанию используется каталог
`префикс/client_body_temp`.
**`--http-proxy-temp-path=путь`**  
  задаёт каталог для хранения временных файлов
с данными, полученными от проксируемых серверов.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_proxy_module.xml#proxy_temp_path).
По умолчанию используется каталог
`префикс/proxy_temp`.
**`--http-fastcgi-temp-path=путь`**  
  задаёт каталог для хранения временных файлов
с данными, полученными от FastCGI-серверов.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_fastcgi_module.xml#fastcgi_temp_path).
По умолчанию используется каталог
`префикс/fastcgi_temp`.
**`--http-uwsgi-temp-path=путь`**  
  задаёт каталог для хранения временных файлов
с данными, полученными от uwsgi-серверов.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_uwsgi_module.xml#uwsgi_temp_path).
По умолчанию используется каталог
`префикс/uwsgi_temp`.
**`--http-scgi-temp-path=путь`**  
  задаёт каталог для хранения временных файлов
с данными, полученными от SCGI-серверов.
После установки имя файла можно всегда поменять в конфигурационном
файле `nginx.conf` с помощью директивы
[](http/ngx_http_scgi_module.xml#scgi_temp_path).
По умолчанию используется каталог
`префикс/scgi_temp`.

**`--without-http`**  
  запрещает [HTTP-сервер](http/ngx_http_core_module.html).
**`--without-http-cache`**  
  запрещает HTTP-кэш.

**`--with-mail`  

`--with-mail=dynamic`**  
  разрешает POP3/IMAP4/SMTP
[почтовый прокси-сервер](mail/ngx_mail_core_module.html).
**`--with-mail_ssl_module`**  
  разрешает сборку модуля для работы почтового прокси-сервера по
[протоколу SSL/TLS](mail/ngx_mail_ssl_module.html).
По умолчанию модуль не собирается.
Для сборки и работы этого модуля нужна библиотека OpenSSL.
**`--without-mail_pop3_module`**  
  запрещает протокол [POP3](mail/ngx_mail_pop3_module.html)
в почтовом прокси-сервере.
**`--without-mail_imap_module`**  
  запрещает протокол [IMAP](mail/ngx_mail_imap_module.html)
в почтовом прокси-сервере.
**`--without-mail_smtp_module`**  
  запрещает протокол [SMTP](mail/ngx_mail_smtp_module.html)
в почтовом прокси-сервере.

**`--with-stream`  

`--with-stream=dynamic`**  
  разрешает сборку
[модуля stream](stream/ngx_stream_core_module.html)
для TCP/UDP-проксирования и балансировки.
По умолчанию модуль не собирается.
**`--with-stream_ssl_module`**  
  разрешает сборку модуля для работы модуля stream по
[протоколу SSL/TLS](stream/ngx_stream_ssl_module.html).
По умолчанию модуль не собирается.
Для сборки и работы этого модуля нужна библиотека OpenSSL.
**`--with-stream_realip_module`**  
  разрешает сборку модуля
[ngx_stream_realip_module](stream/ngx_stream_realip_module.html),
позволяющего менять адрес клиента на переданный в заголовке протокола PROXY.
По умолчанию модуль не собирается.
**`--with-stream_geoip_module`  

`--with-stream_geoip_module=dynamic`**  
  разрешает сборку модуля
[ngx_stream_geoip_module](stream/ngx_stream_geoip_module.html),
создающего переменные, значения которых зависят от IP-адреса клиента,
используя готовые базы данных
[MaxMind](http://www.maxmind.com).
По умолчанию модуль не собирается.
**`--with-stream_ssl_preread_module`**  
  разрешает сборку модуля
[ngx_stream_ssl_preread_module](stream/ngx_stream_ssl_preread_module.html),
позволяющего извлекать информацию из сообщения
[ClientHello](https://datatracker.ietf.org/doc/html/rfc5246#section-7.4.1.2)
без терминирования SSL/TLS.
По умолчанию модуль не собирается.
**`--without-stream_limit_conn_module`**  
  запрещает сборку модуля
[ngx_stream_limit_conn_module](stream/ngx_stream_limit_conn_module.html),
позволяющего ограничить число соединений по заданному ключу,
в частности, число соединений с одного IP-адреса.
**`--without-stream_access_module`**  
  запрещает сборку модуля
[ngx_stream_access_module](stream/ngx_stream_access_module.html),
позволяющего ограничить доступ для определённых адресов клиентов.
**`--without-stream_geo_module`**  
  запрещает сборку модуля
[ngx_stream_geo_module](stream/ngx_stream_geo_module.html),
позволяющего создавать переменные,
значения которых зависят от IP-адреса клиента.
**`--without-stream_map_module`**  
  запрещает сборку модуля
[ngx_stream_map_module](stream/ngx_stream_map_module.html),
позволяющего создавать переменные,
значения которых зависят от значений других переменных.
**`--without-stream_split_clients_module`**  
  запрещает сборку модуля
[ngx_stream_split_clients_module](stream/ngx_stream_split_clients_module.html),
позволяющего создавать переменные для A/B тестирования.
**`--without-stream_return_module`**  
  запрещает сборку модуля
[ngx_stream_return_module](stream/ngx_stream_return_module.html),
позволяющего отправить заданное значение клиенту
и после этого закрыть соединение.
**`--without-stream_set_module`**  
  запрещает сборку модуля
[ngx_stream_set_module](stream/ngx_stream_set_module.html),
позволяющего устанавливать значение переменной.
**`--without-stream_upstream_hash_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](stream/ngx_stream_upstream_module.xml#hash).
**`--without-stream_upstream_least_conn_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](stream/ngx_stream_upstream_module.xml#least_conn).
**`--without-stream_upstream_random_module`**  
  запрещает сборку модуля, реализующего метод балансировки нагрузки
[](stream/ngx_stream_upstream_module.xml#random).
**`--without-stream_upstream_zone_module`**  
  запрещает сборку модуля, позволяющего сохранять рабочее состояние группы
вышестоящих серверов в
[разделяемой
памяти](stream/ngx_stream_upstream_module.xml#zone).

**`--with-google_perftools_module`**  
  разрешает сборку модуля
[ngx_google_perftools_module](ngx_google_perftools_module.html),
обеспечивающего поддержку профилирования рабочих процессов nginx при помощи
[Google Performance Tools](https://github.com/gperftools/gperftools).
Модуль предназначен для разработчиков nginx и не собирается по умолчанию.
**`--with-cpp_test_module`**  
  разрешает сборку модуля
`ngx_cpp_test_module`.

**`--add-module=путь`**  
  разрешает сборку внешнего модуля.
**`--add-dynamic-module=путь`**  
  разрешает сборку внешнего динамического модуля.

**`--with-compat`**  
  включает режим совместимости с динамическими модулями.

**`--with-cc=путь`**  
  задаёт компилятор, который будет использоваться при сборке.
**`--with-cpp=путь`**  
  задаёт препроцессор, который будет использоваться при сборке.
**`--with-cc-opt=параметры`**  
  задаёт дополнительные параметры, которые будут добавлены к переменной CFLAGS.
При использовании системной библиотеки PCRE во FreeBSD, нужно указать
`--with-cc-opt="-I /usr/local/include"`.
Если нужно увеличить число файлов, с которыми может работать
select, то это тоже можно задать здесь же:
`--with-cc-opt="-D FD_SETSIZE=2048"`.
**`--with-ld-opt=параметры`**  
  задаёт дополнительные параметры, которые будут использованы при линковке.
При использовании системной библиотеки PCRE во FreeBSD, нужно указать
`--with-ld-opt="-L /usr/local/lib"`.
**`--with-cpu-opt=cpu`**  
  разрешает сборку для одного из следующих процессоров:
`pentium`, `pentiumpro`,
`pentium3`, `pentium4`,
`athlon`, `opteron`,
`sparc32`, `sparc64`,
`ppc64`.

**`--without-pcre`**  
  запрещает использование библиотеки PCRE.
**`--with-pcre`**  
  разрешает использование библиотеки PCRE.
**`--with-pcre=путь`**  
  задаёт путь к исходным текстам библиотеки PCRE.
Дистрибутив библиотеки
нужно взять на сайте [PCRE](http://www.pcre.org)
и распаковать.
Всё остальное сделают `./configure` nginx’а и
`make`.
Библиотека нужна для использования регулярных выражений в директиве
[](http/ngx_http_core_module.xml#location)
и для модуля
[ngx_http_rewrite_module](http/ngx_http_rewrite_module.html).
**`--with-pcre-opt=параметры`**  
  задаёт дополнительные параметры сборки PCRE.
**`--with-pcre-jit`**  
  собирает библиотеку PCRE с
поддержкой JIT-компиляции (1.1.12, директива
[](ngx_core_module.xml#pcre_jit)).
**`--without-pcre2`**  
  запрещает использование библиотеки PCRE2
вместо исходной библиотеки PCRE (1.21.5).

**`--with-zlib=путь`**  
  задаёт путь к исходным текстам библиотеки zlib.
Дистрибутив библиотеки нужно взять на сайте
[zlib](http://zlib.net) и распаковать.
Всё остальное сделают `./configure` nginx’а и
`make`.
Библиотека нужна для модуля
[ngx_http_gzip_module](http/ngx_http_gzip_module.html).
**`--with-zlib-opt=параметры`**  
  задаёт дополнительные параметры сборки zlib.
**`--with-zlib-asm=cpu`**  
  разрешает использование при сборке библиотеки zlib ассемблерных вставок,
оптимизированных для одного из следующих процессоров:
`pentium`, `pentiumpro`.

**`--with-libatomic`**  
  разрешает сборку с библиотекой libatomic_ops.
**`--with-libatomic=путь`**  
  задаёт путь к исходным текстам библиотеки libatomic_ops.

**`--with-openssl=путь`**  
  задаёт путь к исходным текстам библиотеки OpenSSL.
**`--with-openssl-opt=параметры`**  
  задаёт дополнительные параметры сборки OpenSSL.

**`--with-debug`**  
  разрешает [отладочный лог](debugging_log.html).

Пример использования параметров (всё это нужно набрать в одной строке):

```
./configure
    --sbin-path=/usr/local/nginx/nginx
    --conf-path=/usr/local/nginx/nginx.conf
    --pid-path=/usr/local/nginx/nginx.pid
    --with-http_ssl_module
    --with-pcre=../pcre2-10.39
    --with-zlib=../zlib-1.3
```

После конфигурации
nginx компилируется и устанавливается с помощью `make`.
