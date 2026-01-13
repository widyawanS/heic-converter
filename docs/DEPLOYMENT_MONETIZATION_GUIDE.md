# Panduan Deployment & Monetisasi API HEIC Converter
# Untuk Pemula Python

## 🎓 Bagian 1: Memahami Struktur Aplikasi

### Apa itu Python?
Python adalah bahasa pemrograman yang mudah dibaca. Seperti resep masakan:
- `def convert_image():` = instruksi untuk melakukan sesuatu
- `if format == 'jpg':` = jika format adalah jpg, maka...
- `import fastapi` = menggunakan alat yang sudah dibuat orang lain

### Struktur Aplikasi Anda
```
api.py         = "chef" yang melayani request dari user
utils.py       = "helper" untuk tugas-tugas spesifik
requirements.txt = "daftar belanja" (library yang dibutuhkan)
```

---

## 🚀 BAGIAN 2: CARA DEPLOY KE SERVER

### Option 1: DEPLOY KE HEROKU (PALING MUDAH UNTUK PEMULA)

**Keuntungan:**
- Gratis untuk test (sampai 550 jam/bulan)
- Tidak perlu setting server kompleks
- Tinggal push ke GitHub, langsung live
- UI yang user-friendly

**Langkah-langkah:**

#### Step 1: Buat akun Heroku
1. Buka https://www.heroku.com
2. Klik "Sign up"
3. Isi email, password, dan pilih "Python" sebagai bahasa
4. Buka email dan verify account

#### Step 2: Install Heroku CLI
```bash
# Linux/Mac
curl https://cli.heroku.com/install.sh | sh

# Windows - download dari: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 3: Siapkan Aplikasi untuk Heroku

Di folder `/home/sigitdev/`, buat file baru bernama `Procfile`:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

**Penjelasan:**
- `web:` = ini adalah web service
- `uvicorn api:app` = jalankan aplikasi
- `--host 0.0.0.0` = bisa diakses dari mana saja
- `--port $PORT` = gunakan port yang diberikan Heroku

#### Step 4: Update requirements.txt
Tambahkan di akhir:
```
gunicorn==21.2.0
```

#### Step 5: Push ke GitHub
```bash
# Inisialisasi git
git init
git add .
git commit -m "Initial commit"

# Buat repo di GitHub.com, kemudian:
git remote add origin https://github.com/YOUR_USERNAME/heic-converter.git
git branch -M main
git push -u origin main
```

#### Step 6: Deploy ke Heroku
```bash
# Login ke Heroku
heroku login

# Buat app baru
heroku create nama-app-anda

# Deploy dari GitHub
heroku git:remote -a nama-app-anda
git push heroku main

# Lihat logs
heroku logs --tail
```

**Selesai!** API Anda live di: `https://nama-app-anda.herokuapp.com`

---

### Option 2: DEPLOY KE RAILWAY.APP (LEBIH MUDAH & GRATIS LEBIH LAMA)

**Keuntungan:**
- Lebih mudah dari Heroku
- Free tier lebih generous ($5/bulan gratis)
- Setup tinggal klik-klik

**Langkah-langkah:**

1. Buka https://railway.app
2. Sign up dengan GitHub
3. Klik "New Project" → "Deploy from GitHub"
4. Pilih repository heic-converter
5. Railway otomatis detect Python project
6. Klik Deploy
7. Done! URL akan diberikan otomatis

---

### Option 3: DEPLOY KE DIGITALOCEAN DROPLET (CONTROL PENUH)

**Keuntungan:**
- Full control
- Lebih murah untuk long-term ($5/bulan untuk droplet basic)
- Tidak ada batasan request

**Setup:**
1. Buat akun di https://www.digitalocean.com
2. Buat Droplet (Ubuntu 22.04 Basic - $5/bulan)
3. SSH ke droplet
4. Install Python & dependencies
5. Clone repository dari GitHub
6. Jalankan dengan `gunicorn` + `nginx`

**Saya bisa bantu setup ini jika Anda mau.**

---

