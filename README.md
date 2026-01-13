# HEIC to Image Converter API - Folder Structure

## 📁 Struktur Folder

```
API-HEIC/                          # Main project folder
├── app/                           # Application files
│   ├── api.py                    # Main FastAPI application
│   ├── utils.py                  # Image conversion utilities
│   ├── database.py               # User & quota tracking
│   ├── requirements.txt          # Python dependencies
│   └── start_api.sh             # Startup script
│
├── data/                          # Data storage (created at runtime)
│   ├── uploads/                 # Temporary uploaded files
│   ├── converted/               # Converted image files
│   │   └── metadata.json       # File tracking info
│   └── api_data.db             # SQLite database
│
├── logs/                          # Log files (created at runtime)
│   └── error.log               # Error log
│
├── docs/                          # Documentation
│   ├── API_USER_GUIDE.md
│   ├── HEROKU_DEPLOYMENT_GUIDE.md
│   ├── MONETIZATION_GUIDE.md
│   ├── DEPLOYMENT_MONETIZATION_GUIDE.md
│   ├── DEPLOYMENT_MONETIZATION_SUMMARY.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── PROJECT_SUMMARY.md
│   └── QUICK_START.txt
│
├── Dockerfile                     # Docker configuration
├── Procfile                       # Heroku configuration
└── .gitignore                     # Git ignore rules
```

---

## 🚀 Cara Menjalankan API

### Option 1: Gunakan Startup Script (Recommended)

```bash
cd /home/sigitdev/Dokumen/API-HEIC
chmod +x app/start_api.sh
./app/start_api.sh
```

### Option 2: Manual dengan Uvicorn

```bash
cd /home/sigitdev/Dokumen/API-HEIC/app

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### Option 3: Docker

```bash
cd /home/sigitdev/Dokumen/API-HEIC

# Build image
docker build -t heic-converter .

# Run container
docker run -p 8000:8000 heic-converter
```

---

## ✅ Paths yang Diupdate (PENTING!)

Semua hardcoded paths sudah diubah ke **dynamic paths** yang work dari mana saja:

### Di `app/utils.py`:
```python
# OLD (hardcoded):
UPLOAD_DIR = Path("/home/sigitdev/uploads")

# NEW (dynamic):
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
```

### Di `app/database.py`:
```python
# OLD (hardcoded):
DB_PATH = Path("/home/sigitdev/api_data.db")

# NEW (dynamic):
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "api_data.db"
```

**Keuntungan:**
✅ Works dari folder mana pun
✅ Works di different servers
✅ Easy to move project around
✅ Easy to deploy to cloud

---

## 📋 Checklist: Semuanya Work?

Setelah pindah folder, verify dengan:

```bash
# 1. Navigate to project
cd /home/sigitdev/Dokumen/API-HEIC

# 2. Install dependencies
pip install -r app/requirements.txt

# 3. Check if imports work
python -c "from app import api; print('✓ Imports OK')"

# 4. Run API
cd app && uvicorn api:app --reload

# 5. Test endpoint
curl http://127.0.0.1:8000/
```

---

## 🔧 Membuat Shortcuts (Optional)

### Linux/Mac: Create symlink

```bash
# Create symlink ke app folder untuk easier access
ln -s /home/sigitdev/Dokumen/API-HEIC /home/sigitdev/heic-api

# Now you can:
cd ~/heic-api/app
./start_api.sh
```

### Windows: Create batch file

Create file `run.bat` di root folder:
```batch
@echo off
cd %~dp0\app
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
pause
```

---

## 📚 Documentation Location

All docs are in `/Dokumen/API-HEIC/docs/`:

- **START HERE:** `DEPLOYMENT_MONETIZATION_SUMMARY.md`
- **Deploy Guide:** `HEROKU_DEPLOYMENT_GUIDE.md`
- **API Docs:** `API_USER_GUIDE.md`
- **Monetization:** `MONETIZATION_GUIDE.md`

---

## 🗑️ Cleanup (Optional)

Jika ingin menghapus file lama dari `/home/sigitdev/`:

```bash
# BACKUP DULU sebelum hapus!
cd /home/sigitdev

# Hapus Python files (duplicate)
rm api.py utils.py database.py

# Hapus config files
rm Dockerfile Procfile .gitignore

# Hapus docs (duplicate)
rm *_GUIDE.md *_SUMMARY.md PROJECT_SUMMARY.md

# Keep:
# - venv/ (virtual environment)
# - uploads/, converted/, logs/ (jika masih digunakan)
```

⚠️ **JANGAN HAPUS:**
- `venv/` (virtual environment)
- Folder `uploads/`, `converted/`, `logs/` (jika masih digunakan old API)

---

## 🔄 Migrasi Data (Jika Ada)

Jika sudah ada data di folder lama:

```bash
# Copy existing files
cp -r /home/sigitdev/uploads/* /home/sigitdev/Dokumen/API-HEIC/data/uploads/
cp -r /home/sigitdev/converted/* /home/sigitdev/Dokumen/API-HEIC/data/converted/
cp /home/sigitdev/api_data.db /home/sigitdev/Dokumen/API-HEIC/data/
```

---

## 📝 Notes

1. **Paths automatically created:**
   - `data/uploads/` (temp files)
   - `data/converted/` (output files)
   - `logs/` (error logs)

2. **No hardcoded paths:**
   - Works dari mana saja
   - Works di different servers
   - Works di Docker

3. **All files preserved:**
   - Original di `/home/sigitdev/` masih ada
   - Dapat dihapus jika sudah confirm berjalan baik

---

## ✅ Verifikasi Successful Migration

```bash
cd /home/sigitdev/Dokumen/API-HEIC
ls -la
# Should show: app/ data/ docs/ logs/ Dockerfile Procfile .gitignore

# Check app folder
ls -la app/
# Should show: api.py utils.py database.py requirements.txt start_api.sh

# Check docs
ls -la docs/
# Should show: multiple .md files

# Test imports
python3 -c "import sys; sys.path.insert(0, 'app'); from api import app; print('✓ All imports working!')"
```

---

**All set!** Your API is now organized in a clean folder structure. 🎉

Next: Read `docs/DEPLOYMENT_MONETIZATION_SUMMARY.md` for deployment!
