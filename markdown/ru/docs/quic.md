# Поддержка QUIC и HTTP/3

**Revision:** 3  
**Language:** ru


Поддержка протоколов
[QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
и
[HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
доступна начиная с версии 1.25.0, она включена в
[бинарных пакетах](../linux_packages.html) для Linux.
Подробнее см. документацию к модулю
[ngx_http_v3_module](http/ngx_http_v3_module.html).

## Сборка из исходных файлов {#building}

Сборка настраивается командой `configure`.
Подробнее см. в статье [configure.html](configure.html).

Для сборки nginx с поддержкой QUIC рекомендуется библиотека
[OpenSSL](https://openssl.org) версии 3.5.1 или выше.
Иначе будет использоваться OpenSSL compatibility layer без поддержки TLS
[early data](http/ngx_http_ssl_module.xml#ssl_early_data).
Также возможно использование предварительно собранной библиотеки
[BoringSSL](https://boringssl.googlesource.com/boringssl),
[LibreSSL](https://www.libressl.org) или
[QuicTLS](https://github.com/quictls/openssl).

При конфигурации nginx с
[BoringSSL](https://boringssl.googlesource.com/boringssl)
используется следующая команда:

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../boringssl/include"
    --with-ld-opt="-L../boringssl/build -lstdc++"
```

Кроме того, можно сконфигурировать nginx с
[QuicTLS](https://github.com/quictls/openssl):

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../quictls/build/include"
    --with-ld-opt="-L../quictls/build/lib"
```

Кроме того, можно сконфигурировать nginx с
[LibreSSL](https://www.libressl.org):

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../libressl/build/include"
    --with-ld-opt="-L../libressl/build/lib"
```

После конфигурации
nginx компилируется и устанавливается с помощью
`make`.

## Советы по настройке {#configuration}

В директиве [](http/ngx_http_core_module.xml#listen)
модуля [ngx_http_core_module](http/ngx_http_core_module.html)
появился новый параметр
[quic](http/ngx_http_core_module.xml#quic),
который позволяет принимать на указанном порту QUIC-соединения.

Вместе с параметром `quic`
можно также указать параметр
[reuseport](http/ngx_http_core_module.xml#reuseport)
для правильной работы с несколькими рабочими процессами.

Чтобы [разрешить](http/ngx_http_v3_module.xml#quic_retry)
проверку адреса:

```
quic_retry on;
```


Чтобы [разрешить](http/ngx_http_ssl_module.xml#ssl_early_data)
0-RTT:

```
ssl_early_data on;
```


Чтобы [разрешить](http/ngx_http_v3_module.xml#quic_gso)
GSO (Generic Segmentation Offloading):

```
quic_gso on;
```


Чтобы [установить](http/ngx_http_v3_module.xml#quic_host_key)
host-ключ для различных токенов:

```
quic_host_key <filename>;
```

Для работы QUIC требуется версия протокла TLSv1.3, которая включена по умолчанию
в директиве [](http/ngx_http_ssl_module.xml#ssl_protocols).

По умолчанию
[GSO Linux-specific optimization](http://vger.kernel.org/lpc_net2018_talks/willemdebruijn-lpc2018-udpgso-paper-DRAFT-1.pdf)
выключена.
Включите, если настроен соответствующий сетевой интерфейс,
поддерживающий GSO.

## Устранение неполадок {#troubleshooting }

Приблизительные шаги при обнаружении проблемы:

- Убедитесь, что nginx собран с правильной SSL-библиотекой.
- Убедитесь, что nginx использует правильную SSL-библиотеку в runtime
(`nginx -V` покажет что именно используется в данный момент).
- Убедитесь, что клиент действительно присылает запросы через QUIC.
Рекомендуется начать с простого консольного клиента, например
[ngtcp2](https://nghttp2.org/ngtcp2),
чтобы убедиться, что сервер настроен правильно, и затем попробовать
в браузерах, так как браузеры могут быть требовательны к сертификатам.
- Соберите nginx с поддержкой [отладочного лога](debugging_log.html)
и проверьте отладочный лог.
В нём должны содержаться все детали соединения и причины ошибок.
Соответствующие сообщения начинаются с префикса “`quic`”
и могут быть по нему отфильтрованы.
- Для детального исследования можно включить дополнительную отладку
при помощи следующих макросов:
`NGX_QUIC_DEBUG_PACKETS`,
`NGX_QUIC_DEBUG_FRAMES`,
`NGX_QUIC_DEBUG_ALLOC`,
`NGX_QUIC_DEBUG_CRYPTO`.



./configure
    --with-http_v3_module
    --with-debug
    --with-cc-opt="-DNGX_QUIC_DEBUG_PACKETS -DNGX_QUIC_DEBUG_CRYPTO"
