# Come nginx processa una richiesta

**Author:** Igor Sysoev  
**Editor:** Brian Mercer  
**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it

# Server virtuali name-based

La prima cosa che nginx fa e' decidere quale *server* deve processare la richiesta. Si consideri una semplice configurazione in cui tutti i tre server virtuali sono in ascolto sulla porta *:80 :

```
server {
    listen      80;
    server_name example.org www.example.org;
    ...
}

server {
    listen      80;
    server_name example.net www.example.net;
    ...
}

server {
    listen      80;
    server_name example.com www.example.com;
    ...
}
```

In questa configurazione nginx verifica solo il campo `Host` dell'header di richiesta, per determinare a quale server la richiesta debba essere assegnata. Se il suo valore non corrisponde con quello di alcun nome di server, oppure se la richiesta semplicemente non contiene tale campo dell'header, allora nginx assegna la richiesta al server di default per la relativa porta. Nella configurazione precedente, il server di default e' il primo—si tratta del comportamento standard di nginx. E' anche possibile indicare esplicitamente il server di default, tramite il parametro `default_server` nella direttiva [listen](ngx_http_core_module.xml#listen) :

```
server {
    listen      80 default_server;
    server_name example.net www.example.net;
    ...
}
```

> **Note:** Il parametro `default_server` e' disponibile a partire dalla
versione 0.8.21 di nginx.
Nelle versioni precedenti bisogna usare invece il parametro `default` .

Si noti che il server di default e' una proprieta' della porta in ascolto, e non del nome del server; l'argomento sara' ripreso in seguito.

# Come evitare di processare richieste in cui il nome del server non e' definito {#how_to_prevent_undefined_server_names}

Se si desidera che le richieste prive dell'header `Host` non siano processate, e' possibile definire un server che si limita a scartarle:

```
server {
    listen      80;
    server_name "";
    return      444;
}
```

In questo caso il nome del server e' definito con una stringa vuota, la quale corrispondera' a tutte le richieste prive del campo `Host` dell'header; per chiudere la connessione nginx restituisce il codice 444 (non standard).

> **Note:** A partire dalla versione 0.8.48 quella descritta e' la configurazione
default per i nomi di server, per cui e' possibile omettere `server_name ""` .
Nelle versioni precedenti, come nome del server di default si utilizzava
l' *hostname* della macchina.

# Configurazione mista di server virtuali name-based e IP-based {#mixed_name_ip_based_servers}

Una configurazione piu' complessa prevede vari server virtuali in ascolto su indirizzi differenti:

```
server {
    listen      192.168.1.1:80;
    server_name example.org www.example.org;
    ...
}

server {
    listen      192.168.1.1:80;
    server_name example.net www.example.net;
    ...
}

server {
    listen      192.168.1.2:80;
    server_name example.com www.example.com;
    ...
}
```

In tale configurazione nginx dapprima confronta l'indirizzo IP e la porta della richiesta con le direttive [listen](ngx_http_core_module.xml#listen) dei blocchi [server](ngx_http_core_module.xml#server) ; quindi, per ciascun blocco per cui c'e' corrispondenza, nginx confronta il campo `Host` dell'header della richiesta con i valori [server_name](ngx_http_core_module.xml#server_name) del blocco. Se il nome del server non e' presente in alcun blocco, la richiesta viene processata dal server di default. Ad esempio, una richiesta per `www.example.com` ricevuta sulla porta 192.168.1.1:80, sara' processata dal server di default di 192.168.1.1:80, vale a dire dal primo server, in quanto non c'e' alcun nome `www.example.com` definito per tale combinazione di indirizzo e porta.

Si precisa nuovamente che il server di default e' una proprieta' di indirizzo e porta in ascolto, e che e' possibile definire server di default differenti per combinazioni differenti di indirizzo e porta:

```
server {
    listen      192.168.1.1:80;
    server_name example.org www.example.org;
    ...
}

server {
    listen      192.168.1.1:80 default_server;
    server_name example.net www.example.net;
    ...
}

server {
    listen      192.168.1.2:80 default_server;
    server_name example.com www.example.com;
    ...
}
```

# Configurazione per un semplice sito PHP {#simple_php_site_configuration}

Nel seguito si analizza come nginx scelga la *location* per processare una richiesta nel caso di un tipico, semplice sito PHP:

```
server {
    listen      80;
    server_name example.org www.example.org;
    root        /data/www;

    location / {
        index   index.html index.php;
    }

    location ~* \.(gif|jpg|png)$ {
        expires 30d;
    }

    location ~ \.php$ {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME
                      $document_root$fastcgi_script_name;
        include       fastcgi_params;
    }
}
```

Per prima cosa nginx individua fra tutte le location definite da una stringa quella con il prefisso specifico piu' lungo (l'ordine con cui sono elencate non e' rilevante); nella configurazione precedente il solo prefisso definito e' “ `/` ”, che trova corrispondenza in qualsiasi richiesta e che quindi verra' comunque preso in considerazione, come ultima risorsa. Successivamente, nginx analizza le location definite tramite una espressione regolare, fermandosi appena ne individua una che corrisponde (in questo caso l'ordine in cui sono inserite nel file di configurazione e' rilevante in quanto nginx parte dalla prima e le analizza una dopo l'altra). La prima location individuata fra quelle definite come espressione regolare e' quella prescelta; se non ce n'e' nessuna, nginx ripiega su quella individuata al passo precedente tramite il prefisso.

Notare che tutti i tipi di location sono confrontati con il solo URI della linea di richiesta, senza argomenti; cio' e' dovuto al fatto che gli argomenti nella stringa di richiesta possono essere inviati in vari modi, ad esempio:

```
/index.php?user=john&page=1
/index.php?page=1&user=john
```

Inoltre, nella stringa di richiesta e' possibile scrivere qualsiasi cosa:

```
/index.php?page=1&something+else&user=john
```

Seguono alcuni esempi di processo di richieste in base alla configurazione precedente:

- Una richiesta “ `/logo.gif` ” corrisponde al prefisso
di location “ `/` ”, ma anche all'espressione regolare
“ `\.(gif|jpg|png)$` ”, per cui si utilizzera' quest'ultima
corrispondenza in quanto, come spiegato in precedenza, le espressioni
regolari hanno sempre priorita' sulle stringhe fisse.
Usando la direttiva “ `root /data/www` ” la richiesta
e' mappata sul file `/data/www/logo.gif` , che quindi e' inviato
al client.
- Una richiesta “ `/index.php` ” corrisponde sia al prefisso
“ `/` ” sia all'espressione regolare
“ `\.(php)$` ”, per cui sara' processata da quest'ultima
sezione della configurazione, e la richiesta sara' inoltrata al server
FastCGI in ascolto su localhost:9000.
La direttiva [fastcgi_param](ngx_http_fastcgi_module.xml#fastcgi_param) imposta il parametro FastCGI `SCRIPT_FILENAME` a “ `/data/www/index.php` ”,
ed il server FastCGI esegue il file.
La variabile `$document_root` contiene il valore della direttiva [root](ngx_http_core_module.xml#root) , e la variabile `$fastcgi_script_name` il valore della richiesta URI, vale a dire
“ `/index.php` ”.
- Una richiesta “ `/about.html` ” corrisponde al solo prefisso
“ `/` ”, per cui sara' processata da questa sezione.
La direttiva “ `root /data/www` ” mappa la richiesta sul file `/data/www/about.html` , che e' inviato al client.
- Una richiesta “ `/` ” e' processata in maniera piuttosto
complessa. Corrisponde al solo prefisso “ `/` ”, per cui e'
processata dalla relativa sezione; la direttiva [index](ngx_http_index_module.xml#index) ,
in accordo ai propri parametri e alla direttiva
“ `root /data/www` ”, verifica la presenza di eventuali file index.
Se il file `/data/www/index.html` non esiste, ma esiste invece il
file `/data/www/index.php` , allora la direttiva esegue una
redirezione interna su “ `/index.php` ”, e nginx ricerca
nuovamente le location, come se si trattasse di una richiesta del client.
Come visto in precedenza, alla fine la richiesta rediretta e' processata
dal server FastCGI.

