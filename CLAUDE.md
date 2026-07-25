# CLAUDE.md — Proje Kök Talimat Dosyası

> Bu dosya, Claude Code'un bu repoda çalışırken her seferinde okuyup bağlam olarak kullanması için yazılmıştır. Kod yazarken burada tanımlı standartlara, klasör yapısına ve karar mimarisine sadık kal. Belirsizlik olursa `docs/ARCHITECTURE.md` ve `docs/TECH_STACK.md` dosyalarına bak.

## Proje Nedir

**Ad:** AtlasPDF (kod adı: `pdfkit`)
**Referans/ilham:** iLovePDF (ilovepdf.com) — ama tam kopyası değil, MVP kapsamı çok daha dar.
**Vizyon:** Mikro bir PDF araç seti olarak başlayıp, zamanla yeni "tool" modülleri eklenerek büyüyen bir platforma (mikrodan makroya) evrilecek. Bu yüzden mimari en baştan **eklenebilir (plugin-style) modüler** kurulacak — her PDF işlemi kendi bağımsız modülü olacak, birbirine sıkı bağımlı olmayacak.

## MVP Kapsamı (SADECE bunlar — başka özellik EKLEME)

1. **Merge** — Birden fazla PDF'i tek PDF'te birleştirme
2. **Split** — PDF'i sayfa aralığına göre bölme / her sayfayı ayrı dosya yapma
3. **Compress** — PDF dosya boyutunu küçültme (kalite seviyesi seçimi: düşük/orta/yüksek sıkıştırma)
4. **PDF → Word** — PDF'i düzenlenebilir .docx dosyasına çevirme
5. **PDF → Excel** — PDF içindeki tablo verisini .xlsx dosyasına çıkarma

MVP'de auth, ödeme, kullanıcı hesabı YOK. Anonim kullanım: dosya yükle → işle → indir → dosya X dakika sonra sunucudan otomatik silinir.

## Mikrodan Makroya Roadmap (bilgi amaçlı — şimdi kodlama)

- **Faz 0 (şimdi):** Monolith FastAPI backend + Next.js (veya vite tech_stack.md yazacak yoksa sorulacak) frontend, senkron/kuyruklu 5 tool.
- **Faz 1:** Kullanıcı hesabı, geçmiş işlemler, dosya limiti/rate limit.
- **Faz 2:** Stripe ile ücretli plan, daha fazla tool (OCR, watermark, e-imza, PDF→PPT vb.).
- **Faz 3:** Ağır işlemler (OCR, convert) ayrı worker servislerine ayrılır (mikroservise geçiş), her tool bağımsız ölçeklenir.

Kod yazarken Faz 0'ı kodla ama Faz 1-3'ü imkansızlaştıracak kısayollara sapma (örn. her şeyi tek dosyaya gömmek, tool'ları birbirine hardcoded bağlamak).

## Klasör Yapısı (hedef)

```
pdf-saas/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/            # config, ayarlar, ortak yardımcılar
│   │   ├── tools/           # HER TOOL KENDİ ALT KLASÖRÜNDE
│   │   │   ├── merge/
│   │   │   ├── split/
│   │   │   ├── compress/
│   │   │   ├── pdf_to_word/
│   │   │   └── pdf_to_excel/
│   │   ├── storage/         # geçici dosya yönetimi, otomatik silme
│   │   └── api/              # router'lar
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── routes/           # React Router v7 route dosyaları
│   │   └── components/
│   │       ├── ui/           # shadcn/ui bileşenleri (kopyalanmış kaynak kod)
│   │       └── shared/       # FileUploader, ProgressIndicator vb. ortak bileşenler
│   ├── vite.config.ts
│   └── package.json
├── docker-compose.yml
├── docs/
└── tasks/
```

## Kodlama Standartları

- **Backend:** Python 3.12+, FastAPI, `async def` endpoint'ler, Pydantic v2 modelleri, tip anotasyonlu her fonksiyon.
- **Her tool bir "black box":** girdi dosya yolu/yolları al, çıktı dosya yolu ver. Router katmanı sadece dosya kabul/döndürme ve hata yönetimi yapar, iş mantığı `tools/<isim>/service.py` içinde olur.
- **Hata yönetimi:** Kullanıcıya asla stack trace gösterme; anlamlı Türkçe/İngilizce hata mesajı + uygun HTTP status code.
- **Dosya güvenliği:** Yüklenen dosyalar UUID isimlendirilir, sadece `.pdf` (ilgili tool'a göre) kabul edilir, boyut limiti (örn. 50MB) uygulanır, MIME type doğrulanır (sadece uzantıya güvenme).
- **Geçici dosya temizliği:** Her işlem sonrası dosyalar TTL (örn. 1 saat) sonra otomatik silinir (cron job veya arka plan task).
- **Frontend:** Vite + React Router v7 (framework mode) + TypeScript + Tailwind CSS v4 + shadcn/ui. Her tool sayfası `/araclar/<tool-slug>` altında, ortak `FileUploader` ve `ProgressIndicator` component'leri paylaşılır. Component giriş/çıkış ve gesture animasyonları **Motion** ile, scroll/timeline animasyonları **GSAP ScrollTrigger** ile yapılır — ikisini karıştırmadan, hangi işin hangisine ait olduğuna (component-level → Motion, scroll-level → GSAP) sadık kal. Yeni bir UI parçası gerektiğinde önce `npx shadcn@latest add <component>` ile ekle, sıfırdan yazma.
- **Test:** Her tool servisi için en az 1 happy-path + 1 hata-durumu pytest testi.
- **Commit mesajları:** Türkçe veya İngilizce olabilir ama tutarlı olsun, conventional commits tercih edilir (`feat:`, `fix:`, `chore:`).

## Görev (Task) Dosyalarını Nasıl Kullanacaksın

`tasks/` klasöründeki dosyalar sıra numarasıyla (00, 01, 02...) verilmiştir. Her task dosyası:
- Ne yapılacağını
- Hangi dosyaların oluşturulacağını/değişeceğini
- Kabul kriterlerini (acceptance criteria)
- İlgili kod/kurulum komutlarını içerir.

Bir task'a başlamadan önce bir önceki task'ın kabul kriterlerinin karşılandığından emin ol. Bir task bitince kısa bir özet ver ve bir sonraki task'a geçip geçmeyeceğimi sor — otomatik ilerleme, benim onayımla ilerleme.

## Genel Kurallar

- Kapsam dışına çıkma: MVP'de listelenmeyen özellik/tool ekleme, kimse istemedi.
- Aşırı mühendislik yapma: MVP basit ve çalışır olsun, mikroservis/kubernetes gibi şeyler Faz 3'e kadar gündeme gelmesin.
- Her önemli mimari kararda kısaca gerekçeni açıkla (1-2 cümle yeterli).
- Belirsiz bir noktada durup bana sor, varsayımla ilerleyip geri dönmek zorunda kalma.
