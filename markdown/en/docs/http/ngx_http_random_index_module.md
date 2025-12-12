# Module ngx_http_random_index_module

**Revision:** 2  
**Language:** en

The `ngx_http_random_index_module` module processes requests ending with the slash character (‘ `/` ’) and picks a random file in a directory to serve as an index file. The module is processed before the [ngx_http_index_module](ngx_http_index_module.xml) module.

This module is not built by default, it should be enabled with the `--with-http_random_index_module` configuration parameter.

# Example Configuration {#example}

```
location / {
    random_index on;
}
```

# Directives {#directives}

## random_index

```
Syntax:  random_index on | off;
Default: off
Context: location
```

Enables or disables module processing in a surrounding location.

