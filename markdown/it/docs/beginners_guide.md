# Guida per il principiante

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it


La presente guida fornisce una introduzione a nginx e descrive alcune
semplici funzionalità per il quale può essere utilizzato.
Nel seguito si presuppone che nginx sia gia' stato installato;
in caso contrario fare riferimento alla pagina
[install.html](install.html).
La presente guida spiega come avviare, come fermare e come ricaricare
la configurazione di nginx, descrive brevemente la struttura del file
di configurazione, spiega come configurare nginx per servire contenuti statici,
come configurarlo per l'uso come proxy server,
e come configurarlo per l'uso con un'applicazione FastCGI.

nginx ha un processo master e numerosi processi worker:
lo scopo principale del processo master e' leggere e interpretare la configurazione,
e mantenere i processi worker attivi;
a loro volta, i processi worker si occupano di gestire effettivamente le richieste.
nginx utilizza un modello event-based e meccanismi dipendenti dal sistema operativo
per distribuire con efficienza le richieste fra i processi worker.
Il numero di processi worker e' definito nel file di configurazione,
e puo' sia essere fisso,
sia essere regolato automaticamente in base al numero di core CPU disponibili
(vedere [](ngx_core_module.xml#worker_processes)).

La maniera in cui nginx e i suoi moduli lavorano e' determinata nel file di configurazione;
per default, tale file si chiama
`nginx.conf`
e si trova in una delle directory:
`/usr/local/nginx/conf` ,
`/etc/nginx` ,
`/usr/local/etc/nginx` .

## Avvio, arresto e ricaricamento della configurazione {#control}

Per far partire nginx, avviare il file eseguibile.
Una volta partito, nginx puo' essere controllato invocando l'eseguibile con il parametro
`-s` .
Usare la seguente sintassi:

```
nginx -s signal
```

Dove *signal* e' uno dei seguenti:

- `stop`—arresto rapido
- `quit`—arresto controllato
- `reload`—ricaricamento della configurazione
- `reopen`—riapertura del file di log

Ad esempio, per fermare il processo nginx ma attendendo che finisca di servire
le richieste correnti, va eseguito il seguente comando:

```
nginx -s quit
```


> **Note:** Questo comando dovrebbe essere eseguito dallo stesso utente che ha avviato nginx.

Le modifiche al file di configurazione non saranno applicate sinche'
nginx non e' riavviato o non riceve il comando di ricaricamento della configurazione.
Per ricaricare la configurazione, eseguire:

```
nginx -s reload
```

Quando il processo master riceve il segnale di ricaricamento della configurazione,
verifica la validita' sintattica e tenta di applicare la configurazione riportata nel relativo file.
Se ha successo, il processo master avvia nuovi processi worker e invia messaggi di chiusura a quelli vecchi,
che smettono di accettare nuove connessioni ma continuano a servire le richieste correnti sinche' non sono
state del tutto completate, dopo di che terminano.
Se la nuova configurazione non risulta corretta, oppure se non e' possibile applicarla,
il processo master continua a lavorare con la configurazione precedente.

E' anche possibile inviare un segnale ai processi nginx tramite i normali comandi Unix,
quale ad esempio `kill`, che invia un segnale al processo individuato tramite il relativo ID;
per default, l'ID del processo master di nginx e' scritto nel file `nginx.pid`
nella directory
`/usr/local/nginx/logs` oppure
`/var/run` .
Ad esempio, se l'ID del processo master e' 1628, per inviare il segnale QUIT,
che causa l'arresto controllato, bisogna eseguire il comando:

```
kill -s QUIT 1628
```

Per ottenere la lista di tutti in processi nginx, e' possibile usare vari comandi,
fra cui ad esempio `ps`
nella maniera seguente:

```
ps -ax | grep nginx
```

Per ulteriori informazioni su come inviare segnali a nginx, fare riferimento a
[control.html](control.html).

## Struttura del file di configurazione {#conf_structure}

nginx e' costituito da moduli che sono controllati da direttiva specificate
nel file di configurazione.
Le direttive possono essere semplici o a blocco.
Una direttiva semplice e' caratterizzata dal nome seguito da parametri separati da spazi,
e termina con punto e virgola (`;`).
Una direttiva a blocco ha la stessa struttura di una direttiva semplice,
ma, invece che con punto e virgola, termina con un insieme di istruzioni aggiuntive racchiuse
fra parentesi graffe ( `{` e `}` ).
Una direttiva che puo' avere altre direttive all'interno delle parentesi graffe e' chiamata
contesto (ad esempio:
[](ngx_core_module.xml#events),
[](http/ngx_http_core_module.xml#http),
[](http/ngx_http_core_module.xml#server),
e
[](http/ngx_http_core_module.xml#location)).

Le direttive del file di configurazione che non sono all'interno di alcun
contesto sono considerate facenti parte del contesto
[main](ngx_core_module.html).
Le direttive `events` e `http`
appartengono al contesto `main`, la direttiva `server`
al contesto `http`,
la direttiva `location` al contesto `server`.

Tutto cio' che in una riga segue il simbolo `#` e' considerato un commento.

## Servizio di contenuti statici {#static}

Un compito importante di un web server e' costituito dal servizio
di file, quali immagini o pagine HTML statiche.
Di seguito si implementa un esempio in cui, a seconda della richiesta,
i file sono serviti prendendoli da varie directory locali: `/data/www`
(che puo' contenere file HTML) e `/data/images`
(che contiene immagini).
Per tale implementazione e' necessaria la modifica del file di configurazione,
con l'aggiunta,
all'interno di un blocco [](http/ngx_http_core_module.xml#http),
di un blocco [](http/ngx_http_core_module.xml#server)
a sua volta contenente due blocchi [](http/ngx_http_core_module.xml#location).

Anzitutto, creare le directory `/data/www` e `/data/images`,
e aggiungere nella prima un file `index.html` contenente un testo qualsiasi,
nella seconda una immagine a caso.

Quindi, aprire il file di configurazione;
si puo' notare che contiene gia' diversi esempi di blocchi `server`,
per la maggior parte inattivati da commenti;
inattivare con commenti tutto il blocco `http`, e scriverne uno nuovo:

```
http {
    server {
    }
}
```

In generale, il file di configurazione puo' includere numerosi blocchi `server`,
[distinti](http/request_processing.html) in base alla porta su cui
sono in [ascolto](http/ngx_http_core_module.xml#listen) e al
[nome del server](http/server_names.html).
Una volta che nginx ha deciso quale `server` deve processare una data richiesta,
confronta l'URI presente nell'header della stessa con i parametri delle direttive
`location` definite all'interno del blocco `server`.

Aggiungere il seguente blocco `location`
al blocco `server`:

```
location / {
    root /data/www;
}
```

Questo blocco `location` fa riferimento al prefisso “`/`”,
da confrontare con l'URI della richiesta:
se la richiesta corrisponde, l'URI viene aggiunto al path specificato dalla
direttiva [](http/ngx_http_core_module.xml#root),
in questo caso cioe' a `/data/www` ,
per definire sul file system locale il path al file richiesto.
Se i blocchi `location` che corrispondono sono piu' di uno,
nginx seleziona quello con il prefisso piu' lungo;
il blocco `location` dell'esempio riguarda il prefisso
piu' breve in assoluto, di lunghezza uno, quindi e' effettivamente usato
solo se tutti gli altri blocchi `location` non corrispondono.

Tornando all'esempio, aggiungere un secondo blocco `location`:

```
location /images/ {
    root /data;
}
```

In questo caso ci sara' corrispondenza con
le richieste che iniziano con `/images/`
(anche `location /` corrisponde alla richiesta,
ma ha un prefisso piu' breve e quindi priorita' inferiore).
La configurazione risultante del blocco `server` risulta quindi:

```
server {
    location / {
        root /data/www;
    }

    location /images/ {
        root /data;
    }
}
```

Tale configurazione e' effettivamente funzionante,
con il server in ascolto sulla porta standard 80 e accessibile
sulla macchina locale a `http://localhost/` .
In risposta alle richieste di URI che iniziano con `/images/` ,
il server inviera' file presi dalla directory `/data/images` ;
ad esempio, in risposta ad una richiesta
`http://localhost/images/example.png`
nginx inviera' il file `/data/images/example.png` .
Se tale file non esiste, nginx inviera' una risposta che indica
l'errore 404.
Richieste di URI che non iniziano con `/images/`
saranno mappate sulla directory `/data/www` ;
ad esempio, in risposta ad una richiesta
`http://localhost/some/example.html`
nginx inviera' il file `/data/www/some/example.html` .

Per applicare la nuova configurazione, avviare nginx se e' spento;
se e' gia' attivo, inviare il segnale `reload` al processo master,
eseguendo:

```
nginx -s reload
```

> **Note:** Nel caso in cui qualcosa non vada come atteso, e' possibile cercare
di capire cosa e' successo verificandolo nei file `access.log` e
`error.log`, presenti nella directory `/usr/local/nginx/logs` o
`/var/log/nginx` .

## Configurare un semplice proxy server {#proxy}

Uno degli usi piu' frequenti di nginx prevede la configurazione come proxy server,
vale a dire un server che riceve le richieste dai client, le passa ai server remoti,
riceve da essi le risposte, e le reinvia ai client.

Di seguito si configura un semplice proxy server, il quale serve le richieste
di immagini con file da una directory locale, e invia invece tutte le altre
richieste a un ulteriore server web.
Nell'esempio, entrambi i server saranno definiti su una singola istanza di nginx..

Per iniziare, definire il server web aggiuntivo inserendo nel file di configurazione di
nginx un ulteriore blocco `server` con il contenuto seguente:

```
server {
    listen 8080;
    root /data/up1;

    location / {
    }
}
```

Si tratta di un semplice server in ascolto sulla porta 8080
(in precedenza la direttiva `listen` non e' stata specificata
in quanto e' stata usata la porta standard 80), che mappa tutte le
richieste sulla directory `/data/up1` del file system locale.
Creare tale directory, e inserire in essa un file `index.html` .
Notare che la direttiva `root` e' posta nel
contesto `server` ; tale direttiva `root` e' usata
quando il blocco `location` scelto per servire una richiesta
non include una direttiva `root` propria.

Procedere usando la configurazione del server della sezione precedente e
modificandola per farne un proxy server.
Nel primo blocco `location`, inserire la direttiva
[](http/ngx_http_proxy_module.xml#proxy_pass)
specificando come parametro il protocollo, il nome e la porta del server
web aggiuntivo (in questo caso `http://localhost:8080` ):

```
server {
    location / {
        proxy_pass http://localhost:8080;
    }

    location /images/ {
        root /data;
    }
}
```

A questo punto modificare il secondo blocco `location`, che al momento
mappa le richieste con il prefisso `/images/` sui file nella directory
`/data/images` , per fare in modo che risponda alle richieste con le
tipiche estensioni file delle immagini.
Il blocco `location` sara' il seguente:

```
location ~ \.(gif|jpg|png)$ {
    root /data/images;
}
```

Il parametro e' una espressione regolare che corrisponde a tutti gli URI
che terminano con `.gif`, `.jpg`, o `.png`
(in nginx le espressioni regolari normalmente iniziano con `~`).
La richiesta corrispondente sara' mappata sulla directory `/data/images` .

Per decidere quale blocco `location` debba servire una richiesta,
nginx per prima cosa verifica le direttive
[](http/ngx_http_core_module.xml#location)
che riportano la specifica di un prefisso, registrando quella con il piu' lungo
prefisso che corrisponde, quindi verifica quelle con una espressione regolare;
se c'e' corrispondenza con una espressione regolare, nginx sceglie tale
`location`, altrimenti sceglie quella registrata in precedenza.

Alla fine la configurazione risultante di un proxy server e' la seguente:

```
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

Tale server selezionera' le richieste che terminano in `.gif`,
`.jpg` o `.png` e le mappera' sulla directory
`/data/images` (aggiungendo l'URI al parametro della direttiva
`root`), mentre invece passera' tutte le altre richieste al web
server configurato in precedenza.

Per applicare la nuova configurazione, inviare il segnale `reload`
ad nginx, come descritto nella sezione precedente.

Ci sono molte [more](http/ngx_http_proxy_module.html)
direttive che possono essere usate nella configurazione di un proxy.

## Configurare il proxying FastCGI {#fastcgi}

nginx puo' essere usato per dirigere le richieste ad uno o piu' server
FastCGI che eseguono applicazioni scritte con vari framework e linguaggi di
programmazione, ad esempio PHP.

La configurazione piu' semplice di nginx che consente di lavorare con un server
FastCGI, richiede l'uso della direttiva
[](http/ngx_http_fastcgi_module.xml#fastcgi_pass)
al posto della direttiva `proxy_pass`,
e della direttiva [](http/ngx_http_fastcgi_module.xml#fastcgi_param)
per impostare i parametri passati al server FastCGI.
Nel seguito si suppone che il server FastCGI sia accessibile a `localhost:9000` .
Prendendo la configurazione di un proxy nella sezione precedente come base,
sostituire la direttiva `proxy_pass` con la direttiva `fastcgi_pass`
e cambiare il relativo parametro in `localhost:9000` .
Nel caso del PHP, il parametro `SCRIPT_FILENAME` e' usato per determinare
il nome dello script, ed il parametro `QUERY_STRING` e' usato per
passare i parametri della richiesta.
La configurazione risulta quindi:

```
server {
    location / {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING    $query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

Tale configurazione realizza un server che inoltra tutte le richieste
(a parte quelle per immagini statiche) tramite il protocollo FastCGI
ad un server esterno che opera su
`localhost:9000` .
