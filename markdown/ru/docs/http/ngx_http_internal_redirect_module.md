# Модуль ngx_http_internal_redirect_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_http_internal_redirect_module` (1.23.4) позволяет осуществлять внутреннее перенаправление. В отличие от [изменения URI](ngx_http_rewrite_module.xml) , перенаправление происходит после проверок ограничений [скорости обработки запросов](ngx_http_limit_req_module.xml) , [числа соединений](ngx_http_limit_conn_module.xml) и [доступа](ngx_http_access_module.xml) .

> **Note:** Модуль доступен как часть [коммерческой подписки](https://nginx.com/products/)

# Пример конфигурации {#example}

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

В примере [скорость обработки запросов](ngx_http_limit_req_module.xml) ограничивается по [идентификатору клиента](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.2) . Конфигурация без [internal_redirect](#internal_redirect) может быть подвержена DoS-атакам при помощи неподписанных JWT, так как проверка [limit_req](ngx_http_limit_req_module.xml#limit_req) выполняется [перед](../dev/development_guide.xml#http_phases) проверкой [auth_jwt](ngx_http_auth_jwt_module.xml#auth_jwt) . Использование [internal_redirect](#internal_redirect) позволяет изменить порядок этих проверок.

# Директивы {#directives}

## internal_redirect

```
Syntax:  internal_redirect uri;
Default: 
Context: location, server
```

Задаёт URI для внутреннего перенаправления запроса. Вместо URI также можно использовать [именованный location](ngx_http_core_module.xml#location_named) . В значении `uri` можно использовать переменные. Если значение `uri` пустое, то перенаправление не осуществляется.

