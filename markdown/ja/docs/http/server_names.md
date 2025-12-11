# サーバ名

**Author:** Igor Sysoev  
**Translator:** DigitalCube Co. Ltd., wokamoto  
**Language:** ja


サーバ名は `server_name` ディレクティブを使用して定義され、リクエストに対してどのサーバブロックが使われるかを決定します。「[request_processing.html](request_processing.html)」もお読みください。これらは完全一致名、ワイルドカード名、正規表現で定義されます:


```
server {
    listen       80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       80;
    server_name  *.example.org;
    ...
}

server {
    listen       80;
    server_name  mail.*;
    ...
}

server {
    listen       80;
    server_name  ~^(?<user>.+)\.example\.net$;
    ...
}
```


サーバ名は次の順序で考査されます:


1. 完全一致名
2. アスタリスクで始まるワイルドカード名: `*.example.org`
3. アスタリスクで終わるワイルドカード名: `mail.*`
4. 設定ファイル内の順序での正規表現

最初にマッチしたところで検索は終了します。.

## ワイルドカード名 {#wildcard_names}

ワイルドカード名にはそのサーバ名の最初か最後のみ、そしてドットに隣接したところのみにアスタリスクが含まれます。サーバ名 `www.*.example.org` や `w*.example.org` は無効です。しかし、これらのサーバ名は正規表現を使用して、例えば  `~^www\..+\.example\.org$` や `~^w.*\.example\.org$` として指定することができます。アスタリスクは複数部分にマッチさせることができます。`*.example.org` は `www.example.org` だけでなく `www.sub.example.org` にもマッチします。

特別なワイルドカードの形式 `.example.org` は、完全一致名 `example.org` とワイルドカード名 `*.example.org` の両方にマッチさせるように利用できます。

## 正規表現名 {#regex_names}

nginx で使用される正規表現は Perl プログラミング言語（PCRE）で使用されているものと互換性があります。正規表現を使用するには、サーバ名を必ずチルダで始めます:


```
server_name  ~^www\d+\.example\.net$;
```


チルダで始まっていないと完全一致名として、またはその正規表現にアスタリスクが含まれている場合はワイルドカード名として（そしてたいていの場合は無効なものとして）扱われてしまいます。"^" と "$" アンカーをセットし忘れないようにしてください。これらは構文的には必須ではありませんが論理的に必須です。また、ドメイン名のドットはバックスラッシュで必ずエスケープしてください。"{" と "}" 文字を含む正規表現は必ずダブルクォーテーションで囲ってください:


```
server_name  "~^(?<name>\w\d{1,3}+)\.example\.net$";
```


さもないと、nginx は起動に失敗し次のエラーメッセージを表示します:


```
directive "server_name" is not terminated by ";" in ...
```


正規表現の名前付きキャプチャは変数としてその後で使用されます:


```
server {
    server_name   ~^(www\.)?(?<domain>.+)$;

    location / {
        root   /sites/$domain;
    }
}
```


PCRE ライブラリは次の構文を使用した名前付きキャプチャをサポートしています:


| `?<name>` | Perl 5.10 互換構文、PCRE-7.0 よりサポート |
| --- | --- |
| `?'name'` | Perl 5.10 互換構文、PCRE-7.0 よりサポート |
| `?P<name>` | Python 互換構文、PCRE-4.0よりサポート |


nginx が起動に失敗すると次のエラーメッセージを表示します:


```
pcre_compile() failed: unrecognized character after (?< in ...
```


これは PCRE ライブラリが古いので `?P<name>` 構文を試すように、という意味です。このキャプチャは数字形式でも使用できます:


```
server {
    server_name   ~^(www\.)?(.+)$;

    location / {
        root   /sites/$2;
    }
}
```


とはいえ、数字形式は簡単に上書きすることができるため、このような使用法は（上記のような）単純なケースに限るべきです。

## その他のサーバ名 {#miscellaneous_names}

デフォルトではないサーバブロックで "Host" ヘッダ無しのリクエストを処理させたい場合は、空のサーバ名を指定します:


```
server {
    listen       80;
    server_name  example.org  www.example.org  "";
    ...
}
```

`server_name` がサーバブロックで定義されていない場合は、nginx は*サーバ名*として空の名前を使用します。

> **Note:** nginx のバージョン 0.8.48 までは、このような場合はサーバ名としてホスト名を使用していました。

サーバ名ではなく IP アドレスを使用したリクエストが送られてきた場合、そのリクエストの "Host" ヘッダには IP アドレスが含まれているので、その IP アドレスをサーバ名として利用してそのリクエストを処理できます:


```
server {
    listen       80;
    server_name  example.org
                 www.example.org
                 ""
                 192.168.1.1
                 ;
    ...
}
```

すべてのサーバに適合させる例では奇妙なサーバ名 "_" が使われます:


```
server {
    listen       80  default_server;
    server_name  _;
    return       444;
}
```


このサーバ名に特別なところはありません。単にどのサーバ名とも決してマッチしない無数の無効なドメイン名のひとつです。したがって、 "--"、"!@#" なども同様な結果を得られます。

