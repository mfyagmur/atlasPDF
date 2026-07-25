# TASK 02 — Split (PDF Bölme)

## Amaç
Kullanıcının tek bir PDF'i sayfa aralıklarına göre bölebilmesi veya her sayfayı ayrı dosya olarak çıkarabilmesi.

## Backend

1. `app/tools/split/service.py`:
   - `split_pdf(input_path: Path, ranges: list[tuple[int, int]] | None, output_dir: Path) -> list[Path]`
   - İki mod: (a) belirli sayfa aralıkları verilir (örn. `[(1,3), (4,10)]`), (b) `ranges=None` ise her sayfa ayrı dosya olur.
   - Çıktı birden fazla dosya olacağı için sonuçları bir ZIP'te paketle (`zipfile`), kullanıcı tek bir ZIP indirsin.
2. `app/tools/split/router.py`:
   - `POST /api/split` — 1 PDF dosyası + opsiyonel `ranges` parametresi (JSON string, örn. `"1-3,4-10"` formatını parse et).
   - Sayfa numarası dosyanın toplam sayfa sayısını aşarsa 400 hatası.
   - Yanıt: ZIP dosyası için download link.

## Frontend

1. `/araclar/bol` sayfası.
2. Tek PDF yükle → backend'den sayfa sayısını öğrenip kullanıcıya göster (küçük bir "sayfa sayısını al" endpoint'i gerekebilir, `GET /api/pdf-info` gibi — bunu da bu task'ta ekle).
3. İki seçenek sun: "Her sayfayı ayır" / "Aralık belirle" (basit bir metin input: `1-3, 4-10`).
4. Sonuç ZIP indirme linki.

## Kabul Kriterleri

- [ ] "Her sayfayı ayır" modu doğru sayıda tek sayfalık PDF üretiyor, ZIP içinde.
- [ ] Aralık modu, girilen aralıklara göre doğru PDF parçaları üretiyor.
- [ ] Sayfa sayısını aşan aralık girilirse anlamlı hata.
- [ ] Geçersiz aralık formatı (örn. "abc") güvenli şekilde reddediliyor.
- [ ] pytest: happy-path (aralık), happy-path (tüm sayfalar), hata durumu (aralık aşımı) testleri.

## Not
Bitince özet ver, TASK 03 için onay bekle.
