# Модуль ngx_http_gzip_module

**Revision:** 5  
**Language:** ru

Модуль `ngx_http_gzip_module` — это фильтр, сжимающий ответ методом gzip, что позволяет уменьшить размер передаваемых данных в 2 и более раз.

> **Note:** При использовании протокола SSL/TLS сжатые ответы могут быть подвержены
атакам [BREACH](https://en.wikipedia.org/wiki/BREACH) .

# Пример конфигурации {#example}

```
gzip            on;
gzip_min_length 1000;
gzip_proxied    expired no-cache no-store private auth;
gzip_types      text/plain application/xml;
```

Для записи в лог достигнутого коэффициента сжатия можно использовать переменную `$gzip_ratio` .

# Директивы {#directives}

## gzip

```
Syntax:  on | off
Default: off
Context: if в location, http, server, location
```

Разрешает или запрещает сжатие ответа методом gzip.

## gzip_buffers

```
Syntax:  число размер
Default: 32 4k|16 8k
Context: location, http, server
```

Задаёт `число` и `размер` буферов, в которые будет сжиматься ответ. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

> **Note:** До версии 0.7.28 по умолчанию использовалось 4 буфера размером 4K или 8K.

## gzip_comp_level

```
Syntax:  степень
Default: 1
Context: location, http, server
```

Устанавливает `степень` сжатия ответа методом gzip. Допустимые значения находятся в диапазоне от 1 до 9.

## gzip_disable

```
Syntax:  regex ...
Default: 
Context: location, http, server
```

*This directive appeared in version 0.6.23.*

Запрещает сжатие ответа методом gzip для запросов с полями заголовка `User-Agent` , совпадающими с заданными регулярными выражениями.

Специальная маска “ `msie6` ” (0.7.12) соответствует регулярному выражению “ `MSIE [4-6]\.` ”, но работает быстрее. Начиная с версии 0.8.11 из этой маски исключается “ `MSIE 6.0; ... SV1` ”.

## gzip_http_version

```
Syntax:  1.0 | 1.1
Default: 1.1
Context: location, http, server
```

Устанавливает минимальную HTTP-версию запроса, необходимую для сжатия ответа.

## gzip_min_length

```
Syntax:  длина
Default: 20
Context: location, http, server
```

Устанавливает минимальную длину ответа, который будет сжиматься методом gzip. Длина определяется только из поля `Content-Length` заголовка ответа.

## gzip_proxied

```
Syntax:  off | expired | no-cache | no-store | private | no_last_modified | no_etag | auth | any ...
Default: off
Context: location, http, server
```

Разрешает или запрещает сжатие ответа методом gzip для проксированных запросов в зависимости от запроса и ответа. То, что запрос проксированный, определяется на основании наличия поля `Via` в заголовке запроса. В директиве можно указать одновременно несколько параметров:

**`off`**  
  запрещает сжатие для всех проксированных запросов,
игнорируя остальные параметры;

**`expired`**  
  разрешает сжатие, если в заголовке ответа есть поле `Expires` со значением, запрещающим кэширование;

**`no-cache`**  
  разрешает сжатие, если в заголовке ответа есть поле `Cache-Control` с параметром “ `no-cache` ”;

**`no-store`**  
  разрешает сжатие, если в заголовке ответа есть поле `Cache-Control` с параметром “ `no-store` ”;

**`private`**  
  разрешает сжатие, если в заголовке ответа есть поле `Cache-Control` с параметром “ `private` ”;

**`no_last_modified`**  
  разрешает сжатие, если в заголовке ответа нет поля `Last-Modified` ;

**`no_etag`**  
  разрешает сжатие, если в заголовке ответа нет поля `ETag` ;

**`auth`**  
  разрешает сжатие, если в заголовке запроса есть поле `Authorization` ;

**`any`**  
  разрешает сжатие для всех проксированных запросов.

## gzip_types

```
Syntax:  mime-тип ...
Default: text/html
Context: location, http, server
```

Разрешает сжатие ответа методом gzip для указанных MIME-типов в дополнение к “ `text/html` ”. Специальное значение “ `*` ” соответствует любому MIME-типу (0.8.29). Ответы с типом “ `text/html` ” сжимаются всегда.

## gzip_vary

```
Syntax:  on | off
Default: off
Context: location, http, server
```

Разрешает или запрещает выдавать в ответе поле заголовка `Vary: Accept-Encoding` , если активны директивы [gzip](#gzip) , [gzip_static](ngx_http_gzip_static_module.xml#gzip_static) или [gunzip](ngx_http_gunzip_module.xml#gunzip) .

# Встроенные переменные {#variables}

**`$gzip_ratio`**  
  достигнутый коэффициент сжатия — отношение размера исходного
ответа к размеру сжатого.

