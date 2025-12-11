# Module ngx_stream_proxy_module

**Revision:** 37  
**Language:** en


The `ngx_stream_proxy_module` module (1.9.0) allows proxying
data streams over TCP, UDP (1.9.13), and UNIX-domain sockets.

## Example Configuration {#example}

```
server {
    listen 127.0.0.1:12345;
    proxy_pass 127.0.0.1:8080;
}

server {
    listen 12345;
    proxy_connect_timeout 1s;
    proxy_timeout 1m;
    proxy_pass example.com:12345;
}

server {
    listen 53 udp reuseport;
    proxy_timeout 20s;
    proxy_pass dns.example.com:53;
}

server {
    listen [::1]:12345;
    proxy_pass unix:/tmp/stream.socket;
}
```

## Directives {#directives}



    address
    [transparent] |
    off

stream
server
1.9.2


Makes outgoing connections to a proxied server originate
from the specified local IP address.
Parameter value can contain variables (1.11.2).
The special value off cancels the effect
of the proxy_bind directive
inherited from the previous configuration level, which allows the
system to auto-assign the local IP address.



The transparent parameter (1.11.0) allows
outgoing connections to a proxied server originate
from a non-local IP address,
for example, from a real IP address of a client:

proxy_bind $remote_addr transparent;

In order for this parameter to work,
it is usually necessary to run nginx worker processes with the
superuser privileges.
On Linux it is not required (1.13.8) as if
the transparent parameter is specified, worker processes
inherit the CAP_NET_RAW capability from the master process.
It is also necessary to configure kernel routing table
to intercept network traffic from the proxied server.




on | off
off
stream
server
1.29.3


When enabled, makes the bind operation
at each connection attempt.




This directive is available as part of our
commercial subscription.





size
16k
stream
server
1.9.4


Sets the size of the buffer used for reading data
from the proxied server.
Also sets the size of the buffer used for reading data
from the client.




time
60s
stream
server


Defines a timeout for establishing a connection with a proxied server.




rate
0
stream
server
1.9.3


Limits the speed of reading the data from the proxied server.
The rate is specified in bytes per second.
The zero value disables rate limiting.
The limit is set per a connection, so if nginx simultaneously opens
two connections to the proxied server,
the overall rate will be twice as much as the specified limit.



Parameter value can contain variables (1.17.0).
It may be useful in cases where rate should be limited
depending on a certain condition:

map $slow $rate {
    1     4k;
    2     8k;
}

proxy_download_rate $rate;





on | off
off
stream
server
1.21.4


Enables or disables closing
each direction of a TCP connection independently (“TCP half-close”).
If enabled, proxying over TCP will be kept
until both sides close the connection.




on | off
on
stream
server


When a connection to the proxied server cannot be established, determines
whether a client connection will be passed to the next server.



Passing a connection to the next server can be limited by
the number of tries
and by time.




time
0
stream
server


Limits the time allowed to pass a connection to the
next server.
The 0 value turns off this limitation.




number
0
stream
server


Limits the number of possible tries for passing a connection to the
next server.
The 0 value turns off this limitation.




address

server


Sets the address of a proxied server.
The address can be specified as a domain name or IP address,
and a port:

proxy_pass localhost:12345;

or as a UNIX-domain socket path:

proxy_pass unix:/tmp/stream.socket;




If a domain name resolves to several addresses, all of them will be
used in a round-robin fashion.
In addition, an address can be specified as a
server group.



The address can also be specified using variables (1.11.3):

proxy_pass $upstream;

In this case, the server name is searched among the described
server groups,
and, if not found, is determined using a
.




on | off
off
stream
server
1.9.2


Enables the
PROXY
protocol for connections to a proxied server.




number
0
stream
server
1.15.7


Sets the number of client datagrams at which
binding between a client and existing UDP stream session is dropped.
After receiving the specified number of datagrams, next datagram
from the same client starts a new session.
The session terminates when all client datagrams are transmitted
to a proxied server and the expected number of
responses is received,
or when it reaches a timeout.




number

stream
server
1.9.13


Sets the number of datagrams expected from the proxied server
in response to a client datagram
if the UDP
protocol is used.
The number serves as a hint for session termination.
By default, the number of datagrams is not limited.



If zero value is specified, no response is expected.
However, if a response is received and the
session is still not finished, the response will be handled.




on | off
off
stream
server
1.15.8


Enables terminating all sessions to a proxied server
after it was removed from the group or marked as permanently unavailable.
This can occur because of
re-resolve
or with the API
DELETE
command.
A server can be marked as permanently unavailable if it is considered
unhealthy
or with the API
PATCH
command.
Each session is terminated when the next
read or write event is processed for the client or proxied server.




