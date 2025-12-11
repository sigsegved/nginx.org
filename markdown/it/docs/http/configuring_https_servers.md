# Configurazione di server HTTPS

**Author:** Igor Sysoev  
**Editor:** Brian Mercer  
**Translator:** Angelo Papadia  
**Revision:** 6  
**Language:** it


Per configurare un server HTTPS, bisogna configurare il parametro
`ssl` nel
[socket in ascolto](ngx_http_core_module.xml#listen)
del blocco [](ngx_http_core_module.xml#server),
e specificare dove sono i file del certificato del server e della relativa
chiave private:


```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ssl_protocols       SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ...
}
```


Il certificato del server e' pubblico: e' inviato a tutti i client che
si connettono al server; la chiave privata al contrario non e' pubblica,
e dovrebbe essere salvata in un file con restrizioni d'accesso, e
comunque non leggibile dal processo master di nginx.
In alternativa, la chiave privata puo' essere salvata nel medesimo file
del certificato:


```
ssl_certificate     www.example.com.cert;
    ssl_certificate_key www.example.com.cert;
```


pure in questo caso i diritti d'accesso al file dovrebbero essere ristretti.
Anche quando certificato e chiave privata sono salvati entrambi
in un unico file, solo il certificato e' inviato al client.

Le direttive [](ngx_http_ssl_module.xml#ssl_protocols) e
[](ngx_http_ssl_module.xml#ssl_ciphers) possono essere usate
per limitare l'uso alle sole versioni e cifrature forti di SSL/TLS nelle
connessioni.
nginx usa per default “`ssl_protocols SSLv3 TLSv1`” e
“`ssl_ciphers HIGH:!aNULL:!MD5`” sin dalla versione 1.0.5,
per cui una configurazione esplicita ha senso solo per le versioni di nginx
piu' vecchie. Dalle versioni 1.1.13 e 1.0.12 nginx usa per default
“`ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2`”.

La modalita' di cifratura CBC e' potenzialmente vulnerabile ad una serie
di attacchi, in particolare ad un attacco BEST (vedi
[CVE-2011-3389](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3389)).
La configurazione della cifratura puo' essere modificata in maniera da
utilizzare RC4-SHA:


```
ssl_ciphers RC4:HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
```

## Ottimizzazione di server HTTPS {#optimization}

Le operazioni SSL utilizzano pesantemente la CPU. Su sistemi
multiprocessore e' bene avviare processi worker in numero almeno pari a
quello dei core.
L'operazione piu' gravosa per la CPU e' l'handshake SSL.
Ci sono due modi per minimizzare il numero di tali operazioni per client:
il primo consiste nell'abilitare connessioni keepalive per inviare diverse
richieste tramite un'unica connessione; il secondo prevede di riutilizzare
i parametri della sessione SSL in maniera tale da evitare l'handshake SSL
per connessioni parallele e susseguenti.
Le sessioni sono salvate in una cache di sessione SSL, condivisa fra i
worker e configurata dalla direttiva
[](ngx_http_ssl_module.xml#ssl_session_cache).

Un megabyte di cache contiene circa 4000 sessioni. Il timeout di default della
cache e' di 5 minuti; puo' essere aumentato intervenendo sulla direttiva
[](ngx_http_ssl_module.xml#ssl_session_timeout).
Segue una configurazione di esempio ottimizzata per un sistema multicore con
10 megabyte di cache di sessione condivisa:


```
worker_processes auto;

http {
    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 10m;

    server {
        listen              443 ssl;
        server_name         www.example.com;
        keepalive_timeout   70;

        ssl_certificate     www.example.com.crt;
        ssl_certificate_key www.example.com.key;
        ssl_protocols       SSLv3 TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        ...
```

## Catene di certificati SSL {#chains}

Capita talvolta che alcuni certificati server firmati da autorita' di
certificazione ben note siano tranquillamente accettati da alcuni browser,
ma mostrino invece problemi con altri. Cio' succede quando' l'autorita'
emittente ha firmato il certificato usandone uno intermedio che non e'
presente nell'elenco delle autorita' di certificazione distribuito con
uno specifico browser.
In tal caso l'autorita' fornisce un gruppo di certificati che dovrebbero
essere concatenati al certificato server firmato.
Il certificato server deve comparire prima dei certificati concatenati
nel file risultante:


```
$ cat www.example.com.crt bundle.crt > www.example.com.chained.crt
```


Il file che ne deriva va usato con la  direttiva
[](ngx_http_ssl_module.xml#ssl_certificate):


```
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.chained.crt;
    ssl_certificate_key www.example.com.key;
    ...
}
```


Se il certificato server ed il gruppo di certificati sono stati concatenati
nell'ordine sbagliato, nginx non riuscira' a partire e mostrera' il
seguente messaggio di errore:


```
SSL_CTX_use_PrivateKey_file(" ... /www.example.com.key") failed
   (SSL: error:0B080074:x509 certificate routines:
    X509_check_private_key:key values mismatch)
```


dato che nginx ha tentato di usare la chiave privata non con il certificato
server ma con il primo certificato del gruppo.

Di solito i browser salvano i certificati intermedi che ricevono se sono
firmati da autorita' di certificazione riconosciute, per cui browser molto
usati potrebbero gia' avere i certificati intermedi richiesti, e quindi
non avere problemi anche quando ricevono un certificato privo della
relativa concatenazione di certificati.
Comunque, per assicurare che il server invii la concatenazione di certificati
completa, e' possibile usare da linea di comando il programma
`openssl`, ad esempio:


```
$ openssl s_client -connect www.godaddy.com:443
...
Certificate chain
 0 s:/C=US/ST=Arizona/L=Scottsdale/1.3.6.1.4.1.311.60.2.1.3=US
     /1.3.6.1.4.1.311.60.2.1.2=AZ/O=GoDaddy.com, Inc
     /OU=MIS Department/CN=www.GoDaddy.com
     /serialNumber=0796928-7/2.5.4.15=V1.0, Clause 5.(b)
   i:/C=US/ST=Arizona/L=Scottsdale/O=GoDaddy.com, Inc.
     /OU=http://certificates.godaddy.com/repository
     /CN=Go Daddy Secure Certification Authority
     /serialNumber=07969287
 1 s:/C=US/ST=Arizona/L=Scottsdale/O=GoDaddy.com, Inc.
     /OU=http://certificates.godaddy.com/repository
     /CN=Go Daddy Secure Certification Authority
     /serialNumber=07969287
   i:/C=US/O=The Go Daddy Group, Inc.
     /OU=Go Daddy Class 2 Certification Authority
 2 s:/C=US/O=The Go Daddy Group, Inc.
     /OU=Go Daddy Class 2 Certification Authority
   i:/L=ValiCert Validation Network/O=ValiCert, Inc.
     /OU=ValiCert Class 2 Policy Validation Authority
     /CN=http://www.valicert.com//emailAddress=info@valicert.com
...
```


In questo esempio, il soggetto (“*s*”, vale a dire "*subject*")
del certificato server #0 `www.GoDaddy.com` e' firmato da
un emittente (“*i*”, vale a dire "*issuer*") che a sua volta e'
il soggetto del certificato #1, il quale e' firmato da un emittente che e'
il soggetto del certificato #2, che e' finalmente firmato dalla autorita'
di certificazione ben nota *ValiCert, Inc.*, il cui certificato e'
presente nella base dati precaricata del browser
("che al mercato mio padre compro'").

Se il gruppo di certificati non fosse stato aggiunto, sarebbe stato
visualizzato il solo certificato #0.

## Un server unico per HTTP e HTTPS {#single_http_https_server}

E' possibile configurare un singolo server che tratti sia richieste HTTP,
sia richieste HTTPS:


```
server {
    listen              80;
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ...
}
```



> **Note:** Prima della versione 0.7.14, SSL non poteva essere abilitato
selettivamente per singoli socket in ascolto, come nell'esempio
precedente: SSL poteva solo essere abilitato per l'intero server,
usando la direttiva [](ngx_http_ssl_module.xml#ssl),
e rendendo quindi impossibile la configurazione di un server
unico per HTTP e HTTPS.
Il parametro `ssl` della direttiva
[](ngx_http_core_module.xml#listen) e' stato aggiunto
per risolvere questo problema. L'uso della direttiva
[](ngx_http_ssl_module.xml#ssl)
e' pertanto sconsigliato nelle versioni recenti.

## Server HTTPS name-based {#name_based_https_servers}

Quando si configurano due o piu' server HTTPS in ascolto su un singolo
indirizzo IP, sorge spesso un problema:


```
server {
    listen          443 ssl;
    server_name     www.example.com;
    ssl_certificate www.example.com.crt;
    ...
}

server {
    listen          443 ssl;
    server_name     www.example.org;
    ssl_certificate www.example.org.crt;
    ...
}
```


Con questa configurazione un browser riceve il certificato del server di default,
vale a dire `www.example.com`, indipendentemente da quale sia
il nome del server richiesto. Cio' e' causato dal comportamento del protocollo
SSL: la connessione SSL si stabilisce prima che il browser invii una richiesta
HTTP, percio' quando nginx ancora non sa quale sara' il nome del server richiesto;
per tale ragione, non puo' fare altro che offrire il certificato del server di default.

Il metodo classico per risolvere questo problema consiste nell'assegnare
un indirizzo IP distinto a ciascun server HTTPS:


```
server {
    listen          192.168.1.1:443 ssl;
    server_name     www.example.com;
    ssl_certificate www.example.com.crt;
    ...
}

server {
    listen          192.168.1.2:443 ssl;
    server_name     www.example.org;
    ssl_certificate www.example.org.crt;
    ...
}
```

### Un certificato SSL con molti nomi {#certificate_with_several_names}

Ci sono altre maniere tramite cui condividere un singolo indirizzo IP
fra molti server HTTPS, tutte comunque non prive di problemi.
Ad esempio, e' possibile usare un certificato con diversi nomi di server
nel campo SubjectAltName, per esempio
`www.example.com` and `www.example.org`,
tuttavia la lunghezza del campo SubjectAltName e' limitata.

Un'altra tecnica prevede l'uso di un certificato il cui nome e' definito con
caratteri jolly, per esempio `*.example.org`.
Un certificato con caratteri jolly va bene per tutti i sottodomini del
dominio specificato, ma per un solo livello: in questo caso ad esempio
verra' riconosciuta corrispondenza con `www.example.org`,
ma non con `example.org` e `www.sub.example.org`.
I due metodi mostrati possono essere combinati: nel campo SubjectAltName
un certificato puo' contenere sia nomi esatti sia nomi con caratteri jolly,
ad esempio `example.org` e `*.example.org`.

Nel caso in cui si usi un certificato con nomi multipli, e' bene
indicare la posizione del relativo file e della chiave nel livello
*http* della configurazione, in maniera da avere una singola
copia in memoria da far ereditare a tutti i server:


```
ssl_certificate     common.crt;
ssl_certificate_key common.key;

server {
    listen          443 ssl;
    server_name     www.example.com;
    ...
}

server {
    listen          443 ssl;
    server_name     www.example.org;
    ...
}
```

### Server Name Indication {#sni}

Una soluzione piu' generale per l'uso di server HTTPS multipli su un singolo
indirizzo IP e' data dalla
[estensione
TLS Server Name Indication](http://en.wikipedia.org/wiki/Server_Name_Indication) (SNI, RFC 6066), che consente ad un
browser di indicare il nome del server richiesto durante l'handshake SSL e,
percio', permette al server di sapere quale certificato dovrebbe essere
usato durante la connessione. Purtroppo, SNI ha un supporto piuttosto
limitato nei browser; al momento e' supportato a partire dalle seguenti
versioni:

- Opera 8.0;
- MSIE 7.0 (ma solo su Windows Vista o superiore);
- Firefox 2.0 e altri browser che usano Mozilla Platform rv:1.8.1;
- Safari 3.2.1 (la versione per Windows supporta SNI su Vista o superiore);
- Chrome (la versione per Windows supporta SNI su Vista o superiore).


> **Note:** Con SNI e' possibile passare solo nomi di dominio, tuttavia alcuni browser
potrebbero erroneamente consentire di passare come nome anche l'indirizzo
IP del server.
E' bene comunque non fare affidamento su questo comportamento.

Per poter usare SNI in nginx, e' necessario che sia supportato sia nella
libreria OpenSSL con cui il binario e' stato compilato, sia nella
libreria a cui e' linkato dinamicamente in esecuzione.
OpenSSL supporta SNI sin dalla versione 0.9.8f, a patto che sia stata
compilata con l'opzione di configurazione “--enable-tlsext”;
dalla versione 0.9.8j tale opzione e' abilitata per default.
Se nginx e' compilato con il supporto a SNI, allora l'esecuzione con
il parametro “-V” mostra:


```
$ nginx -V
...
TLS SNI support enabled
...
```


Di contro, se nginx e' stato compilato con il supporto a SNI, ma la libreria
OpenSSL a cui e' linkato dinamicamente ne e' priva, viene mostrato:


```
nginx was built with SNI support, however, now it is linked
dynamically to an OpenSSL library which has no tlsext support,
therefore SNI is not available
```

## Compatibilita' {#compatibility}

- Il parametro “-V” mostra lo stato del supporto a SNI
dalla versione 0.8.21 e 0.7.62 in poi.
- Il parametro `ssl` della direttiva
[](ngx_http_core_module.xml#listen)
e' supportato
dalla versione 0.7.14 in poi;
prima della versione 0.8.21 poteva essere specificato solo
insieme al parametro `default`.
- SNI e' supportato
dalla versione 0.5.32 in poi.
- La cache condivisa di sessione SSL e' supportata
dalla versione 0.5.6 in poi.

- Versioni 0.7.65, 0.8.19 e successive: i protocolli SSL default sono SSLv2, TLSv1,
e TLSv1.2 (se supportati dalla libreria OpenSSL).
- Versioni 0.7.64, 0.8.18 e precedenti: i protocolli SSL default sono SSLv2,
SSLv3, e TLSv1.

- Versioni 1.0.5 e successive: i sistemi di cifratura SSL default sono
“`HIGH:!aNULL:!MD5`”.
- Versioni 0.7.65, 0.8.20 e successive: i sistemi di cifratura SSL default sono
“`HIGH:!ADH:!MD5`”.
- Versione 0.8.19: i sistemi di cifratura SSL default sono
“`ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM`”.
- Versioni 0.7.64, 0.8.18 e precedenti: i sistemi di cifratura SSL default sono  

“`ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP`”.
