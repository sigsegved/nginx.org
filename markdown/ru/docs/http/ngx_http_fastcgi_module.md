# Модуль ngx_http_fastcgi_module

**Revision:** 55  
**Language:** ru

Модуль `ngx_http_fastcgi_module` позволяет передавать запросы FastCGI-серверу.

# Пример конфигурации {#example}

```
location / {
    fastcgi_pass  localhost:9000;
    fastcgi_index index.php;

    fastcgi_param SCRIPT_FILENAME /home/www/scripts/php$fastcgi_script_name;
    fastcgi_param QUERY_STRING    $query_string;
    fastcgi_param REQUEST_METHOD  $request_method;
    fastcgi_param CONTENT_TYPE    $content_type;
    fastcgi_param CONTENT_LENGTH  $content_length;
}
```

# Директивы {#directives}

## fastcgi_allow_upstream

```
Syntax:  fastcgi_allow_upstream строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Задаёт условия, при которых доступ к FastCGI-серверу будет разрешён или [запрещён](#denied) . Если все значения строковых параметров непустые и не равны “0”, то доступ разрешён. Условия проверяются каждый раз перед установлением соединения с FastCGI-сервером. В значении параметров допустимо использование переменных:

```
geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;

    location / {
        fastcgi_pass           localhost:9000;
        fastcgi_allow_upstream $allow;
        ...
    }
}
```

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## fastcgi_bind

```
Syntax:  fastcgi_bind адрес [transparent] | off;
Default: 
Context: location, http, server
```

*This directive appeared in version 0.8.22.*

Задаёт локальный IP-адрес с необязательным портом (1.11.2), который будет использоваться в исходящих соединениях с FastCGI-сервером. В значении параметра допустимо использование переменных (1.3.12). Специальное значение `off` (1.3.12) отменяет действие унаследованной с предыдущего уровня конфигурации директивы `fastcgi_bind` , позволяя системе самостоятельно выбирать локальный IP-адрес и порт.

Параметр `transparent` (1.11.0) позволяет задать нелокальный IP-aдрес, который будет использоваться в исходящих соединениях с FastCGI-сервером, например, реальный IP-адрес клиента:

```
fastcgi_bind $remote_addr transparent;
```

Для работы параметра обычно требуется запустить рабочие процессы nginx с привилегиями [суперпользователя](../ngx_core_module.xml#user) . В Linux этого не требуется (1.13.8), так как если указан параметр `transparent` , то рабочие процессы наследуют capability `CAP_NET_RAW` из главного процесса. Также необходимо настроить таблицу маршрутизации ядра для перехвата сетевого трафика с FastCGI-сервера.

## fastcgi_bind_dynamic

```
Syntax:  fastcgi_bind_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Если включено, операция [bind](#fastcgi_bind) осуществляется при каждой попытке соединения.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## fastcgi_buffer_size

```
Syntax:  fastcgi_buffer_size размер;
Default: 4k|8k
Context: location, http, server
```

Задаёт `размер` буфера, в который будет читаться первая часть ответа, получаемого от FastCGI-сервера. В этой части ответа находится, как правило, небольшой заголовок ответа. По умолчанию размер одного буфера равен размеру страницы памяти. В зависимости от платформы это или 4K, или 8K, однако его можно сделать меньше.

## fastcgi_buffering

```
Syntax:  fastcgi_buffering on | off;
Default: on
Context: location, http, server
```

*This directive appeared in version 1.5.6.*

Разрешает или запрещает использовать буферизацию ответов FastCGI-сервера.

Если буферизация включена, то nginx принимает ответ FastCGI-сервера как можно быстрее, сохраняя его в буферы, заданные директивами [fastcgi_buffer_size](#fastcgi_buffer_size) и [fastcgi_buffers](#fastcgi_buffers) . Если ответ не вмещается целиком в память, то его часть может быть записана на диск во [временный файл](#fastcgi_temp_path) . Запись во временные файлы контролируется директивами [fastcgi_max_temp_file_size](#fastcgi_max_temp_file_size) и [fastcgi_temp_file_write_size](#fastcgi_temp_file_write_size) .

Если буферизация выключена, то ответ синхронно передаётся клиенту сразу же по мере его поступления. nginx не пытается считать весь ответ FastCGI-сервера. Максимальный размер данных, который nginx может принять от сервера за один раз, задаётся директивой [fastcgi_buffer_size](#fastcgi_buffer_size) .

Буферизация может быть также включена или выключена путём передачи значения “ `yes` ” или “ `no` ” в поле `X-Accel-Buffering` заголовка ответа. Эту возможность можно запретить с помощью директивы [fastcgi_ignore_headers](#fastcgi_ignore_headers) .

## fastcgi_buffers

```
Syntax:  fastcgi_buffers число размер;
Default: 8 4k|8k
Context: location, http, server
```

Задаёт `число` и `размер` буферов для одного соединения, в которые будет читаться ответ, получаемый от FastCGI-сервера. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

## fastcgi_busy_buffers_size

```
Syntax:  fastcgi_busy_buffers_size размер;
Default: 8k|16k
Context: location, http, server
```

При включённой [буферизации](#fastcgi_buffering) ответов FastCGI-сервера, ограничивает суммарный `размер` буферов, которые могут быть заняты для отправки ответа клиенту, пока ответ ещё не прочитан целиком. Оставшиеся буферы тем временем могут использоваться для чтения ответа и, при необходимости, буферизации части ответа во временный файл. По умолчанию `размер` ограничен двумя буферами, заданными директивами [fastcgi_buffer_size](#fastcgi_buffer_size) и [fastcgi_buffers](#fastcgi_buffers) .

## fastcgi_cache

```
Syntax:  fastcgi_cache зона | off;
Default: off
Context: location, http, server
```

Задаёт зону разделяемой памяти, используемой для кэширования. Одна и та же зона может использоваться в нескольких местах. В значении параметра можно использовать переменные (1.7.9). Параметр `off` запрещает кэширование, унаследованное с предыдущего уровня конфигурации.

## fastcgi_cache_background_update

```
Syntax:  fastcgi_cache_background_update on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.11.10.*

Позволяет запустить фоновый подзапрос для обновления просроченного элемента кэша, в то время как клиенту возвращается устаревший закэшированный ответ. Использование устаревшего закэшированного ответа в момент его обновления должно быть [разрешено](#fastcgi_cache_use_stale_updating) .

## fastcgi_cache_bypass

```
Syntax:  fastcgi_cache_bypass строка ...;
Default: 
Context: location, http, server
```

Задаёт условия, при которых ответ не будет браться из кэша. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то ответ не берётся из кэша:

```
fastcgi_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
fastcgi_cache_bypass $http_pragma    $http_authorization;
```

Можно использовать совместно с директивой [fastcgi_no_cache](#fastcgi_no_cache) .

## fastcgi_cache_key

```
Syntax:  fastcgi_cache_key строка;
Default: 
Context: location, http, server
```

Задаёт ключ для кэширования, например,

```
fastcgi_cache_key localhost:9000$request_uri;
```

## fastcgi_cache_lock

```
Syntax:  fastcgi_cache_lock on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

Если включено, одновременно только одному запросу будет позволено заполнить новый элемент кэша, идентифицируемый согласно директиве [fastcgi_cache_key](#fastcgi_cache_key) , передав запрос на FastCGI-сервер. Остальные запросы этого же элемента будут либо ожидать появления ответа в кэше, либо освобождения блокировки этого элемента, в течение времени, заданного директивой [fastcgi_cache_lock_timeout](#fastcgi_cache_lock_timeout) .

## fastcgi_cache_lock_age

```
Syntax:  fastcgi_cache_lock_age время;
Default: 5s
Context: location, http, server
```

*This directive appeared in version 1.7.8.*

Если последний запрос, переданный на FastCGI-сервер для заполнения нового элемента кэша, не завершился за указанное `время` , на FastCGI-сервер может быть передан ещё один запрос.

## fastcgi_cache_lock_timeout

```
Syntax:  fastcgi_cache_lock_timeout время;
Default: 5s
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

Задаёт таймаут для [fastcgi_cache_lock](#fastcgi_cache_lock) . По истечении указанного `времени` запрос будет передан на FastCGI-сервер, однако ответ не будет закэширован.

> **Note:** До версии 1.7.8 такой ответ мог быть закэширован.

## fastcgi_cache_max_range_offset

```
Syntax:  fastcgi_cache_max_range_offset число;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.11.6.*

Задаёт смещение в байтах для запросов с указанием диапазона запрашиваемых байт (byte-range requests). Если диапазон находится за указанным смещением, range-запрос будет передан на FastCGI-сервер и ответ не будет закэширован.

## fastcgi_cache_methods

```
Syntax:  fastcgi_cache_methods GET | HEAD | POST ...;
Default: GET HEAD
Context: location, http, server
```

*This directive appeared in version 0.7.59.*

Если метод запроса клиента указан в этой директиве, то ответ будет закэширован. Методы “ `GET` ” и “ `HEAD` ” всегда добавляются в список, но тем не менее рекомендуется перечислять их явно. См. также директиву [fastcgi_no_cache](#fastcgi_no_cache) .

## fastcgi_cache_min_uses

```
Syntax:  fastcgi_cache_min_uses число;
Default: 1
Context: location, http, server
```

Задаёт `число` запросов, после которого ответ будет закэширован.

## fastcgi_cache_path

```
Syntax:  fastcgi_cache_path путь [levels=уровни] [use_temp_path=on|off] keys_zone=имя:размер [inactive=время] [max_size=размер] [min_free=размер] [manager_files=число] [manager_sleep=время] [manager_threshold=время] [loader_files=число] [loader_sleep=время] [loader_threshold=время] [purger=on|off] [purger_files=число] [purger_sleep=время] [purger_threshold=время];
Default: 
Context: http
```

Задаёт путь и другие параметры кэша. Данные кэша хранятся в файлах. Ключом и именем файла в кэше является результат функции MD5 от проксированного URL. Параметр `levels` задаёт уровни иерархии кэша: можно задать от 1 до 3 уровней, на каждом уровне допускаются значения 1 или 2. Например, при использовании

```
fastcgi_cache_path /data/nginx/cache levels=1:2 keys_zone=one:10m;
```

имена файлов в кэше будут такого вида:

```
/data/nginx/cache/c/29/b7f54b2df7773722d382f4809d65029c
```

Кэшируемый ответ сначала записывается во временный файл, а потом этот файл переименовывается. Начиная с версии 0.8.9 временные файлы и кэш могут располагаться на разных файловых системах. Однако нужно учитывать, что в этом случае вместо дешёвой операции переименовывания в пределах одной файловой системы файл копируется с одной файловой системы на другую. Поэтому лучше, если кэш будет находиться на той же файловой системе, что и каталог с временными файлами. Какой из каталогов будет использоваться для временных файлов определяется параметром `use_temp_path` (1.7.10). Если параметр не задан или установлен в значение “ `on` ”, то будет использоваться каталог, задаваемый директивой [fastcgi_temp_path](#fastcgi_temp_path) для данного location. Если параметр установлен в значение “ `off` ”, то временные файлы будут располагаться непосредственно в каталоге кэша.

Кроме того, все активные ключи и информация о данных хранятся в зоне разделяемой памяти, `имя` и `размер` которой задаются параметром `keys_zone` . Зоны размером в 1 мегабайт достаточно для хранения около 8 тысяч ключей.

> **Note:** Как часть [коммерческой подписки](https://nginx.com/products/) в зоне разделяемой памяти также хранится расширенная [информация](ngx_http_api_module.xml#http_caches_) о кэше,
поэтому для хранения аналогичного количества ключей необходимо указывать
больший размер зоны.
Например
зоны размером в 1 мегабайт достаточно для хранения около 4 тысяч ключей.

Если к данным кэша не обращаются в течение времени, заданного параметром `inactive` , то данные удаляются, независимо от их свежести. По умолчанию `inactive` равен 10 минутам.

Специальный процесс “cache manager” следит за максимальным размером кэша, заданным параметром `max_size` , а также за минимальным объёмом свободного места на файловой системе с кэшем, заданным параметром `min_free` (1.19.1). При превышении максимального размера кэша или недостаточном объёме свободного места процесс удаляет наименее востребованные данные. Удаление данных происходит итерациями, настраиваемыми параметрами (1.11.5) `manager_files` , `manager_threshold` и `manager_sleep` . За одну итерацию загружается не более `manager_files` элементов (по умолчанию 100). Время работы одной итерации ограничено параметром `manager_threshold` (по умолчанию 200 миллисекунд). Между итерациями делается пауза на время, заданное параметром `manager_sleep` (по умолчанию 50 миллисекунд).

Через минуту после старта активируется специальный процесс “cache loader”, который загружает в зону кэша информацию о ранее закэшированных данных, хранящихся на файловой системе. Загрузка также происходит итерациями. За одну итерацию загружается не более `loader_files` элементов (по умолчанию 100). Кроме того, время работы одной итерации ограничено параметром `loader_threshold` (по умолчанию 200 миллисекунд). Между итерациями делается пауза на время, заданное параметром `loader_sleep` (по умолчанию 50 миллисекунд).

Кроме того, следующие параметры доступны как часть [коммерческой подписки](https://nginx.com/products/) :

**`purger` = `on` | `off`**  
  Указывает, будут ли записи в кэше, соответствующие [маске](#fastcgi_cache_purge) ,
удалены с диска при помощи процесса “cache purger” (1.7.12).
Установка параметра в значение `on` (по умолчанию `off` )
активирует процесс “cache purger”, который
проходит по всем записям в кэше
и удаляет записи, соответствующие этой маске.

**`purger_files` = `число`**  
  Задаёт число элементов, которые будут сканироваться за одну итерацию (1.7.12).
По умолчанию `purger_files` равен 10.

**`purger_threshold` = `время`**  
  Задаёт продолжительность одной итерации (1.7.12).
По умолчанию `purger_threshold` равен 50 миллисекундам.

**`purger_sleep` = `время`**  
  Задаёт паузу между итерациями (1.7.12).
По умолчанию `purger_sleep` равен 50 миллисекундам.

> **Note:** В версиях 1.7.3, 1.7.7 и 1.11.10 формат заголовка кэша был изменён.
При обновлении на более новую версию nginx
ранее закэшированные ответы будут считаться недействительными.

## fastcgi_cache_purge

```
Syntax:  fastcgi_cache_purge строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.5.7.*

Задаёт условия, при которых запрос будет считаться запросом на очистку кэша. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то запись в кэше с соответствующим [ключом кэширования](#fastcgi_cache_key) удаляется. В результате успешной операции возвращается ответ с кодом 204 No Content .

Если [ключ кэширования](#fastcgi_cache_key) запроса на очистку заканчивается звёздочкой (“ `*` ”), то все записи в кэше, соответствующие этой маске, будут удалены из кэша. Тем не менее, эти записи будут оставаться на диске или до момента удаления из-за [отсутствия обращения к данным](#fastcgi_cache_path) , или до обработки их процессом “ [cache purger](#purger) ” (1.7.12), или до попытки клиента получить к ним доступ.

Пример конфигурации:

```
fastcgi_cache_path /data/nginx/cache keys_zone=cache_zone:10m;

map $request_method $purge_method {
    PURGE   1;
    default 0;
}

server {
    ...
    location / {
        fastcgi_pass        http://backend;
        fastcgi_cache       cache_zone;
        fastcgi_cache_key   $uri;
        fastcgi_cache_purge $purge_method;
    }
}
```

> **Note:** Функциональность доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## fastcgi_cache_revalidate

```
Syntax:  fastcgi_cache_revalidate on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.5.7.*

Разрешает ревалидацию просроченных элементов кэша при помощи условных запросов с полями заголовка `If-Modified-Since` и `If-None-Match` .

## fastcgi_cache_use_stale

```
Syntax:  fastcgi_cache_use_stale error | timeout | invalid_header | updating | http_500 | http_503 | http_403 | http_404 | http_429 | off ...;
Default: off
Context: location, http, server
```

Определяет, в каких случаях можно использовать устаревший закэшированный ответ. Параметры директивы совпадают с параметрами директивы [fastcgi_next_upstream](#fastcgi_next_upstream) .

Параметр `error` также позволяет использовать устаревший закэшированный ответ при невозможности выбора FastCGI-сервера для обработки запроса.

Кроме того, дополнительный параметр `updating` разрешает использовать устаревший закэшированный ответ, если на данный момент он уже обновляется. Это позволяет минимизировать число обращений к FastCGI-серверам при обновлении закэшированных данных.

Использование устаревшего закэшированного ответа может также быть разрешено непосредственно в заголовке ответа на определённое количество секунд после того, как ответ устарел (1.11.10). Такой способ менее приоритетен, чем задание параметров директивы.

- Расширение
“ [stale-while-revalidate](https://datatracker.ietf.org/doc/html/rfc5861#section-3) ”
поля заголовка `Cache-Control` разрешает
использовать устаревший закэшированный ответ,
если на данный момент он уже обновляется.
- Расширение
“ [stale-if-error](https://datatracker.ietf.org/doc/html/rfc5861#section-4) ”
поля заголовка `Cache-Control` разрешает
использовать устаревший закэшированный ответ в случае ошибки.

Чтобы минимизировать число обращений к FastCGI-серверам при заполнении нового элемента кэша, можно воспользоваться директивой [fastcgi_cache_lock](#fastcgi_cache_lock) .

## fastcgi_cache_valid

```
Syntax:  fastcgi_cache_valid [код ...] время;
Default: 
Context: location, http, server
```

Задаёт время кэширования для разных кодов ответа. Например, директивы

```
fastcgi_cache_valid 200 302 10m;
fastcgi_cache_valid 404      1m;
```

задают время кэширования 10 минут для ответов с кодами 200 и 302 и 1 минуту для ответов с кодом 404.

Если указано только `время` кэширования,

```
fastcgi_cache_valid 5m;
```

то кэшируются только ответы 200, 301 и 302.

Кроме того, можно кэшировать любые ответы с помощью параметра `any` :

```
fastcgi_cache_valid 200 302 10m;
fastcgi_cache_valid 301      1h;
fastcgi_cache_valid any      1m;
```

Параметры кэширования могут также быть заданы непосредственно в заголовке ответа. Такой способ приоритетнее, чем задание времени кэширования с помощью директивы.

- Поле заголовка `X-Accel-Expires` задаёт время кэширования
ответа в секундах.
Значение 0 запрещает кэшировать ответ.
Если значение начинается с префикса `@` , оно задаёт абсолютное
время в секундах с начала эпохи, до которого ответ может быть закэширован.
- Если в заголовке нет поля `X-Accel-Expires` ,
параметры кэширования определяются по полям заголовка `Expires` или `Cache-Control` .
- Ответ, в заголовке которого есть поле `Set-Cookie` ,
не будет кэшироваться.
- Ответ, в заголовке которого есть поле `Vary` со специальным значением “ `*` ”,
не будет кэшироваться (1.7.7).
Ответ, в заголовке которого есть поле `Vary` с другим значением, будет закэширован
с учётом соответствующих полей заголовка запроса (1.7.7).

Обработка одного или более из этих полей заголовка может быть отключена при помощи директивы [fastcgi_ignore_headers](#fastcgi_ignore_headers) .

## fastcgi_catch_stderr

```
Syntax:  fastcgi_catch_stderr строка;
Default: 
Context: location, http, server
```

Задаёт строку для поиска в потоке ошибок ответа, полученного от FastCGI-сервера. Если `строка` найдена, то считается, что FastCGI-сервер вернул [неверный ответ](#fastcgi_next_upstream) . Это позволяет обрабатывать ошибки приложений в nginx, например:

```
location /php/ {
    fastcgi_pass backend:9000;
    ...
    fastcgi_catch_stderr "PHP Fatal error";
    fastcgi_next_upstream error timeout invalid_header;
}
```

## fastcgi_connect_timeout

```
Syntax:  fastcgi_connect_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут для установления соединения с FastCGI-сервером. Необходимо иметь в виду, что этот таймаут обычно не может превышать 75 секунд.

## fastcgi_force_ranges

```
Syntax:  fastcgi_force_ranges on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.7.7.*

Включает поддержку диапазонов запрашиваемых байт (byte-range) для кэшированных и некэшированных ответов FastCGI-сервера вне зависимости от наличия поля `Accept-Ranges` в заголовках этих ответов.

## fastcgi_hide_header

```
Syntax:  fastcgi_hide_header поле;
Default: 
Context: location, http, server
```

По умолчанию nginx не передаёт клиенту поля заголовка `Status` и `X-Accel-...` из ответа FastCGI-сервера. Директива `fastcgi_hide_header` задаёт дополнительные поля, которые не будут передаваться. Если же передачу полей нужно разрешить, можно воспользоваться директивой [fastcgi_pass_header](#fastcgi_pass_header) .

## fastcgi_ignore_client_abort

```
Syntax:  fastcgi_ignore_client_abort on | off;
Default: off
Context: location, http, server
```

Определяет, закрывать ли соединение с FastCGI-сервером в случае, если клиент закрыл соединение, не дождавшись ответа.

## fastcgi_ignore_headers

```
Syntax:  fastcgi_ignore_headers поле ...;
Default: 
Context: location, http, server
```

Запрещает обработку некоторых полей заголовка из ответа FastCGI-сервера. В директиве можно указать поля `X-Accel-Redirect` , `X-Accel-Expires` , `X-Accel-Limit-Rate` (1.1.6), `X-Accel-Buffering` (1.1.6), `X-Accel-Charset` (1.1.6), `Expires` , `Cache-Control` , `Set-Cookie` (0.8.44) и `Vary` (1.7.7).

Если не запрещено, обработка этих полей заголовка заключается в следующем:

- `X-Accel-Expires` , `Expires` , `Cache-Control` , `Set-Cookie` и `Vary` задают параметры [кэширования](#fastcgi_cache_valid) ответа;
- `X-Accel-Redirect` производит [внутреннее
перенаправление](ngx_http_core_module.xml#internal) на указанный URI;
- `X-Accel-Limit-Rate` задаёт [ограничение
скорости](ngx_http_core_module.xml#limit_rate) передачи ответа клиенту;
- `X-Accel-Buffering` включает или выключает [буферизацию](#fastcgi_buffering) ответа;
- `X-Accel-Charset` задаёт желаемую [кодировку](ngx_http_charset_module.xml#charset) ответа.

## fastcgi_index

```
Syntax:  fastcgi_index имя;
Default: 
Context: location, http, server
```

Задаёт имя файла, который при создании переменной `$fastcgi_script_name` будет добавляться после URI, если URI заканчивается слэшом. Например, при таких настройках

```
fastcgi_index index.php;
fastcgi_param SCRIPT_FILENAME /home/www/scripts/php$fastcgi_script_name;
```

и запросе “ `/page.php` ” параметр `SCRIPT_FILENAME` будет равен “ `/home/www/scripts/php/page.php` ”, а при запросе “ `/` ”— “ `/home/www/scripts/php/index.php` ”.

## fastcgi_intercept_errors

```
Syntax:  fastcgi_intercept_errors on | off;
Default: off
Context: location, http, server
```

Определяет, передавать ли клиенту ответы FastCGI-сервера с кодом больше либо равным 300, или же перехватывать их и перенаправлять на обработку nginx’у с помощью директивы [error_page](ngx_http_core_module.xml#error_page) .

## fastcgi_keep_conn

```
Syntax:  fastcgi_keep_conn on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.4.*

По умолчанию FastCGI-сервер будет закрывать соединение сразу же после отправки ответа. При установке значения `on` nginx указывает FastCGI-серверу оставлять соединения открытыми. Это в частности требуется для функционирования [постоянных соединений](ngx_http_upstream_module.xml#keepalive) с FastCGI-серверами.

## fastcgi_limit_rate

```
Syntax:  fastcgi_limit_rate скорость;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.7.*

Ограничивает скорость чтения ответа от FastCGI-сервера. `Скорость` задаётся в байтах в секунду. Значение 0 отключает ограничение скорости. Ограничение устанавливается на запрос, поэтому, если nginx одновременно откроет два соединения к FastCGI-серверу, суммарная скорость будет вдвое выше заданного ограничения. Ограничение работает только в случае, если включена [буферизация](#fastcgi_buffering) ответов FastCGI-сервера. В значении параметра можно использовать переменные (1.27.0).

## fastcgi_max_temp_file_size

```
Syntax:  fastcgi_max_temp_file_size размер;
Default: 1024m
Context: location, http, server
```

Если включена [буферизация](#fastcgi_buffering) ответов FastCGI-сервера, и ответ не вмещается целиком в буферы, заданные директивами [fastcgi_buffer_size](#fastcgi_buffer_size) и [fastcgi_buffers](#fastcgi_buffers) , часть ответа может быть записана во временный файл. Эта директива задаёт максимальный `размер` временного файла. Размер данных, сбрасываемых во временный файл за один раз, задаётся директивой [fastcgi_temp_file_write_size](#fastcgi_temp_file_write_size) .

Значение 0 отключает возможность буферизации ответов во временные файлы.

> **Note:** Данное ограничение не распространяется на ответы,
которые будут [закэшированы](#fastcgi_cache) или [сохранены](#fastcgi_store) на диске.

## fastcgi_next_upstream

```
Syntax:  fastcgi_next_upstream error | timeout | denied | invalid_header | http_500 | http_503 | http_403 | http_404 | http_429 | non_idempotent | off ...;
Default: error timeout
Context: location, http, server
```

Определяет, в каких случаях запрос будет передан следующему серверу:

**`error`**  
  произошла ошибка соединения с сервером, передачи ему запроса или
чтения заголовка ответа сервера;

**`timeout`**  
  произошёл таймаут во время соединения с сервером,
передачи ему запроса или чтения заголовка ответа сервера;

**`denied`**  
  сервер [отклонил](#proxy_allow_upstream) соединение (1.29.3);

> **Note:** Параметр доступен как часть [коммерческой подписки](https://nginx.com/products/) .

**`invalid_header`**  
  сервер вернул пустой или неверный ответ;

**`http_500`**  
  сервер вернул ответ с кодом 500;

**`http_503`**  
  сервер вернул ответ с кодом 503;

**`http_403`**  
  сервер вернул ответ с кодом 403;

**`http_404`**  
  сервер вернул ответ с кодом 404;

**`http_429`**  
  сервер вернул ответ с кодом 429 (1.11.13);

**`non_idempotent`**  
  обычно запросы с [неидемпотентным](https://datatracker.ietf.org/doc/html/rfc7231#section-4.2.2) методом
( `POST` , `LOCK` , `PATCH` )
не передаются на другой сервер,
если запрос серверу группы уже был отправлен (1.9.13);
включение параметра явно разрешает повторять подобные запросы;

**`off`**  
  запрещает передачу запроса следующему серверу.

Необходимо понимать, что передача запроса следующему серверу возможна только при условии, что клиенту ещё ничего не передавалось. То есть, если ошибка или таймаут возникли в середине передачи ответа, то исправить это уже невозможно.

Директива также определяет, что считается [неудачной попыткой](ngx_http_upstream_module.xml#max_fails) работы с сервером. Случаи `error` , `timeout` , `denied` и `invalid_header` всегда считаются неудачными попытками, даже если они не указаны в директиве. Случаи `http_500` , `http_503` и `http_429` считаются неудачными попытками, только если они указаны в директиве. Случаи `http_403` и `http_404` никогда не считаются неудачными попытками.

Передача запроса следующему серверу может быть ограничена по [количеству попыток](#fastcgi_next_upstream_tries) и по [времени](#fastcgi_next_upstream_timeout) .

## fastcgi_next_upstream_timeout

```
Syntax:  fastcgi_next_upstream_timeout время;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает время, в течение которого возможна передача запроса [следующему серверу](#fastcgi_next_upstream) . Значение `0` отключает это ограничение.

## fastcgi_next_upstream_tries

```
Syntax:  fastcgi_next_upstream_tries число;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает число допустимых попыток для передачи запроса [следующему серверу](#fastcgi_next_upstream) . Значение `0` отключает это ограничение.

## fastcgi_no_cache

```
Syntax:  fastcgi_no_cache строка ...;
Default: 
Context: location, http, server
```

Задаёт условия, при которых ответ не будет сохраняться в кэш. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то ответ не будет сохранён:

```
fastcgi_no_cache $cookie_nocache $arg_nocache$arg_comment;
fastcgi_no_cache $http_pragma    $http_authorization;
```

Можно использовать совместно с директивой [fastcgi_cache_bypass](#fastcgi_cache_bypass) .

## fastcgi_param

```
Syntax:  fastcgi_param параметр значение [if_not_empty];
Default: 
Context: location, http, server
```

Задаёт `параметр` , который будет передаваться FastCGI-серверу. В качестве значения можно использовать текст, переменные и их комбинации. Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `fastcgi_param` .

Ниже приведён пример минимально необходимых параметров для PHP:

```
fastcgi_param SCRIPT_FILENAME /home/www/scripts/php$fastcgi_script_name;
fastcgi_param QUERY_STRING    $query_string;
```

Параметр `SCRIPT_FILENAME` используется в PHP для определения имени скрипта, а в параметре `QUERY_STRING` передаются параметры запроса.

Если скрипты обрабатывают запросы `POST` , то нужны ещё три параметра:

```
fastcgi_param REQUEST_METHOD  $request_method;
fastcgi_param CONTENT_TYPE    $content_type;
fastcgi_param CONTENT_LENGTH  $content_length;
```

Если PHP был собран с параметром конфигурации `--enable-force-cgi-redirect` , то нужно передавать параметр `REDIRECT_STATUS` со значением “200”:

```
fastcgi_param REDIRECT_STATUS 200;
```

Если директива указана с `if_not_empty` (1.1.11), то такой параметр с пустым значением передаваться на сервер не будет:

```
fastcgi_param HTTPS           $https if_not_empty;
```

## fastcgi_pass

```
Syntax:  fastcgi_pass адрес;
Default: 
Context: if в location, location
```

Задаёт адрес FastCGI-сервера. Адрес может быть указан в виде доменного имени или IP-адреса, и порта:

```
fastcgi_pass localhost:9000;
```

или в виде пути UNIX-сокета:

```
fastcgi_pass unix:/tmp/fastcgi.socket;
```

Если доменному имени соответствует несколько адресов, то все они будут использоваться по очереди (round-robin). И, кроме того, адрес может быть [группой серверов](ngx_http_upstream_module.xml) .

В значении параметра можно использовать переменные. В этом случае, если адрес указан в виде доменного имени, имя ищется среди описанных [групп серверов](ngx_http_upstream_module.xml) и если не найдено, то определяется с помощью [resolver](ngx_http_core_module.xml#resolver) ’а.

## fastcgi_pass_header

```
Syntax:  fastcgi_pass_header поле;
Default: 
Context: location, http, server
```

Разрешает передавать от FastCGI-сервера клиенту [запрещённые для передачи](#fastcgi_hide_header) поля заголовка.

## fastcgi_pass_request_body

```
Syntax:  fastcgi_pass_request_body on | off;
Default: on
Context: location, http, server
```

Позволяет запретить передачу исходного тела запроса на FastCGI-сервер. См. также директиву [fastcgi_pass_request_headers](#fastcgi_pass_request_headers) .

## fastcgi_pass_request_headers

```
Syntax:  fastcgi_pass_request_headers on | off;
Default: on
Context: location, http, server
```

Позволяет запретить передачу полей заголовка исходного запроса на FastCGI-сервер. См. также директивы [fastcgi_pass_request_body](#fastcgi_pass_request_body) .

## fastcgi_read_timeout

```
Syntax:  fastcgi_read_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при чтении ответа FastCGI-сервера. Таймаут устанавливается не на всю передачу ответа, а только между двумя операциями чтения. Если по истечении этого времени FastCGI-сервер ничего не передаст, соединение закрывается.

## fastcgi_request_buffering

```
Syntax:  fastcgi_request_buffering on | off;
Default: on
Context: location, http, server
```

*This directive appeared in version 1.7.11.*

Разрешает или запрещает использовать буферизацию тела запроса клиента.

Если буферизация включена, то тело запроса полностью [читается](ngx_http_core_module.xml#client_body_buffer_size) от клиента перед отправкой запроса на FastCGI-сервер.

Если буферизация выключена, то тело запроса отправляется на FastCGI-сервер сразу же по мере его поступления. В этом случае запрос не может быть передан [следующему серверу](#fastcgi_next_upstream) , если nginx уже начал отправку тела запроса.

## fastcgi_request_dynamic

```
Syntax:  fastcgi_request_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Разрешает или запрещает создание отдельного экземпляра запроса для каждого FastCGI-сервера. По умолчанию для всех FastCGI-серверов используется единый запрос. Если разрешено, то для каждого сервера создаётся отдельный экземпляр запроса, что позволяет кастомизировать запрос для конкретного сервера.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## fastcgi_send_lowat

```
Syntax:  fastcgi_send_lowat размер;
Default: 0
Context: location, http, server
```

При установке директивы в ненулевое значение nginx будет пытаться минимизировать число операций отправки на исходящих соединениях с FastCGI-сервером либо при помощи флага NOTE_LOWAT метода [kqueue](../events.xml#kqueue) , либо при помощи параметра сокета SO_SNDLOWAT , с указанным `размером` .

Эта директива игнорируется на Linux, Solaris и Windows.

## fastcgi_send_timeout

```
Syntax:  fastcgi_send_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при передаче запроса FastCGI-серверу. Таймаут устанавливается не на всю передачу запроса, а только между двумя операциями записи. Если по истечении этого времени FastCGI-сервер не примет новых данных, соединение закрывается.

## fastcgi_socket_keepalive

```
Syntax:  fastcgi_socket_keepalive on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.15.6.*

Конфигурирует поведение “TCP keepalive” для исходящих соединений к FastCGI-серверу. По умолчанию для сокета действуют настройки операционной системы. Если указано значение “ `on` ”, то для сокета включается параметр SO_KEEPALIVE .

## fastcgi_split_path_info

```
Syntax:  fastcgi_split_path_info regex;
Default: 
Context: location
```

Задаёт регулярное выражение, выделяющее значение для переменной `$fastcgi_path_info` . Регулярное выражение должно иметь два выделения, из которых первое становится значением переменной `$fastcgi_script_name` , а второе—значением переменной `$fastcgi_path_info` . Например, при таких настройках

```
location ~ ^(.+\.php)(.*)$ {
    fastcgi_split_path_info       ^(.+\.php)(.*)$;
    fastcgi_param SCRIPT_FILENAME /path/to/php$fastcgi_script_name;
    fastcgi_param PATH_INFO       $fastcgi_path_info;
```

и запросе “ `/show.php/article/0001` ” параметр `SCRIPT_FILENAME` будет равен “ `/path/to/php/show.php` ”, а параметр `PATH_INFO` —“ `/article/0001` ”.

## fastcgi_store

```
Syntax:  fastcgi_store on | off | строка;
Default: off
Context: location, http, server
```

Разрешает сохранение на диск файлов. Параметр `on` сохраняет файлы в соответствии с путями, указанными в директивах [alias](ngx_http_core_module.xml#alias) или [root](ngx_http_core_module.xml#root) . Параметр `off` запрещает сохранение файлов. Кроме того, имя файла можно задать явно с помощью строки с переменными:

```
fastcgi_store /data/www$original_uri;
```

Время изменения файлов выставляется согласно полученному полю `Last-Modified` в заголовке ответа. Ответ сначала записывается во временный файл, а потом этот файл переименовывается. Начиная с версии 0.8.9 временный файл и постоянное место хранения ответа могут располагаться на разных файловых системах. Однако нужно учитывать, что в этом случае вместо дешёвой операции переименовывания в пределах одной файловой системы файл копируется с одной файловой системы на другую. Поэтому лучше, если сохраняемые файлы будут находиться на той же файловой системе, что и каталог с временными файлами, задаваемый директивой [fastcgi_temp_path](#fastcgi_temp_path) для данного location.

Директиву можно использовать для создания локальных копий статических неизменяемых файлов, например, так:

```
location /images/ {
    root                 /data/www;
    error_page           404 = /fetch$uri;
}

location /fetch/ {
    internal;

    fastcgi_pass         backend:9000;
    ...

    fastcgi_store        on;
    fastcgi_store_access user:rw group:rw all:r;
    fastcgi_temp_path    /data/temp;

    alias                /data/www/;
}
```

## fastcgi_store_access

```
Syntax:  fastcgi_store_access пользователи:права ...;
Default: user:rw
Context: location, http, server
```

Задаёт права доступа для создаваемых файлов и каталогов, например,

```
fastcgi_store_access user:rw group:rw all:r;
```

Если заданы какие-либо права для `group` или `all` , то права для `user` указывать необязательно:

```
fastcgi_store_access group:rw all:r;
```

## fastcgi_temp_file_write_size

```
Syntax:  fastcgi_temp_file_write_size размер;
Default: 8k|16k
Context: location, http, server
```

Ограничивает `размер` данных, сбрасываемых во временный файл за один раз, при включённой буферизации ответов FastCGI-сервера во временные файлы. По умолчанию `размер` ограничен двумя буферами, заданными директивами [fastcgi_buffer_size](#fastcgi_buffer_size) и [fastcgi_buffers](#fastcgi_buffers) . Максимальный размер временного файла задаётся директивой [fastcgi_max_temp_file_size](#fastcgi_max_temp_file_size) .

## fastcgi_temp_path

```
Syntax:  fastcgi_temp_path путь [уровень1 [уровень2 [уровень3]]];
Default: fastcgi_temp
Context: location, http, server
```

Задаёт имя каталога для хранения временных файлов с данными, полученными от FastCGI-серверов. В каталоге может использоваться иерархия подкаталогов до трёх уровней. Например, при такой конфигурации

```
fastcgi_temp_path /spool/nginx/fastcgi_temp 1 2;
```

временный файл будет следующего вида:

```
/spool/nginx/fastcgi_temp/7/45/00000123457
```

См. также параметр `use_temp_path` директивы [fastcgi_cache_path](#fastcgi_cache_path) .

# Параметры, передаваемые FastCGI-серверу {#parameters}

Поля заголовка HTTP-запроса передаются FastCGI-серверу в виде параметров. В приложениях и скриптах, запущенных в виде FastCGI-сервера, эти параметры обычно доступны в виде переменных среды. Например, поле заголовка `User-Agent` передаётся как параметр `HTTP_USER_AGENT` . Кроме полей заголовка HTTP-запроса можно передавать произвольные параметры с помощью директивы [fastcgi_param](#fastcgi_param) .

# Встроенные переменные {#variables}

В модуле `ngx_http_fastcgi_module` есть встроенные переменные, которые можно использовать для формирования параметров с помощью директивы [fastcgi_param](#fastcgi_param) :

**`$fastcgi_script_name`**  
  URI запроса или же, если URI заканчивается слэшом,
то URI запроса, дополненное именем индексного файла, задаваемого директивой [fastcgi_index](#fastcgi_index) .
Эту переменную можно использовать для задания параметров `SCRIPT_FILENAME` и `PATH_TRANSLATED` ,
используемых, в частности, для определения имени скрипта в PHP.
Например, для запроса “ `/info/` ” и при использовании
директив

```
fastcgi_index index.php;
fastcgi_param SCRIPT_FILENAME /home/www/scripts/php$fastcgi_script_name;
```

  параметр `SCRIPT_FILENAME` будет равен
“ `/home/www/scripts/php/info/index.php` ”.

При использовании директивы [fastcgi_split_path_info](#fastcgi_split_path_info) переменная `$fastcgi_script_name` равна значению первого выделения, задаваемого этой директивой.

**`$fastcgi_path_info`**  
  значение второго выделения, задаваемого директивой [fastcgi_split_path_info](#fastcgi_split_path_info) .
Эту переменную можно использовать для задания параметра `PATH_INFO` .

