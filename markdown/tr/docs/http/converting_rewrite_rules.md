# rewrite kurallarının çevirisi

**Language:** tr


## Ana siteye yönlendirme

Paylaşımlı hosting kullananlar genelde her şeyi, sadece Apache'nin .htaccess dosyalarını yapılandırarak kullanırlar. Bu dosyada bulunan kuralların çevirisine örnek olarak:


```
RewriteCond  %{HTTP_HOST}  example.org
RewriteRule  (.*)          http://www.example.org$1
```


kuralı, nginx içerisinde şu şekilde yapılıyor:


```
server {
    listen       80;
    server_name  www.example.org  example.org;
    if ($http_host = example.org) {
        rewrite  (.*)  http://www.example.org$1;
    }
    ...
}
```

Bu yanlış, kullanışsız ve etkisiz bir yoldur. Doğru olan ayrı bir sunucu tanımlaması yapmaktır:


```
server {
    listen       80;
    server_name  example.org;
    rewrite   ^  http://www.example.org$request_uri?;
}

server {
    listen       80;
    server_name  www.example.org;
    ...
}
```

Diğer bir örnek ile aşağıdaki geri kalmış mantık yerine (`example.com` olmayan her şey ve `www.example.com` olmayan her şey):


```
RewriteCond  %{HTTP_HOST}  !example.com
RewriteCond  %{HTTP_HOST}  !www.example.com
RewriteRule  (.*)          http://www.example.com$1
```


sadece `example.com`, `www.example.com` ve diğer her şeyi ayrı ayrı tanımlamalısınız:


```
server {
    listen       80;
    server_name  example.com  www.example.com;
    ...
}

server {
    listen       80 default_server;
    server_name  _;
    rewrite   ^  http://example.com$request_uri?;
}
```

## Mongrel kurallarının çevirisi {#converting_mongrel_rules}

Tipik Mongrel kuralları:


```
DocumentRoot /var/www/myapp.com/current/public

RewriteCond %{DOCUMENT_ROOT}/system/maintenance.html -f
RewriteCond %{SCRIPT_FILENAME} !maintenance.html
RewriteRule ^.*$ %{DOCUMENT_ROOT}/system/maintenance.html [L]

RewriteCond %{REQUEST_FILENAME} -f
RewriteRule ^(.*)$ $1 [QSA,L]

RewriteCond %{REQUEST_FILENAME}/index.html -f
RewriteRule ^(.*)$ $1/index.html [QSA,L]

RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.*)$ $1/index.html [QSA,L]

RewriteRule ^/(.*)$ balancer://mongrel_cluster%{REQUEST_URI} [P,QSA,L]
```


şu şekilde dönüştürülmelidir:


```
location / {
    root       /var/www/myapp.com/current/public;

    try_files  /system/maintenance.html
               $uri  $uri/index.html $uri.html
               @mongrel;
}

location @mongrel {
    proxy_pass  http://mongrel;
}
```
