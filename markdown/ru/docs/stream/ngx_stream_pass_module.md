# Модуль ngx_stream_pass_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_stream_pass_module` (1.25.5) позволяет передавать принятое соединение напрямую в любой настроенный слушающий сокет в `http` , `stream` , `mail` и других подобных модулях.

# Пример конфигурации {#example}

```
http {
    server {
        listen 8000;

        location / {
            root html;
        }
    }
}

stream {
    server {
        listen 12345 ssl;

        ssl_certificate     domain.crt;
        ssl_certificate_key domain.key;

        pass 127.0.0.1:8000;
    }
}
```

В примере после терминирования SSL в модуле `stream` соединение передаётся в модуль `http` .

# Директивы {#directives}

## pass

```
Syntax:  адрес
Default: 
Context: server, stream
```

Задаёт адрес сервера с передаваемым соединением. Адрес может быть указан в виде IP-адреса и порта:

```
pass 127.0.0.1:12345;
```

или в виде пути UNIX-сокета:

```
pass unix:/tmp/stream.socket;
```

В адресе также можно использовать переменные:

```
pass $upstream;
```

