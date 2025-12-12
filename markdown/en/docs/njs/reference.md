# Reference

**Revision:** 129  
**Language:** en

[njs](index.xml) provides objects, methods and properties for extending nginx functionality.

This reference contains only njs specific properties, methods and modules not compliant with ECMAScript. Definitions of njs properties and methods compliant with ECMAScript can be found in [ECMAScript specification](http://www.ecma-international.org/ecma-262/) . List of all njs properties and methods can be found in [Compatibility](compatibility.xml) .

# nginx objects {#http_stream}

## HTTP Request {#http}

 

The HTTP request object is available only in the [ngx_http_js_module](../http/ngx_http_js_module.xml) module. Before [0.8.5](changes.xml#njs0.8.5) , all string properties of the object were [byte strings](#string) .

**`r.args{}`**  
  request arguments object, read-only.

The query string is returned as an object. Since [0.7.6](changes.xml#njs0.7.6) , duplicate keys are returned as an array, keys are case-sensitive, both keys and values are percent-decoded.

For example, the query string

```
'a=1&b=%32&A=3&b=4&B=two%20words'
```

is converted to `r.args` as:

```
{a: "1", b: ["2", "4"], A: "3", B: "two words"}
```

More advanced parsing scenarios can be achieved with the [Query String](#querystring) module and with the [`$args`](../http/ngx_http_core_module.xml#var_args) variable, for example:

```
import qs from 'querystring';

function args(r) {
    return qs.parse(r.variables.args);
}
```

The argument object is evaluated at the first access to `r.args` . If only a single argument is needed, for example `foo` , [nginx variables](../varindex.xml) can be used:

```
r.variables.arg_foo
```

Here, [nginx variables object](#r_variables) returns the first value for a given key, case-insensitive, without percent-decoding.

To convert `r.args` back to a string, the Query String [`stringify`](#querystring_stringify) method can be used.

**`r.done()`**  
  after calling this function,
next data chunks will be passed to client without calling [js_body_filter](../http/ngx_http_js_module.xml#js_body_filter) ( [0.5.2](changes.xml#njs0.5.2) ).
May be called only from the [js_body_filter](../http/ngx_http_js_module.xml#js_body_filter) function

**`r.error(`**  
  writes a `string` to the error log
on the `error` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

**`r.finish()`**  
  finishes sending a response to the client

**`r.headersIn{}`**  
  incoming headers object, read-only.

The `Foo` request header can be accessed with the syntax: `headersIn.foo` or `headersIn['Foo']` .

The `Authorization` , `Content-Length` , `Content-Range` , `Content-Type` , `ETag` , `Expect` , `From` , `Host` , `If-Match` , `If-Modified-Since` , `If-None-Match` , `If-Range` , `If-Unmodified-Since` , `Max-Forwards` , `Proxy-Authorization` , `Referer` , `Transfer-Encoding` , and `User-Agent` request headers can have only one field value ( [0.4.1](changes.xml#njs0.4.1) ). Duplicate field values in `Cookie` headers are separated by semicolon ( `;` ). Duplicate field values in all other request headers are separated by commas.

**`r.headersOut{}`**  
  outgoing headers object for the main request, writable.

If `r.headersOut{}` is the response object of a [subrequest](#r_subrequest) , it represents response headers. In this case, field values in `Accept-Ranges` , `Connection` , `Content-Disposition` , `Content-Encoding` , `Content-Length` , `Content-Range` , `Date` , `Keep-Alive` , `Server` , `Transfer-Encoding` , `X-Accel-*` response headers may be omitted.

The `Foo` response header can be accessed with the syntax: `headersOut.foo` or `headersOut['Foo']` .

Outgoing headers should be set before a response header is sent to a client, otherwise header update will be ignored. This means that `r.headersOut{}` is effectively writable in:

- the [js_content](../http/ngx_http_js_module.xml#js_content) handler before [`r.sendHeader()`](#r_send_header) or [`r.return()`](#r_return) are called
- the [js_header_filter](../http/ngx_http_js_module.xml#js_header_filter) handler

Field values of multi-value response headers ( [0.4.0](changes.xml#njs0.4.0) ) can be set with the syntax:

```
r.headersOut['Foo'] = ['a', 'b']
```

where the output will be:

```
Foo: a
Foo: b
```

All previous field values of the `Foo` response header will be deleted.

For standard response headers that accept only a single field value such as `Content-Type` , only the last element of the array will take effect. Field values of the `Set-Cookie` response header are always returned as an array. Duplicate field values in `Age` , `Content-Encoding` , `Content-Length` , `Content-Type` , `ETag` , `Expires` , `Last-Modified` , `Location` , `Retry-After` response headers are ignored. Duplicate field values in all other response headers are separated by commas.

**`r.httpVersion`**  
  HTTP version, read-only

**`r.internal`**  
  boolean value, true for [internal](../http/ngx_http_core_module.xml#internal) locations

**`r.internalRedirect(`**  
  performs an [internal
redirect](../dev/development_guide.xml#http_request_redirection) to the specified `uri` .
If the uri starts with the “ `@` ” prefix,
it is considered a named location.
In a new location, all request processing is repeated
starting from [NGX_HTTP_SERVER_REWRITE_PHASE](../dev/development_guide.xml#http_phases) for ordinary locations and from [NGX_HTTP_REWRITE_PHASE](../dev/development_guide.xml#http_phases) for named locations.
As a result, a redirect to a named location
does not check [client_max_body_size](../http/ngx_http_core_module.xml#client_max_body_size) limit.
See [dev guide](../dev/development_guide.xml#http_request_redirection) for more details.
Redirected requests become internal and can access the [internal](../http/ngx_http_core_module.xml#internal) locations.
The actual redirect happens after the handler execution is completed.

> **Note:** After redirect,
a new njs VM is started in the target location,
the VM in the original location is stopped.
Values of [nginx variables](../varindex.xml) are kept
and can be used to pass information to the target location.
Since [0.5.3](changes.xml#njs0.5.3) ,
the variable declared with the `js_var` directive for [http](../http/ngx_http_js_module.xml#js_var) or [stream](../stream/ngx_stream_js_module.xml#js_var) can be used.

> **Note:** Since [0.7.4](changes.xml#njs0.7.4) ,
the method accepts escaped URIs.

**`r.log(`**  
  writes a `string` to the error log
on the `info` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

**`r.method`**  
  HTTP method, read-only

**`r.parent`**  
  references the parent request object

**`r.remoteAddress`**  
  client address, read-only

**`r.requestBody`**  
  the property was made obsolete in [0.5.0](changes.xml#njs0.5.0) and was removed in [0.8.0](changes.xml#njs0.8.0) .
The [`r.requestBuffer`](#r_request_buffer) or [`r.requestText`](#r_request_text) property
should be used instead.

**`r.requestBuffer`**  
  client request body if it has not been written to a temporary file
(since [0.5.0](changes.xml#njs0.5.0) ).
To ensure that the client request body is in memory,
its size should be limited by [client_max_body_size](../http/ngx_http_core_module.xml#client_max_body_size) ,
and a sufficient buffer size should be set using [client_body_buffer_size](../http/ngx_http_core_module.xml#client_body_buffer_size) .
The property is available only in the [js_content](../http/ngx_http_js_module.xml#js_content) directive.

**`r.requestText`**  
  the same as [`r.requestBuffer`](#r_request_buffer) ,
but returns a `string` .
Note that
it may convert bytes invalid in UTF-8 encoding into the replacement character.

**`r.rawHeadersIn[]`**  
  returns an array of key-value pairs
exactly as they were received from the client
( [0.4.1](changes.xml#njs0.4.1) ).

For example, with the following request headers:

```
Host: localhost
Foo:  bar
foo:  bar2
```

the output of `r.rawHeadersIn` will be:

```
[
    ['Host', 'localhost'],
    ['Foo', 'bar'],
    ['foo', 'bar2']
]
```

All `foo` headers can be collected with the syntax:

```
r.rawHeadersIn.filter(v=>v[0].toLowerCase() == 'foo').map(v=>v[1])
```

the output will be:

```
['bar', 'bar2']
```

Header field names are not converted to lower case, duplicate field values are not merged.

**`r.rawHeadersOut[]`**  
  returns an array of key-value pairs of response headers
( [0.4.1](changes.xml#njs0.4.1) ).
Header field names are not converted to lower case,
duplicate field values are not merged.

**`r.responseBody`**  
  the property was made obsolete in [0.5.0](changes.xml#njs0.5.0) and was removed in [0.8.0](changes.xml#njs0.8.0) .
The [`r.responseBuffer`](#r_response_buffer) or
the [`r.responseText`](#r_response_text) property
should be used instead.

**`r.responseBuffer`**  
  holds the [subrequest](#r_subrequest) response body,
read-only
(since [0.5.0](changes.xml#njs0.5.0) ).
The size of `r.responseBuffer` is limited by the [subrequest_output_buffer_size](../http/ngx_http_core_module.xml#subrequest_output_buffer_size) directive.

**`r.responseText`**  
  the same as [`r.responseBuffer`](#r_response_buffer) but returns a string
(since [0.5.0](changes.xml#njs0.5.0) ).
Note that
it may convert bytes invalid in UTF-8 encoding into the replacement character.

**`r.return(status[,
string | Buffer])`**  
  sends the entire response
with the specified `status` to the client.
The response can be a string or Buffer
( [0.5.0](changes.xml#njs0.5.0) ).

It is possible to specify either a redirect URL (for codes 301, 302, 303, 307, and 308) or the response body text (for other codes) as the second argument

**`r.send(string
| Buffer)`**  
  sends a part of the response body to the client.
The data sent can be a string or Buffer
( [0.5.0](changes.xml#njs0.5.0) )

**`r.sendBuffer(`**  
  adds data to the chain of data chunks to be forwarded to the next body filter
( [0.5.2](changes.xml#njs0.5.2) ).
The actual forwarding happens later,
when the all the data chunks of the current chain are processed.

The data can be a string or Buffer. The `options` is an object used to override nginx buffer flags derived from an incoming data chunk buffer. The flags can be overridden with the following flags:

**`last`**  
  boolean,
true if the buffer is the last buffer

**`flush`**  
  boolean,
true if the buffer should have the `flush` flag

  The method may be called only from the [js_body_filter](../http/ngx_http_js_module.xml#js_body_filter) function.

**`r.sendHeader()`**  
  sends the HTTP headers to the client

**`r.setReturnValue(`**  
  sets the return value of the [js_set](../http/ngx_http_js_module.xml#js_set) handler
( [0.7.0](changes.xml#njs0.7.0) ).
Unlike an ordinary return statement,
this method should be used when the handler is JS async function.
For example:

```
async function js_set(r) {
    const digest = await crypto.subtle.digest('SHA-256', r.headersIn.host);
    r.setReturnValue(digest);
}
```

**`r.status`**  
  status, writable

**`r.subrequest(`**  
  creates a subrequest with the given `uri` and `options` , and installs
an optional completion `callback` .

A [subrequest](../dev/development_guide.xml.xml#http_subrequests) shares its input headers with the client request. To send headers different from original headers to a proxied server, the [proxy_set_header](../http/ngx_http_proxy_module.xml#proxy_set_header) directive can be used. To send a completely new set of headers to a proxied server, the [proxy_pass_request_headers](../http/ngx_http_proxy_module.xml#proxy_pass_request_headers) directive can be used.

If `options` is a string, then it holds the subrequest arguments string. Otherwise, `options` is expected to be an object with the following keys:

**`args`**  
  arguments string, by default an empty string is used

**`body`**  
  request body,
by default the request body of the parent request object is used

**`method`**  
  HTTP method, by default the `GET` method is used

**`detached`**  
  boolean flag ( [0.3.9](changes.xml#njs0.3.9) ),
if `true` , the created subrequest is a detached subrequest.
Responses to detached subrequests are ignored.
Unlike ordinary subrequests, a detached subrequest
can be created inside a variable handler.
The `detached` flag and callback argument
are mutually exclusive.

The completion `callback` receives a [subrequest response object](#http) with methods and properties identical to the parent request object.

Since [0.3.8](changes.xml#njs0.3.8) , if a `callback` is not provided, the `Promise` object that resolves to the [subrequest response object](#http) is returned.

For example, to view all response headers in the subrequest:

```
async function handler(r) {
    const reply = await r.subrequest('/path');

    for (const h in reply.headersOut) {
        r.log(`${h}: ${reply.headersOut[h]}`);
    }

    r.return(200);
}
```

**`r.uri`**  
  current [URI](../http/ngx_http_core_module.xml#var_uri) in request, [normalized](../http/ngx_http_core_module.xml#location) ,
read-only

**`r.rawVariables{}`**  
  nginx [variables](#r_variables) as Buffers,
writable
(since [0.5.0](changes.xml#njs0.5.0) )

**`r.variables{}`**  
  [nginx variables](../varindex.xml) object, writable
(since [0.2.8](changes.xml#njs0.2.8) ).

For example, to get the `$foo` variable, one of the following syntax can be used:

```
r.variables['foo']
r.variables.foo
```

Since [0.8.6](changes.xml#njs0.8.6) , regular expression captures can be accessed using the following syntax:

```
r.variables['1']
r.variables[1]
```

nginx treats variables referenced in `nginx.conf` and unreferenced variables differently. When a variable is referenced, it may be cacheable, but when it is unreferenced it is always uncacheable. For example, when the [$request_id](../http/ngx_http_core_module.xml#var_request_id) variable is only accessed from njs, it has a new value every time it is evaluated. But, when the [$request_id](../http/ngx_http_core_module.xml#var_request_id) is referenced, for example:

```
proxy_set_header X-Request-Id $request_id;
```

the `r.variables.request_id` returns the same value every time.

A variable is writable if:

- it was created using the `js_var` directive for [http](../http/ngx_http_js_module.xml#js_var) or [stream](../stream/ngx_stream_js_module.xml#js_var) (since [0.5.3](changes.xml#njs0.5.3) )
- it is referenced in nginx configuration file

Even so, some embedded variables still cannot be assigned a value (for example, [`$http_`](../http/ngx_http_core_module.xml#var_http_) ).

**`r.warn(`**  
  writes a `string` to the error log
on the `warning` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

## Stream Session {#stream}

 

The stream session object is available only in the [ngx_stream_js_module](../stream/ngx_stream_js_module.xml) module. Before [0.8.5](changes.xml#njs0.8.5) , all string properties of the object were [byte strings](#string) .

**`s.allow()`**  
  an alias to [`s.done(0)`](#s_done) ( [0.2.4](changes.xml#njs0.2.4) )

**`s.decline()`**  
  an alias to [`s.done(-5)`](#s_done) ( [0.2.4](changes.xml#njs0.2.4) )

**`s.deny()`**  
  an alias to [`s.done(403)`](#s_done) ( [0.2.4](changes.xml#njs0.2.4) )

**`s.done([` )**  
  sets an exit `code` for the current [phase](../stream/stream_processing.xml) handler
to a code value, by default `0` .
The actual finalization happens when the js handler is completed
and all pending events, for example, from [`ngx.fetch()`](#ngx_fetch) or [`setTimeout()`](#settimeout) ,
are processed
( [0.2.4](changes.xml#njs0.2.4) ).

Possible code values:

- `0` —
successful finalization, passing control to the next phase
- `-5` —
undecided, passing control to the next handler of the current phase (if any)
- `403` —
access is forbidden

  May be called only from a phase handler function: [`js_access`](../stream/ngx_stream_js_module.xml#js_access) or [`js_preread`](../stream/ngx_stream_js_module.xml#js_preread) .

**`s.error(`**  
  writes a sent `string` to the error log
on the `error` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

**`s.log(`**  
  writes a sent `string` to the error log
on the `info` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

**`s.off(`**  
  unregisters the callback set by the [s.on()](#s_on) method
( [0.2.4](changes.xml#njs0.2.4) )

**`s.on(`**  
  registers a `callback` for the specified `event` ( [0.2.4](changes.xml#njs0.2.4) ).

An `event` may be one of the following strings:

**`upload`**  
  new data (string) from a client

**`download`**  
  new data (string) to a client

**`upstream`**  
  new data (Buffer) from a client
(since [0.5.0](changes.xml#njs0.5.0) )

**`downstream`**  
  new data (Buffer) to a client
(since [0.5.0](changes.xml#njs0.5.0) )

The completion callback has the following prototype: `callback(data, flags)` , where `data` is string or Buffer (depending on the event type) `flags` is an object with the following properties:

**`last`**  
  a boolean value, true if data is a last buffer.

**`s.remoteAddress`**  
  client address, read-only

**`s.rawVariables`**  
  nginx [variables](#s_variables) as Buffers,
writable
(since [0.5.0](changes.xml#njs0.5.0) )

**`s.send(`**  
  adds data to the chain of data chunks that will be forwarded in
the forward direction:
in download callback to a client; in upload to an upstream server
( [0.2.4](changes.xml#njs0.2.4) ).
The actual forwarding happens later,
when the all the data chunks of the current chain are processed.

The data can be a string or Buffer ( [0.5.0](changes.xml#njs0.5.0) ). The `options` is an object used to override nginx buffer flags derived from an incoming data chunk buffer. The flags can be overridden with the following flags:

**`last`**  
  boolean,
true if the buffer is the last buffer

**`flush`**  
  boolean,
true if the buffer should have the `flush` flag

  The method can be called multiple times per callback invocation.

**`s.sendDownstream()`**  
  is identical to [s.send()](#s_send) ,
except for it always sends data to a client
(since [0.7.8](changes.xml#njs0.7.8) ).

**`s.sendUpstream()`**  
  is identical to [s.send()](#s_send) ,
except for it always sends data from a client
(since [0.7.8](changes.xml#njs0.7.8) ).

**`s.status`**  
  session status code, an alias to the [`$status`](../stream/ngx_stream_core_module.xml#var_status) variable,
read only
(since [0.5.2](changes.xml#njs0.5.2) )

**`s.setReturnValue(`**  
  sets the return value of the [js_set](../stream/ngx_stream_js_module.xml#js_set) handler
( [0.7.0](changes.xml#njs0.7.0) ).
Unlike an ordinary return statement,
this method should be used when the handler is JS async function.
For example:

```
async function js_set(r) {
    const digest = await crypto.subtle.digest('SHA-256', r.headersIn.host);
    r.setReturnValue(digest);
}
```

**`s.variables{}`**  
  [nginx variables](../varindex.xml) object, writable
(since [0.2.8](changes.xml#njs0.2.8) ).
A variable can be writable only
if it is referenced in nginx configuration file.
Even so, some embedded variables still cannot be assigned a value.

**`s.warn(`**  
  writes a sent `string` to the error log
on the `warning` level of logging

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

## Periodic Session {#periodic_session}

 

The `Periodic Session` object is provided as the first argument for the `js_periodic` handler for [http](../http/ngx_http_js_module.xml#js_periodic) and [stream](../stream/ngx_stream_js_module.xml#js_periodic) (since [0.8.1](changes.xml#njs0.8.1) ).

**`PeriodicSession.rawVariables{}`**  
  nginx [variables](#periodic_session_variables) as Buffers,
writable.

**`PeriodicSession.variables{}`**  
  [nginx variables](../varindex.xml) object, writable.

## Headers {#headers}

 

The `Headers` interface of the [`Fetch API`](#ngx_fetch) is available since [0.5.1](changes.xml#njs0.5.1) .

A new `Headers` object can be created using the [`Headers()`](#headers_constructor) constructor: (since [0.7.10](changes.xml#njs0.7.10) ):

**`Headers([`**  
**`init`**  
  An object containing HTTP headers for
prepopulating the `Headers` object,
can be a `string` ,
an `array` of name-value pairs,
or an existing `Headers` object.

A new `Headers` object can be created with the following properties and methods:

**`append()`**  
  Appends a new value into an existing header in the `Headers` object,
or adds the header if it does not already exist
(since [0.7.10](changes.xml#njs0.7.10) ).

**`delete()`**  
  Deletes a header from the `Headers` object
(since [0.7.10](changes.xml#njs0.7.10) ).

**`get()`**  
  Returns a string containing the values of all headers with the specified name
separated by a comma and a space.

**`getAll(`**  
  Returns an array containing the values of all headers with the specified name.

**`forEach()`**  
  Executes a provided function once for each key/value pair
in the `Headers` object
(since [0.7.10](changes.xml#njs0.7.10) ).

**`has()`**  
  Returns a boolean value
indicating whether a header with the specified name exists.

**`set()`**  
  Sets a new value for an existing header inside
the `Headers` object,
or adds the header if it does not already exist
(since [0.7.10](changes.xml#njs0.7.10) ).

## Request {#request}

 

The `Request` interface of the [`Fetch API`](#ngx_fetch) is available since [0.7.10](changes.xml#njs0.7.10) .

A new `Request` object can be created using the [`Request()`](#request_constructor) constructor:

**`Request[`**  
  Creates a `Request` object to fetch
that can be passed later to [`ngx.fetch()`](#ngx_fetch) .
The `resource` can be a URL
or an existing `Request` object.
The `options` is an optional argument
that is expected to be an object with the following keys:

**`body`**  
  The request body, by default is empty.

**`headers`**  
  The response headers object—
the object containing HTTP headers for
prepopulating the [`Headers`](#headers) object,
can be a `string` ,
an `array` of name-value pairs,
or an existing [`Headers`](#headers) object.

**`method`**  
  The HTTP method, by default the GET method is used.

A new `Request` object can be created with the following properties and methods:

**`arrayBuffer()`**  
  Returns a `Promise` that resolves with
an `ArrayBuffer` .

**`bodyUsed`**  
  A boolean value, `true` if the body was used in the request.

**`cache`**  
  Contains the cache mode of the request.

**`credentials`**  
  Contains the credentials of the request,
by default is `same-origin` .

**`headers`**  
  The [`Headers`](#headers) read-only object
associated with the [`Request`](#request) .

**`json()`**  
  Returns a `Promise` that resolves with
the result of parsing the request body as JSON.

**`method`**  
  Contains the request method.

**`mode`**  
  Contains the mode of the request.

**`text()`**  
  Returns a `Promise` that resolves with a
string representation of the request body.

**`url`**  
  Contains the URL of the request.

## Response {#response}

 

The `Response` interface is available since [0.5.1](changes.xml#njs0.5.1) .

A new `Response` object can be created using the [`Response()`](#response_constructor) constructor (since [0.7.10](changes.xml#njs0.7.10) ):

**`Response[`**  
  Creates a `Response` object.
The `body` is an optional argument,
can be a `string` or a `buffer` ,
by default is `null` .
The `options` is an optional argument
that is expected to be an object with the following keys:

**`headers`**  
  The response headers object—
the object containing HTTP headers for
prepopulating the [`Headers`](#headers) object,
can be a `string` ,
an `array` of name-value pairs,
or an existing [`Headers`](#headers) object.

**`status`**  
  The status code of the response.

**`statusText`**  
  The status message corresponding to the status code.

A new `Response()` object can be created with the following properties and methods:

**`arrayBuffer()`**  
  Takes a `Response` stream and reads it to completion.
Returns a `Promise` that resolves with
an `ArrayBuffer` .

**`bodyUsed`**  
  A boolean value, `true` if the body was read.

**`headers`**  
  The [`Headers`](#headers) read-only object
associated with the [`Response`](#response) .

**`json()`**  
  Takes a `Response` stream and reads it to completion.
Returns a `Promise` that resolves with
the result of parsing the body text as JSON.

**`ok`**  
  A boolean value, `true` if the response was successful (status codes between 200–299).

**`redirected`**  
  A boolean value, `true` if the response is the result of a redirect.

**`status`**  
  The status code of the response.

**`statusText`**  
  The status message corresponding to the status code.

**`text()`**  
  Takes a `Response` stream and reads it to completion.
Returns a `Promise` that resolves with a string.

**`type`**  
  The type of the response.

**`url`**  
  The URL of the response.

## ngx {#ngx}

 

The `ngx` global object is available since [0.5.0](changes.xml#njs0.5.0) .

**`ngx.build`**  
  a string containing an optional nginx build name, corresponds to the [`--build=name`](../configure.xml#build) argument
of the [configure](../configure.xml) script,
by default is `""` ( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.conf_file_path`**  
  a string containing the file path to current nginx configuration file
( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.conf_prefix`**  
  a string containing the file path to [nginx configuration prefix](../configure.xml#conf_path) —
the directory where nginx is currently looking for configuration
( [0.7.8](changes.xml#njs0.7.8) )

**`ngx.error_log_path`**  
  a string containing the file path to the current [error log](../ngx_core_module.xml#error_log) file
( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.fetch(`**  
Makes a request to fetch a `resource` ( [0.5.1](changes.xml#njs0.5.1) ), which can be an URL or the [`Request`](#request) object ( [0.7.10](changes.xml#njs0.7.10) ). Returns a `Promise` that resolves with the [`Response`](#response) object. Since [0.7.0](changes.xml#njs0.7.0) , the `https://` scheme is supported, redirects are not handled.

If the URL in the `resource` is specified as a domain name, it is determined using a [resolver](../http/ngx_http_core_module.xml#resolver) . If the `https://` scheme is specified, the [js_fetch_trusted_certificate](../http/ngx_http_js_module.xml#js_fetch_trusted_certificate) directive should be configured for the authentication of the `resource` 's HTTPS server.

The `options` parameter is expected to be an object with the following keys:

**`body`**  
  request body,
by default is empty

**`buffer_size`**  
  the buffer size for reading the response,
by default is `4096`

**`headers`**  
  request [headers](#headers) object

**`max_response_body_size`**  
  the maximum size of the response body in bytes,
by default is `32768`

**`method`**  
  HTTP method,
by default the `GET` method is used

**`verify`**  
  enables or disables verification of the HTTPS server certificate,
by default is `true` ( [0.7.0](changes.xml#njs0.7.0) )

Example:

```
let reply = await ngx.fetch('http://nginx.org/');
let body = await reply.text();

r.return(200, body);
```

**`ngx.log` ( `level` , `message` )**  
  writes a message to the error log with the specified level of logging.
The `level` parameter specifies one of the log levels,
the `message` parameter can be a string or Buffer.
The following log levels can be specified: `ngx.INFO` , `ngx.WARN` , and `ngx.ERR` .

> **Note:** As nginx has a [hardcoded](../dev/development_guide.xml#logging) maximum line length limit,
only first 2048 bytes of the string can be logged.

**`ngx.prefix`**  
  a string containing the file path to [nginx prefix](../configure.xml#prefix) —
a directory that keeps server files
( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.version`**  
  a string containing nginx version,
for example: `1.25.0` ( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.version_number`**  
  a number containing nginx version,
for example: `1025000` ( [0.8.0](changes.xml#njs0.8.0) )

**`ngx.worker_id`**  
  a number that corresponds to nginx internal worker id,
the value is between `0` and the value specified in the [worker_processes](../ngx_core_module.xml#worker_processes) directive
( [0.8.0](changes.xml#njs0.8.0) )

## ngx.shared {#ngx_shared}

The `ngx.shared` global object is available since [0.8.0](changes.xml#njs0.8.0) .

### SharedDict {#dict}

 

The shared dictionary object is available since [0.8.0](changes.xml#njs0.8.0) . The shared dictionary name, type, and size are set with the `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) .

A `SharedDict()` object has the following properties and methods:

**`ngx.shared.SharedDict.add(`**  
  Sets the `value` for the specified `key` in the dictionary
only if the key does not exist yet.
The `key` is a string representing
the key of the item to add,
the `value` is the value of the item to add.

The optional `timeout` argument is specified in milliseconds and overrides the `timeout` parameter of the `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) (since [0.8.5](changes.xml#njs0.8.5) ). It can be useful when some keys are expected to have unique timeouts.

Returns `true` if the value has been successfully added to the `SharedDict` dictionary, `false` if the key already exists in the dictionary. Throws `SharedMemoryError` if there is not enough free space in the `SharedDict` dictionary. Throws `TypeError` if the `value` is of a different type than expected by this dictionary.

**`ngx.shared.SharedDict.capacity`**  
  Returns the capacity of the `SharedDict` dictionary,
corresponds to the `size` parameter of `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) .

**`ngx.shared.SharedDict.clear()`**  
  Removes all items from the `SharedDict` dictionary.

**`ngx.shared.SharedDict.delete(`**  
  Removes the item associated with the specified key
from the `SharedDict` dictionary, `true` if the item in the dictionary existed and was removed, `false` otherwise.

**`ngx.shared.SharedDict.freeSpace()`**  
  Returns the free page size in bytes.
If the size is zero, the `SharedDict` dictionary
will still accept new values if there is space in the occupied pages.

**`ngx.shared.SharedDict.get(`**  
  Retrieves the item by its `key` ,
returns the value associated with the `key` or `undefined` if there is none.

**`ngx.shared.SharedDict.has(`**  
  Searches for an item by its `key` ,
returns `true` if such item exists or `false` otherwise.

**`ngx.shared.SharedDict.incr(`**  
  Increments the integer value associated with the `key` by `delta` .
The `key` is a string,
the `delta` is the number
to increment or decrement the value by.
If the key does not exist,
the item will be initialized to an optional `init` argument,
by default is `0` .

The optional `timeout` argument is specified in milliseconds and overrides the `timeout` parameter of the `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) (since [0.8.5](changes.xml#njs0.8.5) ). It can be useful when some keys are expected to have unique timeouts.

Returns the new value. Throws `SharedMemoryError` if there is not enough free space in the `SharedDict` dictionary. Throws `TypeError` if this dictionary does not expect numbers.

> **Note:** This method can be used only if the dictionary type was declared with `type=number` parameter of the `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) .

**`ngx.shared.SharedDict.items([`**  
  Returns an array of the `SharedDict` dictionary
key-value items (since [0.8.1](changes.xml#njs0.8.1) ).
The `maxCount` parameter
sets maximum number of items to retrieve,
by default is `1024` .

**`ngx.shared.SharedDict.keys([`**  
  Returns an array of the `SharedDict` dictionary keys.
The `maxCount` parameter
sets maximum number of keys to retrieve,
by default is `1024` .

**`ngx.shared.SharedDict.name`**  
  Returns the name of the `SharedDict` dictionary,
corresponds to the `zone=` parameter of `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) .

**`ngx.shared.SharedDict.pop(`**  
  Removes the item associated with the specified `key` from the `SharedDict` dictionary,
returns the value associated with the `key` or `undefined` if there is none.

**`ngx.shared.SharedDict.replace(`**  
  Replaces the `value` for the specified `key` only if the key already exists,
returns `true` if the value was successfully replaced, `false` if the key does not exist
in the `SharedDict` dictionary.
Throws `SharedMemoryError` if
there is not enough free space in the `SharedDict` dictionary.
Throws `TypeError` if the `value` is
of a different type than expected by this dictionary.

**`ngx.shared.SharedDict.set(`**  
  Sets the `value` for the specified `key` ,
returns this `SharedDict` dictionary (for method chaining).

The optional `timeout` argument is specified in milliseconds and overrides the `timeout` parameter of the `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) (since [0.8.5](changes.xml#njs0.8.5) ). It can be useful when some keys are expected to have unique timeouts.

**`ngx.shared.SharedDict.size()`**  
  Returns the number of items for the `SharedDict` dictionary.

**`ngx.shared.SharedDict.type`**  
  Returns `string` or `number` that
corresponds to the `SharedDict` dictionary type
set by the `type=` parameter of `js_shared_dict_zone` directive in [http](../http/ngx_http_js_module.xml#js_shared_dict_zone) or [stream](../stream/ngx_stream_js_module.xml#js_shared_dict_zone) .

# built-in objects {#builtin_objects}

## console {#console}

 

The `console` object is available in nginx since [0.8.2](changes.xml#njs0.8.2) , in CLI since [0.2.6](changes.xml#njs0.2.6) .

**`console.error(`**  
  Outputs one or more error messages.
The message may be a string or an object.

**`console.info(`**  
  Outputs one or more info messages.
The message may be a string or an object.

**`console.log(`**  
  Outputs one or more log messages.
The message may be a string or an object.

**`console.time(`**  
  Starts a timer that can track how long an operation takes.
The `label` parameter allows naming different timers.
If [`console.timeEnd()`](#console_time_end) with the same name is called,
the time that elapsed since the timer was started will be output,
in milliseconds.

**`console.timeEnd(`**  
  Stops a timer previously started by [`console.time()`](#console_time) The `label` parameter allows naming different timers.

**`console.warn(`**  
  Outputs one or more warning messages.
The message may be a string or an object.

## crypto {#builtin_crypto}

 

The `crypto` object is a global object that allows using cryptographic functionality (since [0.7.0](changes.xml#njs0.7.0) ).

**`сrypto.getRandomValues` ( [`typedArray`](#crypto_get_random_values_array) )**  
  Gets cryptographically strong random values.
Returns the same array passed as `typedArray` but with its contents replaced with the newly generated random numbers.
Possible values:

**`typedArray`**  
  can be `Int8Array` , `Int16Array` , `Uint16Array` , `Int32Array` , or `Uint32Array`

**`сrypto.subtle.encrypt` ( [`algorithm`](#crypto_encrypt_alg) , [`key`](#crypto_encrypt_key) , [`data`](#crypto_encrypt_data) )**  
  Encrypts [`data`](#crypto_encrypt_data) using the provided [`algorithm`](#crypto_encrypt_algorithm) and [`key`](#crypto_encrypt_key) .
Returns a `Promise` that fulfills with
an `ArrayBuffer` containing the ciphertext.
Possible values:

**`algorithm`**  
  an object that specifies
the algorithm to be used and any extra parameters if required:

- for `RSA-OAEP` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `RSA-OAEP` :
    ```
crypto.subtle.encrypt({name: "RSA-OAEP"}, key, data)
```

  
- for `AES-CTR` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `AES-CTR`
  - `counter` is an `ArrayBuffer` , `TypedArray` , or `DataView` —
the initial value of the counter block,
must be 16 bytes long (the AES block size).
The rightmost length bits of this block are used for the counter,
and the rest is used for the nonce.
For example, if length is set to 64,
then the first half of counter is the nonce
and the second half is used for the counter
  - `length` is the number of bits in the counter block
that are used for the actual counter.
The counter must be big enough that it doesn't wrap.
  
- for `AES-CBC` , pass the object with the following keys:
  - `name` is a string,
should be set to `AES-CBC`
  - `iv` or the initialization vector, is an `ArrayBuffer` , `TypedArray` , or `DataView` ,
must be 16 bytes, unpredictable,
and preferably cryptographically random.
However, it need not be secret,
for example, it may be transmitted unencrypted along with the ciphertext.
  
- for `AES-GCM` , pass the object with the following keys:
  - `name` is a string,
should be set to `AES-GCM`
  - `iv` or the initialization vector, is an `ArrayBuffer` , `TypedArray` , or `DataView` ,
must be 16 bytes,
and must be unique for every encryption operation carried out with a given key
  - `additionalData` (optional) is an `ArrayBuffer` , `TypedArray` , or `DataView` that contains additional data that
will not be encrypted but will be authenticated along with the encrypted data.
If `additionalData` is specified,
then the same data must be specified in the corresponding call to `decrypt()` :
if the data given to the `decrypt()` call
does not match the original data,
the decryption will throw an exception.
The bit length of `additionalData` must be smaller than `2^64 - 1` .
  - `tagLength` (optional, default is `128` ) -
a `number` that determines the size in bits
of the authentication tag generated in the encryption operation
and used for authentication in the corresponding decryption
Possible values: `32` , `64` , `96` , `104` , `112` , `120` , or `128` .
The AES-GCM specification recommends that it should be `96` , `104` , `112` , `120` , or `128` ,
although `32` or `64` bits may be acceptable in some applications.
  

**`key`**  
  a [`CryptoKey`](#cryptokey) that contains
the key to be used for encryption

**`data`**  
  an `ArrayBuffer` , `TypedArray` , or `DataView` that contains
the data to be encrypted (also known as the plaintext)

**`сrypto.subtle.decrypt` ( [`algorithm`](#crypto_decrypt_alg) , [`key`](#crypto_decrypt_key) , [`data`](#crypto_decrypt_data) )**  
  Decrypts encrypted data.
Returns a `Promise` with the decrypted data.
Possible values:

**`algorithm`**  
  an object
that specifies the algorithm to be used, and any extra parameters as required.
The values given for the extra parameters must match
those passed into the corresponding `encrypt()` call.

- for `RSA-OAEP` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `RSA-OAEP` :
    ```
crypto.subtle.encrypt({name: "RSA-OAEP"}, key, data)
```

  
- for `AES-CTR` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `AES-CTR`
  - `counter` is an `ArrayBuffer` , `TypedArray` , or `DataView` —
the initial value of the counter block,
must be 16 bytes long (the AES block size).
The rightmost length bits of this block are used for the counter,
and the rest is used for the nonce.
For example, if length is set to 64,
then the first half of counter is the nonce
and the second half is used for the counter.
  - `length` is the number of bits in the counter block
that are used for the actual counter.
The counter must be big enough that it doesn't wrap.
  
- for `AES-CBC` , pass the object with the following keys:
  - `name` is a string,
should be set to `AES-CBC`
  - `iv` or the initialization vector, is an `ArrayBuffer` , `TypedArray` , or `DataView` ,
must be 16 bytes, unpredictable,
and preferably cryptographically random.
However, it need not be secret
(for example, it may be transmitted unencrypted along with the ciphertext).
  
- for `AES-GCM` , pass the object with the following keys:
  - `name` is a string,
should be set to `AES-GCM`
  - `iv` or the initialization vector, is an `ArrayBuffer` , `TypedArray` , or `DataView` ,
must be 16 bytes,
and must be unique for every encryption operation carried out with a given key
  - `additionalData` (optional) is an `ArrayBuffer` , `TypedArray` , or `DataView` that contains additional data that
will not be encrypted but will be authenticated along with the encrypted data.
If `additionalData` is specified,
then the same data must be specified in the corresponding call to `decrypt()` :
if the data given to the `decrypt()` call
does not match the original data,
the decryption will throw an exception.
The bit length of `additionalData` must be smaller than `2^64 - 1` .
  - `tagLength` (optional, default is `128` ) -
a `number` that determines the size in bits
of the authentication tag generated in the encryption operation
and used for authentication in the corresponding decryption.
Possible values: `32` , `64` , `96` , `104` , `112` , `120` , or `128` .
The AES-GCM specification recommends that it should be `96` , `104` , `112` , `120` , or `128` ,
although `32` or `64` bits may be acceptable in some applications.
  

**`key`**  
  a [`CryptoKey`](#cryptokey) that contains the key to be used for decryption.
If `RSA-OAEP` is used, this is the `privateKey` property of the [`CryptoKeyPair`](#cryptokeypair) object.

**`data`**  
  an `ArrayBuffer` , `TypedArray` , or `DataView` that contains the data to be decrypted (also known as ciphertext)

**`сrypto.subtle.deriveBits` ( [`algorithm`](#crypto_derive_bits_alg) , [`baseKey`](#crypto_derive_bits_basekey) , [`length`](#crypto_derive_bits_length) )**  
  Derives an array of bits from a base key.
Returns a `Promise` which will be fulfilled with an `ArrayBuffer` that contains the derived bits.
Possible values:

**`algorithm`**  
  is an object that defines the derivation algorithm to use:

- for `HKDF` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `HKDF`
  - `hash` is a string with the digest algorithm to use: `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  - `salt` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents random or pseudo-random value
with the same length as the output of the `digest` function.
Unlike the input key material passed into `deriveKey()` ,
salt does not need to be kept secret.
  - `info` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents application-specific contextual information
used to bind the derived key to an application or context,
and enables deriving different keys for different contexts
while using the same input key material.
This property is required but may be an empty buffer.
  
- for `PBKDF2` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `PBKDF2`
  - `hash` is a string with the digest algorithm to use: `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  - `salt` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents random or pseudo-random value
of at least `16` bytes.
Unlike the input key material passed into `deriveKey()` ,
salt does not need to be kept secret.
  - `iterations` is a `number` that represents the number of times the hash function will be executed
in `deriveKey()`
  
- for `ECDH` ,
pass the object with the following keys
(since [0.9.1](changes.xml#njs0.9.1) ):
  - `name` is a string,
should be set to `ECDH`
  - `public` is a [`CryptoKey`](#cryptokey) that represents the public key of the other party.
The key must be generated using the same curve as the base key.
  

**`baseKey`**  
  is a [`CryptoKey`](#cryptokey) that represents the input to the derivation algorithm
- the initial key material for the derivation function:
for example, for `PBKDF2` it might be a password,
imported as a [`CryptoKey`](#cryptokey) using [`сrypto.subtle.importKey()`](#crypto_subtle_import_key)

**`length`**  
  is a number representing the number of bits to derive.
For browsers compatibility,
the number should be a multiple of `8`

**`сrypto.subtle.deriveKey` ( [`algorithm`](#crypto_derive_key_alg) , [`baseKey`](#crypto_derive_key_basekey) , [`derivedKeyAlgorithm`](#crypto_derive_key_derivedkeyalg) , [`extractable`](#crypto_derive_key_extractable) , [`keyUsages`](#crypto_derive_key_keyusages) )**  
  Derives a secret key from a master key.
Possible values:

**`algorithm`**  
  is an object that defines the derivation algorithm to use:

- for `HKDF` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `HKDF`
  - `hash` is a string with the digest algorithm to use: `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  - `salt` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents random or pseudo-random value
with the same length as the output of the `digest` function.
Unlike the input key material passed into `deriveKey()` ,
salt does not need to be kept secret.
  - `info` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents application-specific contextual information
used to bind the derived key to an application or context,
and enables deriving different keys for different contexts
while using the same input key material.
This property is required but may be an empty buffer.
  
- for `PBKDF2` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `PBKDF2`
  - `hash` is a string with the digest algorithm to use: `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  - `salt` is an `ArrayBuffer` , `TypedArray` , or `DataView` that represents random or pseudo-random value
of at least `16` bytes.
Unlike the input key material passed into `deriveKey()` ,
salt does not need to be kept secret.
  - `iterations` is a `number` that represents the number of times the hash function will be executed
in `deriveKey()`
  
- for `ECDH` ,
pass the object with the following keys
(since [0.9.1](changes.xml#njs0.9.1) ):
  - `name` is a string,
should be set to `ECDH`
  - `publicKey` is a [`CryptoKey`](#cryptokey) that represents the public key of the other party.
The key must be generated using the same curve as the base key.
  

**`baseKey`**  
  is a [`CryptoKey`](#cryptokey) that represents the input to the derivation algorithm
- the initial key material for the derivation function:
for example, for `PBKDF2` it might be a password,
imported as a [`CryptoKey`](#cryptokey) using [`сrypto.subtle.importKey()`](#crypto_subtle_import_key) .

**`derivedKeyAlgorithm`**  
  is an object
that defines the algorithm the derived key will be used for:

- for `HMAC` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `HMAC`
  - `hash` is a string with the name of the digest function to use: `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  - `length` (optional) is a `number` that represents the length in bits of the key.
If not specified, the length of the key is equal to
the block size of the chozen hash function
  
- for `AES-CTR` , `AES-CBC` , or `AES-GCM` ,
pass the object with the following keys:
  - `name` is a string,
should be set to `AES-CTR` , `AES-CBC` , or `AES-GCM` ,
depending on the algorithm used
  - `length` is a `number` that represents
the length in bits of the key to generate: `128` , `192` , or `256`
  

**`extractable`**  
  is a boolean value
that indicates whether it will be possible to export the key

**`keyUsages`**  
  is an `Array` that indicates what can be done with the derived key.
The key usages must be allowed by the algorithm
set in `derivedKeyAlgorithm` .
Possible values:

**`encrypt`**  
  key for encrypting messages

**`decrypt`**  
  key for decrypting messages

**`sign`**  
  key for signing messages

**`verify`**  
  key for verifying signatures

**`deriveKey`**  
  key for deriving a new key

**`deriveBits`**  
  key for deriving bits

**`wrapKey`**  
  key for wrapping a key

**`unwrapKey`**  
  key for unwrapping a key

**`сrypto.subtle.digest` ( [`algorithm`](#crypto_digest_alg) , [`data`](#crypto_digest_data) )**  
  Generates a digest of the given data.
Takes as its arguments an identifier for the digest algorithm to use
and the data to digest.
Returns a `Promise` which will be fulfilled with the digest.
Possible values:

**`algorithm`**  
  is a string that defines the hash function to use: `SHA-1` (not for cryptographic applications), `SHA-256` , `SHA-384` , or `SHA-512`

**`data`**  
  is an `ArrayBuffer` , `TypedArray` , or `DataView` that contains the data to be digested

**`сrypto.subtle.exportKey` ( [`format`](#crypto_export_key_format) , [`key`](#crypto_export_key_keydata) )**  
  Exports a key: takes a key as
a [`CryptoKey`](#cryptokey) object
and returns the key in an external, portable format
(since [0.7.10](changes.xml#njs0.7.10) ).
If the `format` was `jwk` ,
then the `Promise` fulfills with a JSON object
containing the key.
Otherwise, the promise fulfills with an `ArrayBuffer` containing the key.
Possible values:

**`format`**  
  a string that describes the data format in which the key should be exported,
can be the following:

**`raw`**  
  the raw data format

**`pkcs8`**  
  the [PKCS #8](https://datatracker.ietf.org/doc/html/rfc5208) format

**`spki`**  
  the [SubjectPublicKeyInfo](https://datatracker.ietf.org/doc/html/rfc5280#section-4.1) format

**`jwk`**  
  the [JSON Web Key](https://datatracker.ietf.org/doc/html/rfc7517) (JWK) format (since [0.7.10](changes.xml#njs0.7.10) )

**`key`**  
  the [`CryptoKey`](#cryptokey) that contains the key to be exported

**`сrypto.subtle.generateKey` ( [`algorithm`](#crypto_generate_key_alg) , [`extractable`](#crypto_generate_key_extractable) , [`usage`](#crypto_generate_key_usage) )**  
  Generates a new key for symmetric algorithms
or key pair for public-key algorithms
(since [0.7.10](changes.xml#njs0.7.10) ).
Returns a `Promise` that fulfills with the generated key
as
a [`CryptoKey`](#cryptokey) or [`CryptoKeyPair`](#cryptokeypair) object.
Possible values:

**`algorithm`**  
  a dictionary object that defines the type of key to generate
and provides extra algorithm-specific parameters:

- for `RSASSA-PKCS1-v1_5` , `RSA-PSS` , or `RSA-OAEP` ,
pass the object with the following keys:
  - `name` is a string, should be set to `RSASSA-PKCS1-v1_5` , `RSA-PSS` , or `RSA-OAEP` ,
depending on the used algorithm
  - `hash` is a string that represents
the name of the `digest` function to use, can be `SHA-256` , `SHA-384` , or `SHA-512`
  
- for `ECDSA` ,
pass the object with the following keys:
  - `name` is a string, should be set to `ECDSA`
  - `namedCurve` is a string that represents
the name of the elliptic curve to use, may be `P-256` , `P-384` , or `P-521`
  
- for `HMAC` ,
pass the object with the following keys:
  - `name` is a string, should be set to `HMAC`
  - `hash` is a string that represents
the name of the `digest` function to use, can be `SHA-256` , `SHA-384` , or `SHA-512`
  - `length` (optional) is a number that represents
the length in bits of the key.
If omitted, the length of the key is equal to the length of the digest
generated by the chosen digest function.
  
- for `AES-CTR` , `AES-CBC` , or `AES-GCM` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }` ,
where `ALGORITHM` is the name of the algorithm
- for `ECDH` ,
pass the object with the following keys
(since [0.9.1](changes.xml#njs0.9.1) ):
  - `name` is a string, should be set to `ECDH`
  - `namedCurve` is a string that represents
the name of the elliptic curve to use, may be `P-256` , `P-384` , or `P-521`
  

**`extractable`**  
  boolean value that indicates if it is possible to export the key

**`usage`**  
  an `array` that indicates possible actions with the key:

**`encrypt`**  
  key for encrypting messages

**`decrypt`**  
  key for decrypting messages

**`sign`**  
  key for signing messages

**`verify`**  
  key for verifying signatures

**`deriveKey`**  
  key for deriving a new key

**`deriveBits`**  
  key for deriving bits

**`wrapKey`**  
  key for wrapping a key

**`unwrapKey`**  
  key for unwrapping a key

**`сrypto.subtle.importKey` ( [`format`](#crypto_import_key_format) , [`keyData`](#crypto_import_key_keydata) , [`algorithm`](#crypto_import_key_alg) , [`extractable`](#crypto_import_key_extractable) , [`keyUsages`](#crypto_import_key_keyusages) )**  
  Imports a key: takes as input a key in an external, portable format
and gives a [`CryptoKey`](#cryptokey) object.
Returns a `Promise` that fulfills with the imported key
as a [`CryptoKey`](#cryptokey) object.
Possible values:

**`format`**  
  a string that describes the data format of the key to import,
can be the following:

**`raw`**  
  the raw data format

**`pkcs8`**  
  the [PKCS #8](https://datatracker.ietf.org/doc/html/rfc5208) format

**`spki`**  
  the [SubjectPublicKeyInfo](https://datatracker.ietf.org/doc/html/rfc5280#section-4.1) format

**`jwk`**  
  the [JSON Web Key](https://datatracker.ietf.org/doc/html/rfc7517) (JWK) format (since [0.7.10](changes.xml#njs0.7.10) )

**`keyData`**  
  the `ArrayBuffer` , `TypedArray` , or `DataView` object that contains the key in the given format

**`algorithm`**  
  a dictionary object that defines the type of key to import
and provides extra algorithm-specific parameters:

- for `RSASSA-PKCS1-v1_5` , `RSA-PSS` , or `RSA-OAEP` ,
pass the object with the following keys:
  - `name` is a string, should be set to `RSASSA-PKCS1-v1_5` , `RSA-PSS` , or `RSA-OAEP` ,
depending on the used algorithm
  - `hash` is a string that represents
the name of the `digest` function to use, can be `SHA-1` , `SHA-256` , `SHA-384` , or `SHA-512`
  
- for `ECDSA` ,
pass the object with the following keys:
  - `name` is a string, should be set to `ECDSA`
  - `namedCurve` is a string that represents
the name of the elliptic curve to use, may be `P-256` , `P-384` , or `P-521`
  
- for `HMAC` ,
pass the object with the following keys:
  - `name` is a string, should be set to `HMAC`
  - `hash` is a string that represents
the name of the `digest` function to use, can be `SHA-256` , `SHA-384` , or `SHA-512`
  - `length` (optional) is a number that represents
the length in bits of the key.
If omitted, the length of the key is equal to the length of the digest
generated by the chosen digest function.
  
- for `AES-CTR` , `AES-CBC` , or `AES-GCM` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }` ,
where `ALGORITHM` is the name of the algorithm
- for `PBKDF2` ,
pass the `PBKDF2` string
- for `HKDF` ,
pass the `HKDF` string
- for `ECDH` ,
pass the object with the following keys
(since [0.9.1](changes.xml#njs0.9.1) ):
  - `name` is a string, should be set to `ECDH`
  - `namedCurve` is a string that represents
the name of the elliptic curve to use, may be `P-256` , `P-384` , or `P-521`
  

**`extractable`**  
  boolean value that indicates if it is possible to export the key

**`keyUsages`**  
  an `array` that indicates possible actions with the key:

**`encrypt`**  
  key for encrypting messages

**`decrypt`**  
  key for decrypting messages

**`sign`**  
  key for signing messages

**`verify`**  
  key for verifying signatures

**`deriveKey`**  
  key for deriving a new key

**`deriveBits`**  
  key for deriving bits

**`wrapKey`**  
  key for wrapping a key

**`unwrapKey`**  
  key for unwrapping a key

**`сrypto.subtle.sign` ( [`algorithm`](#crypto_sign_alg) , [`key`](#crypto_sign_key) , [`data`](#crypto_sign_data) )**  
  Returns `signature` as a `Promise` that fulfills with an `ArrayBuffer` containing the signature.
Possible values:

**`algorithm`**  
  is a string or object that specifies the signature algorithm to use
and its parameters:

- for `RSASSA-PKCS1-v1_5` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }`
- for `RSA-PSS` ,
pass the object with the following keys:
  - `name` is a string, should be set to `RSA-PSS`
  - `saltLength` is a long `integer` that represents the length of the random salt to use, in bytes
  
- for `ECDSA` ,
pass the object with the following keys:
  - `name` is a string, should be set to `ECDSA`
  - `hash` is an identifier for the digest algorithm to use,
can be `SHA-256` , `SHA-384` , or `SHA-512`
  
- for `HMAC` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }`

**`key`**  
  is a [`CryptoKey`](#cryptokey) object
that the key to be used for signing.
If algorithm identifies a public-key cryptosystem, this is the private key.

**`data`**  
  is an `ArrayBuffer` , `TypedArray` , or `DataView` object that contains the data to be signed

**`сrypto.subtle.verify` ( [`algorithm`](#crypto_verify_alg) , [`key`](#crypto_verify_key) , [`signature`](#crypto_verify_signature) , [`data`](#crypto_verify_data) )**  
  Verifies a digital signature,
returns a `Promise` that fulfills with a boolean value: `true` if the signature is valid,
otherwise `false` .
Possible values:

**`algorithm`**  
  is a string or object that specifies the algorithm to use
and its parameters:

- for `RSASSA-PKCS1-v1_5` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }`
- for `RSA-PSS` ,
pass the object with the following keys:
  - `name` is a string, should be set to `RSA-PSS`
  - `saltLength` is a long `integer` that represents the length of the random salt to use, in bytes
  
- for `ECDSA` ,
pass the object with the following keys:
  - `name` is a string, should be set to `ECDSA`
  - `hash` is an identifier for the digest algorithm to use,
can be `SHA-256` , `SHA-384` , or `SHA-512`
  
- for `HMAC` ,
pass the string identifying the algorithm or an object
of the form `{ "name": "ALGORITHM" }`

**`key`**  
  is a [`CryptoKey`](#cryptokey) object
that the key to be used for verifying.
It is the secret key for a symmetric algorithm
and the public key for a public-key system.

**`signature`**  
  is an `ArrayBuffer` , `TypedArray` , or `DataView` that contains the signature to verify

**`data`**  
  is an `ArrayBuffer` , `TypedArray` , or `DataView` object that contains the data whose signature is to be verified

## CryptoKey {#cryptokey}

 

The `CryptoKey` object represents a cryptographic `key` obtained from one of the `SubtleCrypto` methods: [`сrypto.subtle.generateKey()`](#crypto_subtle_generate_key) , [`сrypto.subtle.deriveKey()`](#crypto_subtle_derive_key) , [`сrypto.subtle.importKey()`](#crypto_subtle_import_key) .

**`CryptoKey.algorithm`**  
  returns an object describing the algorithm for which this key can be used
and any associated extra parameters
(since [0.8.0](changes.xml#njs0.8.0) ),
read-only

**`CryptoKey.extractable`**  
  a boolean value, `true` if the key can be exported
(since [0.8.0](changes.xml#njs0.8.0) ),
read-only

**`CryptoKey.type`**  
  a string value that indicates which kind of key is represented by the object,
read-only.
Possible values:

**`secret`**  
  This key is a secret key for use with a symmetric algorithm.

**`private`**  
  This key is the private half of an asymmetric algorithm's [`CryptoKeyPair`](#cryptokeypair)

**`public`**  
  This key is the public half of an asymmetric algorithm's [`CryptoKeyPair`](#cryptokeypair) .

**`CryptoKey.usages`**  
  An array of strings indicating what this key can be used for
(since [0.8.0](changes.xml#njs0.8.0) ),
read-only.
Possible array values:

**`encrypt`**  
  key for encrypting messages

**`decrypt`**  
  key for decrypting messages

**`sign`**  
  key for signing messages

**`verify`**  
  key for verifying signatures

**`deriveKey`**  
  key for deriving a new key

**`deriveBits`**  
  key for deriving bits

## CryptoKeyPair {#cryptokeypair}

 

The `CryptoKeyPair` is a dictionary object of the [WebCrypto API](#builtin_crypto) that represents an asymmetric key pair.

**`CryptoKeyPair.privateKey`**  
  A [`CryptoKey`](#cryptokey) object
representing the private key.

**`CryptoKeyPair.publicKey`**  
  A [`CryptoKey`](#cryptokey) object
representing the public key.

## njs {#njs}

 

The `njs` object is a global object that represents the current VM instance (since [0.2.0](changes.xml#njs0.2.0) ).

**`njs.version`**  
  Returns a string with the current version of njs
(for example, “0.7.4”).

**`njs.version_number`**  
  Returns a number with the current version of njs.
For example, “0.7.4” is returned as `0x000704` (since [0.7.4](changes.xml#njs0.7.4) ).

**`njs.dump(`**  
  Returns the pretty-print string representation for a value.

**`njs.memoryStats`**  
  Object containing memory statistics for current VM instance
(since [0.7.8](changes.xml#njs0.7.8) ).

**`size`**  
  amount of memory in bytes njs memory pool claimed from the operating system.

**`njs.on(`**  
  Registers a callback for the specified VM event
(since [0.5.2](changes.xml#njs0.5.2) ).
An event may be one of the following strings:

**`exit`**  
  is called before the VM is destroyed.
The callback is called without arguments.

## process {#process}

 

The `process` object is a global object that provides information about the current process ( [0.3.3](changes.xml#njs0.3.3) ).

**`process.argv`**  
  Returns an array that contains the command line arguments
passed when the current process was launched.

**`process.env`**  
  Returns an object containing the user environment.

> **Note:** By default, nginx removes all environment variables inherited
from its parent process except the TZ variable.
Use the [env](../ngx_core_module.xml#env) directive
to preserve some of the inherited variables.

**`process.kill(`**  
  Sends the signal to the process identified by `pid` .
Signal names are numbers or strings such as 'SIGINT' or 'SIGHUP'.
See [kill(2)](https://man7.org/linux/man-pages/man2/kill.2.html) for more information.

**`process.pid`**  
  Returns the PID of the current process.

**`process.ppid`**  
  Returns the PID of the current parent process.

## String {#string}

By default all strings in njs are Unicode strings. They correspond to ECMAScript strings that contain Unicode characters. Before [0.8.0](changes.xml#njs0.8.0) , byte strings were also supported.

### Byte strings {#byte_string}

> **Note:** Since [0.8.0](changes.xml#njs0.8.0) ,
the support for byte strings and byte string methods were removed.
When working with byte sequence,
the [Buffer](#buffer) object
and `Buffer` properties, such as [`r.requestBuffer`](#r_request_buffer) , [`r.rawVariables`](#r_raw_variables) ,
should be used.

Byte strings contain a sequence of bytes and are used to serialize Unicode strings to external data and deserialize from external sources. For example, the [toUTF8()](#string_toutf8) method serializes a Unicode string to a byte string using UTF-8 encoding:

```
>> '£'.toUTF8().toString('hex')
'c2a3'  /* C2 A3 is the UTF-8 representation of 00A3 ('£') code point */
```

The [toBytes()](#string_tobytes) method serializes a Unicode string with code points up to 255 into a byte string, otherwise, `null` is returned:

```
>> '£'.toBytes().toString('hex')
'a3'  /* a3 is a byte equal to 00A3 ('£') code point  */
```

**`String.bytesFrom(`**  
  The method was made obsolete in [0.4.4](changes.xml#njs0.4.4) and was removed in [0.8.0](changes.xml#njs0.8.0) .
The `Buffer.from` method should be used instead:

```
>> Buffer.from([0x62, 0x75, 0x66, 0x66, 0x65, 0x72]).toString()
'buffer'

>> Buffer.from('YnVmZmVy', 'base64').toString()
'buffer'
```

  Before [0.4.4](changes.xml#njs0.4.4) ,
created a byte string either from an array that contained octets,
or from an encoded string
( [0.2.3](changes.xml#njs0.2.3) ),
the encoding could be `hex` , `base64` , and `base64url` .

**`String.prototype.fromBytes(`**  
  the property was made obsolete in [0.7.7](changes.xml#njs0.7.7) and was removed in [0.8.0](changes.xml#njs0.8.0) .
Before [0.7.7](changes.xml#njs0.7.7) ,
returned a new Unicode string from a byte string
where each byte was replaced with a corresponding Unicode code point.

**`String.prototype.fromUTF8(`**  
  the property was made obsolete in [0.7.7](changes.xml#njs0.7.7) and was removed in [0.8.0](changes.xml#njs0.8.0) .
The [`TextDecoder`](#textedeoder) method
should be used instead.
Before [0.7.7](changes.xml#njs0.7.7) ,
converted a byte string containing a valid UTF-8 string
into a Unicode string,
otherwise `null` was returned.

**`String.prototype.toBytes(`**  
  the property was made obsolete in [0.7.7](changes.xml#njs0.7.7) and was removed in [0.8.0](changes.xml#njs0.8.0) .
Before [0.7.7](changes.xml#njs0.7.7) ,
serialized a Unicode string to a byte string,
returned `null` if a character larger than 255 was
found in the string.

**`String.prototype.toString(`**  
the property was made obsolete in [0.7.7](changes.xml#njs0.7.7) and was removed in [0.8.0](changes.xml#njs0.8.0) . Before [0.7.7](changes.xml#njs0.7.7) , encoded a string to `hex` , `base64` , or `base64url` :

```
>>  'αβγδ'.toString('base64url')
'zrHOss6zzrQ'
```

Before version [0.4.3](changes.xml#njs0.4.3) , only a [byte string](#string_tobytes) could be encoded:

```
>>  'αβγδ'.toUTF8().toString('base64url')
'zrHOss6zzrQ'
```

**`String.prototype.toUTF8(`**  
  the property was made obsolete in [0.7.7](changes.xml#njs0.7.7) and was removed in [0.8.0](changes.xml#njs0.8.0) .
The [`TextEncoder`](#textencoder) method
should be used instead.
Before [0.7.7](changes.xml#njs0.7.7) ,
serialized a Unicode string
to a byte string using UTF-8 encoding:

```
>> 'αβγδ'.toUTF8().length
8
>> 'αβγδ'.length
4
```

# web API {#webapi}

## Text Decoder {#textdecoder}

 

The `TextDecoder` produces a stream of code points from a stream of bytes ( [0.4.3](changes.xml#njs0.4.3) ).

**`TextDecoder([[`**  
  Creates a new `TextDecoder` object
for specified `encoding` ,
currently, only UTF-8 is supported.
The `options` is `TextDecoderOptions` dictionary with the property:

**`fatal`**  
  boolean flag indicating if [`TextDecoder.decode()`](#textdecoder_decode) must throw the `TypeError` exception when
a coding error is found, by default is `false` .

**`TextDecoder.prototype.encoding`**  
  Returns a string with the name of the encoding used by [`TextDecoder()`](#textdecoder) ,
read-only.

**`TextDecoder.prototype.fatal`**  
  boolean flag, `true` if
the error mode is fatal,
read-only.

**`TextDecoder.prototype.ignoreBOM`**  
  boolean flag, `true` if
the byte order marker is ignored,
read-only.

**`TextDecoder.prototype.decode(`**  
  Returns a string with the text
decoded from the `buffer` by [`TextDecoder()`](#textdecoder) .
The buffer can be `ArrayBuffer` .
The `options` is `TextDecodeOptions` dictionary with the property:

**`stream`**  
  boolean flag indicating if
additional data will follow in subsequent calls to `decode()` : `true` if processing the data in chunks, and `false` for the final chunk
or if the data is not chunked.
By default is `false` .

```
>> (new TextDecoder()).decode(new Uint8Array([206,177,206,178]))
αβ
```

## Text Encoder {#textencoder}

 

The `TextEncoder` object produces a byte stream with UTF-8 encoding from a stream of code points ( [0.4.3](changes.xml#njs0.4.3) ).

**`TextEncoder()`**  
  Returns a newly constructed `TextEncoder` that will generate a byte stream with UTF-8 encoding.

**`TextEncoder.prototype.encode(`**  
  Encodes `string` into a `Uint8Array` with UTF-8 encoded text.

**`TextEncoder.prototype.encodeInto(`**  
  Encodes a `string` to UTF-8,
puts the result into destination `Uint8Array` , and
returns a dictionary object that shows the progress of the encoding.
The dictionary object contains two members:

**`read`**  
  the number of UTF-16 units of code from the source `string` converted to UTF-8

**`written`**  
  the number of bytes modified in the destination `Uint8Array`

# timers {#njs_api_timers}

 

**`clearTimeout(`**  
  Cancels a `timeout` object
created by [`setTimeout()`](#settimeout) .

**`setTimeout(`**  
  Calls a `function` after a specified number of `milliseconds` .
One or more optional `arguments` can be passed to the specified function.
Returns a `timeout` object.

```
function handler(v)
{
    // ...
}

t = setTimeout(handler, 12);

// ...

clearTimeout(t);
```

## Global functions {#njs_global_functions}

 

**`atob(`**  
  Decodes a string of data which has been encoded
using `Base64` encoding.
The `encodedData` parameter is a binary string
that contains Base64-encoded data.
Returns a string that contains decoded data from `encodedData` .

The similar [`btoa()`](#btoa) method can be used to encode and transmit data which may otherwise cause communication problems, then transmit it and use the `atob()` method to decode the data again. For example, you can encode, transmit, and decode control characters such as ASCII values `0` through `31` .

```
const encodedData = btoa("text to encode"); // encode a string
const decodedData = atob(encodedData); // decode the string
```

**`btoa(`**  
  Creates a Base64-encoded ASCII string from a binary string.
The `stringToEncode` parameter is a binary string to encode.
Returns an ASCII string containing the Base64 representation of `stringToEncode` .

The method can be used to encode data which may otherwise cause communication problems, transmit it, then use the [`atob()`](#atob) method to decode the data again. For example, you can encode control characters such as ASCII values `0` through `31` .

```
const encodedData = btoa("text to encode"); // encode a string
const decodedData = atob(encodedData); // decode the string
```

# built-in modules {#builtin_modules}

## Buffer {#buffer}

 

**`Buffer.alloc(`**  
Allocates a new Buffer of a specified `size` . If `fill` is not specified, the Buffer will be zero-filled. If `fill` is specified, the allocated Buffer will be initialized by calling [`buf.fill(fill)`](#buf_fill) . If `fill` and `encoding` are specified, the allocated Buffer will be initialized by calling [`buf.fill(fill, encoding)`](#buf_fill) .

The `fill` parameter may be a `string` , `Buffer` , `Uint8Array` , or `integer` .

**`Buffer.allocUnsafe(`**  
The same as [`Buffer.alloc()`](#buffer_alloc) , with the difference that the memory allocated for the buffer is not initialized, the contents of the new buffer is unknown and may contain sensitive data.

**`Buffer.byteLength(`**  
  Returns the byte length of a specified value,
when encoded using `encoding` .
The value can be a `string` , `Buffer` , `TypedArray` , `DataView` , or `ArrayBuffer` .
If the value is a `string` ,
the `encoding` parameter is its encoding, can be `utf8` , `hex` , `base64` , `base64url` ;
by default is `utf8` .

**`Buffer.compare(`**  
  Compares `buffer1` with `buffer2` when sorting arrays of Buffer instances.
Returns `0` if `buffer1` is the same as `buffer2` , `1` if `buffer2` should come before `buffer1` when sorted, or `-1` if `buffer2` should come after `buffer1` when sorted.

**`Buffer.concat(`**  
  Returns a new Buffer
which is the result of concatenating all the Buffer instances in the list.
If there are no items in the list or the total length is 0,
a new zero-length Buffer is returned.
If `totalLength` is not specified,
it is calculated from the Buffer instances in list by adding their lengths.
If `totalLength` is specified,
it is coerced to an unsigned integer.
If the combined length of the Buffers in list exceeds `totalLength` ,
the result is truncated to `totalLength` .

**`Buffer.from(`**  
  Allocates a new Buffer using an array of bytes
in the range `0` – `255` .
Array entries outside that range will be truncated.

**`Buffer.from(`**  
  Creates a view of the `ArrayBuffer` without copying the underlying memory.
The optional `byteOffset` and `length` arguments
specify a memory range within the `arrayBuffer` that will be shared by the Buffer.

**`Buffer.from(`**  
  Copies the passed buffer data onto a new Buffer instance.

**`Buffer.from(`**  
  For objects whose `valueOf()` function
returns a value not strictly equal to object,
returns `Buffer.from(object.valueOf()` , `offsetOrEncoding` , `length` ).

**`Buffer.from(`**  
  Creates a new Buffer with a `string` .
The `encoding` parameter identifies the character encoding
to be used when converting a string into bytes.
The encoding can be `utf8` , `hex` , `base64` , `base64url` ;
by default is `utf8` .

**`Buffer.isBuffer(`**  
  A boolean value,
returns `true` if `object` is a Buffer.

**`Buffer.isEncoding(`**  
  A boolean value,
returns `true` if encoding is the name of a supported character encoding.

**`buffer[`**  
  The index operator that can be used to get and set the octet
at position `index` in `buffer` .
The values refer to individual bytes,
so the legal value range is between 0 and 255 (decimal).

**`buf.buffer`**  
  The underlying `ArrayBuffer` object
based on which this Buffer object is created.

**`buf.byteOffset`**  
  An integer,
specifying the `byteOffset` of the Buffers
underlying `ArrayBuffer` object.

**`buf.compare(`**  
  Compares buffer with `target` and returns a number
indicating whether buffer comes before, after, or is the same
as `target` in sort order.
Comparison is based on the actual sequence of bytes in each Buffer.
The `targetStart` is an integer specifying
the offset within `target` at which to begin comparison,
by default is 0.
The `targetEnd` is an integer specifying
the offset within `target` at which to end comparison,
by default is `target.length` .
The `sourceStart` is an integer specifying
the offset within buffer at which to begin comparison,
by default is 0.
The `sourceEnd` is an integer specifying
the offset within buffer at which to end comparison (not inclusive),
by default is `buf.length` .

**`buf.copy(`**  
  Copies data from a region of buffer to a region in `target` ,
even if the target memory region overlaps with buffer.
The `target` parameter is a `Buffer` or `Uint8Array` to copy into.

The `targetStart` is an integer specifying the offset within target at which to begin writing, by default is 0. The `sourceStart` is an integer specifying the offset within buffer from which to begin copying, by default is 0. The `sourceEnd` is an integer specifying the offset within buffer at which to stop copying (not inclusive) by default is `buf.length` .

**`buf.equals(`**  
  A boolean value,
returns `true` if both Buffer and `otherBuffer` have exactly the same bytes.

**`buf.fill(`**  
  Fills the Buffer with the specified `value` .
If the `offset` and `end` are not specified,
the entire Buffer will be filled.
The `value` is coerced to `uint32` if it is not a `string` , `Buffer` , or `integer` .
If the resulting integer is greater than 255,
the Buffer will be filled with `value` and 255.

**`buf.includes(`**  
  Equivalent to [`buf.indexOf()`](#buf_indexof) `!== -1` ,
returns `true` if the `value` was found
in Buffer.

**`buf.indexOf(`**  
  Returns an integer which is the index of the first occurrence of `value` in Buffer, or `-1` if Buffer does not contain value.
The `value` can be a `string` with specified `encoding` (by default `utf8` ), `Buffer` , `Unit8Array` ,
or a number between 0 and 255.

**`buf.lastIndexOf(`**  
  The same as [`buf.indexOf()`](#buf_indexof) ,
except the last occurrence of the `value` is found
instead of the first occurrence.
The `value` can be a string, Buffer, or
integer between 1 and 255.
If the `value` is an empty string or empty Buffer, `byteOffset` will be returned.

**`buf.length`**  
  Returns the number of bytes in Buffer.

**`buf.readIntBE(`**  
  Reads the `byteLength` from `buf` at the specified `offset` and interprets the result as a big-endian,
two's complement signed value supporting up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The similar methods are also supported: `buf.readInt8([offset])` , `buf.readInt16BE([offset])` , `buf.readInt32BE([offset])` .

**`buf.readIntLE(`**  
  Reads the `byteLength` from `buf` at the specified `offset` and interprets the result as a little-endian,
two's complement signed value supporting up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The similar methods are also supported: `buf.readInt8([offset])` , `buf.readInt16LE([offset])` , `buf.readInt32LE([offset])` .

**`buf.readUIntBE(`**  
  Reads the `byteLength` from `buf` at the specified `offset` and interprets the result as a big-endian
integer supporting up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The similar methods are also supported: `buf.readUInt8([offset])` , `buf.readUInt16BE([offset])` , `buf.readUInt32BE([offset])` .

**`buf.readUIntLE(`**  
  Reads the `byteLength` from `buf` at the specified `offset` and interprets the result as a little-endian
integer supporting up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The similar methods are also supported: `buf.readUInt8([offset])` , `buf.readUInt16LE([offset])` , `buf.readUInt32LE([offset])` .

**`buf.readDoubleBE` ([ `offset` ])**  
  Reads a 64-bit, big-endian double from `buf` at the specified `offset` .

**`buf.readDoubleLE` ([ `offset` ])**  
  Reads a 64-bit, little-endian double from `buf` at the specified `offset` .

**`buf.readFloatBE` ([ `offset` ])**  
  Reads a 32-bit, big-endian float from `buf` at the specified `offset` .

**`buf.readFloatLE` ([ `offset` ])**  
  Reads a 32-bit, little-endian float from `buf` at the specified `offset` .

**`buf.subarray([`**  
  Returns a new `buf` that references the same memory as the original,
but offset and cropped by `start` and `end` .
If `end` is greater than [`buf.length`](#buf_length) ,
the same result as that of end equal to [`buf.length`](#buf_length) is returned.

**`buf.slice([`**  
  Returns a new `buf` that references the same memory as the original,
but offset and cropped by the `start` and `end` values.
The method is not compatible with the `Uint8Array.prototype.slice()` ,
which is a superclass of Buffer.
To copy the slice, use `Uint8Array.prototype.slice()` .

**`buf.swap16` ()**  
  Interprets `buf` as an array of unsigned 16-bit numbers
and swaps the byte order in-place.
Throws an error if [`buf.length`](#buf_length) is not a multiple of 2.

**`buf.swap32` ()**  
  Interprets `buf` as an array of unsigned 32-bit numbers
and swaps the byte order in-place.
Throws an error if [`buf.length`](#buf_length) is not a multiple of 4.

**`buf.swap64` ()**  
  Interprets `buf` as an array of 64-bit numbers
and swaps byte order in-place.
Throws an error if [`buf.length`](#buf_length) is not a multiple of 8.

**`buf.toJSON` ()**  
  Returns a JSON representation of `buf.` `JSON.stringify()` implicitly calls this function when stringifying a Buffer instance.

**`buf.toString([`**  
  Decodes `buf` to a string
according to the specified character `encoding` which can be `utf8` , `hex` , `base64` , `base64url` .
The `start` and `end` parameters
may be passed to decode only a subset of Buffer.

**`buf.write(`**  
  Writes a `string` to `buf` at `offset` according to the character `encoding` .
The `length` parameter is the number of bytes to write.
If Buffer did not contain enough space to fit the entire string,
only part of string will be written,
however, partially encoded characters will not be written.
The `encoding` can be `utf8` , `hex` , `base64` , `base64url` .

**`buf.writeIntBE(`**  
  Writes `byteLength` bytes of `value` to `buf` at the specified `offset` as big-endian.
Supports up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The following similar methods are also supported: `buf.writeInt8` , `buf.writeInt16BE` , `buf.writeInt32BE` .

**`buf.writeIntLE(`**  
  Writes `byteLength` bytes of `value` to `buf` at the specified `offset` as little-endian.
Supports up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The following similar methods are also supported: `buf.writeInt8` , `buf.writeInt16LE` , `buf.writeInt32LE` .

**`buf.writeUIntBE(`**  
  Writes `byteLength` bytes of `value` to `buf` at the specified `offset` as big-endian.
Supports up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The following similar methods are also supported: `buf.writeUInt8` , `buf.writeUInt16BE` , `buf.writeUInt32BE` .

**`buf.writeUIntLE(`**  
  Writes `byteLength` bytes of `value` to `buf` at the specified `offset` as little-endian.
Supports up to 48 bits of accuracy.
The `byteLength` parameter is an integer between 1 and 6
specifying the number of bytes to read.

The following similar methods are also supported: `buf.writeUInt8` , `buf.writeUInt16LE` , `buf.writeUInt32LE` .

**`buf.writeDoubleBE(`**  
  Writes the `value` to `buf` at the specified `offset` as big-endian.

**`buf.writeDoubleLE(`**  
  Writes the `value` to `buf` at the specified `offset` as little-endian.

**`buf.writeFloatBE(`**  
  Writes the `value` to `buf` at the specified `offset` as big-endian.

**`buf.writeFloatLE(`**  
  Writes the `value` to `buf` at the specified `offset` as little-endian.

## Crypto {#crypto}

 

> **Note:** Since [0.7.0](changes.xml#njs0.7.0) ,
extended crypto API is available as a global [crypto](#builtin_crypto) object.

The Crypto module provides cryptographic functionality support. The Crypto module object is imported using `import crypto from 'crypto'` .

**`crypto.createHash(`**  
  Creates and returns a [Hash](#crypto_hash) object
that can be used to generate hash digests
using the given `algorithm` .
The algorithm can be `md5` , `sha1` , and `sha256` .

**`crypto.createHmac(`**  
  Creates and returns an [HMAC](#crypto_hmac) object that uses
the given `algorithm` and `secret key` .
The algorithm can be `md5` , `sha1` , and `sha256` .

### Hash {#crypto_hash}

 

**`hash.update(`**  
  Updates the hash content with the given `data` .

**`hash.digest([`**  
  Calculates the digest of all of the data passed using `hash.update()` .
The encoding can be `hex` , `base64` , and `base64url` .
If encoding is not provided, a Buffer object
( [0.4.4](changes.xml#njs0.4.4) ) is returned.

> **Note:** Before version ( [0.4.4](changes.xml#njs0.4.4) ),
a byte string was returned instead of a Buffer object.

**`hash.copy()`**  
  Makes a copy of the current state of the hash
(since [0.7.12](changes.xml#njs0.7.12) ).

```
import crypto from 'crypto';

crypto.createHash('sha1').update('A').update('B').digest('base64url');
/* BtlFlCqiamG-GMPiK_GbvKjdK10 */
```

### HMAC {#crypto_hmac}

 

**`hmac.update(`**  
  Updates the HMAC content with the given `data` .

**`hmac.digest([`**  
  Calculates the HMAC digest of all of the data passed using `hmac.update()` .
The encoding can be `hex` , `base64` , and `base64url` .
If encoding is not provided, a Buffer object
( [0.4.4](changes.xml#njs0.4.4) ) is returned.

> **Note:** Before version [0.4.4](changes.xml#njs0.4.4) ,
a byte string was returned instead of a Buffer object.

```
import crypto from 'crypto';

crypto.createHmac('sha1', 'secret.key').update('AB').digest('base64url');
/* Oglm93xn23_MkiaEq_e9u8zk374 */
```

## File System {#njs_api_fs}

 

 

The File System module provides operations with files.

The module object is imported using `import fs from 'fs'` . Since [0.3.9](changes.xml#njs0.3.9) , promissified versions of file system methods are available through `fs.promises` object after importing with `import fs from 'fs'` :

```
import fs from 'fs';

fs.promises.readFile("/file/path").then((data) => {
    /* <file data> */
});
```

**`accessSync(`**  
  Synchronously tests permissions for a file or directory
specified in the `path` ( [0.3.9](changes.xml#njs0.3.9) ).
If the check fails, an error will be returned,
otherwise, the method will return undefined.

**`mode`**  
  an optional integer
that specifies the accessibility checks to be performed,
by default is [`fs.constants.F_OK`](#access_const)

```
try {
    fs.accessSync('/file/path', fs.constants.R_OK | fs.constants.W_OK);
    console.log('has access');
} catch (e) {
    console.log('no access');)
}
```

**`appendFileSync(`**  
  Synchronously appends specified `data` to a file with provided `filename` .
The `data` is expected to be a string
or a Buffer object ( [0.4.4](changes.xml#njs0.4.4) ).
If the file does not exist, it will be created.
The `options` parameter is expected to be
an object with the following keys:

**`mode`**  
  mode option, by default is `0o666`

**`flag`**  
  file system [flag](#njs_api_fs_flags) ,
by default is `a`

**`closeSync(`**  
  Closes the `fd` file descriptor represented by an integer
used by the method.
Returns `undefined` .

**`existsSync(`**  
  Boolean value, returns `true` if the specified `path` exists.
( [0.8.2](changes.xml#njs0.8.2) )

**`fstatSync(`**  
  Retrieves the [`fs.Stats`](#fs_stats) object
for the file descriptor
( [0.7.7](changes.xml#njs0.7.7) ).
The `fd` parameter is an integer
representing the file descriptor used by the method.

**`lstatSync(`**  
  Synchronously retrieves
the [`fs.Stats`](#fs_stats) object
for the symbolic link referred to by `path` ( [0.7.1](changes.xml#njs0.7.1) ).
The `options` parameter is expected to be
an object with the following keys:

**`throwIfNoEntry`**  
  a boolean value which indicates
whether an exception is thrown if no file system entry exists,
rather than returning `undefined` ,
by default is `false` .

**`mkdirSync(`**  
  Synchronously creates a directory at the specified `path` ( [0.4.2](changes.xml#njs0.4.2) ).
The `options` parameter is expected to be an `integer` that specifies
the [mode](#fs_mkdirsync_mode) ,
or an object with the following keys:

**`mode`**  
  mode option, by default is `0o777` .

**`openSync(`**  
  Returns an integer
representing the file descriptor for the opened file `path` ( [0.7.7](changes.xml#njs0.7.7) ).

**`flags`**  
  file system [flag](#njs_api_fs_flags) ,
by default is `r`

**`mode`**  
  mode option, by default is `0o666`

**`promises.open(`**  
  Returns a [`FileHandle`](#fs_filehandle) object
representing the opened file `path` ( [0.7.7](changes.xml#njs0.7.7) ).

**`flags`**  
  file system [flag](#njs_api_fs_flags) ,
by default is `r`

**`mode`**  
  mode option, by default is `0o666`

**`readdirSync(`**  
  Synchronously reads the contents of a directory
at the specified `path` ( [0.4.2](changes.xml#njs0.4.2) ).
The `options` parameter is expected to be
a string that specifies [encoding](#fs_readdirsync_encoding) or an object with the following keys:

**`encoding`**  
  encoding, by default is `utf8` .
The encoding can be `utf8` and `buffer` ( [0.4.4](changes.xml#njs0.4.4) ).

**`withFileTypes`**  
  if set to `true` , the files array will contain [`fs.Dirent`](#fs_dirent) objects,
by default is `false` .

**`readFileSync(`**  
  Synchronously returns the contents of the file
with provided `filename` .
The `options` parameter holds `string` that specifies encoding.
If an encoding is specified, a string is returned,
otherwise, a Buffer object
( [0.4.4](changes.xml#njs0.4.4) ) is returned.

> **Note:** Before version [0.4.4](changes.xml#njs0.4.4) ,
a [byte string](#string_tobytes) was returned
if encoding was not specified.

  Otherwise, `options` is expected to be
an object with the following keys:

**`encoding`**  
  encoding, by default is not specified.
The encoding can be `utf8` , `hex` ( [0.4.4](changes.xml#njs0.4.4) ), `base64` ( [0.4.4](changes.xml#njs0.4.4) ), `base64url` ( [0.4.4](changes.xml#njs0.4.4) ).

**`flag`**  
  file system [flag](#njs_api_fs_flags) ,
by default is `r`

```
import fs from 'fs';

var file = fs.readFileSync('/file/path.tar.gz');
console.log(file.slice(0,2).toString('hex')) /* '1f8b' */
```

**`readlinkSync(`**  
  Synchronously gets the contents of the symbolic link `path` using [readlink(2)](https://man7.org/linux/man-pages/man2/readlink.2.html) ( [0.8.7](changes.xml#njs0.8.7) ).
The `options` argument can be a string specifying an encoding,
or an object with `encoding` property
specifying the character encoding to use.
If the `encoding` is `buffer` ,
the result is returned as a `Buffer` object,
otherwise as a string.

**`readSync(`**  
  Reads the content of a file path using file descriptor `fd` ,
returns the number of bytes read
( [0.7.7](changes.xml#njs0.7.7) ).

**`buffer`**  
  the `buffer` value can be a `Buffer` , `TypedArray` , or `DataView`

**`offset`**  
  is an `integer` representing
the position in buffer to write the data to

**`length`**  
  is an `integer` representing
the number of bytes to read

**`position`**  
  specifies where to begin reading from in the file,
the value can be `integer` or `null` ,
by default is `null` .
If `position` is `null` ,
data will be read from the current file position,
and the file position will be updated.
If position is an `integer` ,
the file position will be unchanged

**`realpathSync(`**  
  Synchronously computes the canonical pathname by resolving `.` , `..` and symbolic links using [realpath(3)](http://man7.org/linux/man-pages/man3/realpath.3.html) .
The `options` argument can be a string specifying an encoding,
or an object with an encoding property specifying the character encoding
to use for the path passed to the callback
( [0.3.9](changes.xml#njs0.3.9) ).

**`renameSync(`**  
  Synchronously changes the name or location of a file from `oldPath` to `newPath` ( [0.3.4](changes.xml#njs0.3.4) ).

```
import fs from 'fs';

fs.renameSync('hello.txt', 'HelloWorld.txt');
```

**`rmdirSync(`**  
  Synchronously removes a directory at the specified `path` ( [0.4.2](changes.xml#njs0.4.2) ).

**`statSync(`**  
  Synchronously retrieves
the [`fs.Stats`](#fs_stats) object
for the specified `path` ( [0.7.1](changes.xml#njs0.7.1) ).
The `path` can be a `string` or `buffer` .
The `options` parameter is expected to be
an object with the following keys:

**`throwIfNoEntry`**  
  a boolean value which indicates whether
an exception is thrown if no file system entry exists
rather than returning `undefined` ,
by default is `true` .

**`symlinkSync(`**  
  Synchronously creates the link called `path` pointing to `target` using [symlink(2)](http://man7.org/linux/man-pages/man2/symlink.2.html) ( [0.3.9](changes.xml#njs0.3.9) ).
Relative targets are relative to the link’s parent directory.

**`unlinkSync(`**  
  Synchronously unlinks a file by `path` ( [0.3.9](changes.xml#njs0.3.9) ).

**`writeFileSync(`**  
  Synchronously writes `data` to a file
with provided `filename` .
The `data` is expected to be a string
or a Buffer object ( [0.4.4](changes.xml#njs0.4.4) ).
If the file does not exist, it will be created,
if the file exists, it will be replaced.
The `options` parameter is expected to be
an object with the following keys:

**`mode`**  
  mode option, by default is `0o666`

**`flag`**  
  file system [flag](#njs_api_fs_flags) ,
by default is `w`

```
import fs from 'fs';

fs.writeFileSync('hello.txt', 'Hello world');
```

**`writeSync(`**  
  Writes a buffer to a file using file descriptor,
returns the `number` of bytes written
( [0.7.7](changes.xml#njs0.7.7) ).

**`fd`**  
  an `integer` representing the file descriptor

**`buffer`**  
  the `buffer` value can be a `Buffer` , `TypedArray` , or `DataView`

**`offset`**  
  is an `integer` that determines
the part of the buffer to be written,
by default `0`

**`length`**  
  is an `integer` specifying the number of bytes to write,
by default is an offset of [Buffer.byteLength](#buffer_bytelength)

**`position`**  
  refers to the offset from the beginning of the file
where this data should be written,
can be an `integer` or `null` ,
by default is `null` .
See also [pwrite(2)](https://man7.org/linux/man-pages/man2/write.2.html) .

**`writeSync(`**  
  Writes a `string` to a file
using file descriptor `fd` ,
returns the `number` of bytes written
( [0.7.7](changes.xml#njs0.7.7) ).

**`fd`**  
  is an `integer` representing a file descriptor

**`position`**  
  refers to the offset from the beginning of the file
where this data should be written,
can be an `integer` or `null` , by default is `null` .
See also [pwrite(2)](https://man7.org/linux/man-pages/man2/write.2.html)

**`encoding`**  
  is a `string` ,
by default is `utf8`

### fs.Dirent {#fs_dirent}

`fs.Dirent` is a representation of a directory entry— a file or a subdirectory. When [`readdirSync()`](#fs_readdirsync) is called with the [`withFileTypes`](#fs_readdirsync_withfiletypes) option, the resulting array contains `fs.Dirent` objects.

- `dirent.isBlockDevice()` —returns `true` if the `fs.Dirent` object describes
a block device.
- `dirent.isCharacterDevice()` —returns `true` if the `fs.Dirent` object describes
a character device.
- `dirent.isDirectory()` —returns `true` if the `fs.Dirent` object describes
a file system directory.
- `dirent.isFIFO()` —returns `true` if the `fs.Dirent` object describes
a first-in-first-out (FIFO) pipe.
- `dirent.isFile()` —returns `true` if the `fs.Dirent` object describes
a regular file.
- `dirent.isSocket()` —returns `true` if the `fs.Dirent` object describes
a socket.
- `dirent.isSymbolicLink()` —returns `true` if the `fs.Dirent` object describes
a symbolic link.
- `dirent.name` —
the name of the file `fs.Dirent` object refers to.

### fs.FileHandle {#fs_filehandle}

 

The `FileHandle` object is an object wrapper for a numeric file descriptor ( [0.7.7](changes.xml#njs0.7.7) ). Instances of the `FileHandle` object are created by the [`fs.promises.open()`](#fs_promises_open) method. If a `FileHandle` is not closed using the [`filehandle.close()`](#filehandle_close) method, it will try to automatically close the file descriptor, helping to prevent memory leaks. Please do not rely on this behavior because it can be unreliable. Instead, always explicitly close a `FileHandle` .

**`filehandle.close()`**  
  Closes the file handle after waiting for any pending operation on the handle
to complete.
Returns a `promise` , fulfills with undefined upon success.

**`filehandle.fd`**  
  The numeric file descriptor
managed by the `FileHandle` object.

**`filehandle.read(`**  
  Reads data from the file and stores that in the given buffer.

**`buffer`**  
  a buffer that will be filled with the file data read,
the value can be a `Buffer` , `TypedArray` , or `DataView`

**`offset`**  
  is an `integer` representing the location in the buffer at which to start filling

**`length`**  
  is an `integer` representing the number of bytes to read

**`position`**  
  the location where to begin reading data from the file,
the value can be `integer` , `null` .
If `null` , data will be read from the current file position
and the position will be updated.
If position is an `integer` ,
the current file position will remain unchanged.

  Returns a `Promise` which fulfills upon success
with an object with two properties:

**`bytesRead`**  
  is an `integer` representing the number of bytes read

**`buffer`**  
  is a reference to the passed argument in buffer, can be `Buffer` , `TypedArray` , or `DataView`

**`filehandle.stat()`**  
  Fulfills with an [fs.Stats](#fs_stats) for the file,
returns a `promise` .

**`filehandle.write(`**  
  Writes a buffer to the file.

**`buffer`**  
  the `buffer` value can be a `Buffer` , `TypedArray` , or `DataView`

**`offset`**  
  is an `integer` representing
the start position from within buffer where the data to write begins

**`length`**  
  is an `integer` representing
the number of bytes from buffer to write, by default
is an offset of [Buffer.byteLength](#buffer_bytelength)

**`position`**  
  the offset from the beginning of the file
where the data from buffer should be written,
can be an `integer` or `null` ,
by default is `null` .
If `position` is not a `number` ,
the data will be written at the current position.
See the POSIX [pwrite(2)](https://man7.org/linux/man-pages/man2/write.2.html) documentation for details.

  Returns a `Promise` which is resolved with an object
containing two properties:

**`bytesWritten`**  
  is an `integer` representing the number of bytes written

**`buffer`**  
  a reference to the buffer written, can be a `Buffer` , `TypedArray` , or `DataView`

> **Note:** It is unsafe to use `filehandle.write()` multiple times
on the same file without waiting for the promise to be resolved or rejected.

**`filehandle.write(`**  
  Writes a `string` to the file.

**`position`**  
  the offset from the beginning of the file
where the data from buffer should be written,
can be an `integer` or `null` ,
by default is `null` .
If `position` is not a `number` ,
the data will be written at the current position.
See the POSIX [pwrite(2)](https://man7.org/linux/man-pages/man2/write.2.html) documentation for details.

**`encoding`**  
  the expected encoding of the string, by default `utf8`

  Returns a `Promise` which is resolved with an object
containing two properties:

**`bytesWritten`**  
  is an `integer` representing the number of bytes written

**`buffer`**  
  a reference to the buffer written, can be a `Buffer` , `TypedArray` , or `DataView`

> **Note:** It is unsafe to use `filehandle.write()` multiple times
on the same file without waiting for the promise to be resolved or rejected.

### fs.Stats {#fs_stats}

The `fs.Stats` object provides information about a file. The object is returned from [fs.statSync()](#fs_statsync) and [fs.lstatSync()](#fs_lstatsync) .

- `stats.isBlockDevice()` —returns `true` if the `fs.Stats` object describes
a block device.
- `stats.isDirectory()` —returns `true` if the `fs.Stats` object describes
a file system directory.
- `stats.isFIFO()` —returns `true` if the `fs.Stats` object describes
a first-in-first-out (FIFO) pipe.
- `stats.isFile()` —returns `true` if the `fs.Stats` object describes
a regular file.
- `stats.isSocket()` —returns `true` if the `fs.Stats` object describes
a socket.
- `stats.isSymbolicLink()` —returns `true` if the `fs.Stats` object describes
a symbolic link.
- `stats.dev` —
the numeric identifier of the device containing the file.
- `stats.ino` —
the file system specific `Inode` number for the file.
- `stats.mode` —
a bit-field describing the file type and mode.
- `stats.nlink` —
the number of hard-links that exist for the file.
- `stats.uid` —
the numeric user identifier of the user that owns the file (POSIX).
- `stats.gid` —
the numeric group identifier of the group that owns the file (POSIX).
- `stats.rdev` —
the numeric device identifier if the file represents a device.
- `stats.size` —
the size of the file in bytes.
- `stats.blksize` —
the file system block size for i/o operations.
- `stats.blocks` —
the number of blocks allocated for this file.
- `stats.atimeMs` —
the timestamp indicating the last time this file was accessed expressed
in milliseconds since the POSIX Epoch.
- `stats.mtimeMs` —
the timestamp indicating the last time this file was modified expressed
in milliseconds since the POSIX Epoch.
- `stats.ctimeMs` —
the timestamp indicating the last time this file was changed expressed
in milliseconds since the POSIX Epoch.
- `stats.birthtimeMs` —
the timestamp indicating the creation time of this file expressed
in milliseconds since the POSIX Epoch.
- `stats.atime` —
the timestamp indicating the last time this file was accessed.
- `stats.mtime` —
the timestamp indicating the last time this file was modified.
- `stats.ctime` —
the timestamp indicating the last time this file was changed.
- `stats.birthtime` —
the timestamp indicating the creation time of this file.

### File Access Constants {#access_const}

The [`access()`](#fs_accesssync) method can accept the following flags. These flags are exported by `fs.constants` :

- `F_OK` —indicates that the file
is visible to the calling process,
used by default if no mode is specified
- `R_OK` —indicates that the file can be
read by the calling process
- `W_OK` —indicates that the file can be
written by the calling process
- `X_OK` —indicates that the file can be
executed by the calling process

### File System Flags {#njs_api_fs_flags}

The `flag` option can accept the following values:

- `a` —open a file for appending.
The file is created if it does not exist
- `ax` —the same as `a` but fails if the file already exists
- `a+` —open a file for reading and appending.
If the file does not exist, it will be created
- `ax+` —the same as `a+` but fails if the file already exists
- `as` —open a file for appending
in synchronous mode.
If the file does not exist, it will be created
- `as+` —open a file for reading and appending
in synchronous mode.
If the file does not exist, it will be created
- `r` —open a file for reading.
An exception occurs if the file does not exist
- `r+` —open a file for reading and writing.
An exception occurs if the file does not exist
- `rs+` —open a file for reading and writing
in synchronous mode.
Instructs the operating system to bypass the local file system cache
- `w` —open a file for writing.
If the file does not exist, it will be created.
If the file exists, it will be replaced
- `wx` —the same as `w` but fails if the file already exists
- `w+` —open a file for reading and writing.
If the file does not exist, it will be created.
If the file exists, it will be replaced
- `wx+` —the same as `w+` but fails if the file already exists

## Query String {#querystring}

 

The Query String module provides support for parsing and formatting URL query strings ( [0.4.3](changes.xml#njs0.4.3) ). The Query String module object is imported using `import qs from 'querystring'` .

**`querystring.decode()`**  
  is an alias for [`querystring.parse()`](#querystring_parse) .

**`querystring.encode()`**  
  is an alias for [`querystring.stringify()`](#querystring_stringify) .

**`querystring.escape(`**  
Performs URL encoding of the given `string` , returns an escaped query string. The method is used by [`querystring.stringify()`](#querystring_stringify) and should not be used directly.

**`querystring.parse(`**  
Parses the query string URL and returns an object.

The `separator` parameter is a substring for delimiting key and value pairs in the query string, by default is “ `&` ”.

The `equal` parameter is a substring for delimiting keys and values in the query string, by default is “ `=` ”.

The `options` parameter is expected to be an object with the following keys:

**`decodeURIComponent` `function`**  
  Function used
to decode percent-encoded characters in the query string,
by default is [`querystring.unescape()`](#querystring_unescape)

**`maxKeys` `number`**  
  the maximum number of keys to parse,
by default is `1000` .
The `0` value removes limitations for counting keys.

By default, percent-encoded characters within the query string are assumed to use the UTF-8 encoding, invalid UTF-8 sequences will be replaced with the `U+FFFD` replacement character.

For example, for the following query string

```
'foo=bar&abc=xyz&abc=123'
```

the output will be:

```
{
  foo: 'bar',
  abc: ['xyz', '123']
}
```

**`querystring.stringify(`**  
Serializes an object and returns a URL query string.

The `separator` parameter is a substring for delimiting key and value pairs in the query string, by default is “ `&` ”.

The `equal` parameter is a substring for delimiting keys and values in the query string, by default is “ `=` ”.

The `options` parameter is expected to be an object with the following keys:

**`encodeURIComponent` `function`**  
  The function to use when converting
URL-unsafe characters to percent-encoding in the query string,
by default is [`querystring.escape()`](#querystring_escape) .

By default, characters that require percent-encoding within the query string are encoded as UTF-8. If other encoding is required, then `encodeURIComponent` option should be specified.

For example, for the following command

```
querystring.stringify({ foo: 'bar', baz: ['qux', 'quux'], 123: '' });
```

the query string will be:

```
'foo=bar&baz=qux&baz=quux&123='
```

**`querystring.unescape(`**  
Performs decoding of URL percent-encoded characters of the `string` , returns an unescaped query string. The method is used by [`querystring.parse()`](#querystring_parse) and should not be used directly.

## XML {#xml}

 

The XML module allows working with XML documents (since [0.7.10](changes.xml#njs0.7.10) ). The XML module object is imported using `import xml from 'xml'` .

Example:

```
import xml from 'xml';

let data = `<note><to b="bar" a= "foo" >Tove</to><from>Jani</from></note>`;
let doc = xml.parse(data);

console.log(doc.note.to.$text) /* 'Tove' */
console.log(doc.note.to.$attr$b) /* 'bar' */
console.log(doc.note.$tags[1].$text) /* 'Jani' */

let dec = new TextDecoder();
let c14n = dec.decode(xml.exclusiveC14n(doc.note));
console.log(c14n) /* '<note><to a="foo" b="bar">Tove</to><from>Jani</from></note>' */

c14n = dec.decode(xml.exclusiveC14n(doc.note.to));
console.log(c14n) /* '<to a="foo" b="bar">Tove</to>' */

c14n = dec.decode(xml.exclusiveC14n(doc.note, doc.note.to /* excluding 'to' */));
console.log(c14n) /* '<note><from>Jani</from></note>' */
```

**`parse(`**  
  Parses a string or Buffer for an XML document,
returns an [`XMLDoc`](#xml_doc) wrapper object
representing the parsed XML document.

**`c14n(`**  
  Canonicalizes `root_node` and its children according to [Canonical XML Version 1.1](https://www.w3.org/TR/xml-c14n) .
The `root_node` can be [`XMLNode`](#xml_node) or [`XMLDoc`](#xml_doc) wrapper object
around XML structure.
Returns Buffer object that contains canonicalized output.

**`excluding_node`**  
  allows omitting from the output a part of the document

**`exclusiveC14n(`**  
  Canonicalizes `root_node` and its children according to [Exclusive XML
Canonicalization Version 1.0](https://www.w3.org/TR/xml-exc-c14n/) .

**`root_node`**  
  is [`XMLNode`](#xml_node) or [`XMLDoc`](#xml_doc) wrapper object
around XML structure

**`excluding_node`**  
  allows omitting from the output a part of the document
corresponding to the node and its children

**`withComments`**  
  a boolean value, `false` by default.
If `true` , canonicalization corresponds to [Exclusive XML
Canonicalization Version 1.0](http://www.w3.org/2001/10/xml-exc-c14n#WithComments) .
Returns Buffer object that contains canonicalized output.

**`prefix_list`**  
  an optional string with a space separated namespace prefixes
for namespaces that should also be included into the output

**`serialize()`**  
  The same as [`xml.c14n()`](#xml_c14n) (since [0.7.11](changes.xml#njs0.7.11) ).

**`serializeToString()`**  
  The same as [`xml.c14n()`](#xml_c14n) except it returns the result as a `string` (since [0.7.11](changes.xml#njs0.7.11) ).

**`XMLDoc`**  
  An XMLDoc wrapper object around XML structure,
the root node of the document.

**`doc.$root`**  
  the document's root by its name or undefined

**`doc.`**  
  the first root tag named `abc` as [`XMLNode`](#xml_node) wrapper object

**`XMLNode`**  
  An XMLNode wrapper object around XML tag node.

**`node.`**  
  the same as [`node.$tag$`](#node_tag)

**`node.$attr$`**  
  the node's attribute value of `abc` ,
writable
since [0.7.11](changes.xml#njs0.7.11)

**`node.$attr$` = `xyz`**  
  the same as [`node.setAttribute('`](#node_setattribute) (since [0.7.11](changes.xml#njs0.7.11) )

**`node.$attrs`**  
  an [`XMLAttr`](#xml_xmlattr) wrapper object
for all attributes of the node

**`node.$name`**  
  the name of the node

**`node.$ns`**  
  the namespace of the node

**`node.$parent`**  
  the parent node of the current node

**`node.$tag$`**  
  the first child tag of the node named `abc` ,
writable
since [0.7.11](changes.xml#njs0.7.11)

**`node.$tags`**  
  an array of all children tags

**`node.$tags = [node1, node2, ...]`**  
  the same as [`node.removeChildren`()](#node_removechildren) ; [`node.addChild(`](#node_addchild) ; [`node.addChild(`](#node_addchild) (since [0.7.11](changes.xml#njs0.7.11) ).

**`node.$tags$`**  
  all children tags named `abc` of the node,
writable
since [0.7.11](changes.xml#njs0.7.11)

**`node.$text`**  
  the content of the node,
writable
since [0.7.11](changes.xml#njs0.7.11)

**`node.$text = 'abc'`**  
  the same as [`node.setText('abc')`](#node_settext) (since [0.7.11](changes.xml#njs0.7.11) )

**`node.addChild(`**  
  adds XMLNode as a child to node
(since [0.7.11](changes.xml#njs0.7.11) ). `nd` is recursively copied before adding to the node

**`node.removeAllAttributes()`**  
  removes all attributes of the node
(since [0.7.11](changes.xml#njs0.7.11) )

**`node.removeAttribute(`**  
  removes the attribute named `attr_name` (since [0.7.11](changes.xml#njs0.7.11) )

**`node.removeChildren(`**  
  removes all the children tags named `tag_name` (since [0.7.11](changes.xml#njs0.7.11) ).
If `tag_name` is absent, all children tags are removed

**`node.removeText()`**  
  removes the node's text value
( [0.7.11](changes.xml#njs0.7.11) )

**`node.setAttribute(`**  
  sets a value for an `attr_name` (since [0.7.11](changes.xml#njs0.7.11) ).
When the value is `null` ,
the attribute named `attr_name` is deleted

**`node.setText(`**  
  sets a text value for the node
(since [0.7.11](changes.xml#njs0.7.11) ).
When the value is `null` , the text of the node is deleted.

**`XMLAttr`**  
  An XMLAttrs wrapper object around XML node attributes.

**`attr.`**  
  the attribute value of `abc`

## zlib {#zlib}

 

The zlib module provides compression functionality using the “deflate” and “inflate” algorithms (since [0.7.12](changes.xml#njs0.7.12) ). The zlib module object is imported using `import zlib from 'zlib'` .

**`deflateRawSync(`**  
  Compresses data using the “deflate” algorithm provided as a string or Buffer
and does not append a zlib header.
The buffer value can be a `Buffer` , `TypedArray` , or `DataView` . `Options` is an optional object that contains [zlib_options](#zlib_options) .
Returns Buffer instance that contains the compressed data.

**`deflateSync(`**  
  Compresses data using the “deflate” algorithm provided as a string or Buffer.
The Buffer value can be a `Buffer` , `TypedArray` , or `DataView` . `Options` is an optional object that contains [zlib_options](#zlib_options) .
Returns Buffer instance that contains the compressed data.

**`inflateRawSync(`**  
  Decompresses a raw stream by using the “deflate” algorithm.
Returns Buffer instance that contains the decompressed data.

**`inflateSync(`**  
  Decompresses a stream by using the “deflate” algorithm.
Returns Buffer instance that contains the decompressed data.

### zlib options {#zlib_options}

- `chunkSize` —is an integer,
by default is `1024`
- `dictionary` —is a `Buffer` , `TypedArray` , or `DataView` .
by default is empty
- `level` —is an integer, compression only,
see [zlib_compression_levels](#zlib_compression_levels)
- `memLevel` —is an integer
from `1` to `9` , compression only
- `strategy` —is an integer, compression only,
see [zlib_compression_strategy](#zlib_compression_strategy)
- `windowBits` —is an integer
from `-15` to `-9` for raw data,
from `9` to `15` for an ordinary stream

### zlib compression levels {#zlib_compression_levels}

 

### zlib compression strategy {#zlib_compression_strategy}

 

