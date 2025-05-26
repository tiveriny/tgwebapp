import firebase_admin
from firebase_admin import credentials, db
import json

# Инициализация Firebase
cred = credentials.Certificate('firebase-config.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://miniapptgliberty-default-rtdb.firebaseio.com/'  # url базы данных
})

def add_product(name, description, price, image_url, latitude, longitude, user_id):
    """Добавление нового товара"""
    ref = db.reference('products')
    new_product = ref.push({
        'name': name,
        'description': description,
        'price': price,
        'image_url': image_url,
        'latitude': latitude,
        'longitude': longitude,
        'user_id': user_id,
        'created_at': {'.sv': 'timestamp'}
    })
    return new_product.key

def get_all_products():
    """Получение всех товаров"""
    ref = db.reference('products')
    products = ref.get()
    if not products:
        return []
    
    # Преобразуем данные в список
    return [
        {
            'id': key,
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'image_url': data['image_url'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'user_id': data['user_id']
        }
        for key, data in products.items()
    ]

def get_user_products(user_id):
    """Получение товаров пользователя"""
    ref = db.reference('products')
    products = ref.order_by_child('user_id').equal_to(user_id).get()
    if not products:
        return []
    
    return [
        {
            'id': key,
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'image_url': data['image_url'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'user_id': data['user_id']
        }
        for key, data in products.items()
    ] 