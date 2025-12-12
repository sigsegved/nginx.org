# Модуль ngx_stream_split_clients_module

**Revision:** 2  
**Language:** ru

Модуль `ngx_stream_split_clients_module` (1.11.3) создаёт переменные для A/B тестирования (также известного как “split-тестирование”).

# Пример конфигурации {#example}

```
stream {
    ...
    split_clients "${remote_addr}AAA" $upstream {
                  0.5%                feature_test1;
                  2.0%                feature_test2;
                  *                   production;
    }

    server {
        ...
        proxy_pass $upstream;
    }
}
```

# Директивы {#directives}

## split_clients

```
Syntax:  строка $переменная
Default: 
Context: stream
```

Создаёт переменную для A/B тестирования, например:

```
split_clients "${remote_addr}AAA" $variant {
               0.5%               .one;
               2.0%               .two;
               *                  "";
}
```

Значение исходной строки хэшируется с помощью MurmurHash2. В приведённом примере при значениях хэша от 0 до 21474835 (0.5%) переменная `$variant` получит значение `".one"` . При значениях хэша от 21474836 до 107374180 (2%) — `".two"` . И при значениях хэша от 107374181 до 4294967295 — `""` (пустая строка).

