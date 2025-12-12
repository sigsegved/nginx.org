# Модуль ngx_http_memcached_module

**Revision:** 19  
**Language:** ru

Модуль `ngx_http_memcached_module` позволяет получать ответ из сервера memcached. Ключ задаётся в переменной `$memcached_key` . Ответ в memcached должен быть предварительно помещён внешним по отношению к nginx’у способом.

# Пример конфигурации {#example}

```
server {
    location / {
        set            $memcached_key "$uri?$args";
        memcached_pass host:11211;
        error_page     404 502 504 = @fallback;
    }

    location @fallback {
        proxy_pass     http://backend;
    }
}
```

# Директивы {#directives}

## memcached_allow_upstream

```
Syntax:  memcached_allow_upstream строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Задаёт условия, при которых доступ к серверу memcached будет разрешён или [запрещён](#denied) . Если все значения строковых параметров непустые и не равны “0”, то доступ разрешён. Условия проверяются каждый раз перед установлением соединения с сервером memcached. В значении параметров допустимо использование переменных:

```
geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;

    location / {
        memcached_pass           host:11211;
        memcached_allow_upstream $allow;
        ...
    }
}
```

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## memcached_bind

```
Syntax:  memcached_bind адрес [transparent ] | off;
Default: 
Context: location, http, server
```

*This directive appeared in version 0.8.22.*

Задаёт локальный IP-адрес с необязательным портом (1.11.2), который будет использоваться в исходящих соединениях с сервером memcached. В значении параметра допустимо использование переменных (1.3.12). Специальное значение `off` (1.3.12) отменяет действие унаследованной с предыдущего уровня конфигурации директивы `memcached_bind` , позволяя системе самостоятельно выбирать локальный IP-адрес и порт.

Параметр `transparent` (1.11.0) позволяет задать нелокальный IP-aдрес, который будет использоваться в исходящих соединениях с сервером memcached, например, реальный IP-адрес клиента:

```
memcached_bind $remote_addr transparent;
```

Для работы параметра обычно требуется запустить рабочие процессы nginx с привилегиями [суперпользователя](../ngx_core_module.xml#user) . В Linux этого не требуется (1.13.8), так как если указан параметр `transparent` , то рабочие процессы наследуют capability `CAP_NET_RAW` из главного процесса. Также необходимо настроить таблицу маршрутизации ядра для перехвата сетевого трафика с сервера memcached.

## memcached_bind_dynamic

```
Syntax:  memcached_bind_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Если включено, операция [bind](#memcached_bind) осуществляется при каждой попытке соединения.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## memcached_buffer_size

```
Syntax:  memcached_buffer_size размер;
Default: 4k|8k
Context: location, http, server
```

Задаёт `размер` буфера, в который будет читаться ответ, получаемый от сервера memcached. Ответ синхронно передаётся клиенту сразу же по мере его поступления.

## memcached_connect_timeout

```
Syntax:  memcached_connect_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут для установления соединения с сервером memcached. Необходимо иметь в виду, что этот таймаут обычно не может превышать 75 секунд.

## memcached_gzip_flag

```
Syntax:  memcached_gzip_flag флаг;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.3.6.*

Включает проверку указанного `флага` в ответе сервера memcached и установку поля “ `Content-Encoding` ” заголовка ответа в “ `gzip` ”, если этот флаг установлен.

## memcached_next_upstream

```
Syntax:  memcached_next_upstream error | timeout | denied | invalid_response | not_found | off ...;
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

**`invalid_response`**  
  сервер вернул пустой или неверный ответ;

**`not_found`**  
  сервер не нашёл ответ;

**`off`**  
  запрещает передачу запроса следующему серверу.

Необходимо понимать, что передача запроса следующему серверу возможна только при условии, что клиенту ещё ничего не передавалось. То есть, если ошибка или таймаут возникли в середине передачи ответа, то исправить это уже невозможно.

Директива также определяет, что считается [неудачной попыткой](ngx_http_upstream_module.xml#max_fails) работы с сервером. Случаи `error` , `timeout` , `denied` и `invalid_response` всегда считаются неудачными попытками, даже если они не указаны в директиве. Случай `not_found` никогда не считается неудачной попыткой.

Передача запроса следующему серверу может быть ограничена по [количеству попыток](#memcached_next_upstream_tries) и по [времени](#memcached_next_upstream_timeout) .

## memcached_next_upstream_timeout

```
Syntax:  memcached_next_upstream_timeout время;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает время, в течение которого возможна передача запроса [следующему серверу](#memcached_next_upstream) . Значение `0` отключает это ограничение.

## memcached_next_upstream_tries

```
Syntax:  memcached_next_upstream_tries число;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает число допустимых попыток для передачи запроса [следующему серверу](#memcached_next_upstream) . Значение `0` отключает это ограничение.

## memcached_pass

```
Syntax:  memcached_pass адрес;
Default: 
Context: if в location, location
```

Задаёт адрес сервера memcached. Адрес может быть указан в виде доменного имени или IP-адреса, и порта:

```
memcached_pass localhost:11211;
```

или в виде пути UNIX-сокета:

```
memcached_pass unix:/tmp/memcached.socket;
```

Если доменному имени соответствует несколько адресов, то все они будут использоваться по очереди (round-robin). И, кроме того, адрес может быть [группой серверов](ngx_http_upstream_module.xml) .

## memcached_read_timeout

```
Syntax:  memcached_read_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при чтении ответа сервера memcached. Таймаут устанавливается не на всю передачу ответа, а только между двумя операциями чтения. Если по истечении этого времени сервер memcached ничего не передаст, соединение закрывается.

## memcached_send_timeout

```
Syntax:  memcached_send_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при передаче запроса серверу memcached. Таймаут устанавливается не на всю передачу запроса, а только между двумя операциями записи. Если по истечении этого времени сервер memcached не примет новых данных, соединение закрывается.

## memcached_socket_keepalive

```
Syntax:  memcached_socket_keepalive on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.15.6.*

Конфигурирует поведение “TCP keepalive” для исходящих соединений к серверу memcached. По умолчанию для сокета действуют настройки операционной системы. Если указано значение “ `on` ”, то для сокета включается параметр SO_KEEPALIVE .

# Встроенные переменные {#variables}

**`$memcached_key`**  
  Задаёт ключ для получения ответа из сервера memcached.

