# Render Configure Page - Field by Field Guide

Ketika kamu di Render create Web Service, akan ada beberapa field. Mari kita lihat satu-satu apa yang harus diisi.

---

## 📍 FIELD-BY-FIELD GUIDE

### Field 1: NAME
**Label**: "Name"  
**Tipe**: Text input  
**Isi dengan**: `heic-converter`  
**Catatan**: 
- Gunakan nama sederhana
- Hanya huruf kecil, angka, dash
- Ini akan jadi bagian dari URL
- Contoh URL hasil: `heic-converter-xxxxx.onrender.com`

**Contoh**:
```
heic-converter ✅
heic-converter-widya ✅
heic_converter ✅
heic converter ❌ (spasi tidak boleh)
HEIC-Converter ❌ (huruf besar tidak boleh)
```

---

### Field 2: ENVIRONMENT (atau Runtime)
**Label**: "Environment" atau "Runtime"  
**Tipe**: Dropdown/Select  
**Pilih**: `Docker`  
**Catatan**:
- Penting! Render harus detect dari Dockerfile
- Ada 3 opsi biasanya: Node, Python, Docker
- Kita pakai Docker karena ada Dockerfile di repo
- Render akan otomatis build dari Dockerfile

**Opsi yang mungkin ada**:
- Node.js
- Python
- Docker ← **PILIH INI**
- Ruby
- dll

---

### Field 3: REPOSITORY (atau "Connect Repository")
**Label**: Berbeda tergantung step, bisa jadi section sendiri  
**Tipe**: Select/Dropdown dari list GitHub repos  
**Pilih**: `widyawanS/heic-converter` atau `heic-converter`  
**Catatan**:
- Ini list repo GitHub kamu
- Cari yang namanya `heic-converter`
- Klik untuk select
- Jika tidak ada, mungkin belum authorize GitHub penuh

---

### Field 4: BRANCH
**Label**: "Branch"  
**Tipe**: Dropdown  
**Pilih**: `main`  
**Catatan**:
- Ini cabang git yang akan di-deploy
- Kita pakai `main` branch
- Jangan pakai `master` (kecuali kamu ada branch `master`)
- Check di GitHub: cabang default apa? Pakai itu

**Opsi yang mungkin**:
- main ← **PILIH INI**
- master
- develop
- dll

---

### Field 5: ROOT DIRECTORY (Optional)
**Label**: "Root Directory" atau "Build command"  
**Tipe**: Text input (optional)  
**Isi dengan**: Kosongkan (biarkan default)  
**Catatan**:
- Jarang diisi untuk project kita
- Render akan cari Dockerfile di root
- Biarkan kosong

---

### Field 6: INSTANCE TYPE (atau Plan)
**Label**: "Instance Type" atau "Plan"  
**Tipe**: Radio button atau dropdown  
**Pilih**: `Free`  
**Catatan**:
- Ada beberapa opsi plan
- Free: gratis, tapi ada limitation
- Starter: $7/month, recommended untuk production
- Professional: $25+/month

**Opsi yang mungkin**:
- Free ← **PILIH INI** (untuk testing)
- Starter ($7/month)
- Professional ($25+/month)

---

### Field 7: ENVIRONMENT VARIABLES (atau Config)
**Label**: "Environment Variables" atau "Env"  
**Tipe**: Key-Value input (bisa ada banyak)  
**Isi dengan**: Ada 2 variable

#### Variable 1:
**Key**: `PYTHONUNBUFFERED`  
**Value**: `1`

#### Variable 2:
**Key**: `DEBUG`  
**Value**: `False`

**Cara mengisi**:
1. Cari tombol "Add Environment Variable" atau "Add"
2. Klik tombol itu
3. Muncul dua field: KEY dan VALUE
4. Isi KEY dengan nama variable (contoh: PYTHONUNBUFFERED)
5. Isi VALUE dengan nilai (contoh: 1)
6. Klik Add atau Save
7. Ulangi untuk variable kedua

**Contoh apa yang harus terlihat**:
```
Key              Value
PYTHONUNBUFFERED 1
DEBUG            False
```

**Penjelasan**:
- `PYTHONUNBUFFERED=1` → Output Python real-time (tidak di-buffer)
- `DEBUG=False` → Production mode (tidak development mode)

---

## 🔍 VISUAL REFERENCE

Kalau kamu bingung, Render page biasanya terlihat seperti ini:

