# JavaScript Engine

**Revision:** 5  
**Language:** en


Starting from version [0.8.6](changes.xml#njs0.8.6),
multiple JavaScript engines are supported.
To specify a particular engine, use the `js_engine` directive
available for both the
[http](../http/ngx_http_js_module.xml#js_engine)
and
[stream](../stream/ngx_stream_js_module.xml#js_engine).
By default, the njs engine is used.

## njs engine {#njs_engine}

njs is an embeddable JavaScript engine
developed as a part of the njs module.
See the [Сompatibility](compatibility.html) section for details.

## QuickJS engine {#quickjs_engine}

[QuickJS](https://bellard.org/quickjs/) is a lightweight,
embeddable JavaScript engine that supports
the [ES2023](https://tc39.es/ecma262/2023/) specification,
including features as modules, asynchronous generators, proxies and BigInt.

Since version [0.8.6](changes.xml#njs0.8.6),
a drop-in replacement for
[njs/nginx objects](reference.html)
has been introduced
to ensure compatibility with the njs engine, with the following exceptions:


- njs-specific API:
[njs.dump()](reference.xml#njs_dump),
`console.dump()`.
- deprecated API:
`require()`,
use the `import` statement instead.
- `js_preload_object` directive for
[http](../http/ngx_http_js_module.xml#js_preload_object)
and
[stream](../stream/ngx_stream_js_module.xml#js_preload_object).

njs built-in modules status:


- [buffer](reference.xml#buffer):
since [0.8.6](changes.xml#njs0.8.6).
- [crypto](reference.xml#crypto):
since [0.8.10](changes.xml#njs0.8.10).
- [fs](reference.xml#njs_api_fs):
since [0.8.9](changes.xml#njs0.8.9).
- [querystring](reference.xml#querystring):
since [0.8.10](changes.xml#njs0.8.10).
- [WebCrypto](reference.xml#builtin_crypto):
since [0.8.10](changes.xml#njs0.8.10).
- [xml](reference.xml#xml):
since [0.8.10](changes.xml#njs0.8.10).
- [zlib](reference.xml#zlib):
since [0.8.5](changes.xml#njs0.8.5).

njs built-in objects status:


- [process](reference.xml#process):
since [0.8.8](changes.xml#njs0.8.8).
- [TextDecoder](reference.xml#textdecoder):
since [0.8.10](changes.xml#njs0.8.10).
- [TextEncoder](reference.xml#textencoder):
since [0.8.10](changes.xml#njs0.8.10).

nginx built-in objects status:


- [ngx.fetch](reference.xml#ngx_fetch):
since [0.9.1](changes.xml#njs0.9.1).
- [shared dictionary](reference.xml#ngx_shared):
since [0.8.8](changes.xml#njs0.8.8).
