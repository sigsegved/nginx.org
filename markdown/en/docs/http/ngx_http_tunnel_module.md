# Module ngx_http_tunnel_module

**Revision:** 1  
**Language:** en


The `ngx_http_tunnel_module` (1.29.3) handles
[CONNECT
requests](https://datatracker.ietf.org/doc/html/rfc9110#section-9.3.6)
and establishes an end-to-end virtual connection.

> **Note:** This module is available as part of our
commercial subscription.

## Example Configuration {#example}

```
http {

    map $request_port $allow_port {
        443            1;
    }

    map $host $allow_host {
        hostnames;

        example.org    1;
        *.example.org  1;
    }

    server {
        listen 8000;

        resolver dns.example.com;

        if ($allow_port != 1) {
            return 502;
        }

        if ($allow_host != 1) {
            return 502;
        }

        tunnel_pass;
    }
}
```

## Directives {#directives}


string ...

http
server
location


Defines conditions under which access to the backend server
is allowed or denied.
If all string parameters are not empty
and not equal to “0” then the access is allowed.
The conditions are evaluated each time
before a connection to a backend server is established.
Parameter values can contain variables:

geo $upstream_last_addr $allow {
    volatile;
    10.10.0.0/24        1;
}

server {
    listen 127.0.0.1:8080;

    tunnel_pass;
    tunnel_allow_upstream $allow;
}






    address |
    off

http
server
location


Makes outgoing connections to a backend server originate
from the specified local IP address with an optional port.
Parameter value can contain variables.
The special value off cancels the effect
of the tunnel_bind directive
inherited from the previous configuration level, which allows the
system to auto-assign the local IP address and port.




on | off
off
http
server
location


When enabled, makes the  operation
at each connection attempt:

geo $upstream_last_addr $bind_addr {
    volatile;
    10.0.0.0/24    10.0.0.1;
    192.168.0.0/24  192.168.0.1;
}

tunnel_bind         $bind_addr;
tunnel_bind_dynamic on;





size
16k
http
server
location


Sets the size of the buffer used for reading data
from the backend server.
Also sets the size of the buffer used for reading data
from the client.




time
60s
http
server
location


Defines a timeout for establishing a connection with a backend server.
It should be noted that this timeout cannot usually exceed 75 seconds.





    error |
    timeout |
    denied |
    off
    ...
error timeout
http
server
location


Specifies in which cases a request should be passed to the next server:


error
an error occurred while establishing a connection with the
server or reading data from the server;

timeout
a timeout has occurred while establishing a connection with the
server, passing a request to it, or reading data from the server;

denied
the server denied
the connection;

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
and denied
are always considered unsuccessful attempts,
even if they are not specified in the directive.



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




[address]

server
location
if in location


Enables handling of CONNECT requests and sets the address of a backend server.
By default, the address is
$host:$request_port and is taken from the client request.
In most cases, tunnel_pass does not require
configuring any arguments.



The address can be specified as a domain name or IP address,
and a port:

tunnel_pass localhost:9000;

or as a UNIX-domain socket path:

tunnel_pass unix:/tmp/backend.socket;




If a domain name resolves to several addresses, all of them will be
used in a round-robin fashion.
In addition, an address can be specified as a
server group.



Parameter value can contain variables.
In this case, if an address is specified as a domain name,
the name is searched among the described
server groups,
and, if not found, is determined using a
.




time
60s
http
server
location


Sets the timeout between two successive read or write operations
on client or backend server connections. 
If no data is transmitted within this time, the connection is closed.




size
0
http
server
location


If the directive is set to a non-zero value, nginx will try to
minimize the number
of send operations on outgoing connections to a backend server by using either
NOTE_LOWAT flag of the
 method,
or the SO_SNDLOWAT socket option,
with the specified size.



This directive is ignored on Linux, Solaris, and Windows.




time
60s
http
server
location


Sets a timeout for transmitting a request to the backend server.
The timeout is set only between two successive write operations,
not for the transmission of the whole request.
If the backend server does not receive anything within this time,
the connection is closed.




on | off
off
http
server
location


Configures the “TCP keepalive” behavior
for outgoing connections to a backend server.
By default, the operating system’s settings are in effect for the socket.
If the directive is set to the value “on”, the
SO_KEEPALIVE socket option is turned on for the socket.