nginx バージョン 0.6.25 までは特別なサーバ名 "*" をサポートしていて、これは誤ってすべてのサーバ名と一致するもの（キャッチオール名）として解釈されていました。この特別なサーバ名 "*"はキャッチオールまたはワイルドカードとして機能したことはありませんでした。代わりに、今は `server_name_in_redirect` ディレクティブによって提供されている機能の役を果たしていました。特別なサーバ名 "*" は今後廃止予定ですので、`server_name_in_redirect` ディレクティブを使うようにしてください。キャッチオール名を指定したり `server_name` ディレクティブを使用した*デフォルト*サーバを指定したりする方法はないことに注意してください。これは `listen` ディレクティブのプロパティであり、`server_name` ディレクティブのプロパティではありません。"[request_processing.html](request_processing.html)" も参照してください。
ポート *:80 と *:8080 で待ち受けているサーバを定義し、ひとつをポート *:8080 のデフォルトサーバへ、もうひとつをポート *:80 のデフォルトサーバへ振り向けることができます。


```
server {
    listen       80;
    listen       8080  default_server;
    server_name  example.net;
    ...
}

server {
    listen       80  default_server;
    listen       8080;
    server_name  example.org;
    ...
}
```

## 最適化 {#optimization}

完全一致名とワイルドカード名はハッシュで保存されます。このハッシュは待ち受けポートに結び付けられ、各待ち受けポートは、完全一致名のハッシュ、アスタリスクで始まるワイルドカード名のハッシュ、アスタリスクで終わるワイルドカード名のハッシュの３つまでのハッシュを持つことができます。ハッシュのサイズは構成フェーズで最適化されるので、CPU キャッシュのミスは最低でもサーバ名を見つけることができます。最初に完全一致名のハッシュが検索されます。完全一致名のハッシュを使って見つからなければ、次にアスタリスクで始まるワイルドカード名のハッシュが検索されます。さらにまだ見つからなければ、アスタリスクで終わるワイルドカード名のハッシュが検索されます。ワイルドカード名のハッシュの検索は完全一致名のハッシュの検索よりも遅くなります。これはサーバ名の検索がドメイン部分によって検索されるからです。特別なワイルドカード形式の `.example.org` は完全一致名のハッシュではなくワイルドカード名のハッシュで保存されます。正規表現は順番に考査されるので、これがもっとも遅い方式ですし、非スケーラブルでもあります。

これらの理由から、可能な場合は完全一致名を利用するのがよいでしょう。例えば、もっとも頻繁にリクエストされるサーバ名が `example.org` と `www.example.org` だとすると、これらを明示的に定義するとより効率的です:


```
server {
    listen       80;
    server_name  example.org  www.example.org  *.example.org;
    ...
}
```


上記は次の単純化された形式を使用するよりも効率的です:


```
server {
    listen       80;
    server_name  .example.org;
    ...
}
```

たくさんの数のサーバ名を定義したり非常に長いサーバ名を定義したりする場合は、http レベルの `server_names_hash_max_size` と `server_names_hash_bucket_size` ディレクティブを調整する必要があるかもしれません。`server_names_hash_bucket_size` のデフォルト値は 32、もしくは 64、あるいはお使いの CPU キャッシュラインのサイズによってはその他の値になっているかもしれません。もしデフォルト値が 32 でサーバ名として "too.long.server.name.example.org" のような非常に長いサーバ名を定義している場合、nginx は起動に失敗し、次のエラーメッセージを表示させます:


```
could not build the server_names_hash,
you should increase server_names_hash_bucket_size: 32
```


この場合、このディレクティブの値を次の 2 の累乗にセットします:


```
http {
    server_names_hash_bucket_size  64;
    ...
```


非常にたくさんの数のサーバ名を定義した場合は次のエラーメッセージが表示されます:


```
could not build the server_names_hash,
you should increase either server_names_hash_max_size: 512
or server_names_hash_bucket_size: 32
```


まず最初に `server_names_hash_max_size` の値を、定義するサーバ名の数に近い数に設定して試します。この設定がうまくいかない時だけ、もしくは nginx の起動時間が許容できないほど長い場合だけ `server_names_hash_bucket_size` の値を増やしてみます。

待ち受けているポートがひとつだけでサーバもひとつだけの場合、nginx はサーバ名を考査しません（また、待ち受けポート用のハッシュも生成しません）。しかし一つ例外があります。`server_name` がキャプチャを伴った正規表現の場合、nginx はキャプチャを取得するためにこの正規表現を実行します。

## 互換性 {#compatibility}

- 0.8.48 以降、デフォルトのサーバ名の値は空の名前 "" です。
- 正規表現サーバ名の名前付きキャプチャのサポートは 0.8.25 からです。
- 正規表現サーバ名のキャプチャのサポートは 0.7.40 からです。
- 空のサーバ名 "" のサポートは 0.7.12 からです。
- ワイルドカードサーバ名と正規表現の最初のサーバ名としての使用は0.6.25 からサポートされています。
- 正規表現サーバ名のサポートは 0.6.7 からです。
- ワイルドカードの形式 `example.*` のサポートは 0.6.0 からです。
- 特別な形式 `.example.org` のサポートは 0.3.18 からです。
- ワイルドカードの形式 `*.example.org` のサポートは 0.1.13 からです。
