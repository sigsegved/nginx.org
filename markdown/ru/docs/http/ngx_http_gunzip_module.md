# Модуль ngx_http_gunzip_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_http_gunzip_module` — это фильтр, распаковывающий ответы с “ `Content-Encoding: gzip` ” для тех клиентов, которые не поддерживают метод сжатия “gzip”. Модуль будет полезен, когда данные желательно хранить сжатыми для экономии места и сокращения затрат на ввод-вывод.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_gunzip_module` .

# Пример конфигурации {#example}

```
location /storage/ {
    gunzip on;
    ...
}
```

# Директивы {#directives}

## gunzip

```
Syntax:  gunzip on | off;
Default: off
Context: location, http, server
```

Разрешает или запрещает распаковку ответов, сжатых методом gzip, для тех клиентов, которые его не поддерживают. Если разрешено, то для определения, поддерживает ли клиент gzip, также учитываются следующие директивы: [gzip_http_version](ngx_http_gzip_module.xml#gzip_http_version) , [gzip_proxied](ngx_http_gzip_module.xml#gzip_proxied) и [gzip_disable](ngx_http_gzip_module.xml#gzip_disable) . См. также директиву [gzip_vary](ngx_http_gzip_module.xml#gzip_vary) .

## gunzip_buffers

```
Syntax:  gunzip_buffers число размер;
Default: 32 4k|16 8k
Context: location, http, server
```

Задаёт `число` и `размер` буферов, в которые будет разжиматься ответ. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

