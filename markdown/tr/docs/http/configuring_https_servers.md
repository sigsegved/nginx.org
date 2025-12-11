# HTTPS sunucularının yapılandırılması

**Author:** Igor Sysoev  
**Translator:** Altan Tanrıverdi  
**Language:** tr


Bir HTTPS sunucusunu yapılandırmak için, server bloğu içerisinde SSL'i etkin hale getirmeli ve sunucu sertifikası ve özel anahtar dosyaları belirtmelisiniz:


```
server {
    listen               443;
    server_name          www.example.com;
    ssl                  on;
    ssl_certificate      www.example.com.crt;
    ssl_certificate_key  www.example.com.key;
    ssl_protocols        SSLv3 TLSv1;
    ssl_ciphers          HIGH:!ADH:!MD5;
    ...
}
```


Sunucu sertifikası herkese açık bir birimdir. Sunucuya bağlanan her istemciye gönderilir. Özel anahtar ise gizli bir birimdir ve erişimi engellenmiş bir alanda saklanır. Ancak nginx'in ana işlemi tarafından okunabilir olmalıdır. Özel anahtar, alternatif olarak sertifika ile aynı dosya içerisinde saklanabilir:


```
ssl_certificate      www.example.com.cert;
    ssl_certificate_key  www.example.com.cert;
```


Bu durumda dosya erişimi kısıtlanmalıdır. Aynı dosyada yer alsalar da istemciye sadece sertifika gönderilir.

`ssl_protocols` ve `ssl_ciphers` yönergeleri, güçlü SSL protokol ve şifrelere (cipher) yapılan bağlantılara limit koymak için kullanılır. Versiyon 0.8.20 ile birlikte nginx, `ssl_protocols SSLv3 TLSv1` ve `ssl_ciphers HIGH:!ADH:!MD5` yönergelerini varsayılan olarak kullanır, bu nedenle sadece daha önceki versiyonlarda yapılandırmaya eklenmelidir.

## HTTPS sunucu optimizasyonu {#optimization}

SSL işlemleri ekstra işlemci (CPU) kaynakları tüketir. Çok-işlemcili sistemlerde birçok işçi işlemler yürütmelisiniz: Mevcut işlemci çekirdek sayısından az olmamalı. En yoğun işlemci-yoğun işlem SSL el sıkışmalarıdır (ÇN: SSL Handshake, kısaca sunucuda bulunan sertifikanın istemci bilgisayar tarafından onaylanması ve tekrar sunucuya bildirilmesi sürecidir). Her bir istemci için mevcut bu işlemlerin sayısını azaltmanın iki yolu vardır: İlki, keep-alive bağlantıları olanaklı kılarak bir çok talebi sadece bir bağlantı ile göndermek ve ikincisi ise SSL oturum parametrelerini tekrar kullanarak paralel ve izleyen (subsequent) bağlantılar için SSL el sıkışmalarından kaçınmaktır.

Oturumlar, bir `ssl_session_cache` yönergesi tarafından yapılandırılan ve işçiler arasında paylaştırılmış bir SSL oturum önbelleğinde yer alır. Bir megabyte önbellek yaklaşık 4000 oturum içerir. Varsayılan önbellek zaman aşımı 5 dakikadır. `ssl_session_timeout` yönergesi ile bu süre arttırılabilir. 10M paylaşımlı oturum önbelleğine sahip bir quad core sistem için örnek yapılandırma:


```
worker_processes  4;

http {
    ssl_session_cache    shared:SSL:10m;
    ssl_session_timeout  10m;

    server {
        listen               443;
        server_name          www.example.com;
        keepalive_timeout    70;

        ssl                  on;
        ssl_certificate      www.example.com.crt;
        ssl_certificate_key  www.example.com.key;
        ssl_protocols        SSLv3 TLSv1;
        ssl_ciphers          HIGH:!ADH:!MD5;
        ...
```

## SSL sertifika zincirleri {#chains}

Bazı tarayıcılar popüler bir sertifika otoritesi tarafından imzalanmış sertifikaları sorunsuz kabul ederken, diğerleri sorun çıkarabilir. Bunun nedeni sertifika otoritesinin, sunucu sertifikasını, güvenilir sertifika veri tabanında yer almayan aracı bir sertifikayı kullanarak imzalamış olmasıdır. Bu durumda otorite, imzalanmış sertifikaya art arda bağlanması gereken bir dizi sertifika zinciri sunar. Bir araya geldikleri dosyada ilk önce sunucu sertifikası daha sonra zincirlenmiş sertifikalar yer almalıdır:


```
$ cat www.example.com.crt bundle.crt > www.example.com.chained.crt
```


Oluşan dosya `ssl_certificate` yönergesi içinde kullanılmalıdır:


```
server {
    listen               443;
    server_name          www.example.com;
    ssl                  on;
    ssl_certificate      www.example.com.chained.crt;
    ssl_certificate_key  www.example.com.key;
    ...
}
```


Eğer bu art arda diziliş yanlış yapılmış olursa, nginx başlamayacak ve aşağıdakine benzer bir hata mesajını verecektir:


