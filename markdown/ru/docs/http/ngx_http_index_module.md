# Модуль ngx_http_index_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_http_index_module` обслуживает запросы, оканчивающиеся слэшом (‘ `/` ’). Такие запросы также могут обслуживаться модулями [ngx_http_autoindex_module](ngx_http_autoindex_module.xml) и [ngx_http_random_index_module](ngx_http_random_index_module.xml) .

# Пример конфигурации {#example}

```
location / {
    index index.$geo.html index.html;
}
```

# Директивы {#directives}

## index

```
Syntax:  файл ...
Default: index.html
Context: location, http, server
```

Определяет файлы, которые будут использоваться в качестве индекса. В имени файла можно использовать переменные. Наличие файлов проверяется в порядке их перечисления. В конце списка может стоять файл с абсолютным путём. Пример:

```
index index.$geo.html index.0.html /index.html;
```

Необходимо иметь в виду, что при использовании индексного файла делается внутреннее перенаправление и запрос может быть обработан уже в другом location’е. Например, в такой конфигурации:

```
location = / {
    index index.html;
}

location / {
    ...
}
```

запрос “ `/` ” будет фактически обработан во втором location’е как “ `/index.html` ”.

