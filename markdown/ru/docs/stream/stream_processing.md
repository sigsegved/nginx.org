# Как nginx обрабатывает TCP/UDP-сессии

**Revision:** 4  
**Language:** ru


Обработка клиентской TCP/UDP-сессии происходит
последовательными **фазами**:


**`Post-accept`**  
  Первая фаза после принятия клиентского соединения.
В этой фазе выполняется модуль
[ngx_stream_realip_module](ngx_stream_realip_module.html).
**`Pre-access`**  
  Предварительная проверка доступа.
В этой фазе выполняются модули
[ngx_stream_limit_conn_module](ngx_stream_limit_conn_module.html)
и
[ngx_stream_set_module](ngx_stream_set_module.html).
**`Access`**  
  Ограничение доступа для клиента перед обработкой данных.
В этой фазе
выполняется модуль
[ngx_stream_access_module](ngx_stream_access_module.html),
при использовании [njs](../njs/index.html)
выполняется
директива [](ngx_stream_js_module.xml#js_access).
**`SSL`**  
  Терминирование TLS/SSL.
В этой фазе выполняется модуль
[ngx_stream_ssl_module](ngx_stream_ssl_module.html).
**`Preread`**  
  Чтение первых байт данных в
[буфер
предварительного чтения](ngx_stream_core_module.xml#preread_buffer_size) для анализа,
например модулем
[ngx_stream_ssl_preread_module](ngx_stream_ssl_preread_module.html),
перед их обработкой.
При использовании [njs](../njs/index.html)
в этой фазе выполняется
директива [](ngx_stream_js_module.xml#js_preread).
**`Content`**  
  Обязательная фаза, в которой происходит обработка данных, как правило
[проксирование](ngx_stream_proxy_module.html) на
[группу серверов](ngx_stream_upstream_module.html)
или [отправка](ngx_stream_return_module.html) клиенту
заданного значения.
При использовании [njs](../njs/index.html)
в этой фазе выполняется
директива [](ngx_stream_js_module.xml#js_filter).
**`Log`**  
  Заключительная фаза,
в которой записывается результат обработки клиентской сессии.
В этой фазе выполняется модуль
[ngx_stream_log_module](ngx_stream_log_module.html).
