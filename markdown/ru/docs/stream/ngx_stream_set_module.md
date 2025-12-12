# Модуль ngx_stream_set_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_stream_set_module` (1.19.3) позволяет устанавливать значение переменной.

# Пример конфигурации {#example}

```
server {
    listen 12345;
    set    $true 1;
}
```

# Директивы {#directives}

## set

```
Syntax:  set $переменная значение;
Default: 
Context: server
```

Устанавливает значение указанной переменной. В качестве значения можно использовать текст, переменные и их комбинации.

