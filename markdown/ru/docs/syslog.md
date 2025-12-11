# Запись в syslog

**Revision:** 6  
**Language:** ru


Директивы
[](ngx_core_module.xml#error_log)
и
[](http/ngx_http_log_module.xml#access_log)
поддерживают запись в syslog.
Запись в syslog настраивается при помощи следующих параметров:

**`server=`*адрес***  
  Задаёт адрес сервера syslog.
Адрес может быть указан в виде доменного имени или IP-адреса,
и необязательного порта, или в виде пути UNIX-сокета, который
указывается после префикса “`unix:`”.
Если порт не указан, используется UDP-порт 514.
Если доменному имени соответствует несколько IP-адресов,
используется только первый адрес.
**`facility=`*строка***  
  Задаёт категорию сообщений syslog в соответствии с
[RFC 3164](https://datatracker.ietf.org/doc/html/rfc3164#section-4.1.1).
В качестве категории может быть указано одно из следующих значений:
“`kern`”, “`user`”,
“`mail`”, “`daemon`”,
“`auth`”, “`intern`”,
“`lpr`”, “`news`”, “`uucp`”,
“`clock`”, “`authpriv`”,
“`ftp`”, “`ntp`”, “`audit`”,
“`alert`”, “`cron`”,
“`local0`”..“`local7`”.
По умолчанию используется “`local7`”.
**`severity=`*строка***  
  Задаёт важность сообщений syslog для
[](http/ngx_http_log_module.xml#access_log)
в соответствии с
[RFC 3164](https://datatracker.ietf.org/doc/html/rfc3164#section-4.1.1).
Возможны те же самые значения, что и у второго параметра (уровень)
директивы [](ngx_core_module.xml#error_log).
По умолчанию используется “`info`”.

> **Note:** Важность сообщений об ошибках определяется самим nginx, поэтому
в директиве `error_log` параметр игнорируется.
**`tag=`*строка***  
  Задаёт метку сообщений syslog.
По умолчанию используется “`nginx`”.
**`nohostname`**  
  Запрещает добавление поля “hostname” в заголовок сообщения syslog (1.9.7).

Пример конфигурации syslog:

```
error_log syslog:server=192.168.1.1 debug;

access_log syslog:server=unix:/var/log/nginx.sock,nohostname;
access_log syslog:server=[2001:db8::1]:12345,facility=local7,tag=nginx,severity=info combined;
```

> **Note:** Запись в syslog доступна начиная с версии 1.7.1.
Как часть
коммерческой подписки
запись в syslog доступна начиная с версии 1.5.3.
