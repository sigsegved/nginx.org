# Модуль ngx_mail_smtp_module

**Revision:** 8  
**Language:** ru

# Директивы {#directives}

## smtp_auth

```
Syntax:  метод ...
Default: plain login
Context: server, mail
```

Задаёт разрешённые методы [SASL-аутентификации](https://datatracker.ietf.org/doc/html/rfc2554) SMTP-клиентов. Поддерживаемые методы:

**`plain`**  
  [AUTH PLAIN](https://datatracker.ietf.org/doc/html/rfc4616)

**`login`**  
  [AUTH LOGIN](https://datatracker.ietf.org/doc/html/draft-murchison-sasl-login-00)

**`cram-md5`**  
  [AUTH CRAM-MD5](https://datatracker.ietf.org/doc/html/rfc2195) .
Для работы этого метода пароль должен храниться в незашифрованном виде.

**`external`**  
  [AUTH EXTERNAL](https://datatracker.ietf.org/doc/html/rfc4422) (1.11.6).

**`none`**  
  Аутентификация не требуется.

Методы аутентификации с передачей пароля открытым текстом ( `AUTH PLAIN` и `AUTH LOGIN` ) включены всегда, однако если методы `plain` и `login` не указаны, то `AUTH PLAIN` и `AUTH LOGIN` не будут автоматически добавляться в [smtp_capabilities](#smtp_capabilities) .

## smtp_capabilities

```
Syntax:  расширение ...
Default: 
Context: server, mail
```

Позволяет указать список расширений протокола SMTP, выдаваемый клиенту в ответе на команду `EHLO` . В зависимости от значения директивы [starttls](ngx_mail_ssl_module.xml#starttls) к этому списку автоматически добавляются методы аутентификации, указанные в директиве [smtp_auth](#smtp_auth) , и [STARTTLS](https://datatracker.ietf.org/doc/html/rfc3207) .

В данной директиве имеет смысл указать расширения, поддерживаемые MTA, на который проксируются клиенты (если эти расширения относятся к командам, используемым после аутентификации, когда nginx прозрачно проксирует подключение клиента на бэкенд).

Текущий список стандартизованных расширений опубликован на [www.iana.org](http://www.iana.org/assignments/mail-parameters) .

## smtp_client_buffer

```
Syntax:  размер
Default: 4k|8k
Context: server, mail
```

Задаёт `размер` буфера для чтения SMTP-команд. По умолчанию размер одного буфера равен размеру страницы. В зависимости от платформы это или 4K, или 8K.

## smtp_greeting_delay

```
Syntax:  время
Default: 0
Context: server, mail
```

Позволяет задать задержку перед отправкой SMTP-приветствия, чтобы отклонить клиентов, не дожидающихся приветствия до начала отправки SMTP-команд.

