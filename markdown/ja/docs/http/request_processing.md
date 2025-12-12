# nginx はどのようにリクエストを処理するか

**Author:** Igor Sysoev  
**Translator:** DigitalCube Co. Ltd., wokamoto  
**Language:** ja

# 名前ベースの仮想サーバ

nginx はまず最初にどの *サーバ* がそのリクエストを処理すべきなのかを決定します。手はじめに、３つすべての仮想サーバが port *:80 で待ち受けている単純な設定から見てみましょう:

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

この設定では nginx は、（ブラウザからの）HTTP リクエストの "Host" ヘッダだけを考査して、そのリクエストをどのサーバに振り向けるべきかを決定します。もし "Host" ヘッダがどのサーバ名ともマッチしない場合、またはリクエストにこのフィールドがまったく含まれていない場合は、nginxはこのリクエストをデフォルトサーバに振り向けます。上記の設定ではデフォルトサーバは最初のもので、これは nginx の標準的なデフォルトの挙動です。設定内の最初のサーバをデフォルトサーバにしたくない場合は、 `listen` ディレクティブに `default_server` パラメータを使って明示的に設定することができます:

```
server {
    listen       80  default_server;
    server_name  example.net  www.example.net;
    ...
}
```

> **Note:** この `default_server` パラメータはバージョン 0.8.21 以上で利用できます。それ以前のバージョンでは代わりに `default` パラメータを使用してください。

このデフォルトサーバは `listen` ディレクティブのプロパティで、 `server_name` ディレクティブのプロパティではないことに注意してください。詳細は後述します。

# サーバ名未定義のリクエストの処理を防ぐ {#how_to_prevent_undefined_server_names}

"Host" ヘッダが未定義のリクエストを処理させたくない場合は、リクエストを単にドロップさせるデフォルトサーバを設定できます:

```
server {
    listen       80  default_server;
    server_name  _;
    return       444;
}
```

ここでは存在しないドメイン名 “_” をサーバ名として選択し、接続を閉じる nginx の特別な標準外コード 444 を返します。このサーバ用にサーバ名を設定しなければならないことに注意してください。さもなければ nginx は *ホスト名* を使用します。

# 名前ベースとIPベースをミックスした仮想サーバ {#mixed_name_ip_based_servers}

異なるアドレスで待ち受けている仮想サーバのより複雑な設定をみてみましょう:

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

この設定では、nginx はまず最初に `server` ブロックの `listen` ディレクティブに対してリクエストの IP アドレスとポートを考査します。次に、その IP アドレスとポートにマッチする `server` ブロックの `server_name` ディレクティブに対して、その HTTP リクエストの "Host" ヘッダを考査します。 もしサーバ名が見つからなければ、そのリクエストはデフォルトサーバによって処理されます。例えば、192.168.1.1:80 ポートで受信された `www.example.com` へのリクエストは 192.168.1.1:80 ポートのデフォルトサーバ、つまり最初のサーバで処理されます。これはこのポートでは `www.example.com` は定義されていないからです。

すでに述べたように、デフォルトサーバは `listen` ディレクティブのプロパティで、別の `listen` ディレクティブには別のデフォルトサーバが定義されています:

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

# 単純な PHP サイトの設定 {#simple_php_site_configuration}

では、典型的で単純な PHP サイトで nginx がどのように *ロケーション（location）* を選択してリクエストを処理するのかを見てみましょう:

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

nginx はまず最初に、リストの順序には関係なくリテラルな文字列によって指定されているもっとも限定されたロケーションを検索します。上記の設定では唯一のリテラルなロケーションは `/` であり、したがってどのリクエストでもマッチして最終的にこのロケーションが使われます。次に nginx は、設定ファイルにリストされている順番で正規表現によって指定されているロケーションをチェックします。最初にマッチした正規表現で検索はストップし、 nginx そのロケーションを使用します。もしどの正規表現もリクエストにマッチしない場合は、nginx はその前に見つかったもっとも限定されたリテラルなロケーションを使用します。

すべてのタイプのロケーションはクエリー部分を除いたリクエスト URI 部分のみを考査することに注意してください。これはクエリー文字列の引数がいろいろな方法で渡されることがあるためです。例えば:

```
/index.php?user=john&page=1
/index.php?page=1&user=john
```

さらに、クエリー文字列ではどのようなリクエストでも可能だからです:

```
/index.php?page=1&something+else&user=john
```

では、上記の設定ではどのようにリクエストが処理されるのかを見てみましょう:

  リクエスト `/logo.gif` はリテラルなロケーション `/` に最初にマッチし、次に正規表現 `\.(gif|jpg|png)$` にマッチするので、後者のロケーションによって処理されます。 このリクエストは `root /data/www` ディレクティブを使用してファイル `/data/www/logo.gif` にマップされ、このファイルがクライアントに送られます。

  リクエスト `/index.php` もまたリテラルなロケーション `/` に最初にマッチし、次に正規表現 `\.(php)$` にマッチします。したがって、このリクエストは後者のロケーションによって処理され、localhost:9000 で待ち受けている FastCGI サーバに渡されます。 `fastcgi_param` ディレクティブは FastCGI のパラメータ SCRIPT_FILENAME を `/data/www/index.php` にセットし、この FastCGI サーバがこのファイルを実行します。変数 $document_root は `root` ディレクティブの値と同等で、変数 $fastcgi_script_name はリクエスト URI、例えば `/index.php` と同等です。

  リクエスト `/about.html` はリテラルなロケーション `/` のみにマッチします。したがってこのロケーションで処理されます。このリクエストは `root` ディレクティブのパラメータ `/data/www` を使い、ファイル `/data/www/about.html` にマップされ、クライアントに送られます。

  リクエスト `/` の処理はより複雑です。これはリテラルなロケーション `/` のみにマッチし、このロケーションで処理されます。ついで `index` ディレクティブがパラメータと `root` ディレクティブのパラメータ `/data/www` にしたがって index ファイルが存在するかどうかを考査します。もし `/data/www/index.php` ファイル存在すればこのディレクティブは `/index.php` への内部リダイレクトを実行し、nginx はまるでこのリクエストがクライアントに送られたかのようにこのロケーションを再び検索します。先に見たように、リダイレクトされたリクエストは最終的に FastCGI サーバで処理されます。

