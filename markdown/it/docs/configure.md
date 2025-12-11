# Compilare i sorgenti di nginx

**Translator:** Angelo Papadia  
**Revision:** 4  
**Language:** it


La compilazione si configura tramite il comando `configure`,
che definisce vari aspetti del sistema, fra cui i metodi che nginx puo'
usare per processare le connessioni; alla fine viene creato un `Makefile`.
Il comando `configure` supporta, fra gli altri, i seguenti parametri:

- --prefix=path—
definisce la directory che conterra' i file del server.
La medesima directory sara' pure usata per tutti i path relativi
definiti da configure (a parte i path ai sorgenti
delle librerie) e nel file di configurazione nginx.conf.
Per default vale /usr/local/nginx.
- --sbin-path=path—
stabilisce il nome del file eseguibile di nginx.
Tale valore e' usato solo nel corso dell'installazione.
Per default il file eseguibile e' chiamato
prefix/sbin/nginx.
- --conf-path=path—
stabilisce il nome del file di configurazione nginx.conf.
In ogni caso, nginx puo' sempre essere avviato con un file di
configurazione differente, specificando quest'ultimo tramite il parametro
a linea di comando -c file.
Per default il file di configurazione e'
prefix/conf/nginx.conf.
- --pid-path=path—
stabilisce il nome del file nginx.pid in cui e' registrato l'ID
del processo principale.
Dopo l'installazione, il nome del file puo' sempre essere modificato
tramite la direttiva 
del file di configurazione nginx.conf.
Per default il file contenente il pid e'
prefix/logs/nginx.pid.
- --error-log-path=path—
stabilisce il nome del principale file di diagnostica in cui sono
registrati gli errori e gli avvisi.
Dopo l'installazione, il nome del file puo' sempre essere modificato
tramite la direttiva 
del file di configurazione nginx.conf.
Per default il file degli errori e'
prefix/logs/error.log.
- --http-log-path=path—
stabilisce il nome del principale file di log delle richieste
al server HTTP.
Dopo l'installazione, il nome del file puo' sempre essere modificato tramite
la direttiva 
del file di configurazione nginx.conf.
Per default il file di log delle richieste e'
prefix/logs/access.log.
- --user=name—
stabilisce il nome di un utente non privilegiato le cui credenziali saranno
usate dai processi worker.
Dopo l'installazione, l'utente puo' sempre essere modificato tramite
la direttiva 
del file di configurazione nginx.conf.
L'utente di default e' nobody.
- --group=name—
stabilisce il nome di un gruppo le cui credenziali saranno
usate dai processi worker.
Dopo l'installazione, il gruppo puo' sempre essere modificato tramite
la direttiva 
del file di configurazione nginx.conf.
Per default il gruppo e scelto fra uno di quelli degli utenti non priviliegiati.
- --with-select_module
--without-select_module—
abilita o disabilita la compilazione del modulo che consente al server
di utilizzare il metodo select.
Tale modulo e' compilato automaticamente nel caso in cui la piattaforma non
supporti metodi piu' appropriati, quali kqueue, epoll, rtsig, o /dev/poll.
- --with-poll_module
--without-poll_module—
abilita o disabilita la compilazione del modulo che consente al server
di utilizzare il metodo poll.
Tale modulo e' compilato automaticamente nel caso in cui la piattaforma non
supporti metodi piu' appropriati, quali kqueue, epoll, rtsig, o /dev/poll.
- --without-http_gzip_module—
disabilita la compilazione del modulo che
comprime le risposte
del server HTTP.
Per la compilazione e l'utilizzo di questo modulo e' richiesta la libreria zlib.
- --without-http_rewrite_module—
disabilita la compilazione del modulo che consente al server HTTP di
redirigere e cambiare l'URI
delle richieste.
Per la compilazione e l'utilizzo di questo modulo e' richiesta la libreria PCRE.
- --without-http_proxy_module—
disabilita la compilazione del
modulo di proxy
del server HTTP.
- --with-http_ssl_module—
abilita la compilazione del modulo che aggiunge al server HTTP il
supporto al protocollo HTTPS.
Per default tale modulo non e' compilato.
Per la compilazione e l'utilizzo di questo modulo e' richiesta la libreria OpenSSL.
- --with-pcre=path—
indica il path ai sorgenti della libreria PCRE.
E' necessario scaricare dal sito di PCRE
la distribuzione della libreria (versioni da 4.4 a 8.32), ed estrarla.
Al resto ci pensano i comandi ./configure e
make di nginx.
La libreria e' richiesta per il supporto alle espressioni regolari nella
direttiva  e per il
modulo ngx_http_rewrite_module.
- --with-pcre-jit—
compila la libreria PCRE con il supporto “just-in-time"
(1.1.12, direttiva ).
- --with-zlib=path—
indica il path ai sorgenti della libreria zlib.
E' necessario scaricare dal sito di zlib
la distribuzione della libreria (versioni da 1.1.3 a 1.2.7), ed estrarla.
Al resto ci pensano i comandi ./configure e
make di nginx.
La libreria e' richiesta per il modulo
ngx_http_gzip_module.
- --with-cc-opt=parameters—
definisce i parametri che saranno aggiunti alla variabile CFLAGS.
Nel caso in cui si stia usando la libreria PCRE in ambiente FreeBSD,
bisognerebbe specificare --with-cc-opt="-I /usr/local/include".
Se il numero di file supportati da select deve essere
incrementato, e' possibile farlo anche con questo parametro, ad esempio con:
--with-cc-opt="-D FD_SETSIZE=2048".
- --with-ld-opt=parameters—
definisce i parametri aggiuntivi che saranno usati durante il linking.
Nel caso in cui si stia usando la libreria PCRE in ambiente FreeBSD,
bisognerebbe specificare --with-ld-opt="-L /usr/local/lib".

Un esempio d'uso dei parametri (da scrivere tutti su un'unica linea):

```
./configure
    --sbin-path=/usr/local/nginx/nginx
    --conf-path=/usr/local/nginx/nginx.conf
    --pid-path=/usr/local/nginx/nginx.pid
    --with-http_ssl_module
    --with-pcre=../pcre-4.4
    --with-zlib=../zlib-1.1.3
```

Dopo la configurazione, nginx e' compilato ed installato tramite
il comando `make`.