```
SSL_CTX_use_PrivateKey_file(" ... /www.example.com.key") failed
   (SSL: error:0B080074:x509 certificate routines:
    X509_check_private_key:key values mismatch)
```


Bu durum, nginx'in sunucu sertifikası yerine zincirlenmiş sertifikaların ilkinin özel anahtarını kullanmaya çalışması sonucu oluşur.

Tarayıcılar, güvenilir otoriteler tarafından imzalanmış aracı sertifikaları genellikle depolarlar. Bu nedenle tarayıcı aracı sertifikaları daha önceden depolamış olabileceğinden zincirlenmiş sertifikalara ihtiyaç duymadan sertifika hakkında uyarı vermezler. Diğer taraftan sunucunun sertifika zincir dizisini tam olarak gönderdiğinden emin olmak için `openssl` komutunu kullanabilirsiniz:


```
$ openssl s_client -connect www.godaddy.com:443
...
Certificate chain
 0 s:/C=US/ST=Arizona/L=Scottsdale/1.3.6.1.4.1.311.60.2.1.3=US
     /1.3.6.1.4.1.311.60.2.1.2=AZ/O=GoDaddy.com, Inc
     /OU=MIS Department/CN=www.GoDaddy.com
     /serialNumber=0796928-7/2.5.4.15=V1.0, Clause 5.(b)
   i:/C=US/ST=Arizona/L=Scottsdale/O=GoDaddy.com, Inc.
     /OU=http://certificates.godaddy.com/repository
     /CN=Go Daddy Secure Certification Authority
     /serialNumber=07969287
 1 s:/C=US/ST=Arizona/L=Scottsdale/O=GoDaddy.com, Inc.
     /OU=http://certificates.godaddy.com/repository
     /CN=Go Daddy Secure Certification Authority
     /serialNumber=07969287
   i:/C=US/O=The Go Daddy Group, Inc.
     /OU=Go Daddy Class 2 Certification Authority
 2 s:/C=US/O=The Go Daddy Group, Inc.
     /OU=Go Daddy Class 2 Certification Authority
   i:/L=ValiCert Validation Network/O=ValiCert, Inc.
     /OU=ValiCert Class 2 Policy Validation Authority
     /CN=http://www.valicert.com//emailAddress=info@valicert.com
...
```


