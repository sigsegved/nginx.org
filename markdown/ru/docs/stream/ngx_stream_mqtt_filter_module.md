# Модуль ngx_stream_mqtt_filter_module

**Revision:** 2  
**Language:** ru


Модуль `ngx_stream_mqtt_filter_module` (1.23.4) обеспечивает
поддержку протокола Message Queuing Telemetry Transport (MQTT)
версий
[3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)
и
[5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html).

> **Note:** Модуль доступен как часть
коммерческой подписки.

## Пример конфигурации {#example}

```
listen            127.0.0.1:18883;
proxy_pass        backend;
proxy_buffer_size 16k;

mqtt             on;
mqtt_set_connect clientid "$client";
mqtt_set_connect username "$name";
```

## Директивы {#directives}


on | off
off
stream
server


Включает протокол MQTT для данного виртуального сервера.




число размер
100 1k
stream
server
1.25.1


Задаёт число и размер буферов,
необходимых для обработки MQTT-сообщений,
для одного соединения.




размер
4k|8k
server



Эта директива устарела начиная с версии 1.25.1.
Вместо неё следует использовать директиву
.




Задаёт размер буфера,
в который будет записываться модифицированное сообщение.
По умолчанию размер одного буфера равен размеру страницы памяти.
В зависимости от платформы это или 4K, или 8K,
однако его можно сделать меньше.




поле значение

server


Устанавливает поле
в заданное значение для сообщения CONNECT.
Поддерживаются следующие поля:
clientid,
username и
password.
В качестве значения можно использовать текст, переменные и их комбинации.



На одном уровне может быть указано
несколько директив mqtt_set_connect:

mqtt_set_connect clientid "$client";
mqtt_set_connect username "$name";



