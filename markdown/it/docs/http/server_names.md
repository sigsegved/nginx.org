# I nomi dei server

**Author:** Igor Sysoev  
**Editor:** Brian Mercer  
**Translator:** Angelo Papadia  
**Revision:** 2  
**Language:** it

I nomi dei server, definiti usando la direttiva [server_name](ngx_http_core_module.xml#server_name) , determinano quale blocco [server](ngx_http_core_module.xml#server) viene usato per una data richiesta (per approfondire vedi " ”). I nomi possono essere definiti tramite una stringa determinata, oppure con caratteri jolly, oppure ancora tramite espressioni regolari:

```
server {
    listen       80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       80;
    server_name  *.example.org;
    ...
}

server {
    listen       80;
    server_name  mail.*;
    ...
}

server {
    listen       80;
    server_name  ~^(?<user>.+)\.example\.net$;
    ...
}
```

Nel corso della ricerca di un server virtuale name-based, se il nome corrisponde a piu' di una delle definizioni, ad esempio sia a nomi definiti tramite caratteri jolly che a nomi definiti tramite espressioni regolari, verra' scelta la prima variante individuata, secondo il seguente ordine di precedenza decrescente:

1. nome esatto
2. fra quelli definiti con caratteri jolly, il piu' lungo nome che comincia per
asterisco, ad esempio “ `*.example.org` ”
3. fra quelli definiti con caratteri jolly, il piu' lungo nome che termina per
asterisco, ad esempio “ `mail.*` ”
4. fra quelli definiti come espressioni regolare, il primo corrispondente
(in base all'ordine con cui compaiono nel file di configurazione)

# Nomi con caratteri jolly {#wildcard_names}

Un nome con caratteri jolly puo' contenere un asterisco solo all'inizio o alla fine del nome, e solo accanto ad un punto; ad esempio, i nomi “ `www.*.example.org` ” e “ `w*.example.org` ” non sono validi (pero' e' possibile definirli tramite espressioni regolari, per esempio in questo caso “ `~^www\..+\.example\.org$` ” e “ `~^w.*\.example\.org$` ”). Un asterisco puo' corrispondere a piu' parti di un nome: “ `*.example.org` ” corrisponde non solo a `www.example.org` ma anche a `www.sub.example.org` .

E' possibile definire un nome speciale nella forma “ `.example.org` ”, che corrisponde sia al nome esatto “ `example.org` ” sia al nome con caratteri jolly “ `*.example.org` ”.

# Nomi con espressioni regolari {#regex_names}

Le espressioni regolari usate da nginx sono compatibili con quelle usate dal linguaggio di programmazione Perl (PCRE). Per usare una espressione regolare, il nome del server deve iniziare con il carattere tilde:

```
server_name  ~^www\d+\.example\.net$;
```

altrimenti viene considerato e trattato come un nome esatto, oppure, se l'espressione contiene un asterisco, come un nome con caratteri jolly (e molto probabilmente come uno non valido). E' importante non dimenticare i caratteri ancora “ `^` ” e “ `$` ”: non sono necessari dal punto di vista sintattico, ma lo sono da quello logico. Si noti inoltre che i caratteri punto nei nomi di dominio sono definiti facendoli precedere da “ `\` ”. Una espressione regolare contenente i caratteri “ `{` ” e “ `}` ”, deve essere racchiusa fra doppi apici:

```
server_name  "~^(?<name>\w\d{1,3}+)\.example\.net$";
```

altrimenti nginx non sara' in grado di avviarsi e mostrera' l'errore:

```
directive "server_name" is not terminated by ";" in ...
```

La sezione catturata di una espressione regolare che definisce un nome puo' essere usata in seguito come una variabile:

```
server {
    server_name   ~^(www\.)?(?<domain>.+)$;

    location / {
        root   /sites/$domain;
    }
}
```

La libreria PCRE supporta sezioni catturate di nomi tramite la seguente sintassi: Quando nginx non riesce ad avviarsi e mostra il seguente messaggio d'errore:

```
pcre_compile() failed: unrecognized character after (?< in ...
```

significa che la libreria PCRE e' troppo vecchia, per cui e' bene provare ad usare invece la sintassi: “ `?P<` ”. E' possibile riferirsi a sezioni catturate anche usando cifre:

```
server {
    server_name   ~^(www\.)?(.+)$;

    location / {
        root   /sites/$2;
    }
}
```

Comunque, tale uso dovrebbe essere limitato ai casi piu' semplici (come ad esempio quello appena mostrato), dato che i riferimenti con cifra possono essere sovrascritti facilmente.

# Nomi vari {#miscellaneous_names}

Alcuni nomi di server sono trattati in maniera speciale.

Se si desidera che le richieste prive del campo `Host` dell'header siano processato in un blocco [server](ngx_http_core_module.xml#server) che non e' quello di default, e' necessario specificare un nome vuoto:

```
server {
    listen       80;
    server_name  example.org  www.example.org  "";
    ...
}
```

Se in un blocco [server](ngx_http_core_module.xml#server) non e' specificato alcun [server_name](ngx_http_core_module.xml#server_name) , allora nginx usa il nome vuoto come nome del server.

> **Note:** sino alla versione 0.8.48, in questi casi nginx usava l'hostname della
macchina come nome del server.

Se il nome del server e' definito come “ `$hostname` ” (0.9.4), il nome del server effettivamente usato e' l'hostname della macchina.

Se viene fatta una richiesta usando l'indirizzo IP invece di un nome di server, il campo `Host` dell'header di richiesta conterra' l'indirizzo IP, e la richiesta potra' essere processata usando l'indirizzo IP come nome del server:

```
server {
    listen       80;
    server_name  example.org
                 www.example.org
                 ""
                 192.168.1.1
                 ;
    ...
}
```

In molti esempi di configurazione di un server catch-all e' spesso possibile notare l'uso di uno strano nome “ `_` ”:

```
server {
    listen       80  default_server;
    server_name  _;
    return       444;
}
```

Tale nome non ha niente di speciale, si tratta di un nome qualsiasi, scelto piu' o meno a caso fra quelli non validi come nome di dominio. Altri esempi di nomi non validi che sono talvolta pure usati sono “ `--` ” e “ `!@#` ”.

Sino alla versione 0.6.25 nginx supportava il nome speciale “ `*` ”, che e' stato spesso interpretato erroneamente come un nome, non valido, per un server catch-all. In effetti, non si e' mai trattato di un nome per un server catch-all o di un nome con caratteri jolly: piuttosto, serviva a fornire la funzionalita' attualmente affidata alla direttiva [server_name_in_redirect](ngx_http_core_module.xml#server_name_in_redirect) . Il nome speciale “ `*` ” e' attualmente sconsigliato, ed e' considerato preferibile l'uso della direttiva [server_name_in_redirect](ngx_http_core_module.xml#server_name_in_redirect) . Si noti che non c'e' alcun modo di specificare un nome catch-all o un server di default usando la direttiva [server_name](ngx_http_core_module.xml#server_name) : si tratta di una proprieta' della direttiva [listen](ngx_http_core_module.xml#listen) e non della direttiva [server_name](ngx_http_core_module.xml#server_name) Si faccia riferimento anche a “ ”. E' possibile definire server in ascolto sulle porte *:80 e *:8080, e specificare che uno e' quello di default per la porta *:8080, mentre l'altro e' quello di default per la porta *:80:

```
server {
    listen       80;
    listen       8080  default_server;
    server_name  example.net;
    ...
}

server {
    listen       80  default_server;
    listen       8080;
    server_name  example.org;
    ...
}
```

# Ottimizzazione {#optimization}

I nomi esatti, i nomi con caratteri jolly che iniziano per asterisco, ed i nomi con caratteri jolly che terminano per asterisco, sono registrati in tre tabelle di hash collegate alle porte in ascolto. Le dimensioni delle tabelle sono ottimizzate in fase di configurazione, in maniera tale che i nomi possano essere recuperati con il minimo numero di miss alla cache della CPU. Dettagli su come configurare le tabelle di hash sono forniti in un [documento](../hash.xml) apposito.

La prima tabella di hash consultata e' quella dei nomi esatti; se non si trova il nome ricercato, si prosegue nella tabella di hash dei nomi con caratteri jolly che iniziano per asterisco; in caso di ulteriore riscontro negativo, si passa alla tabella di hash dei nomi con caratteri jolly che finiscono per asterisco.

La ricerca in una tabella di hash per nomi con caratteri jolly e' piu' lenta della ricerca nella tabella relativa ai nomi esatti, dato che i nomi sono ricercati per parti del dominio. Si noti che il formato speciale “ `.example.org` ” e' salvato in una tabella di hash di nomi con caratteri jolly, e non in quella dei nomi esatti.

Le espressioni regolari sono testate in sequenza, per cui sono il metodo piu' lento e sono non scalabili.

Per queste ragioni, se possibile e' sempre meglio usare nomi esatti. Ad esempio, se i nomi di server richiesti piu' di frequente sono `example.org` e `www.example.org` , e' piu' efficiente definirli in maniera esplicita:

```
server {
    listen       80;
    server_name  example.org  www.example.org  *.example.org;
    ...
}
```

che usare il formato piu' semplice:

```
server {
    listen       80;
    server_name  .example.org;
    ...
}
```

Se il numero di nomi di server definiti e' molto grande, oppure se sono stati definiti nomi di server decisamente lunghi, per la messa a punto e' possibile che sia necessario utilizzare le direttive del livello *http* [server_names_hash_max_size](ngx_http_core_module.xml#server_names_hash_max_size) e [server_names_hash_bucket_size](ngx_http_core_module.xml#server_names_hash_bucket_size) . Il valore di default della direttiva [server_names_hash_bucket_size](ngx_http_core_module.xml#server_names_hash_bucket_size) puo' essere pari a 32 o 64, oppure ad un altro valore, in base alla dimensione della linea di cache della CPU. Se il valore di default e' 32 ed il nome del server e' definito come “ `too.long.server.name.example.org` ”, allora nginx non potra' partire e sara' mostrato il seguente messaggio d'errore:

```
could not build the server_names_hash,
you should increase server_names_hash_bucket_size: 32
```

In tal caso, il valore della direttiva dovrebbe essere aumentata sino alla successiva potenza di due:

```
http {
    server_names_hash_bucket_size  64;
    ...
```

Se sono stati definiti molti nomi di server, potrebbe comparire un altro messaggio di errore:

```
could not build the server_names_hash,
you should increase either server_names_hash_max_size: 512
or server_names_hash_bucket_size: 32
```

In tal caso, si provi prima a impostare [server_names_hash_max_size](ngx_http_core_module.xml#server_names_hash_max_size) ad un numero prossimo al numero dei nomi di server. Solo nel caso in cui cio' non risultasse sufficiente, oppure se il tempo di avvio di nginx fosse inaccetabilmente alto, si provi ad incrementare [server_names_hash_bucket_size](ngx_http_core_module.xml#server_names_hash_bucket_size) .

Se su una data porta in ascolto c'e' un unico server, allora nginx saltera' del tutto la verifica dei nomi dei server (e non costituira' le tabelle di hash per la porta in questione). C'e' una eccezione: se un nome di server e' una espressione regolare con sezioni catturate, allora nginx dovra' svolgere l'espressione regolare per recuperare le sezioni catturate.

# Compatibilita' {#compatibility}

- Il nome di server speciale “ `$hostname` ” e' supportato
dalla versione 0.9.4 in poi.
- Il nome vuoto “” e' il valore di default per il nome dei server
dalla versione 0.8.48 in poi.
- Il riferimento tramite nome a sezioni catturate in un nome di server definito
tramite espressione regolare e' supportato dalla versione 0.8.25 in poi.
- Le sezioni catturate in un nome di server definito tramite espressione regolare
sono supportate dalla versione 0.7.40 in poi.
- Il nome di server vuoto  “” e' supportato
dalla versione 0.7.12 in poi.
- La definizione di nomi di server e di espressioni regolari tramite caratteri jolly
e' supportata dalla versione 0.6.25 in poi.
- La definizione di nomi di server tramite espressioni regolari e' supportata
dalla versione 0.6.7 in poi.
- Il formato con caratteri jolly `example.*` e' supportato
dalla versione 0.6.0 in poi.
- Il formato speciale `.example.org` e' supportato
dalla versione 0.3.18 in poi.
- Il formato con caratteri jolly `*.example.org` e' supportato
dalla versione 0.1.13 in poi.

