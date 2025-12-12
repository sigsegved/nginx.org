# Модуль ngx_http_js_module

**Revision:** 54  
**Language:** ru

Модуль `ngx_http_js_module` позволяет задавать обработчики location и переменных на [njs](../njs/index.xml) — подмножестве языка JavaScript.

Инструкция по сборке и установке доступны [здесь](../njs/install.xml) .

# Пример конфигурации {#example}

Пример работает начиная с версии [0.4.0](../njs/changes.xml#njs0.4.0) .

```
http {
    js_import http.js;

    js_set $foo     http.foo;
    js_set $summary http.summary;
    js_set $hash    http.hash;

    resolver 10.0.0.1;

    server {
        listen 8000;

        location / {
            add_header X-Foo $foo;
            js_content http.baz;
        }

        location = /summary {
            return 200 $summary;
        }

        location = /hello {
            js_content http.hello;
        }

        # начиная с версии 0.7.0
        location = /fetch {
            js_content                   http.fetch;
            js_fetch_trusted_certificate /path/to/ISRG_Root_X1.pem;
        }

        # начиная с версии 0.7.0
        location = /crypto {
            add_header Hash $hash;
            return     200;
        }
    }
}
```

Файл `http.js` :

```
function foo(r) {
    r.log("hello from foo() handler");
    return "foo";
}

function summary(r) {
    var a, s, h;

    s = "JS summary\n\n";

    s += "Method: " + r.method + "\n";
    s += "HTTP version: " + r.httpVersion + "\n";
    s += "Host: " + r.headersIn.host + "\n";
    s += "Remote Address: " + r.remoteAddress + "\n";
    s += "URI: " + r.uri + "\n";

    s += "Headers:\n";
    for (h in r.headersIn) {
        s += "  header '" + h + "' is '" + r.headersIn[h] + "'\n";
    }

    s += "Args:\n";
    for (a in r.args) {
        s += "  arg '" + a + "' is '" + r.args[a] + "'\n";
    }

    return s;
}

function baz(r) {
    r.status = 200;
    r.headersOut.foo = 1234;
    r.headersOut['Content-Type'] = "text/plain; charset=utf-8";
    r.headersOut['Content-Length'] = 15;
    r.sendHeader();
    r.send("nginx");
    r.send("java");
    r.send("script");

    r.finish();
}

function hello(r) {
    r.return(200, "Hello world!");
}

// начиная с версии 0.7.0
async function fetch(r) {
    let results = await Promise.all([ngx.fetch('https://nginx.org/'),
                                     ngx.fetch('https://nginx.org/en/')]);

    r.return(200, JSON.stringify(results, undefined, 4));
}

// начиная с версии 0.7.0
async function hash(r) {
    let hash = await crypto.subtle.digest('SHA-512', r.headersIn.host);
    r.setReturnValue(Buffer.from(hash).toString('hex'));
}

export default {foo, summary, baz, hello, fetch, hash};
```

# Директивы {#directives}

## js_body_filter

```
Syntax:  функция | модуль.функция [buffer_type=string | buffer]
Default: 
Context: limit_except, location, if in location
```

*This directive appeared in version 0.5.2.*

Задаёт функцию njs в качестве фильтра тела ответа. Функция фильтра вызывается для каждого блока данных тела ответа со следующими аргументами:

**`r`**  
  объект [HTTP request](../njs/reference.xml#http)

**`data`**  
  входящий блок данных
может быть строкой или буфером
в зависимости от значения `buffer_type` ,
по умолчанию является строкой.
Начиная с [0.8.5](../njs/changes.xml#njs0.8.5) ,
по умолчанию
значение `data` неявно преобразуется в валидную строку UTF-8.
Для бинарных данных параметр `buffer_type` необходимо установить в `buffer` .

**`flags`**  
  объект со следующими свойствами:

**`last`**  
  логическое значение, true, если данные являются последним буфером.

Функция фильтра может передавать свою модифицированную версию входящего блока данных следующему фильтру тела ответа при помощи вызова [`r.sendBuffer()`](../njs/reference.xml#r_sendbuffer) . Пример преобразования букв в нижний регистр в теле ответа:

```
function filter(r, data, flags) {
    r.sendBuffer(data.toLowerCase(), flags);
}
```

Для отмены фильтра (блоки данных будут передаваться клиенту без вызова `js_body_filter` ), можно использовать [`r.done()`](../njs/reference.xml#r_done) .

Если функция фильтра изменяет длину тела ответа, то необходимо очистить заголовок ответа `Content-Length` (если присутствует) в [`js_header_filter`](#js_header_filter) , чтобы применить поблочное кодирование.

> **Note:** Так как обработчик `js_body_filter` должен сразу возвращать результат,
то поддерживаются только синхронные операции,
Таким образом, асинхронные операции, например [r.subrequest()](../njs/reference.xml#r_subrequest) или [setTimeout()](../njs/reference.xml#settimeout) ,
не поддерживаются.

> **Note:** Директива может быть указана внутри
блока [if](../http/ngx_http_rewrite_module.xml#if) начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_content

```
Syntax:  функция | модуль.функция
Default: 
Context: limit_except, location, if in location
```

Задаёт функцию njs в качестве обработчика содержимого location. Начиная с версии [0.4.0](../njs/changes.xml#njs0.4.0) можно ссылаться на функцию модуля.

> **Note:** Директива может быть указана внутри
блока [if](../http/ngx_http_rewrite_module.xml#if) начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_context_reuse

```
Syntax:  число
Default: 128
Context: location, http, server
```

*This directive appeared in version 0.8.6.*

Задаёт максимальное число контекстов JS для повторного использования [движке QuickJS](../njs/engine.xml) . Каждый контекст используется для одного запроса. Завершённый контекст помещается в пул повторно используемых контекстов. Если пул заполнен, контекст уничтожается.

## js_engine

```
Syntax:  njs | qjs
Default: njs
Context: location, http, server
```

*This directive appeared in version 0.8.6.*

Задаёт [движок JavaScript](../njs/engine.xml) для использования в сценариях njs. Параметр `njs` задаёт использование движка njs, также используемого по умолчанию. Параметр `qjs` задаёт использование движка QuickJS.

## js_fetch_buffer_size

```
Syntax:  размер
Default: 16k
Context: location, http, server
```

*This directive appeared in version 0.7.4.*

Задаёт `размер` буфера, который будет использоваться для чтения и записи для [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_ciphers

```
Syntax:  шифры
Default: HIGH:!aNULL:!MD5
Context: location, http, server
```

*This directive appeared in version 0.7.0.*

Описывает разрешённые шифры для HTTPS-запросов при помощи [Fetch API](../njs/reference.xml#ngx_fetch) . Шифры задаются в формате, поддерживаемом библиотекой OpenSSL.

Полный список можно посмотреть с помощью команды “ `openssl ciphers` ”.

## js_fetch_max_response_buffer_size

```
Syntax:  размер
Default: 1m
Context: location, http, server
```

*This directive appeared in version 0.7.4.*

Задаёт максимальный `размер` ответа, полученного при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_protocols

```
Syntax:  [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3]
Default: TLSv1 TLSv1.1 TLSv1.2
Context: location, http, server
```

*This directive appeared in version 0.7.0.*

Разрешает указанные протоколы для HTTPS-запросов при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_timeout

```
Syntax:  время
Default: 60s
Context: location, http, server
```

*This directive appeared in version 0.7.4.*

Задаёт таймаут при чтении и записи при помощи [Fetch API](../njs/reference.xml#ngx_fetch) . Таймаут устанавливается не на всю передачу ответа, а только между двумя операциями чтения. Если по истечении этого времени данные не передавались, соединение закрывается.

## js_fetch_trusted_certificate

```
Syntax:  файл
Default: 
Context: location, http, server
```

*This directive appeared in version 0.7.0.*

Задаёт `файл` с доверенными сертификатами CA в формате PEM, используемыми при [проверке](../njs/reference.xml#fetch_verify) HTTPS-сертификата при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_verify

```
Syntax:  on | off
Default: on
Context: location, http, server
```

*This directive appeared in version 0.7.4.*

Разрешает или запрещает проверку сертификата HTTPS-сервера при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_verify_depth

```
Syntax:  число
Default: 100
Context: location, http, server
```

*This directive appeared in version 0.7.0.*

Устанавливает глубину проверки в цепочке HTTPS-сертификатов при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_proxy

```
Syntax:  url
Default: 
Context: location, http, server
```

*This directive appeared in version 0.9.4.*

Задаёт URL прямого прокси-сервера при помощи [Fetch API](../njs/reference.xml#ngx_fetch) . `url` поддерживает только схему HTTP и может содержать необязательные учётные данные пользователя в формате `http://[user:password@]host:port` для базовой аутентификации. Поддерживает как HTTP, так и HTTPS соединения с серверами назначения. Если `url` пустой, маршрутизация через прокси отключается. Значение параметра может содержать переменные.

Пример:

```
location /fetch {
    js_fetch_proxy http://user:pass@proxy.example.com:3128;
    js_content main.fetch_handler;
}
```

## js_fetch_keepalive

```
Syntax:  соединения
Default: 0
Context: location, http, server
```

*This directive appeared in version 0.9.2.*

Активирует кэш для соединений с серверами назначения. Если значение больше `0` , включает keepalive-соединения для [Fetch API](../njs/reference.xml#ngx_fetch) .

Параметр `соединения` задаёт максимальное количество неактивных keepalive-соединений с серверами назначения, которые сохраняются в кэше каждого рабочего процесса. Если это количество превышено, наименее недавно использованные соединения закрываются.

Пример:

```
location /fetch {
    js_fetch_keepalive 32;
    js_fetch_trusted_certificate /path/to/ISRG_Root_X1.pem;
    js_content main.fetch_handler;
}
```

## js_fetch_keepalive_requests

```
Syntax:  число
Default: 1000
Context: location, http, server
```

*This directive appeared in version 0.9.2.*

Задаёт максимальное количество запросов, которые могут быть обслужены через одно keepalive-соединение при помощи [Fetch API](../njs/reference.xml#ngx_fetch) . После выполнения максимального количества запросов соединение закрывается.

Периодическое закрытие соединений необходимо для освобождения выделенной под соединение памяти. Поэтому использование слишком большого максимального количества запросов может привести к чрезмерному потреблению памяти и не рекомендуется.

## js_fetch_keepalive_time

```
Syntax:  время
Default: 1h
Context: location, http, server
```

*This directive appeared in version 0.9.2.*

Ограничивает максимальное время, в течение которого запросы могут обрабатываться через одно keepalive-соединение при помощи [Fetch API](../njs/reference.xml#ngx_fetch) . По истечении этого времени соединение закрывается после обработки очередного запроса.

## js_fetch_keepalive_timeout

```
Syntax:  время
Default: 60s
Context: location, http, server
```

*This directive appeared in version 0.9.2.*

Задаёт таймаут, в течение которого неактивное keepalive-соединение с сервером назначения остается открытым при помощи [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_header_filter

```
Syntax:  функция | модуль.функция
Default: 
Context: limit_except, location, if in location
```

*This directive appeared in version 0.5.1.*

Задаёт функцию njs в качестве фильтра заголовка ответа. Директива позволяет менять произвольные поля заголовка ответа.

> **Note:** Так как обработчик `js_header_filter` должен сразу возвращать результат,
то поддерживаются только синхронные операции,
Таким образом, асинхронные операции, например [r.subrequest()](../njs/reference.xml#r_subrequest) или [setTimeout()](../njs/reference.xml#settimeout) ,
не поддерживаются.

> **Note:** Директива может быть указана внутри
блока [if](../http/ngx_http_rewrite_module.xml#if) начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_import

```
Syntax:  модуль.js | имя_экспорта from модуль.js
Default: 
Context: location, http, server
```

*This directive appeared in version 0.4.0.*

Импортирует модуль, позволяющий задавать обработчики location и переменных на njs. `Имя_экспорта` является пространством имён при доступе к функциям модуля. Если `имя_экспорта` не задано, то пространством имён будет являться имя модуля.

```
js_import http.js;
```

В примере при доступе к экспорту в качестве пространства имён используется имя модуля `http` . Если импортируемый модуль экспортирует `foo()` , то для доступа используется `http.foo` .

Директив `js_import` может быть несколько.

> **Note:** Директива может быть указана
на уровне `server` и `location` начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_include

```
Syntax:  файл
Default: 
Context: http
```

Задаёт файл, позволяющий задавать обработчики location и переменных на njs:

```
nginx.conf:
js_include http.js;
location   /version {
    js_content version;
}

http.js:
function version(r) {
    r.return(200, njs.version);
}
```

Директива устарела в версии [0.4.0](../njs/changes.xml#njs0.4.0) и была удалена в версии [0.7.1](../njs/changes.xml#njs0.7.1) . Вместо неё следует использовать директиву [js_import](#js_import) .

## js_path

```
Syntax:  путь
Default: 
Context: location, http, server
```

*This directive appeared in version 0.3.0.*

Задаёт дополнительный путь для модулей njs.

> **Note:** Директива может быть указана
на уровне `server` и `location` начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_periodic

```
Syntax:  функция | модуль.функция [interval=время] [jitter=число] [worker_affinity=маска]
Default: 
Context: location
```

*This directive appeared in version 0.8.1.*

Задаёт периодичность запуска обработчика содержимого. В качестве первого аргумента обработчик получает [объект сессии](../njs/reference.xml#periodic_session) , также у обработчика есть доступ к глобальным объектам таким как [ngx](../njs/reference.xml#ngx) .

Необязательный параметр `interval` задаёт интервал между двумя последовательными запусками, по умолчанию 5 секунд.

Необязательный параметр `jitter` задаёт время, в пределах которого случайным образом задерживается каждый запуск, по умолчанию задержки нет.

По умолчанию `js_handler` выполняется для рабочего процесса 0. Необязательный параметр `worker_affinity` позволяет указать рабочий процесс, для которого будет выполняться обработчик содержимого location. Рабочие процессы задаются битовой маской разрешённых к использованию рабочих процессов. Маска `all` позволяет обработчику выполняться для всех рабочих процессов.

Пример:

```
example.conf:

location @periodics {
    # интервал выполнения 1 минута для рабочего процесса 0
    js_periodic main.handler interval=60s;

    # интервал выполнения 1 минута для всех рабочих процессов
    js_periodic main.handler interval=60s worker_affinity=all;

    # интервал выполнения 1 минута для рабочих процессов 1 и 3
    js_periodic main.handler interval=60s worker_affinity=0101;

    resolver 10.0.0.1;
    js_fetch_trusted_certificate /path/to/ISRG_Root_X1.pem;
}

example.js:

async function handler(s) {
    let reply = await ngx.fetch('https://nginx.org/en/docs/njs/');
    let body = await reply.text();

    ngx.log(ngx.INFO, body);
}
```

## js_preload_object

```
Syntax:  имя.json | имя from файл.json
Default: 
Context: location, http, server
```

*This directive appeared in version 0.7.8.*

Предварительно загружает [неизменяемый объект](../njs/preload_objects.xml) во время конфигурации. `Имя` используется в качестве имени глобальной переменной, через которую объект доступен в коде njs. Если `имя` не указано, то будет использоваться имя файла.

```
js_preload_object map.json;
```

В примере `map` используется в качестве имени во время доступа к предварительно загруженному объекту.

Директив `js_preload_object` может быть несколько.

## js_set

```
Syntax:  $переменная функция | модуль.функция [nocache]
Default: 
Context: location, http, server
```

Задаёт `функцию` njs для указанной `переменной` . Начиная с [0.4.0](../njs/changes.xml#njs0.4.0) можно ссылаться на функцию модуля.

Функция вызывается в момент первого обращения к переменной для данного запроса. Точный момент вызова функции зависит от [фазы](../dev/development_guide.xml#http_phases) , в которой происходит обращение к переменной. Это можно использовать для реализации дополнительной логики, не относящейся к вычислению переменной. Например, если переменная указана в директиве [log_format](ngx_http_log_module.xml#log_format) , то её обработчик не будет выполняться до фазы записи в лог. Этот обработчик также может использоваться для выполнения процедур непосредственно перед освобождением запроса.

Начиная с [0.8.6](../njs/changes.xml#njs0.8.6) , если указан необязательный параметр `nocache` , то обработчик выполняется каждый раз при обращении к переменной. Из-за ограничения модуля [rewrite](ngx_http_rewrite_module.xml) при обращении к `nocache` -переменной при помощи директивы [set](ngx_http_rewrite_module.xml#set) , обработчик должен возвращать значение фиксированной длины.

> **Note:** Так как обработчик `js_set` должен сразу возвращать результат,
то поддерживаются только синхронные операции,
Таким образом, асинхронные операции, например [r.subrequest()](../njs/reference.xml#r_subrequest) или [setTimeout()](../njs/reference.xml#settimeout) ,
не поддерживаются.

> **Note:** Директива может быть указана
на уровне `server` и `location` начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_shared_dict_zone

```
Syntax:  zone=имя:размер [timeout=время] [type=строка|число] [evict]
Default: 
Context: http
```

*This directive appeared in version 0.8.0.*

Задаёт `имя` и `размер` зоны разделяемой памяти, в которой хранится [словарь](../njs/reference.xml#dict) ключей и значений, разделяемый между рабочими процессами.

По умолчанию в качестве ключа и значения используется строка. Необязательный параметр `type` позволяет изменить тип значения на число.

Необязательный параметр `timeout` задаёт время в миллисекундах, по завершении которого все записи в словаре удаляются из зоны. Если для части записей требуется другое время удаления, его можно задать при помощи аргумента `timeout` методов [add](../njs/reference.xml#dict_add) , [incr](../njs/reference.xml#dict_incr) и [set](../njs/reference.xml#dict_set) ( [0.8.5](../njs/changes.xml#njs0.8.5) ).

Необязательный параметр `evict` удаляет самую старую пару ключ-значение при переполнении зоны.

Пример:

```
example.conf:
    # Создаётся словарь размером 1Мб со строковыми значениями,
    # пары ключ-значение удаляются при отсутствии активности в течение 60 секунд:
    js_shared_dict_zone zone=foo:1M timeout=60s;

    # Создаётся словарь размером 512Кб со строковыми значениями,
    # удаляется самая старая пара ключ-значение при переполнении зоны:
    js_shared_dict_zone zone=bar:512K timeout=30s evict;

    # Создаётся постоянный словарь размером 32Кб с числовыми значениями:
    js_shared_dict_zone zone=num:32k type=number;

example.js:
    function get(r) {
        r.return(200, ngx.shared.foo.get(r.args.key));
    }

    function set(r) {
        r.return(200, ngx.shared.foo.set(r.args.key, r.args.value));
    }

    function del(r) {
        r.return(200, ngx.shared.bar.delete(r.args.key));
    }

    function increment(r) {
        r.return(200, ngx.shared.num.incr(r.args.key, 2));
    }
```

## js_var

```
Syntax:  $переменная [значение]
Default: 
Context: location, http, server
```

*This directive appeared in version 0.5.3.*

Объявляет [перезаписываемую](../njs/reference.xml#r_variables) переменную. В качестве значения можно использовать текст, переменные и их комбинации. Переменная не перезаписывается после перенаправления, в отличие от переменных, созданных при помощи директивы [set](ngx_http_rewrite_module.xml#set) .

> **Note:** Директива может быть указана
на уровне `server` и `location` начиная с [0.7.7](../njs/changes.xml#njs0.7.7) .

# Аргумент запроса {#arguments}

Каждый HTTP-обработчик njs получает один аргумент, [объект](../njs/reference.xml#http) запроса.

