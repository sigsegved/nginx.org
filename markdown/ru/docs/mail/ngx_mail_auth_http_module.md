# Модуль ngx_mail_auth_http_module

**Revision:** 11  
**Language:** ru

# Директивы {#directives}

## auth_http

```
Syntax:  URL
Default: 
Context: server, mail
```

Задаёт URL HTTP-сервера аутентификации. Протокол описан [ниже](#protocol) .

## auth_http_header

```
Syntax:  заголовок значение
Default: 
Context: server, mail
```

Добавляет указанный заголовок к запросам, посылаемым на сервер аутентификации. Заголовок можно использовать в качестве shared secret для проверки, что запрос поступил от nginx. Например:

```
auth_http_header X-Auth-Key "secret_string";
```

## auth_http_pass_client_cert

```
Syntax:  on | off
Default: off
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Добавляет заголовок `Auth-SSL-Cert` с [клиентским](ngx_mail_ssl_module.xml#ssl_verify_client) сертификатом в формате PEM (закодирован в формате urlencode) к запросам, посылаемым на сервер аутентификации.

## auth_http_timeout

```
Syntax:  время
Default: 60s
Context: server, mail
```

Задаёт таймаут общения с сервером аутентификации.

# Протокол {#protocol}

Для общения с сервером аутентификации используется протокол HTTP. Данные в теле ответа игнорируются, информация передаётся только в заголовках.

Примеры запросов и ответов:

Запрос:

```
GET /auth HTTP/1.0
Host: localhost
Auth-Method: plain # plain/apop/cram-md5/external
Auth-User: user
Auth-Pass: password
Auth-Protocol: imap # imap/pop3/smtp
Auth-Login-Attempt: 1
Client-IP: 192.0.2.42
Client-Host: client.example.org
```

Хороший ответ:

```
HTTP/1.0 200 OK
Auth-Status: OK
Auth-Server: 198.51.100.1
Auth-Port: 143
```

Плохой ответ:

```
HTTP/1.0 200 OK
Auth-Status: Invalid login or password
Auth-Wait: 3
```

Если заголовка `Auth-Wait` нет, то после выдачи ошибки соединение будет закрыто. В текущей реализации на каждую попытку аутентификации выделяется память, которая освобождается только при завершении сессии. Поэтому число неудачных попыток аутентификации в рамках одной сессии должно быть ограничено — после 10-20 попыток (номер попытки передаётся в заголовке `Auth-Login-Attempt` ) сервер должен выдать ответ без заголовка `Auth-Wait` .

При использовании APOP или CRAM-MD5 запрос и ответ будут выглядеть так:

```
GET /auth HTTP/1.0
Host: localhost
Auth-Method: apop
Auth-User: user
Auth-Salt: <238188073.1163692009@mail.example.com>
Auth-Pass: auth_response
Auth-Protocol: imap
Auth-Login-Attempt: 1
Client-IP: 192.0.2.42
Client-Host: client.example.org
```

Хороший ответ:

```
HTTP/1.0 200 OK
Auth-Status: OK
Auth-Server: 198.51.100.1
Auth-Port: 143
Auth-Pass: plain-text-pass
```

Если в ответе есть заголовок `Auth-User` , то он переопределяет имя пользователя, используемое для аутентификации с бэкендом.

Для SMTP в ответе дополнительно учитывается заголовок `Auth-Error-Code` — если он есть, то используется как код ответа в случае ошибки. Если его нет, то по умолчанию к `Auth-Status` будет добавлен код 535 5.7.0.

Например, если от сервера аутентификации будет получен ответ:

```
HTTP/1.0 200 OK
Auth-Status: Temporary server problem, try again later
Auth-Error-Code: 451 4.3.0
Auth-Wait: 3
```

то по SMTP клиенту будет выдана ошибка

```
451 4.3.0 Temporary server problem, try again later
```

Если при проксировании SMTP не требуется аутентификация, запрос будет выглядеть так:

```
GET /auth HTTP/1.0
Host: localhost
Auth-Method: none
Auth-User:
Auth-Pass:
Auth-Protocol: smtp
Auth-Login-Attempt: 1
Client-IP: 192.0.2.42
Client-Host: client.example.org
Auth-SMTP-Helo: client.example.org
Auth-SMTP-From: MAIL FROM: <>
Auth-SMTP-To: RCPT TO: <postmaster@mail.example.com>
```

Для клиентского соединения по протоколу SSL/TLS (1.7.11) добавляется заголовок `Auth-SSL` , и если директива [ssl_verify_client](ngx_mail_ssl_module.xml#ssl_verify_client) включена, заголовок `Auth-SSL-Verify` содержит результат проверки клиентского сертификата: “ `SUCCESS` ”, “ `FAILED:` `reason` ” и, если сертификат не был предоставлен, “ `NONE` ”.

> **Note:** До версии 1.11.7 результат “ `FAILED` ”
не содержал строку `reason` .

Если клиентский сертификат был предоставлен, информация о нём передаётся в следующих заголовках запроса: `Auth-SSL-Subject` , `Auth-SSL-Issuer` , `Auth-SSL-Serial` и `Auth-SSL-Fingerprint` . Если директива [auth_http_pass_client_cert](#auth_http_pass_client_cert) включена, сам сертификат передаётся в заголовке `Auth-SSL-Cert` . Протокол и шифр установленного соединения передаются в заголовках `Auth-SSL-Protocol` и `Auth-SSL-Cipher` (1.21.2). Запрос будет выглядеть так:

```
GET /auth HTTP/1.0
Host: localhost
Auth-Method: plain
Auth-User: user
Auth-Pass: password
Auth-Protocol: imap
Auth-Login-Attempt: 1
Client-IP: 192.0.2.42
Auth-SSL: on
Auth-SSL-Protocol: TLSv1.3
Auth-SSL-Cipher: TLS_AES_256_GCM_SHA384
Auth-SSL-Verify: SUCCESS
Auth-SSL-Subject: /CN=example.com
Auth-SSL-Issuer: /CN=example.com
Auth-SSL-Serial: C07AD56B846B5BFF
Auth-SSL-Fingerprint: 29d6a80a123d13355ed16b4b04605e29cb55a5ad
```

При использовании [протокола PROXY](ngx_mail_core_module.xml#proxy_protocol) , информация о нём передаётся в следующих заголовках запроса: `Proxy-Protocol-Addr` , `Proxy-Protocol-Port` , `Proxy-Protocol-Server-Addr` и `Proxy-Protocol-Server-Port` (1.19.8).

