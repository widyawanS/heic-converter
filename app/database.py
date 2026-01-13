"""
Database module untuk tracking user dan quota
Menggunakan SQLite (built-in Python, tidak perlu install)
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Get database path dynamically (works from any location)
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "api_data.db"


def init_db():
    """Initialize database dengan tabel yang diperlukan"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    c = conn.cursor()
    
    # Tabel Users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            is_subscriber BOOLEAN DEFAULT 0,
            subscription_expires TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabel untuk tracking konversi harian
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            conversion_date DATE NOT NULL,
            count INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, conversion_date)
        )
    ''')
    
    # Tabel untuk tracking total konversi
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            format TEXT,
            file_size INTEGER,
            conversion_time FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabel untuk tracking payments
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            stripe_payment_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")


# ============= USER MANAGEMENT =============

def create_user(email: str, name: str = None) -> dict:
    """
    Buat user baru dan generate API key
    
    Returns:
        dict dengan user_id dan api_key
    """
    api_key = str(uuid.uuid4())
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO users (api_key, email, name)
            VALUES (?, ?, ?)
        ''', (api_key, email, name))
        conn.commit()
        
        user_id = c.lastrowid
        conn.close()
        
        return {
            "success": True,
            "user_id": user_id,
            "api_key": api_key,
            "email": email
        }
    except sqlite3.IntegrityError as e:
        conn.close()
        return {
            "success": False,
            "error": f"Email sudah terdaftar: {str(e)}"
        }
    except Exception as e:
        conn.close()
        return {
            "success": False,
            "error": str(e)
        }


def get_user_by_api_key(api_key: str) -> dict:
    """Get user berdasarkan API key"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE api_key = ?', (api_key,))
    user = c.fetchone()
    conn.close()
    
    return dict(user) if user else None


def get_user_by_id(user_id: int) -> dict:
    """Get user berdasarkan ID"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    
    return dict(user) if user else None


# ============= QUOTA MANAGEMENT =============

def get_conversions_today(user_id: int) -> int:
    """
    Hitung berapa banyak konversi hari ini
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('''
        SELECT count FROM conversions
        WHERE user_id = ? AND conversion_date = ?
    ''', (user_id, today))
    
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else 0


def get_conversions_month(user_id: int) -> int:
    """
    Hitung konversi bulan ini
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # Ambil tanggal awal bulan
    now = datetime.now()
    first_day = now.strftime('%Y-%m-01')
    last_day = now.strftime('%Y-%m-%d')
    
    c.execute('''
        SELECT SUM(count) FROM conversions
        WHERE user_id = ? AND conversion_date BETWEEN ? AND ?
    ''', (user_id, first_day, last_day))
    
    result = c.fetchone()
    conn.close()
    
    return result[0] if result[0] else 0


def get_total_conversions(user_id: int) -> int:
    """
    Total konversi semua waktu
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    c.execute('''
        SELECT COUNT(*) FROM conversion_logs
        WHERE user_id = ?
    ''', (user_id,))
    
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else 0


def increment_conversion_count(user_id: int):
    """
    Tambah counter konversi hari ini
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Cek apakah sudah ada record hari ini
    c.execute('''
        SELECT id FROM conversions
        WHERE user_id = ? AND conversion_date = ?
    ''', (user_id, today))
    
    exists = c.fetchone()
    
    if exists:
        # Update
        c.execute('''
            UPDATE conversions SET count = count + 1
            WHERE user_id = ? AND conversion_date = ?
        ''', (user_id, today))
    else:
        # Insert
        c.execute('''
            INSERT INTO conversions (user_id, conversion_date, count)
            VALUES (?, ?, 1)
        ''', (user_id, today))
    
    conn.commit()
    conn.close()


