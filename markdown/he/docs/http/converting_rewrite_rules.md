# המרת כללי rewrite

**Author:** Igor Sysoev  
**Translator:** מבזקים.נט  
**Language:** he

# הפנייה לאתר ראשי

משתמשים שבמהלך חיי האירוח המשותף נהגו להגדיר *הכל* באמצעות שימוש *רק* בקובצי htaccess. של Apache, יתרגמו בדרך כלל את הכללים הבאים:

```
RewriteCond  %{HTTP_HOST}  example.org
RewriteRule  (.*)          http://www.example.org$1
```

למשהו כזה:

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

צורה זו היא שגוייה, מסובכת, ולא יעילה. הדרך הנכונה היא להגדיר שרת נפרד עבור `example.org` :

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

דוגמה נוספת, במקום הגיון הפוך: כל מה שהוא לא `example.com` וגם לא `www.example.com` :

```
RewriteCond  %{HTTP_HOST}  !example.com
RewriteCond  %{HTTP_HOST}  !www.example.com
RewriteRule  (.*)          http://www.example.com$1
```

עלייך רק להגדיר את `example.com` , `www.example.com` , וכל דבר אחר:

```
server {
    listen       80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       80 default_server;
    server_name  _;
    rewrite   ^  http://example.org$request_uri?;
}
```

# המרת כללי Mongrel {#converting_mongrel_rules}

כללי Mongrel טיפוסיים:

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

יש להמיר כך

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