### Option 4: DOCKER + CLOUD (AWS, GCP, Azure)

Ini lebih advanced, tapi akan saya jelaskan di bawah.

---

## 📦 BAGIAN 3: CARA MEMBUAT DOCKER IMAGE

### Apa itu Docker?
Docker adalah "kotak" yang berisi:
- Aplikasi Anda
- Python
- Semua library yang dibutuhkan

Jadi ketika deploy, tidak perlu setup lagi. Tinggal "buka kotak" dan jalankan.

### Buat Dockerfile

Di `/home/sigitdev/`, buat file bernama `Dockerfile` (TANPA extension):

```dockerfile
# Gunakan Python 3.11 sebagai base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy aplikasi
COPY . .

# Create necessary directories
RUN mkdir -p uploads converted logs

# Expose port
EXPOSE 8000

# Run aplikasi
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Penjelasan:**
- `FROM python:3.11-slim` = gunakan Python resmi
- `WORKDIR /app` = folder tempat aplikasi
- `COPY` = salin file
- `RUN pip install` = install dependencies
- `EXPOSE 8000` = port yang digunakan
- `CMD` = perintah yang dijalankan saat container start

### Build Docker Image

```bash
# Build image
docker build -t heic-converter:1.0 .

# Test local
docker run -p 8000:8000 heic-converter:1.0

# Akses http://localhost:8000
```

### Deploy Docker Image ke Cloud

**Pilihan:**

**A. Docker Hub (Gratis)**
```bash
# Login
docker login

# Tag image
docker tag heic-converter:1.0 username/heic-converter:1.0

# Push
docker push username/heic-converter:1.0

# Sekarang siapa saja bisa pull dan run:
# docker pull username/heic-converter:1.0
```

**B. AWS (Amazon)**
```bash
# Push ke ECR (Elastic Container Registry)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxxxx.dkr.ecr.us-east-1.amazonaws.com

docker tag heic-converter:1.0 xxxxx.dkr.ecr.us-east-1.amazonaws.com/heic-converter:1.0

docker push xxxxx.dkr.ecr.us-east-1.amazonaws.com/heic-converter:1.0
```

---

## 💰 BAGIAN 4: CARA MONETISASI API

### Strategy 1: FREEMIUM MODEL (Recommended)

**Konsep:**
- Free tier: 5 konversi/hari
- Paid tier: Unlimited

**Implementasi:**

1. **Tambahkan Database** (SQLite dulu, mudah)
   - Tracking user ID
   - Count konversi per user
   - Track subscription status

2. **Tambahkan Authentication**
   - Setiap user dapat API key
   - API key dikirim via email

3. **Charge dengan Stripe/PayPal**
   - User upgrade → masuk ke subscriber list
   - Subscriber dapat unlimited quota

**Contoh Kode untuk Check Quota:**
```python
@app.post("/convert")
async def convert_image(
    file: UploadFile = File(...),
    api_key: str = Header(None),
    # ... parameters lainnya
):
    # Check API key
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Check quota
    if not user.is_subscriber:
        conversions_today = count_conversions_today(user.id)
        if conversions_today >= 5:
            raise HTTPException(status_code=429, detail="Daily limit reached. Upgrade to premium!")
    
    # Process conversion...
    # ... rest of code
```

---

### Strategy 2: PAY-PER-USE MODEL

**Konsep:**
- Charging per conversion
- Misal $0.01 - $0.05 per konversi
- Tergantung file size atau output format

**Pricing Examples:**
```
JPG Conversion: $0.01
PNG Conversion: $0.02 (karena file lebih besar)
Bulk (>10 files): Discount 20%

