# Модуль ngx_mail_ssl_module

**Revision:** 33  
**Language:** ru

Модуль `ngx_mail_ssl_module` обеспечивает работу почтового прокси-сервера по протоколу SSL/TLS.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-mail_ssl_module` .

> **Note:** Для сборки и работы этого модуля нужна библиотека [OpenSSL](http://www.openssl.org) .

# Пример конфигурации {#example}

Для уменьшения загрузки процессора рекомендуется

- установить число [рабочих процессов](../ngx_core_module.xml#worker_processes) равным числу процессоров,
- включить [разделяемый](#ssl_session_cache_shared) кэш сессий,
- выключить [встроенный](#ssl_session_cache_builtin) кэш сессий
- и, возможно, увеличить [время жизни](#ssl_session_timeout) сессии
(по умолчанию 5 минут):

```
worker_processes auto;

mail {

    ...

    server {
        listen              993 ssl;

        ssl_protocols       TLSv1.2 TLSv1.3;
        ssl_ciphers         AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
        ssl_certificate     /usr/local/nginx/conf/cert.pem;
        ssl_certificate_key /usr/local/nginx/conf/cert.key;
        ssl_session_cache   shared:SSL:10m;
        ssl_session_timeout 10m;

        ...
    }
```

# Директивы {#directives}

## ssl

```
Syntax:  on | off
Default: off
Context: server, mail
```

Эта директива устарела в версии 1.15.0 и была удалена в версии 1.25.1. Вместо неё следует использовать параметр `ssl` директивы [listen](ngx_mail_core_module.xml#listen) .

## ssl_certificate

```
Syntax:  файл
Default: 
Context: server, mail
```

Указывает `файл` с сертификатом в формате PEM для данного сервера. Если вместе с основным сертификатом нужно указать промежуточные, то они должны находиться в этом же файле в следующем порядке: сначала основной сертификат, а затем промежуточные. В этом же файле может находиться секретный ключ в формате PEM.

Начиная с версии 1.11.0 эта директива может быть указана несколько раз для загрузки сертификатов разных типов, например RSA и ECDSA:

```
server {
    listen              993 ssl;

    ssl_certificate     example.com.rsa.crt;
    ssl_certificate_key example.com.rsa.key;

    ssl_certificate     example.com.ecdsa.crt;
    ssl_certificate_key example.com.ecdsa.key;

    ...
}
```

> **Note:** Возможность задавать отдельные [цепочки
сертификатов](../http/configuring_https_servers.xml#chains) для разных сертификатов
есть только в OpenSSL 1.0.2 и выше.
Для более старых версий следует указывать только одну цепочку сертификатов.

Вместо `файла` можно указать значение `data` : `сертификат` (1.15.10), при котором сертификат загружается без использования промежуточных файлов. При этом следует учитывать, что ненадлежащее использование подобного синтаксиса может быть небезопасно, например данные секретного ключа могут попасть в [лог ошибок](../ngx_core_module.xml#error_log) .

## ssl_certificate_compression

```
Syntax:  on | off
Default: off
Context: server, mail
```

*This directive appeared in version 1.29.1.*

Разрешает [сжатие](https://datatracker.ietf.org/doc/html/rfc8879) серверных сертификатов при использовании TLS 1.3.

> **Note:** Директива поддерживается при использовании OpenSSL 3.2 и выше;
список поддерживаемых алгоритмов сжатия обеспечивается библиотекой.

> **Note:** Директива поддерживается при использовании BoringSSL;
список поддерживаемых алгоритмов сжатия включает `zlib` (1.29.3).

## ssl_certificate_key

```
Syntax:  файл
Default: 
Context: server, mail
```

Указывает `файл` с секретным ключом в формате PEM для данного сервера.

Вместо `файла` можно указать значение `engine` : `имя` : `id` (1.7.9), которое загружает ключ с указанным `id` из OpenSSL engine с заданным `именем` .

Вместо `файла` можно указать значение `store` : `схема` : `id` (1.29.0), которое используется для загрузки ключа с указанным `id` и зарегистрированной провайдером OpenSSL `схемой` URI, такой как [`pkcs11`](https://datatracker.ietf.org/doc/html/rfc7512) .

Вместо `файла` можно указать значение `data` : `ключ` (1.15.10), при котором секретный ключ загружается без использования промежуточных файлов. При этом следует учитывать, что ненадлежащее использование подобного синтаксиса может быть небезопасно, например данные секретного ключа могут попасть в [лог ошибок](../ngx_core_module.xml#error_log) .

## ssl_ciphers

```
Syntax:  шифры
Default: HIGH:!aNULL:!MD5
Context: server, mail
```

Описывает разрешённые шифры. Шифры задаются в формате, поддерживаемом библиотекой OpenSSL, например:

```
ssl_ciphers ALL:!aNULL:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
```

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

> **Note:** В предыдущих версиях nginx по умолчанию использовались [другие](../http/configuring_https_servers.xml#compatibility) шифры.

## ssl_client_certificate

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Указывает `файл` с доверенными сертификатами CA в формате PEM, которые используются для [проверки](#ssl_verify_client) клиентских сертификатов.

Список сертификатов будет отправляться клиентам. Если это нежелательно, можно воспользоваться директивой [ssl_trusted_certificate](#ssl_trusted_certificate) .

## ssl_conf_command

```
Syntax:  имя значение
Default: 
Context: server, mail
```

*This directive appeared in version 1.19.4.*

Задаёт произвольные конфигурационные [команды](https://www.openssl.org/docs/man1.1.1/man3/SSL_CONF_cmd.html) OpenSSL.

> **Note:** Директива поддерживается при использовании OpenSSL 1.0.2 и выше.

На одном уровне может быть указано несколько директив `ssl_conf_command` :

```
ssl_conf_command Options PrioritizeChaCha;
ssl_conf_command Ciphersuites TLS_CHACHA20_POLY1305_SHA256;
```

Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `ssl_conf_command` .

> **Note:** Следует учитывать, что изменение настроек OpenSSL напрямую
может привести к неожиданному поведению.

## ssl_crl

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Указывает `файл` с отозванными сертификатами (CRL) в формате PEM, используемыми для [проверки](#ssl_verify_client) клиентских сертификатов.

## ssl_dhparam

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 0.7.2.*

Указывает `файл` с параметрами для DHE-шифров.

По умолчанию параметры не заданы, и соответственно DHE-шифры не будут использоваться.

> **Note:** До версии 1.11.0 по умолчанию использовались встроенные параметры.

## ssl_ecdh_curve

```
Syntax:  кривая
Default: auto
Context: server, mail
```

*This directive appeared in version 1.0.6.*

Задаёт кривую для ECDHE-шифров.

При использовании OpenSSL 1.0.2 и выше можно указывать несколько кривых (1.11.0), например:

```
ssl_ecdh_curve prime256v1:secp384r1;
```

Специальное значение `auto` (1.11.0) соответствует встроенному в библиотеку OpenSSL списку кривых для OpenSSL 1.0.2 и выше, или `prime256v1` для более старых версий.

> **Note:** До версии 1.11.0
по умолчанию использовалась кривая `prime256v1` .

> **Note:** При использовании OpenSSL 1.0.2 и выше
директива задаёт список кривых, поддерживаемых сервером.
Поэтому для работы ECDSA-сертификатов
важно, чтобы список включал кривые, используемые в сертификатах.

## ssl_password_file

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 1.7.3.*

Задаёт `файл` с паролями от [секретных ключей](#ssl_certificate_key) , где каждый пароль указан на отдельной строке. Пароли применяются по очереди в момент загрузки ключа.

Пример:

```
mail {
    ssl_password_file /etc/keys/global.pass;
    ...

    server {
        server_name mail1.example.com;
        ssl_certificate_key /etc/keys/first.key;
    }

    server {
        server_name mail2.example.com;

        # вместо файла можно указать именованный канал
        ssl_password_file /etc/keys/fifo;
        ssl_certificate_key /etc/keys/second.key;
    }
}
```

## ssl_prefer_server_ciphers

```
Syntax:  on | off
Default: off
Context: server, mail
```

Указывает, чтобы при использовании протоколов SSLv3 и TLS серверные шифры были более приоритетны, чем клиентские.

## ssl_protocols

```
Syntax:  [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3]
Default: TLSv1.2 TLSv1.3
Context: server, mail
```

Разрешает указанные протоколы.

> **Note:** Параметры `TLSv1.1` и `TLSv1.2` (1.1.13, 1.0.12) работают только при использовании OpenSSL 1.0.1 и выше.

> **Note:** Параметр `TLSv1.3` (1.13.0) работает только
при использовании OpenSSL 1.1.1 и выше.

> **Note:** Параметр `TLSv1.3` используется по умолчанию
начиная с 1.23.4.

## ssl_session_cache

```
Syntax:  off | none | [builtin[:размер]] [shared:название:размер]
Default: none
Context: server, mail
```

Задаёт тип и размеры кэшей для хранения параметров сессий. Тип кэша может быть следующим:

**`off`**  
  жёсткое запрещение использования кэша сессий:
nginx явно сообщает клиенту, что сессии не могут использоваться повторно.

**`none`**  
  мягкое запрещение использования кэша сессий:
nginx сообщает клиенту, что сессии могут использоваться повторно, но
на самом деле не хранит параметры сессии в кэше.

**`builtin`**  
  встроенный в OpenSSL кэш, используется в рамках только одного рабочего процесса.
Размер кэша задаётся в сессиях.
Если размер не задан, то он равен 20480 сессиям.
Использование встроенного кэша может вести к фрагментации памяти.

**`shared`**  
  кэш, разделяемый между всеми рабочими процессами.
Размер кэша задаётся в байтах, в 1 мегабайт может поместиться
около 4000 сессий.
У каждого разделяемого кэша должно быть произвольное название.
Кэш с одинаковым названием может использоваться в нескольких
серверах.
Также он используется для автоматического создания, хранения и
периодического обновления ключей TLS session tickets (1.23.2),
если они не указаны явно
с помощью директивы [ssl_session_ticket_key](#ssl_session_ticket_key) .

Можно использовать одновременно оба типа кэша, например:

```
ssl_session_cache builtin:1000 shared:SSL:10m;
```

однако использование только разделяемого кэша без встроенного должно быть более эффективным.

## ssl_session_ticket_key

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 1.5.7.*

Задаёт `файл` с секретным ключом, применяемым при шифровании и расшифровании TLS session tickets. Директива необходима, если один и тот же ключ нужно использовать на нескольких серверах. По умолчанию используется случайно сгенерированный ключ.

Если указано несколько ключей, то только первый ключ используется для шифрования TLS session tickets. Это позволяет настроить ротацию ключей, например:

```
ssl_session_ticket_key current.key;
ssl_session_ticket_key previous.key;
```

`Файл` должен содержать 80 или 48 байт случайных данных и может быть создан следующей командой:

```
openssl rand 80 > ticket.key
```

В зависимости от размера файла для шифрования будет использоваться либо AES256 (для 80-байтных ключей, 1.11.8), либо AES128 (для 48-байтных ключей).

## ssl_session_tickets

```
Syntax:  on | off
Default: on
Context: server, mail
```

*This directive appeared in version 1.5.9.*

Разрешает или запрещает возобновление сессий при помощи [TLS session tickets](https://datatracker.ietf.org/doc/html/rfc5077) .

## ssl_session_timeout

```
Syntax:  время
Default: 5m
Context: server, mail
```

Задаёт время, в течение которого клиент может повторно использовать параметры сессии.

## ssl_trusted_certificate

```
Syntax:  файл
Default: 
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Задаёт `файл` с доверенными сертификатами CA в формате PEM, которые используются для [проверки](#ssl_verify_client) клиентских сертификатов.

В отличие от [ssl_client_certificate](#ssl_client_certificate) , список этих сертификатов не будет отправляться клиентам.

## ssl_verify_client

```
Syntax:  on | off | optional | optional_no_ca
Default: off
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Разрешает проверку клиентских сертификатов. Результат проверки передаётся в заголовке `Auth-SSL-Verify` в запросе [аутентификации](ngx_mail_auth_http_module.xml#auth_http) .

Параметр `optional` запрашивает клиентский сертификат, и если сертификат был предоставлен, проверяет его.

Параметр `optional_no_ca` запрашивает сертификат клиента, но не требует, чтобы он был подписан доверенным сертификатом CA. Это предназначено для случаев, когда фактическая проверка сертификата осуществляется внешним по отношению к nginx’у сервисом. Содержимое сертификата доступно в запросах, [посылаемых](ngx_mail_auth_http_module.xml#auth_http_pass_client_cert) на сервер аутентификации.

## ssl_verify_depth

```
Syntax:  число
Default: 1
Context: server, mail
```

*This directive appeared in version 1.7.11.*

Устанавливает глубину проверки в цепочке клиентских сертификатов.

## starttls

```
Syntax:  on | off | only
Default: off
Context: server, mail
```

**`on`**  
  разрешить использование команд `STLS` для POP3
и `STARTTLS` для IMAP и SMTP;

**`off`**  
  запретить использование команд `STLS` и `STARTTLS` ;

**`only`**  
  требовать предварительного перехода на TLS.

