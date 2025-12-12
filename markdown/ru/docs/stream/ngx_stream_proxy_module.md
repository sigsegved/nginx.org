# Модуль ngx_stream_proxy_module

**Revision:** 37  
**Language:** ru

Модуль `ngx_stream_proxy_module` (1.9.0) позволяет проксировать потоки данных по TCP, UDP (1.9.13) и UNIX-сокетам.

# Пример конфигурации {#example}

```
server {
    listen 127.0.0.1:12345;
    proxy_pass 127.0.0.1:8080;
}

server {
    listen 12345;
    proxy_connect_timeout 1s;
    proxy_timeout 1m;
    proxy_pass example.com:12345;
}

server {
    listen 53 udp reuseport;
    proxy_timeout 20s;
    proxy_pass dns.example.com:53;
}

server {
    listen [::1]:12345;
    proxy_pass unix:/tmp/stream.socket;
}
```

# Директивы {#directives}

## proxy_bind

```
Syntax:  address [transparent] | off
Default: 
Context: server, stream
```

*This directive appeared in version 1.9.2.*

Задаёт локальный IP- `адрес` , который будет использоваться в исходящих соединениях с проксируемым сервером. В значении параметра допустимо использование переменных (1.11.2). Специальное значение `off` отменяет действие унаследованной с предыдущего уровня конфигурации директивы `proxy_bind` , позволяя системе самостоятельно выбирать локальный IP-адрес.

Параметр `transparent` (1.11.0) позволяет задать нелокальный IP-aдрес, который будет использоваться в исходящих соединениях с проксируемым сервером, например, реальный IP-адрес клиента:

```
proxy_bind $remote_addr transparent;
```

