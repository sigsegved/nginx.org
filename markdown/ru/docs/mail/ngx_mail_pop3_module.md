# Модуль ngx_mail_pop3_module

**Revision:** 5  
**Language:** ru

# Директивы {#directives}

## pop3_auth

```
Syntax:  pop3_auth метод ...;
Default: plain
Context: server, mail
```

Задаёт разрешённые методы аутентификации POP3-клиентов. Поддерживаемые методы:

**`plain`**  
  [USER/PASS](https://datatracker.ietf.org/doc/html/rfc1939) , [AUTH PLAIN](https://datatracker.ietf.org/doc/html/rfc4616) , [AUTH LOGIN](https://datatracker.ietf.org/doc/html/draft-murchison-sasl-login-00)

**`apop`**  
  [APOP](https://datatracker.ietf.org/doc/html/rfc1939) .
Для работы этого метода пароль должен храниться в незашифрованном виде.

**`cram-md5`**  
  [AUTH CRAM-MD5](https://datatracker.ietf.org/doc/html/rfc2195) .
Для работы этого метода пароль должен храниться в незашифрованном виде.

**`external`**  
  [AUTH EXTERNAL](https://datatracker.ietf.org/doc/html/rfc4422) (1.11.6).

Методы аутентификации с передачей пароля открытым текстом ( `USER/PASS` , `AUTH PLAIN` и `AUTH LOGIN` ) включены всегда, однако если метод `plain` не указан, то `AUTH PLAIN` и `AUTH LOGIN` не будут автоматически добавляться в [pop3_capabilities](#pop3_capabilities) .

## pop3_capabilities

```
Syntax:  pop3_capabilities расширение ...;
Default: TOP USER UIDL
Context: server, mail
```

Позволяет указать список расширений [протокола POP3](https://datatracker.ietf.org/doc/html/rfc2449) , выдаваемый клиенту по команде `CAPA` . В зависимости от значения директивы [starttls](ngx_mail_ssl_module.xml#starttls) к этому списку автоматически добавляются методы аутентификации, указанные в директиве [pop3_auth](#pop3_auth) (расширение [SASL](https://datatracker.ietf.org/doc/html/rfc2449) ), и [STLS](https://datatracker.ietf.org/doc/html/rfc2595) .

В данной директиве имеет смысл указать расширения, поддерживаемые POP3-бэкендами, на которые проксируются клиенты (если эти расширения относятся к командам, используемым после аутентификации, когда nginx прозрачно проксирует подключение клиента на бэкенд).

Текущий список стандартизованных расширений опубликован на [www.iana.org](http://www.iana.org/assignments/pop3-extension-mechanism) .

