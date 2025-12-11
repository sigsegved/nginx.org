# Come contribuire

**Translator:** Angelo Papadia  
**Revision:** 1  
**Language:** it


## Ottenere i sorgenti {#getting_sources}

Il codice sorgente e' gestito tramite
[Mercurial](http://mercurial.selenic.com).
L'[archivio](http://hg.nginx.org/nginx) puo' essere
clonato con il comando:

```
hg clone http://hg.nginx.org/nginx
```

## Formattazione delle modifiche {#formatting_changes}

Il codice delle modifiche dovrebbe essere formattato secondo lo stile di nginx.
La formattazione non deve fare affidamento su caratteristiche proprie
dell'editor, dovrebbe invece seguire alcune regole base:

- la larghezza del testo non deve superare gli 80 caratteri
- l'indentazione va ottenuta con blocchi di quattro spazi
- non va usato il tab (tabulatore)
- in un file, i diversi blocchi logici di codice vanno separati con due linee vuote

E' bene esaminare il codice di nginx esistente, e cercare di riprodurne lo stile
di formattazione nel proprio codice: e' piu' facile che una modifica sia accettata
se lo stile e' simile a quello del resto del codice.

L'esecuzione di un commit sulle modifiche crea un
[changeset](http://mercurial.selenic.com/wiki/ChangeSet)
Mercurial; bisogna assicurarsi che siano corretti l'indirizzo
[e-mail](http://mercurial.selenic.com/wiki/QuickStart#Setting_a_username)
e il nome dell'autore delle modifiche.

Il messaggio di commit dovrebbe avere una breve descrizione su riga singola
(preferibilmente non piu' lunga di 67 caratteri),
seguita da una riga vuota e da una descrizione piu' lunga.
Il risultante changeset puo' essere ottenuto sotto forma di patch
tramite il comando `hg export`:

```
# HG changeset patch
# User Filipe Da Silva <username@example.com>
# Date 1368089668 -7200
#      Thu May 09 10:54:28 2013 +0200
# Node ID 2220de0521ca2c0b664a8ea1e201ce1cb90fd7a2
# Parent  822b82191940ef309cd1e6502f94d50d811252a1
Mail: removed surplus ngx_close_connection() call.

It is already called for a peer connection a few lines above.

diff -r 822b82191940 -r 2220de0521ca src/mail/ngx_mail_auth_http_module.c
--- a/src/mail/ngx_mail_auth_http_module.c      Wed May 15 15:04:49 2013 +0400
+++ b/src/mail/ngx_mail_auth_http_module.c      Thu May 09 10:54:28 2013 +0200
@@ -699,7 +699,6 @@ ngx_mail_auth_http_process_headers(ngx_m

                     p = ngx_pnalloc(s->connection->pool, ctx->err.len);
                     if (p == NULL) {
-                        ngx_close_connection(ctx->peer.connection);
                         ngx_destroy_pool(ctx->pool);
                         ngx_mail_session_internal_server_error(s);
                         return;
```

## Prima di proporre modifiche {#before_submitting}

E' bene tenere in considerazione alcuni punti:

- Le modifiche proposte dovrebbero funzionare correttamente sul piu' ampio
numero possibile di
[piattaforme supportate](../index.xml#tested_os_and_platforms).
- Bisogna spiegare chiaramente perche' e' necessaria la modifica proposta,
e se possibile fornire un esempio.

## Proporre modifiche {#submitting_changes}

Le proposte di modifica vanno inviate alla mailing list degli
[sviluppatori di nginx](../support.xml#nginx_devel).
L'estensione
[patchbomb](http://mercurial.selenic.com/wiki/PatchbombExtension)
e' la maniera preferibile e piu' comoda di sottoporre i changeset.

## Licenza {#license}

Se si sottopone una proposta di modifica, automaticamente al progetto
viene concesso il permesso di utilizzarla in base ad una opportuna
[licenza](../../LICENSE).
