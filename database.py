# database.py
import sqlite3
from datetime import datetime
import os

DB_PATH = "sales.db"

def init_db():
    """Создаёт базу данных и таблицу sales, если их нет."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id TEXT PRIMARY KEY,
            product TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_sale(product: str, amount: float) -> bool:
    """Добавляет продажу в БД. Возвращает True при успехе."""
    try:
        sale_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sales (id, product, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (sale_id, product.strip(), amount, timestamp))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] Не удалось добавить продажу: {e}")
        return False

def get_all_sales():
    """Возвращает список всех продаж (словари)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[DB ERROR] Не удалось загрузить продажи: {e}")
        return []

def get_sales_like(query: str):
    """Возвращает продажи, где product содержит query (регистронезависимо)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM sales 
            WHERE LOWER(product) LIKE ?
            ORDER BY timestamp DESC
        """, (f"%{query.lower()}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[DB ERROR] Поиск не удался: {e}")
        return []

def get_sales_count():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_total_revenue():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM sales")
        total = cursor.fetchone()[0] or 0.0
        conn.close()
        return round(total, 2)
    except:
        return 0.0

# Инициализация при импорте
init_db()