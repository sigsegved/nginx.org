# Sunucu adları

**Author:** Igor Sysoev  
**Translator:** Altan Tanrıverdi  
**Language:** tr

Sunucu adları `server_name` yönergesi kullanılarak tanımlanırlar ve gelen bir talep için hangi server bloğunun kullanılacağını belirlerler. Ayrıca bakınız " ". Gerçek, wildcard veya düzenli ifadeler şeklinde tanımlanabilirler.

```
server {
    listen       80;
    server_name  example.org  www.example.org;
    ...
}

server {
    listen       80;
    server_name  *.example.org;
    ...
}

server {
    listen       80;
    server_name  mail.*;
    ...
}

server {
    listen       80;
    server_name  ~^(?<user>.+)\.example\.net$;
    ...
}
```

Bu adlar şu sıra ile test edilirler:

1. gerçek adlar;
2. * ile başlayan wildcard adlar: `*.example.org` ;
3. * ile biten wildcard adlar: `mail.*` ;
4. ve düzenli ifadeler (regular expressions).

İlk eşleşme arama işlemini bitirir.

# Wildcard adlar {#wildcard_names}

Bir wildcard ad ancak başlangıçta veya bitişte * ifadesini içerir ve nokta ile sınırlandırılır. `www.*.example.org` ve `w*.example.org` adları geçersizdir. Ancak bu adlar düzenli ifadeler ile geçerli hale getirilebilir, örneğin, `~^www\..+\.example\.org$` ve `~^w.*\.example\.org$` . Buradaki * bir çok eşleşmeyi tanımlayabilir. `*.example.org` ifadesi `www.example.org` ve `www.sub.example.org` adlarına karşılık gelebilir.

`.example.org` şeklindeki bir wildcard `example.org` gerçek adı ile `*.example.org` wildcard adına karşılık gelir.

# Düzenli ifade adları {#regex_names}

nginx tarafından kullanılan düzenli ifadeler, Perl programlama dili (PCRE) tarafından kullanılanlar ile tam uyumludur. Bir düzenli ifade kullanmak için sunucu adı tilda (~) ile başlamalıdır:

```
server_name  ~^www\d+\.example\.net$;
```

diğer türlü ifade gerçek ad veya düzenli ifade * içeriyorsa wildcard ad gibi algılanacaktır (ve yüksek ihtimal geçersiz bir ad olarak). "^" ve "$" çapalarını kullanmayı unutmayın. Sentaks açısından gerekli olmasalar da mantık açısından gereklidir. Ayrıca alan adında bulunan noktalarda da \ önceli ile kullanılmalıdır. "{" ve "}" kullanan bir düzenli ifade tırnak arasına alınmalıdır:

```
server_name  "~^(?<name>\w\d{1,3}+)\.example\.net$";
```

diğer türlü, nginx şu şekilde bir hata verecektir:

```
directive "server_name" is not terminated by ";" in ...
```

Bir düzenli ifade adı değişken olarak sonraki aşamalarda kullanılabilir:

```
server {
    server_name   ~^(www\.)?(?<domain>.+)$;

    location / {
        root   /sites/$domain;
    }
}
```

PCRE kütüphanesi ile ad yakalama işlemi de şu şekildedir: Eğer nginx aşağıdaki hatayı verirse:

```
pcre_compile() failed: unrecognized character after (?< in ...
```

bu PCRE kütüphanesini eski olduğu ve `?P<` şeklinde kullanmanız gerektiği anlamına gelir. Yakalama ayrıca dijital formda da olabilir:

```
server {
    server_name   ~^(www\.)?(.+)$;

    location / {
        root   /sites/$2;
    }
}
```

Ancak, dijital referanslar kolaylıkla üstüne yazılabilir olduğundan, bu şekilde kullanım basit durumlar için sınırlandırılmalıdır (yukarıdaki gibi).

# Diğer muhtelif adlar {#miscellaneous_names}

Eğer server bloğu içerisinde bir `server_name` tanımlanmamışsa nginx, sunucu adı olarak *hostname* ifadesini kullanır.

Eğer varsayılan dışındaki bir server bloğuna gelen ve header bilgisinde "Host" datası yer almayan bir talebi işlemek isterseniz boş bir ad kullanmak zorundasınız:

```
server {
    listen       80;
    server_name  example.org  www.example.org  "";
    ...
}
```

Eğer bir istemci ad yerine IP adresini kullanarak bir talepte bulunursa, header içerisinde bulunan "Host" datası IP bilgisini içerecektir ve bu IP adresini, sunucu adı olarak kullanarak talebi işleyebilirsiniz:

```
server {
    listen       80;
    server_name  example.org
                 www.example.org
                 ""
                 192.168.1.1
                 ;
    ...
}
```

Bir catch-all (tümünü-yakala) sunucuda "_" şeklinde garip bir ifade ile karşılaşabilirsiniz:

```
server {
    listen       80  default_server;
    server_name  _;
    return       444;
}
```

Bu ad ile ilgili özel bir durum söz konusu değil, sadece gerçek bir ad ile kesişmeyen sayısız geçersiz alan adlarından biridir. Ayrıca "--", "!@#" ve benzeri ifadeler de kullanabilirsiniz.

