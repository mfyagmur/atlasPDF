# AtlasPDF

Mikro bir PDF araç seti: PDF birleştirme, bölme, sıkıştırma, PDF → Word ve PDF → Excel dönüşümü. Anonim kullanım — dosya yükle, işle, indir; dosyalar bir süre sonra sunucudan otomatik silinir.

MVP kapsamı, mimari kararlar ve klasör yapısı için [CLAUDE.md](CLAUDE.md) dosyasına, teknoloji seçimleri için [docs/TECH_STACK.md](docs/TECH_STACK.md) dosyasına bakın.

## Teknolojiler

- **Backend:** Python 3.14, FastAPI
- **Frontend:** Vite + React Router v7 (framework mode) + TypeScript + Tailwind CSS v4 + shadcn/ui

## Çalıştırma (Docker ile)

```bash
docker compose up
```

- Backend: http://localhost:8000 (health check: `GET /health`)
- Frontend: http://localhost:3000

## Çalıştırma (yerel geliştirme)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

> Not: `pikepdf` ve `pdf2docx` gibi C-extension içeren kütüphaneler Windows'ta Python 3.14 için önceden derlenmiş wheel bulamayabilir (Visual C++ Build Tools gerektirir). Bu durumda Docker ile çalıştırmak veya Python 3.12 kullanmak önerilir — mimariyi etkilemez.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Proje Yapısı

```
backend/app/
├── main.py       # FastAPI app, CORS, /health
├── core/         # config, ortak yardımcılar
├── tools/        # her PDF işlemi kendi alt klasöründe
├── storage/      # geçici dosya yönetimi (uploads/, outputs/)
└── api/          # router'lar

frontend/app/
├── routes/       # React Router v7 route dosyaları
└── components/
    ├── ui/       # shadcn/ui bileşenleri
    └── shared/   # ortak bileşenler (FileUploader, HealthCheck, vb.)
```
