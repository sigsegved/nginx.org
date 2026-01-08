# Module ngx_http_gunzip_module

**Revision:** 2  
**Language:** en

The `ngx_http_gunzip_module` module is a filter that decompresses responses with “ `Content-Encoding: gzip` ” for clients that do not support “gzip” encoding method. The module will be useful when it is desirable to store data compressed to save space and reduce I/O costs.

This module is not built by default, it should be enabled with the `--with-http_gunzip_module` configuration parameter.

# Example Configuration {#example}

```
location /storage/ {
    gunzip on;
    ...
}
```

# Directives {#directives}

## gunzip

```
Syntax:  gunzip on | off;
Default: off
Context: location, http, server
```

Enables or disables decompression of gzipped responses for clients that lack gzip support. If enabled, the following directives are also taken into account when determining if clients support gzip: [gzip_http_version](ngx_http_gzip_module.xml#gzip_http_version) , [gzip_proxied](ngx_http_gzip_module.xml#gzip_proxied) , and [gzip_disable](ngx_http_gzip_module.xml#gzip_disable) . See also the [gzip_vary](ngx_http_gzip_module.xml#gzip_vary) directive.

## gunzip_buffers

```
Syntax:  gunzip_buffers number size;
Default: 32 4k|16 8k
Context: location, http, server
```

Sets the `number` and `size` of buffers used to decompress a response. By default, the buffer size is equal to one memory page. This is either 4K or 8K, depending on a platform.

