# デバッギングログ

**Language:** ja

デバッギングログを有効にするには、nginx をデバッグオプションを付けて設定する必要があります:

```
./configure --with-debug ...
```

次に `error_log` の `debug` レベルをセットします:

```
error_log  /path/to/log  debug;
```

nginx の Windows バイナリバージョンでは常にデバッグログモードがサポートされてビルドされているので、 `debug` レベルをセットするだけです。

別のレベル、例えば *server* レベルでログを定義するとそのサーバでのデバッギングログが無効になりますので注意してください:

```
error_log  /path/to/log  debug;

http {
    server {
        error_log  /path/to/log;
        ...
```

このサーバログをコメントアウトするか `debug` フラグを追加してください:

```
error_log  /path/to/log  debug;

http {
    server {
        error_log  /path/to/log  debug;
        ...
```

また、特定のアドレスだけデバッギングログを有効にすることもできます:

```
error_log  /path/to/log;

events {
    debug_connection   192.168.1.1;
    debug_connection   192.168.10.0/24;
}
```

