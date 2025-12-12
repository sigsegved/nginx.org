# Модуль ngx_http_sub_module

**Revision:** 6  
**Language:** ru

Модуль `ngx_http_sub_module` — это фильтр, изменяющий в ответе одну заданную строку на другую.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_sub_module` .

# Пример конфигурации {#example}

```
location / {
    sub_filter '<a href="http://127.0.0.1:8080/'  '<a href="https://$host/';
    sub_filter '<img src="http://127.0.0.1:8080/' '<img src="https://$host/';
    sub_filter_once on;
}
```

# Директивы {#directives}

## sub_filter

```
Syntax:  sub_filter строка замена;
Default: 
Context: location, http, server
```

Задаёт строку, которую нужно заменить, и строку замены. Заменяемая строка проверяется без учёта регистра. В заменяемой строке (1.9.4) и в строке замены можно использовать переменные. На одном уровне конфигурации может быть указано несколько директив `sub_filter` (1.9.4). Директивы наследуются с предыдущего уровня конфигурации при условии, что на данном уровне не описаны свои директивы `sub_filter` .

## sub_filter_last_modified

```
Syntax:  sub_filter_last_modified on | off;
Default: off
Context: location, http, server
```

*This directive appeared in version 1.5.1.*

Позволяет сохранить поле заголовка `Last-Modified` исходного ответа во время замены для лучшего кэширования ответов.

По умолчанию поле заголовка удаляется, так как содержимое ответа изменяется во время обработки.

## sub_filter_once

```
Syntax:  sub_filter_once on | off;
Default: on
Context: location, http, server
```

Определяет, сколько раз нужно искать каждую из заменяемых строк: один раз или многократно.

## sub_filter_types

```
Syntax:  sub_filter_types mime-тип ...;
Default: text/html
Context: location, http, server
```

Разрешает замену строк в ответах с указанными MIME-типами в дополнение к “ `text/html` ”. Специальное значение “ `*` ” соответствует любому MIME-типу (0.8.29).