This directive is available as part of our
commercial subscription.





on | off
off
stream
server
1.15.6


Configures the “TCP keepalive” behavior
for outgoing connections to a proxied server.
By default, the operating system’s settings are in effect for the socket.
If the directive is set to the value “on”, the
SO_KEEPALIVE socket option is turned on for the socket.




on | off
off
stream
server


Enables the SSL/TLS protocol for connections to a proxied server.




file

stream
server


Specifies a file with the certificate in the PEM format
used for authentication to a proxied server.



Since version 1.21.0, variables can be used in the file name.




off

    max=N
    [inactive=time]
    [valid=time]
off
stream
server
1.27.4


Defines a cache that stores
SSL certificates and
secret keys
specified with variables.



The directive has the following parameters:



max


sets the maximum number of elements in the cache;
on cache overflow the least recently used (LRU) elements are removed;



inactive


defines a time after which an element is removed from the cache
if it has not been accessed during this time;
by default, it is 10 seconds;



valid


defines a time during which
an element in the cache is considered valid
and can be reused;
by default, it is 60 seconds.
Certificates that exceed this time will be reloaded or revalidated;



off


disables the cache.






Example:

proxy_ssl_certificate       $proxy_ssl_server_name.crt;
proxy_ssl_certificate_key   $proxy_ssl_server_name.key;
proxy_ssl_certificate_cache max=1000 inactive=20s valid=1m;





file

stream
server


The value
store:scheme:id
can be specified instead of the file (1.29.0),
which is used to load a secret key with a specified id
and OpenSSL provider registered URI scheme, such as
pkcs11.



Specifies a file with the secret key in the PEM format
used for authentication to a proxied server.



Since version 1.21.0, variables can be used in the file name.




ciphers
DEFAULT
stream
server


Specifies the enabled ciphers for connections to a proxied server.
The ciphers are specified in the format understood by the OpenSSL library.



The full list can be viewed using the
“openssl ciphers” command.




name value

stream
server
1.19.4


Sets arbitrary OpenSSL configuration
commands
when establishing a connection with the proxied server.

The directive is supported when using OpenSSL 1.0.2 or higher.




Several proxy_ssl_conf_command directives
can be specified on the same level.
These directives are inherited from the previous configuration level
if and only if there are
no proxy_ssl_conf_command directives
defined on the current level.




Note that configuring OpenSSL directly
might result in unexpected behavior.





file

stream
server


Specifies a file with revoked certificates (CRL)
in the PEM format used to verify
the certificate of the proxied server.




path

stream
server
1.27.2


Enables logging of proxied server connection SSL keys
and specifies the path to the key log file.
Keys are logged in the
SSLKEYLOGFILE
format compatible with Wireshark.




This directive is available as part of our
commercial subscription.





name
host from proxy_pass
stream
server


Allows overriding the server name used to
verify
the certificate of the proxied server and to be
passed through SNI
when establishing a connection with the proxied server.
The server name can also be specified using variables (1.11.3).



By default, the host part of the  address is used.




file

stream
server


Specifies a file with passphrases for
secret keys
where each passphrase is specified on a separate line.
Passphrases are tried in turn when loading the key.





    [SSLv2]
    [SSLv3]
    [TLSv1]
    [TLSv1.1]
    [TLSv1.2]
    [TLSv1.3]
TLSv1.2 TLSv1.3
stream
server


Enables the specified protocols for connections to a proxied server.




The TLSv1.3 parameter is used by default
since 1.23.4.





on | off
off
stream
server


Enables or disables passing of the server name through
TLS
Server Name Indication extension (SNI, RFC 6066)
when establishing a connection with the proxied server.




on | off
on
stream
server


Determines whether SSL sessions can be reused when working with
the proxied server.
If the errors
“digest check failed”
appear in the logs, try disabling session reuse.




file

stream
server


Specifies a file with trusted CA certificates in the PEM format
used to verify
the certificate of the proxied server.




on | off
off
stream
server


Enables or disables verification of the proxied server certificate.




number
1
stream
server


Sets the verification depth in the proxied server certificates chain.




timeout
10m
stream
server


Sets the timeout between two successive
read or write operations on client or proxied server connections.
If no data is transmitted within this time, the connection is closed.




rate
0
stream
server
1.9.3


Limits the speed of reading the data from the client.
The rate is specified in bytes per second.
The zero value disables rate limiting.
The limit is set per a connection, so if the client simultaneously opens
two connections,
the overall rate will be twice as much as the specified limit.



Parameter value can contain variables (1.17.0).
It may be useful in cases where rate should be limited
depending on a certain condition:

map $slow $rate {
    1     4k;
    2     8k;
}

proxy_upload_rate $rate;



