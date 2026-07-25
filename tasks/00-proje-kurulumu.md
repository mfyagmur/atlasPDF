# TASK 00 — Proje Kurulumu ve İskelet

## Amaç
Backend ve frontend için temel proje iskeletini kurmak. Henüz hiçbir PDF işlevi yok — sadece çalışan bir "hello world" seviyesi FastAPI + Vite/React Router iskeleti ve aralarındaki bağlantı.

## Yapılacaklar

1. `docs/TECH_STACK.md`'deki komutlarla `backend/` (Python 3.14, FastAPI) ve `frontend/` (Vite + React Router v7 framework mode + Tailwind v4 + shadcn/ui init) klasörlerini oluştur.
2. Backend'de `app/main.py` içinde:
   - FastAPI app instance'ı
   - CORS middleware (frontend origin'e izin ver)
   - `GET /health` endpoint'i → `{"status": "ok"}` döner
3. Backend klasör yapısını `CLAUDE.md`'deki hedef yapıya göre oluştur (`app/core`, `app/tools`, `app/storage`, `app/api` — boş `__init__.py` dosyalarıyla).
4. `app/storage/` altında geçici dosyalar için `uploads/` ve `outputs/` klasörleri (git'e dahil olmasın, `.gitignore`'a ekle, sadece `.gitkeep` ile klasör yapısı korunsun).
5. Frontend'de:
   - `npx shadcn@latest init` ile shadcn/ui kurulumu (Tailwind v4 ile birlikte).
   - `motion`, `gsap`, `@gsap/react`, `react-dropzone` paketlerini kur.
   - Basit bir ana sayfa: başlık + backend `/health` endpoint'ine fetch atıp sonucu ekranda gösteren bir test bileşeni (bağlantı çalışıyor mu diye).
   - shadcn/ui'dan 1-2 temel component ekle (`button`, `card`) ve ana sayfada kullanarak kurulumun çalıştığını doğrula.
6. `docker-compose.yml` ve her iki `Dockerfile`'ı ekle, `docker-compose up` ile ikisinin de ayağa kalktığını doğrula.
7. Kök dizine `.gitignore` ekle (Python: `venv/`, `__pycache__/`; Node: `node_modules/`, `.react-router/`, `build/`; ayrıca `storage/uploads/*`, `storage/outputs/*`).
8. `README.md` (proje kökünde) — projenin ne olduğu, nasıl çalıştırılacağı (kısa kurulum talimatı).

## Kabul Kriterleri

- [ ] `docker-compose up` komutu hatasız çalışıyor, backend 8000 portunda, frontend 3000 portunda ayakta.
- [ ] `curl http://localhost:8000/health` → `{"status":"ok"}` dönüyor.
- [ ] Frontend ana sayfası açıldığında backend'den gelen health check sonucunu gösteriyor (bağlantı kanıtlanmış oluyor).
- [ ] shadcn/ui `Button` ve `Card` component'leri ana sayfada görünür şekilde çalışıyor.
- [ ] Klasör yapısı `CLAUDE.md`'de tanımlanan hedef yapıyla birebir uyumlu.
- [ ] `.gitignore` doğru çalışıyor, `venv/`, `node_modules/`, geçici dosyalar repoya girmiyor.

## Not
Bu task bitince bana kısa bir özet ver (ne oluşturuldu, nasıl test edilir) ve TASK 01'e geçmemi onaylamamı bekle.
