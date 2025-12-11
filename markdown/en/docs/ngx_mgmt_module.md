# Module ngx_mgmt_module

**Revision:** 2  
**Language:** en


The `ngx_mgmt_module` module enables
NGINX Plus license verification and usage reporting.
This is mandatory for each NGINX Plus instance since 1.27.2 (
[NGINX Plus R33](https://docs.nginx.com/nginx/releases/#r33)).

A JWT license file named `license.jwt`
should be located at
`/etc/nginx/` for Linux or
`/usr/local/etc/nginx/` for FreeBSD
or at the path specified by the  directive.
The license file is available from
[MyF5](https://my.f5.com).

Usage report is sent directly or via proxy
to F5 licensing endpoint
every hour using the
secure connection.
Optionally, in network-restricted environments
reporting can be configured to
[F5 NGINX
Instance Manager](https://docs.nginx.com/nginx-management-suite/about/) from which the report can be sent
to F5 licensing endpoint.

By default, if the initial usage report
is not received by F5 licensing endpoint, nginx will stop processing traffic.

Automatic license renewal is supported since 1.29.0
([NGINX Plus R35](https://docs.nginx.com/nginx/releases/#r35))
for instances that report directly to the F5 licensing endpoint.
On renewal, NGINX downloads the updated JWT from F5 licensing endpoint
and applies it without
configuration [reload](switches.html).
The updated license is stored
in the state_path directory.

> **Note:** This module is available as part of our
commercial subscription.

## Example Configuration {#example}

```
mgmt {
    # in case if custom path is required
    license_token custom/file/path/license.jwt;

    # in case of reporting to NGINX Instance Manager
    usage_report endpoint=NIM_FQDN;
}
```

## Directives {#directives}




main


Provides the configuration file context in which
usage reporting and license management directives
are specified.




on | off
on
mgmt
1.27.2


Enables or disables the 180-day grace period
for sending the initial usage report.



The initial usage report is sent immediately
upon nginx first start after installation.
By default, if the initial report is not received by F5 licensing endpoint,
nginx stops processing traffic until the report is successfully delivered.
Setting the directive value to off enables
the 180-day grace period during which
the initial usage report must be received by F5 licensing endpoint.




file
license.jwt
mgmt
1.27.2


Specifies a JWT license file.
By default, the license.jwt file is expected to be at
/etc/nginx/ for Linux or at
/usr/local/etc/nginx/ for FreeBSD.




host:port

mgmt
1.27.4


Sets the HTTP CONNECT proxy
used for sending the usage report.




string

mgmt
1.27.4


Sets the user name used for authentication on
the proxy.




string

mgmt
1.27.4


Sets the password used for authentication on
the proxy.



The password is sent unencrypted by default.
If the proxy supports TLS, the connection to the proxy can be
protected with the stream
module:

mgmt {
    proxy          127.0.0.1:8080;
    proxy_username <name>;
    proxy_password <password>;
}

stream {
    server {
        listen 127.0.0.1:8080;
        
        proxy_ssl                     on;
        proxy_ssl_verify              on;
        proxy_ssl_trusted_certificate <proxy_ca_file>;

        proxy_pass <proxy_host>:<proxy_port>;
    }
}






    address ...
    [valid=time]
    [ipv4=on|off]
    [ipv6=on|off]
    [status_zone=zone]

mgmt


Configures name servers used to resolve usage reporting endpoint name.
By default, the system resolver is used.



See  for details.




file

mgmt


Specifies a file with revoked certificates (CRL)
in the PEM format used to verify
the certificate of the usage reporting endpoint.




file
system CA bundle
mgmt


Specifies a file with trusted CA certificates in the PEM format
used to verify
the certificate of the usage reporting endpoint.




on | off
on
mgmt


Enables or disables verification of the usage reporting endpoint certificate.




Before 1.27.2, the default value was off.





path

mgmt
1.27.2


Defines a directory for storing state files
(nginx-mgmt-*)
created by the ngx_mgmt_module module.
The default directory
for Linux is /var/lib/nginx/state,
for FreeBSD is /var/db/nginx/state.




 [endpoint=address]
         [interval=time]
endpoint=product.connect.nginx.com interval=1h
mgmt


Sets the address and port
of the usage reporting endpoint.
The interval parameter sets an interval between
two consecutive reports.

Before 1.27.2, the default values were
nginx-mgmt.local and
30m.



