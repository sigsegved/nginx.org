# Отладочный лог

**Revision:** 6  
**Language:** ru


Для работы отладочного лога nginx должен быть сконфигурирован с поддержкой
отладки на этапе сборки:


```
./configure --with-debug ...
```


Затем нужно задать уровень `debug` с помощью
директивы [](ngx_core_module.xml#error_log):


```
error_log /path/to/log debug;
```


Чтобы убедиться, что поддержка отладки сконфигурирована,
необходимо выполнить команду `nginx -V`:


```
configure arguments: --with-debug ...
```


Готовые пакеты для [Linux](../linux_packages.html)
по умолчанию предоставляют поддержку отладочного лога
при помощи бинарного файла `nginx-debug` (1.9.8),
который можно запустить при помощи команд


```
service nginx stop
service nginx-debug start
```


и затем задать уровень `debug`.
Бинарная версия nginx для Windows всегда собирается с поддержкой отладочного
лога, поэтому понадобится лишь задать уровень `debug`.

Обратите внимание, что переопределение лога без одновременного указания
уровня `debug` отключит отладочный лог.
В примере ниже, переопределение лога на уровне
[](http/ngx_http_core_module.xml#server)
отключает отладочный лог для этого сервера:

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log;
        ...
```

Чтобы избежать этого, следует либо закомментировать строку, переопределяющую
лог, либо добавить определение уровня `debug`:

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log debug;
        ...
```

## Отладочный лог для определённых клиентов {#clients}

Можно включить отладочный лог только для
[определённых
клиентских адресов](ngx_core_module.xml#debug_connection):


```
error_log /path/to/log;

events {
    debug_connection 192.168.1.1;
    debug_connection 192.168.10.0/24;
}
```

## Запись в кольцевой буфер в памяти {#memory}

Отладочный лог можно записывать в кольцевой буфер в памяти:

```
error_log memory:32m debug;
```

Запись в буфер в памяти на уровне `debug`
не оказывает существенного влияния на производительность
даже при высоких нагрузках.
В этом случае лог может быть извлечён при помощи
`gdb`-скрипта, подобного следующему:

```
set $log = ngx_cycle->log

while $log->writer != ngx_log_memory_writer
    set $log = $log->next
end

set $buf = (ngx_log_memory_buf_t *) $log->wdata
dump binary memory debug_log.txt $buf->start $buf->end
```

Или при помощи такого `lldb`-скрипта:

```
expr ngx_log_t *$log = ngx_cycle->log
expr while ($log->writer != ngx_log_memory_writer) { $log = $log->next; }
expr ngx_log_memory_buf_t *$buf = (ngx_log_memory_buf_t *) $log->wdata
memory read --force --outfile debug_log.txt --binary $buf->start $buf->end
```
