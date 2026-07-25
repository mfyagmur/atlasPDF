# TASK 05 — PDF → Excel

## Amaç
Kullanıcının PDF içindeki tablo(lar)ı .xlsx dosyasına çıkarabilmesi.

## Backend

1. `app/tools/pdf_to_excel/service.py`:
   - `pdf_to_excel(input_path: Path, output_path: Path) -> Path`
   - `pdfplumber` ile her sayfadaki tabloları tespit et (`page.extract_tables()`).
   - Her tespit edilen tabloyu `openpyxl` ile ayrı bir sheet'e yaz (sheet adı örn. `Sayfa1_Tablo1`).
   - Hiç tablo bulunamazsa: sayfa metnini satır satır tek bir sheet'e dök ve kullanıcıya "Tablo tespit edilemedi, metin çıkarıldı" uyarısı döndür.
2. `app/tools/pdf_to_excel/router.py`:
   - `POST /api/pdf-to-excel` — 1 PDF dosyası.
   - Yanıt: download link + `tables_found: int` + varsa `warning`.

## Frontend

1. `/araclar/pdf-excel` sayfası.
2. Tek PDF yükle → dönüştür → .xlsx indir.
3. Sonuçta "X tablo bulundu" bilgisini göster; tablo bulunamadıysa uyarıyı göster.

## Kabul Kriterleri

- [ ] Düzenli tablo içeren bir PDF'ten doğru satır/sütun yapısında .xlsx üretiliyor.
- [ ] Birden fazla tablo/sayfa içeren PDF'te her tablo ayrı sheet'te.
- [ ] Tablosuz bir PDF'te sistem çökmüyor, metin fallback + uyarı çalışıyor.
- [ ] pytest: tablo tespiti happy-path, çoklu tablo senaryosu, tablosuz PDF fallback senaryosu.

## Not
Bitince özet ver, TASK 06 için onay bekle. (5 tool da tamamlandı — bir sonraki adım genel arayüz/anasayfa ve production hazırlığı.)
