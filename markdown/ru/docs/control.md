# Управление nginx

**Revision:** 7  
**Language:** ru

Управлять nginx можно с помощью сигналов. Номер главного процесса по умолчанию записывается в файл `/usr/local/nginx/logs/nginx.pid` . Изменить имя этого файла можно при конфигурации сборки или же в `nginx.conf` директивой [pid](ngx_core_module.xml#pid) . Главный процесс поддерживает следующие сигналы:

> **Note:** 

Управлять рабочими процессами по отдельности не нужно. Тем не менее, они тоже поддерживают некоторые сигналы:

> **Note:** 

# Изменение конфигурации {#reconfiguration}

Для того чтобы nginx перечитал файл конфигурации, нужно послать главному процессу сигнал HUP. Главный процесс сначала проверяет синтаксическую правильность конфигурации, а затем пытается применить новую конфигурацию, то есть, открыть лог-файлы и новые listen сокеты. Если ему это не удаётся, то он откатывает изменения и продолжает работать со старой конфигурацией. Если же удаётся, то он запускает новые рабочие процессы, а старым шлёт сообщение о плавном выходе. Старые рабочие процессы закрывают listen сокеты и продолжают обслуживать старых клиентов. После обслуживания всех клиентов старые рабочие процессы завершаются.

Предположим, на FreeBSD команда

```
ps axw -o pid,ppid,user,%cpu,vsz,wchan,command | egrep '(nginx|PID)'
```

показывает примерно такую картину:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
33127 33126 nobody   0.0  1380 kqread nginx: worker process (nginx)
33128 33126 nobody   0.0  1364 kqread nginx: worker process (nginx)
33129 33126 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

Если послать сигнал HUP главному процессу, то картина может быть такой:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33129 33126 nobody   0.0  1380 kqread nginx: worker process is shutting down (nginx)
33134 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33135 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33136 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
```

Один старый рабочий процесс 33129 всё ещё продолжает работать. По истечении некоторого времени он завершается:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33134 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33135 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33136 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
```

# Ротация лог-файлов {#logs}

Лог-файлы нужно переименовать, а затем послать сигнал USR1 главному процессу. Он откроет заново все текущие открытые файлы и назначит им в качестве владельца непривилегированного пользователя, под которым работают рабочие процессы. После успешного открытия главный процесс закрывает все открытые файлы и посылает сообщение о переоткрытии файлов рабочим процессам. Они также открывают новые файлы и сразу же закрывают старые. В результате старые файлы практически сразу же готовы для дальнейшей обработки, например, их можно сжимать.

# Обновление исполняемого файла на лету {#upgrade}

Для обновления исполняемого файла сервера вначале нужно записать на место старого файла новый. Затем нужно послать сигнал USR2 главному процессу—он переименует свой файл с номером процесса в файл с суффиксом `.oldbin` , например, `/usr/local/nginx/logs/nginx.pid.oldbin` , после чего запустит новый исполняемый файл, а тот в свою очередь—свои рабочие процессы:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33134 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33135 33126 nobody   0.0  1380 kqread nginx: worker process (nginx)
33136 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
36264 33126 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

Теперь все рабочие процессы наравне принимают запросы. Если послать сигнал WINCH первому главному процессу, то он пошлёт своим рабочим процессам сообщение о плавном выходе, и они будут постепенно выходить:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33135 33126 nobody   0.0  1380 kqread nginx: worker process is shutting down (nginx)
36264 33126 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

По истечении времени запросы будут обрабатывать только новые рабочие процессы:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
36264 33126 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

Нужно заметить, что старый процесс не закрывает свои listen сокеты и при необходимости ему можно сказать, чтобы он снова запустил свои рабочие процессы. Если работа нового исполняемого файла по каким-то причинам не устраивает, можно проделать одно из следующих действий:

  Послать старому главному процессу сигнал HUP. Старый главный процесс, не перечитывая конфигурации, запустит новые рабочие процессы. После этого можно плавно завершить все новые процессы, послав новому главному процессу сигнал QUIT.

  Послать новому главному процессу сигнал TERM. В ответ на это он пошлёт сообщение о немедленном выходе своим рабочим процессам, и все они практически сразу же завершатся. (Если новые процессы по каким-то причинам не завершаются, нужно послать им сигнал KILL, который заставит их завершиться.) По завершению нового главного процесса старый главный процесс автоматически запустит новые рабочие процессы.

Если новый главный процесс выходит, то старый главный процесс убирает суффикс `.oldbin` из имени файла с номером процесса.

Если же обновление прошло удачно, то старому процессу нужно послать сигнал QUIT, и останутся только новые процессы:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
36264     1 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

