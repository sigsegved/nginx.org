# How nginx processes a TCP/UDP session

**Revision:** 4  
**Language:** en

A TCP/UDP session from a client is processed in successive steps called **phases** :

**`Post-accept`**  
  The first phase after accepting a client connection.
The [ngx_stream_realip_module](ngx_stream_realip_module.xml) module is invoked at this phase.

**`Pre-access`**  
  Preliminary check for access.
The [ngx_stream_limit_conn_module](ngx_stream_limit_conn_module.xml) and [ngx_stream_set_module](ngx_stream_set_module.xml) modules are invoked at this phase.

**`Access`**  
  Client access limitation before actual data processing.
At this phase,
the [ngx_stream_access_module](ngx_stream_access_module.xml) module is invoked,
for [njs](../njs/index.xml) ,
the [js_access](ngx_stream_js_module.xml#js_access) directive
is invoked.

**`SSL`**  
  TLS/SSL termination.
The [ngx_stream_ssl_module](ngx_stream_ssl_module.xml) module is invoked at this phase.

**`Preread`**  
  Reading initial bytes of data into the [preread buffer](ngx_stream_core_module.xml#preread_buffer_size) to allow modules such as [ngx_stream_ssl_preread_module](ngx_stream_ssl_preread_module.xml) analyze the data before its processing.
For [njs](../njs/index.xml) ,
the [js_preread](ngx_stream_js_module.xml#js_preread) directive
is invoked at this phase.

**`Content`**  
  Mandatory phase where data is actually processed, usually [proxied](ngx_stream_proxy_module.xml) to [upstream](ngx_stream_upstream_module.xml) servers,
or a specified value
is [returned](ngx_stream_return_module.xml) to a client.
For [njs](../njs/index.xml) ,
the [js_filter](ngx_stream_js_module.xml#js_filter) directive
is invoked at this phase.

**`Log`**  
  The final phase
where the result of a client session processing is recorded.
The [ngx_stream_log_module](ngx_stream_log_module.xml) module is invoked at this phase.

