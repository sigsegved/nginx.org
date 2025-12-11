# Module ngx_http_session_log_module

**Revision:** 3  
**Language:** en


The `ngx_http_session_log_module` module enables logging
sessions (that is, aggregates of multiple HTTP requests) instead of
individual HTTP requests.

> **Note:** This module is available as part of our
commercial subscription.

## Example Configuration {#example}

The following configuration sets up a session log and maps requests to
sessions according to the request client address and **User-Agent**
request header field:

```
session_log_zone /path/to/log format=combined
                     zone=one:1m timeout=30s
                     md5=$binary_remote_addr$http_user_agent;

    location /media/ {
        session_log one;
    }
```

## Directives {#directives}


name | off
off
http
server
location


Enables the use of the specified session log.
The special value off cancels the effect
of the session_log directives
inherited from the previous configuration level.





    name
    string ...
combined "..."
http


Specifies the output format of a log.
The value of the $body_bytes_sent variable is aggregated across
all requests in a session.
The values of all other variables available for logging correspond to the
first request in a session.





    path
    zone=name:size
    [format=format]
    [timeout=time]
    [id=id]
    [md5=md5]


http


Sets the path to a log file and configures the shared memory zone that is used
to store currently active sessions.



A session is considered active for as long as the time elapsed since
the last request in the session does not exceed the specified
timeout (by default, 30 seconds).
Once a session is no longer active, it is written to the log.



The id parameter identifies the
session to which a request is mapped.
The id parameter is set to the hexadecimal representation
of an MD5 hash (for example, obtained from a cookie using variables).
If this parameter is not specified or does not represent the valid
MD5 hash, nginx computes the MD5 hash from the value of
the md5 parameter and creates a new session using this hash.
Both the id and md5 parameters
can contain variables.



The format parameter sets the custom session log
format configured by the  directive.
If format is not specified, the predefined
“combined” format is used.



## Embedded Variables {#variables}

The `ngx_http_session_log_module` module supports
two embedded variables:


***$session_log_id***  
  current session ID;
***$session_log_binary_id***  
  current session ID in binary form (16 bytes).
