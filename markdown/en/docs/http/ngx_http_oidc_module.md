# Module ngx_http_oidc_module

**Revision:** 1  
**Language:** en


The `ngx_http_oidc_module` module (1.27.4)
implements authentication as a Relying Party in OpenID Connect using the
[
Authorization Code Flow](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth).

The module expects the OpenID Provider's configuration to be available via
[
metadata](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) and requires dynamic
[resolver](ngx_http_core_module.xml#resolver).

The module can be combined with other access modules
via the [](ngx_http_core_module.xml#satisfy) directive.
Note that the module may still block requests even with
`satisfy any;`
as an OpenID Provider might not redirect the user back to nginx.

> **Note:** This module is available as part of our
commercial subscription.

## Example Configuration {#example}

```
http {
    resolver 10.0.0.1;

    oidc_provider my_idp {
        issuer        "https://provider.domain";
        client_id     "unique_id";
        client_secret "unique_secret";
    }

    server {
        location / {
            auth_oidc my_idp;

            proxy_set_header username $oidc_claim_sub;
            proxy_pass       http://backend;
        }
    }
}
```

The example assumes that the
“`https://<nginx-host>/oidc_callback`”
Redirection URI is configured on the OpenID Provider's side.
The path can be customized with the  directive.

## Directives {#directives}


name

http


Defines an OpenID Provider for use with the  directive.




name | off
off
http
server
location


Enables end user authentication with the
specified OpenID Provider.



Parameter value can contain variables (1.29.0).



The special value off cancels the effect
of the auth_oidc directive
inherited from the previous configuration level.




URL

oidc_provider


Sets the Issuer Identifier URL of the OpenID Provider;
required directive.
The URL must exactly match the value of “issuer”
in the OpenID Provider metadata
and requires the “https” scheme.




string

oidc_provider


Specifies the client ID of the Relying Party;
required directive.




string

oidc_provider


Specifies a secret value
used to authenticate the Relying Party with the OpenID Provider.
The supported
authentication
methods are
client_secret_basic and
client_secret_post (1.29.3).
The method is selected based on the OpenID Provider metadata
with a preference to client_secret_basic.




URL
<issuer>/.well-known/openid-configuration
oidc_provider


Sets a custom URL to retrieve the OpenID Provider metadata.




name
NGX_OIDC_SESSION
oidc_provider


Sets the name of a session cookie.




string

oidc_provider


Sets additional query arguments for the
authentication
request URL.

extra_auth_args "display=page&prompt=login";





uri

oidc_provider
1.29.3


Defines the URI path for triggering
front-channel
logout.
For the logout request to be associated with a user session,
it must either include the module session cookie or provide
both the “iss” and “sid” arguments.
It is recommended to configure the OpenID Provider to set the
“iss” and “sid” arguments
when invoking this endpoint.




on | off

oidc_provider
1.29.3


Explicitly enables or disables PKCE.
By default, PKCE is automatically enabled
based on OpenID Provider metadata.




uri
/oidc_callback
oidc_provider


Defines the Redirection URI path for post-authentication redirects
expected by the module from the OpenID Provider.
The uri must match the configuration on the Provider's side.



Absolute “https” URIs are supported since 1.29.0.




uri

oidc_provider
1.29.0


Defines the URI path for initiating session logout.
Upon session termination, the user is redirected to
Provider's
Logout Endpoint
or to the post logout page.
If neither is configured, the built-in post logout page is displayed.




uri

oidc_provider
1.29.0


Defines the path or absolute URI
to redirect the user to after the logout.
The uri must match the configuration on the Provider's side.
If the post logout page is served by NGINX,
the OIDC module shouldn't be enabled for this location:

http {
    oidc_provider my_idp {
        ...

        logout_uri      /logout;
        post_logout_uri /logged_out_page.html;
    }

    server {
        auth_oidc my_idp;

        location /logged_out_page.html {
            auth_oidc off;
        }
    }
}





on | off
off
oidc_provider
1.29.0


Adds the
id_token_hint
argument to the
Provider's
Logout Endpoint
when redirecting user during logout.
This argument can be required by some OpenID Providers.




scope ...
openid
oidc_provider


Sets requested scopes.
The openid scope is always required by OIDC.




name

oidc_provider


Specifies a custom
key-value database
that stores session data.
By default, an 8-megabyte key-value database named 
oidc_default_store_<provider name>
is created automatically.

A separate key-value database should be configured for each Provider
to prevent session reuse across providers.





time
8h
oidc_provider


Sets a timeout after which the session is deleted, unless it was
refreshed.




file

oidc_provider


Specifies a file with revoked certificates (CRL)
in the PEM format used to verify
the certificates of the OpenID Provider endpoints.




file
system CA bundle
oidc_provider


Specifies a file with trusted CA certificates in the PEM format
used to verify
the certificates of the OpenID Provider endpoints.




on | off
off
oidc_provider
1.29.0


Enables downloading of the
UserInfo
data and makes UserInfo claims available via the 
$oidc_claim_name variables.



## Embedded Variables {#variables}

The `ngx_http_oidc_module` module supports embedded variables:

***$oidc_id_token***  
  ID token
***$oidc_access_token***  
  access token
***$oidc_claim_**name***  
  top-level ID token or UserInfo claim

Nested claims can be fetched with the
auth_jwt module:

http {
    auth_jwt_claim_set $postal_code address postal_code;

    server {
        location / {
            auth_oidc my_idp;
            auth_jwt  off token=$oidc_id_token;

            proxy_set_header x-postal_code $postal_code;
            proxy_pass       http://backend;
        }
    }
}
***$oidc_userinfo***  
  UserInfo data in the JSON format (1.29.0)
