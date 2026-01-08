# Модуль ngx_stream_return_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_stream_return_module` (1.11.2) позволяет отправить заданное значение клиенту и после этого закрыть соединение.

# Пример конфигурации {#example}

```
server {
    listen 12345;
    return $time_iso8601;
}
```

# Директивы {#directives}

## return

```
Syntax:  return значение;
Default: 
Context: server
```

Задаёт `значение` , отправляемое клиенту. В качестве значения можно использовать текст, переменные и их комбинации.

