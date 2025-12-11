# Модуль ngx_mail_realip_module

**Revision:** 1  
**Language:** ru


Модуль `ngx_mail_realip_module` позволяет
менять адрес и порт клиента
на переданные в заголовке протокола PROXY (1.19.8).
Протокол PROXY должен быть предварительно включён при помощи установки
параметра [](ngx_mail_core_module.xml#proxy_protocol)
в директиве `listen`.

## Пример конфигурации {#example}

```
listen 110 proxy_protocol;

set_real_ip_from  192.168.1.0/24;
set_real_ip_from  192.168.2.1;
set_real_ip_from  2001:0db8::/32;
```

## Директивы {#directives}



    адрес |
    CIDR |
    unix:

mail
server


Задаёт доверенные адреса, которые передают верный адрес
для замены.
Если указано специальное значение unix:,
доверенными будут считаться все UNIX-сокеты.


