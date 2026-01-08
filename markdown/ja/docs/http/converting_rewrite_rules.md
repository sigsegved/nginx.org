# rewrite ルールのコンバート

**Language:** ja

# メインサイトへのリダイレクト

共有のホスティングで Apache の .htaccess ファイル *のみ* で *すべて* を設定してきたのなら、次のようにルールをコンバートします:

```
RewriteCond  %{HTTP_HOST}  example.org
RewriteRule  (.*)          http://www.example.org$1
```

上記は下記のようになります:

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

これは間違っていて面倒で非効率的な方法です。正しい方法は `example.org` 用に別のサーバを定義します:

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

別の例として、 `example.com` 以外と `www.example.com` 以外のすべて、という後方ロジックの代わりの例です:

```
RewriteCond  %{HTTP_HOST}  !example.com
RewriteCond  %{HTTP_HOST}  !www.example.com
RewriteRule  (.*)          http://www.example.com$1
```

この場合、単に `example.com` 、 `www.example.com` 、そしてそれ以外を定義します:

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

# Mongrel ルールのコンバート {#converting_mongrel_rules}

典型的な Mongrel のルール:

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

上記は次のようにコンバートされます

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

