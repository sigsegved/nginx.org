# sys_errlist                 is deprecated;                 use strerror or strerror_r                 instead uyarısı

**Language:** tr


nginx versiyon 0.7.66, 0.8.35 ve üstü için Linux kurulumu yaparken, şu uyarıları alabilirsiniz:


```
warning: `sys_errlist' is deprecated;
    use `strerror' or `strerror_r' instead
warning: `sys_nerr' is deprecated;
    use `strerror' or `strerror_r' instead
```


Bu normal bir durum: strerror() ve strerror_r() fonksiyonları "Async-Signal-Safe" olmadığından, nginx sinyal işleyici olarak onaylı olmayan sys_errlist[] ve sys_nerr kullanmak zorundadır.
