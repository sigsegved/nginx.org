# Модуль ngx_stream_geoip_module

**Revision:** 1  
**Language:** ru


Модуль `ngx_stream_geoip_module` (1.11.3) создаёт переменные,
значения которых зависят от IP-адреса клиента, используя готовые базы данных
[MaxMind](http://www.maxmind.com).

При использовании баз данных с поддержкой IPv6
IPv4-адреса ищутся отображёнными на IPv6.

По умолчанию этот модуль не собирается, его сборку необходимо
разрешить с помощью конфигурационного параметра
`--with-stream_geoip_module`.

> **Note:** Для сборки и работы этого модуля нужна библиотека
[MaxMind GeoIP](http://www.maxmind.com/app/c).

## Пример конфигурации {#example}

```
stream {
    geoip_country         GeoIP.dat;
    geoip_city            GeoLiteCity.dat;

    map $geoip_city_continent_code $nearest_server {
        default        example.com;
        EU          eu.example.com;
        NA          na.example.com;
        AS          as.example.com;
    }
   ...
}
```

## Директивы {#directives}


файл

stream


Задаёт базу данных для определения страны в зависимости
от значения IP-адреса клиента.
При использовании этой базы данных доступны следующие переменные:


$geoip_country_code

двухбуквенный код страны, например,
“RU”, “US”.


$geoip_country_code3


трёхбуквенный код страны, например,
“RUS”, “USA”.


$geoip_country_name

название страны, например,
“Russian Federation”, “United States”.







файл

stream


Задаёт базу данных для определения страны, региона и города
в зависимости от значения IP-адреса клиента.
При использовании этой базы данных доступны следующие переменные:


$geoip_area_code
телефонный код области (только для США).

Данная переменная может содержать неактуальную информацию, т.к.
соответствующее поле базы данных объявлено устаревшим.




$geoip_city_continent_code

двухбуквенный код континента, например,
“EU”, “NA”.


$geoip_city_country_code


двухбуквенный код страны, например,
“RU”, “US”.


$geoip_city_country_code3


трёхбуквенный код страны, например,
“RUS”, “USA”.


$geoip_city_country_name


название страны, например,
“Russian Federation”, “United States”.


$geoip_dma_code

DMA-код региона в США (также известный как “код агломерации”), согласно
геотаргетингу
Google AdWords API.


$geoip_latitude
широта.

$geoip_longitude
долгота.

$geoip_region

двухсимвольный код региона страны (область, край, штат,
провинция, федеральная земля и тому подобное), например,
“48”, “DC”.


$geoip_region_name

название региона страны (область, край, штат,
провинция, федеральная земля и тому подобное), например,
“Moscow City”, “District of Columbia”.


$geoip_city

название города, например,
“Moscow”, “Washington”.


$geoip_postal_code

почтовый индекс.







файл

stream


Задаёт базу данных для определения названия организации
в зависимости от значения IP-адреса клиента.
При использовании этой базы данных доступна следующая переменная:


$geoip_org

название организации, например, “The University of Melbourne”.





