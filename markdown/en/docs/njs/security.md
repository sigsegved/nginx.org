# Security

**Revision:** 2  
**Language:** en

All nginx security issues should be reported to [F5SIRT@f5.com](mailto:F5SIRT@f5.com) or via one of the methods listed [here](https://github.com/nginx/njs/blob/master/SECURITY.md) .

Patches are signed using one of the [PGP public keys](../../pgp_keys.xml) .

# Special considerations {#considerations}

njs does not evaluate dynamic code and especially the code received from the network in any way. The only way to evaluate that code using njs is to configure the [js_import](../http/ngx_http_js_module.xml#js_import) directive in nginx. JavaScript code is loaded once during nginx start.

In nginx/njs threat model, JavaScript code is considered a trusted source in the same way as `nginx.conf` and sites certificates. What this means in practice:

- memory disclosure and other security issues
triggered by JavaScript code modification
are not considered security issues, but as ordinary bugs
- measures should be taking for protecting JavaScript code used by njs
- if no [js_import](../http/ngx_http_js_module.xml#js_import) directives are present in `nginx.conf` ,
nginx is safe from JavaScript-related vulnerabilities

