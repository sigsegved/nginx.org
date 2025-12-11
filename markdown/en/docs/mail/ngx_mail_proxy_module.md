# Module ngx_mail_proxy_module

**Revision:** 6  
**Language:** en


## Directives {#directives}


size
4k|8k
mail
server


Sets the size of the buffer used for proxying.
By default, the buffer size is equal to one memory page.
Depending on a platform, it is either 4K or 8K.




on | off
off
mail
server


Indicates whether to pass the error message obtained during
the authentication on the backend to the client.



Usually, if the authentication in nginx is a success,
the backend cannot return an error.
If it nevertheless returns an error,
it means some internal error has occurred.
In such case the backend message can contain information
that should not be shown to the client.
However, responding with an error for the correct password
is a normal behavior for some POP3 servers.
For example, CommuniGatePro informs a user about
mailbox
overflow or other events by periodically outputting the
authentication
error.
The directive should be enabled in this case.




on | off
off
mail
server
1.19.8


Enables the
PROXY
protocol for connections to a backend.




on | off
off
mail
server
1.19.4


Enables or disables user authentication on the SMTP backend
using the AUTH command.



If XCLIENT is also enabled,
then the XCLIENT command will not send
the LOGIN parameter.




timeout
24h
mail
server


Sets the timeout between two successive
read or write operations on client or proxied server connections.
If no data is transmitted within this time, the connection is closed.




on | off
on
mail
server


Enables or disables the passing of the
XCLIENT
command with client parameters when connecting to the SMTP backend.



With XCLIENT, the MTA is able to write client information
to the log and apply various limitations based on this data.



If XCLIENT is enabled
then nginx passes the following commands when connecting to the backend:


EHLO with the
server name




XCLIENT




EHLO or HELO,
as passed by the client





If the name
found
by the client IP address points to the same address,
it is passed in the NAME parameter
of the XCLIENT command.
If the name could not be found, points to a different address,
or  is not specified,
the [UNAVAILABLE] is passed
in the NAME parameter.
If an error has occurred in the process of resolving,
the [TEMPUNAVAIL] value is used.



If XCLIENT is disabled
then nginx passes the EHLO command with the
server name
when connecting to the backend if the client has passed
EHLO,
or HELO with the server name, otherwise.


