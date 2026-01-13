# API Usage Examples - Testing Guide

Dokumentasi ini menunjukkan cara test API HEIC Converter setelah deploy ke Heroku.

## 📌 Base URL (ganti dengan URL Heroku kamu)

```
https://heic-converter-widya.herokuapp.com
```

Setelah deploy, ganti `heic-converter-widya` dengan nama app Heroku kamu!

---

## 1. Health Check / Test Koneksi

### Endpoint
```
GET /health
```

### Cara Test di Browser
```
https://heic-converter-widya.herokuapp.com/health
```

### Response
```json
{
  "status": "ok",
  "disk_space_gb": 0.5,
  "message": "API is running"
}
```

### Curl Command
```bash
curl https://heic-converter-widya.herokuapp.com/health
```

---

## 2. Get API Info

### Endpoint
```
GET /
```

### Cara Test di Browser
```
https://heic-converter-widya.herokuapp.com/
```

### Response
```json
{
  "message": "HEIC to JPG/PNG/JPEG Converter API",
  "version": "1.0",
  "endpoints": [
    {
      "method": "POST",
      "path": "/convert",
      "description": "Convert HEIC file to JPG/PNG/JPEG"
    },
    {
      "method": "GET",
      "path": "/download/{file_id}",
      "description": "Download converted file"
    },
    ...
  ]
}
```

---

## 3. Convert Image (HEIC → JPG/PNG/JPEG)

Ini adalah endpoint utama untuk convert gambar!

### Endpoint
```
POST /convert
```

### Cara Test

#### A. Pakai Swagger UI (Paling Mudah!)
1. Buka: `https://heic-converter-widya.herokuapp.com/docs`
2. Cari endpoint **POST /convert**
3. Klik **"Try it out"**
4. Upload file HEIC
5. Atur parameter (quality, width, height, format)
6. Klik **"Execute"**
7. Lihat hasilnya!

#### B. Pakai curl (Command Line)
```bash
# Convert HEIC ke JPG dengan quality 85
curl -X POST https://heic-converter-widya.herokuapp.com/convert \
  -F "file=@/path/ke/gambar.heic" \
  -F "format=jpg" \
  -F "quality=85"
```

#### C. Pakai Python
```python
import requests

url = "https://heic-converter-widya.herokuapp.com/convert"
files = {'file': open('gambar.heic', 'rb')}
data = {
    'format': 'jpg',
    'quality': 85,
    'width': 1920,
    'height': 1080
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(f"File ID: {result['file_id']}")
print(f"Download URL: {result['download_url']}")
```

### Parameters

| Parameter | Type | Required | Contoh | Keterangan |
|-----------|------|----------|--------|-----------|
| `file` | File | ✅ Yes | gambar.heic | File HEIC |
| `format` | String | ✅ Yes | jpg, png, jpeg | Format output |
| `quality` | Integer | ❌ No | 0-100 | Kualitas kompresi (default: 85) |
| `width` | Integer | ❌ No | 1920 | Lebar resize (px) |
| `height` | Integer | ❌ No | 1080 | Tinggi resize (px) |
| `return_file` | Boolean | ❌ No | true/false | Return file binary atau JSON link |

### Response - JSON (default)
```json
{
  "success": true,
  "file_id": "abc123xyz",
  "format": "jpg",
  "quality": 85,
  "original_size": 2048576,
  "converted_size": 512000,
  "compression_ratio": 0.75,
  "download_url": "/download/abc123xyz"
}
```

### Response - Binary File
Jika `return_file=true`, API langsung return file JPG/PNG/JPEG sebagai binary.

---

## 4. Download Converted File

Setelah convert, download file hasil konversi.

### Endpoint
```
GET /download/{file_id}
```

### Cara Test di Browser
```
https://heic-converter-widya.herokuapp.com/download/abc123xyz
```

### Curl Command
```bash
curl -O https://heic-converter-widya.herokuapp.com/download/abc123xyz
# File akan di-download dengan nama otomatis
```

---

## 5. Delete File

Hapus file yang sudah diconvert (untuk save storage).

### Endpoint
```
DELETE /delete/{file_id}
```

### Cara Test

#### Pakai curl
```bash
curl -X DELETE https://heic-converter-widya.herokuapp.com/delete/abc123xyz
```

