# Module ngx_http_auth_require_module

**Revision:** 1  
**Language:** en


The `ngx_http_auth_require_module` module (1.29.0)
implements variable-based client authorization.
It can also use variables
provided by other access modules such as
[ngx_http_auth_request_module](ngx_http_auth_request_module.html)
or
[ngx_http_auth_oidc_module](ngx_http_auth_request_module.html).

> **Note:** This module is available as part of our
commercial subscription.

## Example Configuration {#example}

```
http {
    oidc_provider my_idp {
        ...
    }

    map $oidc_claim_role $admin_role {
        "admin" 1;
    }

    server {
        auth_oidc my_idp;

        location /admin {
            auth_require $admin_role;
        }
    }
}
```

## Directives {#directives}



    $value ...
    [error=4xx |
                              5xx]

off
http
server
location
limit_except


Enables authorization based on the specified variables.
The access is allowed only if all the variables are not
empty and are not equal to “0”.
Otherwise, the module returns 403 code, which can be
overridden by the error parameter.
Several auth_require directives can be used to return
different error codes.


