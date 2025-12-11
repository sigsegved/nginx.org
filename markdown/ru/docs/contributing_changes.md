# Внесение изменений

**Revision:** 5  
**Language:** ru


## Получение исходного кода {#getting_sources}

Для хранения исходного кода используется
[GitHub](https://github.com).
[Репозиторий](https://github.com/nginx/nginx) можно клонировать
следующей командой:

```
git clone https://github.com/nginx/nginx.git
```

## Оформление изменений {#formatting_changes}

Изменения должны быть оформлены согласно
[стилю](../docs/dev/development_guide.xml#code_style),
принятому в nginx.
В случае возникновения затруднений в оформлении
изучите, как оформлен исходный код nginx, и следуйте этому стилю в своём коде.
Изменения скорее будут приняты, если их стиль соответствует окружающему
коду.

[Зафиксируйте](https://docs.github.com/ru/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/about-commits)
изменения в вашем ответвлении (fork) проекта.
Пожалуйста, убедитесь, что адрес
[электронной
почты](https://docs.github.com/ru/get-started/getting-started-with-git/setting-your-username-in-git) и настоящее имя автора изменения указаны правильно.

Сообщение фиксации должно содержать однострочное резюме и подробное описание
после пустой строки.
Желательно, чтобы первая строка была не длиннее 67 символов,
остальные строки не длиннее 76 символов.
Итоговый набор изменений может быть получен с помощью
команды `git show`:

```
commit 8597218f386351d6c6cdced24af6716e19a18fc3
Author: Filipe Da Silva <username@example.com>
Date:   Thu May 9 10:54:28 2013 +0200

    Mail: removed surplus ngx_close_connection() call.

    It is already called for a peer connection a few lines above.

diff --git a/src/mail/ngx_mail_auth_http_module.c b/src/mail/ngx_mail_auth_http_module.c
index 2e9b9f24d..8094bbc5c 100644
--- a/src/mail/ngx_mail_auth_http_module.c
+++ b/src/mail/ngx_mail_auth_http_module.c
@@ -699,7 +699,6 @@ ngx_mail_auth_http_process_headers(ngx_mail_session_t *s,

                     p = ngx_pnalloc(s->connection->pool, ctx->err.len);
                     if (p == NULL) {
-                        ngx_close_connection(ctx->peer.connection);
                         ngx_destroy_pool(ctx->pool);
                         ngx_mail_session_internal_server_error(s);
                         return;
```

## Перед отправкой {#before_submitting}

Несколько моментов, на которые следует обратить внимание перед
отправкой изменения:

- Предлагаемые изменения должны корректно работать на всех
[поддерживаемых
платформах](../index.xml#tested_os_and_platforms).
- Постарайтесь разъяснить, почему предлагаемое изменение нужно, и, если возможно,
опишите вариант использования.
- Проверка изменений при помощи специального набора тестов позволит убедиться,
что они не вызывают регрессию.
[Репозиторий](https://github.com/nginx/nginx-tests) с тестами
можно клонировать следующей командой:

```
git clone https://github.com/nginx/nginx-tests.git
```

## Отправка изменений {#submitting_changes}

Предлагаемые изменения следует отправлять из вашего ответвления проекта в
исходный [репозиторий](https://github.com/nginx/nginx) как
[pull request](https://docs.github.com/ru/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

## Веб-сайт {#website}

Для хранения исходных файлов этого веб-сайта также используется GitHub.
[Репозиторий](https://www.github.com/nginx/nginx.org)
можно клонировать следующей командой:

```
https://github.com/nginx/nginx.org.git
```

Предлагаемые изменения следует отправлять из вашего ответвления проекта
как pull request.

## Лицензия {#license}

Отправка изменений подразумевает предоставление проекту права на их
использование под соответствующей [лицензией](../../LICENSE).