Atau:
- 100 konversi: $0.99
- 1000 konversi: $9.99
- 10000 konversi: $49.99
```

**Payment Gateway:**
- Stripe (paling populer, mudah)
- PayPal
- 2Checkout

---

### Strategy 3: SUBSCRIPTION MODEL

**Konsep:**
- Basic: $2.99/bulan (50 konversi)
- Pro: $9.99/bulan (500 konversi)
- Enterprise: $29.99/bulan (Unlimited)

**Implementasi:**
```python
# Check subscription status
@app.post("/convert")
async def convert_image(api_key: str = Header(None)):
    user = get_user_by_api_key(api_key)
    
    # Check if subscription active
    if user.subscription_expires < datetime.now():
        raise HTTPException(status_code=402, detail="Subscription expired")
    
    # Check monthly quota
    monthly_usage = count_conversions_this_month(user.id)
    if monthly_usage >= user.subscription.monthly_limit:
        raise HTTPException(status_code=429, detail="Monthly quota exceeded")
    
    # Process conversion...
```

---

### Strategy 4: API MARKETPLACE

Jual API Anda di:
- **RapidAPI** (https://rapidapi.com) - commission 30%
- **API.AI** (https://api.ai)
- **Postman** (https://www.postman.com/api-platform/api-marketplace/)

**Keuntungan:**
- Instant credibility
- Built-in payment system
- Ready audience

---

## 🔧 BAGIAN 5: IMPLEMENTASI SIMPLE FREEMIUM

Saya akan buatkan kode tambahan untuk Anda.

### Step 1: Tambah Database (SQLite)

File: `database.py`
```python
import sqlite3
from datetime import datetime, timedelta

