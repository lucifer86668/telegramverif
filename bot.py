from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

TOKEN = '7631236448:AAHUk7NH8PnnB4STRj0K6LGsDCncH7mdYNE'  # Замените на токен вашего бота
CHANNEL_LINK = 'https://t.me/+QJyC8NbFDbhkYTk6'  # Ссылка на ваш канал

# Состояния для проверки
AGE_CONFIRMATION, HUMAN_VERIFICATION = range(2)

# Приветственное сообщение
def start(update: Update, context):
    update.message.reply_text(
        "👋 Welcome! To proceed, you need to verify a few things.\n"
        "Step 1: Confirm that you are over 18 years old."
    )
    keyboard = [[InlineKeyboardButton("I am over 18", callback_data='over_18')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Click the button below to confirm:", reply_markup=reply_markup)
    return AGE_CONFIRMATION

# Проверка возраста
def age_confirmation(update: Update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'over_18':
        query.edit_message_text(
            text="✅ Thank you for confirming! Now, please verify that you are human."
        )
        keyboard = [[InlineKeyboardButton("I am human", callback_data='human')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Click the button below to confirm:", reply_markup=reply_markup)
        return HUMAN_VERIFICATION
    else:
        query.edit_message_text(
            text="❌ You must confirm your age to proceed."
        )
        return AGE_CONFIRMATION

# Проверка на "человек ли"
def human_verification(update: Update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'human':
        query.edit_message_text(
            text="✅ Verification complete! Click the button below to join the channel."
        )
        keyboard = [[InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Click below:", reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        query.edit_message_text(
            text="❌ Verification failed. Please try again."
        )
        return HUMAN_VERIFICATION

# Отмена
def cancel(update: Update, context):
    update.message.reply_text("❌ Verification process canceled.")
    return ConversationHandler.END

# Основной блок
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE_CONFIRMATION: [CallbackQueryHandler(age_confirmation)],
            HUMAN_VERIFICATION: [CallbackQueryHandler(human_verification)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()