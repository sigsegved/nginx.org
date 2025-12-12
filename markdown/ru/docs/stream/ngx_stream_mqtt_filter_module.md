# Модуль ngx_stream_mqtt_filter_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_stream_mqtt_filter_module` (1.23.4) обеспечивает поддержку протокола Message Queuing Telemetry Transport (MQTT) версий [3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html) и [5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) .

> **Note:** Модуль доступен как часть [коммерческой подписки](https://nginx.com/products/) .

# Пример конфигурации {#example}

```
listen            127.0.0.1:18883;
proxy_pass        backend;
proxy_buffer_size 16k;

mqtt             on;
mqtt_set_connect clientid "$client";
mqtt_set_connect username "$name";
```

# Директивы {#directives}

## mqtt

```
Syntax:  mqtt on | off;
Default: off
Context: server, stream
```

Включает протокол MQTT для данного виртуального сервера.

## mqtt_buffers

```
Syntax:  mqtt_buffers число размер;
Default: 100 1k
Context: server, stream
```

*This directive appeared in version 1.25.1.*

Задаёт `число` и `размер` буферов, необходимых для обработки MQTT-сообщений, для одного соединения.

## mqtt_rewrite_buffer_size

```
Syntax:  mqtt_rewrite_buffer_size размер;
Default: 4k|8k
Context: server
```

> **Note:** Эта директива устарела начиная с версии 1.25.1.
Вместо неё следует использовать директиву [mqtt_buffers](#mqtt_buffers) .

Задаёт `размер` буфера, в который будет записываться модифицированное сообщение. По умолчанию размер одного буфера равен размеру страницы памяти. В зависимости от платформы это или 4K, или 8K, однако его можно сделать меньше.

## mqtt_set_connect

```
Syntax:  mqtt_set_connect поле значение;
Default: 
Context: server
```

Устанавливает `поле` в заданное `значение` для сообщения CONNECT. Поддерживаются следующие поля: `clientid` , `username` и `password` . В качестве значения можно использовать текст, переменные и их комбинации.

На одном уровне может быть указано несколько директив `mqtt_set_connect` :

```
mqtt_set_connect clientid "$client";
mqtt_set_connect username "$name";
```

