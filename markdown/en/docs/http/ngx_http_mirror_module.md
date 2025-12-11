# Module ngx_http_mirror_module

**Revision:** 4  
**Language:** en


The `ngx_http_mirror_module` module (1.13.4) implements
mirroring of an original request
by creating background mirror subrequests.
Responses to mirror subrequests are ignored.

## Example Configuration {#example}

```
location / {
    mirror /mirror;
    proxy_pass http://backend;
}

location = /mirror {
    internal;
    proxy_pass http://test_backend$request_uri;
}
```

## Directives {#directives}


uri | off
off
http
server
location


Sets the URI to which an original request will be mirrored.
Several mirrors can be specified on the same configuration level.




on | off
on
http
server
location


Indicates whether the client request body is mirrored.
When enabled, the client request body will be read
prior to creating mirror subrequests.
In this case, unbuffered client request body proxying
set by the
,
,
,
and

directives will be disabled.

location / {
    mirror /mirror;
    mirror_request_body off;
    proxy_pass http://backend;
}

location = /mirror {
    internal;
    proxy_pass http://log_backend;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
}



