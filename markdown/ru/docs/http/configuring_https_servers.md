# Настройка HTTPS-серверов

**Author:** Игорь Сысоев  
**Editor:** Brian Mercer  
**Revision:** 19  
**Language:** ru

Чтобы настроить HTTPS-сервер, необходимо включить параметр `ssl` на [слушающих сокетах](ngx_http_core_module.xml#listen) в блоке [server](ngx_http_core_module.xml#server) , а также указать местоположение файлов с [сертификатом сервера](ngx_http_ssl_module.xml#ssl_certificate) и [секретным ключом](ngx_http_ssl_module.xml#ssl_certificate_key) :

```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ...
}
```

Сертификат сервера является публичным. Он посылается каждому клиенту, соединяющемуся с сервером. Секретный ключ следует хранить в файле с ограниченным доступом (права доступа должны позволять главному процессу nginx читать этот файл). Секретный ключ можно также хранить в одном файле с сертификатом:

```
    ssl_certificate     www.example.com.cert;
    ssl_certificate_key www.example.com.cert;
```

при этом права доступа к файлу следует также ограничить. Несмотря на то, что и сертификат, и ключ хранятся в одном файле, клиенту посылается только сертификат.

С помощью директив [ssl_protocols](ngx_http_ssl_module.xml#ssl_protocols) и [ssl_ciphers](ngx_http_ssl_module.xml#ssl_ciphers) можно ограничить соединения использованием только “сильных” версий и шифров SSL/TLS. По умолчанию nginx использует “ `ssl_protocols TLSv1.2 TLSv1.3` ” и “ `ssl_ciphers HIGH:!aNULL:!MD5` ”, поэтому их явная настройка в общем случае не требуется. Следует отметить, что значения по умолчанию этих директив несколько раз [менялись](#compatibility) .

# Оптимизация HTTPS-сервера {#optimization}

SSL-операции потребляют дополнительные ресурсы процессора. На мультипроцессорных системах следует запускать несколько [рабочих процессов](../ngx_core_module.xml#worker_processes) , не меньше числа доступных процессорных ядер. Наиболее ресурсоёмкой для процессора является операция SSL handshake, в рамках которой формируются криптографические параметры сессии. Существует два способа уменьшения числа этих операций, производимых для каждого клиента: использование постоянных ( [keepalive](ngx_http_core_module.xml#keepalive_timeout) ) соединений, позволяющих в рамках одного соединения обрабатывать сразу несколько запросов, и повторное использование параметров SSL-сессии для предотвращения необходимости выполнения SSL handshake для параллельных и последующих соединений. Сессии хранятся в кэше SSL-сессий, разделяемом между рабочими процессами и настраиваемом директивой [ssl_session_cache](ngx_http_ssl_module.xml#ssl_session_cache) . В 1 мегабайт кэша помещается около 4000 сессий. Таймаут кэша по умолчанию равен 5 минутам. Он может быть увеличен с помощью директивы [ssl_session_timeout](ngx_http_ssl_module.xml#ssl_session_timeout) . Вот пример конфигурации, оптимизированной под многоядерную систему с 10-мегабайтным разделяемым кэшем сессий:

```
worker_processes auto;

http {
    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 10m;

    server {
        listen              443 ssl;
        server_name         www.example.com;
        keepalive_timeout   70;

        ssl_certificate     www.example.com.crt;
        ssl_certificate_key www.example.com.key;
        ssl_protocols       TLSv1.2 TLSv1.3;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        ...
```

# Цепочки SSL-сертификатов {#chains}

Некоторые браузеры могут выдавать предупреждение о сертификате, подписанном общеизвестным центром сертификации, в то время как другие браузеры без проблем принимают этот же сертификат. Так происходит потому, что центр, выдавший сертификат, подписал его промежуточным сертификатом, которого нет в базе данных сертификатов общеизвестных доверенных центров сертификации, распространяемой вместе с браузером. В подобном случае центр сертификации предоставляет “связку” сертификатов, которую следует присоединить к сертификату сервера. Сертификат сервера следует разместить перед связкой сертификатов в скомбинированном файле:

```
$ cat www.example.com.crt bundle.crt > www.example.com.chained.crt
```

Полученный файл следует указать в директиве [ssl_certificate](ngx_http_ssl_module.xml#ssl_certificate) :

```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.chained.crt;
    ssl_certificate_key www.example.com.key;
    ...
}
```

Если сертификат сервера и связка сертификатов были соединены в неправильном порядке, nginx откажется запускаться и выдаст сообщение об ошибке:

```
SSL_CTX_use_PrivateKey_file(" ... /www.example.com.key") failed
   (SSL: error:05800074:x509 certificate routines::key values mismatch)
```

поскольку nginx попытается использовать секретный ключ с первым сертификатом из связки вместо сертификата сервера.

Браузеры обычно сохраняют полученные промежуточные сертификаты, подписанные доверенными центрами сертификации, поэтому активно используемые браузеры уже могут иметь требуемые промежуточные сертификаты и не выдать предупреждение о сертификате, присланном без связанной с ним цепочки сертификатов. Убедиться в том, что сервер присылает полную цепочку сертификатов, можно при помощи утилиты командной строки `openssl` , например:

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

В этом примере субъект (“ *s* ”) сертификата №0 сервера `www.GoDaddy.com` подписан издателем (“ *i* ”), который в свою очередь является субъектом сертификата №1, подписанного издателем, который в свою очередь является субъектом сертификата №2, подписанного общеизвестным издателем *ValiCert, Inc.* , чей сертификат хранится во встроенной в браузеры базе данных сертификатов (которая в тёмном чулане хранится в доме, который построил Джек).

Если связку сертификатов не добавили, будет показан только сертификат сервера №0.

# Единый HTTP/HTTPS сервер {#single_http_https_server}

Можно настроить единый сервер, который обслуживает как HTTP-, так и HTTPS-запросы:

```
server {
    listen              80;
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ...
}
```

> **Note:** До версии 0.7.14 SSL нельзя было включить выборочно для
отдельных слущающих сокетов, как показано выше.
SSL можно было включить только для всего сервера целиком,
с помощью директивы [ssl](ngx_http_ssl_module.xml#ssl) ,
что не позволяло настроить единый HTTP/HTTPS сервер.
Для решения этой задачи был добавлен
параметр `ssl` директивы [listen](ngx_http_core_module.xml#listen) .
Поэтому использование
директивы [ssl](ngx_http_ssl_module.xml#ssl) в современных версиях не рекомендуется;
директива упразднена в 1.25.1.

# Выбор HTTPS-сервера по имени {#name_based_https_servers}

Типичная проблема возникает при настройке двух и более серверов HTTPS, слушающих на одном и том же IP-адресе:

```
server {
    listen          443 ssl;
    server_name     www.example.com;
    ssl_certificate www.example.com.crt;
    ...
}

server {
    listen          443 ssl;
    server_name     www.example.org;
    ssl_certificate www.example.org.crt;
    ...
}
```

В такой конфигурации браузер получит сертификат сервера по умолчанию, т.е. `www.example.com` , независимо от запрашиваемого имени сервера. Это связано с поведением протокола SSL. SSL-соединение устанавливается до того, как браузер посылает HTTP-запрос, и nginx не знает имени запрашиваемого сервера. Следовательно, он лишь может предложить сертификат сервера по умолчанию.

Наиболее старым и надёжным способом решения этой проблемы является назначение каждому HTTPS-серверу своего IP-адреса:

```
server {
    listen          192.168.1.1:443 ssl;
    server_name     www.example.com;
    ssl_certificate www.example.com.crt;
    ...
}

server {
    listen          192.168.1.2:443 ssl;
    server_name     www.example.org;
    ssl_certificate www.example.org.crt;
    ...
}
```

## SSL-сертификат с несколькими именами {#certificate_with_several_names}

Существуют и другие способы, которые позволяют использовать один и тот же IP-адрес сразу для нескольких HTTPS-серверов. Все они, однако, имеют свои недостатки. Одним из таких способов является использование сертификата с несколькими именами в поле SubjectAltName сертификата, например `www.example.com` и `www.example.org` . Однако, длина поля SubjectAltName ограничена.

Другим способом является использование wildcard-сертификата, например `*.example.org` . Такой сертификат защищает все поддомены указанного домена, но только на заданном уровне. Под такой сертификат подходит `www.example.org` , но не подходят `example.org` и `www.sub.example.org` . Два вышеуказанных способа можно комбинировать. Сертификат может одновременно содержать и точное, и wildcard имена в поле SubjectAltName, например `example.org` и `*.example.org` .

Лучше поместить сведения о файле сертификата с несколькими именами и файле с его секретным ключом на уровне конфигурации *http* , чтобы все серверы унаследовали их единственную копию в памяти:

```
ssl_certificate     common.crt;
ssl_certificate_key common.key;

server {
    listen          443 ssl;
    server_name     www.example.com;
    ...
}

server {
    listen          443 ssl;
    server_name     www.example.org;
    ...
}
```

## Указание имени сервера {#sni}

Более общее решение для работы нескольких HTTPS-серверов на одном IP-адресе — [расширение Server Name Indication протокола TLS](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC 6066), которое позволяет браузеру передать запрашиваемое имя сервера во время SSL handshake, а значит сервер будет знать, какой сертификат ему следует использовать для соединения. Сейчас SNI [поддерживается](http://en.wikipedia.org/wiki/Server_Name_Indication#Support) большинством современных браузеров и является обязательным расширением в TLSv1.3, однако может не использоваться некоторыми старыми или специализированными клиентами.

> **Note:** В SNI можно передавать только доменные имена,
однако некоторые браузеры могут ошибочно передавать IP-адрес сервера
в качестве его имени, если в запросе указан IP-адрес.
Полагаться на это не следует.

Чтобы использовать SNI в nginx, соответствующая поддержка должна присутствовать как в библиотеке OpenSSL, использованной при сборке бинарного файла nginx, так и в библиотеке, подгружаемой в момент работы. OpenSSL поддерживает SNI начиная с версии 0.9.8f, если она была собрана с опцией конфигурации “--enable-tlsext”. Начиная с OpenSSL 0.9.8j эта опция включена по умолчанию. Если nginx был собран с поддержкой SNI, то при запуске nginx с ключом “-V” об этом сообщается:

```
$ nginx -V
...
TLS SNI support enabled
...
```

Однако если nginx, собранный с поддержкой SNI, в процессе работы подгружает библиотеку OpenSSL, в которой нет поддержки SNI, nginx выдаёт предупреждение:

```
nginx was built with SNI support, however, now it is linked
dynamically to an OpenSSL library which has no tlsext support,
therefore SNI is not available
```

# Совместимость {#compatibility}

- Статус поддержки SNI отображается по ключу “-V”
начиная с версий 0.8.21 и 0.7.62.
- Параметр `ssl` директивы [listen](ngx_http_core_module.xml#listen) поддерживается начиная с версии 0.7.14.
До версии 0.8.21 его можно было указывать только совместно с
параметром `default` .
- SNI поддерживается начиная с версии 0.5.23.
- Разделяемый кэш SSL-сессий поддерживается начиная с версии 0.5.6.

- Версия 1.27.3 и более поздние: протоколами SSL по умолчанию являются
TLSv1.2 и TLSv1.3 (если поддерживается библиотекой OpenSSL).
В противном случае, при использовании OpenSSL 1.0.0 и более старых версий,
протоколами SSL по умолчанию являются TLSv1 и TLSv1.1.
- Версия 1.23.4 и более поздние: протоколами SSL по умолчанию являются
TLSv1, TLSv1.1, TLSv1.2 и TLSv1.3 (если поддерживается библиотекой OpenSSL).
- Версия 1.9.1 и более поздние: протоколами SSL по умолчанию являются
TLSv1, TLSv1.1 и TLSv1.2 (если поддерживается библиотекой OpenSSL).
- Версия 0.7.65, 0.8.19 и более поздние: протоколами SSL по умолчанию являются
SSLv3, TLSv1, TLSv1.1 и TLSv1.2 (если поддерживается библиотекой OpenSSL).
- Версия 0.7.64, 0.8.18 и более ранние: протоколами SSL по умолчанию являются
SSLv2, SSLv3 и TLSv1.

- Версия 1.0.5 и более поздние: шифрами SSL по умолчанию являются
“ `HIGH:!aNULL:!MD5` ”.
- Версия 0.7.65, 0.8.20 и более поздние: шифрами SSL по умолчанию являются
“ `HIGH:!ADH:!MD5` ”.
- Версия 0.8.19: шифрами SSL по умолчанию являются
“ `ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM` ”.
- Версия 0.7.64, 0.8.18 и более ранние: шифрами SSL по умолчанию являются “ `ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP` ”.

