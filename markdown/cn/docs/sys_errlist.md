# 关于“sys_errlist is deprecated; use strerror or strerror_r instead”的提示

**Revision:** 1  
**Language:** cn


在Linux环境下编译nginx 0.7.66、0.8.35或更高版本时，会出现以下警告：


```
warning: `sys_errlist' is deprecated;
    use `strerror' or `strerror_r' instead
warning: `sys_nerr' is deprecated;
    use `strerror' or `strerror_r' instead
```


这属于正常情况：nginx必须在信号处理函数中使用过时的sys_errlist[]和sys_nerr，因为strerror()和strerror_r()是非异步信号安全的。
