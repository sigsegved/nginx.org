# Модуль ngx_http_mirror_module

**Revision:** 4  
**Language:** ru


Модуль `ngx_http_mirror_module` (1.13.4) позволяет
зеркалировать исходный запрос
при помощи создания фоновых зеркалирующих подзапросов.
Ответы на зеркалирующие подзапросы игнорируются.

## Пример конфигурации {#example}

```
location / {
    mirror /mirror;
    proxy_pass http://backend;
}

location = /mirror {
    internal;
    proxy_pass http://test_backend$request_uri;
}
```

## Директивы {#directives}


uri | off
off
http
server
location


Задаёт URI, на который будет зеркалироваться исходный запрос.
На одном уровне конфигурации может быть задано несколько зеркал.




on | off
on
http
server
location


Определяет, зеркалировать ли тело запроса клиента.
Если включено, то тело запроса клиента будет прочитано
перед созданием зеркалирующих подзапросов.
В этом случае небуферизованное проксирование тела запроса клиента,
задаваемое директивами
,
,

и
,
будет отключено.

location / {
    mirror /mirror;
    mirror_request_body off;
    proxy_pass http://backend;
}

location = /mirror {
    internal;
    proxy_pass http://log_backend;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
}