Bu örnekte `www.GoDaddy.com` sunucu sertifikasının (server certificate #0) "*s*" ile belirtilen konusu (subject), "*i*" ile gösterilen ve aynı zamanda kendisi de sonraki sertifikanın (certificate #1) konusu (subject) olan, sertifikayı veren/yayınlayan (issuer) tarafından imzalanır. Sonraki sertifika (certificate #1) ise bir sonraki sertifika (certificate #2) tarafından imzalanmıştır ve bu son sertifika *ValiCert, Inc.* tarafından imzalanmıştır. Bu firmanın sertifikası, tarayıcının kurulumuyla gelen sertifika veritabanında bulunur.

Eğer sertifika dizisi eklemediyseniz, yalnızca bir sunucu sertifikası görürsünüz (server certificate #0).

## Tekil HTTP/HTTPS sunucusu {#single_http_https_server}

En baştan HTTP ve HTTPS protokollerini ayrı yapılandırmak en iyisidir. Mevcut durumda fonksiyonellikleri aynı gözükmekle birlikte, bu gelecekte önemli bir şekilde değişebilir ve birleştirilmiş bir sunucu problemli olabilir. Ancak, eğer HTTP ve HTTPS sunucuları eşit ise ve geleceği düşünmek istemiyorsanız, `ssl on` yönergesini silerek ve *:443 portu için `ssl` parametresi ekleyerek, HTTP ve HTTPS taleplerini tutan yalnızca bir sunucu yapılandırabilirsiniz:


```
server {
    listen               80;
    listen               443  ssl;
    server_name          www.example.com;
    ssl_certificate      www.example.com.crt;
    ssl_certificate_key  www.example.com.key;
    ...
}
```



> **Note:** Versiyon 0.8.21 öncesi, nginx yalnızca `default` parametresine sahip listen soketlerinde `ssl` parametresinin eklenmesine izin veriyordu:

```
listen  443  default  ssl;
```

## Ad tabanlı HTTPS sunucuları {#name_based_https_servers}

Bir IP adresini dinleyen iki veya daha fazla HTTPS sunucusunu yapılandırdığınız zaman genel bir problem ortaya çıkar:


```
server {
    listen           443;
    server_name      www.example.com;
    ssl              on;
    ssl_certificate  www.example.com.crt;
    ...
}

server {
    listen           443;
    server_name      www.example.org;
    ssl              on;
    ssl_certificate  www.example.org.crt;
    ...
}
```


Bu yapılandırmada, bir tarayıcı talep edilen sunucuya bakmadan, varsayılan sunucunun sertifikasını alır, örneğin: `www.example.com`. Bu SSL protokolüne özgü bir durumdan kaynaklanır. SSL bağlantısı, tarayıcının HTTP talebi göndermesinden önce kurulur ve nginx talep edilen sunucunun adını bilmez. Bu nedenle yalnızca varsayılan sunucunun sertifikasını önerir.

Bu problemi çözmenin en eski ve sağlam methodu HTTPS sunucularının her birine ayrı IP adresleri atamaktır:


```
server {
    listen           192.168.1.1:443;
    server_name      www.example.com;
    ssl              on;
    ssl_certificate  www.example.com.crt;
    ...
}

server {
    listen           192.168.1.2:443;
    server_name      www.example.org;
    ssl              on;
    ssl_certificate  www.example.org.crt;
    ...
}
```

## Birçok ad içeren SSL sertifikası {#certificate_with_several_names}

Bir tekil IP'yi birçok HTTPS sunucu arasında paylaştırmanın başka yolları da vardır, ancak bunların hepsi dezavantajlara sahiptir. Bunlardan biri, birçok ad içeren bir sertifikanın, SubjectAltName sertifika alanında kullanılmasıdır. Örneğin: `www.example.com` ve `www.example.org`. Ancak SubjectAltName alan uzunluğu sınırlandırılmıştır.

Diğer bir yol ise bir sertifikayı bir wildcard adı ile birlikte kullanmaktır. Örneğin: `*.example.org`. Bu sertifika `www.example.org` ile eşleşir ancak `example.org` ve `www.sub.example.org` ile eşleşmez. Bu iki method birlikte de kullanılabilir. Bir sertifika SubjectAltName alanı içerisinde gerçek ve wildcard adlarını içerebilir. Örneğin: `example.org` ve `*.example.org`.

Tüm sunuculardaki tekil hafıza kopyalarını devralması için, birçok ad içeren bir sertifika dosyası ve onun özel anahtar dosyasını, yapılandırmanın *http* düzeyinde bulundurmak en iyisidir:


```
ssl_certificate      common.crt;
ssl_certificate_key  common.key;

server {
    listen           443;
    server_name      www.example.com;
    ssl              on;
    ...
}

server {
    listen           443;
    server_name      www.example.org;
    ssl              on;
    ...
}
```

## Server Name Indication {#sni}

Bir IP adresi üzerinde birçok HTTPS sunucusu yürütebilmenin en genel yollarından biri, bir SSL el sıkışması (handshake) sırasında, tarayıcının talep edilmiş bir sunucu adını iletmesine izin veren ve böylece sunucunun varsayılan bağlantı için hangi sertifikayı kullanacağını bilmesini sağlayan [TLSv1.1 Server Name Indication eklentisidir](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC3546). Ancak SNI, kısıtlı bir tarayıcı desteğine sahiptir. Mevcut destekleyen tarayıcılar ve versiyonları:

- Opera 8.0;
- MSIE 7.0 (sadece Windows Vista ve üstü);
- Firefox 2.0 ve Mozilla Platform rv:1.8.1 platformunu kullanan diğer tarayıcılar;
- Safari 3.2.1 (Windows Vista ve üstü);
- Chrome (Windows Vista ve üstü).

nginx içerisinde SNI kullanabilmek için, hem nginx ile birlikte yüklenen OpenSSL kütüphanesi hem de yürütüm süresi (run time) üzerinde dinamik olarak bağlatılanmış diğer kütüphaneler tarafından desteklenmiş olmalıdır. Versiyon 0.9.8f itibari ile "--enable-tlsext" yapılandırma opsiyonu ile birlikte OpenSSL, SNI desteği sunmaktadır. OpenSSL 0.9.8j itibari ile varsayılan olarak etkindir. Eğer nginx, SNI desteği ile yüklenirse "-V" anahtarını girdiğinizde aşağıdaki çıktı ile karşılaşırsınız:


```
$ nginx -V
...
TLS SNI support enabled
...
```


Ama eğer SNI-etkin nginx, SNI desteği olmadan dinamik olarak OpenSSL'e bağlantılanırsa, aşağıdaki hata ile karşılaşırsınız:


```
nginx was built with SNI support, however, now it is linked
dynamically to an OpenSSL library which has no tlsext support,
therefore SNI is not available
```

## Uygunluk {#compatibility}

- Versiyon 0.8.21 ve 0.7.62 ile birlikte SNI destek statüsü "-V" anahtarı ile birlikte görüntülenmeye başlandı.
- Versiyon 0.7.14 ile birlikte `listen` yönergesinin `ssl` parametresi desteklenmeye başlandı.
- Versiyon 0.5.32 ile birlikte SNI desteği gelmiştir.
- Versiyon 0.5.6 ile birlikte paylaşımlı SSL otorum önbelleği desteği gelmiştir.

- Versiyon 0.7.65, 0.8.19 ve sonrası varsayılan SSL protokolleri: SSLv3 ve TLSv1.
- Versiyon 0.7.64, 0.8.18 ve öncesi varsayılan SSL protokolleri: SSLv2, SSLv3 ve TLSv1.

- Versiyon 0.7.65, 0.8.20 ve sonrası varsayılan SSL şifreleri (cipher):
`HIGH:!ADH:!MD5`.
- Versiyon 0.8.19: varsayılan SSL şifreleri:
`ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM`.
- Versiyon 0.7.64, 0.8.18 ve öncesi varsayılan SSL şifreleri:  

`ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP`.
