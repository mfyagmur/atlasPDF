# TASK 03 — Compress (PDF Sıkıştırma)

## Amaç
Kullanıcının PDF dosya boyutunu küçültebilmesi, kalite seviyesi seçerek (iLovePDF'teki gibi: düşük/orta/yüksek sıkıştırma).

## Backend

1. `app/tools/compress/service.py`:
   - `compress_pdf(input_path: Path, output_path: Path, level: Literal["low","recommended","extreme"]) -> Path`
   - Öncelik: Ghostscript komut satırı aracı (`subprocess` ile çağır) — `-dPDFSETTINGS` parametresi ile seviye ayarla:
     - `low` → `/printer` (az sıkıştırma, yüksek kalite)
     - `recommended` → `/ebook` (dengeli)
     - `extreme` → `/screen` (agresif sıkıştırma, düşük kalite)
   - Ghostscript yoksa/başarısız olursa `pikepdf` ile fallback sıkıştırma (en azından stream compression) yap.
   - Orijinal ve sıkıştırılmış boyutu karşılaştırıp yüzde kazanç bilgisini de döndür.
2. `app/tools/compress/router.py`:
   - `POST /api/compress` — 1 PDF + `level` parametresi.
   - Yanıt: download link + `original_size`, `compressed_size`, `savings_percent`.

## Frontend

1. `/araclar/sikistir` sayfası.
2. Tek PDF yükle, 3 seviye arasında seçim (radio button/kart UI, iLovePDF tarzı).
3. Sonuç ekranında "X MB → Y MB (%Z küçültme)" gibi bir özet göster.

## Kabul Kriterleri

- [ ] 3 seviyenin de farklı çıktı boyutu ürettiği doğrulanıyor (extreme < recommended < low boyut olarak).
- [ ] Zaten küçük/optimize PDF'lerde hata vermiyor, sadece minimal kazanç gösteriyor.
- [ ] Ghostscript kurulu değilse sistem çökmüyor, fallback devreye giriyor (bunun testi için Docker image'da Ghostscript'in kurulu olduğunu doğrula; fallback yine de kod olarak var olsun).
- [ ] pytest: her 3 seviye için happy-path, + Ghostscript'siz fallback testi (mock ile).

## Not
Bitince özet ver, TASK 04 için onay bekle.