def log_conversion(user_id: int, filename: str, format: str, file_size: int, conversion_time: float):
    """
    Log setiap konversi untuk analytics
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO conversion_logs (user_id, filename, format, file_size, conversion_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, filename, format, file_size, conversion_time))
    
    conn.commit()
    conn.close()


# ============= SUBSCRIPTION MANAGEMENT =============

def is_subscriber_active(user_id: int) -> bool:
    """
    Check apakah user memiliki subscription aktif
    """
    user = get_user_by_id(user_id)
    
    if not user or not user['is_subscriber']:
        return False
    
    if user['subscription_expires']:
        expires = datetime.fromisoformat(user['subscription_expires'])
        return expires > datetime.now()
    
    return False


def activate_subscription(user_id: int, days: int = 30) -> bool:
    """
    Activate subscription untuk user
    
    Args:
        user_id: ID user
        days: Berapa hari subscription (default 30 hari)
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    expires = datetime.now() + timedelta(days=days)
    expires_str = expires.isoformat()
    
    c.execute('''
        UPDATE users
        SET is_subscriber = 1, subscription_expires = ?
        WHERE id = ?
    ''', (expires_str, user_id))
    
    conn.commit()
    conn.close()
    
    return True


def deactivate_subscription(user_id: int) -> bool:
    """
    Deactivate subscription
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    c.execute('''
        UPDATE users
        SET is_subscriber = 0, subscription_expires = NULL
        WHERE id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()
    
    return True


# ============= PAYMENT TRACKING =============

def create_payment_record(user_id: int, amount: float, stripe_payment_id: str = None) -> int:
    """
    Buat record payment untuk audit trail
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO payments (user_id, amount, stripe_payment_id, status)
        VALUES (?, ?, ?, 'pending')
    ''', (user_id, amount, stripe_payment_id))
    
    conn.commit()
    payment_id = c.lastrowid
    conn.close()
    
    return payment_id


def update_payment_status(payment_id: int, status: str):
    """
    Update status payment (pending/completed/failed)
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    c.execute('''
        UPDATE payments SET status = ? WHERE id = ?
    ''', (status, payment_id))
    
    conn.commit()
    conn.close()


def get_user_payments(user_id: int) -> list:
    """
    Get semua payments untuk user
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,))
    
    payments = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return payments


# ============= ANALYTICS =============

def get_user_stats(user_id: int) -> dict:
    """
    Get statistik user lengkap
    """
    user = get_user_by_id(user_id)
    
    if not user:
        return None
    
    return {
        "user_id": user['id'],
        "email": user['email'],
        "name": user['name'],
        "is_subscriber": bool(user['is_subscriber']),
        "subscription_expires": user['subscription_expires'],
        "conversions_today": get_conversions_today(user_id),
        "conversions_this_month": get_conversions_month(user_id),
        "total_conversions": get_total_conversions(user_id),
        "joined_at": user['created_at']
    }


def get_api_stats() -> dict:
    """
    Get statistik API keseluruhan
    """
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # Total users
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    
    # Total subscribers
    c.execute('SELECT COUNT(*) FROM users WHERE is_subscriber = 1')
    total_subscribers = c.fetchone()[0]
    
    # Total conversions
    c.execute('SELECT COUNT(*) FROM conversion_logs')
    total_conversions = c.fetchone()[0]
    
    # Revenue
    c.execute('SELECT SUM(amount) FROM payments WHERE status = "completed"')
    total_revenue = c.fetchone()[0] or 0
    
    # Conversions today
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT SUM(count) FROM conversions WHERE conversion_date = ?', (today,))
    conversions_today = c.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_users": total_users,
        "total_subscribers": total_subscribers,
        "free_users": total_users - total_subscribers,
        "total_conversions": total_conversions,
        "conversions_today": conversions_today,
        "total_revenue_usd": round(total_revenue, 2)
    }


if __name__ == "__main__":
    # Setup database
    init_db()
    print("Database setup complete!")
    
    # Test: Create user
    result = create_user("test@example.com", "Test User")
    print(f"Created user: {result}")
    
    # Test: Get user
    if result['success']:
        user = get_user_by_api_key(result['api_key'])
        print(f"Retrieved user: {user}")
        
        # Test: Get stats
        stats = get_user_stats(user['id'])
        print(f"User stats: {stats}")
