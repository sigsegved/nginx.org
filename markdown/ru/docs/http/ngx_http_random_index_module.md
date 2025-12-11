# Модуль ngx_http_random_index_module

**Revision:** 2  
**Language:** ru


Модуль `ngx_http_random_index_module` обслуживает запросы,
оканчивающиеся слэшом (‘`/`’), и выдаёт случайный
файл в качестве индексного файла каталога.
Модуль выполняется до модуля
[ngx_http_index_module](ngx_http_index_module.html).

По умолчанию этот модуль не собирается, его сборку необходимо
разрешить с помощью конфигурационного параметра
`--with-http_random_index_module`.

## Пример конфигурации {#example}

```
location / {
    random_index on;
}
```

## Директивы {#directives}


on | off
off
location


Разрешает или запрещает в содержащем location обработку этим модулем.


