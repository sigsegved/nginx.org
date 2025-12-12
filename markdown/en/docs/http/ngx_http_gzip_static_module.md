# Module ngx_http_gzip_static_module

**Revision:** 2  
**Language:** en

The `ngx_http_gzip_static_module` module allows sending precompressed files with the “ `.gz` ” filename extension instead of regular files.

This module is not built by default, it should be enabled with the `--with-http_gzip_static_module` configuration parameter.

# Example Configuration {#example}

```
gzip_static  on;
gzip_proxied expired no-cache no-store private auth;
```

# Directives {#directives}

## gzip_static

```
Syntax:  on | off | always
Default: off
Context: location, http, server
```

Enables (“ `on` ”) or disables (“ `off` ”) checking the existence of precompressed files. The following directives are also taken into account: [gzip_http_version](ngx_http_gzip_module.xml#gzip_http_version) , [gzip_proxied](ngx_http_gzip_module.xml#gzip_proxied) , [gzip_disable](ngx_http_gzip_module.xml#gzip_disable) , and [gzip_vary](ngx_http_gzip_module.xml#gzip_vary) .

With the “ `always` ” value (1.3.6), gzipped file is used in all cases, without checking if the client supports it. It is useful if there are no uncompressed files on the disk anyway or the [ngx_http_gunzip_module](ngx_http_gunzip_module.xml) is used.

The files can be compressed using the `gzip` command, or any other compatible one. It is recommended that the modification date and time of original and compressed files be the same.

