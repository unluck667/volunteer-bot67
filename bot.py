import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

user_state = {}

main_menu = ReplyKeyboardMarkup(
    [["О боте"], ["Заказать услугу"], ["Тех. поддержка"]],
    resize_keyboard=True
)

services_menu = ReplyKeyboardMarkup(
    [
        ["Совместный досуг"],
        ["Прогулка"],
        ["Сопровождение в поликлинику"],
        ["Бытовая помощь"],
        ["Смартфон с нуля"],
        ["Другое"],
        ["Назад"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! 👋\nВыберите пункт меню:",
        reply_markup=main_menu
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    if text == "О боте":
        await update.message.reply_text(
            "Данный бот создан для помощи волонтёров людям в пожилом возрасте."
        )

    elif text == "Заказать услугу":
        await update.message.reply_text("Выберите услугу:", reply_markup=services_menu)

    elif text in [
        "Совместный досуг",
        "Прогулка",
        "Сопровождение в поликлинику",
        "Бытовая помощь",
        "Смартфон с нуля"
    ]:
        await update.message.reply_text(
            "Отлично! С вами скоро свяжутся.",
            reply_markup=main_menu
        )
        await context.bot.send_message(
            ADMIN_ID,
            f"📩 Новый запрос!\nУслуга: {text}\nПользователь: @{user.username}\nID: {user.id}"
        )

    elif text == "Другое":
        user_state[user.id] = "waiting"
        await update.message.reply_text("Опишите вашу проблему:")

    elif user_state.get(user.id) == "waiting":
        await context.bot.send_message(
            ADMIN_ID,
            f"📩 Другое:\n{text}\nПользователь: @{user.username}\nID: {user.id}"
        )
        await update.message.reply_text("Запрос отправлен!", reply_markup=main_menu)
        user_state[user.id] = None

    elif text == "Тех. поддержка":
        await update.message.reply_text(
            f"ID: {user.id}\nНапишите этому пользователю."
        )

    elif text == "Назад":
        await update.message.reply_text("Меню:", reply_markup=main_menu)

def main():
    print("Бот запущен...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
