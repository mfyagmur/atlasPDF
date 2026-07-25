# TASK 07 — Animasyon ve Etkileşim Katmanı

## Amaç
Siteye modern, profesyonel bir "his" kazandırmak: component giriş/çıkış animasyonları, parmak hareketleri (gesture), scroll tabanlı ve timeline gerektiren geçişler. Bu task'ta iki farklı araç bilinçli olarak ayrı sorumluluklarda kullanılacak — birbirine karıştırılmayacak:

- **Motion (Framer Motion):** component seviyesi — mount/unmount, hover/tap, sürükleme.
- **GSAP + ScrollTrigger:** sayfa seviyesi — scroll'a bağlı, zaman çizelgeli, orkestre edilmiş animasyonlar.

## Yapılacaklar

### Motion ile (component seviyesi)

1. Tool kartları (ana sayfa grid'i): sayfa yüklendiğinde sırayla belirip yukarı kayarak gelme (stagger animasyon), hover'da hafif büyüme/gölge artışı.
2. `FileUploader` component'i: dosya sürüklenip alana getirildiğinde (`onDragEnter`) alan görsel olarak tepki versin (renk/boyut animasyonu); dosya başarıyla eklendiğinde `AnimatePresence` ile dosya kartı animasyonlu şekilde listeye girsin, silinirken animasyonlu çıksın.
3. Sonuç/indirme kartı (`DownloadCard`): işlem tamamlandığında `AnimatePresence` ile animasyonlu şekilde belirsin (fade + scale).
4. Split sayfasındaki sayfa sırası değiştirme (varsa) `Reorder` (Motion'ın `Reorder.Group`/`Reorder.Item` API'si) ile sürükle-bırak sıralama olarak yükseltilebilir (opsiyonel iyileştirme, zorunlu değil).
5. Mobilde dokunma hedefleri (tap target) yeterince büyük olsun, `whileTap` ile dokunma geri bildirimi (hafif küçülme) tüm tıklanabilir kartlara uygulansın.

### GSAP + ScrollTrigger ile (sayfa seviyesi)

1. `@gsap/react`'in `useGSAP()` hook'unu kullan (route değişiminde temizlik/cleanup otomatik olsun, sızıntı olmasın — SPA'da bu kritik).
2. Ana sayfada: kullanıcı aşağı kaydırdıkça "Nasıl çalışır" / "Neden biz" gibi bölümler sırayla, scroll pozisyonuna bağlı olarak sahneye girsin (basit bir `ScrollTrigger` + `timeline` kurulumu).
3. Sayfa üstünde ince bir scroll-progress göstergesi (opsiyonel, iLovePDF'te yok ama modern SaaS sitelerinde yaygın — istersen ekle, zorunlu değil).
4. Performans notu: `ScrollTrigger` kurulumları `useGSAP()` içinde yapılmalı ve component unmount olduğunda `.kill()` ile temizlenmeli — aksi halde route değiştikçe hayalet ScrollTrigger instance'ları birikip performansı düşürür.

## Kabul Kriterleri

- [ ] Ana sayfa kartları sayfa yüklenince stagger ile beliriyor, hover'da tepki veriyor.
- [ ] Dosya yükleme akışının her adımı (ekleme/çıkarma/tamamlanma) animasyonlu, ani/sert geçiş yok.
- [ ] Scroll ile tetiklenen en az bir bölüm (ana sayfada) düzgün çalışıyor.
- [ ] Route değiştirildiğinde (bir tool sayfasından diğerine geçildiğinde) konsolda GSAP/ScrollTrigger ile ilgili sızıntı/uyarı yok — `useGSAP()` cleanup'ı doğrulanmış.
- [ ] Mobilde gesture'lar (dokunma, sürükleme varsa) düzgün çalışıyor, animasyonlar düşük performanslı cihazlarda da takılmıyor (60fps hedefi, ağır efektlerden kaçın).
- [ ] Animasyonlar işlevselliği geciktirmiyor — örn. dosya işleme sonucu animasyon bitmeden gösterilmiyor değil, animasyon sonucu göstermeyi engellemiyor.

## Not
Bitince özet ver, TASK 08 (production hazırlığı) için onay bekle.
