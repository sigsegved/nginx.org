# Модуль ngx_http_charset_module

**Revision:** 5  
**Language:** ru

Модуль `ngx_http_charset_module` добавляет указанную кодировку в поле `Content-Type` заголовка ответа. Кроме того, модуль может перекодировать данные из одной кодировки в другую с некоторыми ограничениями:

- перекодирование осуществляется только в одну сторону — от сервера к клиенту,
- перекодироваться могут только однобайтные кодировки
- или однобайтные кодировки в UTF-8 и обратно.

# Пример конфигурации {#example}

```
include        conf/koi-win;

charset        windows-1251;
source_charset koi8-r;
```

# Директивы {#directives}

## charset

```
Syntax:  кодировка | off
Default: off
Context: if в location, http, server, location
```

Добавляет указанную кодировку в поле `Content-Type` заголовка ответа. Если эта кодировка отличается от указанной в директиве [source_charset](#source_charset) , то выполняется перекодирование.

Параметр `off` отменяет добавление кодировки в поле `Content-Type` заголовка ответа.

Кодировка может быть задана с помощью переменной:

```
charset $charset;
```

В этом случае необходимо, чтобы все возможные значения переменной присутствовали хотя бы один раз в любом месте конфигурации в виде директив [charset_map](#charset_map) , [charset](#charset) или [source_charset](#source_charset) . Для кодировок `utf-8` , `windows-1251` и `koi8-r` для этого достаточно включить в конфигурацию файлы `conf/koi-win` , `conf/koi-utf` и `conf/win-utf` . Для других кодировок можно просто сделать фиктивную таблицу перекодировки, например:

```
charset_map iso-8859-5 _ { }
```

Кроме того, кодировка может быть задана в поле `X-Accel-Charset` заголовка ответа. Эту возможность можно запретить с помощью директив [proxy_ignore_headers](ngx_http_proxy_module.xml#proxy_ignore_headers) , [fastcgi_ignore_headers](ngx_http_fastcgi_module.xml#fastcgi_ignore_headers) , [uwsgi_ignore_headers](ngx_http_uwsgi_module.xml#uwsgi_ignore_headers) , [scgi_ignore_headers](ngx_http_scgi_module.xml#scgi_ignore_headers) и [grpc_ignore_headers](ngx_http_grpc_module.xml#grpc_ignore_headers) .

## charset_map

```
Syntax:  кодировка1 кодировка2
Default: 
Context: http
```

Описывает таблицу перекодирования из одной кодировки в другую. Таблица для обратного перекодирования строится на основании тех же данных. Коды символов задаются в шестнадцатеричном виде. Неописанные символы в пределах 80-FF заменяются на “ `?` ”. При перекодировании из UTF-8 символы, отсутствующие в однобайтной кодировке, заменяются на “ `&#XXXX;` ”.

Пример:

```
charset_map koi8-r windows-1251 {
    C0 FE ; # small yu
    C1 E0 ; # small a
    C2 E1 ; # small b
    C3 F6 ; # small ts
    ...
}
```

При описании таблицы перекодирования в UTF-8, коды кодировки UTF-8 должны быть указаны во второй колонке, например:

```
charset_map koi8-r utf-8 {
    C0 D18E ; # small yu
    C1 D0B0 ; # small a
    C2 D0B1 ; # small b
    C3 D186 ; # small ts
    ...
}
```

Полные таблицы преобразования из `koi8-r` в `windows-1251` и из `koi8-r` и `windows-1251` в `utf-8` входят в дистрибутив и находятся в файлах `conf/koi-win` , `conf/koi-utf` и `conf/win-utf` .

## charset_types

```
Syntax:  mime-тип ...
Default: text/html text/xml text/plain text/vnd.wap.wml
application/javascript application/rss+xml
Context: location, http, server
```

*This directive appeared in version 0.7.9.*

Разрешает работу модуля в ответах с указанными MIME-типами в дополнение к “ `text/html` ”. Специальное значение “ `*` ” соответствует любому MIME-типу (0.8.29).

> **Note:** До версии 1.5.4 по умолчанию вместо MIME-типа
“ `application/javascript` ” использовался
“ `application/x-javascript` ”.

## override_charset

```
Syntax:  on | off
Default: off
Context: if в location, http, server, location
```

Определяет, выполнять ли перекодирование для ответов, полученных от проксированного сервера или от FastCGI/uwsgi/SCGI/gRPC-сервера, если в ответах уже указана кодировка в поле `Content-Type` заголовка ответа. Если перекодирование разрешено, то в качестве исходной кодировки используется кодировка, указанная в полученном ответе.

> **Note:** Необходимо отметить, что если ответ был получен в подзапросе,
то, независимо от значения директивы `override_charset` ,
всегда выполняется перекодирование из кодировки ответа в кодировку
основного запроса.

## source_charset

```
Syntax:  кодировка
Default: 
Context: if в location, http, server, location
```

Задаёт исходную кодировку ответа. Если эта кодировка отличается от указанной в директиве [charset](#charset) , то выполняется перекодирование.

