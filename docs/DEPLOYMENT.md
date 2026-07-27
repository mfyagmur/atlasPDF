# DEPLOYMENT.md — Deploy Rehberi

> MVP kapsamındaki AtlasPDF'i (backend + frontend) sıfırdan bir sunucuya kurmak için adım adım rehber. Mimari detaylar için `docs/ARCHITECTURE.md` ve `docs/TECH_STACK.md`'e bakın.

## 1. Genel Bakış

Sistem iki process'ten oluşur, tek bir reverse proxy'nin arkasında çalışır:

- **Backend** — FastAPI + Uvicorn, `:8000` portunda, `/api/*` altında.
- **Frontend** — React Router v7 SSR (Node runtime), `:3000` portunda, geri kalan tüm path'lerde.

Veritabanı yok (stateless, dosya tabanlı MVP); geçici dosyalar `backend/app/storage/{uploads,outputs}` altında tutulur ve TTL sonunda otomatik silinir.

## 2. Hosting Seçenekleri

Aşağıdaki iki seçenekten biri seçilebilir; karar ekibin operasyon konforuna ve bütçesine bağlıdır, ikisi de bu MVP ölçeği için uygundur.

### Seçenek A — VPS + Docker Compose (Hetzner, DigitalOcean, vb.)
- Tam kontrol, ölçekte daha ucuz, manuel işletim sistemi/güvenlik bakımı gerektirir.
- Adımlar:
  1. VPS satın al, Docker + Docker Compose kur.
  2. Repoyu klonla.
  3. `backend/.env.example` dosyasını `backend/.env` olarak kopyala, değerleri doldur.
  4. `docker compose up -d --build`.
  5. `deploy/nginx.conf.example` veya `deploy/Caddyfile.example`'ı kullanarak reverse proxy kur (bkz. §5).
  6. DNS kaydını sunucu IP'sine yönlendir.
  7. SSL sertifikası al (nginx: certbot; Caddy: otomatik).

### Seçenek B — Railway / Render (PaaS)
- Daha az operasyon yükü, servis başına ücretlendirme, daha az yapılandırma kontrolü.
- Adımlar:
  1. İki servis oluştur: biri `backend/Dockerfile`'dan, biri `frontend/`den (Node runtime).
  2. Her platformun panelinden `backend/.env.example`'daki değişkenleri (ve frontend için `VITE_API_URL`) ortam değişkeni olarak gir.
  3. Özel domain/SSL platformun kendi arayüzünden yapılandırılır — ayrı bir nginx/Caddy config'e gerek yoktur.

## 3. Ortam Değişkenleri

`backend/.env.example` dosyasındaki tüm değişkenler:

| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `ENV` | `development` / `production` | `development` |
| `CORS_ORIGINS` | Virgülle ayrılmış izinli frontend origin'leri | `http://localhost:3000` |
| `MAX_TOTAL_UPLOAD_MB` | Toplam yükleme boyutu limiti (MB) | `50` |
| `FILE_TTL_MINUTES` | Geçici dosyaların ömrü (dakika) | `60` |
| `CLEANUP_INTERVAL_MINUTES` | Temizlik job'ının çalışma aralığı (dakika) | `10` |
| `RATE_LIMIT_PER_MINUTE` | IP+endpoint başına dakikalık istek limiti | `10` |
| `LOG_LEVEL` | Log seviyesi | `INFO` |
| `LOG_JSON` | Loglar JSON formatında mı basılsın | `true` |

Frontend tarafında: `VITE_API_URL` (backend'in erişilebilir olduğu URL, örn. `https://api.your-domain.com` veya aynı domain kullanılıyorsa `https://your-domain.com`).

## 4. Docker Compose ile Çalıştırma

```bash
docker compose build
docker compose up -d
docker compose logs -f backend
```

`docker-compose.yml`, `backend` servisi için `env_file: ./backend/.env` kullanır — böylece yerel geliştirme ve Compose aynı `.env` dosyasını paylaşır, değerler iki yerde tekrar edilmez.

## 5. Reverse Proxy Kurulumu (sadece VPS yolunda)

`deploy/nginx.conf.example` veya `deploy/Caddyfile.example`'ı kopyalayıp domain'inizle güncelleyin. İkisi de:
- `/api/*` → backend `:8000`
- geri kalan her şey → frontend `:3000`
- gzip ve `MAX_TOTAL_UPLOAD_MB` ile uyumlu body-size limiti içerir.

**Önemli not (rate limiting + proxy):** Backend'deki IP bazlı rate limiting (`slowapi`, `get_remote_address`) `request.client.host`'u okur ve `X-Forwarded-For`'a güvenmez (spoofing riski nedeniyle). Bu, reverse proxy arkasında farklı gerçek istemcilerin proxy IP'si üzerinden rate limit'i paylaşabileceği anlamına gelir — bilinen bir MVP sınırlamasıdır. Trusted-proxy allowlist'i ile düzeltmek Faz 1+ kapsamındadır, bu task'ta bilinçli olarak yapılmamıştır.

## 6. Deploy Sonrası Smoke Test

Bkz. `docs/SMOKE_TEST.md` — her deploy sonrası manuel olarak kontrol edilmesi gereken maddeler listesi.

## 7. Rollback / Güncelleme

Veritabanı/migration yok (stateless, dosya tabanlı MVP), bu yüzden rollback basitçe önceki commit/image'a dönüp yeniden build etmektir:

```bash
git pull
docker compose up -d --build
```

Geriye dönmek gerekirse aynı şekilde önceki commit'e `git checkout` yapıp tekrar `docker compose up -d --build` çalıştırın.
