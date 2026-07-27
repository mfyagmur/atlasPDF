# SMOKE_TEST.md — Deploy Sonrası Manuel Kontrol Listesi

> Her deploy'dan (veya önemli backend değişikliğinden) sonra bu listeyi baştan sona çalıştırın. Gerçek dosyalarla test edin, fixture değil — en az 2 sayfalık, tablo içeren gerçek bir PDF ve merge testi için ikinci bir PDF hazırlayın.

- [ ] `GET /health` → 200 döner, `status: "ok"` ve makul disk sayıları içerir.
- [ ] `POST /api/merge` — 2 gerçek PDF ile → 200, `download_url` çalışır, birleşen PDF açılır ve toplam sayfa sayısı doğrudur.
- [ ] `POST /api/pdf-info` — gerçek bir PDF ile → 200, doğru sayfa sayısı döner.
- [ ] `POST /api/split` — çok sayfalı gerçek bir PDF ile → 200, indirilen ZIP açılır ve beklenen sayıda dosya içerir.
- [ ] `POST /api/compress` (`level=recommended`) → 200, `compressed_size < original_size`, çıktı PDF açılır.
- [ ] `POST /api/pdf-to-word` — gerçek bir PDF ile → 200, çıktı `.docx` Word/LibreOffice'te açılır.
- [ ] `POST /api/pdf-to-excel` — tablo içeren gerçek bir PDF ile → 200, çıktı `.xlsx` açılır ve tablo verisi doğru.
- [ ] `GET /api/download/{bilinmeyen-id}` → 404, anlaşılır hata mesajı (stack trace yok).
- [ ] PDF olmayan bir dosya yükle → 415, anlaşılır hata mesajı.
- [ ] `MAX_TOTAL_UPLOAD_MB` üzerinde bir dosya yükle → 413.
- [ ] Rate limit: aynı endpoint'e 60 saniye içinde `RATE_LIMIT_PER_MINUTE`'dan (varsayılan 10) fazla istek gönder → limiti aşan istek 429 döner.
- [ ] Temizlik: `storage/uploads` içine eski `mtime`'lı sahte bir dosya bırak, bir temizlik döngüsü bekle (veya `cleanup_expired_files`'ı manuel çağır) → dosya silinir ve `cleanup_run_completed` JSON log satırı `deleted_count >= 1` ile görünür.
- [ ] CORS: deploy edilen frontend origin'inden istek başarılı; `CORS_ORIGINS`'te olmayan bir origin'den istek tarayıcı tarafından engellenir.
- [ ] Loglar: her tool çağrısı için `tool`, `duration_ms`, `success` alanlarını içeren geçerli JSON satırları görünür.
