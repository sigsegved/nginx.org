# nginx

**Translator:** Angelo Papadia  
**Revision:** 11  
**Language:** it


nginx [engine x] e' un server HTTP e reverse proxy,
nonche' un server mail proxy, scritto da
[Igor Sysoev](http://sysoev.ru/en/).
Per molto tempo e' stato usato principalmente per alcuni
siti russi ad alto carico, ad esempio
[Yandex](http://www.yandex.ru),
[Mail.Ru](http://www.mail.ru),
[VKontakte](http://vkontakte.ru) e
[Rambler](http://www.rambler.ru);
in base ai dati di Netcraft, nell'ottobre 2013 nginx
e' il server HTTP o reverse proxy del
[15.08%
dei siti a maggiore carico](http://news.netcraft.com/archives/2013/10/02/october-2013-web-server-survey.html).
Alcuni casi di successo sono:
[Netflix](https://signup.netflix.com/openconnect/software),
[FastMail.FM](http://blog.fastmail.fm/2007/01/04/webimappop-frontend-proxies-changed-to-nginx/).

La documentazione ed i sorgenti sono distribuiti in base alla
[licenza BSD con 2 clausole](../LICENSE).

## Caratteristiche principali del server HTTP {#basic_http_features}

- Servizio di file statici e
[index](docs/http/ngx_http_index_module.html),
[autoindexing](docs/http/ngx_http_autoindex_module.html);
[cache dei descrittori dei file aperti](docs/http/ngx_http_core_module.xml#open_file_cache);
- [Reverse proxy accelerato
con cache](docs/http/ngx_http_proxy_module.html);
[semplice bilanciamento
di carico e load balancing](docs/http/ngx_http_upstream_module.html);
- Supporto accelerato con cache di server
[FastCGI](docs/http/ngx_http_fastcgi_module.html),
uwsgi, SCGI, e
[memcached](docs/http/ngx_http_memcached_module.html);
[semplice bilanciamento
di carico e load balancing](docs/http/ngx_http_upstream_module.html);
- Architettura modulare.
Filtri per
[gzip](docs/http/ngx_http_gzip_module.html),
intervalli di byte, risposte a blocchi,
[XSLT](docs/http/ngx_http_xslt_module.html),
[SSI](docs/http/ngx_http_ssi_module.html),
e filtro per la [
trasformazione d'immagini](docs/http/ngx_http_image_filter_module.html).
Inclusioni multiple di SSI in una stessa pagina possono essere
processate in parallelo se sono gestite da server proxy o FastCGI;
- [Supporto a SSL e TLS SNI
](docs/http/ngx_http_ssl_module.html).

## Caratteristiche ulteriori del server HTTP {#other_http_features}

- [server virtuali](docs/http/request_processing.html)
name-based e IP-based;
- Supporto a connessioni
[keep-alive](docs/http/ngx_http_core_module.xml#keepalive_timeout)
e pipelined;
- Configurazione flessibile;
- [Caricamento di una nuova
configurazione ](docs/control.xml#reconfiguration) e [
aggiornamento dell'eseguibile](docs/control.xml#upgrade) senza interruzione di servizio ai client;
- [Access log in vari
formati](docs/http/ngx_http_log_module.xml#log_format), [log con buffer
](docs/http/ngx_http_log_module.xml#access_log), e [veloce rotazione dei log](docs/control.xml#logs);
- [Redirezione](docs/http/ngx_http_core_module.xml#error_page)
dei codici d'errore 3xx-5xx;
- Modulo di rewrite:
[trasformazione delle URI
con uso di espressioni regolari](docs/http/ngx_http_rewrite_module.html);
- [Esecuzione di funzioni differenti
](docs/http/ngx_http_rewrite_module.xml#if) a seconda dell'
[indirizzo del client](docs/http/ngx_http_geo_module.html);
- Controllo d'accesso in base a
[indirizzo IP del client](docs/http/ngx_http_access_module.html), a
[
password (HTTP Basic authentication)](docs/http/ngx_http_auth_basic_module.html), e al
[risultato di una sottorichiesta](docs/http/ngx_http_auth_request_module.html);
- Validazione del
[referer HTTP](docs/http/ngx_http_referer_module.html);
- Metodi [PUT, DELETE, MKCOL, COPY,
e MOVE](docs/http/ngx_http_dav_module.html);
- Streaming
[FLV](docs/http/ngx_http_flv_module.html) e
[MP4](docs/http/ngx_http_mp4_module.html);
- [
Limitazione della velocita' del flusso di risposta](docs/http/ngx_http_core_module.xml#limit_rate);
- Limitazione del numero di
[connessioni](docs/http/ngx_http_limit_conn_module.html) o
[richieste](docs/http/ngx_http_limit_req_module.html)
simultanee da un dato indirizzo;
- [Perl embedded](docs/http/ngx_http_perl_module.html).

## Caratteristiche del server mail proxy {#mail_proxy_server_features}

- Redirezione dell'utente verso server
[IMAP](docs/mail/ngx_mail_imap_module.html)
o
[POP3](docs/mail/ngx_mail_pop3_module.html)
tramite un server esterno di
[autenticazione](docs/mail/ngx_mail_auth_http_module.html)
HTTP;
- Autenticazione dell'utente tramite un server esterno di
[autenticazione](docs/mail/ngx_mail_auth_http_module.html)
e redirezione della connessione verso un server
[SMTP](docs/mail/ngx_mail_smtp_module.html);
- Metodi di autenticazione:


- [POP3](docs/mail/ngx_mail_pop3_module.xml#pop3_auth):
USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
- [IMAP](docs/mail/ngx_mail_imap_module.xml#imap_auth):
LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
- [SMTP](docs/mail/ngx_mail_smtp_module.xml#smtp_auth):
AUTH LOGIN/PLAIN/CRAM-MD5;
- supporto a
[SSL](docs/mail/ngx_mail_ssl_module.html);
- supporto a
[STARTTLS
e STLS](docs/mail/ngx_mail_ssl_module.xml#starttls).

## Architettura e scalabilita' {#architecture_and_scalability}

- Un processo master e numerosi processi worker;
i processi worker girano con un utente non privilegiato;
- [Supporto](docs/events.html) a
kqueue (FreeBSD 4.1+),
epoll (Linux 2.6+), segnali rt (Linux 2.2.19+),
/dev/poll (Solaris 7 11/99+), event ports (Solaris 10),
select, e poll;
- Supporto alle differenti funzionalita' di kqueue, fra cui EV_CLEAR, EV_DISABLE
(per disabilitare temporaneamente eventi), NOTE_LOWAT, EV_EOF,
numero di dati disponibili, codici d'errore;
- supporto a sendfile (FreeBSD 3.1+, Linux 2.2+, Mac OS X 10.5+), sendfile64 (Linux 2.4.21+),
e sendfilev (Solaris 8 7/01+);
- [File AIO](docs/http/ngx_http_core_module.xml#aio)
(FreeBSD 4.3+, Linux 2.6.22+);
- [DIRECTIO](docs/http/ngx_http_core_module.xml#directio)
(FreeBSD 4.4+, Linux 2.4+, Solaris 2.6+, Mac OS X);
- [supporto](docs/http/ngx_http_core_module.xml#listen) a
Accept-filters (FreeBSD 4.1+, NetBSD 5.0+) e TCP_DEFER_ACCEPT (Linux 2.4+);
- 10000 connessioni HTTP keep-alive inattive richiedono circa 2.5M di memoria;
- Le operazioni di copia di dati risultano minime.

## Piattaforme e sistemi operativi testati {#tested_os_and_platforms}

- FreeBSD 3—10 / i386; FreeBSD 5—10 / amd64;
- Linux 2.2—3 / i386; Linux 2.6—3 / amd64;
- Solaris 9 / i386, sun4u; Solaris 10 / i386, amd64, sun4v;
- AIX 7.1 / powerpc;
- HP-UX 11.31 / ia64;
- Mac OS X / ppc, i386;
- Windows XP, Windows Server 2003.
