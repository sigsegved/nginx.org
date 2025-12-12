# Модуль ngx_http_ssi_module

**Revision:** 12  
**Language:** ru

Модуль `ngx_http_ssi_module` — это фильтр, обрабатывающий команды SSI (Server Side Includes) в проходящих через него ответах. На данный момент список поддерживаемых команд SSI неполон.

# Пример конфигурации {#example}

```
location / {
    ssi on;
    ...
}
```

# Директивы {#directives}

## ssi

```
Syntax:  on | off
Default: off
Context: if в location, http, server, location
```

Разрешает или запрещает обработку команд SSI в ответах.

## ssi_last_modified

```
Syntax:  on | off
Default: off
Context: location, http, server
```

*This directive appeared in version 1.5.1.*

Позволяет сохранить поле заголовка `Last-Modified` исходного ответа во время обработки SSI для лучшего кэширования ответов.

По умолчанию поле заголовка удаляется, так как содержимое ответа изменяется во время обработки и может содержать динамически созданные элементы или части, которые изменились независимо от исходного ответа.

## ssi_min_file_chunk

```
Syntax:  размер
Default: 1k
Context: location, http, server
```

Задаёт минимальный `размер` частей ответа, хранящихся на диске, начиная с которого имеет смысл посылать их с помощью [sendfile](ngx_http_core_module.xml#sendfile) .

## ssi_silent_errors

```
Syntax:  on | off
Default: off
Context: location, http, server
```

Разрешает не выводить строку “ `[an error occurred while processing the directive]` ”, если во время обработки SSI произошла ошибка.

## ssi_types

```
Syntax:  mime-тип ...
Default: text/html
Context: location, http, server
```

Разрешает обработку команд SSI в ответах с указанными MIME-типами в дополнение к “ `text/html` ”. Специальное значение “ `*` ” соответствует любому MIME-типу (0.8.29).

## ssi_value_length

```
Syntax:  длина
Default: 256
Context: location, http, server
```

Задаёт максимальную длину значений параметров в SSI-командах.

# Команды SSI {#commands}

Общий формат команд SSI такой:

```
<!--# команда параметр1=значение1 параметр2=значение2 ... -->
```

Поддерживаются следующие команды:

**`block`**  
  Описывает блок, который можно использовать
как заглушку в команде `include` .
Внутри блока могут быть другие команды SSI.
Параметр команды:

**`name`**  
  имя блока.

  Пример:

```
<!--# block name="one" -->
заглушка
<!--# endblock -->
```

**`config`**  
  Задаёт некоторые параметры, используемые при обработке SSI, а именно:

**`errmsg`**  
  строка, выводящаяся при ошибке во время обработки SSI.
По умолчанию выводится такая строка:

```
[an error occurred while processing the directive]
```

**`timefmt`**  
  строка формата, передаваемая функции `strftime()` для вывода даты и времени.
По умолчанию используется такой формат:

```
"%A, %d-%b-%Y %H:%M:%S %Z"
```

  Для вывода времени в секундах подходит формат
“ `%s` ”.

**`echo`**  
  Выводит значение переменной.
Параметры команды:

**`var`**  
  имя переменной.

**`encoding`**  
  способ кодирования.
Возможны три значения — `none` , `url` и `entity` .
По умолчанию используется `entity` .

**`default`**  
  нестандартный параметр, задающий строку, которая выводится,
если переменная не определена.
По умолчанию выводится строка
“ `(none)` ”.
Команда

```
<!--# echo var="name" default="нет" -->
```

  заменяет такую последовательность команд:

```
<!--# if expr="$name" --><!--# echo var="name" --><!--#
       else -->нет<!--# endif -->
```

**`if`**  
  Выполняет условное включение.
Поддерживаются следующие команды:

```
<!--# if expr="..." -->
...
<!--# elif expr="..." -->
...
<!--# else -->
...
<!--# endif -->
```

  На данный момент поддерживается только один уровень вложенности.
Параметр команды:

**`expr`**  
  выражение.
В выражении может быть:

- проверка существования переменной:
  ```
<!--# if expr="$name" -->
```

- сравнение переменной с текстом:
  ```
<!--# if expr="$name = text" -->
<!--# if expr="$name != text" -->
```

- сравнение переменной с регулярным выражением:
  ```
<!--# if expr="$name = /text/" -->
<!--# if expr="$name != /text/" -->
```

  Если в `text` встречаются переменные,
то производится подстановка их значений.
В регулярном выражении можно задать позиционные и именованные выделения,
а затем использовать их через переменные, например:

```
<!--# if expr="$name = /(.+)@(?P<domain>.+)/" -->
    <!--# echo var="1" -->
    <!--# echo var="domain" -->
<!--# endif -->
```

**`include`**  
  Включает в ответ результат другого запроса.
Параметры команды:

**`file`**  
  задаёт включаемый файл, например:

```
<!--# include file="footer.html" -->
```

**`virtual`**  
  задаёт включаемый запрос, например:

```
<!--# include virtual="/remote/body.php?argument=value" -->
```

  Несколько запросов, указанных на одной странице и обрабатываемых
проксируемыми или FastCGI/uwsgi/SCGI/gRPC-серверами, работают параллельно.
Если нужна последовательная обработка, следует воспользоваться параметром `wait` .

**`stub`**  
  нестандартный параметр, задающий имя блока,
содержимое которого будет выведено, если тело ответа на включаемый запрос
пустое или если при исполнении запроса произошла ошибка, например:

```
<!--# block name="one" -->&nbsp;<!--# endblock -->
<!--# include virtual="/remote/body.php?argument=value" stub="one" -->
```

  Содержимое замещающего блока обрабатывается в контексте включаемого запроса.

**`wait`**  
  нестандартный параметр, указывающий, нужно ли ждать
полного исполнения данного запроса, прежде чем продолжать выполнение
SSI, например:

```
<!--# include virtual="/remote/body.php?argument=value" wait="yes" -->
```

**`set`**  
  нестандартный параметр, указывающий, что удачный
результат выполнения запроса нужно записать в заданную переменную,
например:

```
<!--# include virtual="/remote/body.php?argument=value" set="one" -->
```

  Максимальный размер ответа задаётся директивой [subrequest_output_buffer_size](ngx_http_core_module.xml#subrequest_output_buffer_size) (1.13.10):

```
location /remote/ {
    subrequest_output_buffer_size 64k;
    ...
}
```

  До версии 1.13.10 в переменные можно было записать только результаты
ответов, полученные через модули [ngx_http_proxy_module](ngx_http_proxy_module.xml) , [ngx_http_memcached_module](ngx_http_memcached_module.xml) , [ngx_http_fastcgi_module](ngx_http_fastcgi_module.xml) (1.5.6), [ngx_http_uwsgi_module](ngx_http_uwsgi_module.xml) (1.5.6)
и [ngx_http_scgi_module](ngx_http_scgi_module.xml) (1.5.6).
Максимальный размер ответа задавался при помощи директив [proxy_buffer_size](ngx_http_proxy_module.xml#proxy_buffer_size) , [memcached_buffer_size](ngx_http_memcached_module.xml#memcached_buffer_size) , [fastcgi_buffer_size](ngx_http_fastcgi_module.xml#fastcgi_buffer_size) , [uwsgi_buffer_size](ngx_http_uwsgi_module.xml#uwsgi_buffer_size) и [scgi_buffer_size](ngx_http_scgi_module.xml#scgi_buffer_size) .

**`set`**  
  Присваивает значение переменной.
Параметры команды:

**`var`**  
  имя переменной.

**`value`**  
  значение переменной.
Если в присваиваемом значении есть переменные,
то производится подстановка их значений.

# Встроенные переменные {#variables}

Модуль `ngx_http_ssi_module` поддерживает две встроенные переменные:

**`$date_local`**  
  текущее время в локальной временной зоне.
Формат задаётся командой `config` с параметром `timefmt` .

**`$date_gmt`**  
  текущее время в GMT.
Формат задаётся командой `config` с параметром `timefmt` .

