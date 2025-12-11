# Модуль nginx JavaScript

**Revision:** 36  
**Language:** ru


njs - это модуль nginx, который расширяет возможности сервера nginx с помощью
сценариев JavaScript, позволяя создавать пользовательскую
логику на стороне сервера и выполнять другие задачи.

- [install.html](install.html)
- [Изменения в njs](changes.html) [en]
- [Справочник](reference.html) [en]
- [engine.html](engine.html)
- [Примеры использования](https://github.com/nginx/njs-examples/)
- [Безопасность](security.html) [en]
- [compatibility.html](compatibility.html)
- [cli.html](cli.html)
- [preload_objects.html](preload_objects.html)
- Протестированные ОС и платформы

- [
ngx_http_js_module](../http/ngx_http_js_module.html)
- [
ngx_stream_js_module](../stream/ngx_stream_js_module.html)

- [typescript.html](typescript.html)
- [node_modules.html](node_modules.html)

## Сценарии использования {#usecases}

- Комплексное управление доступом и проверка защиты при помощи njs
до получения запроса сервером группы
- Управление заголовками ответа
- Создание гибких асинхронных обработчиков содержимого и фильтров

Подробнее о сценариях использования
см. в [примерах](https://github.com/nginx/njs-examples/).

## Базовый пример HTTP {#example}

Чтобы использовать njs в nginx, необходимо:

- установить njs
- создать файл сценария njs, например http.js.
Описание свойств и методов языка njs
см. в справочнике.

function hello(r) {
    r.return(200, "Hello world!");
}

export default {hello};
- в файле nginx.conf включить
модуль ngx_http_js_module
и указать директиву
js_import
с файлом сценария http.js:

load_module modules/ngx_http_js_module.so;

events {}

http {
    js_import http.js;

    server {
        listen 8000;

        location / {
            js_content http.hello;
        }
    }
}

Также доступна отдельная утилита [командной строки](cli.html),
которая может использоваться независимо от nginx для разработки и отладки njs.

## Протестированные ОС и платформы {#tested_os_and_platforms}

- FreeBSD / amd64;
- Linux / x86, amd64, arm64, ppc64el;
- Solaris 11 / amd64;
- macOS / x86_64;

## Презентация на nginx.conf 2018 {#presentation}

