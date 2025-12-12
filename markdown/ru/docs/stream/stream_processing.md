# Как nginx обрабатывает TCP/UDP-сессии

**Revision:** 4  
**Language:** ru

Обработка клиентской TCP/UDP-сессии происходит последовательными **фазами** :

**`Post-accept`**  
  Первая фаза после принятия клиентского соединения.
В этой фазе выполняется модуль [ngx_stream_realip_module](ngx_stream_realip_module.xml) .

**`Pre-access`**  
  Предварительная проверка доступа.
В этой фазе выполняются модули [ngx_stream_limit_conn_module](ngx_stream_limit_conn_module.xml) и [ngx_stream_set_module](ngx_stream_set_module.xml) .

**`Access`**  
  Ограничение доступа для клиента перед обработкой данных.
В этой фазе
выполняется модуль [ngx_stream_access_module](ngx_stream_access_module.xml) ,
при использовании [njs](../njs/index.xml) выполняется
директива [js_access](ngx_stream_js_module.xml#js_access) .

**`SSL`**  
  Терминирование TLS/SSL.
В этой фазе выполняется модуль [ngx_stream_ssl_module](ngx_stream_ssl_module.xml) .

**`Preread`**  
  Чтение первых байт данных в [буфер
предварительного чтения](ngx_stream_core_module.xml#preread_buffer_size) для анализа,
например модулем [ngx_stream_ssl_preread_module](ngx_stream_ssl_preread_module.xml) ,
перед их обработкой.
При использовании [njs](../njs/index.xml) в этой фазе выполняется
директива [js_preread](ngx_stream_js_module.xml#js_preread) .

**`Content`**  
  Обязательная фаза, в которой происходит обработка данных, как правило [проксирование](ngx_stream_proxy_module.xml) на [группу серверов](ngx_stream_upstream_module.xml) или [отправка](ngx_stream_return_module.xml) клиенту
заданного значения.
При использовании [njs](../njs/index.xml) в этой фазе выполняется
директива [js_filter](ngx_stream_js_module.xml#js_filter) .

**`Log`**  
  Заключительная фаза,
в которой записывается результат обработки клиентской сессии.
В этой фазе выполняется модуль [ngx_stream_log_module](ngx_stream_log_module.xml) .

