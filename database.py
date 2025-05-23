import sqlite3
from datetime import datetime

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    # Создаем таблицу товаров
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_product(name, description, price, image_url, latitude, longitude, user_id):
    """Добавление нового товара"""
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO products (name, description, price, image_url, latitude, longitude, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, description, price, image_url, latitude, longitude, user_id))
    
    product_id = c.lastrowid
    conn.commit()
    conn.close()
    return product_id

def get_all_products():
    """Получение всех товаров"""
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM products ORDER BY created_at DESC')
    products = c.fetchall()
    
    conn.close()
    return products

def get_user_products(user_id):
    """Получение товаров пользователя"""
    conn = sqlite3.connect('marketplace.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM products WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    products = c.fetchall()
    
    conn.close()
    return products

# Инициализируем базу данных при импорте модуля
init_db() 