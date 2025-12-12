# Модуль ngx_http_proxy_protocol_vendor_module

**Revision:** 1  
**Language:** ru

Модуль `ngx_http_proxy_protocol_vendor_module` (1.23.3) позволяет получать дополнительную информацию о соединении из облачных платформ при помощи TLV, полученных из заголовка [протокола PROXY](http://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) .

Поддерживаемые облачные платформы:

- Amazon Web Services
- Google Cloud Platform
- Microsoft Azure

Протокол PROXY должен быть предварительно включён при помощи установки параметра `proxy_protocol` в директиве [listen](ngx_http_core_module.xml#listen) .

> **Note:** Модуль доступен как часть [коммерческой подписки](https://nginx.com/products/)

# Пример конфигурации {#example}

```
proxy_set_header X-Conn-ID $proxy_protocol_tlv_gcp_conn_id;

server {
    listen 80   proxy_protocol;
    listen 443  ssl proxy_protocol;
    ...
}
```

# Встроенные переменные {#variables}

**`$proxy_protocol_tlv_aws_vpce_id`**  
  значение TLV, полученное из заголовка протокола PROXY, содержащее [ID
конечной точки VPC AWS](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#proxy-protocol)

**`$proxy_protocol_tlv_azure_pel_id`**  
  значение TLV, полученное из заголовка протокола PROXY, содержащее [LinkID
частной конечной точки Azure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#getting-connection-information-using-tcp-proxy-v2)

**`$proxy_protocol_tlv_gcp_conn_id`**  
  значение TLV, полученное из заголовка протокола PROXY, содержащее [ID соединения
Google Cloud PSC](https://cloud.google.com/vpc/docs/configure-private-service-connect-producer#proxy-protocol)

