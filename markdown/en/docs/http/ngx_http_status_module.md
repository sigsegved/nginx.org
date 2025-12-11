# Module ngx_http_status_module

**Revision:** 19  
**Language:** en


The `ngx_http_status_module` module provides
access to various status information.

> **Note:** This module was available as part of our
commercial subscription
until 1.13.10.
It was superseded by the
[ngx_http_api_module](ngx_http_api_module.html) module
in 1.13.3.

## Example Configuration {#example}

```
http {
    upstream backend {
        zone http_backend 64k;

        server backend1.example.com weight=5;
        server backend2.example.com;
    }

    proxy_cache_path /data/nginx/cache_backend keys_zone=cache_backend:10m;

    server {
        server_name backend.example.com;

        location / {
            proxy_pass  http://backend;
            proxy_cache cache_backend;

            health_check;
        }

        status_zone server_backend;
    }

    server {
        listen 127.0.0.1;

        location /upstream_conf {
            upstream_conf;
        }

        location /status {
            status;
        }

        location = /status.html {
        }
    }
}

stream {
    upstream backend {
        zone stream_backend 64k;

        server backend1.example.com:12345 weight=5;
        server backend2.example.com:12345;
    }

    server {
        listen      127.0.0.1:12345;
        proxy_pass  backend;
        status_zone server_backend;
        health_check;
    }
}
```

Examples of status requests with this configuration:

```
http://127.0.0.1/status
http://127.0.0.1/status/nginx_version
http://127.0.0.1/status/caches/cache_backend
http://127.0.0.1/status/upstreams
http://127.0.0.1/status/upstreams/backend
http://127.0.0.1/status/upstreams/backend/peers/1
http://127.0.0.1/status/upstreams/backend/peers/1/weight
http://127.0.0.1/status/stream
http://127.0.0.1/status/stream/upstreams
http://127.0.0.1/status/stream/upstreams/backend
http://127.0.0.1/status/stream/upstreams/backend/peers/1
http://127.0.0.1/status/stream/upstreams/backend/peers/1/weight
```

The simple monitoring page is shipped with this distribution,
accessible as “`/status.html`” in the default configuration.
It requires the locations “`/status`” and
“`/status.html`” to be configured as shown above.

## Directives {#directives}




location


The status information will be accessible from the surrounding location.
Access to this location should be
limited.




json
jsonp [callback]
json
http
server
location


By default, status information is output in the JSON format.



Alternatively, data may be output as JSONP.
The callback parameter specifies the name of a callback function.
Parameter value can contain variables.
If parameter is omitted, or the computed value is an empty string,
then “ngx_status_jsonp_callback” is used.




zone

server


Enables collection of virtual
http
or
stream
(1.7.11) server status information in the specified zone.
Several servers may share the same zone.



## Data {#data}

The following status information is provided:

**`version`**  
  Version of the provided data set.
The current version is 8.
**`nginx_version`**  
  Version of nginx.
**`nginx_build`**  
  Name of nginx build.
**`address`**  
  The address of the server that accepted status request.
**`generation`**  
  The total number of configuration
