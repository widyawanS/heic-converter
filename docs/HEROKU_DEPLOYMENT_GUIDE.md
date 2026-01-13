# Step-by-Step Guide: Deploy ke Heroku

## Untuk Pemula - Mudah & Gratis!

Heroku adalah platform yang membuat deploy aplikasi Python SANGAT MUDAH. Tidak perlu setup server kompleks.

---

## 🔧 Prerequisites (Persiapan)

### 1. Install Git (Jika Belum)

**Linux:**
```bash
sudo apt-get install git
```

**Mac:**
```bash
brew install git
```

**Windows:**
Download dari https://git-scm.com/download/win

### 2. Buat Akun GitHub (Gratis)

- Buka https://github.com
- Klik "Sign up"
- Isi email, password, username
- Done!

### 3. Buat Akun Heroku (Gratis)

- Buka https://www.heroku.com
- Klik "Sign up"
- Isi email, password
- Verify via email

---

## 📝 Step 1: Setup Local Git Repository

Di `/home/sigitdev/`, jalankan:

```bash
# Initialize git repository
git init

# Set user name (bisa nama Anda)
git config user.name "Your Name"
git config user.email "your@email.com"

# Stage semua files
git add .

# Create commit pertama
git commit -m "Initial commit - HEIC Converter API"
```

---

## 🐙 Step 2: Push ke GitHub

### 2.1 Buat repository di GitHub

1. Buka https://github.com/new
2. Repository name: `heic-converter`
3. Deskripsi: `HEIC to JPG/PNG/JPEG Converter API`
4. Pilih "Public" (jadi gratis dan everyone bisa lihat)
5. Klik "Create repository"

### 2.2 Push ke GitHub

Setelah membuat repository, GitHub akan berikan instruksi. Jalankan di terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/heic-converter.git
git branch -M main
git push -u origin main
```

Gantikan `YOUR_USERNAME` dengan username GitHub Anda.

**Hasilnya:**
- Repository Anda ada di: `https://github.com/YOUR_USERNAME/heic-converter`
- Semua file ada di GitHub

---

## 🚀 Step 3: Deploy ke Heroku

### 3.1 Install Heroku CLI

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows:**
Download dari https://cli-assets.heroku.com/branches/stable/windows/x64/heroku-x64.exe

### 3.2 Login ke Heroku

```bash
heroku login
```

Browser akan terbuka. Login dengan email dan password Heroku.

### 3.3 Buat App di Heroku

```bash
# Gantikan 'nama-app-anda' dengan nama unik
# Harus lowercase, no spaces, no special characters
# Contoh: heic-converter-123, my-heic-api, etc
heroku create nama-app-anda
```

**Output:**
```
Creating ⬢ nama-app-anda... done
https://nama-app-anda.herokuapp.com/ | https://git.heroku.com/nama-app-anda.git
```

Simpan URL itu! Itu adalah API Anda yang live di internet! 🎉

### 3.4 Deploy!

```bash
git push heroku main
```

Heroku akan:
1. Download code dari GitHub
2. Install Python 3.11
3. Install dependencies dari `requirements.txt`
4. Run server dengan Procfile

### 3.5 Lihat Logs

```bash
# Real-time logs
heroku logs --tail

# Atau logs dari dashboard
heroku dashboard
```

---

## ✅ Verifikasi Deployment

### 1. Test API

Buka di browser:
```
https://nama-app-anda.herokuapp.com/
```

Anda seharusnya lihat:
```json
{
  "name": "HEIC to Image Converter API",
  "version": "1.0.0",
  ...
}
```

### 2. Test Health Check

```
https://nama-app-anda.herokuapp.com/health
```

### 3. Test Docs

```
https://nama-app-anda.herokuapp.com/docs
```

Anda seharusnya lihat Swagger UI dengan semua endpoints!

---

## 🔧 Troubleshooting

### Masalah: Application error

**Solution:**
```bash
heroku logs --tail
```

Lihat error message dan cari di Google.

### Masalah: Port tidak match

Pastikan `Procfile` adalah:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

**Jangan hardcode port!** Heroku memberikan port via `$PORT` variable.

### Masalah: requirements.txt tidak ditemukan

Pastikan file ada di root directory:
```bash
ls requirements.txt
```

### Masalah: Python version mismatch

Heroku default ke Python 3.12. Untuk specify Python 3.11:

Buat file `runtime.txt` di root dengan isi:
```
python-3.11.0
```

---

## 📊 Free Tier Limits

Heroku free tier (sampai 28 Nov 2022, sekarang hanya trial):

**Alternatif Gratis:**
- **Railway.app** - Lebih mudah, $5/bulan gratis
- **Render.com** - Gratis untuk simple apps
- **Fly.io** - Gratis tier bagus

---

## 🔄 Update API (Setelah Deploy)

Setiap kali Anda update kode:

```bash
# 1. Edit file
# ... modify api.py, utils.py, etc ...

# 2. Commit ke GitHub
git add .
git commit -m "Update API features"

# 3. Push ke Heroku
git push heroku main

# 4. Check logs
heroku logs --tail
```

---

## 💡 Pro Tips

### Tip 1: Scale Up (Jika Traffic Tinggi)

```bash
# Bayar untuk 2 dyno (worker)
heroku ps:scale web=2

# Atau dari dashboard
heroku dashboard -> Resources -> Change dyno type
```

### Tip 2: Custom Domain

```bash
# Add custom domain (nama domain harus Anda punya)
heroku domains:add api.yourdomain.com
```

### Tip 3: Environment Variables

```bash
# Set variable (untuk API keys, etc)
heroku config:set STRIPE_KEY=sk_test_xxxxx

# Get variable
heroku config:get STRIPE_KEY

# Lihat semua
heroku config
```

### Tip 4: Database (PostgreSQL)

```bash
# Add PostgreSQL database (free tier available)
heroku addons:create heroku-postgresql:hobby-dev
```

---

## 📈 Monitoring

### Via Dashboard

1. Buka https://dashboard.heroku.com
2. Pilih app Anda
3. Lihat:
   - Resources (active dyno)
   - Metrics (response time, throughput)
   - Logs (error tracking)

### Via CLI

```bash
# Metrics
heroku metrics

# Ps info
heroku ps
```

---

## 🎓 Next Steps

### Setelah Deploy:
1. ✅ Test API endpoints
2. ✅ Share URL dengan teman/klien
3. ✅ Monitor logs untuk errors
4. ✅ Add database untuk user management
5. ✅ Integrasi Stripe untuk payment
6. ✅ Setup custom domain

---

## 📞 Bantuan

Jika ada error:

1. **Check logs:**
   ```bash
   heroku logs --tail
   ```

2. **Google error message** - Kebanyakan error sudah ada solusinya di Stack Overflow

3. **Heroku Documentation:** https://devcenter.heroku.com/

4. **Ask in communities:**
   - r/learnprogramming
   - Stack Overflow
   - Discord communities

---

## 🎉 Selesai!

API Anda sekarang **LIVE DI INTERNET** dan bisa diakses dari mana saja!

URL: `https://nama-app-anda.herokuapp.com`

Dari sini, Anda bisa:
- Share dengan orang lain
- Build website/app yang consume API
- Add monetization
- Scale ke jutaan users

Selamat! 🚀

---

**Pertanyaan?**
- Buka DEPLOYMENT_MONETIZATION_GUIDE.md untuk info monetization
- Atau tanya di comments!
