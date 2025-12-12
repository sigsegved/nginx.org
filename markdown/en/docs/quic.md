# Support for QUIC and HTTP/3

**Revision:** 3  
**Language:** en

Support for [QUIC](https://datatracker.ietf.org/doc/html/rfc9000) and [HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114) protocols is available since 1.25.0, it is included in Linux [binary packages](../linux_packages.xml) . Please refer to the [ngx_http_v3_module](http/ngx_http_v3_module.xml) documentation.

# Building from sources {#building}

The build is configured using the `configure` command. Please refer to for details.

The [OpenSSL](https://openssl.org) library version 3.5.1 or higher is recommended to build nginx with QUIC support. Otherwise, the [OpenSSL](https://openssl.org) compatibility layer will be used that does not support [early data](http/ngx_http_ssl_module.xml#ssl_early_data) . Alternatively, [BoringSSL](https://boringssl.googlesource.com/boringssl) , [LibreSSL](https://www.libressl.org) , or [QuicTLS](https://github.com/quictls/openssl) prebuilt libraries can be used.

Use the following command to configure nginx with [BoringSSL](https://boringssl.googlesource.com/boringssl) :

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../boringssl/include"
    --with-ld-opt="-L../boringssl/build -lstdc++"
```

Alternatively, nginx can be configured with [QuicTLS](https://github.com/quictls/openssl) :

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../quictls/build/include"
    --with-ld-opt="-L../quictls/build/lib"
```

Alternatively, nginx can be configured with [LibreSSL](https://www.libressl.org) :

```
./configure
    --with-debug
    --with-http_v3_module
    --with-cc-opt="-I../libressl/build/include"
    --with-ld-opt="-L../libressl/build/lib"
```

After configuration, nginx is compiled and installed using `make` .

# Configuration tips {#configuration}

The [listen](http/ngx_http_core_module.xml#listen) directive in [ngx_http_core_module](http/ngx_http_core_module.xml) module got a new parameter [quic](http/ngx_http_core_module.xml#quic) which enables HTTP/3 over QUIC on the specified port.

Along with the `quic` parameter it is also possible to specify the [reuseport](http/ngx_http_core_module.xml#reuseport) parameter to make it work properly with multiple workers.

To [enable](http/ngx_http_v3_module.xml#quic_retry) address validation:

```
quic_retry on;
```

To [enable](http/ngx_http_ssl_module.xml#ssl_early_data) 0-RTT:

```
ssl_early_data on;
```

To [enable](http/ngx_http_v3_module.xml#quic_gso) GSO (Generic Segmentation Offloading):

```
quic_gso on;
```

To [set](http/ngx_http_v3_module.xml#quic_host_key) host key for various tokens:

```
quic_host_key <filename>;
```

QUIC requires TLSv1.3 protocol version which is enabled by default in the [ssl_protocols](http/ngx_http_ssl_module.xml#ssl_protocols) directive.

By default, [GSO Linux-specific optimization](http://vger.kernel.org/lpc_net2018_talks/willemdebruijn-lpc2018-udpgso-paper-DRAFT-1.pdf) is disabled. Enable it in case a corresponding network interface is configured to support GSO.

# Troubleshooting {#troubleshooting }

Tips that may help to identify problems:

- Ensure nginx is built with the proper SSL library.
- Ensure nginx is using the proper SSL library in runtime
(the `nginx -V` shows what it is currently used).
- Ensure a client is actually sending requests over QUIC.
It is recommended to start with a simple console client such as [ngtcp2](https://nghttp2.org/ngtcp2) to ensure the server is configured properly before trying
with real browsers that may be quite picky with certificates.
- Build nginx with [debug support](debugging_log.xml) and check the debug log.
It should contain all details about the connection and why it failed.
All related messages contain the “ `quic` ” prefix
and can be easily filtered out.
- For a deeper investigation, additional debugging can be enabled
using the following macros: `NGX_QUIC_DEBUG_PACKETS` , `NGX_QUIC_DEBUG_FRAMES` , `NGX_QUIC_DEBUG_ALLOC` , `NGX_QUIC_DEBUG_CRYPTO` .
  ```
./configure
    --with-http_v3_module
    --with-debug
    --with-cc-opt="-DNGX_QUIC_DEBUG_PACKETS -DNGX_QUIC_DEBUG_CRYPTO"
```

