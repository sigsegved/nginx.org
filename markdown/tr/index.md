# nginx

**Language:** tr

nginx [engine x], [Igor Sysoev](http://sysoev.ru/en/) tarafından yazılan bir HTTP, reverse proxy ve mail proxy sunucusudur. 5 yıldır, özellikle Rus sitelerinde yoğun bir şekilde kullanılmaktadır. Örneğin; [Rambler](http://www.rambler.ru) ( [RamblerMedia.com](http://ramblermedia.com) ). Netcraft'a göre, nginx, [Nisan 2010 itibari ile %4.70](http://news.netcraft.com/archives/2010/04/15/april_2010_web_server_survey.html) oranında kullanılmaktadır. Bazı başarı hikayeleri (İngilizce): [FastMail.FM](http://blog.fastmail.fm/2007/01/04/webimappop-frontend-proxies-changed-to-nginx/) , [Wordpress.com](http://barry.wordpress.com/2008/04/28/load-balancer-update/) .

Kaynak kodu, [2-clause BSD-like license](/LICENSE) lisansı altındadır.

# Temel HTTP özellikleri {#basic_http_features}

- Statik ve index dosyalarının sunumu, otomatik indeksleme;
açık dosya açıklayıcı önbellek;
- Önbellek ile hızlandırılmış reverse proxying;
basit yük dengeleme ve hata toleransı;
- Uzak FastCgi sunucularının önbelleklenmesi ile hızlandırılmış destek;
basit yük dengeleme ve hata toleransı;
- Modüler yapı.
Gzip, byte aralıkları, yığın cevaplar (chunked responses), XSLT, SSI, imaj boyutlandırma gibi filtreler.
FastCGI veya proksilenmiş sunucular ile tek bir sayfada çoklu SSI içermelerinin paralel işlenmesi.
- SSL ve TLS SNI desteği.

# Diğer HTTP özellikleri {#other_http_features}

- Ad ve IP tabanlı sanal sunucular;
- Keep-alive ve pipelined bağlantı desteği;
- Esnek yapılandırma;
- İstemci işlemlerinde kopma olmadan yeniden yapılandırma ve online güncelleme;
- Erişim kayıt (log) formatları, tamponlanmış kayıt yazımı ve hızlı kayıt devri;
- 3xx-5xx hata kod yönlendirmeleri;
- rewrite modülü;
- İstemcinin IP adresine dayalı erişim kontrolü ve HTTP temel kimlik denetleme;
- PUT, DELETE, MKCOL, COPY ve MOVE methodları;
- FLV streaming;
- Hız sınırlandırma;
- Bir adresten gelen eşzamanlı bağlantı ve talepleri sınırlandırma.
- Gömülü perl.

# Mail proxy sunucu özellikleri {#mail_proxy_server_features}

- Harici bir HTTP kimlik denetleme sunucusunu kullanarak, kullanıcıyı IMAP/POP3 backend'ine yönlendirme;
- Harici bir HTTP kimlik denetleme sunucusunu kullanarak, kullanıcıyı SMTP backend'ine yönlendirme ve kullanıcı kimlik denetlemesi;
- Kimlik denetleme methodları:
  - POP3: USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
  - IMAP: LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
  - SMTP: AUTH LOGIN/PLAIN/CRAM-MD5;
  
- SSL desteği;
- STARTTLS ve STLS desteği.

# Yapı ve ölçeklenebilirlik {#architecture_and_scalability}

- Bir ana işlem (main process) ve çok sayıda işçi işlemleri (workers).
İşçiler, imtiyazsız kullanıcı olarak yürütülürler;
- Uyarı methodları: kqueue (FreeBSD 4.1+),
epoll (Linux 2.6+), rt signals (Linux 2.2.19+),
/dev/poll (Solaris 7 11/99+), event ports (Solaris 10),
select ve poll;
- Çeşitli kqueue özellikleri desteği: EV_CLEAR, EV_DISABLE
(event'i geçici olarak etkisizleştirir), NOTE_LOWAT, EV_EOF, olanaklı data sayısı,
hata kodları;
- sendfile (FreeBSD 3.1+, Linux 2.2+, Mac OS X 10.5), sendfile64 (Linux 2.4.21+),
ve sendfilev (Solaris 8 7/01+) desteği;
- File AIO (FreeBSD 4.3+, Linux 2.6.22+);
- Accept-filters (FreeBSD 4.1+) ve TCP_DEFER_ACCEPT (Linux 2.4+) desteği;
- 10,000 inaktif HTTP keep-alive bağlantısı yaklaşık 2.5M hafıza kullanır;
- Data kopyalama operasyonları minimum düzeydedir.

# Test edilen işletim sistemleri ve platformlar {#tested_os_and_platforms}

- FreeBSD 3—8 / i386; FreeBSD 5—8 / amd64;
- Linux 2.2—2.6 / i386; Linux 2.6 / amd64;
- Solaris 9 / i386, sun4u; Solaris 10 / i386, amd64, sun4v;
- MacOS X / ppc, i386;
- Windows XP, Windows Server 2003.

