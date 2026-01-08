# Движок JavaScript

**Revision:** 5  
**Language:** ru

Начиная с версии [0.8.6](../njs/changes.xml#njs0.8.6) поддерживается несколько JS-движков. Для выбора движка используется директива `js_engine` в [http](../http/ngx_http_js_module.xml#js_engine) и [stream](../stream/ngx_stream_js_module.xml#js_engine) . По умолчанию используется движок njs.

# Движок njs {#njs_engine}

njs — встроенный движок JavaScript, разработанный как часть модуля njs. Подробнее см. в разделе [Совместимость](compatibility.xml) .

# Движок QuickJS {#quickjs_engine}

[QuickJS](https://bellard.org/quickjs/) — компактный встроенный движок JavaScript, который поддерживает спецификацию [ES2023](https://tc39.es/ecma262/2023/) , включая модули, асинхронные генераторы, прокси и BigInt.

Начиная с [0.8.6](changes.xml#njs0.8.6) доступна оперативная замена [njs/nginx objects](reference.xml) для обеспечения совместимости с движком njs, но с некоторыми исключениями:

- API njs: [`njs.dump()`](reference.xml#njs_dump) , `console.dump()` .
- устаревшее API: `require()` ,
вместо необходимо использовать утверждение `import` .
- директива `js_preload_object` для [http](../http/ngx_http_js_module.xml#js_preload_object) и [stream](../stream/ngx_stream_js_module.xml#js_preload_object) .

статус встроенных модулей njs:

- [`buffer`](reference.xml#buffer) :
начиная с [0.8.6](changes.xml#njs0.8.6) .
- [`crypto`](reference.xml#crypto) :
начиная с [0.8.10](changes.xml#njs0.8.10) .
- [`fs`](reference.xml#njs_api_fs) :
начиная с [0.8.9](changes.xml#njs0.8.9) .
- [`querystring`](reference.xml#querystring) :
начиная с [0.8.10](changes.xml#njs0.8.10) .
- [`WebCrypto`](reference.xml#builtin_crypto) :
начиная с [0.8.10](changes.xml#njs0.8.10) .
- [`xml`](reference.xml#xml) :
начиная с [0.8.10](changes.xml#njs0.8.10) .
- [`zlib`](reference.xml#zlib) :
начиная с [0.8.5](changes.xml#njs0.8.5) .

статус встроенных объектов njs:

- [`process`](reference.xml#process) :
начиная с [0.8.8](changes.xml#njs0.8.8) .
- [`TextDecoder`](reference.xml#textdecoder) :
начиная с [0.8.10](changes.xml#njs0.8.10) .
- [`TextEncoder`](reference.xml#textencoder) :
начиная с [0.8.10](changes.xml#njs0.8.10) .

статус встроенных объектов nginx:

- [`ngx.fetch`](reference.xml#ngx_fetch) :
начиная с [0.9.1](changes.xml#njs0.9.1) .
- [`shared dictionary`](reference.xml#ngx_shared) :
начиная с [0.8.8](changes.xml#njs0.8.8) .