```
┌─────────────────────────────────────────┐
│ Create a new Web Service                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Connect a repository                    │
├─────────────────────────────────────────┤
│ [Select your GitHub repo]               │
│ └─ widyawanS/heic-converter ✓          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Web Service Settings                    │
├─────────────────────────────────────────┤
│ Name:          [heic-converter________] │
│ Environment:   [Docker______________▼] │
│ Branch:        [main______________▼]   │
│ Root Directory: [________________]      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Instance Type                           │
├─────────────────────────────────────────┤
│ ◉ Free                                  │
│ ○ Starter ($7/month)                    │
│ ○ Professional ($25/month)              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Environment Variables                   │
├─────────────────────────────────────────┤
│ PYTHONUNBUFFERED | 1              [×]   │
│ DEBUG            | False           [×]   │
│                                          │
│ [+ Add Environment Variable]             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ [Create Web Service] button              │
└─────────────────────────────────────────┘
```

---

## ✅ CHECKLIST SEBELUM CREATE

Sebelum klik "Create Web Service", pastikan:

```
Checklist:
☐ Name: heic-converter
☐ Environment: Docker
☐ Repository: widyawanS/heic-converter selected
☐ Branch: main
☐ Root Directory: kosong (atau default)
☐ Instance Type: Free
☐ Environment Variables:
   ☐ PYTHONUNBUFFERED = 1
   ☐ DEBUG = False
```

Kalau semuanya ✓, baru klik "Create Web Service"!

---

## 🎯 FIELD PRIORITY

**PENTING** (HARUS diisi benar):
1. Name: heic-converter
2. Environment: Docker
3. Repository: heic-converter
4. Branch: main
5. Instance: Free
6. Env Variables: 2 variables

**OPTIONAL** (Biarkan default):
- Root Directory
- Build command
- yang lainnya

---

## 🆘 TROUBLESHOOTING CONFIGURE PAGE

### "Tidak bisa select repository"
**Solusi**:
1. Klik "Configure account"
2. Authorize render ke GitHub penuh
3. Kembali ke page ini
4. Refresh page
5. Coba lagi

### "Repository tidak ada di list"
**Solusi**:
1. Repository harus public
2. Cek di GitHub: https://github.com/widyawanS/heic-converter
3. Pastikan public (not private)
4. Refresh Render page
5. Coba lagi

### "Branch tidak ada"
**Solusi**:
1. Kamu push ke branch `main`? Cek
2. Di GitHub, lihat branch apa yang ada
3. Pakai branch yang sudah ada
4. Biasanya `main` atau `master`

### "Bingung mana yang harus diisi"
**Solusi**:
1. Lihat section "FIELD-BY-FIELD GUIDE" di atas
2. Field yang highlight penting, field lain optional
3. Ikuti checklist
4. Tanya saya! 😊

---

## 📝 NOTES TAMBAHAN

### Nama (Name)
- Nama ini untuk Render tracking
- Juga menjadi bagian dari public URL
- Kamu bisa ganti nanti (di settings)
- Jadi tidak perlu perfeksionis

### Environment
- PENTING untuk dipilih dengan benar
- Docker = build pakai Dockerfile
- Python = auto-detect Python project
- Kita punya Dockerfile, jadi pilih Docker

### Branch
- Biasanya `main` untuk project baru
- Check di GitHub kalau ragu
- Cek link: https://github.com/widyawanS/heic-converter

### Instance Type
- Free: Spins down after 15 min idle (normal)
- Starter: Always running ($7/month)
- Untuk testing: Free sudah cukup
- Upgrade nanti kalau perlu

### Environment Variables
- Tidak ada default, harus kita isi manual
- 2 variable saja sudah cukup untuk start
- Bisa add lebih banyak nanti kalau perlu

---

## 💡 TIPS

1. **Jangan overthink** - Cukup ikuti guide ini
2. **Bisa edit nanti** - Kamu bisa ganti settings setelah deploy
3. **Free tier OK** - Cukup untuk testing dan MVP
4. **Render helpful** - Kalau ada error, error message jelas

---

## 🚀 SETELAH SELESAI CONFIGURE

Setelah semua field terisi:
1. Double check checklist di atas
2. Klik tombol "Create Web Service"
3. Tunggu build selesai (~3 menit)
4. Status akan berubah jadi "Live"
5. Klik public URL untuk test

---

**Sudah jelas?** Sekarang coba isi field-field sesuai guide di atas!

Kalau masih bingung, screenshot page kamu dan saya lihat mana field yang confusing.
