# Metodi di processo delle connessioni

**Translator:** Angelo Papadia  
**Revision:** 2  
**Language:** it


nginx supporta diversi metodi di processo delle connessioni.
La disponibilita' di un particolare metodo dipende dalla piattaforma usata;
su piattaforme che supportano piu' di un metodo, nginx in genere
e' in grado di selezionare automaticamente il metodo piu' efficiente.
Comunque, se necessario, e' possibile scegliere esplicitamente il metodo
di processo delle connessioni tramite la direttiva
[](ngx_core_module.xml#use).

I metodi di processo delle connessioni sono i seguenti:

- select—metodo standard.
Il relativo modulo e' compilato automaticamente se la piattaforma non
rende possibile l'uso di metodi piu' efficienti.
E' possibile usare i parametri di configurazione
--with-select_module e
--without-select_module
per abilitare o disabilitare esplicitamente la compilazione di tale modulo.
- poll—metodo standard.
Il relativo modulo e' compilato automaticamente se la piattaforma non
rende possibile l'uso di metodi piu' efficienti.
E' possibile usare i parametri di configurazione
--with-poll_module e
--without-poll_module
per abilitare o disabilitare esplicitamente la compilazione di tale modulo.
- kqueue—metodo efficiente usato su
FreeBSD 4.1+, OpenBSD 2.9+, NetBSD 2.0, e Mac OS X.
- epoll—metodo efficiente usato su
Linux 2.6+.

Alcune distribuzioni piu' vecchie, ad esempio SuSE 8.2, forniscono
patch che rendono possibile l'uso di questo modulo su kernel 2.4.
- rtsig—real time signals, metodo efficiente usato su
Linux 2.2.19+.
Per default, la coda di eventi del sistema e' limitata a 1024 segnali;
su server particolarmente carichi puo' risultare necessario incrementare
tale limite, intervenendo sul parametro del kernel
/proc/sys/kernel/rtsig-max .
Comunque, a partire da Linux 2.6.6-mm2 tale parametro non e' piu' disponibile
e ciascun processo dispone della propria coda di eventi.
La dimensione di ciascuna coda e' definita da RLIMIT_SIGPENDING
e puo' essere modificata tramite il parametro
.



In caso di overflow, nginx scarta del tutto la coda e passa all'uso del
metodo di processo poll sinche' la situazione non
torna normale.
- /dev/poll—metodo efficiente usato su
Solaris 7 11/99+, HP/UX 11.22+ (eventport), IRIX 6.5.15+,
e Tru64 UNIX 5.1A+.
- eventport—event ports, metodo efficiente usato su
Solaris 10.
