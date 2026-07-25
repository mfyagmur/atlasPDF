# ARCHITECTURE.md — Sistem Mimarisi

## 1. Genel Yaklaşım: Modüler Monolith

MVP'de mikroservis YOK. Tek FastAPI uygulaması ama içeride her PDF işlemi (tool) kendi bağımsız modülü. Bunun sebebi:
- Tek servis = tek deploy, düşük operasyonel yük, hızlı MVP.
- "Modüler" olduğu için Faz 3'te bir tool'u ayrı bir servise (mikroservise) çıkarmak, sadece o klasörü taşımak kadar kolay olur.

```
İstemci (Next.js)
      │  (HTTPS, multipart/form-data dosya yükleme)
      ▼
FastAPI Backend (tek servis)
      │
      ├─ /api/merge        → tools/merge/service.py
      ├─ /api/split        → tools/split/service.py
      ├─ /api/compress     → tools/compress/service.py
      ├─ /api/pdf-to-word  → tools/pdf_to_word/service.py
      └─ /api/pdf-to-excel → tools/pdf_to_excel/service.py
      │
      ▼
Geçici Depolama (yerel disk MVP'de, sonra S3/MinIO)
      │
      ▼
Arka plan temizlik görevi (TTL sonrası dosya silme)
```

## 2. Senkron mu, Asenkron (Kuyruklu) mu?

- **Merge, Split:** Genelde hızlı (saniyeler) → senkron endpoint yeterli, MVP'de kuyruk gerekmez.
- **Compress:** Orta boy dosyalarda hızlı, çok büyük dosyalarda yavaşlayabilir → MVP'de senkron, ileride kuyruğa alınabilir.
- **PDF→Word, PDF→Excel:** Daha ağır CPU işlemi (özellikle OCR gerekiyorsa) → **başta senkron dene, dosya boyutu/sayfa sayısı bir eşiği geçerse** (örn. 20 sayfa) kullanıcıya "bu biraz sürebilir" uyarısı ver. Gerçek kullanıcı yükü arttığında Celery + Redis kuyruğuna geçilecek (Faz 1-2).

Bu yaklaşımın gerekçesi: MVP'de Redis/Celery kurup operasyonel karmaşıklık eklemeye gerek yok, ama kod öyle yazılmalı ki (`service.py` fonksiyonları senkron, saf fonksiyon gibi) ileride bir Celery task'ı içine sarmak 1 satırlık değişiklik olsun.

## 3. Dosya Yaşam Döngüsü

1. Kullanıcı dosya yükler → backend `storage/uploads/<uuid>.pdf` içine kaydeder.
2. İlgili tool işler → sonucu `storage/outputs/<uuid>.<ext>` içine yazar.
3. Kullanıcıya indirme linki (kısa ömürlü, imzalı/token'lı) döner.
4. Arka plan görevi (basit bir zamanlanmış fonksiyon, `apscheduler` veya cron) TTL'den (örn. 60 dk) eski dosyaları siler.

**Neden bu önemli:** Kullanıcı verisi (potansiyel olarak hassas PDF'ler) sunucuda süresiz kalmamalı — hem disk hem gizlilik açısından.

## 4. Teknoloji Seçim Gerekçeleri (özet — detay TECH_STACK.md'de)

| Katman | Seçim | Neden |
|---|---|---|
| Backend framework | FastAPI | Async destek, otomatik OpenAPI docs, Python PDF kütüphaneleriyle uyum |
| PDF merge/split | `pypdf` | Saf Python, bağımlılık yok, hafif |
| PDF compress | `pikepdf` (qpdf tabanlı) veya Ghostscript | Gerçek sıkıştırma (pypdf sıkıştırma yapmaz) |
| PDF→Word | `pdf2docx` | Layout'u makul koruyarak dönüştürür |
| PDF→Excel | `pdfplumber` (tablo çıkarma) + `openpyxl` (xlsx yazma) | Tablo tespiti + Excel yazımı ayrı sorumluluk |
| Frontend build | Vite + React Router v7 (framework mode) | Vite'ın esnekliği + framework mode'da SSR desteği (SEO için gerekli) |
| Bileşen altyapısı | shadcn/ui (Radix UI + Tailwind) | Kaynak kod olarak repo'ya kopyalanır → %100 özelleştirilebilir, Tailwind-native |
| Component/gesture animasyonu | Motion (Framer Motion) | Giriş/çıkış, sürükleme, dokunma etkileşimleri için React standardı |
| Scroll/timeline animasyonu | GSAP + ScrollTrigger | Karmaşık scroll-timeline senaryoları için endüstri standardı, artık tamamen ücretsiz |
| Konteynerleştirme | Docker + docker-compose | Yerelde ve production'da tutarlı ortam |

> **SEO notu:** Saf Vite (SSR kapalı) client-side rendering yapar, arama motoru botu boş bir kök `<div>` görür. Bu proje organik aramadan trafik alacağı için React Router v7'nin framework mode'unda SSR açık tutulmalı — Vite'ın esnekliğinden ödün vermeden bu problemi çözer.

## 5. Mikrodan Makroya — Somut Evrim Adımları

**Faz 0 → Faz 1 geçişi tetikleyicileri:** Kullanıcılar hesap/geçmiş istiyor, rate-limit abuse başlıyor.
- Postgres + basit auth (email/magic link veya Clerk gibi hazır servis) eklenir.
- `users`, `jobs` tabloları eklenir; her işlem bir `job` kaydına bağlanır.

**Faz 1 → Faz 2 geçişi tetikleyicileri:** Ücretli plan talebi, yeni tool talepleri.
- Stripe entegrasyonu, plan bazlı limit (örn. ücretsiz: 5 işlem/gün).
- Yeni tool eklemek = `tools/<yeni_tool>/` klasörü açmak + router'a 1 satır eklemek (mimari bunu MVP'den beri destekliyor).

**Faz 2 → Faz 3 geçişi tetikleyicileri:** Belirli tool'lar (OCR, convert) trafiğin çoğunu tüketiyor, tek servis darboğaz oluyor.
- O tool'un `service.py`'ı ayrı bir FastAPI/worker servisine taşınır, ana servis ona HTTP/queue üzerinden istek atar.
- Bu noktada her tool zaten bağımsız modül olduğu için taşıma maliyeti düşük olur — mimarinin asıl amacı bu.

## 6. Güvenlik Notları (MVP'den itibaren)

- Dosya MIME/type doğrulama (uzantıya değil içeriğe bakarak, örn. `python-magic`).
- Dosya boyutu limiti (öneri: 50MB, ileride plana göre değişebilir).
- Rate limiting (MVP'de basit IP bazlı, örn. `slowapi`).
- CORS sadece frontend domain'ine izin versin.
- Yüklenen PDF'ler zararlı içerik (embedded JS vb.) taşıyabilir — işleme sırasında bunları temizleyen kütüphaneler tercih edilir (`pikepdf` bu konuda güvenli).
