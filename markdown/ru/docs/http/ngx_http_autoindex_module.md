# Модуль ngx_http_autoindex_module

**Revision:** 4  
**Language:** ru


Модуль `ngx_http_autoindex_module` обслуживает запросы,
оканчивающиеся слэшом (‘`/`’), и выдаёт листинг каталога.
Обычно запрос попадает к модулю `ngx_http_autoindex_module`,
когда модуль [ngx_http_index_module](ngx_http_index_module.html)
не нашёл индексный файл.

## Пример конфигурации {#example}

```
location / {
    autoindex on;
}
```

## Директивы {#directives}


on | off
off
http
server
location


Разрешает или запрещает вывод листинга каталога.




on | off
on
http
server
location


Для формата HTML
определяет, как выводить размеры файлов в листинге
каталога: точно или округляя до килобайт, мегабайт и гигабайт.





    html |
    xml |
    json |
    jsonp
html
http
server
location
1.7.9


Задаёт формат вывода листинга каталога.



При использовании формата JSONP имя callback-функции
задаётся в аргументе запроса callback.
Если аргумент отсутствует или имеет пустое значение,
то используется формат JSON.



Вывод в формате XML может быть преобразован при помощи модуля
ngx_http_xslt_module.




on | off
off
http
server
location


Для формата HTML
определяет, в какой временной зоне выводить время в листинге
каталога: в локальной или в UTC.


