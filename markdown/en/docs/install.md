# Installing nginx

**Revision:** 3  
**Language:** en


nginx can be installed differently, depending on the operating system.

## Installation on Linux {#linux}

For Linux, nginx [packages](../linux_packages.html)
from nginx.org can be used.

## Installation on FreeBSD {#freebsd}

On FreeBSD, nginx can be installed either from the [packages](https://docs.freebsd.org/en/books/handbook/ports/#pkgng-intro)
or through the
[ports](https://docs.freebsd.org/en/books/handbook/ports/#ports-using)
system.
The ports system provides greater flexibility, allowing selection among
a wide range of options.
The port will compile nginx with the specified options and install it.

## Building from Sources {#source_install}

If some special functionality is required, not available with packages and
ports, nginx can also be compiled from source files.
While more flexible, this approach may be complex for a beginner.
For more information, see [configure.html](configure.html).
