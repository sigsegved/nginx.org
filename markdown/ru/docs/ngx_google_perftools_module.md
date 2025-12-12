# Модуль ngx_google_perftools_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_google_perftools_module` (0.6.29) включает поддержку профилирования рабочих процессов nginx при помощи [Google Performance Tools](https://github.com/gperftools/gperftools) . Модуль предназначен для разработчиков nginx.

По умолчанию этот модуль не собирается, его сборку необходимо разрешить с помощью конфигурационного параметра `--with-google_perftools_module` .

> **Note:** Для сборки и работы этого модуля нужна библиотека [gperftools](https://github.com/gperftools/gperftools) .

# Пример конфигурации {#example}

```
google_perftools_profiles /path/to/profile;
```

Профили будут сохраняться как `/path/to/profile.<worker_pid>` .

# Директивы {#directives}

## google_perftools_profiles

```
Syntax:  файл
Default: 
Context: main
```

Задаёт имя файла, который хранит информацию о профилировании рабочего процесса nginx. Идентификатор рабочего процесса всегда является частью имени файла и добавляется в конце имени после точки.

