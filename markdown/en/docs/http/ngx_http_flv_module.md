# Module ngx_http_flv_module

**Revision:** 1  
**Language:** en


The `ngx_http_flv_module` module provides pseudo-streaming
server-side support for Flash Video (FLV) files.

It handles requests with the `start` argument in
the request URI’s query string specially, by sending back the contents
of a file starting from the requested byte offset and with the prepended FLV
header.

This module is not built by default, it should be enabled with the
`--with-http_flv_module`
configuration parameter.

## Example Configuration {#example}

```
location ~ \.flv$ {
    flv;
}
```

## Directives {#directives}




location


Turns on module processing in a surrounding location.