#### Pakai Python
```python
import requests

response = requests.delete('https://heic-converter-widya.herokuapp.com/delete/abc123xyz')
print(response.json())
# {"success": true, "message": "File deleted"}
```

### Response
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

---

## 🧪 Complete Testing Workflow

### 1. Check API is Running
```bash
curl https://heic-converter-widya.herokuapp.com/health
```

### 2. Convert HEIC File
```bash
curl -X POST https://heic-converter-widya.herokuapp.com/convert \
  -F "file=@foto.heic" \
  -F "format=jpg" \
  -F "quality=90" \
  -o response.json

cat response.json
# {"file_id": "abc123", "download_url": "/download/abc123", ...}
```

### 3. Get File ID from Response
```bash
FILE_ID=$(cat response.json | grep -o '"file_id":"[^"]*"' | cut -d'"' -f4)
echo "File ID: $FILE_ID"
```

### 4. Download Converted File
```bash
curl -O https://heic-converter-widya.herokuapp.com/download/$FILE_ID
```

### 5. Clean Up (Delete File)
```bash
curl -X DELETE https://heic-converter-widya.herokuapp.com/delete/$FILE_ID
```

---

## 📱 Testing dari Mobile (iPhone)

1. Buka di iPhone Safari: `https://heic-converter-widya.herokuapp.com/docs`
2. Klik endpoint **POST /convert**
3. Klik **"Try it out"**
4. Di bagian file, tap untuk upload
5. Pilih foto dari Photos (atau ambil foto baru)
6. Atur format (jpg/png/jpeg)
7. Klik **"Execute"**
8. Klik link hasil download untuk save gambar

---

## ⚠️ Common Issues & Solutions

### "File not found" saat download
- File sudah dihapus otomatis (24 jam retention policy)
- Solusi: Convert ulang

### "Invalid format"
- Format harus: `jpg`, `png`, atau `jpeg` (lowercase)
- Bukan `JPG`, `PNG`, `JPEG`

### "Quality must be 0-100"
- Quality parameter harus integer 0-100
- Contoh valid: 85, 90, 100

### "File too large"
- Max file size: 50MB
- Solusi: Compress HEIC dulu atau resize

### API Error 500
- Biasanya karena file corrupt
- Coba dengan file HEIC lain
- Atau check Heroku logs

---

## 📊 Rate Limiting (Freemium Model)

Setelah setup Stripe:
- **Free tier**: 5 conversions/day
- **Starter**: 50 conversions/day ($4.99/month)
- **Pro**: Unlimited ($14.99/month)

Saat ini (pre-monetization): unlimited untuk testing!

---

## 🔗 Swagger UI Documentation

Cara paling mudah test API adalah via Swagger UI:

```
https://heic-converter-widya.herokuapp.com/docs
```

Di sini kamu bisa:
- ✅ Lihat semua endpoint
- ✅ Baca dokumentasi otomatis
- ✅ Test API langsung dari browser
- ✅ Lihat contoh request/response

---

## 🎓 Contoh Real-World Integration

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function convertImage(filePath) {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));
  form.append('format', 'jpg');
  form.append('quality', 90);

  const response = await axios.post(
    'https://heic-converter-widya.herokuapp.com/convert',
    form,
    { headers: form.getHeaders() }
  );

  return response.data;
}

convertImage('photo.heic').then(result => {
  console.log('Download URL:', result.download_url);
});
```

### PHP
```php
<?php
$file = new CURLFile('photo.heic');
$data = array(
    'file' => $file,
    'format' => 'jpg',
    'quality' => 90
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://heic-converter-widya.herokuapp.com/convert');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

echo $response;
?>
```

### HTML Form
```html
<form action="https://heic-converter-widya.herokuapp.com/convert" method="post" enctype="multipart/form-data">
  <input type="file" name="file" accept=".heic" required>
  
  <label>Format:
    <select name="format">
      <option>jpg</option>
      <option>png</option>
      <option>jpeg</option>
    </select>
  </label>
  
  <label>Quality (0-100):
    <input type="number" name="quality" value="85" min="0" max="100">
  </label>
  
  <label>Width (px):
    <input type="number" name="width" placeholder="optional">
  </label>
  
  <label>Height (px):
    <input type="number" name="height" placeholder="optional">
  </label>
  
  <button type="submit">Convert</button>
</form>
```

---

**Status**: Ready untuk test! Setelah Heroku deploy, semua contoh di atas akan work 🚀
