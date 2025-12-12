# Module ngx_http_hls_module

**Revision:** 7  
**Language:** ru

Модуль `ngx_http_hls_module` обеспечивает серверную поддержку протокола HTTP Live Streaming (HLS) для медиафайлов в формате MP4 и MOV. Такие файлы обычно имеют расширения `.mp4` , `.m4v` , `.m4a` , `.mov` или `.qt` . Модуль поддерживает видеокодек H.264, а также аудиокодеки AAC и MP3.

Для каждого медиафайла поддерживается два URI:

- URI плейлиста, имеющий расширение “ `.m3u8` ”.
URI может принимать необязательные аргументы:
  - “ `start` ” и “ `end` ”
задают границы плейлиста в секундах (1.9.0).
  - “ `offset` ” сдвигает первоначальную позицию воспроизведения
на указанное время в секундах (1.9.0).
Положительное значение задаёт временной сдвиг с начала плейлиста.
Отрицательное значение задаёт временной сдвиг с конца последнего фрагмента
в плейлисте.
  - “ `len` ” задаёт длину фрагмента в секундах.
  
- URI фрагмента, имеющий расширение “ `.ts` ”.
URI может принимать необязательные аргументы:
  - “ `start` ” и “ `end` ”
задают границы фрагмента в секундах.
  

> **Note:** Модуль доступен как часть [коммерческой подписки](https://nginx.com/products/) .

# Пример конфигурации {#example}

```
location / {
    hls;
    hls_fragment            5s;
    hls_buffers             10 10m;
    hls_mp4_buffer_size     1m;
    hls_mp4_max_buffer_size 5m;
    root /var/video/;
}
```

В такой конфигурации для файла “ `/var/video/test.mp4` ” будут поддерживаться следующие URI:

```
http://hls.example.com/test.mp4.m3u8?offset=1.000&start=1.000&end=2.200
http://hls.example.com/test.mp4.m3u8?len=8.000
http://hls.example.com/test.mp4.ts?start=1.000&end=2.200
```

# Директивы {#directives}

## hls

```
Syntax:  
Default: 
Context: location
```

Включает HLS-поток во вложенном location.

## hls_buffers

```
Syntax:  число размер
Default: 8 2m
Context: location, http, server
```

Задаёт максимальное `число` и `размер` буферов, которые используются для чтения и записи блоков данных.

## hls_forward_args

```
Syntax:  on | off
Default: off
Context: location, http, server
```

*This directive appeared in version 1.5.12.*

Добавляет аргументы из запроса плейлиста в URI фрагментов. Это может быть необходимо для авторизации клиента во время запроса фрагментов, а также для защиты HLS-потока с помощью модуля [ngx_http_secure_link_module](ngx_http_secure_link_module.xml) .

Например, если клиент запрашивает плейлист `http://example.com/hls/test.mp4.m3u8?a=1&b=2` , то аргументы `a=1` и `b=2` будут добавлены в URI фрагментов после аргументов `start` и `end` :

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:15
#EXT-X-PLAYLIST-TYPE:VOD

#EXTINF:9.333,
test.mp4.ts?start=0.000&end=9.333&a=1&b=2
#EXTINF:7.167,
test.mp4.ts?start=9.333&end=16.500&a=1&b=2
#EXTINF:5.416,
test.mp4.ts?start=16.500&end=21.916&a=1&b=2
#EXTINF:5.500,
test.mp4.ts?start=21.916&end=27.416&a=1&b=2
#EXTINF:15.167,
test.mp4.ts?start=27.416&end=42.583&a=1&b=2
#EXTINF:9.626,
test.mp4.ts?start=42.583&end=52.209&a=1&b=2

#EXT-X-ENDLIST
```

Если HLS-поток защищён с помощью модуля [ngx_http_secure_link_module](ngx_http_secure_link_module.xml) , переменную `$uri` не следует использовать в выражении [secure_link_md5](ngx_http_secure_link_module.xml#secure_link_md5) , так как это приведёт к ошибкам при запросах к фрагментам. Вместо `$uri` следует использовать [базовую часть URI](ngx_http_map_module.xml#map) ( `$hls_uri` в примере):

```
http {
    ...

    map $uri $hls_uri {
        ~^(?<base_uri>.*).m3u8$ $base_uri;
        ~^(?<base_uri>.*).ts$   $base_uri;
        default                 $uri;
    }

    server {
        ...

        location /hls/ {
            hls;
            hls_forward_args on;

            alias /var/videos/;

            secure_link $arg_md5,$arg_expires;
            secure_link_md5 "$secure_link_expires$hls_uri$remote_addr secret";

            if ($secure_link = "") {
                return 403;
            }

            if ($secure_link = "0") {
                return 410;
            }
        }
    }
}
```

## hls_fragment

```
Syntax:  время
Default: 5s
Context: location, http, server
```

Задаёт длину фрагмента по умолчанию для всех URI в плейлисте, запрошенных без аргумента “ `len` ”.

## hls_mp4_buffer_size

```
Syntax:  размер
Default: 512k
Context: location, http, server
```

Задаёт начальный `размер` буфера, используемого для обработки MP4- и MOV-файлов.

## hls_mp4_max_buffer_size

```
Syntax:  размер
Default: 10m
Context: location, http, server
```

В ходе обработки метаданных может понадобиться буфер большего размера. Его `размер` не может превышать указанного, иначе nginx вернёт серверную ошибку 500 Internal Server Error и запишет в лог следующее сообщение:

```
"/some/movie/file.mp4" mp4 moov atom is too large:
12583268, you may want to increase hls_mp4_max_buffer_size
```

