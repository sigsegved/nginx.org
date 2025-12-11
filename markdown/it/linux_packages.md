# nginx: pacchetti Linux

**Translator:** Angelo Papadia  
**Revision:** 4  
**Language:** it


Attualmente sono disponibili pacchetti nginx per le seguenti distribuzioni
e versioni:

RHEL/CentOS:


| Versione |
| --- |
| 5.x |
| 6.x |

Debian:


| Versione | Nome in codice |
| --- | --- |
| 6.x | squeeze |
| 7.x | wheezy |

Ubuntu:


| Versione | Nome in codice |
| --- | --- |
| 10.04 | lucid |
| 11.10 | oneiric |
| 12.04 | precise |
| 12.10 | quantal |
| 13.04 | raring |

Per abilitare gli aggiornamenti automatici dei pacchetti Linux,
per la distribuzione RHEL/CentOS configurare l'archivio yum,
e per la distribuzione Debian/Ubuntu l'archivio apt.

## Pacchetti precompilati per la versione stabile {#stable}

Nel caso di RHEL/CentOS, per configurare l'archivio yum scegliere
l'opportuno pacchetto `nginx-release` dalla lista:


- [RHEL 5](http://nginx.org/packages/rhel/5/noarch/RPMS/nginx-release-rhel-5-0.el5.ngx.noarch.rpm)
- [RHEL 6](http://nginx.org/packages/rhel/6/noarch/RPMS/nginx-release-rhel-6-0.el6.ngx.noarch.rpm)
- [CentOS 5](http://nginx.org/packages/centos/5/noarch/RPMS/nginx-release-centos-5-0.el5.ngx.noarch.rpm)
- [CentOS 6](http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm)


Questo pacchetto contiene il file di configurazione di yum ed una chiave
PGP pubblica necessaria per autenticare i pacchetti RPM firmati.
Bisogna scaricarlo e installarlo, e quindi lanciare il seguente comando:

```
yum install nginx
```


In alternativa, la configurazione di un archivio puo' essere aggiunta
a mano, quindi senza installare il relativo pacchetto
`nginx-release`. Bisogna creare il file
`/etc/yum.repos.d/nginx.repo` con il contenuto seguente:


```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/OS/OSRELEASE/$basearch/
gpgcheck=0
enabled=1
```


Sostituire “`OS`” con “`rhel`” o
“`centos`”,
a seconda della distribuzione usata, e “`OSRELEASE`”
con “`5`” o “`6`”,
per le versioni 5.x o 6.x, rispettivamente.

Nel caso di Debian/Ubuntu, per autenticare la firma dell'archivio nginx
e per eliminare gli avvisi riguardanti l'assenza della chiave PGP che
vengono visualizzati durante l'installazione dei pacchetti di nginx,
bisogna aggiungere la chiave usata per firmare i pacchetti e l'archivio
nginx al keyring del programma `apt`; a tal proposito
bisogna scaricare [
questa chiave](http://nginx.org/keys/nginx_signing.key), ed aggiungerla al keyring di `apt`
tramite il seguente comando:

```
sudo apt-key add nginx_signing.key
```

Per Debian, bisogna sostituire *nome_in_codice* con il
nome in codice della distribuzione, e
aggiungere in coda al file `/etc/apt/sources.list` le righe seguenti:


```
deb http://nginx.org/packages/debian/ nome_in_codice nginx
deb-src http://nginx.org/packages/debian/ nome_in_codice nginx
```

Per Ubuntu, bisogna sostituire *nome_in_codice* con il
nome in codice della distribuzione, e
aggiungere in coda al file `/etc/apt/sources.list` le righe seguenti:


```
deb http://nginx.org/packages/ubuntu/ nome_in_codice nginx
deb-src http://nginx.org/packages/ubuntu/ nome_in_codice nginx
```

Sia per Debian, sia per Ubuntu, lanciare infine i seguenti comandi:

```
apt-get update
apt-get install nginx
```

## Pacchetti precompilati per la versione principale {#mainline}

Nel caso di RHEL/CentOS, per configurare l'archivio yum creare il file
`/etc/yum.repos.d/nginx.repo`
con il contenuto seguente:


```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/mainline/OS/OSRELEASE/$basearch/
gpgcheck=0
enabled=1
```


Sostituire “`OS`” con “`rhel`” o
“`centos`”,
a seconda della distribuzione usata, e “`OSRELEASE`”
con “`5`” o “`6`”,
per le versioni 5.x o 6.x, rispettivamente.

Nel caso di Debian/Ubuntu, per autenticare la firma dell'archivio nginx
e per eliminare gli avvisi riguardanti l'assenza della chiave PGP che
vengono visualizzati durante l'installazione dei pacchetti di nginx,
bisogna aggiungere la chiave usata per firmare i pacchetti e l'archivio
nginx al keyring del programma `apt`; a tal proposito
bisogna scaricare [
questa chiave](http://nginx.org/keys/nginx_signing.key), ed aggiungerla al keyring di `apt`
tramite il seguente comando:

```
sudo apt-key add nginx_signing.key
```

Per Debian, bisogna sostituire *nome_in_codice* con il
nome in codice della distribuzione, e
aggiungere in coda al file `/etc/apt/sources.list` le righe seguenti:


```
deb http://nginx.org/packages/mainline/debian/ nome_in_codice nginx
deb-src http://nginx.org/packages/mainline/debian/ nome_in_codice nginx
```

Per Ubuntu, bisogna sostituire *nome_in_codice* con il
nome in codice della distribuzione, e
aggiungere in coda al file `/etc/apt/sources.list` le righe seguenti:


```
deb http://nginx.org/packages/mainline/ubuntu/ nome_in_codice nginx
deb-src http://nginx.org/packages/mainline/ubuntu/ nome_in_codice nginx
```

Sia per Debian, sia per Ubuntu, lanciare infine i seguenti comandi:

```
apt-get update
apt-get install nginx
```

## Firme {#signatures}

I pacchetti RPM e gli archivi Debian/Ubuntu usano firme digitali per
verificare l'integrita' e l'origine dei pacchetti scaricati.
Per verificare la firma bisogna scaricare la
[chiave di firma di nginx](http://nginx.org/keys/nginx_signing.key)
e importarla nel keyring del programma `rpm` o `apt`:


- In Debian/Ubuntu:

```
sudo apt-key add nginx_signing.key
```
- In RHEL/CentOS:

```
sudo rpm --import nginx_signing.key
```

In Debian/Ubuntu le firme sono verificate per default,
invece in RHEL/CentOS e' necessario porre

```
gpgcheck=1
```
 nel file
`/etc/yum.repos.d/nginx.repo`.

Essendo tutti su un medesimo server, le nostre
[chiavi PGP](../en/pgp_keys.html) e i
pacchetti sono egualmente affidabili; e' comunque caldamente
consigliato verificare l'autenticita' delle chiavi PGP scaricate.
PGP ha il concetto di "rete di fiducia", con cui si intende
che una chiave e' firmata dalla chiave di qualcun altro,
che a sua volta e' firmata da un'altra chiave, e cosi' via;
grazie a cio' e' spesso possibile costruire una catena ininterrotta
da una chiave arbitraria alla chiave di qualcun altro che e'
conosciuto ed e' considerato affidabile, riuscendo quindi a stabilire
l'affidabilita' della prima chiave della catena.
Tale concetto e' descritto in dettaglio nel
[
GPG Mini Howto](http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto-1.html).
Le nostre chiavi hanno firme sufficienti a rendere relativamente
semplice la verifica dell'autenticita'.
