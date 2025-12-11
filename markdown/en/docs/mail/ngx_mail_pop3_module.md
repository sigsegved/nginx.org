# Module ngx_mail_pop3_module

**Revision:** 5  
**Language:** en


## Directives {#directives}


method ...
plain
mail
server


Sets permitted methods of authentication for POP3 clients.
Supported methods are:


plain

USER/PASS,
AUTH PLAIN,
AUTH LOGIN


apop

APOP.
In order for this method to work, the password must be stored unencrypted.


cram-md5

AUTH CRAM-MD5.
In order for this method to work, the password must be stored unencrypted.


external

AUTH EXTERNAL (1.11.6).






Plain text authentication methods
(USER/PASS, AUTH PLAIN,
and AUTH LOGIN) are always enabled,
though if the plain method is not specified,
AUTH PLAIN and AUTH LOGIN
will not be automatically included in .




extension ...
TOP USER UIDL
mail
server


Sets the
POP3 protocol
extensions list that is passed to the client in response to
the CAPA command.
The authentication methods specified in the  directive
(SASL extension) and
STLS
are automatically added to this list depending on the
 directive value.



It makes sense to specify the extensions
supported by the POP3 backends
to which the clients are proxied (if these extensions are related to commands
used after the authentication, when nginx transparently proxies the client
connection to the backend).



The current list of standardized extensions is published at
www.iana.org.


