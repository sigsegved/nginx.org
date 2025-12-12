# Модуль ngx_mail_proxy_module

**Revision:** 6  
**Language:** ru

# Директивы {#directives}

## proxy_buffer

```
Syntax:  размер
Default: 4k|8k
Context: server, mail
```

Задаёт размер буфера, используемого при проксировании. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

## proxy_pass_error_message

```
Syntax:  on | off
Default: off
Context: server, mail
```

Определяет, передавать ли клиенту сообщение об ошибке, полученное при аутентификации на бэкенде.

Обычно, если аутентификация в nginx прошла успешно, бэкенд не может вернуть ошибку. Если же он всё-таки возвращает ошибку, это значит, что произошла ошибка внутри системы. В таких случаях сообщение бэкенда может содержать информацию, которую нельзя показывать клиенту. Однако для некоторых POP3-серверов ошибка в ответ на правильный пароль является штатным поведением. Например, CommuniGatePro извещает пользователя о [переполнении ящика](http://www.stalker.com/CommuniGatePro/Alerts.html#Quota) или других событиях, периодически выдавая [ошибку аутентификации](http://www.stalker.com/CommuniGatePro/POP.html#Alerts) . В этом случае директиву стоит включить.

## proxy_protocol

```
Syntax:  on | off
Default: off
Context: server, mail
```

*This directive appeared in version 1.19.8.*

Включает [протокол PROXY](http://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) для соединений с бэкендом.

## proxy_smtp_auth

```
Syntax:  on | off
Default: off
Context: server, mail
```

*This directive appeared in version 1.19.4.*

Разрешает или запрещает аутентификацию пользователей на SMTP-бэкенде при помощи команды `AUTH` .

Если также включён [XCLIENT](#xclient) , то команда `XCLIENT` не будет отправлять параметр `LOGIN` .

## proxy_timeout

```
Syntax:  время
Default: 24h
Context: server, mail
```

Задаёт `таймаут` между двумя идущими подряд операциями чтения или записи на клиентском соединении или соединении с проксируемым сервером. Если по истечении этого времени данные не передавались, соединение закрывается.

## xclient

```
Syntax:  on | off
Default: on
Context: server, mail
```

Разрешает или запрещает передачу команды [XCLIENT](http://www.postfix.org/XCLIENT_README.html) с параметрами клиента при подключении к SMTP-бэкенду.

При помощи `XCLIENT` MTA может писать в лог информацию о клиенте и применять различные ограничения на основе этих данных.

Если команда `XCLIENT` разрешена, то при подключении к бэкенду nginx посылает ему следующие команды:

- `EHLO` с [именем сервера](ngx_mail_core_module.xml#server_name)
- `XCLIENT`
- `EHLO` или `HELO` ,
как её передал клиент

Если [найденное](ngx_mail_core_module.xml#resolver) по IP-адресу клиента имя указывает на тот же адрес, оно передаётся в параметре `NAME` команды `XCLIENT` . Если имя не может быть найдено, указывает на другой адрес, или не задан [resolver](ngx_mail_core_module.xml#resolver) , то в параметре `NAME` передаётся `[UNAVAILABLE]` . Если же в процессе поиска имени или адреса произошла ошибка, передаётся `[TEMPUNAVAIL]` .

Если команда `XCLIENT` запрещена, то при подключении к бэкенду nginx передаёт команду `EHLO` с [именем сервера](ngx_mail_core_module.xml#server_name) , если клиент передал `EHLO` , иначе `HELO` с именем сервера.

