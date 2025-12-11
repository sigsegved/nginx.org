# Модуль ngx_http_auth_jwt_module

**Revision:** 12  
**Language:** ru


Модуль `ngx_http_auth_jwt_module` (1.11.3)
предоставляет возможность авторизации клиента с проверкой предоставляемого
[JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519) (JWT)
при помощи указанных ключей.
Модуль поддерживает
[JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515) (JWS),
[JSON Web Encryption](https://datatracker.ietf.org/doc/html/rfc7516) (JWE)
(1.19.7) и Nested JWT (1.21.0).
Модуль может использоваться для настройки аутентификации
[OpenID Connect](http://openid.net/specs/openid-connect-core-1_0.html).

Модуль может быть скомбинирован с
другими модулями доступа, такими как
[ngx_http_access_module](ngx_http_access_module.html),
[ngx_http_auth_basic_module](ngx_http_auth_basic_module.html)
и
[ngx_http_auth_request_module](ngx_http_auth_request_module.html)
с помощью директивы [](ngx_http_core_module.xml#satisfy).

> **Note:** Модуль доступен как часть
коммерческой подписки.

## Поддерживаемые алгоритмы {#algorithms}

Модуль поддерживает следующие криптографические
[алгоритмы](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms).

Алгоритмы JWS:

- HS256, HS384, HS512
- RS256, RS384, RS512
- ES256, ES384, ES512
- EdDSA (подписи Ed25519 и Ed448) (1.15.7)
- PS256, PS384, PS512 (1.29.0)



> **Note:** До версии 1.13.7
поддерживались только алгоритмы HS256, RS256 и ES256.

Алгоритмы JWE для шифрования содержимого (1.19.7):

- A128CBC-HS256, A192CBC-HS384, A256CBC-HS512
- A128GCM, A192GCM, A256GCM

Алгоритмы JWE для управления ключом (1.19.9):

- A128KW, A192KW, A256KW
- A128GCMKW, A192GCMKW, A256GCMKW
- dir—прямое использование симметричного ключа
в качестве ключа шифрования содержимого
- RSA-OAEP, RSA-OAEP-256, RSA-OAEP-384, RSA-OAEP-512 (1.21.0)

## Пример конфигурации {#example}

```
location / {
    auth_jwt          "closed site";
    auth_jwt_key_file conf/keys.json;
}
```

## Директивы {#directives}



    строка
    [token=$переменная] |
    off
off
http
server
location
limit_except


Включает проверку JSON Web Token.
Заданная строка используется в качестве realm.
В значении параметра допустимо использование переменных.



Необязательный параметр token задаёт переменную,
содержащую JSON Web Token.
По умолчанию JWT передаётся в заголовке Authorization
в качестве
Bearer Token.
JWT может также передаваться как кука или часть строки запроса:

auth_jwt "closed site" token=$cookie_auth_token;




Специальное значение off отменяет действие
унаследованной с предыдущего уровня конфигурации
директивы auth_jwt.




$переменная имя ...

http
1.11.10


Устанавливает переменную в параметр JWT claim,
определяемый именами ключей.
Сопоставление имён начинается с верхнего уровня дерева JSON.
Для массива переменная хранит список его элементов, разделяемых запятыми.

auth_jwt_claim_set $email info e-mail;
auth_jwt_claim_set $job info "job title";


До версии 1.13.7 можно было указать лишь одно имя,
результат для массивов был не определён.





Значения переменных для tokens, зашифрованных при помощи JWE,
доступны только после дешифрования, которое происходит в
Access-фазе.





$переменная имя ...

http
1.11.10


Устанавливает переменную в параметр заголовка JOSE,
определяемый именами ключей.
Сопоставление имён начинается с верхнего уровня дерева JSON.
Для массива переменная хранит список его элементов, разделяемых запятыми.

До версии 1.13.7 можно было указать лишь одно имя,
результат для массивов был не определён.





 время
0
http
server
location
1.21.4


Разрешает или запрещает кэширование ключей,
полученных из файла или из
подзапроса,
и задаёт время их кэширования.
Кэширование ключей, полученных из переменных, не поддерживается.
По умолчанию кэширование ключей выключено.




файл

http
server
location
limit_except


Задаёт файл в формате
JSON Web Key Set
для проверки подписи JWT.
В значении параметра допустимо использование переменных.



На одном уровне может быть указано
несколько директив auth_jwt_key_file (1.21.1):

auth_jwt_key_file conf/keys.json;
auth_jwt_key_file conf/key.jwk;

Если хотя бы один из указанных ключей не может быть загружен или обработан,
nginx вернёт ошибку
.




uri

http
server
location
limit_except
1.15.6


Позволяет получать файл в формате
JSON Web Key Set
из подзапроса для проверки подписи JWT и
задаёт URI, на который будет отправлен подзапрос.
В значении параметра допустимо использование переменных.
Для предотвращения дополнительных затрат на проверку
файл рекомендутеся кэшировать.

proxy_cache_path /data/nginx/cache levels=1 keys_zone=foo:10m;

server {
    ...

    location / {
        auth_jwt             "closed site";
        auth_jwt_key_request /jwks_uri;
    }

    location = /jwks_uri {
        internal;
        proxy_cache foo;
        proxy_pass  http://idp.example.com/keys;
    }
}

На одном уровне может быть указано
несколько директив auth_jwt_key_request (1.21.1):

auth_jwt_key_request /jwks_uri;
auth_jwt_key_request /jwks2_uri;

Если хотя бы один из указанных ключей не может быть загружен или обработан,
nginx вернёт ошибку
.




время
0s
http
server
location
1.13.10


Задаёт максимально допустимое отклонение времени для компенсации
расхождения часов при проверке JWT claims
exp
и
nbf.




signed |
        encrypted |
        nested
signed
http
server
location
limit_except
1.19.7


Задаёт ожидаемый тип JSON Web Token:
JWS (signed),
JWE (encrypted)
или подписанный и затем зашифрованный
Nested JWT (nested) (1.21.0).





    $значение ...
    [error=401 |
                              403]


http
server
location
limit_except
1.21.2


Задаёт дополнительные условия для проверки JWT.
В качестве значения можно использовать текст, переменные и их комбинации,
значение должно начинаться c переменной (1.21.7).
Для успешной аутентификации необходимо, чтобы
значение всех строковых параметров было непустое или не равно “0”.

map $jwt_claim_iss $valid_jwt_iss {
    "good" 1;
}
...

auth_jwt_require $valid_jwt_iss;




При невыполнении любого из условий
возвращается код ответа 401.
Необязательный параметр error (1.21.7)
позволяет переопределить код ответа на 403.



## Встроенные переменные {#variables}

Модуль `ngx_http_auth_jwt_module`
поддерживает встроенные переменные:

***$jwt_header_**имя***  
  возвращает значение указанного
[заголовка JOSE](https://datatracker.ietf.org/doc/html/rfc7515#section-4)
***$jwt_claim_**имя***  
  возвращает значение указанной
[JWT claim](https://datatracker.ietf.org/doc/html/rfc7519#section-4)


Для вложенных claim, а также claim, содержащих точку (“.”),
значение переменной вычислить невозможно,
следует использовать директиву .



Значения переменных для tokens, зашифрованных при помощи JWE,
доступны только после дешифрования, которое происходит в
Access-фазе.
***$jwt_payload***  
  возвращает расшифрованную полезную нагрузку (payload) верхнего уровня
для `вложенных`
или `зашифрованных` токенов (1.21.2).
Для вложенных токенов возвращает внутренний JWS токен.
Для зашифрованных токенов возвращает JSON с claims.
