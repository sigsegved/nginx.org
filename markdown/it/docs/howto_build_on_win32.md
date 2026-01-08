# Compilare i sorgenti di nginx su piattaforma Win32 con Visual C

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it

# Prerequisiti

Per compilare nginx su piattaforma Microsoft Win32® , servono:

- Il compilatore Microsoft Visual C; e' stato verificato che con
  Microsoft Visual Studio- 8 e 10 è possibile portare
a termine la compilazione.
- [MSYS](http://www.mingw.org/wiki/MSYS) .
- Perl, se si vuole compilare
  OpenSSL- e nginx con il support SSL;
ad esempio [ActivePerl](http://www.activestate.com/activeperl) o [Strawberry Perl](http://strawberryperl.com) .
- Il client [Mercurial](http://mercurial.selenic.com/) .
- Il codice sorgente delle librerie [PCRE](http://www.pcre.org) , [zlib](http://zlib.net) e [OpenSSL](http://www.openssl.org) .

# Sequenza di compilazione {#build_steps}

Prima di iniziare a compilare, assicurarsi che i path alle directory bin di Perl, Mercurial e MSYS siano stati aggiunti alla variabile d'ambiente PATH. Per configurare l'ambiente di Visual C, avviare lo script vcvarsall.bat dalla directory del Visual C.

Per compilare nginx:

- Avviare la bash MSYS.
- Fare il check out dei sorgenti nginx dall'archivio hg.nginx.org; ad esempio con:
  ```
hg clone http://hg.nginx.org/nginx
```

- Creare la directory per la compilazione e la sottodirectory lib, scompattare il
codice sorgente delle librerie zlib, PCRE e OpenSSL in lib:
  ```
mkdir objs
mkdir objs/lib
cd objs/lib
tar -xzf ../../pcre-8.32.tar.gz
tar -xzf ../../zlib-1.2.7.tar.gz
tar -xzf ../../openssl-1.0.1e.tar.gz
```

- Lanciare lo script configure:
  ```
auto/configure --with-cc=cl --builddir=objs --prefix= \
--conf-path=conf/nginx.conf --pid-path=logs/nginx.pid \
--http-log-path=logs/access.log --error-log-path=logs/error.log \
--sbin-path=nginx.exe --http-client-body-temp-path=temp/client_body_temp \
--http-proxy-temp-path=temp/proxy_temp \
--http-fastcgi-temp-path=temp/fastcgi_temp \
--with-cc-opt=-DFD_SETSIZE=1024 --with-pcre=objs/lib/pcre-8.32 \
--with-zlib=objs/lib/zlib-1.2.7 --with-openssl=objs/lib/openssl-1.0.1e \
--with-select_module --with-http_ssl_module --with-ipv6
```

- lanciare make:
  ```
nmake -f objs/Makefile
```

# Vedi anche {#see_also}

- 

