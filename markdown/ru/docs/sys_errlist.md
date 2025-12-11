# Сообщение sys_errlist                 is deprecated;                 use strerror or strerror_r                 instead

**Revision:** 1  
**Language:** ru


При сборке nginx версий 0.7.66, 0.8.35 и выше на Linux
выводится предупреждение:


```
warning: `sys_errlist' is deprecated;
    use `strerror' or `strerror_r' instead
warning: `sys_nerr' is deprecated;
    use `strerror' or `strerror_r' instead
```


Это нормально: nginx вынужден использовать устаревшие
sys_errlist[] и sys_nerr в обработчиках сигналов, потому
что функции strerror() и strerror_r() не являются Async-Signal-Safe,
и их нельзя использовать в обработчиках сигналов.
