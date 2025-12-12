# Модуль ngx_http_v2_module

**Revision:** 19  
**Language:** ru

Модуль `ngx_http_v2_module` (1.9.5) обеспечивает поддержку [HTTP/2](https://datatracker.ietf.org/doc/html/rfc7540) .

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_v2_module` .

# Известные проблемы {#issues}

До версии 1.9.14 буферизация тела запроса клиента не могла быть запрещена независимо от значения директив [proxy_request_buffering](ngx_http_proxy_module.xml#proxy_request_buffering) , [fastcgi_request_buffering](ngx_http_fastcgi_module.xml#fastcgi_request_buffering) , [uwsgi_request_buffering](ngx_http_uwsgi_module.xml#uwsgi_request_buffering) и [scgi_request_buffering](ngx_http_scgi_module.xml#scgi_request_buffering) .

До версии 1.19.1 механизм [lingering_close](ngx_http_core_module.xml#lingering_close) не использовался в управлении закрытием HTTP/2-соединений.

# Пример конфигурации {#example}

```
server {
    listen 443 ssl;

    http2 on;

    ssl_certificate server.crt;
    ssl_certificate_key server.key;
}
```

Чтобы принимать HTTP/2-соединения по TLS, необходимо наличие поддержки расширения “Application-Layer Protocol Negotiation” (ALPN) протокола TLS, появившейся в [OpenSSL](http://www.openssl.org) версии 1.0.2.

Если директива [ssl_prefer_server_ciphers](ngx_http_ssl_module.xml#ssl_prefer_server_ciphers) установлена в значение “ `on` ”, [шифры](ngx_http_ssl_module.xml#ssl_ciphers) должны быть настроены таким образом, чтобы соответствовать чёрному списку [RFC 9113, Appendix A](https://datatracker.ietf.org/doc/html/rfc9113#appendix-A) , а также поддерживаться клиентами.

# Директивы {#directives}

## http2

```
Syntax:  on | off
Default: off
Context: server, http
```

*This directive appeared in version 1.25.1.*

Разрешает протокол [HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113) .

## http2_body_preread_size

```
Syntax:  размер
Default: 64k
Context: server, http
```

*This directive appeared in version 1.11.0.*

Задаёт `размер` буфера для каждого запроса, в который может сохраняться тело запроса до того, как оно начнёт обрабатываться.

## http2_chunk_size

```
Syntax:  размер
Default: 8k
Context: location, http, server
```

Задаёт максимальный размер частей, на которое будет разделяться тело ответа. Слишком маленькое значение может привести к росту накладных расходов. Слишком большое значение может негативно сказаться на приоритизации из-за [блокировки очереди](http://en.wikipedia.org/wiki/Head-of-line_blocking) .

## http2_idle_timeout

```
Syntax:  время
Default: 3m
Context: server, http
```

> **Note:** Эта директива устарела начиная с версии 1.19.7.
Вместо неё следует использовать директиву [keepalive_timeout](ngx_http_core_module.xml#keepalive_timeout) .

Задаёт таймаут неактивности, после которого соединение закрывается.

## http2_max_concurrent_pushes

```
Syntax:  число
Default: 10
Context: server, http
```

*This directive appeared in version 1.13.9.*

> **Note:** Эта директива устарела начиная с версии 1.25.1.

Ограничивает максимальное число параллельных [push](#http2_push) -запросов в соединении.

## http2_max_concurrent_streams

```
Syntax:  число
Default: 128
Context: server, http
```

Задаёт максимальное число параллельных HTTP/2-потоков в соединении.

## http2_max_field_size

```
Syntax:  размер
Default: 4k
Context: server, http
```

> **Note:** Эта директива устарела начиная с версии 1.19.7.
Вместо неё следует использовать директиву [large_client_header_buffers](ngx_http_core_module.xml#large_client_header_buffers) .

Ограничивает максимальный размер заголовка запроса, сжатого при помощи [HPACK](https://datatracker.ietf.org/doc/html/rfc7541) . Ограничение применяется в равной степени как к имени, так и к значению. Если применяется кодирование Хаффмана, то фактический размер распакованных строк имени и значения может быть больше. Ограничение по умолчанию подходит для большинства запросов.

## http2_max_header_size

```
Syntax:  размер
Default: 16k
Context: server, http
```

> **Note:** Эта директива устарела начиная с версии 1.19.7.
Вместо неё следует использовать директиву [large_client_header_buffers](ngx_http_core_module.xml#large_client_header_buffers) .

Ограничивает максимальный размер всего списка заголовков запроса после распаковки [HPACK](https://datatracker.ietf.org/doc/html/rfc7541) . Ограничение по умолчанию подходит для большинства запросов.

## http2_max_requests

```
Syntax:  число
Default: 1000
Context: server, http
```

*This directive appeared in version 1.11.6.*

> **Note:** Эта директива устарела начиная с версии 1.19.7.
Вместо неё следует использовать директиву [keepalive_requests](ngx_http_core_module.xml#keepalive_requests) .

Задаёт максимальное число запросов (включая [push](#http2_push) -запросы), которые можно сделать по одному соединению HTTP/2, после чего очередной клиентский запрос приведёт к закрытию соединения и необходимости установить новое соединение.

Периодическое закрытие соединений необходимо для освобождения памяти, выделенной под конкретные соединения. Поэтому использование слишком большого максимального числа запросов может приводить к чрезмерному потреблению памяти и не рекомендуется.

## http2_push

```
Syntax:  uri | off
Default: off
Context: location, http, server
```

*This directive appeared in version 1.13.9.*

> **Note:** Эта директива устарела начиная с версии 1.25.1.
Вместо неё можно использовать директиву [early_hints](ngx_http_core_module.xml#early_hints) .

Заблаговременно отправляет ( [push](https://datatracker.ietf.org/doc/html/rfc9113#section-8.4) ) запрос к заданному `uri` вместе с ответом на оригинальный запрос. Будут обработаны только относительные URI с абсолютными путями, например:

```
http2_push /static/css/main.css;
```

В значении `uri` допустимо использование переменных.

На одном уровне конфигурации можно указать несколько `http2_push` директив. Параметр `off` отменяет действие унаследованных с предыдущего уровня конфигурации директив `http2_push` .

## http2_push_preload

```
Syntax:  on | off
Default: off
Context: location, http, server
```

*This directive appeared in version 1.13.9.*

> **Note:** Эта директива устарела начиная с версии 1.25.1.

Разрешает автоматическое преобразование [preload links](https://www.w3.org/TR/preload/#server-push-http-2) , указанных в полях `Link` заголовка ответа, в [push](https://datatracker.ietf.org/doc/html/rfc9113#section-8.4) -запросы.

## http2_recv_buffer_size

```
Syntax:  размер
Default: 256k
Context: http
```

Задаёт размер входного буфера для [рабочего процесса](../ngx_core_module.xml#worker_processes) .

## http2_recv_timeout

```
Syntax:  время
Default: 30s
Context: server, http
```

> **Note:** Эта директива устарела начиная с версии 1.19.7.
Вместо неё следует использовать директиву [client_header_timeout](ngx_http_core_module.xml#client_header_timeout) .

Задаёт таймаут в случае, когда от клиента ожидаются ещё данные, после которого соединение закрывается.

# Встроенные переменные {#variables}

Модуль `ngx_http_v2_module` поддерживает следующие встроенные переменные:

**`$http2`**  
  согласованный идентификатор протокола:
“ `h2` ” для HTTP/2 через TLS,
“ `h2c` ” для HTTP/2 через незашифрованный TCP,
либо пустая строка.

