# Модуль ngx_stream_ssl_preread_module

**Revision:** 3  
**Language:** ru

Модуль `ngx_stream_ssl_preread_module` (1.11.5) позволяет извлекать информацию из сообщения [ClientHello](https://datatracker.ietf.org/doc/html/rfc5246#section-7.4.1.2) без терминирования SSL/TLS, например имя сервера, запрошенное через [SNI](https://datatracker.ietf.org/doc/html/rfc6066#section-3) или протоколы, указанные в [ALPN](https://datatracker.ietf.org/doc/html/rfc7301) . По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-stream_ssl_preread_module` .

# Пример конфигурации {#example}

Выбор сервера по имени:

```
map $ssl_preread_server_name $name {
    backend.example.com      backend;
    default                  backend2;
}

upstream backend {
    server 192.168.0.1:12345;
    server 192.168.0.2:12345;
}

upstream backend2 {
    server 192.168.0.3:12345;
    server 192.168.0.4:12345;
}

server {
    listen      12346;
    proxy_pass  $name;
    ssl_preread on;
}
```

Выбор сервера по протоколу:

```
map $ssl_preread_alpn_protocols $proxy {
    ~\bh2\b           127.0.0.1:8001;
    ~\bhttp/1.1\b     127.0.0.1:8002;
    ~\bxmpp-client\b  127.0.0.1:8003;
}

server {
    listen      9000;
    proxy_pass  $proxy;
    ssl_preread on;
}
```

Выбор сервера по версии протокола SSL:

```
map $ssl_preread_protocol $upstream {
    ""        ssh.example.com:22;
    "TLSv1.2" new.example.com:443;
    default   tls.example.com:443;
}

# ssh и https на одном порту
server {
    listen      192.168.0.1:443;
    proxy_pass  $upstream;
    ssl_preread on;
}
```

# Директивы {#directives}

## ssl_preread

```
Syntax:  on | off
Default: off
Context: server, stream
```

Разрешает извлечение информации из сообщения ClientHello во время фазы [предварительного чтения](stream_processing.xml#preread_phase) .

# Встроенные переменные {#variables}

**`$ssl_preread_protocol`**  
  максимальная версия протокола SSL, поддерживаемая клиентом (1.15.2)

**`$ssl_preread_server_name`**  
  имя сервера, запрошенное через SNI

**`$ssl_preread_alpn_protocols`**  
  список протоколов, переданный клиентом через ALPN (1.13.10).
Значения разделяются запятыми.

