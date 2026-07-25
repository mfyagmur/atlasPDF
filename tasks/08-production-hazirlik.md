# TASK 08 — Production Hazırlığı ve Deployment

## Amaç
MVP'yi gerçek kullanıcılara açılabilir hale getirmek: güvenlik sağlamlaştırma, dosya temizliği otomasyonu, temel izleme, deploy.

## Yapılacaklar

1. **Rate limiting:** `slowapi` ile her endpoint'e IP bazlı limit (örn. dakikada 10 istek) — kötüye kullanımı önlemek için.
2. **Dosya temizliği otomasyonu:** `apscheduler` ile her N dakikada bir `storage/uploads` ve `storage/outputs` altında TTL'i geçen dosyaları silen bir job. Bu job'ın loglaması olsun (kaç dosya silindi).
3. **Ortam değişkenleri:** `.env.example` dosyası oluştur (API URL, dosya boyutu limiti, TTL süresi, CORS origin'leri gibi ayarlar kod içine gömülü olmasın).
4. **Loglama:** Backend'de yapılandırılmış loglama (örn. `structlog` veya standart `logging` ile JSON format) — her tool çağrısı, süresi, başarı/hata durumu loglansın.
5. **Health/monitoring:** `/health` endpoint'ini genişlet (disk doluluk oranı gibi temel bilgi eklenebilir, opsiyonel).
6. **Nginx/Caddy reverse proxy config** taslağı (SSL, gzip, dosya upload boyutu limiti ayarları dahil).
7. **Deploy dokümantasyonu:** `docs/DEPLOYMENT.md` — seçilen hosting'e (VPS/Railway/Render, karar bana ait, sen sadece seçenekleri ve adımları yaz) göre adım adım deploy talimatı.
8. **Basit smoke test checklist'i:** Deploy sonrası manuel kontrol edilecek maddeler listesi (5 tool'un her biri gerçek dosyayla test edilmeli).

## Kabul Kriterleri

- [ ] Rate limit çalışıyor, limiti aşan istek 429 dönüyor.
- [ ] Dosya temizliği job'ı çalışıyor ve loglanıyor (test: eski tarihli sahte dosya oluştur, job'ın sildiğini doğrula).
- [ ] Tüm hassas/ortama-özgü ayarlar `.env` üzerinden okunuyor, kodda hardcoded değil.
- [ ] Loglar okunabilir ve her tool çağrısı iz bırakıyor.
- [ ] `docs/DEPLOYMENT.md` takip edilerek sıfırdan bir sunucuya deploy yapılabiliyor.

## Not
Bu son MVP task'ı. Bitince genel bir "MVP tamamlandı" özeti iste benden — nelerin çalıştığı, bilinen sınırlamalar, Faz 1 için önerilerin neler olduğu.
