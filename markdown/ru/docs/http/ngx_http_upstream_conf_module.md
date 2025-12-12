# Модуль ngx_http_upstream_conf_module

**Revision:** 6  
**Language:** ru

Модуль `ngx_http_upstream_conf_module` позволяет оперативно настраивать группы серверов при помощи простого HTTP-интерфейса без необходимости перезапуска nginx. Группа серверов [http](ngx_http_upstream_module.xml#zone) или [stream](../stream/ngx_stream_upstream_module.xml#zone) должна находиться в разделяемой памяти.

> **Note:** Этот модуль был доступен как часть [коммерческой подписки](https://nginx.com/products/) до версии 1.13.10.
Модуль был заменён модулем [ngx_http_api_module](ngx_http_api_module.xml) в версии 1.13.3.

# Пример конфигурации {#example}

```
upstream backend {
    zone upstream_backend 64k;

    ...
}

server {
    location /upstream_conf {
        upstream_conf;
        allow 127.0.0.1;
        deny all;
    }
}
```

# Директивы {#directives}

## upstream_conf

```
Syntax:  
Default: 
Context: location
```

Активирует HTTP-интерфейс для настройки групп серверов в содержащем location. Доступ в location следует [ограничить](ngx_http_core_module.xml#satisfy) .

С помощью команд настройки можно:

- просматривать конфигурацию группы;
- просматривать или изменять конфигурацию, а также
удалять серверы;
- добавлять новые серверы.

> **Note:** Поскольку адреса в группе не обязаны быть уникальными,
обращение к отдельным серверам в группе осуществляется по их идентификаторам.
Идентификаторы назначаются автоматически и показываются при добавлении сервера
или просмотре конфигурации группы.

Команда настройки состоит из параметров, передаваемых в аргументах запроса, например:

```
http://127.0.0.1/upstream_conf?upstream=backend
```

Поддерживаются следующие параметры:

**`stream=`**  
  Выбирает группу серверов [stream](../stream/ngx_stream_upstream_module.xml) .
Если параметр не задан, будет выбрана группа серверов [http](ngx_http_upstream_module.xml) .

**`upstream=` `имя`**  
  Выбирает группу серверов для работы.
Параметр является обязательным.

**`id=` `число`**  
  Выбирает сервер для просмотра, изменения или удаления.

**`remove=`**  
  Удаляет сервер из группы.

**`add=`**  
  Добавляет новый сервер в группу.

**`backup=`**  
  Необходим для добавления запасного сервера.

> **Note:** До версии 1.7.2 параметр `backup=` требовался
также для просмотра, изменения или удаления существующих запасных серверов.

**`server=` `адрес`**  
  То же, что и параметр “ `адрес` ” сервера группы [http](ngx_http_upstream_module.xml#server) или [stream](../stream/ngx_stream_upstream_module.xml#server) .

При добавлении сервер можно задать в виде доменного имени. В этом случае любые изменения IP-адресов, соответствующих доменному имени сервера, отслеживаются и автоматически применяются к конфигурации группы без необходимости перезапуска nginx (1.7.2). Для этого в блоке [http](ngx_http_core_module.xml#resolver) или [stream](../stream/ngx_stream_core_module.xml#resolver) должна быть задана директива “ `resolver` ”. См. также параметр “ `resolve` ” сервера группы [http](ngx_http_upstream_module.xml#resolve) или [stream](../stream/ngx_stream_upstream_module.xml#resolve) .

**`service=` `имя`**  
  То же, что и параметр “ `service` ” сервера группы [http](ngx_http_upstream_module.xml#service) или [stream](../stream/ngx_stream_upstream_module.xml#service) (1.9.13).

**`weight=` `число`**  
  То же, что и параметр “ `weight` ” сервера группы [http](ngx_http_upstream_module.xml#weight) или [stream](../stream/ngx_stream_upstream_module.xml#weight) .

**`max_conns=` `число`**  
  То же, что и параметр “ `max_conns` ” сервера группы [http](ngx_http_upstream_module.xml#max_conns) или [stream](../stream/ngx_stream_upstream_module.xml#max_conns) .

**`max_fails=` `число`**  
  То же, что и параметр “ `max_fails` ” сервера группы [http](ngx_http_upstream_module.xml#max_fails) или [stream](../stream/ngx_stream_upstream_module.xml#max_fails) .

**`fail_timeout=` `время`**  
  То же, что и параметр “ `fail_timeout` ” сервера группы [http](ngx_http_upstream_module.xml#fail_timeout) или [stream](../stream/ngx_stream_upstream_module.xml#fail_timeout) .

**`slow_start=` `время`**  
  То же, что и параметр “ `slow_start` ” сервера группы [http](ngx_http_upstream_module.xml#slow_start) или [stream](../stream/ngx_stream_upstream_module.xml#slow_start) .

**`down=`**  
  То же, что и параметр “ `down` ” сервера группы [http](ngx_http_upstream_module.xml#down) или [stream](../stream/ngx_stream_upstream_module.xml#down) .

**`drain=`**  
  Переводит сервер группы серверов [http](ngx_http_upstream_module.xml) в режим “draining” (1.7.5).
В этом режиме на сервер будут проксироваться только [привязанные](ngx_http_upstream_module.xml#sticky) к нему запросы.

**`up=`**  
  Параметр, обратный по значению параметру “ `down` ” сервера группы [http](ngx_http_upstream_module.xml#down) или [stream](../stream/ngx_stream_upstream_module.xml#down) .

**`route=` `строка`**  
  То же, что и параметр “ `route` ” сервера группы [http](ngx_http_upstream_module.xml#route) .

Первые три параметра выбирают объект. Объектом может быть либо группа серверов http или stream, либо отдельный сервер. Если остальные параметры не указаны, то показывается конфигурация выбранной группы или сервера.

Например, команда для просмотра конфигурации всей группы выглядит следующим образом:

```
http://127.0.0.1/upstream_conf?upstream=backend
```

Для просмотра конфигурации отдельного сервера следует указать его идентификатор:

```
http://127.0.0.1/upstream_conf?upstream=backend&id=42
```

Для добавления нового сервера в группу следует указать его адрес в параметре “ `server=` ”. Если остальные параметры не указаны, то при добавлении сервера их значения будут установлены по умолчанию (см. директиву “ `server` ” для [http](ngx_http_upstream_module.xml#server) или [stream](../stream/ngx_stream_upstream_module.xml#server) ).

Например, команда для добавления нового основного сервера в группу выглядит следующим образом:

```
http://127.0.0.1/upstream_conf?add=&upstream=backend&server=127.0.0.1:8080
```

Добавление нового запасного сервера происходит следующим образом:

```
http://127.0.0.1/upstream_conf?add=&upstream=backend&backup=&server=127.0.0.1:8080
```

Добавление нового основного сервера с нестандартными значениями параметров и с пометкой его как постоянно недоступного (“ `down` ”) происходит следующим образом:

```
http://127.0.0.1/upstream_conf?add=&upstream=backend&server=127.0.0.1:8080&weight=2&down=
```

Для удаления сервера следует указать его идентификатор:

```
http://127.0.0.1/upstream_conf?remove=&upstream=backend&id=42
```

Пометка существующего сервера как постоянно недоступного (“ `down` ”) происходит следующим образом:

```
http://127.0.0.1/upstream_conf?upstream=backend&id=42&down=
```

Изменение адреса существующего сервера происходит следующим образом:

```
http://127.0.0.1/upstream_conf?upstream=backend&id=42&server=192.0.2.3:8123
```

Изменение других параметров существующего сервера происходит следующим образом:

```
http://127.0.0.1/upstream_conf?upstream=backend&id=42&max_fails=3&weight=4
```

Вышеприведённые примеры актуальны для группы серверов [http](ngx_http_upstream_module.xml) . Аналогичные примеры для группы серверов [stream](../stream/ngx_stream_upstream_module.xml) требуют указания параметра “ `stream=` ”.

