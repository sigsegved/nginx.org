# Module ngx_http_grpc_module

**Revision:** 15  
**Language:** en


The `ngx_http_grpc_module` module allows passing requests
to a gRPC server (1.13.10).
The module requires the
[ngx_http_v2_module](ngx_http_v2_module.html) module.

## Example Configuration {#example}

```
server {
    listen 9000;

    http2 on;

    location / {
        grpc_pass 127.0.0.1:9000;
    }
}
```

## Directives {#directives}


address

http
server
location
1.29.3


Defines conditions under which access to a gRPC server
is allowed or denied.
If all string parameters are not empty
and not equal to “0” then the access is allowed.
The conditions are evaluated each time
before a connection to a gRPC server is established.
Parameter values can contain variables:

geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;
    http2 on;

    location / {
        grpc_pass           localhost:9000;
        grpc_allow_upstream $allow;
        ...
    }
}





This directive is available as part of our
commercial subscription.






    address
    [transparent ] |
    off

http
server
location


Makes outgoing connections to a gRPC server originate
from the specified local IP address with an optional port.
Parameter value can contain variables.
The special value off cancels the effect
of the grpc_bind directive
inherited from the previous configuration level, which allows the
system to auto-assign the local IP address and port.



The transparent parameter allows
outgoing connections to a gRPC server originate
from a non-local IP address,
for example, from a real IP address of a client:

grpc_bind $remote_addr transparent;

In order for this parameter to work,
it is usually necessary to run nginx worker processes with the
superuser privileges.
On Linux it is not required as if
the transparent parameter is specified, worker processes
inherit the CAP_NET_RAW capability from the master process.
It is also necessary to configure kernel routing table
to intercept network traffic from the gRPC server.




on | off
off
http
server
location
1.29.3


When enabled, makes the bind operation
at each connection attempt.




This directive is available as part of our
commercial subscription.





size
4k|8k
http
server
location


Sets the size of the buffer used for reading the response
received from the gRPC server.
The response is passed to the client synchronously, as soon as it is received.




time
60s
http
server
location


Defines a timeout for establishing a connection with a gRPC server.
It should be noted that this timeout cannot usually exceed 75 seconds.




field

http
server
location


By default,
nginx does not pass the header fields Date,
Server, and
X-Accel-... from the response of a gRPC
server to a client.
The grpc_hide_header directive sets additional fields
that will not be passed.
If, on the contrary, the passing of fields needs to be permitted,
the  directive can be used.




field ...

http
server
location


Disables processing of certain response header fields from the gRPC server.
The following fields can be ignored: X-Accel-Redirect
and X-Accel-Charset.



If not disabled, processing of these header fields has the following
effect:



X-Accel-Redirect performs an
internal
redirect to the specified URI;



X-Accel-Charset sets the desired

of a response.







on | off
off
http
server
location


Determines whether gRPC server responses with codes greater than or equal
to 300 should be passed to a client
or be intercepted and redirected to nginx for processing
with the  directive.





    error |
    timeout |
    denied |
    invalid_header |
    http_500 |
    http_502 |
    http_503 |
    http_504 |
    http_403 |
    http_404 |
    http_429 |
    non_idempotent |
    off
    ...
error timeout
http
server
location


Specifies in which cases a request should be passed to the next server:


error
an error occurred while establishing a connection with the
server, passing a request to it, or reading the response header;

timeout
a timeout has occurred while establishing a connection with the
server, passing a request to it, or reading the response header;

denied
the server denied
the connection (1.29.3);


This parameter is available as part of our
commercial subscription.




invalid_header
a server returned an empty or invalid response;

http_500
a server returned a response with the code 500;

http_502
a server returned a response with the code 502;

http_503
a server returned a response with the code 503;

http_504
a server returned a response with the code 504;

http_403
a server returned a response with the code 403;

http_404
a server returned a response with the code 404;

http_429
a server returned a response with the code 429;

non_idempotent
normally, requests with a
non-idempotent
method
(POST, LOCK, PATCH)
are not passed to the next server
if a request has been sent to an upstream server;
enabling this option explicitly allows retrying such requests;


off
disables passing a request to the next server.





One should bear in mind that passing a request to the next server is
only possible if nothing has been sent to a client yet.
That is, if an error or timeout occurs in the middle of the
transferring of a response, fixing this is impossible.



The directive also defines what is considered an
unsuccessful
attempt of communication with a server.
The cases of error, timeout,
denied and
invalid_header are always considered unsuccessful attempts,
even if they are not specified in the directive.
The cases of http_500, http_502,
http_503, http_504,
and http_429 are
considered unsuccessful attempts only if they are specified in the directive.
The cases of http_403 and http_404
are never considered unsuccessful attempts.



Passing a request to the next server can be limited by
the number of tries
and by time.




time
0
http
server
location


Limits the time during which a request can be passed to the
next server.
The 0 value turns off this limitation.




number
0
http
server
location


Limits the number of possible tries for passing a request to the
next server.
The 0 value turns off this limitation.




address

location
if in location


Sets the gRPC server address.
The address can be specified as a domain name or IP address,
and a port:

grpc_pass localhost:9000;

or as a UNIX-domain socket path:

grpc_pass unix:/tmp/grpc.socket;

Alternatively, the “grpc://” scheme can be used:

grpc_pass grpc://127.0.0.1:9000;

To use gRPC over SSL, the “grpcs://” scheme should be used:

grpc_pass grpcs://127.0.0.1:443;




If a domain name resolves to several addresses, all of them will be
used in a round-robin fashion.
In addition, an address can be specified as a
server group.



Parameter value can contain variables (1.17.8).
In this case, if an address is specified as a domain name,
the name is searched among the described
server groups,
and, if not found, is determined using a
.




field

http
server
location


Permits passing otherwise disabled header
fields from a gRPC server to a client.




time
60s
http
server
location


Defines a timeout for reading a response from the gRPC server.
The timeout is set only between two successive read operations,
not for the transmission of the whole response.
If the gRPC server does not transmit anything within this time,
the connection is closed.




on | off
off
http
server
location
1.29.3


Enables or disables creation of a separate request instance
for each gRPC server.
By default, a single request is used for all gRPC servers.
If enabled, a separate request instance is created,
allowing per-server request customization.
For example, the server-specific Host request header field
can be set:

grpc_request_dynamic on;
grpc_set_header      Host $upstream_last_server_name;





This directive is available as part of our
commercial subscription.





time
60s
http
server
location


Sets a timeout for transmitting a request to the gRPC server.
The timeout is set only between two successive write operations,
not for the transmission of the whole request.
If the gRPC server does not receive anything within this time,
the connection is closed.




field value
Content-Length $content_length
http
server
location


Allows redefining or appending fields to the request header
passed to the gRPC server.
The value can contain text, variables, and their combinations.
These directives are inherited from the previous configuration level
if and only if there are no grpc_set_header directives
defined on the current level.



If the value of a header field is an empty string then this
field will not be passed to a gRPC server:

grpc_set_header Accept-Encoding "";





on | off
off
http
server
location
1.15.6


Configures the “TCP keepalive” behavior
for outgoing connections to a gRPC server.
By default, the operating system’s settings are in effect for the socket.
If the directive is set to the value “on”, the
SO_KEEPALIVE socket option is turned on for the socket.




file

http
server
location


Specifies a file with the certificate in the PEM format
used for authentication to a gRPC SSL server.



Since version 1.21.0, variables can be used in the file name.




off

    max=N
    [inactive=time]
    [valid=time]
off
http
server
location
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

grpc_ssl_certificate       $grpc_ssl_server_name.crt;
grpc_ssl_certificate_key   $grpc_ssl_server_name.key;
grpc_ssl_certificate_cache max=1000 inactive=20s valid=1m;





file

http
server
location


Specifies a file with the secret key in the PEM format
used for authentication to a gRPC SSL server.



The value
engine:name:id
can be specified instead of the file,
which loads a secret key with a specified id
from the OpenSSL engine name.



The value
store:scheme:id
can be specified instead of the file (1.29.0),
which is used to load a secret key with a specified id
and OpenSSL provider registered URI scheme, such as
pkcs11.



Since version 1.21.0, variables can be used in the file name.




ciphers
DEFAULT
http
server
location


Specifies the enabled ciphers for requests to a gRPC SSL server.
The ciphers are specified in the format understood by the OpenSSL library.



The full list can be viewed using the
“openssl ciphers” command.




name value

http
server
location
1.19.4


Sets arbitrary OpenSSL configuration
commands
when establishing a connection with the gRPC SSL server.

The directive is supported when using OpenSSL 1.0.2 or higher.




Several grpc_ssl_conf_command directives
can be specified on the same level.
These directives are inherited from the previous configuration level
if and only if there are
no grpc_ssl_conf_command directives
defined on the current level.




Note that configuring OpenSSL directly
might result in unexpected behavior.





file

http
server
location


Specifies a file with revoked certificates (CRL)
in the PEM format used to verify
the certificate of the gRPC SSL server.




path

http
server
location
1.27.2


Enables logging of gRPC SSL server connection SSL keys
and specifies the path to the key log file.
Keys are logged in the
SSLKEYLOGFILE
format compatible with Wireshark.




This directive is available as part of our
commercial subscription.





name
host from grpc_pass
http
server
location


Allows overriding the server name used to
verify
the certificate of the gRPC SSL server and to be
passed through SNI
when establishing a connection with the gRPC SSL server.



By default, the host part from  is used.




file

http
server
location


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
http
server
location


Enables the specified protocols for requests to a gRPC SSL server.




The TLSv1.3 parameter is used by default
since 1.23.4.





on | off
off
http
server
location


Enables or disables passing of the server name through
TLS
Server Name Indication extension (SNI, RFC 6066)
when establishing a connection with the gRPC SSL server.




on | off
on
http
server
location


Determines whether SSL sessions can be reused when working with
the gRPC server.
If the errors
“digest check failed”
appear in the logs, try disabling session reuse.




file

http
server
location


Specifies a file with trusted CA certificates in the PEM format
used to verify
the certificate of the gRPC SSL server.




on | off
off
http
server
location


Enables or disables verification of the gRPC SSL server certificate.




number
1
http
server
location


Sets the verification depth in the gRPC SSL server certificates chain.


