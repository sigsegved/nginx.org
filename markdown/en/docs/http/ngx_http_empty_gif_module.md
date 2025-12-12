# Module ngx_http_empty_gif_module

**Revision:** 1  
**Language:** en

The `ngx_http_empty_gif_module` module emits single-pixel transparent GIF.

# Example Configuration {#example}

```
location = /_.gif {
    empty_gif;
}
```

# Directives {#directives}

## empty_gif

```
Syntax:  empty_gif;
Default: 
Context: location
```

Turns on module processing in a surrounding location.

