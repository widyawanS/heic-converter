# Panduan Deploy ke Render - Step by Step (Bahasa Indonesia)

Render adalah platform deploy yang free dan mudah! Mari kita deploy API HEIC Converter kamu sekarang.

---

## ✅ Pre-requisites

Pastikan kamu sudah punya:
- ✅ GitHub account (sudah ada)
- ✅ Repository di GitHub (sudah ada: `widyawanS/heic-converter`)
- ✅ Tidak perlu kartu kredit untuk Render

---

## 🚀 TAHAP 1: Signup Render (2 menit)

### Langkah 1: Buka Render
- Kunjungi: https://render.com/

### Langkah 2: Klik "Get Started" atau "Sign up"

### Langkah 3: Pilih "Continue with GitHub"
- Render akan redirect ke GitHub authorization
- Klik **"Authorize render-oss"**

### Langkah 4: Verifikasi & Setup Selesai
- Render akan membuat akun kamu
- Redirect ke Dashboard
- Dashboard: https://dashboard.render.com/

**Selesai tahap 1!** ✅

---

## 🔗 TAHAP 2: Deploy Project dari GitHub (5 menit)

### Langkah 1: Buka Render Dashboard
- URL: https://dashboard.render.com/

### Langkah 2: Klik "New +"
- Dropdown di kiri atas
- Pilih **"Web Service"**

### Langkah 3: Pilih Repository
- Di bagian **"Connect a repository"**, kamu akan lihat list GitHub repos
- Cari & klik **`heic-converter`** (atau `widyawanS/heic-converter`)
- Jika tidak terlihat, klik **"Configure account"** lalu authorize full access

### Langkah 4: Setup Web Service Details

#### Name
- **Field**: Name
- **Value**: `heic-converter` (atau nama unik lainnya)

#### Environment
- **Field**: Environment
- **Value**: `Docker` (Render auto-detect dari Dockerfile)

#### Branch
- **Field**: Branch
- **Value**: `main`

#### Root Directory (optional)
- **Field**: Root Directory
- **Value**: `.` (kosongkan, sudah default)

#### Render YAML Path (optional)
- Kosongkan

### Langkah 5: Konfigurasi Instance
Scroll ke bawah:

#### Instance Type
- **Recommended**: Free
- **Alternative**: Starter ($7/month untuk performa lebih)

### Langkah 6: Environment Variables
Di bagian **"Environment"**, klik **"Add Environment Variable"**

Tambahkan:
| Key | Value |
|-----|-------|
| `PYTHONUNBUFFERED` | `1` |
| `DEBUG` | `False` |

(Klik **"Add"** untuk setiap variable)

### Langkah 7: Deploy!
- Klik tombol **"Create Web Service"** di bawah
- Render akan mulai build dan deploy
- Tunggu ~2-3 menit sampai selesai

**Status**: Akan melihat "Building" → "Live"

---

## ⏳ TAHAP 3: Tunggu Build Selesai (2-3 menit)

Di Render dashboard, kamu akan melihat:

### Status Build
- **Building** (sedang diproses)
- **Live** (selesai, API running) ✅

### Logs
- Klik tab **"Logs"** untuk lihat progress
- Jika ada error, error message ada di sini

### Cek Progress
Tunggu sampai lihat:
```
=== Deploying to Render ===
[OK] Web Service deployed
URL: https://heic-converter-xxxxx.onrender.com/
```

---

## 🌐 TAHAP 4: Akses API (instant setelah live)

### Dapatkan URL
Di Render dashboard, copy public URL (format: `https://heic-converter-xxxxx.onrender.com/`)

### Test di Browser
Akses: `https://heic-converter-xxxxx.onrender.com/`

Kamu akan lihat JSON response:
```json
{
  "message": "HEIC to JPG/PNG/JPEG Converter API",
  "version": "1.0",
  "endpoints": [...]
}
```

### Coba Swagger UI
Akses: `https://heic-converter-xxxxx.onrender.com/docs`

Di sini kamu bisa:
- ✅ Test semua endpoint
- ✅ Upload file HEIC
- ✅ Download hasil konversi
- ✅ Baca dokumentasi otomatis

### Health Check
```
https://heic-converter-xxxxx.onrender.com/health
```

Response:
```json
{
  "status": "ok",
  "disk_space_gb": 0.5,
  "message": "API is running"
}
```

