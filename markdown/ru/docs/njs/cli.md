# Интерфейс командной строки

**Revision:** 4  
**Language:** ru

Создание и отладка njs-скриптов может осуществляться в командной строке. Утилита командной строки доступна после установки [пакета](install.xml#install_package) Linux или после сборки из [исходных файлов](install.xml#install_sources) . В отличие от njs, запущенном внутри nginx, в утилите недоступны объекты nginx ( [HTTP](reference.xml#http) и [Stream](reference.xml#stream) ).

```
$ echo "2**3" | njs -q
8

$ njs
>> globalThis
global {
 njs: njs {
  version: '0.3.9'
 },
 global: [Circular],
 process: process {
  argv: [
   '/usr/bin/njs'
  ],
  env: {
   PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
   HOSTNAME: 'f777c149d4f8',
   TERM: 'xterm',
   NGINX_VERSION: '1.17.9',
   NJS_VERSION: '0.3.9',
   PKG_RELEASE: '1~buster',
   HOME: '/root'
  }
 },
 console: {
  log: [Function: native],
  dump: [Function: native],
  time: [Function: native],
  timeEnd: [Function: native]
 },
 print: [Function: native]
}
>>
```

