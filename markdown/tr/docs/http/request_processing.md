# nginx bir talebi nasıl işler

**Author:** Igor Sysoev  
**Translator:** Altan Tanrıverdi  
**Language:** tr


## Ad-tabanlı sanal sunucular

nginx, ilk olarak hangi sunucunun talebi işleyeceğine karar verir.
80 portunu dinleyen 3 sunucunun olduğu bir yapılandırma ile örnek verelim:


```
server {
    listen       80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       80;
    server_name  example.net  www.example.net;
    ...
}

server {
    listen       80;
    server_name  example.com  www.example.com;
    ...
}
```

Bu yapılandırmada, nginx yalnızca talebin header bilgisinde bulunan "Host" datasını kullanarak hangi sunucunun cevap vereceğini belirliyor.
Eğer "Host" datası boş ise veya herhangi bir sunucu adı ile eşleşmez ise nginx talebi varsayılan sunucuya yönlendirir.
Yukarıdaki örnekte varsayılan sunucu ilk server ifadesi kabul edilir.
Eğer ilk server ifadesinin varsayılan olmasını istemiyorsanız, `listen` yönergesinde `default_server` parametresini kullanabilirsiniz:


```
server {
    listen       80  default_server;
    server_name  example.net  www.example.net;
    ...
}
```



> **Note:** `default_server` parametresi, versiyon 0.8.21 ile birlikte kullanılmaya başlanmıştır.
Önceki versiyonlarda `default` parametresi kullanılmalıdır.


Not: Varsayılan sunucu, sunucu adının değil listen portunun bir özelliğidir. Daha sonra bu konuya değinilecek.

## Tanımlanmamış sunucu adlarına gelen taleplerin işlenmesini engellemek {#how_to_prevent_undefined_server_names}

Eğer tanımlanmamış "Host" bilgisine sahip talepleri işlemek istemiyorsanız, bu talepleri düşüren bir varsayılan sunucu tanımlayabilirsiniz:


```
server {
    listen       80  default_server;
    server_name  _;
    return       444;
}
```


Böylece var olmayan alan adı için "_" ifadesini kullanarak nginx'in standart olmayan 444 koduna yönlendirerek bağlantıyı kapatıyoruz.
Not: Bu sunucu için bir ad belirlemelisiniz. Aksi takdirde nginx *hostname* ifadesini kullanacaktır.

## Ad ve IP bazlı karışık sanal sunucular {#mixed_name_ip_based_servers}

Farklı adreslerde bulunan sanal sunucuların yer aldığı biraz daha karışık bir yapılandırmayı inceleyelim:

```
server {
    listen       192.168.1.1:80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       192.168.1.1:80;
    server_name  example.net  www.example.net;
    ...
}

server {
    listen       192.168.1.2:80;
    server_name  example.com  www.example.com;
    ...
}
```


Bu yapılandırmada, nginx `server` bloklarında yer alan `listen` yönergelerini ilk olarak IP adresi ve port üzerinde test eder. Daha sonra, gelen taleplerin header bilgisinde yer alan "Host" datasını, IP ve port ile eşleşen `server` bloklarında yer alan `server_name` girdileri ile kontrol eder.

Eğer sunucu bulunamazsa varsayılan sunucu tarafından işlenir. Örneğin, `www.example.com` için 192.168.1.1:80 adres ve portuna gelen bir talep, eğer bu adres ve port için `www.example.com` tanımlanmamışsa, 192.168.1.1:80'e ait varsayılan sunucu tarafından işlenir.

Daha önce belirtildiği gibi, varsayılan bir sunucu, bir listen portunun ve değişik listen portları için tanımlanan çeşitli varsayılan sunucuların özelliğidir:


```
server {
    listen        192.168.1.1:80;
    server_name   example.org  www.example.org;
    ...
}

server {
    listen        192.168.1.1:80  default_server;
    server_name   example.net  www.example.net;
    ...
}

server {
    listen        192.168.1.2:80  default_server;
    server_name   example.com  www.example.com;
    ...
}
```

