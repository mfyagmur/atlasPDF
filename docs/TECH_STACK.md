# TECH_STACK.md — Teknoloji Yığını ve Kurulum

## Backend

- **Dil/Framework:** Python 3.14+, FastAPI, Uvicorn (ASGI server)
- **PDF işleme kütüphaneleri:**
  - `pypdf` — merge, split
  - `pikepdf` — compress, PDF temizleme/normalize etme
  - `pdf2docx` — PDF → Word
  - `pdfplumber` — PDF'ten tablo/metin çıkarma (PDF → Excel için)
  - `openpyxl` — Excel (.xlsx) dosyası yazma
  - `python-magic` — gerçek dosya tipi doğrulama
- **Diğer:** `python-multipart` (dosya upload), `pydantic` v2, `apscheduler` (zamanlanmış temizlik görevi), `slowapi` (rate limiting)

> **Not (Python 3.14 uyumluluğu):** `pikepdf` ve `pdf2docx` gibi C-extension içeren kütüphanelerin 3.14 wheel'leri kurulum sırasında test edilmeli. Sorun çıkarsa `pyenv` ile 3.12'ye düşmek mimariyi etkilemeyen tek satırlık bir değişikliktir — bu yüzden bir engel değil, sadece kurulumda doğrulanacak bir madde.

### Sistem Bağımlılığı: Ghostscript (opsiyonel ama önerilir)

```bash
apt-get update && apt-get install -y ghostscript
```

### requirements.txt

```
fastapi==0.115.*
uvicorn[standard]==0.32.*
pypdf==5.1.*
pikepdf==9.4.*
pdf2docx==0.5.*
pdfplumber==0.11.*
openpyxl==3.1.*
python-multipart==0.0.*
python-magic==0.4.*
apscheduler==3.10.*
slowapi==0.1.*
pydantic-settings==2.6.*
pytest==8.3.*
httpx==0.27.*
```

### Kurulum (backend)

```bash
cd backend
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## Frontend

### Karar: Neden bu stack?

Next.js yerine **Vite** tercih edildi (akıcı, tamamen özelleştirilebilir bir animasyon/etkileşim katmanı için Vite'ın hafifliği ve esnekliği isteniyor). Ancak saf Vite CSR (client-side rendering) yaptığı için SEO zayıf kalır — bu proje organik aramadan (`pdf birleştir`, `pdf sıkıştır` vb.) trafik alacağı için bu bir risk. Çözüm: **React Router v7'yi "framework mode"da kullanmak** — Vite tabanlı, dosya tabanlı routing veriyor, istenirse (SOR) SSR (server-side rendering) açılabiliyor. Böylece Vite'ın esnekliği korunurken SEO problemi çözülüyor.

### Seçilen Teknolojiler

- **Build/Framework:** Vite + React Router v7 (framework mode) + TypeScript
- **Stil:** Tailwind CSS v4 (`@tailwindcss/vite` eklentisi ile, ayrı PostCSS config gerekmiyor)
- **Bileşen altyapısı:** **shadcn/ui** (Radix UI primitive'leri üzerine kurulu)
  - *Neden bu, MUI/Ant Design değil:* shadcn/ui component'leri paket olarak değil, kaynak kod olarak repo'ya kopyalanır → gerçek anlamda %100 özelleştirilebilir, "kara kutu" yok. Tailwind ile native uyumlu. Ekosistemi (shadcn registry, Aceternity UI, Magic UI gibi Motion-tabanlı zengin bileşen blokları) kurumsal projelerde yaygın kullanılıyor ve zaten animasyon-öncelikli tasarlanmışlar — bizim ihtiyacımızla birebir örtüşüyor.
- **Component animasyonları / gesture (sürükleme, dokunma, giriş-çıkış):** **Motion** (eski adıyla Framer Motion) — `AnimatePresence` (mount/unmount), `drag`, `whileHover`, `whileTap`, layout animasyonları.
- **Scroll tabanlı ve timeline animasyonları:** **GSAP + ScrollTrigger** — 2025'te Webflow'un GSAP'ı satın almasıyla ScrollTrigger dahil tüm eklentiler tamamen ücretsiz oldu (ticari kullanım dahil). Karmaşık scroll-timeline senaryoları için Motion'dan daha güçlü, bu yüzden ikisini birlikte kullanıyoruz: Motion = component/gesture, GSAP = scroll/timeline.
- **Dosya yükleme UI:** `react-dropzone`
- **HTTP client:** native `fetch`

### Kurulum (frontend)

```bash
npx create-react-router@latest frontend
cd frontend
npm install -D tailwindcss @tailwindcss/vite
npm install motion gsap @gsap/react react-dropzone
npx shadcn@latest init
```

`vite.config.ts` içine Tailwind eklentisini ekle:

```ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { reactRouter } from "@react-router/dev/vite";

export default defineConfig({
  plugins: [reactRouter(), tailwindcss()],
});
```

shadcn/ui component eklemek (ihtiyaç oldukça):

```bash
npx shadcn@latest add button card dialog progress
```

GSAP React hook kullanımı için not: `@gsap/react` paketindeki `useGSAP()` hook'u, `useEffect`/`useLayoutEffect` yerine kullanılmalı — cleanup işlemlerini otomatik yönetiyor (SPA route değişimlerinde animasyon/ScrollTrigger sızıntılarını önler).

---

## Docker / Yerel Geliştirme Ortamı

### docker-compose.yml (MVP — sadece backend + frontend)

```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - pdf_storage:/app/storage
    environment:
      - ENV=development

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  pdf_storage:
```

### backend/Dockerfile

```dockerfile
FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    ghostscript \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### frontend/Dockerfile

```dockerfile
FROM node:22-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
```

---

## Production (ileride, Faz 1+ için not)

- **Hosting önerisi (MVP sonrası):** VPS (Hetzner/DigitalOcean) + Docker Compose, ya da Railway/Render.
- **Frontend (SSR açıksa):** React Router v7 SSR modu Node runtime gerektirir — aynı VPS'te Docker ile veya Vercel/Railway gibi Node destekleyen platformlarda çalışır (Next.js'e özgü Vercel bağımlılığı yok).
- **Dosya depolama:** MVP'de yerel disk yeterli; kullanıcı sayısı arttığında S3-uyumlu (MinIO self-hosted veya Cloudflare R2) depolamaya geçilir.
- **Domain/SSL:** Caddy veya Nginx + Let's Encrypt.

Bu bölüm MVP'de UYGULANMAYACAK, sadece ileride ne yapılacağının notu.
