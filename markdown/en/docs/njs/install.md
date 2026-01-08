# Download and install

**Revision:** 5  
**Language:** en

# Installing as a Linux package {#install_package}

For Linux, njs modules [packages](../../linux_packages.xml#dynmodules) can be used:

- `nginx-module-njs` — njs [dynamic](../ngx_core_module.xml#load_module) modules
- `nginx-module-njs-dbg` — debug symbols for the `nginx-module-njs` package

After package installation, njs dynamic modules need to be loaded with the [`load_module`](../ngx_core_module.xml#load_module) directive:

```
load_module modules/ngx_http_js_module.so;
```

or

```
load_module modules/ngx_stream_js_module.so;
```

# Building from the sources {#install_sources}

The [repository](https://github.com/nginx/njs) with njs sources can be cloned with the following command (requires [Git](https://git-scm.com/) client):

```
git clone https://github.com/nginx/njs
```

Then the modules should be compiled from [nginx](../configure.xml) root directory using the `--add-module` configuration parameter:

```
./configure --add-module=path-to-njs/nginx
```

The modules can also be built as [dynamic](../ngx_core_module.xml#load_module) :

```
./configure --add-dynamic-module=path-to-njs/nginx
```

## Adding QuickJS engine support {#install_quickjs}

Make sure you have built the QuickJS library:

```
git clone https://github.com/bellard/quickjs
cd quickjs
CFLAGS='-fPIC' make libquickjs.a
```

At the module compilation step, also specify the include ( `-I` ) and library ( `-L` ) paths with the `--with-cc-opt=` and `--with-ld-opt=` configuration parameters:

```
./configure --add-module=path-to-njs/nginx \
    --with-cc-opt="-I path-to-quickjs" \
    --with-ld-opt="-L path-to-quickjs"
```

# Building njs command-line utility {#cli}

To build only the njs command-line [utility](cli.xml) , run `./configure` and `make njs` commands from njs root directory. After building, the utility is available as `./build/njs` .

