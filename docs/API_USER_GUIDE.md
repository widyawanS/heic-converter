# HEIC to Image Converter API - User Guide

## 📋 Overview

API FastAPI untuk konversi gambar HEIC menjadi format JPG/PNG/JPEG dengan fitur:
- ✅ Konversi HEIC ke JPG/PNG/JPEG
- ✅ Kontrol kualitas kompresi (0-100)
- ✅ Resize gambar (optional)
- ✅ Download langsung atau akses via URL
- ✅ Auto-cleanup file setelah 24 jam
- ✅ Error handling detail dengan JSON responses
- ✅ Comprehensive validation dan security checks

---

## 🚀 Quick Start

### 1. Instalasi & Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Menjalankan Server

```bash
# Development mode (dengan auto-reload)
uvicorn api:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 3. Akses API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### 1. **POST /convert** - Konversi HEIC File

Endpoint utama untuk mengkonversi file HEIC ke format lain.

#### Request
```bash
curl -X POST http://127.0.0.1:8000/convert \
  -F "file=@gambar.heic" \
  -F "format=jpg" \
  -F "quality=85" \
  -F "width=800" \
  -F "height=600" \
  -F "return_file=false"
```

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `file` | File | - | ✅ | File HEIC yang akan dikonversi |
| `format` | string | - | ✅ | Format output: `jpg`, `png`, atau `jpeg` |
| `quality` | integer | 85 | ❌ | Quality level 0-100 (jpg/jpeg saja) |
| `width` | integer | - | ❌ | Target width dalam pixel (auto-scale height) |
| `height` | integer | - | ❌ | Target height dalam pixel (auto-scale width) |
| `return_file` | boolean | false | ❌ | Return file langsung (true) atau JSON URL (false) |

#### Response (Success) - return_file=false

```json
{
  "status": "success",
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "gambar.jpg",
  "size": 45678,
  "url": "/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "format": "jpg",
  "quality": 85,
  "expires_at": "2026-01-14T12:30:00"
}
```

#### Response (Success) - return_file=true
Returns file binary dengan header:
```
Content-Type: image/jpeg
Content-Disposition: attachment; filename="gambar.jpg"
```

#### Response (Error)

```json
{
  "detail": {
    "status": "error",
    "code": "INVALID_FORMAT",
    "message": "Format harus salah satu dari: jpeg, png, jpg"
  }
}
```

#### Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `INVALID_FILENAME` | 400 | Filename kosong atau tidak valid |
| `INVALID_FORMAT` | 400 | Format bukan jpg/png/jpeg |
| `INVALID_QUALITY` | 400 | Quality bukan integer 0-100 |
| `INVALID_DIMENSIONS` | 400 | Width/height tidak valid |
| `EMPTY_FILE` | 400 | File kosong |
| `INVALID_HEIC` | 400 | File bukan HEIC yang valid |
| `CONVERSION_FAILED` | 500 | Konversi gagal (detail di message) |
| `INTERNAL_SERVER_ERROR` | 500 | Error tidak terduga |

---

### 2. **GET /download/{file_id}** - Download File Terkonversi

Download file yang sudah dikonversi sebelumnya.

#### Request
```bash
curl -O http://127.0.0.1:8000/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

#### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `file_id` | string | ID yang diterima dari `/convert` endpoint |

#### Response (Success)
File binary dengan header:
```
Content-Type: image/jpeg (or png)
Content-Disposition: attachment; filename="gambar.jpg"
```

#### Response (Error)

```json
{
  "detail": {
    "status": "error",
    "code": "FILE_NOT_FOUND",
    "message": "File dengan ID xxx tidak ditemukan atau sudah expired"
  }
}
```

---

### 3. **DELETE /delete/{file_id}** - Hapus File

Hapus file yang sudah dikonversi sebelumnya.

#### Request
```bash
curl -X DELETE http://127.0.0.1:8000/delete/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

#### Response (Success)
```json
{
  "status": "success",
  "message": "File a1b2c3d4-e5f6-7890-abcd-ef1234567890 berhasil dihapus",
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### Response (Error)
```json
{
  "detail": {
    "status": "error",
    "code": "FILE_NOT_FOUND",
    "message": "File dengan ID xxx tidak ditemukan"
  }
}
```

---

### 4. **GET /health** - Health Check

Cek status API dan disk space.

#### Request
```bash
curl http://127.0.0.1:8000/health
```

#### Response
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "scheduler_running": true,
  "disk": {
    "total_gb": 117.23,
    "used_gb": 11.86,
    "free_gb": 104.58,
    "percent_used": 10.12
  }
}
```

---

### 5. **GET /** - API Info

Info dasar tentang API.

#### Request
```bash
curl http://127.0.0.1:8000/
```

#### Response
```json
{
  "name": "HEIC to Image Converter API",
  "version": "1.0.0",
  "description": "API untuk konversi gambar HEIC menjadi JPG/PNG/JPEG",
  "endpoints": {
    "POST /convert": "Konversi file HEIC ke format lain",
    "GET /download/{file_id}": "Download file yang sudah dikonversi",
    "DELETE /delete/{file_id}": "Hapus file yang sudah dikonversi",
    "GET /health": "Check status API",
    "GET /docs": "Interactive API documentation (Swagger UI)"
  }
}
```

---

## 💡 Use Cases & Examples

### Example 1: Konversi HEIC ke JPG dengan Quality Control

```bash
curl -X POST http://127.0.0.1:8000/convert \
  -F "file=@photo.heic" \
  -F "format=jpg" \
  -F "quality=90"

