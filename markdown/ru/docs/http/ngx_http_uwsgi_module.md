# Модуль ngx_http_uwsgi_module

**Revision:** 56  
**Language:** ru

Модуль `ngx_http_uwsgi_module` позволяет передавать запросы uwsgi-серверу.

# Пример конфигурации {#example}

```
location / {
    include    uwsgi_params;
    uwsgi_pass localhost:9000;
}
```

# Директивы {#directives}

## uwsgi_allow_upstream

```
Syntax:  uwsgi_allow_upstream строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Задаёт условия, при которых доступ к uwsgi-серверу будет разрешён или [запрещён](#denied) . Если все значения строковых параметров непустые и не равны “0”, то доступ разрешён. Условия проверяются каждый раз перед установлением соединения с uwsgi-сервером. В значении параметров допустимо использование переменных:

```
geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;

    location / {
        uwsgi_pass           localhost:9000;
        uwsgi_allow_upstream $allow;
        ...
    }
}
```

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## uwsgi_bind

```
Syntax:  uwsgi_bind адрес [transparent] | off;
Default: 
Context: location, http, server
```

Задаёт локальный IP-адрес с необязательным портом (1.11.2), который будет использоваться в исходящих соединениях с uwsgi-сервером. В значении параметра допустимо использование переменных (1.3.12). Специальное значение `off` (1.3.12) отменяет действие унаследованной с предыдущего уровня конфигурации директивы `uwsgi_bind` , позволяя системе самостоятельно выбирать локальный IP-адрес и порт.

Параметр `transparent` (1.11.0) позволяет задать нелокальный IP-aдрес, который будет использоваться в исходящих соединениях с uwsgi-сервером, например, реальный IP-адрес клиента:

```
uwsgi_bind $remote_addr transparent;
```

Для работы параметра обычно требуется запустить рабочие процессы nginx с привилегиями [суперпользователя](../ngx_core_module.xml#user) . В Linux этого не требуется (1.13.8), так как если указан параметр `transparent` , то рабочие процессы наследуют capability `CAP_NET_RAW` из главного процесса. Также необходимо настроить таблицу маршрутизации ядра для перехвата сетевого трафика с uwsgi-сервера.

## uwsgi_bind_dynamic

```
Syntax:  uwsgi_bind_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Если включено, операция [bind](#uwsgi_bind) осуществляется при каждой попытке соединения.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## uwsgi_buffer_size

```
Syntax:  uwsgi_buffer_size размер;
Default: 4k|8k
Context: location, http, server
```

Задаёт `размер` буфера, в который будет читаться первая часть ответа, получаемого от uwsgi-сервера. По умолчанию размер одного буфера равен размеру страницы памяти. В зависимости от платформы это или 4K, или 8K, однако его можно сделать меньше.

## uwsgi_buffering

```
Syntax:  uwsgi_buffering on | off;
Default: on
Context: location, http, server
```

Разрешает или запрещает использовать буферизацию ответов uwsgi-сервера.

Если буферизация включена, то nginx принимает ответ uwsgi-сервера как можно быстрее, сохраняя его в буферы, заданные директивами [uwsgi_buffer_size](#uwsgi_buffer_size) и [uwsgi_buffers](#uwsgi_buffers) . Если ответ не вмещается целиком в память, то его часть может быть записана на диск во [временный файл](#uwsgi_temp_path) . Запись во временные файлы контролируется директивами [uwsgi_max_temp_file_size](#uwsgi_max_temp_file_size) и [uwsgi_temp_file_write_size](#uwsgi_temp_file_write_size) .

Если буферизация выключена, то ответ синхронно передаётся клиенту сразу же по мере его поступления. nginx не пытается считать весь ответ uwsgi-сервера. Максимальный размер данных, который nginx может принять от сервера за один раз, задаётся директивой [uwsgi_buffer_size](#uwsgi_buffer_size) .

Буферизация может быть также включена или выключена путём передачи значения “ `yes` ” или “ `no` ” в поле `X-Accel-Buffering` заголовка ответа. Эту возможность можно запретить с помощью директивы [uwsgi_ignore_headers](#uwsgi_ignore_headers) .

## uwsgi_buffers

```
Syntax:  uwsgi_buffers число размер;
Default: 8 4k|8k
Context: location, http, server
```

Задаёт `число` и `размер` буферов для одного соединения, в которые будет читаться ответ, получаемый от uwsgi-сервера. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

## uwsgi_busy_buffers_size

```
Syntax:  uwsgi_busy_buffers_size размер;
Default: 8k|16k
Context: location, http, server
```

При включённой [буферизации](#uwsgi_buffering) ответов uwsgi-сервера, ограничивает суммарный `размер` буферов, которые могут быть заняты для отправки ответа клиенту, пока ответ ещё не прочитан целиком. Оставшиеся буферы тем временем могут использоваться для чтения ответа и, при необходимости, буферизации части ответа во временный файл. По умолчанию `размер` ограничен двумя буферами, заданными директивами [uwsgi_buffer_size](#uwsgi_buffer_size) и [uwsgi_buffers](#uwsgi_buffers) .

## uwsgi_cache

```
Syntax:  uwsgi_cache зона | off;
Default: off
Context: location, http, server
```

Задаёт зону разделяемой памяти, используемой для кэширования. Одна и та же зона может использоваться в нескольких местах. В значении параметра можно использовать переменные (1.7.9). Параметр `off` запрещает кэширование, унаследованное с предыдущего уровня конфигурации.

## uwsgi_cache_background_update

```
Syntax:  uwsgi_cache_background_update on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.11.10.*

Позволяет запустить фоновый подзапрос для обновления просроченного элемента кэша, в то время как клиенту возвращается устаревший закэшированный ответ. Использование устаревшего закэшированного ответа в момент его обновления должно быть [разрешено](#uwsgi_cache_use_stale_updating) .

## uwsgi_cache_bypass

```
Syntax:  uwsgi_cache_bypass строка ...;
Default: 
Context: location, http, server
```

Задаёт условия, при которых ответ не будет браться из кэша. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то ответ не берётся из кэша:

```
uwsgi_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
uwsgi_cache_bypass $http_pragma    $http_authorization;
```

Можно использовать совместно с директивой [uwsgi_no_cache](#uwsgi_no_cache) .

## uwsgi_cache_key

```
Syntax:  uwsgi_cache_key строка;
Default: 
Context: location, http, server
```

Задаёт ключ для кэширования, например,

```
uwsgi_cache_key localhost:9000$request_uri;
```

## uwsgi_cache_lock

```
Syntax:  uwsgi_cache_lock on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

Если включено, одновременно только одному запросу будет позволено заполнить новый элемент кэша, идентифицируемый согласно директиве [uwsgi_cache_key](#uwsgi_cache_key) , передав запрос на uwsgi-сервер. Остальные запросы этого же элемента будут либо ожидать появления ответа в кэше, либо освобождения блокировки этого элемента, в течение времени, заданного директивой [uwsgi_cache_lock_timeout](#uwsgi_cache_lock_timeout) .

## uwsgi_cache_lock_age

```
Syntax:  uwsgi_cache_lock_age время;
Default: 5s
Context: location, http, server
```

*This directive appeared in version 1.7.8.*

Если последний запрос, переданный на uwsgi-сервер для заполнения нового элемента кэша, не завершился за указанное `время` , на uwsgi-сервер может быть передан ещё один запрос.

## uwsgi_cache_lock_timeout

```
Syntax:  uwsgi_cache_lock_timeout время;
Default: 5s
Context: location, http, server
```

*This directive appeared in version 1.1.12.*

Задаёт таймаут для [uwsgi_cache_lock](#uwsgi_cache_lock) . По истечении указанного `времени` запрос будет передан на uwsgi-сервер, однако ответ не будет закэширован.

> **Note:** До версии 1.7.8 такой ответ мог быть закэширован.

## uwsgi_cache_max_range_offset

```
Syntax:  uwsgi_cache_max_range_offset число;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.11.6.*

Задаёт смещение в байтах для запросов с указанием диапазона запрашиваемых байт (byte-range requests). Если диапазон находится за указанным смещением, range-запрос будет передан на uwsgi-сервер и ответ не будет закэширован.

## uwsgi_cache_methods

```
Syntax:  uwsgi_cache_methods GET | HEAD | POST ...;
Default: GET HEAD
Context: location, http, server
```

Если метод запроса клиента указан в этой директиве, то ответ будет закэширован. Методы “ `GET` ” и “ `HEAD` ” всегда добавляются в список, но тем не менее рекомендуется перечислять их явно. См. также директиву [uwsgi_no_cache](#uwsgi_no_cache) .

## uwsgi_cache_min_uses

```
Syntax:  uwsgi_cache_min_uses число;
Default: 1
Context: location, http, server
```

Задаёт `число` запросов, после которого ответ будет закэширован.

## uwsgi_cache_path

```
Syntax:  uwsgi_cache_path путь [levels=уровни] [use_temp_path=on|off] keys_zone=имя:размер [inactive=время] [max_size=размер] [min_free=размер] [manager_files=число] [manager_sleep=время] [manager_threshold=время] [loader_files=число] [loader_sleep=время] [loader_threshold=время] [purger=on|off] [purger_files=число] [purger_sleep=время] [purger_threshold=время];
Default: 
Context: http
```

Задаёт путь и другие параметры кэша. Данные кэша хранятся в файлах. Именем файла в кэше является результат функции MD5 от [ключа кэширования](#uwsgi_cache_key) . Параметр `levels` задаёт уровни иерархии кэша: можно задать от 1 до 3 уровней, на каждом уровне допускаются значения 1 или 2. Например, при использовании

```
uwsgi_cache_path /data/nginx/cache levels=1:2 keys_zone=one:10m;
```

имена файлов в кэше будут такого вида:

```
/data/nginx/cache/c/29/b7f54b2df7773722d382f4809d65029c
```

Кэшируемый ответ сначала записывается во временный файл, а потом этот файл переименовывается. Начиная с версии 0.8.9 временные файлы и кэш могут располагаться на разных файловых системах. Однако нужно учитывать, что в этом случае вместо дешёвой операции переименовывания в пределах одной файловой системы файл копируется с одной файловой системы на другую. Поэтому лучше, если кэш будет находиться на той же файловой системе, что и каталог с временными файлами. Какой из каталогов будет использоваться для временных файлов определяется параметром `use_temp_path` (1.7.10). Если параметр не задан или установлен в значение “ `on` ”, то будет использоваться каталог, задаваемый директивой [uwsgi_temp_path](#uwsgi_temp_path) для данного location. Если параметр установлен в значение “ `off` ”, то временные файлы будут располагаться непосредственно в каталоге кэша.

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
  Указывает, будут ли записи в кэше, соответствующие [маске](#uwsgi_cache_purge) ,
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

## uwsgi_cache_purge

```
Syntax:  uwsgi_cache_purge строка ...;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.5.7.*

Задаёт условия, при которых запрос будет считаться запросом на очистку кэша. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то запись в кэше с соответствующим [ключом кэширования](#uwsgi_cache_key) удаляется. В результате успешной операции возвращается ответ с кодом 204 No Content .

Если [ключ кэширования](#uwsgi_cache_key) запроса на очистку заканчивается звёздочкой (“ `*` ”), то все записи в кэше, соответствующие этой маске, будут удалены из кэша. Тем не менее, эти записи будут оставаться на диске или до момента удаления из-за [отсутствия обращения к данным](#uwsgi_cache_path) , или до обработки их процессом “ [cache purger](#purger) ” (1.7.12), или до попытки клиента получить к ним доступ.

Пример конфигурации:

```
uwsgi_cache_path /data/nginx/cache keys_zone=cache_zone:10m;

map $request_method $purge_method {
    PURGE   1;
    default 0;
}

server {
    ...
    location / {
        uwsgi_pass        http://backend;
        uwsgi_cache       cache_zone;
        uwsgi_cache_key   $uri;
        uwsgi_cache_purge $purge_method;
    }
}
```

> **Note:** Функциональность доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## uwsgi_cache_revalidate

```
Syntax:  uwsgi_cache_revalidate on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.5.7.*

Разрешает ревалидацию просроченных элементов кэша при помощи условных запросов с полями заголовка `If-Modified-Since` и `If-None-Match` .

## uwsgi_cache_use_stale

```
Syntax:  uwsgi_cache_use_stale error | timeout | invalid_header | updating | http_500 | http_503 | http_403 | http_404 | http_429 | off ...;
Default: off
Context: location, http, server
```

Определяет, в каких случаях можно использовать устаревший закэшированный ответ. Параметры директивы совпадают с параметрами директивы [uwsgi_next_upstream](#uwsgi_next_upstream) .

Параметр `error` также позволяет использовать устаревший закэшированный ответ при невозможности выбора uwsgi-сервера для обработки запроса.

Кроме того, дополнительный параметр `updating` разрешает использовать устаревший закэшированный ответ, если на данный момент он уже обновляется. Это позволяет минимизировать число обращений к uwsgi-серверам при обновлении закэшированных данных.

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

Чтобы минимизировать число обращений к uwsgi-серверам при заполнении нового элемента кэша, можно воспользоваться директивой [uwsgi_cache_lock](#uwsgi_cache_lock) .

## uwsgi_cache_valid

```
Syntax:  uwsgi_cache_valid [код ...] время;
Default: 
Context: location, http, server
```

Задаёт время кэширования для разных кодов ответа. Например, директивы

```
uwsgi_cache_valid 200 302 10m;
uwsgi_cache_valid 404      1m;
```

задают время кэширования 10 минут для ответов с кодами 200 и 302 и 1 минуту для ответов с кодом 404.

Если указано только `время` кэширования,

```
uwsgi_cache_valid 5m;
```

то кэшируются только ответы 200, 301 и 302.

Кроме того, можно кэшировать любые ответы с помощью параметра `any` :

```
uwsgi_cache_valid 200 302 10m;
uwsgi_cache_valid 301      1h;
uwsgi_cache_valid any      1m;
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

Обработка одного или более из этих полей заголовка может быть отключена при помощи директивы [uwsgi_ignore_headers](#uwsgi_ignore_headers) .

## uwsgi_connect_timeout

```
Syntax:  uwsgi_connect_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут для установления соединения с uwsgi-сервером. Необходимо иметь в виду, что этот таймаут обычно не может превышать 75 секунд.

## uwsgi_force_ranges

```
Syntax:  uwsgi_force_ranges on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.7.7.*

Включает поддержку диапазонов запрашиваемых байт (byte-range) для кэшированных и некэшированных ответов uwsgi-сервера вне зависимости от наличия поля `Accept-Ranges` в заголовках этих ответов.

## uwsgi_hide_header

```
Syntax:  uwsgi_hide_header поле;
Default: 
Context: location, http, server
```

По умолчанию nginx не передаёт клиенту поля заголовка `Status` и `X-Accel-...` из ответа uwsgi-сервера. Директива `uwsgi_hide_header` задаёт дополнительные поля, которые не будут передаваться. Если же передачу полей нужно разрешить, можно воспользоваться директивой [uwsgi_pass_header](#uwsgi_pass_header) .

## uwsgi_ignore_client_abort

```
Syntax:  uwsgi_ignore_client_abort on | off;
Default: off
Context: location, http, server
```

Определяет, закрывать ли соединение с uwsgi-сервером в случае, если клиент закрыл соединение, не дождавшись ответа.

## uwsgi_ignore_headers

```
Syntax:  uwsgi_ignore_headers поле ...;
Default: 
Context: location, http, server
```

Запрещает обработку некоторых полей заголовка из ответа uwsgi-сервера. В директиве можно указать поля `X-Accel-Redirect` , `X-Accel-Expires` , `X-Accel-Limit-Rate` (1.1.6), `X-Accel-Buffering` (1.1.6), `X-Accel-Charset` (1.1.6), `Expires` , `Cache-Control` , `Set-Cookie` (0.8.44) и `Vary` (1.7.7).

Если не запрещено, обработка этих полей заголовка заключается в следующем:

- `X-Accel-Expires` , `Expires` , `Cache-Control` , `Set-Cookie` и `Vary` задают параметры [кэширования](#uwsgi_cache_valid) ответа;
- `X-Accel-Redirect` производит [внутреннее
перенаправление](ngx_http_core_module.xml#internal) на указанный URI;
- `X-Accel-Limit-Rate` задаёт [ограничение
скорости](ngx_http_core_module.xml#limit_rate) передачи ответа клиенту;
- `X-Accel-Buffering` включает или выключает [буферизацию](#uwsgi_buffering) ответа;
- `X-Accel-Charset` задаёт желаемую [кодировку](ngx_http_charset_module.xml#charset) ответа.

## uwsgi_intercept_errors

```
Syntax:  uwsgi_intercept_errors on | off;
Default: off
Context: location, http, server
```

Определяет, передавать ли клиенту ответы uwsgi-сервера с кодом больше либо равным 300, или же перехватывать их и перенаправлять на обработку nginx’у с помощью директивы [error_page](ngx_http_core_module.xml#error_page) .

## uwsgi_limit_rate

```
Syntax:  uwsgi_limit_rate скорость;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.7.*

Ограничивает скорость чтения ответа от uwsgi-сервера. `Скорость` задаётся в байтах в секунду. Значение 0 отключает ограничение скорости. Ограничение устанавливается на запрос, поэтому, если nginx одновременно откроет два соединения к uwsgi-серверу, суммарная скорость будет вдвое выше заданного ограничения. Ограничение работает только в случае, если включена [буферизация](#uwsgi_buffering) ответов uwsgi-сервера. В значении параметра можно использовать переменные (1.27.0).

## uwsgi_max_temp_file_size

```
Syntax:  uwsgi_max_temp_file_size размер;
Default: 1024m
Context: location, http, server
```

Если включена [буферизация](#uwsgi_buffering) ответов uwsgi-сервера, и ответ не вмещается целиком в буферы, заданные директивами [uwsgi_buffer_size](#uwsgi_buffer_size) и [uwsgi_buffers](#uwsgi_buffers) , часть ответа может быть записана во временный файл. Эта директива задаёт максимальный `размер` временного файла. Размер данных, сбрасываемых во временный файл за один раз, задаётся директивой [uwsgi_temp_file_write_size](#uwsgi_temp_file_write_size) .

Значение 0 отключает возможность буферизации ответов во временные файлы.

> **Note:** Данное ограничение не распространяется на ответы,
которые будут [закэшированы](#uwsgi_cache) или [сохранены](#uwsgi_store) на диске.

## uwsgi_modifier1

```
Syntax:  uwsgi_modifier1 число;
Default: 0
Context: location, http, server
```

Задаёт значение поля `modifier1` в [заголовке пакета uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/Protocol.html#uwsgi-packet-header) .

## uwsgi_modifier2

```
Syntax:  uwsgi_modifier2 число;
Default: 0
Context: location, http, server
```

Задаёт значение поля `modifier2` в [заголовке пакета uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/Protocol.html#uwsgi-packet-header) .

## uwsgi_next_upstream

```
Syntax:  uwsgi_next_upstream error | timeout | denied | invalid_header | http_500 | http_503 | http_403 | http_404 | http_429 | non_idempotent | off ...;
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

Передача запроса следующему серверу может быть ограничена по [количеству попыток](#uwsgi_next_upstream_tries) и по [времени](#uwsgi_next_upstream_timeout) .

## uwsgi_next_upstream_timeout

```
Syntax:  uwsgi_next_upstream_timeout время;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает время, в течение которого возможна передача запроса [следующему серверу](#uwsgi_next_upstream) . Значение `0` отключает это ограничение.

## uwsgi_next_upstream_tries

```
Syntax:  uwsgi_next_upstream_tries число;
Default: 0
Context: location, http, server
```

*This directive appeared in version 1.7.5.*

Ограничивает число допустимых попыток для передачи запроса [следующему серверу](#uwsgi_next_upstream) . Значение `0` отключает это ограничение.

## uwsgi_no_cache

```
Syntax:  uwsgi_no_cache строка ...;
Default: 
Context: location, http, server
```

Задаёт условия, при которых ответ не будет сохраняться в кэш. Если значение хотя бы одного из строковых параметров непустое и не равно “0”, то ответ не будет сохранён:

```
uwsgi_no_cache $cookie_nocache $arg_nocache$arg_comment;
uwsgi_no_cache $http_pragma    $http_authorization;
```

Можно использовать совместно с директивой [uwsgi_cache_bypass](#uwsgi_cache_bypass) .

## uwsgi_param

```
Syntax:  uwsgi_param параметр значение [if_not_empty];
Default: 
Context: location, http, server
```

Задаёт `параметр` , который будет передаваться uwsgi-серверу. В качестве значения можно использовать текст, переменные и их комбинации. Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `uwsgi_param` .

Стандартные [переменные окружения CGI](https://datatracker.ietf.org/doc/html/rfc3875#section-4.1) должны передаваться как заголовки uwsgi, см. файл `uwsgi_params` из дистрибутива:

```
location / {
    include uwsgi_params;
    ...
}
```

Если директива указана с `if_not_empty` (1.1.11), то такой параметр с пустым значением передаваться на сервер не будет:

```
uwsgi_param HTTPS $https if_not_empty;
```

## uwsgi_pass

```
Syntax:  uwsgi_pass [протокол://]адрес;
Default: 
Context: if в location, location
```

Задаёт протокол и адрес uwsgi-сервера. В качестве протокола можно указать “ `uwsgi` ” или “ `suwsgi` ” (secured uwsgi, uwsgi через SSL). Адрес может быть указан в виде доменного имени или IP-адреса, и порта:

```
uwsgi_pass localhost:9000;
uwsgi_pass uwsgi://localhost:9000;
uwsgi_pass suwsgi://[2001:db8::1]:9090;
```

или в виде пути UNIX-сокета:

```
uwsgi_pass unix:/tmp/uwsgi.socket;
```

Если доменному имени соответствует несколько адресов, то все они будут использоваться по очереди (round-robin). И, кроме того, адрес может быть [группой серверов](ngx_http_upstream_module.xml) .

В значении параметра можно использовать переменные. В этом случае, если адрес указан в виде доменного имени, имя ищется среди описанных [групп серверов](ngx_http_upstream_module.xml) и если не найдено, то определяется с помощью [resolver](ngx_http_core_module.xml#resolver) ’а.

> **Note:** Протокол secured uwsgi поддерживается начиная с версии 1.5.8.

## uwsgi_pass_header

```
Syntax:  uwsgi_pass_header поле;
Default: 
Context: location, http, server
```

Разрешает передавать от uwsgi-сервера клиенту [запрещённые для передачи](#uwsgi_hide_header) поля заголовка.

## uwsgi_pass_request_body

```
Syntax:  uwsgi_pass_request_body on | off;
Default: on
Context: location, http, server
```

Позволяет запретить передачу исходного тела запроса на uwsgi-сервер. См. также директиву [uwsgi_pass_request_headers](#uwsgi_pass_request_headers) .

## uwsgi_pass_request_headers

```
Syntax:  uwsgi_pass_request_headers on | off;
Default: on
Context: location, http, server
```

Позволяет запретить передачу полей заголовка исходного запроса на uwsgi-сервер. См. также директивы [uwsgi_pass_request_body](#uwsgi_pass_request_body) .

## uwsgi_read_timeout

```
Syntax:  uwsgi_read_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при чтении ответа uwsgi-сервера. Таймаут устанавливается не на всю передачу ответа, а только между двумя операциями чтения. Если по истечении этого времени uwsgi-сервер ничего не передаст, соединение закрывается.

## uwsgi_request_buffering

```
Syntax:  uwsgi_request_buffering on | off;
Default: on
Context: location, http, server
```

*This directive appeared in version 1.7.11.*

Разрешает или запрещает использовать буферизацию тела запроса клиента.

Если буферизация включена, то тело запроса полностью [читается](ngx_http_core_module.xml#client_body_buffer_size) от клиента перед отправкой запроса на uwsgi-сервер.

Если буферизация выключена, то тело запроса отправляется на uwsgi-сервер сразу же по мере его поступления. В этом случае запрос не может быть передан [следующему серверу](#uwsgi_next_upstream) , если nginx уже начал отправку тела запроса.

Если для отправки тела исходного запроса используется HTTP/1.1 и передача данных частями (chunked transfer encoding), то тело запроса буферизуется независимо от значения директивы.

## uwsgi_request_dynamic

```
Syntax:  uwsgi_request_dynamic on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.29.3.*

Разрешает или запрещает создание отдельного экземпляра запроса для каждого uwsgi-сервера. По умолчанию для всех uwsgi-серверов используется единый запрос. Если разрешено, то для каждого сервера создаётся отдельный экземпляр запроса, что позволяет кастомизировать запрос для конкретного сервера.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## uwsgi_send_timeout

```
Syntax:  uwsgi_send_timeout время;
Default: 60s
Context: location, http, server
```

Задаёт таймаут при передаче запроса uwsgi-серверу. Таймаут устанавливается не на всю передачу запроса, а только между двумя операциями записи. Если по истечении этого времени uwsgi-сервер не примет новых данных, соединение закрывается.

## uwsgi_socket_keepalive

```
Syntax:  uwsgi_socket_keepalive on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.15.6.*

Конфигурирует поведение “TCP keepalive” для исходящих соединений к uwsgi-серверу. По умолчанию для сокета действуют настройки операционной системы. Если указано значение “ `on` ”, то для сокета включается параметр SO_KEEPALIVE .

## uwsgi_ssl_certificate

```
Syntax:  uwsgi_ssl_certificate файл;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.7.8.*

Задаёт `файл` с сертификатом в формате PEM для аутентификации на suwsgi-сервере.

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## uwsgi_ssl_certificate_cache

```
Syntax:  uwsgi_ssl_certificate_cache max=N [inactive=время] [valid=время];
Default: off
Context: location, http, server
```

*This directive appeared in version 1.27.4.*

Задаёт кэш, в котором могут храниться [SSL-сертификаты](#uwsgi_ssl_certificate) и [секретные ключи](#uwsgi_ssl_certificate_key) , полученные из [переменных](#uwsgi_ssl_certificate_key_variables) .

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
uwsgi_ssl_certificate       $uwsgi_ssl_server_name.crt;
uwsgi_ssl_certificate_key   $uwsgi_ssl_server_name.key;
uwsgi_ssl_certificate_cache max=1000 inactive=20s valid=1m;
```

## uwsgi_ssl_certificate_key

```
Syntax:  uwsgi_ssl_certificate_key файл;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.7.8.*

Задаёт `файл` с секретным ключом в формате PEM для аутентификации на suwsgi-сервере.

Вместо `файла` можно указать значение `engine` : `имя` : `id` (1.7.9), которое загружает ключ с указанным `id` из OpenSSL engine с заданным `именем` .

Вместо `файла` можно указать значение `store` : `схема` : `id` (1.29.0), которое используется для загрузки ключа с указанным `id` и зарегистрированной провайдером OpenSSL `схемой` URI, такой как [`pkcs11`](https://datatracker.ietf.org/doc/html/rfc7512) .

Начиная с версии 1.21.0 в имени файла можно использовать переменные.

## uwsgi_ssl_ciphers

```
Syntax:  uwsgi_ssl_ciphers ciphers;
Default: DEFAULT
Context: location, http, server
```

*This directive appeared in version 1.5.8.*

Описывает разрешённые шифры для запросов к suwsgi-серверу. Шифры задаются в формате, поддерживаемом библиотекой OpenSSL.

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

## uwsgi_ssl_conf_command

```
Syntax:  uwsgi_ssl_conf_command имя значение;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.19.4.*

Задаёт произвольные конфигурационные [команды](https://www.openssl.org/docs/man1.1.1/man3/SSL_CONF_cmd.html) OpenSSL при установлении соединения с suwsgi-сервером.

> **Note:** Директива поддерживается при использовании OpenSSL 1.0.2 и выше.

На одном уровне может быть указано несколько директив `uwsgi_ssl_conf_command` . Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `uwsgi_ssl_conf_command` .

> **Note:** Следует учитывать, что изменение настроек OpenSSL напрямую
может привести к неожиданному поведению.

## uwsgi_ssl_crl

```
Syntax:  uwsgi_ssl_crl файл;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Указывает `файл` с отозванными сертификатами (CRL) в формате PEM, используемыми при [проверке](#uwsgi_ssl_verify) сертификата suwsgi-сервера.

## uwsgi_ssl_key_log

```
Syntax:  uwsgi_ssl_key_log путь;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.27.2.*

Включает логирование SSL-ключей соединений с suwsgi-сервером и указывает путь к лог-файлу ключей. Ключи записываются в формате [SSLKEYLOGFILE](https://datatracker.ietf.org/doc/html/draft-ietf-tls-keylogfile) совместимом с Wireshark.

> **Note:** Директива доступна как часть [коммерческой подписки](https://nginx.com/products/) .

## uwsgi_ssl_name

```
Syntax:  uwsgi_ssl_name имя;
Default: имя хоста из uwsgi_pass
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Позволяет переопределить имя сервера, используемое при [проверке](#uwsgi_ssl_verify) сертификата suwsgi-сервера, а также для [передачи его через SNI](#uwsgi_ssl_server_name) при установлении соединения с suwsgi-сервером.

По умолчанию используется имя хоста из [uwsgi_pass](#uwsgi_pass) .

## uwsgi_ssl_password_file

```
Syntax:  uwsgi_ssl_password_file файл;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.7.8.*

Задаёт `файл` с паролями от [секретных ключей](#uwsgi_ssl_certificate_key) , где каждый пароль указан на отдельной строке. Пароли применяются по очереди в момент загрузки ключа.

## uwsgi_ssl_protocols

```
Syntax:  uwsgi_ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3];
Default: TLSv1.2 TLSv1.3
Context: location, http, server
```

*This directive appeared in version 1.5.8.*

Разрешает указанные протоколы для запросов к suwsgi-серверу.

> **Note:** Параметр `TLSv1.3` используется по умолчанию
начиная с 1.23.4.

## uwsgi_ssl_server_name

```
Syntax:  uwsgi_ssl_server_name on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Разрешает или запрещает передачу имени сервера через [расширение Server Name Indication протокола TLS](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC 6066) при установлении соединения с suwsgi-сервером.

## uwsgi_ssl_session_reuse

```
Syntax:  uwsgi_ssl_session_reuse on | off;
Default: on
Context: location, http, server
```

*This directive appeared in version 1.5.8.*

Определяет, использовать ли повторно SSL-сессии при работе с suwsgi-сервером. Если в логах появляются ошибки “ `digest check failed` ”, то можно попробовать выключить повторное использование сессий.

## uwsgi_ssl_trusted_certificate

```
Syntax:  uwsgi_ssl_trusted_certificate файл;
Default: 
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Задаёт `файл` с доверенными сертификатами CA в формате PEM, используемыми при [проверке](#uwsgi_ssl_verify) сертификата suwsgi-сервера.

## uwsgi_ssl_verify

```
Syntax:  uwsgi_ssl_verify on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Разрешает или запрещает проверку сертификата suwsgi-сервера.

## uwsgi_ssl_verify_depth

```
Syntax:  uwsgi_ssl_verify_depth число;
Default: 1
Context: location, http, server
```

*This directive appeared in version 1.7.0.*

Устанавливает глубину проверки в цепочке сертификатов suwsgi-сервера.

## uwsgi_store

```
Syntax:  uwsgi_store on | off | строка;
Default: off
Context: location, http, server
```

Разрешает сохранение на диск файлов. Параметр `on` сохраняет файлы в соответствии с путями, указанными в директивах [alias](ngx_http_core_module.xml#alias) или [root](ngx_http_core_module.xml#root) . Параметр `off` запрещает сохранение файлов. Кроме того, имя файла можно задать явно с помощью строки с переменными:

```
uwsgi_store /data/www$original_uri;
```

Время изменения файлов выставляется согласно полученному полю `Last-Modified` в заголовке ответа. Ответ сначала записывается во временный файл, а потом этот файл переименовывается. Начиная с версии 0.8.9 временный файл и постоянное место хранения ответа могут располагаться на разных файловых системах. Однако нужно учитывать, что в этом случае вместо дешёвой операции переименовывания в пределах одной файловой системы файл копируется с одной файловой системы на другую. Поэтому лучше, если сохраняемые файлы будут находиться на той же файловой системе, что и каталог с временными файлами, задаваемый директивой [uwsgi_temp_path](#uwsgi_temp_path) для данного location.

Директиву можно использовать для создания локальных копий статических неизменяемых файлов, например, так:

```
location /images/ {
    root               /data/www;
    error_page         404 = /fetch$uri;
}

location /fetch/ {
    internal;

    uwsgi_pass         backend:9000;
    ...

    uwsgi_store        on;
    uwsgi_store_access user:rw group:rw all:r;
    uwsgi_temp_path    /data/temp;

    alias              /data/www/;
}
```

## uwsgi_store_access

```
Syntax:  uwsgi_store_access пользователи:права ...;
Default: user:rw
Context: location, http, server
```

Задаёт права доступа для создаваемых файлов и каталогов, например,

```
uwsgi_store_access user:rw group:rw all:r;
```

Если заданы какие-либо права для `group` или `all` , то права для `user` указывать необязательно:

```
uwsgi_store_access group:rw all:r;
```

## uwsgi_temp_file_write_size

```
Syntax:  uwsgi_temp_file_write_size размер;
Default: 8k|16k
Context: location, http, server
```

Ограничивает `размер` данных, сбрасываемых во временный файл за один раз, при включённой буферизации ответов uwsgi-сервера во временные файлы. По умолчанию `размер` ограничен двумя буферами, заданными директивами [uwsgi_buffer_size](#uwsgi_buffer_size) и [uwsgi_buffers](#uwsgi_buffers) . Максимальный размер временного файла задаётся директивой [uwsgi_max_temp_file_size](#uwsgi_max_temp_file_size) .

## uwsgi_temp_path

```
Syntax:  uwsgi_temp_path путь [уровень1 [уровень2 [уровень3]]];
Default: uwsgi_temp
Context: location, http, server
```

Задаёт имя каталога для хранения временных файлов с данными, полученными от uwsgi-серверов. В каталоге может использоваться иерархия подкаталогов до трёх уровней. Например, при такой конфигурации

```
uwsgi_temp_path /spool/nginx/uwsgi_temp 1 2;
```

временный файл будет следующего вида:

```
/spool/nginx/uwsgi_temp/7/45/00000123457
```

См. также параметр `use_temp_path` директивы [uwsgi_cache_path](#uwsgi_cache_path) .

