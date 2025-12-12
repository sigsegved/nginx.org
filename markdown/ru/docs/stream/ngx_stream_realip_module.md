# Модуль ngx_stream_realip_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_stream_realip_module` позволяет менять адрес и порт клиента на переданные в заголовке протокола PROXY (1.11.4). Протокол PROXY должен быть предварительно включён при помощи установки параметра [proxy_protocol](ngx_stream_core_module.xml#proxy_protocol) в директиве `listen` .

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-stream_realip_module` .

# Пример конфигурации {#example}

```
listen 12345 proxy_protocol;

set_real_ip_from  192.168.1.0/24;
set_real_ip_from  192.168.2.1;
set_real_ip_from  2001:0db8::/32;
```

# Директивы {#directives}

## set_real_ip_from

```
Syntax:  адрес | CIDR | unix:
Default: 
Context: server, stream
```

Задаёт доверенные адреса, которые передают верный адрес для замены. Если указано специальное значение `unix:` , доверенными будут считаться все UNIX-сокеты.

# Встроенные переменные {#variables}

**`$realip_remote_addr`**  
  хранит исходный адрес клиента

**`$realip_remote_port`**  
  хранит исходный порт клиента

