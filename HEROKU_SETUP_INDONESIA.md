# Panduan Lengkap Deploy ke Heroku - STEP BY STEP

## Tahap 1: Buat Akun Heroku (5 menit)

### 1. Buka Heroku
- Kunjungi: https://signup.heroku.com/

### 2. Isi Form Pendaftaran
- **Email**: Gunakan email yang sama dengan GitHub (lebih mudah)
- **First name**: Nama depanmu
- **Last name**: Nama belakangmu
- **Company**: Kosongkan atau isi nama proyekmu
- **Primary development language**: Python
- **Agree to terms**: Check/centang

### 3. Verifikasi Email
- Cek email kamu (kemungkinan di spam)
- Klik link verifikasi
- Buat password yang kuat

### 4. Setup Selesai
- Kamu akan diarahkan ke Heroku Dashboard
- Dashboard: https://dashboard.heroku.com/apps

---

## Tahap 2: Sambungkan GitHub ke Heroku (5 menit)

Setelah membuat akun dan verifikasi email, ikuti ini:

### 1. Buka Heroku Dashboard
- https://dashboard.heroku.com/apps

### 2. Buat App Baru
- Klik tombol **"New"** di kanan atas
- Pilih **"Create new app"**

### 3. Isi Detail App
- **App name**: `heic-converter-widya` (atau nama unik lainnya)
  - Nama harus unik di seluruh Heroku (bisa gunakan nama + tanggal)
  - Format: huruf kecil, angka, dan dash saja
- **Choose a region**: Europe (EU) atau United States (US)
  - EU untuk Indo, US untuk coverage lebih luas
- Klik **"Create app"**

### 4. Hubungkan ke GitHub
- Setelah app dibuat, pilih tab **"Deploy"**
- Di bagian **"Deployment method"**, pilih **"GitHub"**
- Klik **"Connect to GitHub"**
- GitHub akan minta izin - klik **"Authorize heroku"**

### 5. Cari Repository
- Setelah authorized, di bawah ada **"Connect to GitHub"**
- Ketik `heic-converter` di search box
- Klik **"Connect"** di repo `widyawanS/heic-converter`

### 6. Setup Auto Deploy
- Scroll ke bawah, di bagian **"Automatic deploys"**
- Pilih branch: `main`
- Centang **"Wait for CI to pass before deploy"** (optional tapi recommended)
- Klik **"Enable Automatic Deploys"**

---

## Tahap 3: Setup Environment Variables (2 menit)

Heroku perlu tahu beberapa konfigurasi:

### 1. Buka Settings Tab
- Di app Heroku kamu, klik tab **"Settings"**

### 2. Reveal Config Vars
- Cari bagian **"Config Vars"**
- Klik tombol **"Reveal Config Vars"**

### 3. Tambah Variabel
Klik **"Add"** dan isi berikut (satu per satu):

| KEY | VALUE | Keterangan |
|-----|-------|-----------|
| `PYTHONUNBUFFERED` | `1` | Supaya Python output real-time |
| `DEBUG` | `False` | Production mode |

Itu saja untuk sekarang! Variabel lainnya optional.

---

## Tahap 4: Deploy Manual (1 menit)

### Opsi A: Auto-Deploy (Recommended)
- Setelah GitHub terhubung, Heroku akan otomatis deploy setiap kali kamu push ke `main`

### Opsi B: Deploy Manual
Jika ingin deploy sekarang juga:
- Di tab **"Deploy"**, scroll ke bawah
- Di bagian **"Manual deploy"**, pilih branch `main`
- Klik **"Deploy Branch"**
- Tunggu build selesai (biasanya 2-3 menit)

---

## Tahap 5: Cek Apakah Live (1 menit)

### 1. Lihat Build Status
- Di bagian "Activity" atau "Deploy", tunggu sampai hijau ✅
- Akan melihat log "Deployed to Heroku"

### 2. Buka App
- Klik tombol **"Open app"** di kanan atas
- Browser akan buka: `https://heic-converter-widya.herokuapp.com/`

### 3. Cek API
- Kamu akan melihat JSON response dengan info API
- Contoh:
  ```json
  {
    "message": "HEIC to JPG/PNG/JPEG Converter API",
    "version": "1.0",
    "endpoints": [...]
  }
  ```

### 4. Cek Swagger Documentation
- Buka: `https://heic-converter-widya.herokuapp.com/docs`
- Kamu bisa test API langsung dari browser!

---

## Troubleshooting - Jika Ada Error

### Error: "App crashed"
1. Buka tab "Activity" atau "Logs"
2. Lihat error message
3. Common issues:
   - Missing environment variable → Tambah di Config Vars
   - Port mismatch → Procfile sudah benar, jangan ubah
   - Import error → Pastikan requirements.txt lengkap

### Error: "Failed to build"
- GitHub Actions atau build process gagal
- Cek di "Activity" → lihat detailed logs
- Biasanya karena missing dependencies

### App runs tapi error saat convert
- Biasanya sudah OK, coba uji dengan file HEIC real
- Atau bisa cek logs: Heroku Dashboard → "View logs"

---

## Testing API Setelah Live

### Coba di Browser
```
https://heic-converter-widya.herokuapp.com/docs
```
- Kamu bisa test endpoint langsung
- Tidak perlu tools lain!

### Atau Pakai curl/Python
```bash
curl -X GET https://heic-converter-widya.herokuapp.com/
```

---

## ✅ Checklist Sebelum Deploy

- [ ] Sudah buat akun Heroku
- [ ] Sudah buat app di Heroku Dashboard
- [ ] Sudah sambungkan GitHub ke Heroku
- [ ] Sudah set Config Vars (PYTHONUNBUFFERED=1, DEBUG=False)
- [ ] Sudah deploy (auto atau manual)
- [ ] Tunggu 2-3 menit untuk build
- [ ] Buka app dan lihat tanda hijau ✅

---

## Informasi Berguna

### Heroku Free Tier
- **Dyno Hours**: 550 free jam/bulan (cukup untuk 1 app)
- **Sleep**: App akan sleep setelah 30 menit tidak ada request
- **Restart**: App restart setiap hari (data di /tmp hilang, tapi database OK)
- **Bandwidth**: 1GB/bulan gratis

### URL App Kamu
- Format: `https://[APP-NAME].herokuapp.com/`
- Contoh: `https://heic-converter-widya.herokuapp.com/`

### Bantuan Lebih Lanjut
- Docs: https://devcenter.heroku.com/
- Status: https://status.heroku.com/

---

## Next Steps Setelah Deploy

1. ✅ Test API
2. ✅ Bagikan URL ke teman
3. Setup Stripe untuk monetization (optional)
4. Buat landing page (optional)
5. Scale ke paid tier kalau ada traffic

---

**Status**: Siap untuk deploy! Ikuti instruksi di atas dan API kamu akan live dalam 5 menit 🚀
