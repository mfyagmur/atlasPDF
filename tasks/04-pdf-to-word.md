# TASK 04 — PDF → Word

## Amaç
Kullanıcının PDF dosyasını düzenlenebilir .docx dosyasına çevirebilmesi.

## Backend

1. `app/tools/pdf_to_word/service.py`:
   - `pdf_to_word(input_path: Path, output_path: Path) -> Path`
   - `pdf2docx.Converter` kullan.
   - Taranmış (scanned/image-only) PDF'lerde metin çıkmayabilir — bu durumu tespit et (örn. sayfa başına çıkarılan metin karakter sayısı çok düşükse) ve kullanıcıya "Bu PDF taranmış görünüyor, sonuç düşük kaliteli olabilir" uyarısı döndür (hata değil, uyarı).
2. `app/tools/pdf_to_word/router.py`:
   - `POST /api/pdf-to-word` — 1 PDF dosyası.
   - Sayfa sayısı bir eşiği (örn. 30 sayfa) aşarsa yanıt gecikebileceğine dair not düş (MVP'de hâlâ senkron çalışır, ama frontend'e "biraz sürebilir" mesajı gönder).
   - Yanıt: download link (+ varsa `warning` alanı, taranmış PDF uyarısı için).

## Frontend

1. `/araclar/pdf-word` sayfası.
2. Tek PDF yükle → dönüştür → .docx indir.
3. Backend'den `warning` gelirse kullanıcıya sarı bir uyarı kutusu göster.
4. Büyük dosyalarda "işleniyor, bu biraz sürebilir" mesajı.

## Kabul Kriterleri

- [ ] Metin tabanlı bir PDF, doğru içerikle .docx'e dönüşüyor (Word'de açılabiliyor, metin seçilebiliyor).
- [ ] Taranmış/image-only bir PDF ile denendiğinde sistem çökmüyor, uyarı ile birlikte (mümkünse boş/minimal) sonuç dönüyor.
- [ ] Bozuk/şifreli PDF anlamlı hata veriyor.
- [ ] pytest: metin tabanlı PDF happy-path, taranmış PDF uyarı senaryosu (mock/örnek dosya ile).

## Not
Bitince özet ver, TASK 05 için onay bekle.
