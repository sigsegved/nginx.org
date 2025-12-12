# Модуль ngx_http_dav_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_http_dav_module` предназначен для автоматизации задач управления файлами на сервере по протоколу WebDAV. Модуль обрабатывает HTTP- и WebDAV-методы PUT, DELETE, MKCOL, COPY и MOVE.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-http_dav_module` .

> **Note:** WebDAV-клиенты, которые требуют для работы дополнительных WebDAV-методов,
не будут работать с этим модулем.

# Пример конфигурации {#example}

```
location / {
    root                  /data/www;

    client_body_temp_path /data/client_temp;

    dav_methods PUT DELETE MKCOL COPY MOVE;

    create_full_put_path  on;
    dav_access            group:rw  all:r;

    limit_except GET {
        allow 192.168.1.0/32;
        deny  all;
    }
}
```

# Директивы {#directives}

## create_full_put_path

```
Syntax:  on | off
Default: off
Context: location, http, server
```

По спецификации WebDAV-метод PUT может создавать файл только в уже существующем каталоге. Данная директива разрешает создавать все необходимые промежуточные каталоги.

## dav_access

```
Syntax:  пользователи:права ...
Default: user:rw
Context: location, http, server
```

Задаёт права доступа для создаваемых файлов и каталогов, например,

```
dav_access user:rw group:rw all:r;
```

Если заданы какие-либо права для `group` или `all` , то права для `user` указывать необязательно:

```
dav_access group:rw all:r;
```

## dav_methods

```
Syntax:  off | метод ...
Default: off
Context: location, http, server
```

Разрешает указанные HTTP- и WebDAV-методы. Параметр `off` запрещает все методы, обрабатываемые данным модулем. Поддерживаются следующие методы: `PUT` , `DELETE` , `MKCOL` , `COPY` и `MOVE` .

Файл, загружаемый методом PUT, записывается во временный файл, а потом этот файл переименовывается. Начиная с версии 0.8.9 временный файл и его постоянное место хранения могут располагаться на разных файловых системах. Однако нужно учитывать, что в этом случае вместо дешёвой операции переименовывания в пределах одной файловой системы файл копируется с одной файловой системы на другую. Поэтому лучше, если сохраняемые файлы будут находиться на той же файловой системе, что и каталог с временными файлами, задаваемый директивой [client_body_temp_path](ngx_http_core_module.xml#client_body_temp_path) для данного location.

При создании файла с помощью метода PUT можно задать дату модификации, передав её в поле заголовка `Date` .

## min_delete_depth

```
Syntax:  число
Default: 0
Context: location, http, server
```

Разрешает методу DELETE удалять файлы при условии, что число элементов в пути запроса не меньше заданного. Например, директива

```
min_delete_depth 4;
```

разрешает удалять файлы по запросам

```
/users/00/00/name
/users/00/00/name/pic.jpg
/users/00/00/page.html
```

и запрещает удаление

```
/users/00/00
```

