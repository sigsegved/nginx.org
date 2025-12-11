# nginx per Windows

**Translator:** Angelo Papadia  
**Revision:** 2  
**Language:** it


La versione di nginx per Windows usa le API native Win32, e non il layer di
emulazione Cygwin.
Attualmente e' usato solo il metodo di connessione select,
per cui non e' possibile attendersi prestazioni e scalabilita' eccellenti;
per tale ragione, e anche per altre, quella per Windows e'
considerata una versione *beta*.
Al momento risultano implementate piu' o meno le stesse funzionalita' della
versione di nginx per UNIX, con l'eccezione del filtro XSLT, del filtro immagini,
del modulo GeoIP, e del linguaggio Perl embedded.

Per installare nginx/Windows, e' bene [scaricare](../download.html)
l'ultima distribuzione disponibile della versione mainline (),
che contiene le correzioni piu' recenti.
Bisogna scompattare la distribuzione, spostarsi nella directory
nginx- e lanciare `nginx`.
Segue un esempio in cui la directory e' sul drive C: :


```
cd c:\
unzip nginx-.zip
cd nginx-
start nginx
```


Avviare l'utility a linea di comando `tasklist`
per vedere i processi nginx:


```
C:\nginx->tasklist /fi "imagename eq nginx.exe"

Image Name           PID Session Name     Session#    Mem Usage
=============== ======== ============== ========== ============
nginx.exe            652 Console                 0      2 780 K
nginx.exe           1332 Console                 0      3 112 K
```


Uno dei due e' il processo master, l'altro il processo worker.
Se nginx non si avvia, verificarne la ragione nel file di log
degli errori `logs\error.log` ;
se tale file non e' stato creato, la ragione dovrebbe essere riportata
nel Windows Event Log.
Se viene mostrata una pagina di errore invece della pagina attesa,
verificarne la ragione nel solito file `logs\error.log` .

nginx/Windows utilizza la directory in cui e' stato avviato come prefisso
per i path relativi della configurazione.
Nell'esempio precedente, il prefisso e'
`C:\nginx-\` .
I path nei file di configurazione devono essere specificati usando gli
slash del formato UNIX:


```
access_log   logs/site.log;
root         C:/web/html;
```

nginx/Windows e' eseguito come una normale applicazione di console e
non come un servizio, e puo' essere gestito con i comandi seguenti:


| nginx -s stop | arresto rapido |
| --- | --- |
| nginx -s quit | arresto controllato |
| nginx -s reload | ricaricamento della configurazione,
con avvio di un nuovo processo worker con la nuova configurazione,
ed arresto controllato del vecchio processo worker. |
| nginx -s reopen | riapertura dei file di log |

## Problemi noti {#known_issues}

- Nonostante sia possibile avviare diversi worker, in effetti
solo uno di essi esegue tutto il lavoro.
- Un worker puo' gestire non piu' di 1024 connessioni simultanee.
- La cache, ed altri moduli che richiedono il supporto alla memoria condivisa,
non funzionano su Windows Vista e versioni successive, in quanto su tali
versioni e' in uso la address space layout randomization.

## Possibili sviluppi futuri {#possible_future_enhancements}

- L'esecuzione come servizio.
- L'uso di I/O completion port come metodo di processo delle connessioni.
- L'uso di piu' thread worker all'interno di un singolo processo worker.
