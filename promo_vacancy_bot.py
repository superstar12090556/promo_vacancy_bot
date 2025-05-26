from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

TARGET_CHAT = '@spa_promo_vacancy_bot'

# Хэндлер команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем метку канала из ссылки
    source_tag = context.args[0] if context.args else 'unknown'

    # Кнопка для отправки номера
    keyboard = [[KeyboardButton("Отправить номер", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    # Сохраняем метку в пользовательском контексте
    context.user_data['source'] = source_tag

    await update.message.reply_text(
        "Привет! Чтобы оставить отклик, нажми кнопку ниже и отправь номер телефона.",
        reply_markup=reply_markup
    )

# Хэндлер получения номера
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user
    source_tag = context.user_data.get('source', 'unknown')

    text = (
        f"📥 Новый отклик\n"
        f"Имя: {user.first_name or '-'}\n"
        f"Username: @{user.username}" if user.username else "Username: —" + "\n"
        f"Телефон: {contact.phone_number}\n"
        f"Источник: {source_tag}"
    )

    await context.bot.send_message(chat_id=TARGET_CHAT, text=text)
    await update.message.reply_text("Спасибо! Мы свяжемся с тобой в ближайшее время.")

# Основной запуск
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

print("Бот запущен")
app.run_polling()
