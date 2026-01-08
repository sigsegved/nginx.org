# nginx: пакеты для Linux

**Revision:** 113  
**Language:** ru

# Поддерживаемые дистрибутивы и версии {#distributions}

Пакеты nginx доступны для следующих дистрибутивов Linux и их версий:

[RHEL и производные](#RHEL) 

[Debian](#Debian) 

[Ubuntu](#Ubuntu) 

[SLES](#SLES) 

[Alpine](#Alpine) 

[Amazon Linux](#Amazon-Linux) 

# Инструкции по установке {#instructions}

Для того, чтобы поставить nginx на новой машине, необходимо подключить и настроить репозиторий пакетов nginx. После этого можно будет установить и обновлять nginx из этого репозитория.

## RHEL и производные {#RHEL}

Эта секция применима к Red Hat Enterprise Linux и его производным, таким как CentOS, Oracle Linux, Rocky Linux, AlmaLinux.

Установите пакеты, необходимые для подключения yum-репозитория:

```
sudo yum install yum-utils
```

Для подключения yum-репозитория создайте файл с именем `/etc/yum.repos.d/nginx.repo` со следующим содержимым:

```
[nginx-stable]
name=nginx stable repo
baseurl=https://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[nginx-mainline]
name=nginx mainline repo
baseurl=https://nginx.org/packages/mainline/centos/$releasever/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
```

По умолчанию используется репозиторий для стабильной версии nginx. Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду:

```
sudo yum-config-manager --enable nginx-mainline
```

Чтобы установить nginx, выполните следующую команду:

```
sudo yum install nginx
```

При запросе подтверждения GPG-ключа проверьте, что отпечаток ключа совпадает с `573B FD6B 3D8F BC64 1079 A6AB ABF5 BD82 7BD9 BF62` , и, если это так, подтвердите его.

## Debian {#Debian}

Установите пакеты, необходимые для подключения apt-репозитория:

```
sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring
```

Теперь нужно импортировать официальный ключ, используемый apt для проверки подлинности пакетов. Скачайте ключ:

```
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
```

Проверьте, верный ли ключ был загружен:

```
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
```

Вывод команды должен содержать полный отпечаток ключа `573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62` :

```
pub   rsa2048 2011-08-19 [SC] [expires: 2027-05-24]
      573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
uid                      nginx signing key <signing-key@nginx.com>
```

Вывод команды может содержать и другие ключи, используемые для подписи пакетов.

Для подключения apt-репозитория для стабильной версии nginx, выполните следующую команду:

```
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду вместо предыдущей:

```
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/mainline/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Для использования пакетов из нашего репозитория вместо распространяемых в дистрибутиве, настройте закрепление:

```
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx
```

Чтобы установить nginx, выполните следующие команды:

```
sudo apt update
sudo apt install nginx
```

## Ubuntu {#Ubuntu}

Установите пакеты, необходимые для подключения apt-репозитория:

```
sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring
```

Теперь нужно импортировать официальный ключ, используемый apt для проверки подлинности пакетов. Скачайте ключ:

```
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
```

Проверьте, верный ли ключ был загружен:

```
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
```

Вывод команды должен содержать полный отпечаток ключа `573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62` :

```
pub   rsa2048 2011-08-19 [SC] [expires: 2027-05-24]
      573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
uid                      nginx signing key <signing-key@nginx.com>
```

Вывод команды может содержать и другие ключи, используемые для подписи пакетов.

Для подключения apt-репозитория для стабильной версии nginx, выполните следующую команду:

```
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду вместо предыдущей:

```
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/mainline/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Для использования пакетов из нашего репозитория вместо распространяемых в дистрибутиве, настройте закрепление:

```
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx
```

Чтобы установить nginx, выполните следующие команды:

```
sudo apt update
sudo apt install nginx
```

## SLES {#SLES}

Установите пакеты, необходимые для подключения zypper-репозитория:

```
sudo zypper install curl ca-certificates gpg2
```

Для подключения zypper-репозитория для стабильной версии nginx, выполните следующую команду:

```
sudo zypper addrepo --gpgcheck --type yum --refresh --check \
    'https://nginx.org/packages/sles/$releasever_major' nginx-stable
```

Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду вместо предыдущей:

```
sudo zypper addrepo --gpgcheck --type yum --refresh --check \
    'https://nginx.org/packages/mainline/sles/$releasever_major' nginx-mainline
```

Теперь нужно импортировать официальный ключ, используемый zypper/rpm для проверки подлинности пакетов. Скачайте ключ:

```
curl -o /tmp/nginx_signing.key https://nginx.org/keys/nginx_signing.key
```

Проверьте, верный ли ключ был загружен:

```
gpg --with-fingerprint /tmp/nginx_signing.key
```

Вывод команды должен содержать полный отпечаток ключа `573B FD6B 3D8F BC64 1079 A6AB ABF5 BD82 7BD9 BF62` :

```
pub  2048R/7BD9BF62 2011-08-19 [expires: 2027-05-24]
      Key fingerprint = 573B FD6B 3D8F BC64 1079  A6AB ABF5 BD82 7BD9 BF62
uid nginx signing key <signing-key@nginx.com>
```

Импортируйте ключ в базу данных rpm:

```
sudo rpmkeys --import /tmp/nginx_signing.key
```

Чтобы установить nginx, выполните следующую команду:

```
sudo zypper install nginx
```

## Alpine {#Alpine}

Установите пакеты, необходимые для подключения apk-репозитория:

```
sudo apk add openssl curl ca-certificates
```

Для подключения apk-репозитория для стабильной версии nginx, выполните следующую команду:

```
printf "%s%s%s%s\n" \
    "@nginx " \
    "https://nginx.org/packages/alpine/v" \
    `egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release` \
    "/main" \
    | sudo tee -a /etc/apk/repositories
```

Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду вместо предыдущей:

```
printf "%s%s%s%s\n" \
    "@nginx " \
    "https://nginx.org/packages/mainline/alpine/v" \
    `egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release` \
    "/main" \
    | sudo tee -a /etc/apk/repositories
```

Теперь нужно импортировать официальный ключ, используемый apk для проверки подлинности пакетов. Скачайте ключ:

```
curl -o /tmp/nginx_signing.rsa.pub https://nginx.org/keys/nginx_signing.rsa.pub
```

Проверьте, верный ли ключ был загружен:

```
openssl rsa -pubin -in /tmp/nginx_signing.rsa.pub -text -noout
```

Вывод команды должен содержать следующий модуль:

```
Public-Key: (2048 bit)
Modulus:
    00:fe:14:f6:0a:1a:b8:86:19:fe:cd:ab:02:9f:58:
    2f:37:70:15:74:d6:06:9b:81:55:90:99:96:cc:70:
    5c:de:5b:e8:4c:b2:0c:47:5b:a8:a2:98:3d:11:b1:
    f6:7d:a0:46:df:24:23:c6:d0:24:52:67:ba:69:ab:
    9a:4a:6a:66:2c:db:e1:09:f1:0d:b2:b0:e1:47:1f:
    0a:46:ac:0d:82:f3:3c:8d:02:ce:08:43:19:d9:64:
    86:c4:4e:07:12:c0:5b:43:ba:7d:17:8a:a3:f0:3d:
    98:32:b9:75:66:f4:f0:1b:2d:94:5b:7c:1c:e6:f3:
    04:7f:dd:25:b2:82:a6:41:04:b7:50:93:94:c4:7c:
    34:7e:12:7c:bf:33:54:55:47:8c:42:94:40:8e:34:
    5f:54:04:1d:9e:8c:57:48:d4:b0:f8:e4:03:db:3f:
    68:6c:37:fa:62:14:1c:94:d6:de:f2:2b:68:29:17:
    24:6d:f7:b5:b3:18:79:fd:31:5e:7f:4c:be:c0:99:
    13:cc:e2:97:2b:dc:96:9c:9a:d0:a7:c5:77:82:67:
    c9:cb:a9:e7:68:4a:e1:c5:ba:1c:32:0e:79:40:6e:
    ef:08:d7:a3:b9:5d:1a:df:ce:1a:c7:44:91:4c:d4:
    99:c8:88:69:b3:66:2e:b3:06:f1:f4:22:d7:f2:5f:
    ab:6d
Exponent: 65537 (0x10001)
```

Переместите ключ в каталог доверенных ключей apk:

```
sudo mv /tmp/nginx_signing.rsa.pub /etc/apk/keys/
```

Чтобы установить nginx, выполните следующую команду:

```
sudo apk add nginx@nginx
```

Тэг `@nginx` должен быть указан и при установке пакетов с [динамическими модулями](#dynmodules) :

```
sudo apk add nginx-module-image-filter@nginx nginx-module-njs@nginx
```

## Amazon Linux {#Amazon-Linux}

Установите пакеты, необходимые для подключения yum-репозитория:

```
sudo yum install yum-utils
```

Для подключения yum-репозитория для Amazon Linux 2 создайте файл с именем `/etc/yum.repos.d/nginx.repo` со следующим содержимым:

```
[nginx-stable]
name=nginx stable repo
baseurl=https://nginx.org/packages/amzn2/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
priority=9

[nginx-mainline]
name=nginx mainline repo
baseurl=https://nginx.org/packages/mainline/amzn2/$releasever/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
priority=9
```

Для подключения yum-репозитория для Amazon Linux 2023 создайте файл с именем `/etc/yum.repos.d/nginx.repo` со следующим содержимым:

```
[nginx-stable]
name=nginx stable repo
baseurl=https://nginx.org/packages/amzn/2023/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
priority=9

[nginx-mainline]
name=nginx mainline repo
baseurl=https://nginx.org/packages/mainline/amzn/2023/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
priority=9
```

По умолчанию используется репозиторий для стабильной версии nginx. Если предпочтительно использовать пакеты для основной версии nginx, выполните следующую команду:

```
sudo yum-config-manager --enable nginx-mainline
```

Чтобы установить nginx, выполните следующую команду:

```
sudo yum install nginx
```

При запросе подтверждения GPG-ключа проверьте, что отпечаток ключа совпадает с `573B FD6B 3D8F BC64 1079 A6AB ABF5 BD82 7BD9 BF62` , и, если это так, подтвердите его.

# Пакеты с исходным кодом {#sourcepackages}

Исходные коды пакетов находятся в соответствующем [репозитории](https://github.com/nginx/pkg-oss) .

Ветка репозитория `master` содержит исходные коды пакетов для mainline-версии, в то время как ветки `stable-*` содержат исходные коды пакетов для стабильных релизов. Для сборки бинарных пакетов запустите `make` в каталоге `debian/` для Debian/Ubuntu, или в каталоге `rpm/SPECS/` для RHEL и производных, SLES, и Amazon Linux, или в каталоге `alpine/` для Alpine.

Исходные коды пакетов распространяются под той же [BSD-подобной лицензией из 2 пунктов](../LICENSE) , что и сам nginx.

# Динамические модули {#dynmodules}

Для того чтобы избежать увеличения числа зависимостей, основной пакет nginx не включает модули, которым требуются дополнительные библиотеки. Начиная с версии 1.9.11 nginx поддерживает [динамические модули](docs/ngx_core_module.xml#load_module) , и следующие модули собираются как динамические и поставляются в виде отдельных пакетов:

```
nginx-module-geoip
nginx-module-image-filter
nginx-module-njs
nginx-module-perl
nginx-module-xslt
```

В дополнение к этому, начиная с версии 1.25.3 следующий модуль поставляется в виде отдельного пакета:

```
nginx-module-otel
```

В дополнение к этому, начиная с версии 1.29.1 следующий модуль поставляется в виде отдельного пакета:

```
nginx-module-acme
```

# Подписи {#signatures}

Поскольку наши [PGP-ключи](../en/pgp_keys.xml) находятся на том же сервере, что и пакеты, им следует доверять в равной степени. Поэтому мы настоятельно рекомендуем дополнительно проверить подлинность загруженных PGP-ключей. В PGP есть понятие “сети доверия”, когда ключ подписывается чьим-либо другим ключом, тот в свою очередь третьим, и т.д. Это зачастую позволяет построить цепочку от произвольного ключа до ключа человека, которого вы знаете и кому доверяете лично, и таким образом удостовериться в подлинности первого ключа в цепочке. Подробно эта концепция описана в [GPG Mini Howto](https://www.gnupg.org/howtos/en/GPGMiniHowto-1.html) . У наших ключей есть достаточное количество подписей, поэтому проверить их подлинность относительно несложно.

