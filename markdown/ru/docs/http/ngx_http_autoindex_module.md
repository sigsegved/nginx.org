# Модуль ngx_http_autoindex_module

**Revision:** 4  
**Language:** ru

Модуль `ngx_http_autoindex_module` обслуживает запросы, оканчивающиеся слэшом (‘ `/` ’), и выдаёт листинг каталога. Обычно запрос попадает к модулю `ngx_http_autoindex_module` , когда модуль [ngx_http_index_module](ngx_http_index_module.xml) не нашёл индексный файл.

# Пример конфигурации {#example}

```
location / {
    autoindex on;
}
```

# Директивы {#directives}

## autoindex

```
Syntax:  autoindex on | off;
Default: off
Context: location, http, server
```

Разрешает или запрещает вывод листинга каталога.

## autoindex_exact_size

```
Syntax:  autoindex_exact_size on | off;
Default: on
Context: location, http, server
```

Для [формата](#autoindex_format) HTML определяет, как выводить размеры файлов в листинге каталога: точно или округляя до килобайт, мегабайт и гигабайт.

## autoindex_format

```
Syntax:  autoindex_format html | xml | json | jsonp;
Default: html
Context: location, http, server
```

*This directive appeared in version 1.7.9.*

Задаёт формат вывода листинга каталога.

При использовании формата JSONP имя callback-функции задаётся в аргументе запроса `callback` . Если аргумент отсутствует или имеет пустое значение, то используется формат JSON.

Вывод в формате XML может быть преобразован при помощи модуля [ngx_http_xslt_module](ngx_http_xslt_module.xml) .

## autoindex_localtime

```
Syntax:  autoindex_localtime on | off;
Default: off
Context: location, http, server
```

Для [формата](#autoindex_format) HTML определяет, в какой временной зоне выводить время в листинге каталога: в локальной или в UTC.

