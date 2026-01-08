# Модуль ngx_http_v3_module

**Revision:** 3  
**Language:** ru

Модуль `ngx_http_v3_module` (1.25.0) обеспечивает экспериментальную поддержку [HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114) .

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_v3_module` .

> **Note:** Для сборки и работы этого модуля нужна библиотека [OpenSSL](http://www.openssl.org) версии 1.1.1 или выше.

> **Note:** Для поддержки 0-RTT нужна библиотека [OpenSSL](http://www.openssl.org) версии 3.5.1 или выше.
Также возможно использование библиотек [BoringSSL](https://boringssl.googlesource.com/boringssl) , [LibreSSL](https://www.libressl.org) , [QuicTLS](https://github.com/quictls/openssl) .

# Известные проблемы {#issues}

Модуль экспериментальный, поэтому возможно всё.

До версии 1.29.1 поддержка 0-RTT не могла быть разрешена при использовании OpenSSL независимо от значения директивы [ssl_early_data](ngx_http_ssl_module.xml#ssl_early_data) .

Сборка модуля не поддерживается на платформе Win32.

# Пример конфигурации {#example}

```
http {
    log_format quic '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" "$http3"';

    access_log logs/access.log quic;

    server {
        # для лучшей совместимости рекомендуется
        # использовать одинаковый порт для http/3 и https
        listen 8443 quic reuseport;
        listen 8443 ssl;

        ssl_certificate     certs/example.com.crt;
        ssl_certificate_key certs/example.com.key;

        location / {
            # используется для объявления о поддержке http/3
            add_header Alt-Svc 'h3=":8443"; ma=86400';
        }
    }
}
```

# Директивы {#directives}

## http3

```
Syntax:  http3 on | off;
Default: on
Context: server, http
```

Разрешает согласование протокола [HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114) .

## http3_hq

```
Syntax:  http3_hq on | off;
Default: off
Context: server, http
```

Разрешает согласование протокола HTTP/0.9, используемого в [функциональных тестах QUIC](https://github.com/marten-seemann/quic-interop-runner) .

## http3_max_concurrent_streams

```
Syntax:  http3_max_concurrent_streams число;
Default: 128
Context: server, http
```

Задаёт максимальное число параллельных HTTP/3-потоков в соединении.

## http3_stream_buffer_size

```
Syntax:  http3_stream_buffer_size размер;
Default: 64k
Context: server, http
```

Задаёт размер буфера, используемого для чтения и записи QUIC-потоков.

## quic_active_connection_id_limit

```
Syntax:  quic_active_connection_id_limit число;
Default: 2
Context: server, http
```

Устанавливает значение транспортного параметра QUIC `active_connection_id_limit` . Это максимальное значение ID соединений, возможное для хранения на сервере.

## quic_bpf

```
Syntax:  quic_bpf on | off;
Default: off
Context: main
```

Разрешает маршрутизацию пакетов QUIC при помощи [eBPF](https://ebpf.io/) . Если маршрутизация включена, то обеспечивается поддержка миграции QUIC-соединений.

> **Note:** Директива поддерживается только на Linux 5.7+.

## quic_gso

```
Syntax:  quic_gso on | off;
Default: off
Context: server, http
```

Разрешает отправку оптимизированного пакетного режима при помощи segmentation offloading.

> **Note:** Оптимизированная отправка поддерживается только на Linux
с поддержкой `UDP_SEGMENT` .

## quic_host_key

```
Syntax:  quic_host_key файл;
Default: 
Context: server, http
```

Задаёт `файл` с секретным ключом, применяемым при шифровании stateless reset и address validation токенов. По умолчанию создаётся случайный ключ при каждой перезагрузке. Токены, созданные при помощи старых ключей, не принимаются.

## quic_retry

```
Syntax:  quic_retry on | off;
Default: off
Context: server, http
```

Разрешает функциональность [QUIC Address Validation](https://datatracker.ietf.org/doc/html/rfc9000#name-address-validation) , в том числе отправку нового токена в `Retry` -пакете или `NEW_TOKEN` frame и валидацию токена, полученного в `Initial` -пакете.

# Встроенные переменные {#variables}

Модуль `ngx_http_v3_module` поддерживает следующие встроенные переменные:

**`$http3`**  
  согласованный идентификатор протокола:
“ `h3` ” для HTTP/3-соединений,
“ `hq` ” для hq-соединений,
либо пустая строка.

