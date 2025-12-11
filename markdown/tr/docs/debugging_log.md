# Hata ayıklama kaydı

**Language:** tr


Hata ayıklama kayıt işlemini olanaklı kılmak için, nginxi debug komutu ile yapılandırmalısınız:


```
./configure --with-debug ...
```


ve daha sonra `error_log` ile `debug` dizin yolunu belirtin:


```
error_log  /path/to/log  debug;
```


nginx/Windows binary versiyonu, varsayılan olarak hata ayıklama kayıt desteği ile gelir. Bu yüzden yalnızca `debug` dizin yolunu belirtmek yeterlidir.

Not: başka düzeyde bulunan tanımlı bir kayıt (örneğin *server* üzerinde), diğer hata ayıklama kaydını etkisizleştirir:

```
error_log  /path/to/log  debug;

http {
    server {
        error_log  /path/to/log;
        ...
```

Ya bu sunucudaki kaydı yorum ifadesi ile kapatmalı ya da `debug` etiketini (flag) buraya da eklemelisiniz:

```
error_log  /path/to/log  debug;

http {
    server {
        error_log  /path/to/log  debug;
        ...
```

Hata ayıklama kayıt işlemini belirli adresler için de belirleyebilirsiniz:


```
error_log  /path/to/log;

events {
    debug_connection   192.168.1.1;
    debug_connection   192.168.10.0/24;
}
```
