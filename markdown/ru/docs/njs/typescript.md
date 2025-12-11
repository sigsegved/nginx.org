# Создание кода njs при помощи файлов деклараций TypeScript

**Revision:** 1  
**Language:** en


[TypeScript](https://www.typescriptlang.org)—это
типизированное подмножество JavaScript,
которое компилируется в обычный JavaScript.

TypeScript поддерживает файлы деклараций, в которых содержится
типизированная информация существующих библиотек JavaScript.
С их помощью программы могут использовать значения в файлах также,
если бы эти значения были статически типизированными сущностями TypeScript.

В njs файлы деклараций TypeScript предоставляются для
[API](reference.html) и могут использоваться при:

- автозаполнении и проверки API в редакторе
- создании типобезопасного njs-кода.

## Компиляция файлов деклараций TypeScript {#get}

```
$ git clone https://github.com/nginx/njs
$ cd njs && ./configure && make ts
$ ls build/ts/
njs_core.d.ts
njs_shell.d.ts
ngx_http_js_module.d.ts
ngx_stream_js_module.d.ts
```

## Проверка API и автозаполнение {#autocomplete}

Файлы деклараций `*.d.ts` необходимо поместить в место,
доступное редактору:

`test.js`:

```
/// <reference path="ngx_http_js_module.d.ts" />
/**
 * @param {NginxHTTPRequest} r
 * */
function content_handler(r) {
    r.headersOut['content-type'] = 'text/plain';
    r.return(200, "Hello");
}
```

## Создание типобезопасного njs кода {#write}

`test.ts`:

```
/// <reference path="ngx_http_js_module.d.ts" />
function content_handler(r: NginxHTTPRequest) {
    r.headersOut['content-type'] = 'text/plain';
    r.return(200, "Hello from TypeScript");
}
```

Установка TypeScript:

```
# npm install -g typescript
```

Компиляция TypeScript:

```
$ tsc test.ts
$ cat test.js
```

Созданный файл `test.js` может использоваться напрямую в njs.
