# Модуль ngx_http_ssl_module

**Revision:** 73  
**Language:** ru

Модуль `ngx_http_ssl_module` обеспечивает работу по протоколу HTTPS.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_ssl_module` .

> **Note:** Для сборки и работы этого модуля нужна библиотека [OpenSSL](http://www.openssl.org) .

# Пример конфигурации {#example}

Для уменьшения загрузки процессора рекомендуется

- установить число [рабочих процессов](../ngx_core_module.xml#worker_processes) равным числу процессоров,
- разрешить [keep-alive](ngx_http_core_module.xml#keepalive_timeout) соединения,
- включить [разделяемый](#ssl_session_cache_shared) кэш сессий,
- выключить [встроенный](#ssl_session_cache_builtin) кэш сессий
- и, возможно, увеличить [время жизни](#ssl_session_timeout) сессии
(по умолчанию 5 минут):

```
worker_processes auto;

http {

    ...

    server {
        listen              443 ssl;
        keepalive_timeout   70;

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
Syntax:  ssl on | off;
Default: off
Context: server, http
```

Эта директива устарела в версии 1.15.0 и была удалена в версии 1.25.1. Вместо неё следует использовать параметр `ssl` директивы [listen](ngx_http_core_module.xml#listen) .

## ssl_buffer_size

```
Syntax:  ssl_buffer_size size;
Default: 16k
Context: server, http
```

*This directive appeared in version 1.5.9.*

Задаёт размер буфера, используемого при отправке данных.

По умолчанию размер буфера равен 16k, что соответствует минимальным накладным расходам при передаче больших ответов. С целью минимизации времени получения начала ответа (Time To First Byte) может быть полезно использовать меньшие значения, например:

```
ssl_buffer_size 4k;
```

## ssl_certificate

```
Syntax:  ssl_certificate файл;
Default: 
Context: server, http
```

Указывает `файл` с сертификатом в формате PEM для данного виртуального сервера. Если вместе с основным сертификатом нужно указать промежуточные, то они должны находиться в этом же файле в следующем порядке: сначала основной сертификат, а затем промежуточные. В этом же файле может находиться секретный ключ в формате PEM.

Начиная с версии 1.11.0 эта директива может быть указана несколько раз для загрузки сертификатов разных типов, например RSA и ECDSA:

```
server {
    listen              443 ssl;
    server_name         example.com;

    ssl_certificate     example.com.rsa.crt;
    ssl_certificate_key example.com.rsa.key;

    ssl_certificate     example.com.ecdsa.crt;
    ssl_certificate_key example.com.ecdsa.key;

    ...
}
```

> **Note:** Возможность задавать отдельные [цепочки
сертификатов](configuring_https_servers.xml#chains) для разных сертификатов есть только в OpenSSL 1.0.2 и выше.
Для более старых версий следует указывать только одну цепочку сертификатов.

Начиная с версии 1.15.9 в имени файла можно использовать переменные при использовании OpenSSL 1.0.2 и выше:

```
ssl_certificate     $ssl_server_name.crt;
ssl_certificate_key $ssl_server_name.key;
```

Однако нужно учитывать, что при использовании переменных сертификат загружается при каждой операции SSL handshake, что может отрицательно влиять на производительность.

Вместо `файла` можно указать значение `data` : `$переменная` (1.15.10), при котором сертификат загружается из переменной без использования промежуточных файлов. При этом следует учитывать, что ненадлежащее использование подобного синтаксиса может быть небезопасно, например данные секретного ключа могут попасть в [лог ошибок](../ngx_core_module.xml#error_log) .

Нужно иметь в виду, что из-за ограничения протокола SSL/TLS для максимальной совместимости с клиентами, которые не используют [SNI](http://en.wikipedia.org/wiki/Server_Name_Indication) , виртуальные серверы с разными сертификатами должны слушать на [разных IP-адресах](configuring_https_servers.xml#name_based_https_servers) .

## ssl_certificate_cache

```
Syntax:  ssl_certificate_cache max=N [inactive=время] [valid=время];
Default: off
Context: server, http
```

*This directive appeared in version 1.27.4.*

Задаёт кэш, в котором могут храниться [SSL-сертификаты](#ssl_certificate) и [секретные ключи](#ssl_certificate_key) , полученные из [переменных](#ssl_certificate_key_variables) .

У директивы есть следующие параметры:

**`max`**  
  задаёт максимальное число элементов в кэше;
при переполнении кэша удаляются наименее востребованные элементы (LRU);

**`inactive`**  
  задаёт время, после которого элемент кэша удаляется,
если к нему не было обращений в течение этого времени;
по умолчанию 10 секунд;

**`valid`**  
  задает время, в течение которого
элемент кэша считается действительным
и может быть повторно использован,
по умолчанию 60 секунд.
По завершении этого времени сертификат будет обновлён или повторно проверен;

**`off`**  
  запрещает кэш.

Пример:

```
ssl_certificate       $ssl_server_name.crt;
ssl_certificate_key   $ssl_server_name.key;
ssl_certificate_cache max=1000 inactive=20s valid=1m;
```

## ssl_certificate_compression

```
Syntax:  ssl_certificate_compression on | off;
Default: off
Context: server, http
```

*This directive appeared in version 1.29.1.*

Разрешает [сжатие](https://datatracker.ietf.org/doc/html/rfc8879) серверных сертификатов при использовании TLS 1.3.

> **Note:** Директива поддерживается при использовании OpenSSL 3.2 и выше;
список поддерживаемых алгоритмов сжатия обеспечивается библиотекой.

> **Note:** Директива поддерживается при использовании BoringSSL;
список поддерживаемых алгоритмов сжатия включает `zlib` (1.29.3).

## ssl_certificate_key

```
Syntax:  ssl_certificate_key файл;
Default: 
Context: server, http
```

Указывает `файл` с секретным ключом в формате PEM для данного виртуального сервера.

Вместо `файла` можно указать значение `engine` : `имя` : `id` (1.7.9), которое загружает ключ с указанным `id` из OpenSSL engine с заданным `именем` .

Вместо `файла` можно указать значение `store` : `схема` : `id` (1.29.0), которое используется для загрузки ключа с указанным `id` и зарегистрированной провайдером OpenSSL `схемой` URI, такой как [`pkcs11`](https://datatracker.ietf.org/doc/html/rfc7512) .

Вместо `файла` можно указать значение `data` : `$переменная` (1.15.10), при котором секретный ключ загружается из переменной без использования промежуточных файлов. При этом следует учитывать, что ненадлежащее использование подобного синтаксиса может быть небезопасно, например данные секретного ключа могут попасть в [лог ошибок](../ngx_core_module.xml#error_log) .

Начиная с версии 1.15.9 в имени файла можно использовать переменные при использовании OpenSSL 1.0.2 и выше.

## ssl_ciphers

```
Syntax:  ssl_ciphers шифры;
Default: HIGH:!aNULL:!MD5
Context: server, http
```

Описывает разрешённые шифры. Шифры задаются в формате, поддерживаемом библиотекой OpenSSL, например:

```
ssl_ciphers ALL:!aNULL:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
```

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

> **Note:** В предыдущих версиях nginx по умолчанию использовались [другие](configuring_https_servers.xml#compatibility) шифры.

## ssl_client_certificate

```
Syntax:  ssl_client_certificate файл;
Default: 
Context: server, http
```

Указывает `файл` с доверенными сертификатами CA в формате PEM, которые используются для [проверки](#ssl_verify_client) клиентских сертификатов и ответов OCSP, если включён [ssl_stapling](#ssl_stapling) .

Список сертификатов будет отправляться клиентам. Если это нежелательно, можно воспользоваться директивой [ssl_trusted_certificate](#ssl_trusted_certificate) .

## ssl_conf_command

```
Syntax:  ssl_conf_command имя значение;
Default: 
Context: server, http
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
Syntax:  ssl_crl файл;
Default: 
Context: server, http
```

*This directive appeared in version 0.8.7.*

Указывает `файл` с отозванными сертификатами (CRL) в формате PEM, используемыми для [проверки](#ssl_verify_client) клиентских сертификатов.

## ssl_dhparam

```
Syntax:  ssl_dhparam файл;
Default: 
Context: server, http
```

*This directive appeared in version 0.7.2.*

Указывает `файл` с параметрами для DHE-шифров.

По умолчанию параметры не заданы, и соответственно DHE-шифры не будут использоваться.

> **Note:** До версии 1.11.0 по умолчанию использовались встроенные параметры.

## ssl_early_data

```
Syntax:  ssl_early_data on | off;
Default: off
Context: server, http
```

*This directive appeared in version 1.15.3.*

Разрешает или запрещает TLS 1.3 [early data](https://datatracker.ietf.org/doc/html/rfc8446#section-2.3) .

> **Note:** Директива поддерживается при использовании OpenSSL 1.1.1 и выше (1.15.4) или [BoringSSL](https://boringssl.googlesource.com/boringssl/) .

> **Note:** Запросы, отправленные внутри early data, могут быть подвержены [атакам повторного воспроизведения](https://datatracker.ietf.org/doc/html/rfc8470) (replay).
Для защиты от подобных атак на уровне приложения
необходимо использовать
переменную [$ssl_early_data](#var_ssl_early_data) .

```
proxy_set_header Early-Data $ssl_early_data;
```

> **Note:** Встроенная в OpenSSL защита от replay-атак отключена,
поскольку это препятствует возобновлению сессий.
При необходимости её можно включить обратно.

```
ssl_conf_command Options AntiReplay;
```

## ssl_ecdh_curve

```
Syntax:  ssl_ecdh_curve кривая;
Default: auto
Context: server, http
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

## ssl_ech_file

```
Syntax:  ssl_ech_file file;
Default: 
Context: server, http
```

*This directive appeared in version 1.29.4.*

Задаёт `файл` с конфигурацией Encrypted ClientHello ( `ECHConfig` ) в формате [PEM](https://datatracker.ietf.org/doc/draft-farrell-tls-pemesni/) , используемой для включения TLS 1.3 [ECH](https://datatracker.ietf.org/doc/html/draft-ietf-tls-esni) в shared-режиме.

> **Note:** В настоящее время директива поддерживается только при использовании [ветки
разработки ECH](https://github.com/openssl/openssl/tree/feature/ech) OpenSSL.

## ssl_key_log

```
Syntax:  ssl_key_log путь;
Default: 
Context: server, http
```

*This directive appeared in version 1.27.2.*

Включает логирование SSL-ключей клиентских соединений и указывает путь к лог-файлу ключей. Ключи записываются в формате [SSLKEYLOGFILE](https://datatracker.ietf.org/doc/html/draft-ietf-tls-keylogfile) совместимом с Wireshark.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## ssl_ocsp

```
Syntax:  ssl_ocsp on | off | leaf;
Default: off
Context: server, http
```

*This directive appeared in version 1.19.0.*

Включает проверку OCSP для цепочки клиентских сертификатов. Параметр `leaf` включает проверку только клиентского сертификата.

Для работы проверки OCSP необходимо дополнительно установить значение директивы [ssl_verify_client](#ssl_verify_client) в `on` или `optional` .

Для преобразования имени хоста OCSP responder’а в адрес необходимо дополнительно задать директиву [resolver](ngx_http_core_module.xml#resolver) .

Пример:

```
ssl_verify_client on;
ssl_ocsp          on;
resolver          192.0.2.1;
```

## ssl_ocsp_cache

```
Syntax:  ssl_ocsp_cache off | [shared:имя:размер];
Default: off
Context: server, http
```

*This directive appeared in version 1.19.0.*

Задаёт `имя` и `размер` кэша, который хранит статус клиентских сертификатов для проверки OCSP-ответов. Кэш разделяется между всеми рабочими процессами. Кэш с одинаковым названием может использоваться в нескольких виртуальных серверах.

Параметр `off` запрещает использование кэша.

## ssl_ocsp_responder

```
Syntax:  ssl_ocsp_responder url;
Default: 
Context: server, http
```

*This directive appeared in version 1.19.0.*

Переопределяет URL OCSP responder’а, указанный в расширении сертификата “ [Authority Information Access](https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.1) ” для [проверки](#ssl_ocsp) клиентских сертификатов.

Поддерживаются только “ `http://` ” OCSP responder’ы:

```
ssl_ocsp_responder http://ocsp.example.com/;
```

## ssl_password_file

```
Syntax:  ssl_password_file файл;
Default: 
Context: server, http
```

*This directive appeared in version 1.7.3.*

Задаёт `файл` с паролями от [секретных ключей](#ssl_certificate_key) , где каждый пароль указан на отдельной строке. Пароли применяются по очереди в момент загрузки ключа.

Пример:

```
http {
    ssl_password_file /etc/keys/global.pass;
    ...

    server {
        server_name www1.example.com;
        ssl_certificate_key /etc/keys/first.key;
    }

    server {
        server_name www2.example.com;

        # вместо файла можно указать именованный канал
        ssl_password_file /etc/keys/fifo;
        ssl_certificate_key /etc/keys/second.key;
    }
}
```

## ssl_prefer_server_ciphers

```
Syntax:  ssl_prefer_server_ciphers on | off;
Default: off
Context: server, http
```

Указывает, чтобы при использовании протоколов SSLv3 и TLS серверные шифры были более приоритетны, чем клиентские.

## ssl_protocols

```
Syntax:  ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3];
Default: TLSv1.2 TLSv1.3
Context: server, http
```

Разрешает указанные протоколы.

Если директива указана на уровне [server](ngx_http_core_module.xml#server) , то может использоваться значение из сервера по умолчанию. Подробнее см. в разделе “ [Выбор виртуального сервера](server_names.xml#virtual_server_selection) ”.

> **Note:** Параметры `TLSv1.1` и `TLSv1.2` (1.1.13, 1.0.12) работают только при использовании OpenSSL 1.0.1 и выше.

> **Note:** Параметр `TLSv1.3` (1.13.0) работает только
при использовании OpenSSL 1.1.1 и выше.

> **Note:** Параметр `TLSv1.3` используется по умолчанию
начиная с 1.23.4.

## ssl_reject_handshake

```
Syntax:  ssl_reject_handshake on | off;
Default: off
Context: server, http
```

*This directive appeared in version 1.19.4.*

Если разрешено, то операции SSL handshake в блоке [server](ngx_http_core_module.xml#server) будут отклонены.

Например в этой конфигурации отклоняются все операции SSL handshake с именем сервера, отличным от `example.com` :

```
server {
    listen               443 ssl default_server;
    ssl_reject_handshake on;
}

server {
    listen              443 ssl;
    server_name         example.com;
    ssl_certificate     example.com.crt;
    ssl_certificate_key example.com.key;
}
```

## ssl_session_cache

```
Syntax:  ssl_session_cache off | none | [builtin[:размер]] [shared:название:размер];
Default: none
Context: server, http
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
виртуальных серверах.
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
Syntax:  ssl_session_ticket_key файл;
Default: 
Context: server, http
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
Syntax:  ssl_session_tickets on | off;
Default: on
Context: server, http
```

*This directive appeared in version 1.5.9.*

Разрешает или запрещает возобновление сессий при помощи [TLS session tickets](https://datatracker.ietf.org/doc/html/rfc5077) .

## ssl_session_timeout

```
Syntax:  ssl_session_timeout время;
Default: 5m
Context: server, http
```

Задаёт время, в течение которого клиент может повторно использовать параметры сессии.

## ssl_stapling

```
Syntax:  ssl_stapling on | off;
Default: off
Context: server, http
```

*This directive appeared in version 1.3.7.*

Разрешает или запрещает [прикрепление OCSP-ответов](https://datatracker.ietf.org/doc/html/rfc6066#section-8) сервером. Пример:

```
ssl_stapling on;
resolver 192.0.2.1;
```

Для работы OCSP stapling’а должен быть известен сертификат издателя сертификата сервера. Если в заданном директивой [ssl_certificate](#ssl_certificate) файле не содержится промежуточных сертификатов, то сертификат издателя сертификата сервера следует поместить в файл, заданный директивой [ssl_trusted_certificate](#ssl_trusted_certificate) .

Для преобразования имени хоста OCSP responder’а в адрес необходимо дополнительно задать директиву [resolver](ngx_http_core_module.xml#resolver) .

## ssl_stapling_file

```
Syntax:  ssl_stapling_file файл;
Default: 
Context: server, http
```

*This directive appeared in version 1.3.7.*

Если задано, то вместо опроса OCSP responder’а, указанного в сертификате сервера, ответ берётся из указанного `файла` .

Ответ должен быть в формате DER и может быть сгенерирован командой “ `openssl ocsp` ”.

## ssl_stapling_responder

```
Syntax:  ssl_stapling_responder url;
Default: 
Context: server, http
```

*This directive appeared in version 1.3.7.*

Переопределяет URL OCSP responder’а, указанный в расширении сертификата “ [Authority Information Access](https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.1) ”.

Поддерживаются только “ `http://` ” OCSP responder’ы:

```
ssl_stapling_responder http://ocsp.example.com/;
```

## ssl_stapling_verify

```
Syntax:  ssl_stapling_verify on | off;
Default: off
Context: server, http
```

*This directive appeared in version 1.3.7.*

Разрешает или запрещает проверку сервером ответов OCSP.

Для работоспособности проверки сертификат издателя сертификата сервера, корневой сертификат и все промежуточные сертификаты должны быть указаны как доверенные с помощью директивы [ssl_trusted_certificate](#ssl_trusted_certificate) .

## ssl_trusted_certificate

```
Syntax:  ssl_trusted_certificate файл;
Default: 
Context: server, http
```

*This directive appeared in version 1.3.7.*

Задаёт `файл` с доверенными сертификатами CA в формате PEM, которые используются для [проверки](#ssl_verify_client) клиентских сертификатов и ответов OCSP, если включён [ssl_stapling](#ssl_stapling) .

В отличие от [ssl_client_certificate](#ssl_client_certificate) , список этих сертификатов не будет отправляться клиентам.

## ssl_verify_client

```
Syntax:  ssl_verify_client on | off | optional | optional_no_ca;
Default: off
Context: server, http
```

Разрешает проверку клиентских сертификатов. Результат проверки доступен через переменную [$ssl_client_verify](#var_ssl_client_verify) .

Параметр `optional` (0.8.7+) запрашивает клиентский сертификат, и если сертификат был предоставлен, проверяет его.

Параметр `optional_no_ca` (1.3.8, 1.2.5) запрашивает сертификат клиента, но не требует, чтобы он был подписан доверенным сертификатом CA. Это предназначено для случаев, когда фактическая проверка сертификата осуществляется внешним по отношению к nginx’у сервисом. Содержимое сертификата доступно через переменную [$ssl_client_cert](#var_ssl_client_cert) .

## ssl_verify_depth

```
Syntax:  ssl_verify_depth число;
Default: 1
Context: server, http
```

Устанавливает глубину проверки в цепочке клиентских сертификатов.

# Обработка ошибок {#errors}

Модуль `ngx_http_ssl_module` поддерживает несколько нестандартных кодов ошибок, которые можно использовать для перенаправления с помощью директивы [error_page](ngx_http_core_module.xml#error_page) :

**495**  
  при проверке клиентского сертификата произошла ошибка;

**496**  
  клиент не предоставил требуемый сертификат;

**497**  
  обычный запрос был послан на порт HTTPS.

Перенаправление делается после того, как запрос полностью разобран и доступны такие переменные, как `$request_uri` , `$uri` , `$args` и другие переменные.

# Встроенные переменные {#variables}

Модуль `ngx_http_ssl_module` поддерживает встроенные переменные:

**`$ssl_alpn_protocol`**  
  возвращает протокол, выбранный при помощи ALPN во время операции SSL handshake,
либо пустую строку (1.21.4);

**`$ssl_cipher`**  
  возвращает название используемого шифра для установленного SSL-соединения;

**`$ssl_ciphers`**  
  возвращает список шифров, поддерживаемых клиентом (1.11.7).
Известные шифры указаны по имени, неизвестные указаны в шестнадцатеричном виде,
например:

```
AES128-SHA:AES256-SHA:0x00ff
```

> **Note:** Переменная полностью поддерживается при использовании OpenSSL версии 1.0.2
и выше.
При использовании более старых версий переменная доступна
только для новых сессий и может содержать только известные шифры.

**`$ssl_client_escaped_cert`**  
  возвращает клиентский сертификат в формате PEM
(закодирован в формате urlencode) для установленного SSL-соединения (1.13.5);

**`$ssl_client_cert`**  
  возвращает клиентский сертификат в формате PEM
для установленного SSL-соединения, перед каждой строкой которого, кроме первой,
вставляется символ табуляции;
предназначена для использования в директиве [proxy_set_header](ngx_http_proxy_module.xml#proxy_set_header) ;

> **Note:** Переменная устарела, вместо неё следует использовать
переменную `$ssl_client_escaped_cert` .

**`$ssl_client_fingerprint`**  
  возвращает SHA1-отпечаток клиентского сертификата
для установленного SSL-соединения (1.7.1);

**`$ssl_client_i_dn`**  
  возвращает строку “issuer DN” клиентского сертификата
для установленного SSL-соединения согласно [RFC 2253](https://datatracker.ietf.org/doc/html/rfc2253) (1.11.6);

**`$ssl_client_i_dn_legacy`**  
  возвращает строку “issuer DN” клиентского сертификата
для установленного SSL-соединения;

> **Note:** До версии 1.11.6 переменная называлась `$ssl_client_s_dn` .

**`$ssl_client_raw_cert`**  
  возвращает клиентский сертификат в формате PEM
для установленного SSL-соединения;

**`$ssl_client_s_dn`**  
  возвращает строку “subject DN” клиентского сертификата
для установленного SSL-соединения согласно [RFC 2253](https://datatracker.ietf.org/doc/html/rfc2253) (1.11.6);

**`$ssl_client_s_dn_legacy`**  
  возвращает строку “subject DN” клиентского сертификата
для установленного SSL-соединения;

> **Note:** До версии 1.11.6 переменная называлась `$ssl_client_s_dn` .

**`$ssl_client_serial`**  
  возвращает серийный номер клиентского сертификата
для установленного SSL-соединения;

**`$ssl_client_sigalg`**  
  возвращает [алгоритм подписи](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-16) клиентского сертификата для установленного SSL-соединения (1.29.3).

> **Note:** Переменная поддерживается при использовании OpenSSL версии 3.5 и выше.
При использовании более старых версий значением переменной будет пустая строка.

> **Note:** Переменная доступна только для новых сессий.

**`$ssl_client_v_end`**  
  возвращает дату окончания срока действия клиентского сертификата (1.11.7);

**`$ssl_client_v_remain`**  
  возвращает число дней,
оставшихся до истечения срока действия клиентского сертификата (1.11.7);

**`$ssl_client_v_start`**  
  возвращает дату начала срока действия клиентского сертификата (1.11.7);

**`$ssl_client_verify`**  
  возвращает результат проверки клиентского сертификата:
“ `SUCCESS` ”, “ `FAILED:` `reason` ”
и, если сертификат не был предоставлен, “ `NONE` ”;

> **Note:** До версии 1.11.7 результат “ `FAILED` ”
не содержал строку `reason` .

**`$ssl_curve`**  
  возвращает согласованную кривую, использованную для
обмена ключами во время операции SSL handshake (1.21.5).
Известные кривые указаны по имени, неизвестные указаны в шестнадцатеричном виде,
например:

```
prime256v1
```

> **Note:** Переменная поддерживается при использовании OpenSSL версии 3.0 и выше.
При использовании более старых версий значением переменной будет пустая строка.

**`$ssl_curves`**  
  возвращает список кривых, поддерживаемых клиентом (1.11.7).
Известные кривые указаны по имени, неизвестные указаны в шестнадцатеричном виде,
например:

```
0x001d:prime256v1:secp521r1:secp384r1
```

> **Note:** Переменная поддерживается при использовании OpenSSL версии 1.0.2 и выше.
При использовании более старых версий значением переменной будет пустая строка.

> **Note:** Переменная доступна только для новых сессий.

**`$ssl_early_data`**  
  возвращает “ `1` ”, если
используется TLS 1.3 [early data](#ssl_early_data) и операция handshake не завершена, иначе “” (1.15.3).

**`$ssl_ech_outer_server_name`**  
  возвращает публичное имя сервера, запрошенное через [SNI](http://en.wikipedia.org/wiki/Server_Name_Indication) если TLS 1.3 [ECH](#ssl_ech_file) был принят,
иначе “” (1.29.4);

**`$ssl_ech_status`**  
  возвращает результат обработки TLS 1.3 [ECH](#ssl_ech_file) :
“ `FAILED` ”,
“ `BACKEND` ”,
“ `GREASE` ”,
“ `SUCCESS` ” или
“ `NOT_TRIED` ” (1.29.4);

> **Note:** В настоящее время переменная поддерживается при использовании [ветки разработки ECH](https://github.com/openssl/openssl/tree/feature/ech) и, таким образом, может измениться.
В остальных случаях значением переменной будет пустая строка.

**`$ssl_protocol`**  
  возвращает протокол установленного SSL-соединения;

**`$ssl_server_name`**  
  возвращает имя сервера, запрошенное через [SNI](http://en.wikipedia.org/wiki/Server_Name_Indication) (1.7.0);

**`$ssl_session_id`**  
  возвращает идентификатор сессии установленного SSL-соединения;

**`$ssl_session_reused`**  
  возвращает “ `r` ”, если сессия была использована повторно,
иначе “ `.` ” (1.5.11).

**`$ssl_sigalg`**  
  возвращает [алгоритм подписи](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-16) сертификата сервера для установленного SSL-соединения (1.29.3).

> **Note:** Переменная поддерживается при использовании OpenSSL версии 3.5 и выше.
При использовании более старых версий значением переменной будет пустая строка.

> **Note:** Переменная доступна только для новых сессий.

