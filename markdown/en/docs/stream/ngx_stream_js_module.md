# Module ngx_stream_js_module

**Revision:** 53  
**Language:** en

The `ngx_stream_js_module` module is used to implement handlers in [njs](../njs/index.xml) — a subset of the JavaScript language.

Download and install instructions are available [here](../njs/install.xml) .

# Example Configuration {#example}

The example works since [0.4.0](../njs/changes.xml#njs0.4.0) .

```
stream {
    js_import stream.js;

    js_set $bar stream.bar;
    js_set $req_line stream.req_line;

    server {
        listen 12345;

        js_preread stream.preread;
        return     $req_line;
    }

    server {
        listen 12346;

        js_access  stream.access;
        proxy_pass 127.0.0.1:8000;
        js_filter  stream.header_inject;
    }
}

http {
    server {
        listen 8000;
        location / {
            return 200 $http_foo\n;
        }
    }
}
```

The `stream.js` file:

```
var line = '';

function bar(s) {
    var v = s.variables;
    s.log("hello from bar() handler!");
    return "bar-var" + v.remote_port + "; pid=" + v.pid;
}

function preread(s) {
    s.on('upload', function (data, flags) {
        var n = data.indexOf('\n');
        if (n != -1) {
            line = data.substr(0, n);
            s.done();
        }
    });
}

function req_line(s) {
    return line;
}

// Read HTTP request line.
// Collect bytes in 'req' until
// request line is read.
// Injects HTTP header into a client's request

var my_header =  'Foo: foo';
function header_inject(s) {
    var req = '';
    s.on('upload', function(data, flags) {
        req += data;
        var n = req.search('\n');
        if (n != -1) {
            var rest = req.substr(n + 1);
            req = req.substr(0, n + 1);
            s.send(req + my_header + '\r\n' + rest, flags);
            s.off('upload');
        }
    });
}

function access(s) {
    if (s.remoteAddress.match('^192.*')) {
        s.deny();
        return;
    }

    s.allow();
}

export default {bar, preread, req_line, header_inject, access};
```

# Directives {#directives}

## js_access

```
Syntax:  module.function
Default: 
Context: server, stream
```

Sets an njs function which will be called at the [access](stream_processing.xml#access_phase) phase. Since [0.4.0](../njs/changes.xml#njs0.4.0) , a module function can be referenced.

The function is called once at the moment when the stream session reaches the [access](stream_processing.xml#access_phase) phase for the first time. The function is called with the following arguments:

**`s`**  
  the [Stream Session](../njs/reference.xml#stream) object

At this phase, it is possible to perform initialization or register a callback with the [`s.on()`](../njs/reference.xml#s_on) method for each incoming data chunk until one of the following methods are called: [`s.allow()`](../njs/reference.xml#s_allow) , [`s.decline()`](../njs/reference.xml#s_decline) , [`s.done()`](../njs/reference.xml#s_done) . As soon as one of these methods is called, the stream session processing switches to the [next phase](stream_processing.xml) and all current [`s.on()`](../njs/reference.xml#s_on) callbacks are dropped.

## js_context_reuse

```
Syntax:  number
Default: 128
Context: server, stream
```

*This directive appeared in version 0.8.6.*

Sets a maximum number of JS context to be reused for [QuickJS engine](../njs/engine.xml) . Each context is used for a single stream session. The finished context is put into a pool of reusable contexts. If the pool is full, the context is destroyed.

## js_engine

```
Syntax:  njs | qjs
Default: njs
Context: server, stream
```

*This directive appeared in version 0.8.6.*

Sets a [JavaScript engine](../njs/engine.xml) to be used for njs scripts. The `njs` parameter sets the njs engine, also used by default. The `qjs` parameter sets the QuickJS engine.

## js_fetch_buffer_size

```
Syntax:  size
Default: 16k
Context: server, stream
```

*This directive appeared in version 0.7.4.*

Sets the `size` of the buffer used for reading and writing with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_ciphers

```
Syntax:  ciphers
Default: HIGH:!aNULL:!MD5
Context: server, stream
```

*This directive appeared in version 0.7.0.*

Specifies the enabled ciphers for HTTPS connections with [Fetch API](../njs/reference.xml#ngx_fetch) . The ciphers are specified in the format understood by the OpenSSL library.

The full list can be viewed using the “ `openssl ciphers` ” command.

## js_fetch_max_response_buffer_size

```
Syntax:  size
Default: 1m
Context: server, stream
```

*This directive appeared in version 0.7.4.*

Sets the maximum `size` of the response received with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_protocols

```
Syntax:  [TLSv1] [TLSv1.1] [TLSv1.2] [TLSv1.3]
Default: TLSv1 TLSv1.1 TLSv1.2
Context: server, stream
```

*This directive appeared in version 0.7.0.*

Enables the specified protocols for HTTPS connections with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_timeout

```
Syntax:  time
Default: 60s
Context: server, stream
```

*This directive appeared in version 0.7.4.*

Defines a timeout for reading and writing for [Fetch API](../njs/reference.xml#ngx_fetch) . The timeout is set only between two successive read/write operations, not for the whole response. If no data is transmitted within this time, the connection is closed.

## js_fetch_trusted_certificate

```
Syntax:  file
Default: 
Context: server, stream
```

*This directive appeared in version 0.7.0.*

Specifies a `file` with trusted CA certificates in the PEM format used to [verify](../njs/reference.xml#fetch_verify) the HTTPS certificate with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_verify

```
Syntax:  on | off
Default: on
Context: server, stream
```

*This directive appeared in version 0.7.4.*

Enables or disables verification of the HTTPS server certificate with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_verify_depth

```
Syntax:  number
Default: 100
Context: server, stream
```

*This directive appeared in version 0.7.0.*

Sets the verification depth in the HTTPS server certificates chain with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_fetch_proxy

```
Syntax:  url
Default: 
Context: server, stream
```

*This directive appeared in version 0.9.4.*

Configures a forward proxy URL with [Fetch API](../njs/reference.xml#ngx_fetch) . The `url` supports the HTTP scheme only and can contain optional user credentials in the format `http://[user:password@]host:port` for Basic authentication. Supports both HTTP and HTTPS connections to destination servers. If the `url` is empty, proxy routing is disabled. The parameter value can contain variables.

Example:

```
server {
    listen 12345;
    js_fetch_proxy http://user:pass@proxy.example.com:3128;
    js_preread main.fetch_handler;
}
```

## js_fetch_keepalive

```
Syntax:  connections
Default: 0
Context: server, stream
```

*This directive appeared in version 0.9.2.*

Activates the cache for connections to destination servers. When the value is greater than `0` , enables keepalive connections for [Fetch API](../njs/reference.xml#ngx_fetch) .

The `connections` parameter sets the maximum number of idle keepalive connections to destination servers that are preserved in the cache of each worker process. When this number is exceeded, the least recently used connections are closed.

Example:

```
server {
    listen 12345;
    js_fetch_keepalive 32;
    js_fetch_trusted_certificate /path/to/ISRG_Root_X1.pem;
    js_preread main.fetch_handler;
}
```

## js_fetch_keepalive_requests

```
Syntax:  number
Default: 1000
Context: server, stream
```

*This directive appeared in version 0.9.2.*

Sets the maximum number of requests that can be served through one keepalive connection with [Fetch API](../njs/reference.xml#ngx_fetch) . After the maximum number of requests is made, the connection is closed.

Closing connections periodically is necessary to free per-connection memory allocations. Therefore, using too high maximum number of requests could result in excessive memory usage and not recommended.

## js_fetch_keepalive_time

```
Syntax:  time
Default: 1h
Context: server, stream
```

*This directive appeared in version 0.9.2.*

Limits the maximum time during which requests can be processed through one keepalive connection with [Fetch API](../njs/reference.xml#ngx_fetch) . After this time is reached, the connection is closed following the subsequent request processing.

## js_fetch_keepalive_timeout

```
Syntax:  time
Default: 60s
Context: server, stream
```

*This directive appeared in version 0.9.2.*

Sets a timeout during which an idle keepalive connection to a destination server will stay open with [Fetch API](../njs/reference.xml#ngx_fetch) .

## js_filter

```
Syntax:  module.function
Default: 
Context: server, stream
```

Sets a data filter. Since [0.4.0](../njs/changes.xml#njs0.4.0) , a module function can be referenced. The filter function is called once at the moment when the stream session reaches the [content](stream_processing.xml#content_phase) phase.

The filter function is called with the following arguments:

**`s`**  
  the [Stream Session](../njs/reference.xml#stream) object

At this phase, it is possible to perform initialization or register a callback with the [`s.on()`](../njs/reference.xml#s_on) method for each incoming data chunk. The [`s.off()`](../njs/reference.xml#s_off) method may be used to unregister a callback and stop filtering.

> **Note:** As the `js_filter` handler
returns its result immediately, it supports
only synchronous operations.
Thus, asynchronous operations such as [`ngx.fetch()`](../njs/reference.xml#ngx_fetch) or [`setTimeout()`](../njs/reference.xml#settimeout) are not supported.

## js_import

```
Syntax:  module.js | export_name from module.js
Default: 
Context: server, stream
```

*This directive appeared in version 0.4.0.*

Imports a module that implements location and variable handlers in njs. The `export_name` is used as a namespace to access module functions. If the `export_name` is not specified, the module name will be used as a namespace.

```
js_import stream.js;
```

Here, the module name `stream` is used as a namespace while accessing exports. If the imported module exports `foo()` , `stream.foo` is used to refer to it.

Several `js_import` directives can be specified.

> **Note:** The directive can be specified on the `server` level
since [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_include

```
Syntax:  file
Default: 
Context: stream
```

Specifies a file that implements server and variable handlers in njs:

```
nginx.conf:
js_include stream.js;
js_set     $js_addr address;
server {
    listen 127.0.0.1:12345;
    return $js_addr;
}

stream.js:
function address(s) {
    return s.remoteAddress;
}
```

The directive was made obsolete in version [0.4.0](../njs/changes.xml#njs0.4.0) and was removed in version [0.7.1](../njs/changes.xml#njs0.7.1) . The [js_import](#js_import) directive should be used instead.

## js_path

```
Syntax:  path
Default: 
Context: server, stream
```

*This directive appeared in version 0.3.0.*

Sets an additional path for njs modules.

> **Note:** The directive can be specified on the `server` level
since [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_periodic

```
Syntax:  module.function [interval=time] [jitter=number] [worker_affinity=mask]
Default: 
Context: server
```

*This directive appeared in version 0.8.1.*

Specifies a content handler to run at regular interval. The handler receives a [session object](../njs/reference.xml#periodic_session) as its first argument, it also has access to global objects such as [ngx](../njs/reference.xml#ngx) .

The optional `interval` parameter sets the interval between two consecutive runs, by default, 5 seconds.

The optional `jitter` parameter sets the time within which the location content handler will be randomly delayed, by default, there is no delay.

By default, the `js_handler` is executed on worker process 0. The optional `worker_affinity` parameter allows specifying particular worker processes where the location content handler should be executed. Each worker process set is represented by a bitmask of allowed worker processes. The `all` mask allows the handler to be executed in all worker processes.

Example:

```
example.conf:

location @periodics {
    # to be run at 1 minute intervals in worker process 0
    js_periodic main.handler interval=60s;

    # to be run at 1 minute intervals in all worker processes
    js_periodic main.handler interval=60s worker_affinity=all;

    # to be run at 1 minute intervals in worker processes 1 and 3
    js_periodic main.handler interval=60s worker_affinity=0101;

    resolver 10.0.0.1;
    js_fetch_trusted_certificate /path/to/ISRG_Root_X1.pem;
}

example.js:

async function handler(s) {
    let reply = await ngx.fetch('https://nginx.org/en/docs/njs/');
    let body = await reply.text();

    ngx.log(ngx.INFO, body);
}
```

## js_preload_object

```
Syntax:  name.json | name from file.json
Default: 
Context: server, stream
```

*This directive appeared in version 0.7.8.*

Preloads an [immutable object](../njs/preload_objects.xml) at configure time. The `name` is used as a name of the global variable though which the object is available in njs code. If the `name` is not specified, the file name will be used instead.

```
js_preload_object map.json;
```

Here, the `map` is used as a name while accessing the preloaded object.

Several `js_preload_object` directives can be specified.

## js_preread

```
Syntax:  module.function
Default: 
Context: server, stream
```

Sets an njs function which will be called at the [preread](stream_processing.xml#preread_phase) phase. Since [0.4.0](../njs/changes.xml#njs0.4.0) , a module function can be referenced.

The function is called once at the moment when the stream session reaches the [preread](stream_processing.xml#preread_phase) phase for the first time. The function is called with the following arguments:

**`s`**  
  the [Stream Session](../njs/reference.xml#stream) object

At this phase, it is possible to perform initialization or register a callback with the [`s.on()`](../njs/reference.xml#s_on) method for each incoming data chunk until one of the following methods are called: [`s.allow()`](../njs/reference.xml#s_allow) , [`s.decline()`](../njs/reference.xml#s_decline) , [`s.done()`](../njs/reference.xml#s_done) . When one of these methods is called, the stream session switches to the [next phase](stream_processing.xml) and all current [`s.on()`](../njs/reference.xml#s_on) callbacks are dropped.

> **Note:** As the `js_preread` handler
returns its result immediately, it supports
only synchronous callbacks.
Thus, asynchronous callbacks such as [`ngx.fetch()`](../njs/reference.xml#ngx_fetch) or [`setTimeout()`](../njs/reference.xml#settimeout) are not supported.
Nevertheless, asynchronous operations are supported in [`s.on()`](../njs/reference.xml#s_on) callbacks in the [preread](stream_processing.xml#preread_phase) phase.
See [this example](https://github.com/nginx/njs-examples#authorizing-connections-using-ngx-fetch-as-auth-request-stream-auth-request) for more information.

## js_set

```
Syntax:  $variable module.function [nocache]
Default: 
Context: server, stream
```

Sets an njs `function` for the specified `variable` . Since [0.4.0](../njs/changes.xml#njs0.4.0) , a module function can be referenced.

The function is called when the variable is referenced for the first time for a given request. The exact moment depends on a [phase](stream_processing.xml) at which the variable is referenced. This can be used to perform some logic not related to variable evaluation. For example, if the variable is referenced only in the [log_format](ngx_stream_log_module.xml#log_format) directive, its handler will not be executed until the log phase. This handler can be used to do some cleanup right before the request is freed.

Since [0.8.6](../njs/changes.xml#njs0.8.6) , when optional argument `nocache` is provided the handler is called every time it is referenced. Due to current limitations of the [rewrite](ngx_stream_rewrite_module.xml) module, when a `nocache` variable is referenced by the [set](ngx_stream_set_module.xml#set) directive its handler should always return a fixed-length value.

> **Note:** As the `js_set` handler
returns its result immediately, it supports
only synchronous callbacks.
Thus, asynchronous callbacks such as [ngx.fetch()](../njs/reference.xml#ngx_fetch) or [setTimeout()](../njs/reference.xml#settimeout) are not supported.

> **Note:** The directive can be specified on the `server` level
since [0.7.7](../njs/changes.xml#njs0.7.7) .

## js_shared_dict_zone

```
Syntax:  zone=name:size [timeout=time] [type=string|number] [evict] [state=file]
Default: 
Context: stream
```

*This directive appeared in version 0.8.0.*

Sets the `name` and `size` of the shared memory zone that keeps the key-value [dictionary](../njs/reference.xml#dict) shared between worker processes.

By default the shared dictionary uses a string as a key and a value. The optional `type` parameter allows redefining the value type to number.

The optional `timeout` parameter sets the time in milliseconds after which all shared dictionary entries are removed from the zone. If some entries require a different removal time, it can be set with the `timeout` argument of the [add](../njs/reference.xml#dict_add) , [incr](../njs/reference.xml#dict_incr) , and [set](../njs/reference.xml#dict_set) methods ( [0.8.5](../njs/changes.xml#njs0.8.5) ).

The optional `evict` parameter removes the oldest key-value pair when the zone storage is exhausted.

The optional `state` parameter specifies a `file` that keeps the shared dictionary state in JSON format and makes it persistent across nginx restarts ( [0.9.1](../njs/changes.xml#njs0.9.1) ).

Example:

```
example.conf:
    # Creates a 1Mb dictionary with string values,
    # removes key-value pairs after 60 seconds of inactivity:
    js_shared_dict_zone zone=foo:1M timeout=60s;

    # Creates a 512Kb dictionary with string values,
    # forcibly removes oldest key-value pairs when the zone is exhausted:
    js_shared_dict_zone zone=bar:512K timeout=30s evict;

    # Creates a 32Kb permanent dictionary with number values:
    js_shared_dict_zone zone=num:32k type=number;

    # Creates a 1Mb dictionary with string values and persistent state:
    js_shared_dict_zone zone=persistent:1M state=/tmp/dict.json;

example.js:
    function get(r) {
        r.return(200, ngx.shared.foo.get(r.args.key));
    }

    function set(r) {
        r.return(200, ngx.shared.foo.set(r.args.key, r.args.value));
    }

    function del(r) {
        r.return(200, ngx.shared.bar.delete(r.args.key));
    }

    function increment(r) {
        r.return(200, ngx.shared.num.incr(r.args.key, 2));
    }
```

## js_var

```
Syntax:  $variable [value]
Default: 
Context: server, stream
```

*This directive appeared in version 0.5.3.*

Declares a [writable](../njs/reference.xml#r_variables) variable. The value can contain text, variables, and their combination.

> **Note:** The directive can be specified on the `server` level
since [0.7.7](../njs/changes.xml#njs0.7.7) .

# Session Object Properties {#properties}

Each stream njs handler receives one argument, a stream session [object](../njs/reference.xml#stream) .

