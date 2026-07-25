# TASK 06 — Ana Sayfa ve Genel Arayüz Toparlama

## Amaç
5 tool ayrı ayrı çalışıyor artık; bunları tek, tutarlı ve görsel olarak profesyonel bir siteye bağlamak. iLovePDF'in ana sayfası gibi: bir grid içinde tool kartları, her biri kendi sayfasına götürüyor. (Animasyon/geçiş katmanı bu task'ta DEĞİL, bir sonraki TASK 07'de ele alınacak — burada sadece statik/işlevsel arayüz tamamlanıyor.)

## Yapılacaklar

1. Ana sayfa (`/`): Site başlığı, kısa açıklama, 5 tool'un kart grid'i (shadcn/ui `Card` component'i + ikon + isim + kısa açıklama + tıklanınca `/araclar/<slug>`'a gider).
2. Ortak layout: header (logo/isim, ileride "Giriş Yap" için yer tutucu ama MVP'de pasif) + footer.
3. Ortak component'lerin tekilleştirilmesi: `FileUploader`, `ProgressIndicator`, `DownloadCard`, `ErrorBanner` — `app/components/shared/` altında, her tool sayfası bunları import etsin (kod tekrarını temizle, bu task'ta refactor de kapsamda). Mümkün olduğunca shadcn/ui primitive'leri (`Button`, `Progress`, `Alert`, `Dialog`) üzerine inşa et, sıfırdan yazma.
4. Responsive kontrol: mobilde de kartlar ve upload akışı düzgün görünsün.
5. Basit bir 404 sayfası ve genel hata sınırı (React Router `ErrorBoundary`).
6. Temel SEO: her tool route'una `meta` fonksiyonu ile `<title>` ve `<meta description>` (React Router v7'nin route-level meta API'si), SSR açık olduğu için bunlar gerçekten sunucu tarafında render edilip arama motoruna gidecek.

## Kabul Kriterleri

- [ ] Ana sayfadan 5 tool'un tamamına tek tıkla ulaşılabiliyor.
- [ ] Tüm tool sayfaları aynı görsel dile (renk, tipografi, spacing) sahip.
- [ ] Kod tekrarı azaltıldı: upload/progress/error UI'ları ortak component'lerden geliyor.
- [ ] Mobil genişlikte (375px) arayüz bozulmuyor.
- [ ] Her sayfa kendine özgü `<title>` içeriyor ve `view-source` ile bakıldığında (SSR sayesinde) içerik boş değil.

## Not
Bitince özet ver, TASK 07 (animasyon/etkileşim katmanı) için onay bekle.
