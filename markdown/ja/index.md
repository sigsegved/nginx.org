# nginx

**Language:** ja


nginx [えんじんえっくす] は [Igor Sysoev](http://sysoev.ru/en/) によって作られた HTTP とリバースプロキシのサーバで、メールプロキシサーバでもあります。[Rambler](http://www.rambler.ru)
([RamblerMedia.com](http://ramblermedia.com)) を含むロシアの多くの高負荷サイトで５年以上も動いています。Netcraft によると、nginx は [2010 年 4 月時点で 4.70%](http://news.netcraft.com/archives/2010/04/15/april_2010_web_server_survey.html) の人気サイトでサーバーとして、もしくはプロキシとして利用されています。成功例としては [FastMail.FM](http://blog.fastmail.fm/2007/01/04/webimappop-frontend-proxies-changed-to-nginx/) や
[Wordpress.com](http://barry.wordpress.com/2008/04/28/load-balancer-update/) があります。

ソースコードは [BSD 風の 2 箇条ライセンス](/LICENSE)でライセンスされています。

## 基本的な HTTP 機能 {#basic_http_features}

- スタティックなインデックスファイルの提供、自動インデクシング、オープンなファイルディスクリプタキャッシュ
- キャッシングで高速化されたリバースプロキシ、シンプルなロードバランシングとフォールトトレランス
- リモートの FastCGI サーバのキャッシングによる高速化サポート、シンプルなロードバランシングとフォールトトレランス
- モジュールアーキテクチャ。フィルタには gzip、バイトレンジ、チャンク化されたレスポンス、XSLT、SSI、画像リサイズフィルタが含まれます。FastCGI もしくはプロキシ化されたサーバなら、単一ページ内への複数 SSI 封入が並列で処理可能。
- SSL と TLS SNI サポート。

## 他の HTTP 機能 {#other_http_features}

- 名前ベースと IP ベースの仮想サーバ
- キープアライブとパイプライン接続のサポート
- 柔軟な設定
- クライアント処理を中断させること無く再構成、オンラインアップグレード
- アクセスログフォーマット、バッファされたログ書き込み、素早いログローテーション
- 3xx-5xx エラーコードのリダイレクト
- rewrite モジュール
- クライアントの IP アドレスをベースにしたアクセスコントロールと HTTP ベーシック認証
- PUT、DELETE、MKCOL、COPY、MOVE メソッド
- FLV ストリーミング
- 速度制限
- 同一アドレスからの同時接続もしくは同時リクエストの制限
- 埋め込み perl

## メールプロキシサーバ機能 {#mail_proxy_server_features}

- 外部の HTTP 認証サーバを利用した IMAP/POP3 バックエンドへのユーザリダイレクト
- 外部の HTTP 認証サーバと内部 SMTP バックエンドへの接続リダイレクトを利用したユーザ認証
- 認証メソッド:


- POP3: USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
- IMAP: LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
- SMTP: AUTH LOGIN/PLAIN/CRAM-MD5;
- SSL サポート
- STARTTLS と STLS のサポート

## アーキテクチャとスケーラビリティ {#architecture_and_scalability}

- 一つのマスタープロセスと複数のワーカープロセス。ワーカーは非特権ユーザとして動く
- 通知メソッド: kqueue (FreeBSD 4.1+)、epoll (Linux 2.6+)、rt シグナルs (Linux 2.2.19+)、/dev/poll (Solaris 7 11/99+)、イベントポート (Solaris 10)、select、poll
- EV_CLEAR, EV_DISABLE (イベントを一時的に無効にする)、 NOTE_LOWAT, EV_EOF、利用可能なデータの数、エラーコードを含む様々な kqueue 機能のサポート
- sendfile (FreeBSD 3.1+, Linux 2.2+, Mac OS X 10.5)、sendfile64 (Linux 2.4.21+)、sendfilev (Solaris 8 7/01+) のサポート
- ファイル AIO (FreeBSD 4.3+, Linux 2.6.22+)
- Accept-filters (FreeBSD 4.1+) と TCP_DEFER_ACCEPT (Linux 2.4+) のサポート
- 1 万の非アクティブな HTTP キープアライブ接続は約 2.5M のメモリーを使用
- データコピーの実施は最小に保たれる

## テスト済み OS とプラットフォーム {#tested_os_and_platforms}

- FreeBSD 3—8 / i386; FreeBSD 5—8 / amd64;
- Linux 2.2—2.6 / i386; Linux 2.6 / amd64;
- Solaris 9 / i386, sun4u; Solaris 10 / i386, amd64, sun4v;
- MacOS X / ppc, i386;
- Windows XP, Windows Server 2003.
