# Messa a punto degli hash

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it


Per processare rapidamente insiemi di dati, quali ad esempio
nomi di server, valori relativi alla direttiva
[](http/ngx_http_map_module.xml#map),
MIME type, stringhe di nomi di header di richiesta,
nginx usa tabelle di hash.
Durante l'avvio ed in seguito ad ogni rilettura della configurazione,
nginx seleziona la minore dimensione possibile delle tabelle
di hash, tale che la dimensione del bucket che memorizza le chiavi
con identico valore hash non superi il relativo parametro configurato
(hash bucket size).
La dimensione di una tabella e' espressa in bucket; tale dimensione
viene regolata continuamente, sinche' la dimensione non eccede il
valore configurato (hash max size).
Molti hash dispongono di specifiche direttive che consentono la modifica
di tali parametri; ad esempio, per l'hash dei nomi dei server esistono
[](http/ngx_http_core_module.xml#server_names_hash_bucket_size)
e [](http/ngx_http_core_module.xml#server_names_hash_max_size).

Il parametro hash bucket size e' allineato ad una dimensione
multipla di quella di una linea di cache del processore utilizzato;
nei moderni processori cio' riduce il numero di accessi alla memoria
e quindi il tempo necessario a ricercare la chiave di un hash.
Se la dimensione del bucket hash e' pari a quella di una linea di
cache, allora il numero di accessi alla memoria durante la ricerca di
una chiave sara' nel peggiore dei casi pari a due —uno per l'indirizzo
del bucket, l'altro durante la ricerca della chiave nel bucket.
Per tale ragione, se nginx mostra un messaggio che suggerisce
l'incremento o della dimensione massima dell'hash oppure della
dimensione del bucket hash, e' preferibile intervenire anzitutto
sul primo dei due parametri e non modificare per quanto possibile
il secondo.
