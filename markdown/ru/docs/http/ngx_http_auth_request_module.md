# Модуль ngx_http_auth_request_module

**Revision:** 5  
**Language:** ru

Модуль `ngx_http_auth_request_module` (1.5.4+) предоставляет возможность авторизации клиента, основанной на результате подзапроса. Если подзапрос возвращает код ответа 2xx, доступ разрешается. Если 401 или 403 — доступ запрещается с соответствующим кодом ошибки. Любой другой код ответа, возвращаемый подзапросом, считается ошибкой.

При ошибке 401 клиенту также передаётся заголовок `WWW-Authenticate` из ответа подзапроса.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_auth_request_module` .

Модуль может быть скомбинирован с другими модулями доступа, такими как [ngx_http_access_module](ngx_http_access_module.xml) , [ngx_http_auth_basic_module](ngx_http_auth_basic_module.xml) и [ngx_http_auth_jwt_module](ngx_http_auth_jwt_module.xml) , с помощью директивы [satisfy](ngx_http_core_module.xml#satisfy) .

> **Note:** До версии 1.7.3 ответы на авторизационные подзапросы не могли быть закэшированы
(с использованием директив [proxy_cache](ngx_http_proxy_module.xml#proxy_cache) , [proxy_store](ngx_http_proxy_module.xml#proxy_store) и т.п.).

# Пример конфигурации {#example}

```
location /private/ {
    auth_request /auth;
    ...
}

location = /auth {
    proxy_pass ...
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
}
```

# Директивы {#directives}

## auth_request

```
Syntax:  uri | off
Default: off
Context: location, http, server
```

Включает авторизацию, основанную на результате выполнения подзапроса, и задаёт URI, на который будет отправлен подзапрос.

## auth_request_set

```
Syntax:  $переменная значение
Default: 
Context: location, http, server
```

Устанавливает `переменную` в запросе в заданное `значение` после завершения запроса авторизации. Значение может содержать переменные из запроса авторизации, например, `$upstream_http_*` .

