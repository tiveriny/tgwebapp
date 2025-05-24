from telegram import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен вашего бота
TOKEN = "7842727926:AAGNz2OAkkucu94mAzg8VU18P-RD3BZCA3Q"

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть приложение", web_app=WebAppInfo(url="https://tiveriny.github.io/tgwebapp"))]
    ])
    
    await update.message.reply_text(
        "Привет! Я бот для справочника цен Либерти. "
        "Нажмите на кнопку ниже, чтобы открыть мини-приложение-справочник.",
        reply_markup=keyboard
    )

def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main() 