---

## ✅ Checklist Deploy Render

```
DEPLOYMENT CHECKLIST:
☐ Buat akun Render (https://render.com/)
☐ Authorize GitHub
☐ Buka Dashboard
☐ Klik "New +" → "Web Service"
☐ Select repository: heic-converter
☐ Name: heic-converter
☐ Environment: Docker (auto-detect)
☐ Branch: main
☐ Instance Type: Free
☐ Environment Variables:
   ☐ PYTHONUNBUFFERED = 1
   ☐ DEBUG = False
☐ Klik "Create Web Service"
☐ Tunggu build selesai (2-3 menit)
☐ Status berubah jadi "Live"
☐ Test di https://heic-converter-xxxxx.onrender.com/
☐ Coba Swagger UI di /docs
☐ Success! 🎉
```

---

## 🔄 Auto-Deploy dari GitHub (Otomatis!)

Setelah deploy pertama, Render akan auto-deploy setiap kali kamu:
1. Push code ke `main` branch di GitHub
2. Merge Pull Request ke `main`

**Cara kerja**:
- Kamu push ke GitHub
- GitHub notify Render
- Render auto-build & deploy
- Tidak perlu manual lagi!

---

## 🐛 Troubleshooting

### Error: "Build Failed"
1. Buka tab **"Logs"**
2. Lihat error message
3. Common issues:
   - Missing dependencies → check `app/requirements.txt`
   - Port mismatch → check `Procfile` atau Dockerfile
   - Python syntax error → check code

### Error: "Deployment failed"
- Biasanya karena build stage error
- Lihat logs untuk detail
- Fix code di GitHub
- Auto-redeploy akan trigger

### App "Spinning up"
- Render free tier spin-down setelah idle
- First request akan lambat (~5-10 detik)
- Request berikutnya cepat normal
- Ini normal untuk free tier

### Database/File issue
- SQLite file bisa hilang saat redeploy
- Untuk production, gunakan PostgreSQL (Render bisa link)
- Untuk testing, OK-OK saja

---

## 📊 Render Free Tier Details

### Apa yang Included:
- ✅ Deploy service gratis
- ✅ 750 jam/bulan compute
- ✅ Auto-redeploy dari GitHub
- ✅ Environment variables
- ✅ Custom domain (nantinya bisa)
- ✅ HTTPS automatic

### Limitations:
- ⏸️ Spin down setelah 15 menit idle (biasa untuk free tier)
- 📦 Limited RAM & CPU
- 📁 Limited storage
- Tidak ada database gratis (tapi bisa add PostgreSQL berbayar)

### Kalau upgrade (paid):
- **Starter**: $7/month
  - Dedicated instance
  - No spin-down
  - Better performance
  - Recommended untuk production

---

## 🔐 PENTING: Secure Practices

### Do's ✅
- Environment variables di Render (bukan di code)
- Sensitive data di config vars (API keys, etc)
- Regular backups (jika data penting)

### Don'ts ❌
- Jangan commit `.env` ke GitHub
- Jangan simpan API keys di code
- Jangan expose database credentials

Kamu sudah OK! Code kamu aman.

---

## 📈 Next Steps

### Setelah Deploy Berhasil:

#### 1. Test API
- Coba convert HEIC file
- Test semua endpoints
- Pastikan semuanya work

#### 2. Share URL
- Bagikan ke teman
- Test dari mobile
- Minta feedback

#### 3. Monitor
- Cek logs jika ada error
- Monitor performance
- Scale kalau ada traffic

#### 4. Improvement (optional)
- Add landing page
- Setup Stripe (monetization)
- Add more features
- Upgrade instance kalau perlu

---

## 🚀 Auto-Deploy Workflow Explanation

Setiap kali kamu update code:

```
┌─────────────────┐
│  Edit code      │
│  di local       │
└────────┬────────┘
         │ git push origin main
         ↓
┌─────────────────┐
│  GitHub         │ 
│  (receives push)│
└────────┬────────┘
         │ webhook notification
         ↓
┌─────────────────┐
│  Render         │
│  (detects push) │
└────────┬────────┘
         │ trigger build
         ↓
┌─────────────────┐
│  Build process  │ (install deps, build)
│  (2-3 menit)    │
└────────┬────────┘
         │ build success
         ↓
┌─────────────────┐
│  Deploy         │
│  (replace old)  │
└────────┬────────┘
         │ done!
         ↓
┌─────────────────┐
│  Live! 🎉       │
│  New version up │
└─────────────────┘
```

