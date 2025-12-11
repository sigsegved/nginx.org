# Модуль ngx_http_internal_redirect_module

**Revision:** 1  
**Language:** ru


Модуль `ngx_http_internal_redirect_module` (1.23.4) позволяет
осуществлять внутреннее перенаправление.
В отличие от
[изменения URI](ngx_http_rewrite_module.html),
перенаправление происходит после проверок ограничений
[скорости обработки запросов](ngx_http_limit_req_module.html),
[числа соединений](ngx_http_limit_conn_module.html)
и [доступа](ngx_http_access_module.html).

> **Note:** Модуль доступен как часть
коммерческой подписки

## Пример конфигурации {#example}

```
limit_req_zone $jwt_claim_sub zone=jwt_sub:10m rate=1r/s;

server {
    location / {
        auth_jwt          "realm";
        auth_jwt_key_file key.jwk;

        internal_redirect @rate_limited;
    }

    location @rate_limited {
        internal;

        limit_req  zone=jwt_sub burst=10;
        proxy_pass http://backend;
    }
}
```

В примере
[скорость обработки запросов](ngx_http_limit_req_module.html)
ограничивается по
[идентификатору
клиента](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.2).
Конфигурация без internal_redirect
может быть подвержена DoS-атакам при помощи неподписанных JWT, так как проверка
[limit_req](ngx_http_limit_req_module.xml#limit_req)
выполняется
[перед](../dev/development_guide.xml#http_phases)
проверкой
[auth_jwt](ngx_http_auth_jwt_module.xml#auth_jwt).
Использование internal_redirect
позволяет изменить порядок этих проверок.

## Директивы {#directives}


uri

server
location


Задаёт URI для внутреннего перенаправления запроса.
Вместо URI также можно использовать
именованный location.
В значении uri можно использовать переменные.
Если значение uri пустое,
то перенаправление не осуществляется.


