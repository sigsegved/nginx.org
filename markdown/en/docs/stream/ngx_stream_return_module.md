# Module ngx_stream_return_module

**Revision:** 1  
**Language:** en

The `ngx_stream_return_module` module (1.11.2) allows sending a specified value to the client and then closing the connection.

# Example Configuration {#example}

```
server {
    listen 12345;
    return $time_iso8601;
}
```

# Directives {#directives}

## return

```
Syntax:  return value;
Default: 
Context: server
```

Specifies a `value` to send to the client. The value can contain text, variables, and their combination.

