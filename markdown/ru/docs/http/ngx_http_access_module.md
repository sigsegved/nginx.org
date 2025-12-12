# Модуль ngx_http_access_module

**Revision:** 4  
**Language:** ru

Модуль `ngx_http_access_module` позволяет ограничить доступ для определённых адресов клиентов.

Ограничить доступ можно также по [паролю](ngx_http_auth_basic_module.xml) , по [результату подзапроса](ngx_http_auth_request_module.xml) или по [JWT](ngx_http_auth_jwt_module.xml) . Одновременное ограничение доступа по адресу и паролю управляется директивой [satisfy](ngx_http_core_module.xml#satisfy) .

# Пример конфигурации {#example}

```
location / {
    deny  192.168.1.1;
    allow 192.168.1.0/24;
    allow 10.1.1.0/16;
    allow 2001:0db8::/32;
    deny  all;
}
```

Правила проверяются в порядке их записи до первого соответствия. В данном примере доступ разрешён только для IPv4-сетей `10.1.1.0/16` и `192.168.1.0/24` , кроме адреса `192.168.1.1` , и для IPv6-сети `2001:0db8::/32` . Если правил много, то лучше воспользоваться переменными модуля [ngx_http_geo_module](ngx_http_geo_module.xml) .

# Директивы {#directives}

## allow

```
Syntax:  адрес | CIDR | unix: | all
Default: 
Context: limit_except, http, server, location
```

Разрешает доступ для указанной сети или адреса. Если указано специальное значение `unix:` (1.5.1), разрешает доступ для всех UNIX-сокетов.

## deny

```
Syntax:  адрес | CIDR | unix: | all
Default: 
Context: limit_except, http, server, location
```

Запрещает доступ для указанной сети или адреса. Если указано специальное значение `unix:` (1.5.1), запрещает доступ для всех UNIX-сокетов.

