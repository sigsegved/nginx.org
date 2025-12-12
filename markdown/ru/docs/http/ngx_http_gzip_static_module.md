# Модуль ngx_http_gzip_static_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_http_gzip_static_module` позволяет отдавать вместо обычного файла предварительно сжатый файл с таким же именем и с расширением “ `.gz` ”.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_gzip_static_module` .

# Пример конфигурации {#example}

```
gzip_static  on;
gzip_proxied expired no-cache no-store private auth;
```

# Директивы {#directives}

## gzip_static

```
Syntax:  on | off | always
Default: off
Context: location, http, server
```

Разрешает (“ `on` ”) или запрещает (“ `off` ”) проверку готового сжатого файла. При использовании также учитываются директивы [gzip_http_version](ngx_http_gzip_module.xml#gzip_http_version) , [gzip_proxied](ngx_http_gzip_module.xml#gzip_proxied) , [gzip_disable](ngx_http_gzip_module.xml#gzip_disable) и [gzip_vary](ngx_http_gzip_module.xml#gzip_vary) .

Со значением “ `always` ” (1.3.6) во всех случаях будет использоваться сжатый файл, без проверки поддержки на стороне клиента. Это полезно, если на диске всё равно нет несжатых файлов, или используется модуль [ngx_http_gunzip_module](ngx_http_gunzip_module.xml) .

Сжимать файлы можно с помощью программы `gzip` или совместимой с ней. Желательно, чтобы дата и время модификации исходного и сжатого файлов совпадали.

