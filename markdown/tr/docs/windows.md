# nginx/Windows kullanımı

**Language:** tr


nginx/Windows doğrudan Win32 API'yi kullanır (Cygwin emülasyon tabakasını değil).
Şu an için sadece *select* methodunu kullandığından yüksek performans ve ölçeklenebilirlik beklememelisiniz.
Bu ve bilinen diğer nedenlerle nginx/Windows'u *beta* versiyon olarak kabul etmek gerekir.
Unix versiyonu ile karşılaştırıldığında, XSLT filtresi, imaj filtresi, GeoIP modülü ve gömülü Perl dili hariç tam fonklsiyoneldir.

nginx/Windows versiyonunu yüklemek için [indir](../../en/download.html) bağlantısından zip formatındaki  geliştirme versiyonunu indirebilirsiniz. Geliştirme versiyonu, özellikle Windows ile ilgili en son yamaları içerir. Dosyayı indirdikten sonra açarak, nginx- klasörü içerisinden nginx'i çalıştırabilirsiniz.
C sürücüsü için örnek. root dizini:


```
cd c:\
unzip nginx-.zip
cd nginx-
start nginx
```


Ayrıca `tasklist` komutu ile nginx işlemlerini takip edebilirsiniz:


```
C:\nginx->tasklist /fi "imagename eq nginx.exe"

Image Name           PID Session Name     Session#    Mem Usage
=============== ======== ============== ========== ============
nginx.exe            652 Console                 0      2 780 K
nginx.exe           1332 Console                 0      3 112 K
```


Bu işlemlerden biri ana, diğerleri işçi işlemleridir.
Eğer nginx başlamazsa `logs\error.log` dosyasından nedenini öğrenebilirsiniz.
Eğer kayıt (log) dosyası yaratılmamış ise bunun nedeni de Windows Event Log içerisinde belirtilmiştir.
Eğer beklenen sayfa yerine hata sayfası ile karşılaşırsanız, yine `logs\error.log` dosyasını kontrol etmelisiniz.

nginx/Windows, yapılandırmada yer alan nisbi dizin yolları için yürütüldüğü klasörü, önek klasör olarak kullanır.
Buna örnek olarak, önek klasör şu şekildedir:
`C:\nginx-\`.
Ayarlarda yer alan dizin yolları Unix-stili kesme işaretleri ile belirtilir:


```
access_log   logs/site.log;
root         C:/web/html;
```

nginx/Windows bir servis olarak değil, standart konsol uygulaması olarak yürütülür ve aşağıdaki komutlar ile yönetilir:


| nginx -s stop | hızlı çıkış |
| --- | --- |
| nginx -s quit | yavaş çıkış |
| nginx -s reload | ayarları değiştirmek,
yeni işçi çalıştırmak,
eski işçi işlemden yavaşça çıkmak |
| nginx -s reopen | Kayıt dosyalarını tekrar açmak |

## Bilinen sorunlar {#known_issues}

- Bir çok işçi yürütülebildiği halde sadece biri iş yapabilmektedir.
- Bir işçi, 1024 eşzamanlı bağlantıdan fazlasını karşılayamamaktadır.
- Paylaşımlı hafıza desteğine ihtiyaç duyan önbellek ve diğer modüller,
"address space layout randomization" etkin olduğundan,
Windows Vista ve sonraki versiyonlarda çalışmamaktadır.

## Muhtemel geliştirmeler {#possible_future_enhancements}

- Servis olarak yürütme.
- I/O completion portlarını, uyarı methodu olarak kulanmak.
- Bir işçi işleminde (worker process) çoklu thread (yürütme birimi) kullanmak.
