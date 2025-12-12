# Загрузка и установка

**Revision:** 5  
**Language:** ru

# Установка пакета Linux {#install_package}

Для установки модулей njs на Linux могут быть использованы [пакеты](../../linux_packages.xml#dynmodules) :

- `nginx-module-njs` — [динамические](../ngx_core_module.xml#load_module) модули
njs
- `nginx-module-njs-dbg` — debug-символы для
пакета `nginx-module-njs`

После установки пакетов необходимо загрузить динамические модули njs при помощи директивы [`load_module`](../ngx_core_module.xml#load_module) :

```
load_module modules/ngx_http_js_module.so;
```

или

```
load_module modules/ngx_stream_js_module.so;
```

# Установка из исходных файлов {#install_sources}

[Репозиторий](https://github.com/nginx/njs) с исходным кодом njs можно клонировать следующей командой (необходим клиент [Git](https://git-scm.com/) ):

```
git clone https://github.com/nginx/njs
```

Затем модули необходимо собрать из корневого каталога [nginx](../configure.xml) с помощью конфигурационного параметра `--add-module` :

```
./configure --add-module=path-to-njs/nginx
```

Модули также можно собрать как [динамические](../ngx_core_module.xml#load_module) :

```
./configure --add-dynamic-module=path-to-njs/nginx
```

## Добавление поддержки QuickJS {#install_quickjs}

Убедитесь, что присутствует библиотека QuickJS:

```
git clone https://github.com/bellard/quickjs
cd quickjs
CFLAGS='-fPIC' make libquickjs.a
```

На этапе компиляции модулей также укажите пути include ( `-I` ) и library ( `-L` ) с помощью конфигурационных параметров `--with-cc-opt=` и `--with-ld-opt=` :

```
./configure --add-module=path-to-njs/nginx \
    --with-cc-opt="-I path-to-quickjs" \
    --with-ld-opt="-L path-to-quickjs"
```

# Сборка утилиты командной строки njs {#cli}

Чтобы собрать только [утилиту](cli.xml) командной строки njs, необходимо запустить команды `./configure` и `make njs` из корневого каталога njs. После сборки утилита доступна как `./build/njs` .

