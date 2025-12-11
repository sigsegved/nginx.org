# Module ngx_http_charset_module

**Revision:** 5  
**Language:** en


The `ngx_http_charset_module` module adds the specified
charset to the **Content-Type** response header field.
In addition, the module can convert data from one charset to another,
with some limitations:

- conversion is performed one way — from server to client,
- only single-byte charsets can be converted
- or single-byte charsets to/from UTF-8.

## Example Configuration {#example}

```
include        conf/koi-win;

charset        windows-1251;
source_charset koi8-r;
```

## Directives {#directives}


charset | off
off
http
server
location
if in location


Adds the specified charset to the Content-Type
response header field.
If this charset is different from the charset specified
in the  directive, a conversion is performed.



The parameter off cancels the addition of charset
to the Content-Type response header field.



A charset can be defined with a variable:

charset $charset;

In such a case, all possible values of a variable need to be present
in the configuration at least once in the form of the
, , or
 directives.
For utf-8, windows-1251, and
koi8-r charsets, it is sufficient to include the files
conf/koi-win, conf/koi-utf, and
conf/win-utf into configuration.
For other charsets, simply making a fictitious conversion table works,
for example:

charset_map iso-8859-5 _ { }




In addition, a charset can be set in the
X-Accel-Charset response header field.
This capability can be disabled using the
,
,
,
,
and

directives.




charset1 charset2

http


Describes the conversion table from one charset to another.
A reverse conversion table is built using the same data.
Character codes are given in hexadecimal.
Missing characters in the range 80-FF are replaced with “?”.
When converting from UTF-8, characters missing in a one-byte charset
are replaced with “&#XXXX;”.



Example:

charset_map koi8-r windows-1251 {
    C0 FE ; # small yu
    C1 E0 ; # small a
    C2 E1 ; # small b
    C3 F6 ; # small ts
    ...
}




When describing a conversion table to UTF-8, codes for the UTF-8 charset should
be given in the second column, for example:

charset_map koi8-r utf-8 {
    C0 D18E ; # small yu
    C1 D0B0 ; # small a
    C2 D0B1 ; # small b
    C3 D186 ; # small ts
    ...
}




Full conversion tables from koi8-r to
windows-1251, and from koi8-r and
windows-1251 to utf-8
are provided in the distribution files conf/koi-win,
conf/koi-utf, and conf/win-utf.




mime-type ...
text/html text/xml text/plain text/vnd.wap.wml
application/javascript application/rss+xml
http
server
location
0.7.9


Enables module processing in responses with the specified MIME types
in addition to “text/html”.
The special value “*” matches any MIME type (0.8.29).




Until version 1.5.4, “application/x-javascript” was used
as the default MIME type instead of “application/javascript”.





on | off
off
http
server
location
if in location


Determines whether a conversion should be performed for answers
received from a proxied or a FastCGI/uwsgi/SCGI/gRPC server
when the answers already carry a charset in the Content-Type
response header field.
If conversion is enabled, a charset specified in the received
response is used as a source charset.

It should be noted that if a response is received in a subrequest
then the conversion from the response charset to the main request charset
is always performed, regardless of the override_charset
directive setting.





charset

http
server
location
if in location


Defines the source charset of a response.
If this charset is different from the charset specified
in the  directive, a conversion is performed.


