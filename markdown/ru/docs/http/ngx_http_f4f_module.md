# Модуль ngx_http_f4f_module

**Revision:** 1  
**Language:** ru


Модуль `ngx_http_f4f_module` обеспечивает
серверную поддержку протокола Adobe HTTP Dynamic Streaming (HDS).

Модуль предоставляет возможность обработки запросов HTTP Dynamic Streaming в
виде “`/videoSeg1-Frag1`”, т.е. извлечения необходимого фрагмента
из `videoSeg1.f4f` при помощи
индексного файла `videoSeg1.f4x`.
Модуль является альтернативой модулю Adobe f4f (HTTP Origin Module)
для Apache.

Необходима предварительная обработка данных при помощи Adobe f4fpackager,
дополнительную информацию см. в соответствующей документации.

> **Note:** Модуль доступен как часть
коммерческой подписки.

## Пример конфигурации {#example}

```
location /video/ {
    f4f;
    ...
}
```

## Директивы {#directives}




location


Включает обработку данным модулем во вложенном location.




размер
512k
http
server
location


Задаёт размер буфера, в который будет
читаться индексный файл .f4x.