[reloads](../control.xml#reconfiguration).
**`load_timestamp`**  
  Time of the last reload of configuration, in milliseconds since Epoch.
**`timestamp`**  
  Current time in milliseconds since Epoch.
**`pid`**  
  The ID of the worker process that handled status request.
**`ppid`**  
  The ID of the master process that started
the worker process.
**`processes`**  
  **`respawned`**  
  The total number of abnormally terminated and respawned
child processes.
**`connections`**  
  **`accepted`**  
  The total number of accepted client connections.
**`dropped`**  
  The total number of dropped client connections.
**`active`**  
  The current number of active client connections.
**`idle`**  
  The current number of idle client connections.
**`ssl`**  
  **`handshakes`**  
  The total number of successful SSL handshakes.
**`handshakes_failed`**  
  The total number of failed SSL handshakes.
**`session_reuses`**  
  The total number of session reuses during SSL handshake.
**`requests`**  
  **`total`**  
  The total number of client requests.
**`current`**  
  The current number of client requests.
**`server_zones`**  
  For each :

**`processing`**  
  The number of
client requests that are currently being processed.
**`requests`**  
  The total number of
client requests received from clients.
**`responses`**  
  **`total`**  
  The total number of
responses sent to clients.
**`1xx`,
`2xx`,
`3xx`,
`4xx`,
`5xx`**  
  The number of responses with status codes 1xx, 2xx, 3xx, 4xx, and 5xx.
**`discarded`**  
  The total number of requests completed without sending a response.
**`received`**  
  The total number of bytes received from clients.
**`sent`**  
  The total number of bytes sent to clients.
**`slabs`**  
  For each shared memory zone that uses slab allocator:

**`pages`**  
  **`used`**  
  The current number of used memory pages.
**`free`**  
  The current number of free memory pages.
**`slots`**  
  For each memory slot size (8, 16, 32, 64, 128, etc.)
the following data are provided:

**`used`**  
  The current number of used memory slots.
**`free`**  
  The current number of free memory slots.
**`reqs`**  
  The total number of attempts to allocate memory of specified size.
**`fails`**  
  The number of unsuccessful attempts to allocate memory of specified size.
**`upstreams`**  
  For each
[dynamically
configurable](ngx_http_upstream_module.xml#zone)
[group](ngx_http_upstream_module.xml#upstream),
the following data are provided:

**`peers`**  
  For each
[](ngx_http_upstream_module.xml#server),
the following data are provided:

**`id`**  
  The ID of the server.
**`server`**  
  An
[address](ngx_http_upstream_module.xml#server)
of the server.
**`name`**  
  The name of the server specified in the
[](ngx_http_upstream_module.xml#server)
directive.
**`service`**  
  The [](ngx_http_upstream_module.xml#service)
parameter value of the
[](ngx_http_upstream_module.xml#server) directive.
**`backup`**  
  A boolean value indicating whether the server is a
[](ngx_http_upstream_module.xml#backup)
server.
**`weight`**  
  [Weight](ngx_http_upstream_module.xml#weight)
of the server.
**`state`**  
  Current state, which may be one of
“`up`”,
“`draining`”,
“`down`”,
“`unavail`”,
“`checking`”,
or
“`unhealthy`”.
**`active`**  
  The current number of active connections.
**`max_conns`**  
  The [](ngx_http_upstream_module.xml#max_conns) limit
for the server.
**`requests`**  
  The total number of
client requests forwarded to this server.
**`responses`**  
  **`total`**  
  The total number of
responses obtained from this server.
**`1xx`,
`2xx`,
`3xx`,
`4xx`,
`5xx`**  
  The number of responses with status codes 1xx, 2xx, 3xx, 4xx, and 5xx.
**`sent`**  
  The total number of bytes sent to this server.
**`received`**  
  The total number of bytes received from this server.
**`fails`**  
  The total number of
unsuccessful attempts to communicate with the server.
**`unavail`**  
  How many times
the server became unavailable for client requests
(state “`unavail`”)
due to the number of unsuccessful attempts reaching the
[](ngx_http_upstream_module.xml#max_fails)
threshold.
**`health_checks`**  
  **`checks`**  
  The total number of
[health check](ngx_http_upstream_hc_module.xml#health_check)
requests made.
**`fails`**  
  The number of failed health checks.
**`unhealthy`**  
  How many times
the server became unhealthy (state “`unhealthy`”).
**`last_passed`**  
  Boolean indicating
if the last health check request was successful and passed
[tests](ngx_http_upstream_hc_module.xml#match).
**`downtime`**  
  Total time
the server was in the “`unavail`”,
“`checking`”, and “`unhealthy`” states.
**`downstart`**  
  The time (in milliseconds since Epoch)
when the server became
“`unavail`”,
“`checking`”, or “`unhealthy`”.
**`selected`**  
  The time (in milliseconds since Epoch)
when the server was last selected to process a request (1.7.5).
**`header_time`**  
  The average time to get the
[response
header](ngx_http_upstream_module.xml#var_upstream_header_time) from the server (1.7.10).
Prior to version 1.11.6,
the field was available only when using the
[](ngx_http_upstream_module.xml#least_time)
load balancing method.
**`response_time`**  
  The average time to get the
[full
response](ngx_http_upstream_module.xml#var_upstream_response_time) from the server (1.7.10).
Prior to version 1.11.6,
the field was available only when using the
[](ngx_http_upstream_module.xml#least_time)
load balancing method.
**`keepalive`**  
  The current number of
idle [](ngx_http_upstream_module.xml#keepalive) connections.
**`zombies`**  
  The current number of servers removed
from the group but still processing active client requests.
**`zone`**  
  The name of the shared memory
[](ngx_http_upstream_module.xml#zone)
that keeps the group’s configuration and run-time state.
**`queue`**  
  For the requests [](ngx_http_upstream_module.xml#queue),
the following data are provided:

**`size`**  
  The current number of requests in the queue.
**`max_size`**  
  The maximum number of requests that can be in the queue at the same time.
**`overflows`**  
  The total number of requests rejected due to the queue overflow.
**`caches`**  
  For each cache (configured by
[](ngx_http_proxy_module.xml#proxy_cache_path) and the likes):

**`size`**  
  The current size of the cache.
**`max_size`**  
  The limit on the maximum size of the cache specified in the configuration.
**`cold`**  
  A boolean value indicating whether the “cache loader” process is still loading
data from disk into the cache.
**`hit`,
    `stale`,
    `updating`,
    `revalidated`**  
  **`responses`**  
  The total number of responses read from the cache (hits, or stale responses
due to [](ngx_http_proxy_module.xml#proxy_cache_use_stale)
and the likes).
**`bytes`**  
  The total number of bytes read from the cache.
**`miss`,
    `expired`,
    `bypass`**  
  **`responses`**  
  The total number of responses not taken from the cache (misses, expires, or
bypasses due to
[](ngx_http_proxy_module.xml#proxy_cache_bypass)
and the likes).
**`bytes`**  
  The total number of bytes read from the proxied server.
**`responses_written`**  
  The total number of responses written to the cache.
**`bytes_written`**  
  The total number of bytes written to the cache.
**`stream`**  
  **`server_zones`**  
  For each :

**`processing`**  
  The number of
client connections that are currently being processed.
**`connections`**  
  The total number of
connections accepted from clients.
**`sessions`**  
  **`total`**  
  The total number of completed client sessions.
**`2xx`,
`4xx`,
`5xx`**  
  The number of sessions completed with
[status codes](../stream/ngx_stream_core_module.xml#var_status)
2xx, 4xx, or 5xx.
**`discarded`**  
  The total number of connections completed without creating a session.
**`received`**  
  The total number of bytes received from clients.
**`sent`**  
  The total number of bytes sent to clients.
**`upstreams`**  
  For each
[dynamically
configurable](../stream/ngx_stream_upstream_module.xml#zone)
[group](../stream/ngx_stream_upstream_module.xml#upstream),
the following data are provided:

**`peers`**  
  For each
[](../stream/ngx_stream_upstream_module.xml#server)
the following data are provided:

**`id`**  
  The ID of the server.
**`server`**  
  An
[address](../stream/ngx_stream_upstream_module.xml#server)
of the server.
**`name`**  
  The name of the server specified in the
[](../stream/ngx_stream_upstream_module.xml#server) directive.
**`service`**  
  The [](../stream/ngx_stream_upstream_module.xml#service)
parameter value of the
[](../stream/ngx_stream_upstream_module.xml#server) directive.
**`backup`**  
  A boolean value indicating whether the server is a
[](../stream/ngx_stream_upstream_module.xml#backup)
server.
**`weight`**  
  [Weight](../stream/ngx_stream_upstream_module.xml#weight)
of the server.
**`state`**  
  Current state, which may be one of
“`up`”,
“`down`”,
“`unavail`”,
“`checking`”,
or
“`unhealthy`”.
**`active`**  
  The current number of connections.
**`max_conns`**  
  The [](../stream/ngx_stream_upstream_module.xml#max_conns) limit
for the server.
**`connections`**  
  The total number of
client connections forwarded to this server.
**`connect_time`**  
  The average time to connect to the upstream server.
Prior to version 1.11.6,
the field was available only when using the
[](../stream/ngx_stream_upstream_module.xml#least_time)
load balancing method.
**`first_byte_time`**  
  The average time to receive the first byte of data.
Prior to version 1.11.6,
the field was available only when using the
[](../stream/ngx_stream_upstream_module.xml#least_time)
load balancing method.
**`response_time`**  
  The average time to receive the last byte of data.
Prior to version 1.11.6,
the field was available only when using the
[](../stream/ngx_stream_upstream_module.xml#least_time)
load balancing method.
**`sent`**  
  The total number of bytes sent to this server.
**`received`**  
  The total number of bytes received from this server.
**`fails`**  
  The total number of
unsuccessful attempts to communicate with the server.
**`unavail`**  
  How many times
the server became unavailable for client connections
(state “`unavail`”)
due to the number of unsuccessful attempts reaching the
[](../stream/ngx_stream_upstream_module.xml#max_fails)
threshold.
**`health_checks`**  
  **`checks`**  
  The total number of
[health check](../stream/ngx_stream_upstream_hc_module.xml#health_check)
requests made.
**`fails`**  
  The number of failed health checks.
**`unhealthy`**  
  How many times
the server became unhealthy (state “`unhealthy`”).
**`last_passed`**  
  Boolean indicating
if the last health check request was successful and passed
[tests](../stream/ngx_stream_upstream_hc_module.xml#match).
**`downtime`**  
  Total time
the server was in the “`unavail`”,
“`checking`”, and “`unhealthy`” states.
**`downstart`**  
  The time (in milliseconds since Epoch)
when the server became
“`unavail`”,
“`checking`”, or “`unhealthy`”.
**`selected`**  
  The time (in milliseconds since Epoch)
when the server was last selected to process a connection.
**`zombies`**  
  The current number of servers removed
from the group but still processing active client connections.
**`zone`**  
  The name of the shared memory
[](../stream/ngx_stream_upstream_module.xml#zone)
that keeps the group’s configuration and run-time state.

## Compatibility {#compatibility}

- The
 field in
http and stream
upstreams
was added in  8.
- The  status data
were added in  8.
- The
checking state
was added in  8.
- The
 and  fields in
http and stream
upstreams
were added in  8.
- The
 and  fields
were added in  8.
- The
 status data
and the discarded field in
stream server_zones
were added in  7.
- The  field
was moved from nginx [debug](../debugging_log.html) version
in  6.
- The  status data
were added in  6.
- The
 field in

was added in  6.
- The  status data
were added in  6.
- The
 field
was added in  6.
- The list of servers in 
was moved into  in
 6.
- The `keepalive` field of an upstream server
was removed in  5.
- The stream status data
were added in  5.
- The
 field
was added in  5.
- The
 field in

was added in  5.
- The
 and  fields in

were added in  5.
- The
 field in

was added in  4.
- The draining state in

was added in  4.
- The
 and  fields in

were added in  3.
- The `revalidated` field in

was added in  3.
- The , ,
and  status data
were added in  2.
