# Модуль ngx_http_grpc_module

**Revision:** 15  
**Language:** ru

Модуль `ngx_http_grpc_module` позволяет передавать запросы gRPC-серверу (1.13.10). Для работы этого модуля необходим модуль [ngx_http_v2_module](ngx_http_v2_module.xml) .

# Пример конфигурации {#example}

```
server {
    listen 9000;

    http2 on;

    location / {
        grpc_pass 127.0.0.1:9000;
    }
}
```

# Директивы {#directives}

## grpc_allow_upstream

```
Syntax:  grpc_allow_upstream строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Задаёт условия, при которых доступ к gRPC-серверу будет разрешён или [запрещён](#denied) . Если все значения строковых параметров непустые и не равны “0”, то доступ разрешён. Условия проверяются каждый раз перед установлением соединения с gRPC-сервером. В значении параметров допустимо использование переменных:

```
geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;
    http2 on;

    location / {
        grpc_pass           localhost:9000;
        grpc_allow_upstream $allow;
        ...
    }
}
```

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## grpc_bind

```
Syntax:  grpc_bind адрес [transparent ] | off;
Default: 
Context: location, http, server
```

Задаёт локальный IP-адрес с необязательным портом, который будет использоваться в исходящих соединениях с gRPC-сервером. В значении параметра допустимо использование переменных. Специальное значение `off` отменяет действие унаследованной с предыдущего уровня конфигурации директивы `grpc_bind` , позволяя системе самостоятельно выбирать локальный IP-адрес и порт.

Параметр `transparent` позволяет задать нелокальный IP-aдрес, который будет использоваться в исходящих соединениях с gRPC-сервером, например, реальный IP-адрес клиента:

```
grpc_bind $remote_addr transparent;
```

Для работы параметра обычно требуется запустить рабочие процессы nginx с привилегиями [суперпользователя](../ngx_core_module.xml#user) . В Linux этого не требуется, так как если указан параметр `transparent` , то рабочие процессы наследуют capability `CAP_NET_RAW` из главного процесса. Также необходимо настроить таблицу маршрутизации ядра для перехвата сетевого трафика с gRPC-сервера.

## grpc_bind_dynamic

```
Syntax:  grpc_bind_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Если включено, операция [bind](#grpc_bind) осуществляется при каждой попытке соединения.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## grpc_buffer_size

```
Syntax:  grpc_buffer_size размер;
Default: 4k|8k
Context: location, http, server
```

Задаёт `размер` буфера, в который будет читаться ответ, получаемый от gRPC-сервера. Ответ синхронно передаётся клиенту сразу же по мере его поступления.

## grpc_connect_timeout

```
Syntax:  grpc_connect_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут для установления соединения с gRPC-сервером. Необходимо иметь в виду, что этот таймаут обычно не может превышать 75 секунд.

## grpc_hide_header

```
Syntax:  grpc_hide_header поле;
Default: 
Context: location, http, server
```

По умолчанию nginx не передаёт клиенту поля заголовка `Date` , `Server` и `X-Accel-...` из ответа gRPC-сервера. Директива `grpc_hide_header` задаёт дополнительные поля, которые не будут передаваться. Если же передачу полей нужно разрешить, можно воспользоваться директивой [grpc_pass_header](#grpc_pass_header) .

## grpc_ignore_headers

```
Syntax:  grpc_ignore_headers поле ...;
Default: 
Context: location, http, server
```

Запрещает обработку некоторых полей заголовка из ответа gRPC-сервера. В директиве можно указать поля `X-Accel-Redirect` и `X-Accel-Charset` .

Если не запрещено, обработка этих полей заголовка заключается в следующем:

- `X-Accel-Redirect` производит [внутреннее
перенаправление](ngx_http_core_module.xml#internal) на указанный URI;
- `X-Accel-Charset` задаёт желаемую [кодировку](ngx_http_charset_module.xml#charset) ответа.

## grpc_intercept_errors

```
Syntax:  grpc_intercept_errors on | off;
Default: off
Context: location, http, server
```

Определяет, передавать ли клиенту ответы gRPC-сервера с кодом больше либо равным 300, или же перехватывать их и перенаправлять на обработку nginx’у с помощью директивы [error_page](ngx_http_core_module.xml#error_page) .

## grpc_next_upstream

```
Syntax:  grpc_next_upstream error | timeout | denied | invalid_header | http_500 | http_502 | http_503 | http_504 | http_403 | http_404 | http_429 | non_idempotent | off ...;
Default: error timeout
Context: location, http, server
```

Определяет, в каких случаях запрос будет передан следующему серверу:

**`error`**  
  произошла ошибка соединения с сервером, передачи ему запроса или
чтения заголовка ответа сервера;

**`timeout`**  
  произошёл таймаут во время соединения с сервером,
передачи ему запроса или чтения заголовка ответа сервера;

**`denied`**  
  сервер [отклонил](#proxy_allow_upstream) соединение (1.29.3);

> **Note:** Параметр доступен как часть [коммерческой подписки](https://nginx.com/products/) .

**`invalid_header`**  
  сервер вернул пустой или неверный ответ;

**`http_500`**  
  сервер вернул ответ с кодом 500;

**`http_502`**  
  сервер вернул ответ с кодом 502;

**`http_503`**  
  сервер вернул ответ с кодом 503;

**`http_504`**  
  сервер вернул ответ с кодом 504;

**`http_403`**  
  сервер вернул ответ с кодом 403;

**`http_404`**  
  сервер вернул ответ с кодом 404;

**`http_429`**  
  сервер вернул ответ с кодом 429;

**`non_idempotent`**  
  обычно запросы с [неидемпотентным](https://datatracker.ietf.org/doc/html/rfc7231#section-4.2.2) методом
( `POST` , `LOCK` , `PATCH` )
не передаются на другой сервер,
если запрос серверу группы уже был отправлен;
включение параметра явно разрешает повторять подобные запросы;

**`off`**  
  запрещает передачу запроса следующему серверу.

Необходимо понимать, что передача запроса следующему серверу возможна только при условии, что клиенту ещё ничего не передавалось. То есть, если ошибка или таймаут возникли в середине передачи ответа, то исправить это уже невозможно.

Директива также определяет, что считается [неудачной попыткой](ngx_http_upstream_module.xml#max_fails) работы с сервером. Случаи `error` , `timeout` , `denied` и `invalid_header` всегда считаются неудачными попытками, даже если они не указаны в директиве. Случаи `http_500` , `http_502` , `http_503` , `http_504` и `http_429` считаются неудачными попытками, только если они указаны в директиве. Случаи `http_403` и `http_404` никогда не считаются неудачными попытками.

Передача запроса следующему серверу может быть ограничена по [количеству попыток](#grpc_next_upstream_tries) и по [времени](#grpc_next_upstream_timeout) .

## grpc_next_upstream_timeout

```
Syntax:  grpc_next_upstream_timeout время;
Default: 0
Context: location, http, server
```

Ограничивает время, в течение которого возможна передача запроса [следующему серверу](#grpc_next_upstream) . Значение `0` отключает это ограничение.

## grpc_next_upstream_tries

```
Syntax:  grpc_next_upstream_tries число;
Default: 0
Context: location, http, server
```

Ограничивает число допустимых попыток для передачи запроса [следующему серверу](#grpc_next_upstream) . Значение `0` отключает это ограничение.

## grpc_pass

```
Syntax:  grpc_pass адрес;
Default: 
Context: if в location, location
```

Задаёт адрес gRPC-сервера. Адрес может быть указан в виде доменного имени или IP-адреса, и порта:

```
grpc_pass localhost:9000;
```

или в виде пути UNIX-сокета:

```
grpc_pass unix:/tmp/grpc.socket;
```

Также может использоваться схема “ `grpc://` ”:

```
grpc_pass grpc://127.0.0.1:9000;
```

Для использования gRPC по SSL необходимо использовать схему “ `grpcs://` ”:

```
grpc_pass grpcs://127.0.0.1:443;
```

Если доменному имени соответствует несколько адресов, то все они будут использоваться по очереди (round-robin). И, кроме того, адрес может быть [группой серверов](ngx_http_upstream_module.xml) .

В значении параметра можно использовать переменные (1.17.8). В этом случае, если адрес указан в виде доменного имени, имя ищется среди описанных [групп серверов](ngx_http_upstream_module.xml) и если не найдено, то определяется с помощью [resolver](ngx_http_core_module.xml#resolver) ’а.

## grpc_pass_header

```
Syntax:  grpc_pass_header поле;
Default: 
Context: location, http, server
```

Разрешает передавать от gRPC-сервера клиенту [запрещённые для передачи](#grpc_hide_header) поля заголовка.

## grpc_read_timeout

```
Syntax:  grpc_read_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при чтении ответа gRPC-сервера. Таймаут устанавливается не на всю передачу ответа, а только между двумя операциями чтения. Если по истечении этого времени gRPC-сервер ничего не передаст, соединение закрывается.

## grpc_request_dynamic

```
Syntax:  grpc_request_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Разрешает или запрещает создание отдельного экземпляра запроса для каждого gRPC-сервера. По умолчанию для всех gRPC-серверов используется единый запрос. Если разрешено, то для каждого сервера создаётся отдельный экземпляр запроса, что позволяет кастомизировать запрос для конкретного сервера. Например каждому серверу можно назначить своё значение поля `Host` в заголовке запроса:

```
grpc_request_dynamic on;
grpc_set_header      Host $upstream_last_server_name;
```

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## grpc_send_timeout

```
Syntax:  grpc_send_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при передаче запроса gRPC-серверу. Таймаут устанавливается не на всю передачу запроса, а только между двумя операциями записи. Если по истечении этого времени gRPC-сервер не примет новых данных, соединение закрывается.

## grpc_set_header

```
Syntax:  grpc_set_header поле значение;
Default: Content-Length $content_length
Context: location, http, server
```

Позволяет переопределять или добавлять поля заголовка запроса, [передаваемые](#proxy_pass_request_headers) gRPC-серверу. В качестве значения можно использовать текст, переменные и их комбинации. Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `grpc_set_header` .

Если значение поля заголовка — пустая строка, то поле вообще не будет передаваться gRPC-серверу:

```
grpc_set_header Accept-Encoding "";
```

## grpc_socket_keepalive

```
Syntax:  grpc_socket_keepalive on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.15.6.*

Конфигурирует поведение “TCP keepalive” для исходящих соединений к gRPC-серверу. По умолчанию для сокета действуют настройки операционной системы. Если указано значение “ `on` ”, то для сокета включается параметр SO_KEEPALIVE .

## grpc_ssl_certificate

```
Syntax:  grpc_ssl_certificate файл;
Default: 
Context: location, http, server
```

Задаёт `файл` с сертификатом в формате PEM для аутентификации на gRPC SSL-сервере.

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## grpc_ssl_certificate_cache

```
Syntax:  grpc_ssl_certificate_cache max=N [inactive=время] [valid=время];
Default: off
Context: location, http, server
```

*This directive appeared in version 1.27.4.*

Задаёт кэш, в котором могут храниться [SSL-сертификаты](#grpc_ssl_certificate) и [секретные ключи](#grpc_ssl_certificate_key) , полученные из [переменных](#grpc_ssl_certificate_key_variables) .

У директивы есть следующие параметры:

**`max`**  
  задаёт максимальное число элементов в кэше;
при переполнении кэша удаляются наименее востребованные элементы (LRU);

**`inactive`**  
  задаёт время, после которого элемент кэша удаляется,
если к нему не было обращений в течение этого времени;
по умолчанию 10 секунд;

**`valid`**  
  задает время, в течение которого
элемент кэша считается действительным
и может быть повторно использован,
по умолчанию 60 секунд.
По завершении этого времени сертификат будет обновлён или повторно проверен;

**`off`**  
  запрещает кэш.

Пример:

```
grpc_ssl_certificate       $grpc_ssl_server_name.crt;
grpc_ssl_certificate_key   $grpc_ssl_server_name.key;
grpc_ssl_certificate_cache max=1000 inactive=20s valid=1m;
```

## grpc_ssl_certificate_key

```
Syntax:  grpc_ssl_certificate_key файл;
Default: 
Context: location, http, server
```

Задаёт `файл` с секретным ключом в формате PEM для аутентификации на gRPC SSL-сервере.

Вместо `файла` можно указать значение `engine` : `имя` : `id` , которое загружает ключ с указанным `id` из OpenSSL engine с заданным `именем` .

Вместо `файла` можно указать значение `store` : `схема` : `id` (1.29.0), которое используется для загрузки ключа с указанным `id` и зарегистрированной провайдером OpenSSL `схемой` URI, такой как [`pkcs11`](https://datatracker.ietf.org/doc/html/rfc7512) .

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## grpc_ssl_ciphers

```
Syntax:  grpc_ssl_ciphers шифры;
Default: DEFAULT
Context: location, http, server
```

Описывает разрешённые шифры для запросов к gRPC SSL-серверу. Шифры задаются в формате, поддерживаемом библиотекой OpenSSL.

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

## grpc_ssl_conf_command

```
Syntax:  grpc_ssl_conf_command имя значение;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.19.4.*

Задаёт произвольные конфигурационные [команды](https://www.openssl.org/docs/man1.1.1/man3/SSL_CONF_cmd.html) OpenSSL при установлении соединения с gRPC SSL-сервером.

> **Note:** Директива поддерживается при использовании OpenSSL 1.0.2 и выше.

На одном уровне может быть указано несколько директив `grpc_ssl_conf_command` . Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `grpc_ssl_conf_command` .

> **Note:** Следует учитывать, что изменение настроек OpenSSL напрямую
может привести к неожиданному поведению.

## grpc_ssl_crl

```
Syntax:  grpc_ssl_crl файл;
Default: 
Context: location, http, server
```

Указывает `файл` с отозванными сертификатами (CRL) в формате PEM, используемыми при [проверке](#proxy_ssl_verify) сертификата gRPC SSL-сервера.

## grpc_ssl_key_log

```
Syntax:  grpc_ssl_key_log путь;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.27.2.*

Включает логирование SSL-ключей соединений с gRPC SSL-сервером и указывает путь к лог-файлу ключей. Ключи записываются в формате [SSLKEYLOGFILE](https://datatracker.ietf.org/doc/html/draft-ietf-tls-keylogfile) совместимом с Wireshark.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## grpc_ssl_name

```
Syntax:  grpc_ssl_name имя;
Default: имя хоста из grpc_pass
Context: location, http, server
```

Позволяет переопределить имя сервера, используемое при [проверке](#grpc_ssl_verify) сертификата gRPC SSL-сервера, а также для [передачи его через SNI](#grpc_ssl_server_name) при установлении соединения с gRPC SSL-сервером.

По умолчанию используется имя хоста из [grpc_pass](#grpc_pass) .

## grpc_ssl_password_file

```
Syntax:  grpc_ssl_password_file файл;
Default: 
Context: location, http, server
```

Задаёт `файл` с паролями от [секретных ключей](#grpc_ssl_certificate_key) , где каждый пароль указан на отдельной строке. Пароли применяются по очереди в момент загрузки ключа.

## grpc_ssl_protocols

```
Syntax:  grpc_ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3];
Default: TLSv1.2 TLSv1.3
Context: location, http, server
```

Разрешает указанные протоколы для запросов к gRPC SSL-серверу.

> **Note:** Параметр `TLSv1.3` используется по умолчанию
начиная с 1.23.4.

## grpc_ssl_server_name

```
Syntax:  grpc_ssl_server_name on | off;
Default: off
Context: location, http, server
```

Разрешает или запрещает передачу имени сервера через [расширение Server Name Indication протокола TLS](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC 6066) при установлении соединения с gRPC SSL-сервером.

## grpc_ssl_session_reuse

```
Syntax:  grpc_ssl_session_reuse on | off;
Default: on
Context: location, http, server
```

Определяет, использовать ли повторно SSL-сессии при работе с gRPC-сервером. Если в логах появляются ошибки “ `digest check failed` ”, то можно попробовать выключить повторное использование сессий.

## grpc_ssl_trusted_certificate

```
Syntax:  grpc_ssl_trusted_certificate файл;
Default: 
Context: location, http, server
```

Задаёт `файл` с доверенными сертификатами CA в формате PEM, используемыми при [проверке](#grpc_ssl_verify) сертификата gRPC SSL-сервера.

## grpc_ssl_verify

```
Syntax:  grpc_ssl_verify on | off;
Default: off
Context: location, http, server
```

Разрешает или запрещает проверку сертификата gRPC SSL-сервера.

## grpc_ssl_verify_depth

```
Syntax:  grpc_ssl_verify_depth число;
Default: 1
Context: location, http, server
```

Устанавливает глубину проверки в цепочке сертификатов gRPC SSL-сервера.

