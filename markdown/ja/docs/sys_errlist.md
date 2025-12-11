# メッセージ sys_errlist                 is deprecated;                 use strerror or strerror_r                 instead

**Language:** ja


nginx のバージョン 0.7.66、0.8.35、もしくはそれ以上を Linux でビルド中、次の警告メッセージが出ます:


```
warning: `sys_errlist' is deprecated;
    use `strerror' or `strerror_r' instead
warning: `sys_nerr' is deprecated;
    use `strerror' or `strerror_r' instead
```


これは正常です。strerror() と strerror_r() 関数が非同期シグナルセーフではないので、nginx はシングルハンドラの中で非推奨の sys_errlist[] と sys_nerr を使う必要があります。
