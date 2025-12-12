# Il log di debug

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it

Per poter abilitare il log di `debug` , nginx deve essere stato configurato appositamente in fase di compilazione:

```
./configure --with-debug ...
```

Dopo di cio', e' possibile configurare il livello di `debug` tramite la direttiva [error_log](ngx_core_module.xml#error_log) :

```
error_log /path/to/log debug;
```

La versione binaria di nginx per Windows e' sempre compilata con tale supporto, per cui in questo caso e' sufficiente configurare il livello di `debug` .

Si tenga presente che ridefinire il log senza anche specificare il livello di `debug` causa la disabilitazione del log. Nell'esempio che segue, la ridefinizione del log nel livello [server](http/ngx_http_core_module.xml#server) disabilita il log di `debug` per tale server:

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log;
        ...
```

Se ridefinire il log risulta necessario, per non incorrere in questo problema bisogna indicare esplicitamente il livello di `debug` :

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log debug;
        ...
```

E' pure possibile abilitare il `debug` solo per [indirizzi client specifici](ngx_core_module.xml#debug_connection) :

```
error_log /path/to/log;

events {
    debug_connection 192.168.1.1;
    debug_connection 192.168.10.0/24;
}
```

