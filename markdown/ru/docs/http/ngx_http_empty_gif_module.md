# Модуль ngx_http_empty_gif_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_http_empty_gif_module` выдаёт однопиксельный прозрачный GIF.

# Пример конфигурации {#example}

```
location = /_.gif {
    empty_gif;
}
```

# Директивы {#directives}

## empty_gif

```
Syntax:  empty_gif;
Default: 
Context: location
```

Разрешает в содержащем location выдавать однопиксельный прозрачный GIF.

