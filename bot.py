import os
import json
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import firebase_db

# Токен вашего бота
TOKEN = "7842727926:AAGNz2OAkkucu94mAzg8VU18P-RD3BZCA3Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть приложение", web_app=WebAppInfo(url="https://tiveriny.github.io/tgwebapp"))],
        [InlineKeyboardButton("Мои товары", callback_data="my_products")]
    ])
    
    await update.message.reply_text(
        "Привет! Я бот для Маркетплейса Либерти. "
        "Нажмите на кнопку ниже, чтобы открыть веб-приложение.",
        reply_markup=keyboard
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback-запросов"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "my_products":
        user_id = query.from_user.id
        products = firebase_db.get_user_products(user_id)
        
        if not products:
            await query.message.reply_text("У вас пока нет товаров.")
            return
        
        message = "Ваши товары:\n\n"
        for product in products:
            message += f"📦 {product['name']}\n"
            message += f"💰 Цена: {product['price']} руб.\n"
            message += f"📍 Местоположение: {product['latitude']}, {product['longitude']}\n\n"
        
        await query.message.reply_text(message)

async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик данных от веб-приложения"""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        user_id = update.effective_message.from_user.id

        if data.get('action') == 'add_product':
            product = data.get('product', {})
            product_id = firebase_db.add_product(
                name=product.get('name'),
                description=product.get('description'),
                price=product.get('price'),
                image_url=product.get('image_url'),
                latitude=product.get('latitude'),
                longitude=product.get('longitude'),
                user_id=user_id
            )
            await update.message.reply_text("Товар успешно добавлен!")

        elif data.get('action') == 'get_products':
            products = firebase_db.get_all_products()
            # Отправляем список товаров обратно в веб-приложение
            await update.message.reply_text(
                json.dumps({
                    'action': 'update_products',
                    'products': products
                })
            )

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main() 