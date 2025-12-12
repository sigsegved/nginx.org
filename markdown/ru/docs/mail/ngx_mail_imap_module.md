# Модуль ngx_mail_imap_module

**Revision:** 7  
**Language:** ru

# Директивы {#directives}

## imap_auth

```
Syntax:  метод ...
Default: plain
Context: server, mail
```

Задаёт разрешённые методы аутентификации IMAP-клиентов. Поддерживаемые методы:

**`plain`**  
  [LOGIN](https://datatracker.ietf.org/doc/html/rfc3501) , [AUTH=PLAIN](https://datatracker.ietf.org/doc/html/rfc4616)

**`login`**  
  [AUTH=LOGIN](https://datatracker.ietf.org/doc/html/draft-murchison-sasl-login-00)

**`cram-md5`**  
  [AUTH=CRAM-MD5](https://datatracker.ietf.org/doc/html/rfc2195) .
Для работы этого метода пароль должен храниться в незашифрованном виде.

**`external`**  
  [AUTH=EXTERNAL](https://datatracker.ietf.org/doc/html/rfc4422) (1.11.6).

Методы аутентификации с передачей пароля открытым текстом (команда `LOGIN` , `AUTH=PLAIN` и `AUTH=LOGIN` ) включены всегда, однако если методы `plain` и `login` не указаны, то `AUTH=PLAIN` и `AUTH=LOGIN` не будут автоматически добавляться в [imap_capabilities](#imap_capabilities) .

## imap_capabilities

```
Syntax:  расширение ...
Default: IMAP4 IMAP4rev1 UIDPLUS
Context: server, mail
```

Позволяет указать список расширений [протокола IMAP](https://datatracker.ietf.org/doc/html/rfc3501) , выдаваемый клиенту по команде `CAPABILITY` . В зависимости от значения директивы [starttls](ngx_mail_ssl_module.xml#starttls) к этому списку автоматически добавляются методы аутентификации, указанные в директиве [imap_auth](#imap_auth) , и [STARTTLS](https://datatracker.ietf.org/doc/html/rfc2595) .

В данной директиве имеет смысл указать расширения, поддерживаемые IMAP-бэкендами, на которые проксируются клиенты (если эти расширения относятся к командам, используемым после аутентификации, когда nginx прозрачно проксирует подключение клиента на бэкенд).

Текущий список стандартизованных расширений опубликован на [www.iana.org](http://www.iana.org/assignments/imap4-capabilities) .

## imap_client_buffer

```
Syntax:  размер
Default: 4k|8k
Context: server, mail
```

Задаёт `размер` буфера для чтения IMAP-команд. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

