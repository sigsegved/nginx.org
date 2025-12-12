# Module ngx_http_oidc_module

**Revision:** 1  
**Language:** en

The `ngx_http_oidc_module` module (1.27.4) implements authentication as a Relying Party in OpenID Connect using the [Authorization Code Flow](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth) .

The module expects the OpenID Provider's configuration to be available via [metadata](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) and requires dynamic [resolver](ngx_http_core_module.xml#resolver) .

The module can be combined with other access modules via the [satisfy](ngx_http_core_module.xml#satisfy) directive. Note that the module may still block requests even with `satisfy any;` as an OpenID Provider might not redirect the user back to nginx.

> **Note:** This module is available as part of our [commercial subscription](https://nginx.com/products/) .

# Example Configuration {#example}

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

The example assumes that the “ `https://<nginx-host>/oidc_callback` ” Redirection URI is configured on the OpenID Provider's side. The path can be customized with the [redirect_uri](#redirect_uri) directive.

# Directives {#directives}

## oidc_provider

```
Syntax:  oidc_provider name { ... }
Default: 
Context: http
```

Defines an OpenID Provider for use with the [auth_oidc](#auth_oidc) directive.

## auth_oidc

```
Syntax:  auth_oidc name | off;
Default: off
Context: location, http, server
```

Enables end user authentication with the [specified](#oidc_provider) OpenID Provider.

Parameter value can contain variables (1.29.0).

The special value `off` cancels the effect of the `auth_oidc` directive inherited from the previous configuration level.

## issuer

```
Syntax:  issuer URL;
Default: 
Context: oidc_provider
```

Sets the Issuer Identifier URL of the OpenID Provider; required directive. The URL must exactly match the value of “ `issuer` ” in the OpenID Provider metadata and requires the “ `https` ” scheme.

## client_id

```
Syntax:  client_id string;
Default: 
Context: oidc_provider
```

Specifies the client ID of the Relying Party; required directive.

## client_secret

```
Syntax:  client_secret string;
Default: 
Context: oidc_provider
```

Specifies a secret value used to authenticate the Relying Party with the OpenID Provider. The supported [authentication methods](https://openid.net/specs/openid-connect-core-1_0.html#ClientAuthentication) are `client_secret_basic` and `client_secret_post` (1.29.3). The method is selected based on the OpenID Provider metadata with a preference to `client_secret_basic` .

## config_url

```
Syntax:  config_url URL;
Default: <issuer>/.well-known/openid-configuration
Context: oidc_provider
```

Sets a custom URL to retrieve the OpenID Provider metadata.

## cookie_name

```
Syntax:  cookie_name name;
Default: NGX_OIDC_SESSION
Context: oidc_provider
```

Sets the name of a session cookie.

## extra_auth_args

```
Syntax:  extra_auth_args string;
Default: 
Context: oidc_provider
```

Sets additional query arguments for the [authentication request](https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest) URL.

```
extra_auth_args "display=page&prompt=login";
```

## frontchannel_logout_uri

```
Syntax:  frontchannel_logout_uri uri;
Default: 
Context: oidc_provider
```

*This directive appeared in version 1.29.3.*

Defines the URI path for triggering [front-channel logout](https://openid.net/specs/openid-connect-frontchannel-1_0.html) . For the logout request to be associated with a user session, it must either include the module session cookie or provide both the “ `iss` ” and “ `sid` ” arguments. It is recommended to configure the OpenID Provider to set the “ `iss` ” and “ `sid` ” arguments when invoking this endpoint.

## pkce

```
Syntax:  pkce on | off;
Default: 
Context: oidc_provider
```

*This directive appeared in version 1.29.3.*

Explicitly enables or disables PKCE. By default, PKCE is automatically enabled based on OpenID Provider metadata.

## redirect_uri

```
Syntax:  redirect_uri uri;
Default: /oidc_callback
Context: oidc_provider
```

Defines the Redirection URI path for post-authentication redirects expected by the module from the OpenID Provider. The `uri` must match the configuration on the Provider's side.

Absolute “ `https` ” URIs are supported since 1.29.0.

## logout_uri

```
Syntax:  logout_uri uri;
Default: 
Context: oidc_provider
```

*This directive appeared in version 1.29.0.*

Defines the URI path for initiating session logout. Upon session termination, the user is redirected to [Provider's Logout Endpoint](https://openid.net/specs/openid-connect-rpinitiated-1_0.html#OPMetadata) or to the [post logout page](#post_logout_uri) . If neither is configured, the built-in post logout page is displayed.

## post_logout_uri

```
Syntax:  post_logout_uri uri;
Default: 
Context: oidc_provider
```

*This directive appeared in version 1.29.0.*

Defines the path or absolute URI to redirect the user to after the logout. The `uri` must match the configuration on the Provider's side. If the post logout page is served by NGINX, the OIDC module shouldn't be enabled for this location:

```
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
```

## logout_token_hint

```
Syntax:  logout_token_hint on | off;
Default: off
Context: oidc_provider
```

*This directive appeared in version 1.29.0.*

Adds the [`id_token_hint`](https://openid.net/specs/openid-connect-rpinitiated-1_0.html#RPLogout) argument to the [Provider's Logout Endpoint](https://openid.net/specs/openid-connect-rpinitiated-1_0.html#OPMetadata) when redirecting user during logout. This argument can be required by some OpenID Providers.

## scope

```
Syntax:  scope scope ...;
Default: openid
Context: oidc_provider
```

Sets requested scopes. The `openid` scope is always required by OIDC.

## session_store

```
Syntax:  session_store name;
Default: 
Context: oidc_provider
```

Specifies a custom [key-value database](ngx_http_keyval_module.xml#keyval_zone) that stores session data. By default, an 8-megabyte key-value database named `oidc_default_store_<provider name>` is created automatically.

> **Note:** A separate key-value database should be configured for each Provider
to prevent session reuse across providers.

## session_timeout

```
Syntax:  session_timeout time;
Default: 8h
Context: oidc_provider
```

Sets a timeout after which the session is deleted, unless it was [refreshed](https://openid.net/specs/openid-connect-core-1_0.html#RefreshTokens) .

## ssl_crl

```
Syntax:  ssl_crl file;
Default: 
Context: oidc_provider
```

Specifies a `file` with revoked certificates (CRL) in the PEM format used to verify the certificates of the OpenID Provider endpoints.

## ssl_trusted_certificate

```
Syntax:  ssl_trusted_certificate file;
Default: system CA bundle
Context: oidc_provider
```

Specifies a `file` with trusted CA certificates in the PEM format used to verify the certificates of the OpenID Provider endpoints.

## userinfo

```
Syntax:  userinfo on | off;
Default: off
Context: oidc_provider
```

*This directive appeared in version 1.29.0.*

Enables downloading of the [UserInfo](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo) data and makes UserInfo claims available via the [$oidc_claim_](#var_oidc_claim_) variables.

# Embedded Variables {#variables}

The `ngx_http_oidc_module` module supports embedded variables:

**`$oidc_id_token`**  
  ID token

**`$oidc_access_token`**  
  access token

**`$oidc_claim_` `name`**  
  top-level ID token or UserInfo claim

Nested claims can be fetched with the [auth_jwt](ngx_http_auth_jwt_module.xml) module:

```
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
```

**`$oidc_userinfo`**  
  UserInfo data in the JSON format (1.29.0)

