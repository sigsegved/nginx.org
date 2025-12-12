# Controllo di nginx

**Translator:** Angelo Papadia  
**Revision:** 5  
**Language:** it

nginx puo' essere controllato tramite segnali. L'ID del processo master e' scritto per default nel file `/usr/local/nginx/logs/nginx.pid` . E' possibile utilizzare un altro file utilizzando la direttiva [pid](ngx_core_module.xml#pid) , definendola all'avvio oppure in `nginx.conf` . Il processo master riconosce i seguenti segnali:

> **Note:** 

E' anche possibile controllare ciascun processo worker, per quanto cio' non sia richiesto. I segnali riconosciuti sono:

> **Note:** 

# Cambio della configurazione {#reconfiguration}

Per far rileggere la configurazione a nginx, bisogna inviare un segnale HUP al processo master. Tale processo per prima cosa verifica la validita' sintattica della nuova configurazione, quindi tenta di applicarla, vale a dire di aprire i file di log e i nuovi socket di ascolto. In caso di fallimento, annulla i cambiamenti e continua a lavorare con la vecchia configurazione. Invece, in caso di successo, avvia nuovi processi worker e invia a quelli vecchi appositi segnali per chiederne l'arresto controllato. I vecchi processi chiudono i socket di ascolto, ma continuano il servizio per i vecchi client. Quanto tutti i vecchi client sono stati servizi, i vecchi processi worker terminano.

Di seguito si illustra con un esempio. Si immagini che nginx sia in esecuzione su FreeBSD 4.x e che il comando

```
ps axw -o pid,ppid,user,%cpu,vsz,wchan,command | egrep '(nginx|PID)'
```

produca il seguente risultato:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
33127 33126 nobody   0.0  1380 kqread nginx: worker process (nginx)
33128 33126 nobody   0.0  1364 kqread nginx: worker process (nginx)
33129 33126 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

Se al processo master si invia il segnale HUP, si ottiene:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33129 33126 nobody   0.0  1380 kqread nginx: worker process is shutting down (nginx)
33134 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33135 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33136 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
```

Uno dei vecchi processi worker con PID 33129 continua ad essere attivo; dopo un po', esce:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33134 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33135 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
33136 33126 nobody   0.0  1368 kqread nginx: worker process (nginx)
```

# Rotazione dei file di log {#logs}

Per poter ruotare i file di log, e' prima necessario cambiare loro il nome, quindi bisogna inviare il segnale USR1 al processo master, il quale provvede a riaprire tutti i file di log correnti e ad assegnarli all'utente non privilegiato sotto i quali sono in esecuzione i processi worker. Dopo aver riaperto con successo i file, il processo master chiude tutti i file aperti, ed invia un messaggio ai processi worker per chiedere loro di riaprire i file; i processi worker provvedono quindi immediatamente ad aprire i nuovi file ed a chiudere i vecchi. Come risultato, i vecchi file sono quasi immediatamente disponibili per eventuali attivita' successive, ad esempio per la compressione.

# Aggiornamento al volo del file eseguibile {#upgrade}

Per poter aggiornare l'eseguibile del server, prima e' necessario porre il nuovo file al posto del vecchio; dopo, bisogna inviare al processo master il segnale USR2. Il processo master provvede a rinominare il file contenente il proprio ID di processo, aggiungendo il suffisso `.oldbin` , ad esempio `/usr/local/nginx/logs/nginx.pid.oldbin` , quindi avvia un nuovo file eseguibile, che a sua volta fa partire i propri processi worker:

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

A questo punto, sia i processi worker relativi al vecchio eseguibile, sia quelli relativi al nuovo, accettano richieste. Se al processo master e' inviato il segnale WINCH, tutti i relativi processi worker ricevono a loro volta un segnale che chiede loro l'arresto controllato, e quindi iniziano a spegnersi:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
33135 33126 nobody   0.0  1380 kqread nginx: worker process is shutting down (nginx)
36264 33126 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

> **Note:** Quando su Linux si usa il metodo "rtsig", i nuovi processi potrebbero non
accettare connessioni anche dopo che al processo master vecchio e' stato
inviato il segnale WINCH.
In tal caso, bisogna continuare ad inviare il segnale USR1 al nuovo processo
master, sinche' i nuovi processi iniziano ad accettare connessioni.

In breve, i soli processi worker a processare le richieste saranno quelli nuovi:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
33126     1 root     0.0  1164 pause  nginx: master process /usr/local/nginx/sbin/nginx
36264 33126 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

Si noti che il vecchio processo master non chiude i suoi socket di ascolto, e che se necessario e' possibile chiedergli di riavviare i propri processi worker. Se per qualche ragione il nuovo file eseguibile non lavora correttamente, e' possibile procedere in due modi:

  inviare il segnale HUP al vecchio processo master. Il vecchio processo master provvedera' ad avviare nuovi processi worker, senza rileggere la configurazione. A questo punto, tutti i nuovi processi possono essere fermati in maniera controllata, inviando il segnale QUIT al nuovo processo master.

  inviare il segnale TERM al nuovo processo master. Tale processo inviare a sua volta un messaggio ai suoi processi worker che causera' la loro chiusura immediata. (Se per qualche ragione i nuovi processi non terminano, e' possibile inviare loro il segnale KILL per forzarne la chiusura.) Quando il nuovo processo master si e' chiuso, il vecchio processo master provvedera' immediatamente ad avviare nuovi processi worker.

Se il nuovo processo master termina, allora in vecchio processo master provvede a cancellare il suffisso `.oldbin` dal nome del file contenente l'ID del processo.

Se l'aggiornamento ha successo, al vecchio processo master dovrebbe essere inviato il segnale QUIT, in maniera che rimangano solo i processi nuovi:

```
  PID  PPID USER    %CPU   VSZ WCHAN  COMMAND
36264     1 root     0.0  1148 pause  nginx: master process /usr/local/nginx/sbin/nginx
36265 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36266 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
36267 36264 nobody   0.0  1364 kqread nginx: worker process (nginx)
```