# Response:
# {
#   "status": "success",
#   "file_id": "abc123...",
#   "filename": "photo.jpg",
#   "url": "/download/abc123...",
#   "expires_at": "2026-01-14T12:30:00"
# }

# Download file
curl -O http://127.0.0.1:8000/download/abc123...
```

### Example 2: Resize Gambar

```bash
# Resize ke lebar 800px (height auto)
curl -X POST http://127.0.0.1:8000/convert \
  -F "file=@photo.heic" \
  -F "format=png" \
  -F "width=800"

# Atau resize ke 800x600
curl -X POST http://127.0.0.1:8000/convert \
  -F "file=@photo.heic" \
  -F "format=jpg" \
  -F "width=800" \
  -F "height=600"
```

### Example 3: Return File Langsung (Tanpa JSON)

```bash
# Return file binary langsung untuk di-stream ke browser
curl -X POST http://127.0.0.1:8000/convert \
  -F "file=@photo.heic" \
  -F "format=jpg" \
  -F "return_file=true" \
  -o output.jpg
```

### Example 4: Python Client Example

```python
import requests

# Upload dan convert
files = {'file': open('photo.heic', 'rb')}
data = {
    'format': 'jpg',
    'quality': 85,
    'width': 800
}

response = requests.post(
    'http://127.0.0.1:8000/convert',
    files=files,
    data=data
)

result = response.json()
print(f"File ID: {result['file_id']}")
print(f"Download URL: {result['url']}")

# Download file
download_response = requests.get(
    f"http://127.0.0.1:8000/download/{result['file_id']}"
)
with open('output.jpg', 'wb') as f:
    f.write(download_response.content)
```

---

## 📁 File Structure

```
/home/sigitdev/
├── api.py                      # Main FastAPI application
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── venv/                       # Virtual environment
├── uploads/                    # Original HEIC files (temp storage)
├── converted/                  # Converted image files
│   └── metadata.json          # File tracking & expiry info
├── logs/
│   └── error.log              # Error log file
└── test_image.heic            # Test files
```

---

## ⚙️ Configuration

### File Storage
- **Upload folder**: `/home/sigitdev/uploads/`
- **Converted folder**: `/home/sigitdev/converted/`
- **Logs folder**: `/home/sigitdev/logs/`

### Cleanup Settings
- **Expiry time**: 24 hours setelah file dibuat
- **Cleanup interval**: Setiap 1 jam (background scheduler)
- **Metadata file**: `/home/sigitdev/converted/metadata.json`

### Default Settings
```python
EXPIRY_HOURS = 24
DEFAULT_QUALITY = 85
ALLOWED_FORMATS = {"jpg", "png", "jpeg"}
ALLOWED_EXTENSIONS = {".heic"}
```

---

## 🔒 Security Features

1. **File Validation**
   - Extension check (.heic only)
   - Magic bytes verification (HEIF/HEIC signature)
   - File size validation

2. **Input Sanitization**
   - Quality parameter validation (0-100)
   - Dimension validation (positive integers)
   - Format whitelist validation

3. **Error Handling**
   - No sensitive information leak
   - Detailed JSON error responses
   - Comprehensive error logging

4. **Auto Cleanup**
   - Automatic file deletion setelah 24 jam
   - Background scheduler task
   - Metadata cleanup

---

## 🐛 Troubleshooting

### Issue: "File harus berformat HEIC"
**Solution**: Pastikan file benar-benar berekstensi `.heic`

### Issue: "Magic bytes HEIC tidak ditemukan"
**Solution**: File bukan HEIC yang valid. Cek:
- Download file dari iPhone/Mac yang genuine
- Gunakan tools seperti `ffmpeg` untuk convert ke HEIC
- Verify file dengan: `file photo.heic`

### Issue: "Konversi HEIC gagal: cannot identify image file"
**Solution**: File HEIC corrupt atau tidak complete. Try:
- Re-export dari iPhone/Mac
- Use `exiftool` to check file integrity

### Issue: File tidak ditemukan saat download
**Solution**: File sudah expired (> 24 jam). Re-convert file baru.

### Issue: Server not responding
**Solution**: Check scheduler atau background task:
```bash
# Check if server is running
ps aux | grep uvicorn

# Check logs
cat logs/error.log

# Restart server
pkill -f "uvicorn api:app"
uvicorn api:app --host 127.0.0.1 --port 8000
```

---

## 📊 Monitoring

### Check Server Status
```bash
curl http://127.0.0.1:8000/health
```

### View Error Logs
```bash
tail -f /home/sigitdev/logs/error.log
```

### Check File Metadata
```bash
cat /home/sigitdev/converted/metadata.json | python -m json.tool
```

### Clean Files Manually
```bash
rm -rf /home/sigitdev/converted/*
rm /home/sigitdev/converted/metadata.json
```

---

## 🚀 Deployment

### Development
```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
```

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📝 License & Support

API ini dibuat sesuai dengan AGENTS.md guidelines.

Untuk feedback atau issue, silakan report di GitHub.

---

## 🔄 Version History

### v1.0.0 (2026-01-13)
- Initial release
- HEIC to JPG/PNG/JPEG conversion
- Quality control (0-100)
- Resize support
- Auto cleanup (24 hours)
- Full error handling
- Comprehensive logging
