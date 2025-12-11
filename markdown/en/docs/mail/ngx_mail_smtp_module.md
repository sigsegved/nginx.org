# Module ngx_mail_smtp_module

**Revision:** 8  
**Language:** en


## Directives {#directives}


method ...
plain login
mail
server


Sets permitted methods of
SASL authentication
for SMTP clients.
Supported methods are:


plain

AUTH PLAIN


login

AUTH LOGIN


cram-md5

AUTH CRAM-MD5.
In order for this method to work, the password must be stored unencrypted.


external

AUTH EXTERNAL (1.11.6).


none

Authentication is not required.






Plain text authentication methods
(AUTH PLAIN and AUTH LOGIN)
are always enabled,
though if the plain and login methods
are not specified,
AUTH PLAIN and AUTH LOGIN
will not be automatically included in .




extension ...

mail
server


Sets the SMTP protocol extensions list
that is passed to the client in response to the
EHLO command.
The authentication methods specified in the  directive and
STARTTLS
are automatically added to this list depending on the
 directive value.



It makes sense to specify the extensions
supported by the MTA
to which the clients are proxied (if these extensions are related to commands
used after the authentication, when nginx transparently proxies the client
connection to the backend).



The current list of standardized extensions is published at
www.iana.org.




size
4k|8k
mail
server


Sets the size of the buffer used for reading SMTP commands.
By default, the buffer size is equal to one memory page.
This is either 4K or 8K, depending on a platform.




time
0
mail
server


Allows setting a delay before sending an SMTP greeting
in order to reject clients who fail to wait for the greeting before
sending SMTP commands.