def init_db():
    """Create database tables"""
    conn = sqlite3.connect('api_data.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            api_key TEXT UNIQUE,
            email TEXT,
            is_subscriber BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subscription_expires TIMESTAMP
        )
    ''')
    
    # Conversions table (for tracking)
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            conversion_date DATE,
            count INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_conversions_today(user_id):
    """Count conversions for today"""
    conn = sqlite3.connect('api_data.db')
    c = conn.cursor()
    
    today = datetime.now().date()
    c.execute(
        'SELECT count FROM conversions WHERE user_id = ? AND conversion_date = ?',
        (user_id, today)
    )
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else 0

def increment_conversion_count(user_id):
    """Increment conversion count for today"""
    conn = sqlite3.connect('api_data.db')
    c = conn.cursor()
    
    today = datetime.now().date()
    
    # Check if exists
    c.execute(
        'SELECT id FROM conversions WHERE user_id = ? AND conversion_date = ?',
        (user_id, today)
    )
    exists = c.fetchone()
    
    if exists:
        c.execute(
            'UPDATE conversions SET count = count + 1 WHERE user_id = ? AND conversion_date = ?',
            (user_id, today)
        )
    else:
        c.execute(
            'INSERT INTO conversions (user_id, conversion_date, count) VALUES (?, ?, 1)',
            (user_id, today)
        )
    
    conn.commit()
    conn.close()
```

### Step 2: Update API dengan Authentication

Di `api.py`, tambahkan di awal:
```python
from fastapi import Header, HTTPException
from database import get_user_conversions_today, increment_conversion_count

@app.post("/convert")
async def convert_image(
    file: UploadFile = File(...),
    format: str = Form(...),
    quality: int = Form(85),
    api_key: str = Header(None),  # NEW
    # ... other parameters
):
    """
    Konversi file HEIC.
    
    Require header: X-API-Key
    """
    
    # NEW: Check API key
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "MISSING_API_KEY",
                "message": "Silakan kirim API key di header: X-API-Key"
            }
        )
    
    # NEW: Get user
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "code": "INVALID_API_KEY",
                "message": "API key tidak valid"
            }
        )
    
    # NEW: Check daily limit for free users
    if not user['is_subscriber']:
        conversions_today = get_user_conversions_today(user['id'])
        if conversions_today >= 5:
            raise HTTPException(
                status_code=429,
                detail={
                    "status": "error",
                    "code": "DAILY_LIMIT_EXCEEDED",
                    "message": f"Anda sudah menggunakan 5 konversi hari ini. Upgrade ke Premium untuk unlimited!",
                    "upgrade_url": "https://yoursite.com/pricing"
                }
            )
    
    # ... rest of conversion code ...
    
    # NEW: Increment counter after successful conversion
    increment_conversion_count(user['id'])
    
    return response_data
```

---

## 💳 BAGIAN 6: INTEGRASI STRIPE (PAYMENT)

### Setup Stripe Account
1. Buka https://stripe.com
2. Create account
3. Get API keys dari dashboard

### Install Stripe
```bash
pip install stripe
```

### Buat Checkout Endpoint
```python
import stripe

stripe.api_key = "sk_test_xxxxx"  # dari dashboard Stripe

@app.post("/create-checkout")
async def create_checkout(api_key: str = Header(None)):
    """
    Create Stripe checkout session untuk upgrade ke Premium
    """
    
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Create checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'HEIC Converter - Monthly Premium',
                    },
                    'unit_amount': 999,  # $9.99 dalam cents
                },
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url='https://yoursite.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://yoursite.com/cancel',
    )
    
    return {"checkout_url": session.url}
```

---

## 📊 BAGIAN 7: DASHBOARD & MONITORING

### Setup Simple Dashboard (HTML)

File: `dashboard.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>HEIC Converter - Dashboard</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; }
        .stat { font-size: 24px; font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <h1>Statistik Penggunaan</h1>
    
    <div class="card">
        <h3>Konversi Hari Ini</h3>
        <div class="stat" id="today-count">0</div>
    </div>
    
    <div class="card">
        <h3>Total Konversi</h3>
        <div class="stat" id="total-count">0</div>
    </div>
    
    <div class="card">
        <h3>Status Subscription</h3>
        <div id="subscription-status">Free Plan</div>
    </div>
    
    <script>
        const apiKey = localStorage.getItem('api_key');
        
        // Get user stats
        fetch('/api/stats', {
            headers: { 'X-API-Key': apiKey }
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('today-count').textContent = data.conversions_today;
            document.getElementById('total-count').textContent = data.conversions_total;
            document.getElementById('subscription-status').textContent = 
                data.is_subscriber ? 'Premium ✓' : 'Free (5/hari)';
        });
    </script>
</body>
</html>
```

### Endpoint untuk Stats
```python
@app.get("/api/stats")
async def get_stats(api_key: str = Header(None)):
    """Get user statistics"""
    
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "conversions_today": get_user_conversions_today(user['id']),
        "conversions_total": get_user_total_conversions(user['id']),
        "is_subscriber": user['is_subscriber'],
        "subscription_expires": user['subscription_expires']
    }
```

---

## 🎯 RINGKASAN STEP-BY-STEP

### UNTUK DEPLOY:
1. Pilih salah satu: Heroku / Railway / DigitalOcean / Docker
2. Setup account di platform pilihan
3. Connect repository GitHub
4. Deploy!

### UNTUK MONETISASI:
1. Tambah database SQLite (tracking user & quota)
2. Tambah API key authentication
3. Implementasi freemium (5 gratis, unlimited berbayar)
4. Integrasi Stripe untuk payment
5. Buat dashboard untuk user

### RECOMMENDED FLOW:
```
Week 1: Deploy ke Heroku (free)
        ↓
Week 2: Tambah API key authentication
        ↓
Week 3: Setup database & quota system
        ↓
Week 4: Integrasi Stripe
        ↓
Week 5: Launch pricing page
```

---

## 📚 RESOURCES UNTUK BELAJAR

**Python Basics:**
- https://www.codecademy.com/learn/learn-python-3 (FREE)
- https://www.freecodecamp.org/learn/python-for-beginners/

**FastAPI:**
- https://fastapi.tiangolo.com/tutorial/
- https://www.youtube.com/watch?v=7t2alWQ9-9E

**Database (SQLite):**
- https://www.sqlitetutorial.net/

**Stripe:**
- https://stripe.com/docs/stripe-cli

**Docker:**
- https://www.docker.com/101-tutorial/

---

Apakah Anda ingin saya:
1. Buatkan kode lengkap untuk Freemium model?
2. Setup Docker file untuk Anda?
3. Buat panduan step-by-step deploy ke Heroku?
4. Buat simple pricing page?

Atau ada pertanyaan lainnya? 😊
