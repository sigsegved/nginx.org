# nginx JavaScript module

**Revision:** 36  
**Language:** en


njs is an nginx module that extends the server's functionality through
JavaScript scripting, enabling the creation of custom
server-side logic and more.

- [install.html](install.html)
- [changes.html](changes.html)
- [reference.html](reference.html)
- [engine.html](engine.html)
- [Examples](https://github.com/nginx/njs-examples/)
- [security.html](security.html)
- [compatibility.html](compatibility.html)
- [cli.html](cli.html)
- [preload_objects.html](preload_objects.html)
- Tested OS and platforms

- [
ngx_http_js_module](../http/ngx_http_js_module.html)
- [
ngx_stream_js_module](../stream/ngx_stream_js_module.html)

- [typescript.html](typescript.html)
- [node_modules.html](node_modules.html)

## Use cases {#usecases}

- Complex access control and security checks in njs
before a request reaches an upstream server
- Manipulating response headers
- Writing flexible asynchronous content handlers and filters

See [examples](https://github.com/nginx/njs-examples/)
for more njs use cases.

## Basic HTTP Example {#example}

To use njs in nginx:

- install njs scripting language
- create an njs script file, for example, http.js.
See Reference
for the list of njs properties and methods.

function hello(r) {
    r.return(200, "Hello world!");
}

export default {hello};
- in the nginx.conf file, enable
ngx_http_js_module module
and specify the
js_import
directive
with the http.js script file:

load_module modules/ngx_http_js_module.so;

events {}

http {
    js_import http.js;

    server {
        listen 8000;

        location / {
            js_content http.hello;
        }
    }
}

There is also a standalone [command line](cli.html) utility
that can be used independently of nginx for njs development and debugging.

## Tested OS and platforms {#tested_os_and_platforms}

- FreeBSD / amd64;
- Linux / x86, amd64, arm64, ppc64el;
- Solaris 11 / amd64;
- macOS / x86_64;

## Presentation at nginx.conf 2018 {#presentation}