---

## 📞 Support & Resources

### Render Documentation
- Docs: https://render.com/docs
- Guides: https://render.com/docs/deploy-web-services
- GitHub integration: https://render.com/docs/github

### Our Project Documentation
- API Testing: `/API_TESTING_GUIDE.md`
- Endpoints Info: `/docs/API_USER_GUIDE.md`
- Swagger UI: `https://[your-url]/docs`

### Troubleshooting
- Check Logs: Render Dashboard → Logs tab
- Check Status: https://render.com/status
- Community: Render Discord (link di website)

---

## 🎯 Success Indicators

Kamu berhasil deploy jika:

✅ Render dashboard status: **Live**  
✅ Bisa akses: `https://heic-converter-xxxxx.onrender.com/`  
✅ JSON response di `/` endpoint  
✅ Swagger UI loading: `/docs`  
✅ Health check OK: `/health`  
✅ Bisa convert file (test di Swagger UI)  

---

## 💡 Pro Tips

### 1. Custom Domain (Optional)
Render allows custom domain untuk paid tier. Untuk free:
- URL akan seperti: `heic-converter-xxxxx.onrender.com`
- Cukup untuk testing

### 2. Environment Variables
Render meng-encrypt environment variables. Aman! ✅

### 3. Monitoring
Di Render dashboard, kamu bisa:
- See logs real-time
- Monitor memory usage
- See deploy history
- Rollback jika perlu

### 4. GitHub Integration
Render detect Dockerfile automatically:
- Jika ada `Dockerfile` → pakai Docker
- Jika ada `requirements.txt` → auto-detect Python
- Auto-select buildpack yang tepat

---

## 🔄 Update Code Workflow

Setelah deploy awal, workflow update code:

```bash
# 1. Edit code di local
vim app/api.py

# 2. Test locally (optional)
./start_api.sh

# 3. Commit & push ke GitHub
git add .
git commit -m "Fix atau feature baru"
git push origin main

# 4. Render auto-deploy!
# (Tunggu 2-3 menit)

# 5. Verify di live URL
# https://heic-converter-xxxxx.onrender.com/
```

**Itu saja!** Render handle selebihnya.

---

## ❓ FAQ

### Q: Apakah API akan sleep?
A: Akan spin-down setelah 15 menit idle (free tier). Akses pertama lambat, tapi tidak permanent sleep.

### Q: Bagaimana dengan data/database?
A: SQLite file bisa hilang saat redeploy. Untuk production, gunakan PostgreSQL.

### Q: Bisa pakai custom domain?
A: Ya, tapi untuk paid tier. Free tier pakai `*.onrender.com` subdomain.

### Q: Berapa lama build?
A: Biasanya 2-3 menit untuk project kamu.

### Q: Bisa rollback versi lama?
A: Ya, di Render dashboard → Deployments → select previous version.

### Q: Perlu CLI tools?
A: Tidak! Semua via web dashboard.

---

## 🎉 Selesai!

Setelah selesai deploy, API kamu LIVE dan accessible dari mana saja!

**Langkah selanjutnya**:
1. Test API secara menyeluruh
2. Bagikan URL ke teman
3. Implementasikan features baru
4. Setup monetization (optional)

---

**Status**: Ready to Deploy to Render!  
**Time Estimate**: 10 menit total (5 menit setup + 3 menit build + 2 menit testing)  
**Difficulty**: Very Easy  

Ikuti checklist di atas dan API kamu akan live! 🚀

---

## 📍 Render vs Heroku (Old) Comparison

| Aspect | Heroku (Old Free) | Render (Free) |
|--------|------------------|---------------|
| Cost | $0 | $0 |
| Setup Time | ~5 min | ~5 min |
| Build Time | ~2 min | ~2 min |
| Cold Start | < 1s | 5-10s (idle) |
| GitHub Integration | ✅ | ✅ |
| Environment Vars | ✅ | ✅ |
| Database | Heroku Postgres | PostgreSQL (paid) |
| Uptime SLA | 99.9% | 99.9% |
| Current Status | ❌ NO FREE | ✅ GRATIS |

**Render adalah replacement terbaik untuk Heroku free tier!**

