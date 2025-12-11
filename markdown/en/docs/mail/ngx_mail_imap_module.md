# Module ngx_mail_imap_module

**Revision:** 7  
**Language:** en


## Directives {#directives}


method ...
plain
mail
server


Sets permitted methods of authentication for IMAP clients.
Supported methods are:


plain

LOGIN,
AUTH=PLAIN


login

AUTH=LOGIN


cram-md5

AUTH=CRAM-MD5.
In order for this method to work, the password must be stored unencrypted.


external

AUTH=EXTERNAL (1.11.6).






Plain text authentication methods
(the LOGIN command, AUTH=PLAIN,
and AUTH=LOGIN) are always enabled,
though if the plain and login methods
are not specified,
AUTH=PLAIN and AUTH=LOGIN
will not be automatically included in .




extension ...
IMAP4 IMAP4rev1 UIDPLUS
mail
server


Sets the
IMAP protocol
extensions list that is passed to the client in response to
the CAPABILITY command.
The authentication methods specified in the  directive and
STARTTLS
are automatically added to this list depending on the
 directive value.



It makes sense to specify the extensions
supported by the IMAP backends
to which the clients are proxied (if these extensions are related to commands
used after the authentication, when nginx transparently proxies a client
connection to the backend).



The current list of standardized extensions is published at
www.iana.org.




size
4k|8k
mail
server


Sets the size of the buffer used for reading IMAP commands.
By default, the buffer size is equal to one memory page.
This is either 4K or 8K, depending on a platform.