Для работы параметра обычно требуется запустить рабочие процессы nginx с привилегиями [суперпользователя](../ngx_core_module.xml#user) . В Linux этого не требуется (1.13.8), так как если указан параметр `transparent` , то рабочие процессы наследуют capability `CAP_NET_RAW` из главного процесса. Также необходимо настроить таблицу маршрутизации ядра для перехвата сетевого трафика с проксируемого сервера.

## proxy_bind_dynamic

```
Syntax:  on | off
Default: off
Context: server, stream
```

*This directive appeared in version 1.29.3.*

Если включено, операция [bind](#proxy_bind) осуществляется при каждой попытке соединения.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## proxy_buffer_size

```
Syntax:  размер
Default: 16k
Context: server, stream
```

*This directive appeared in version 1.9.4.*

Задаёт `размер` буфера, в который будут читаться данные, получаемые от проксируемого сервера. Также задаёт `размер` буфера, в который будут читаться данные, получаемые от клиента.

## proxy_connect_timeout

```
Syntax:  время
Default: 60s
Context: server, stream
```

Задаёт таймаут для установления соединения с проксированным сервером.

## proxy_download_rate

```
Syntax:  скорость
Default: 0
Context: server, stream
```

*This directive appeared in version 1.9.3.*

Ограничивает скорость чтения данных от проксируемого сервера. `Скорость` задаётся в байтах в секунду. Значение 0 отключает ограничение скорости. Ограничение устанавливается на соединение, поэтому, если nginx одновременно откроет два соединения к проксируемому серверу, суммарная скорость будет вдвое выше заданного ограничения.

В значении параметра можно использовать переменные (1.17.0). Это может быть полезно в случаях, когда скорость нужно ограничивать в зависимости от какого-либо условия:

```
map $slow $rate {
    1     4k;
    2     8k;
}

proxy_download_rate $rate;
```

## proxy_half_close

```
Syntax:  on | off
Default: off
Context: server, stream
```

*This directive appeared in version 1.21.4.*

Разрешает или запрещает независимое закрытие каждой из сторон проксируемого соединения TCP (“TCP half-close”). Если разрешено, то проксирование по TCP будет продолжаться, пока обе стороны не закроют соединение.

## proxy_next_upstream

```
Syntax:  on | off
Default: on
Context: server, stream
```

При невозможности установить соединение с проксируемым сервером определяет, будет ли клиентское соединение передано следующему серверу.

Передача соединения следующему серверу может быть ограничена по [количеству попыток](#proxy_next_upstream_tries) и по [времени](#proxy_next_upstream_timeout) .

## proxy_next_upstream_timeout

```
Syntax:  время
Default: 0
Context: server, stream
```

Ограничивает время, в течение которого возможна передача соединения [следующему серверу](#proxy_next_upstream) . Значение `0` отключает это ограничение.

## proxy_next_upstream_tries

```
Syntax:  число
Default: 0
Context: server, stream
```

Ограничивает число допустимых попыток для передачи соединения [следующему серверу](#proxy_next_upstream) . Значение `0` отключает это ограничение.

## proxy_pass

```
Syntax:  адрес
Default: 
Context: server
```

Задаёт адрес проксируемого сервера. Адрес может быть указан в виде доменного имени или IP-адреса, и порта:

```
proxy_pass localhost:12345;
```

или в виде пути UNIX-сокета:

```
proxy_pass unix:/tmp/stream.socket;
```

Если доменному имени соответствует несколько адресов, то все они будут использоваться по очереди (round-robin). Кроме того, в качестве адреса можно указать [группу серверов](ngx_stream_upstream_module.xml) .

Адрес можно также задать с помощью переменных (1.11.3):

```
proxy_pass $upstream;
```

В этом случае имя сервера ищется среди описанных [групп серверов](ngx_stream_upstream_module.xml) и если не найдено, то определяется с помощью [resolver](ngx_stream_core_module.xml#resolver) ’а.

## proxy_protocol

```
Syntax:  on | off
Default: off
Context: server, stream
```

*This directive appeared in version 1.9.2.*

Включает [протокол PROXY](http://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) для соединений с проксируемым сервером.

## proxy_requests

```
Syntax:  число
Default: 0
Context: server, stream
```

*This directive appeared in version 1.15.7.*

Задаёт число датаграмм, полученных от клиента, по достижении которого удаляется привязка между клиентом и существующей UDP-сессией. После получения указанного количества датаграмм следующая датаграмма, полученная от того же клиента, начинает новую сессию. Cессия завершится после отправки всех принятых датаграмм на проксируемый сервер и получения указанного количества [ответов](#proxy_responses) или после [таймаута](#proxy_timeout) .

## proxy_responses

```
Syntax:  число
Default: 
Context: server, stream
```

*This directive appeared in version 1.9.13.*

Задаёт количество датаграмм, ожидаемых от проксируемого сервера в ответ на датаграмму клиента в случае, если используется протокол [UDP](ngx_stream_core_module.xml#udp) . Задаваемое число cлужит подсказкой для завершения сессии. По умолчанию количество датаграмм не ограничено.

Если указано нулевое значение, то ответ не ожидается. Однако если ответ получен и сессия ещё не завершилась, то ответ будет обработан.

## proxy_session_drop

```
Syntax:  on | off
Default: off
Context: server, stream
```

*This directive appeared in version 1.15.8.*

Позволяет завершить все сессии к проксируемому серверу, если он был удалён из группы или помечен как постоянно недоступный. Это может произойти вследствие повторного [преобразования имён](ngx_stream_core_module.xml#resolver) в адреса, а также при помощи команды API [`DELETE`](../http/ngx_http_api_module.xml#deleteStreamUpstreamServer) . Сервер может быть помечен как постоянно недоступный в случае неуспешной [проверки работоспособности](ngx_stream_upstream_hc_module.xml#health_check) , а также при помощи команды API [`PATCH`](../http/ngx_http_api_module.xml#patchStreamUpstreamServer) . Сессия завершается при обработке очередного события чтения или записи на стороне клиента или проксируемого сервера.

> **Note:** Эта директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## proxy_socket_keepalive

```
Syntax:  on | off
Default: off
Context: server, stream
```

*This directive appeared in version 1.15.6.*

Конфигурирует поведение “TCP keepalive” для исходящих соединений к проксируемому серверу. По умолчанию для сокета действуют настройки операционной системы. Если указано значение “ `on` ”, то для сокета включается параметр SO_KEEPALIVE .

## proxy_ssl

```
Syntax:  on | off
Default: off
Context: server, stream
```

Включает протоколы SSL/TLS для соединений с проксируемым сервером.

## proxy_ssl_certificate

```
Syntax:  файл
Default: 
Context: server, stream
```

Задаёт `файл` с сертификатом в формате PEM для аутентификации на проксируемом сервере.

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## proxy_ssl_certificate_cache

```
Syntax:  max=N [inactive=время] [valid=время]
Default: off
Context: server, stream
```

*This directive appeared in version 1.27.4.*

Задаёт кэш, в котором могут храниться [SSL-сертификаты](#proxy_ssl_certificate) и [секретные ключи](#proxy_ssl_certificate_key) , полученные из [переменных](#proxy_ssl_certificate_key_variables) .

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
proxy_ssl_certificate       $proxy_ssl_server_name.crt;
proxy_ssl_certificate_key   $proxy_ssl_server_name.key;
proxy_ssl_certificate_cache max=1000 inactive=20s valid=1m;
```

## proxy_ssl_certificate_key

```
Syntax:  файл
Default: 
Context: server, stream
```

Задаёт `файл` с секретным ключом в формате PEM для аутентификации на проксируемом сервере.

Вместо `файла` можно указать значение `store` : `схема` : `id` (1.29.0), которое используется для загрузки ключа с указанным `id` и зарегистрированной провайдером OpenSSL `схемой` URI, такой как [`pkcs11`](https://datatracker.ietf.org/doc/html/rfc7512) .

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## proxy_ssl_ciphers

```
Syntax:  шифры
Default: DEFAULT
Context: server, stream
```

Описывает разрешённые шифры для соединений с проксируемым сервером. Шифры задаются в формате, поддерживаемом библиотекой OpenSSL.

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

## proxy_ssl_conf_command

```
Syntax:  имя значение
Default: 
Context: server, stream
```

*This directive appeared in version 1.19.4.*

Задаёт произвольные конфигурационные [команды](https://www.openssl.org/docs/man1.1.1/man3/SSL_CONF_cmd.html) OpenSSL при установлении соединения с проксируемым сервером.

> **Note:** Директива поддерживается при использовании OpenSSL 1.0.2 и выше.

На одном уровне может быть указано несколько директив `proxy_ssl_conf_command` . Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `proxy_ssl_conf_command` .

> **Note:** Следует учитывать, что изменение настроек OpenSSL напрямую
может привести к неожиданному поведению.

## proxy_ssl_crl

```
Syntax:  файл
Default: 
Context: server, stream
```

Указывает `файл` с отозванными сертификатами (CRL) в формате PEM, используемыми при [проверке](#proxy_ssl_verify) сертификата проксируемого сервера.

## proxy_ssl_key_log

```
Syntax:  путь
Default: 
Context: server, stream
```

*This directive appeared in version 1.27.2.*

Включает логирование SSL-ключей соединений с проксируемым сервером и указывает путь к лог-файлу ключей. Ключи записываются в формате [SSLKEYLOGFILE](https://datatracker.ietf.org/doc/html/draft-ietf-tls-keylogfile) совместимом с Wireshark.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## proxy_ssl_name

```
Syntax:  имя
Default: хост из proxy_pass
Context: server, stream
```

Позволяет переопределить имя сервера, используемое при [проверке](#proxy_ssl_verify) сертификата проксируемого сервера, а также для [передачи его через SNI](#proxy_ssl_server_name) при установлении соединения с проксируемым сервером. Имя сервера можно также задать с помощью переменных (1.11.3).

По умолчанию используется имя хоста из адреса, заданного директивой [proxy_pass](#proxy_pass) .

## proxy_ssl_password_file

```
Syntax:  файл
Default: 
Context: server, stream
```

Задаёт `файл` с паролями от [секретных ключей](#proxy_ssl_certificate_key) , где каждый пароль указан на отдельной строке. Пароли применяются по очереди в момент загрузки ключа.

## proxy_ssl_protocols

```
Syntax:  [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3]
Default: TLSv1.2 TLSv1.3
Context: server, stream
```

Разрешает указанные протоколы для соединений с проксируемым сервером.

> **Note:** Параметр `TLSv1.3` используется по умолчанию
начиная с 1.23.4.

## proxy_ssl_server_name

```
Syntax:  on | off
Default: off
Context: server, stream
```

Разрешает или запрещает передачу имени сервера через [расширение Server Name Indication протокола TLS](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC 6066) при установлении соединения с проксируемым сервером.

## proxy_ssl_session_reuse

```
Syntax:  on | off
Default: on
Context: server, stream
```

Определяет, использовать ли повторно SSL-сессии при работе с проксируемым сервером. Если в логах появляются ошибки “ `digest check failed` ”, то можно попробовать выключить повторное использование сессий.

## proxy_ssl_trusted_certificate

```
Syntax:  файл
Default: 
Context: server, stream
```

Задаёт `файл` с доверенными сертификатами CA в формате PEM, используемыми при [проверке](#proxy_ssl_verify) сертификата проксируемого сервера.

## proxy_ssl_verify

```
Syntax:  on | off
Default: off
Context: server, stream
```

Разрешает или запрещает проверку сертификата проксируемого сервера.

## proxy_ssl_verify_depth

```
Syntax:  число
Default: 1
Context: server, stream
```

Устанавливает глубину проверки в цепочке сертификатов проксируемого сервера.

## proxy_timeout

```
Syntax:  время
Default: 10m
Context: server, stream
```

Задаёт `таймаут` между двумя идущими подряд операциями чтения или записи на клиентском соединении или соединении с проксируемым сервером. Если по истечении этого времени данные не передавались, соединение закрывается.

## proxy_upload_rate

```
Syntax:  скорость
Default: 0
Context: server, stream
```

*This directive appeared in version 1.9.3.*

Ограничивает скорость чтения данных от клиента. `Скорость` задаётся в байтах в секунду. Значение 0 отключает ограничение скорости. Ограничение устанавливается на соединение, поэтому, если клиент одновременно откроет два соединения, суммарная скорость будет вдвое выше заданного ограничения.

В значении параметра можно использовать переменные (1.17.0). Это может быть полезно в случаях, когда скорость нужно ограничивать в зависимости от какого-либо условия:

```
map $slow $rate {
    1     4k;
    2     8k;
}

proxy_upload_rate $rate;
```

