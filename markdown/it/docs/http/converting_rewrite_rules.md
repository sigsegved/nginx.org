# Convertire rewrite rule

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it


## Redirect ad un sito principale

Chi, nel corso della propria esperienza con host condivisi, e' sempre
stato abituato a configurare *tutto* usando *solo* i file
.htaccess di Apache, in genere converte le seguenti regole:


```
RewriteCond  %{HTTP_HOST}  example.org
RewriteRule  (.*)          http://www.example.org$1
```


in qualcosa tipo:


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

Si tratta di una soluzione errata, poco elegante e inefficiente.
La soluzione corretta prevede la definizione di un server distinto per
`example.org`:


```
server {
    listen       80;
    server_name  example.org;
    return       301 http://www.example.org$request_uri;
}

server {
    listen       80;
    server_name  www.example.org;
    ...
}
```



> **Note:** Nelle versioni antecedenti la 0.9.1, i redirect possono essere definiti con:

```
rewrite      ^ http://www.example.org$request_uri?;
```

Un altro esempio:
invece della logica "upside-down", vale a dire "tutto quello
che non e' `example.com` ne' `www.example.com`":


```
RewriteCond  %{HTTP_HOST}  !example.com
RewriteCond  %{HTTP_HOST}  !www.example.com
RewriteRule  (.*)          http://www.example.com$1
```


e' meglio semplicemente definire
`example.com`, `www.example.com`,
e "tutto il resto":


```
server {
    listen       80;
    server_name  example.com www.example.com;
    ...
}

server {
    listen       80 default_server;
    server_name  _;
    return       301 http://example.com$request_uri;
}
```



> **Note:** Nelle versioni antecedenti la 0.9.1, i redirect possono essere definiti con:

```
rewrite      ^ http://example.com$request_uri?;
```

## Conversione delle regole di Mongrel {#converting_mongrel_rules}

Regole di Mongrel tipiche, quali:


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


andrebbero convertite in:


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