nginx, 0.6.25 versiyonuna kadar, bir catch-all adı olmak için hatalı bir şekilde yorumlanan "*" özel adını destekliyordu. Fakat bu bir catch-all veya wildcard sunucu adı olarak fonksiyonel değil. Bunun yerine, `server_name_in_redirect` yönergesini kullanarak fonksiyonelliği sağlamaya başladık. "*" özel karakteri artık desteklenmiyor, bu yüzden `server_name_in_redirect` yönergesi kullanılmalıdır. Not: `server_name` yönergesini kullanan varsayılan sunucuyu veya catch-all adını belirtmenin bir yolu bulunmuyor. Bu, `server_name` yönergesinin değil, `listen` yönergesinin bir özelliğidir. Ayrıca bakınız " ". *:80 ve *:8080 portlarını dinleyen sunucular tanımlayabilir ve birini *:8080 portu için varsayılan olarak belirlerken, diğerini de *:80 için varsayılan olarak belirleyebilirsiniz:

```
server {
    listen       80;
    listen       8080  default_server;
    server_name  example.net;
    ...
}

server {
    listen       80  default_server;
    listen       8080;
    server_name  example.org;
    ...
}
```

# Optimizasyon {#optimization}

Gerçek ve wildcard adlar çırpılarda (hash) depolanır. Çırpılar listen portlarına bağlıdırlar ve her bir listen port 3 farklı çırpıya sahip olabilir: gerçek ad çırpısı, * ile başlayan bir wildcard adı çırpısı ve * ile biten bir wildcard adı çırpısı. Çırpıların boyutu yapılandırma aşamasında optimize edilir ve böylece bir ad en az önbellek kayıpları ile bulundurulur. İlk olarak gerçek ad çırpısı aranır. Gerçek ad çırpısı kullanan bir ad bulunmaz ise, * ile başlayan wildcard ad çırpısı aranır. Bu da bulunmaz ise, * ile biten wildcard ad çırpısı aranır. Adların alanadı parçaları ile aranması nedeniyle wildcard ad çırpıları araması, gerçek ad çırpı aramasına oranla daha yavaştır. Not: Özel `.example.org` wildcard formu, gerçek ad çırpısında değil, wildcard ad çırpısında saklanır. Düzenli İfadeler sırayla test edildiğinden bu en yavaş ve ölçeklenebilir olmayan yöntemdir.

Bu nedenlerden dolayı, imkanlar el veriyorsa gerçek adları kullanmak en iyisidir. Örneğin, bir sunucunun en sık talep edilen adları `example.org` ve `www.example.org` ise bunları açıkca belirtmek daha etkili olacaktır:

```
server {
    listen       80;
    server_name  example.org  www.example.org  *.example.org;
    ...
}
```

bu kullanım aşağıdaki basit kullanımdan daha etkili olacaktır:

```
server {
    listen       80;
    server_name  .example.org;
    ...
}
```

Eğer çok miktarda veya olağandışı şekilde uzun sunucu adları tanımladıysanız, *http* düzeyinde `server_names_hash_max_size` ve `server_names_hash_bucket_size` yönergelerini tekrar ayarlamalısınız. `server_names_hash_bucket_size` yönergesinin varsayılan değeri CPU önbellek satır boyutuna göre 32, 64 veya başka bir rakam olabilir. Eğer bu değer 32 ise ve "cok.uzun.sunucu.adi.example.org" ifadesini sunucu adı olarak belirlerseniz nginx, başlamayacak ve aşağıdaki hatayı verecektir:

```
could not build the server_names_hash,
you should increase server_names_hash_bucket_size: 32
```

Bu durumda yönerge değerini aşağıdaki gibi belirlemelisiniz:

```
http {
    server_names_hash_bucket_size  64;
    ...
```

Eğer çok fazla sunu adı belirlemiş iseniz şu şekilde bir hata alacaksınız:

```
could not build the server_names_hash,
you should increase either server_names_hash_max_size: 512
or server_names_hash_bucket_size: 32
```

Bu durumda ilk olarak `server_names_hash_max_size` değerini sunucu ad sayısına yakın bir değeri yükseltin. Eğer bu da yardımcı sorunu çözmez ise veya nginx başlama süresi çok uzar ise `server_names_hash_bucket_size` değerini arttırın.

Eğer bir sunucu sadece bir listen port için ise, nginx sunucu adlarını test etmeyecek ve listen port için çırpılar yaratmayacaktır. Fakat bu durumun bir istisnası var; eğer `server_name` tutuklar (capture) içeren bir düzenli ifade ise nginx, bu tutukları almak için ifadeyi yürütmek zorundadır.

# Uygunluk {#compatibility}

- Named düzenli ifade sunucu adı tutukları, 0.8.25 versiyonundan beri destekleniyor.
- Düzenli ifade sunucu adı tutukları, 0.7.40 versiyonundan beri destekleniyor.
- "" boş sunucu adı 0.7.12 versiyonundan beri destekleniyor.
- Bir wildcard sunucu adının veya düzenli ifadenin ilk sunucu adı olarak kullanılması 0.6.25 versiyonundan beri destekleniyor.
- Düzenli ifade sunucu adları 0.6.7 versiyonundan beri destekleniyor.
- `example.*` wildcard formu 0.6.0 versiyonundan beri destekleniyor.
- `.example.org` özel formu 0.3.18 versiyonundan beri destekleniyor.
- `*.example.org` wildcard formu 0.1.13 versiyonundan beri destekleniyor.

