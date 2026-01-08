# Модуль ngx_http_addition_module

**Revision:** 4  
**Language:** ru

Модуль `ngx_http_addition_module` — это фильтр, добавляющий текст до и после ответа. По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_addition_module` .

# Пример конфигурации {#example}

```
location / {
    add_before_body /before_action;
    add_after_body  /after_action;
}
```

# Директивы {#directives}

## add_before_body

```
Syntax:  add_before_body uri;
Default: 
Context: location, http, server
```

Добавляет перед телом ответа текст, выдаваемый в результате работы заданного подзапроса. Пустая строка ( `""` ) в качестве параметра отменяет добавление, унаследованное с предыдущего уровня конфигурации.

## add_after_body

```
Syntax:  add_after_body uri;
Default: 
Context: location, http, server
```

Добавляет после тела ответа текст, выдаваемый в результате работы заданного подзапроса. Пустая строка ( `""` ) в качестве параметра отменяет добавление, унаследованное с предыдущего уровня конфигурации.

## addition_types

```
Syntax:  addition_types mime-тип ...;
Default: text/html
Context: location, http, server
```

*This directive appeared in version 0.7.9.*

Разрешает добавлять текст в ответах с указанными MIME-типами в дополнение к “ `text/html` ”. Специальное значение “ `*` ” соответствует любому MIME-типу (0.8.29).

