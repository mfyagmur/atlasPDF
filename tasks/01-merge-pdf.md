# TASK 01 — Merge (PDF Birleştirme)

## Amaç
Kullanıcının birden fazla PDF dosyası yükleyip tek bir PDF olarak indirebilmesi.

## Backend

1. `app/tools/merge/service.py`:
   - `merge_pdfs(input_paths: list[Path], output_path: Path) -> Path` fonksiyonu.
   - `pypdf.PdfWriter` kullanarak dosyaları verilen sırayla birleştir.
   - Şifreli/bozuk PDF gelirse anlamlı bir exception fırlat (örn. `InvalidPDFError`).
2. `app/tools/merge/router.py`:
   - `POST /api/merge` — çoklu dosya kabul eder (`UploadFile` listesi).
   - Doğrulamalar: en az 2 dosya, her biri gerçekten PDF (MIME kontrolü), toplam boyut limiti (örn. 50MB).
   - Dosyaları `storage/uploads/` altına UUID isimle kaydet, `merge_pdfs` çağır, sonucu `storage/outputs/` altına yaz.
   - Yanıt: indirme için dosya id/token döner (örn. `{"file_id": "...", "download_url": "/api/download/<id>"}`).
3. Ortak bir `GET /api/download/{file_id}` endpoint'i (bu ve sonraki tüm tool'lar bunu paylaşacak) — `app/api/download.py` içinde, ilk burada oluşturulacak.
4. Hata durumları: 2'den az dosya → 400, dosya PDF değil → 415, dosya çok büyük → 413.

## Frontend

1. `/araclar/birlestir` sayfası.
2. Çoklu dosya sürükle-bırak (`react-dropzone`, `multiple: true`).
3. Yüklenen dosyaların listesi + sürükleyerek sıra değiştirme (basit MVP: yukarı/aşağı ok butonlarıyla da olur, drag-reorder şart değil).
4. "Birleştir" butonu → backend'e istek → işlem sırasında yükleniyor göstergesi → tamamlanınca indirme linki.
5. Hata mesajlarını kullanıcıya anlaşılır şekilde göster (Türkçe).

## Kabul Kriterleri

- [ ] 2+ PDF yüklenip doğru sırada birleştirilmiş tek PDF indirilebiliyor.
- [ ] 1 dosya ile denenirse anlamlı hata mesajı dönüyor.
- [ ] PDF olmayan dosya yüklenirse reddediliyor.
- [ ] Şifreli/bozuk PDF ile denenirse çökme değil, düzgün hata mesajı.
- [ ] `pytest` ile en az: happy-path testi + "1 dosya ile hata" testi + "geçersiz dosya" testi.
- [ ] İndirilen dosya bir süre sonra (TTL) sunucudan siliniyor (bu task'ta basit bir zamanlayıcı yeterli, tam otomasyon TASK 06/07'de olgunlaştırılabilir).

## Not
Bitince özet ver, TASK 02 için onay bekle.