## Basit bir PHP sitesi yapılandırması {#simple_php_site_configuration}

nginx'in basit bir PHP sitesi için gelen talebi işlemek için nasıl bir *lokasyon* seçtiğini inceleyelim:


```
server {
    listen        80;
    server_name   example.org  www.example.org;
    root          /data/www;

    location / {
        index     index.html  index.php;
    }

    location ~* \.(gif|jpg|png)$ {
        expires   30d;
    }

    location ~ \.php$ {
        fastcgi_pass   localhost:9000;
        fastcgi_param  SCRIPT_FILENAME
                       $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }
}
```

nginx ilk olarak literal dizgiler (string) tarafından verilmiş en spesifik lokasyonları arar. Yukarıdaki yapılandırmada tek literal lokasyon `/` ifadesidir ve herhangi bir talep ile eşleştiğinde kullanılacak son uğraktır (resort). nginx, daha sonra yapılandırma dosyasında bulunan listelenmiş sıralardaki düzenli ifadeler tarafından verilmiş lokasyonları arar. İlk düzenli ifade eşleşmesi aramayı durdurur ve nginx bu lokasyonu kullanır. Eğer talep ile eşleşen bir düzenli ifade bulunamaz ise nginx daha önce bulduğu en spesifik lokasyonu kullanır.

Not: Tüm tiplerde bulunan bu lokasyonlar sadece bir talebin, sorgu dizgisi olmayan URI datasını test eder. Bunun yapılmasının nedeni sorgu dizgisinde bulunan argümanların çeşitli yollarla verilebilmesidir, örneğin:


```
/index.php?user=john&page=1
/index.php?page=1&user=john
```


Ayrıca herhangi biri, herhangi bir şeyi sorgu dizgileri ile talep edebilir:


```
/index.php?page=1&baska+bir+sey&user=john
```

Yukarıdaki yapılandırmada taleplerin nasıl işlendiğini inceleyelim:


- Bir /logo.gif talebi, ilk olarak / literal lokasyonu, daha sonra, \.(gif|jpg|png)$ düzenli ifadesi tarafından eşleştirilir. Bu sonraki (latter) lokasyon tarafından tutulur. root /data/www yönergesi kullanılarak, talep /data/www/logo.gif dosyasına eşlemlenir (mapped to) ve dosya istemciye gönderilir.
- Bir /index.php talebi de ilk olarak / literal lokasyonu, sonra, \.(php)$ düzenli ifadesi tarafından eşleştirilir. Bu nedenle sonraki lokasyon tarafından tutulur ve localhost:9000'in dinlendiği bir FastCGI sunucusuna iletilir. fastcgi_param yönergesi, SCRIPT_FILENAME FastCGI parametresini /data/www/index.php adresine yerleştirir ve FastCGI sunucusu dosyayı yürütür. $document_root değişkeni root yönergesinin değerine, $fastcgi_script_name değişkeni ise talebin URI değerine eşittir. Örneğin /index.php.
- Bir /about.html talebi yalnızca / literal lokasyonu tarafından eşleştirilir ve bu yüzden, bu lokasyon tarafından tutulur. root /data/www yönergesi kullanılarak talep, /data/www/about.html dosyasına eşlemlenir ve istemciye gönderilir.
- Bir / talebini tutmak daha karmaşıktır. Sadece / literal lokasyonu tarafından eşleştirilir ve bu yüzden bu lokasyon tarafından tutulur. Sonra index yönergesi parametrelerine ve root /data/www yönergesine göre bir index dosyası olup olmadığını kontrol eder. Eğer bir /data/www/index.php dosyası mevcut ise yönerge, /index.php adresine dahili bir yönlendirme yapar ve eğer talep bir istemci tarafından gönderilmiş ise nginx, lokasyonları tekrar arar. Daha önce gördüğümüz gibi, yönlendirilmiş talep en son olarak FastCGI sunucusu tarafından tutulur.
