from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
import requests
import threading
import time

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

TARGET_CHAT = '@spa_promo_vacancy_bot'

# Хэндлер команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем метку из ссылки
    source_tag = context.args[0] if context.args else 'unknown'

    # Сохраняем метку в контексте чата
    context.chat_data['source'] = source_tag

    # Кнопка для отправки номера
    keyboard = [[KeyboardButton("Отправить номер", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Чтобы оставить отклик, нажмите кнопку ниже и отправь номер телефона.",
        reply_markup=reply_markup
    )

# Хэндлер получения номера
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("DEBUG — contact handler triggered")
    print("RAW update:", update)
    print("RAW context.user_data:", context.user_data)
    contact = update.message.contact
    user = update.message.from_user
    source_tag = context.chat_data.get('source', 'unknown')

    username = f"@{user.username}" if user.username else "—"
    text = (
        f"📥 Новый отклик\n"
        f"Имя: {user.first_name or '-'}\n"
        f"Username: {username}\n"
        f"Телефон: {contact.phone_number}\n"
        f"Источник: {source_tag}"
)


    await context.bot.send_message(chat_id=TARGET_CHAT, text=text)
    await update.message.reply_text("Спасибо! Мы свяжемся с вами в ближайшее время.")

def self_ping():
    while True:
        try:
            requests.get("https://promo-vacancy-bot.onrender.com")
        except Exception as e:
            print("self-ping failed:", e)
        time.sleep(30)

threading.Thread(target=self_ping).start()

# Основной запуск
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

print("Бот запущен")
app.run_polling()
