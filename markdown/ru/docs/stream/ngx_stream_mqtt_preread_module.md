# Модуль ngx_stream_mqtt_preread_module

**Revision:** 2  
**Language:** ru


Модуль `ngx_stream_mqtt_preread_module` (1.23.4) позволяет
извлекать информацию из сообщения CONNECT
протокола Message Queuing Telemetry Transport (MQTT)
версий
[3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)
и
[5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html),
например имя пользователя или ID клиента.

> **Note:** Модуль доступен как часть
коммерческой подписки.

## Пример конфигурации {#example}

```
mqtt_preread on;
return       $mqtt_preread_clientid;
```

## Директивы {#directives}


on | off
off
stream
server


Разрешает извлечение информации из сообщения СONNECT во время фазы
предварительного чтения.



## Встроенные переменные {#variables}

***$mqtt_preread_clientid***  
  значение `clientid` из СONNECT-сообщения
***$mqtt_preread_username***  
  значение `username` из СONNECT-сообщения
