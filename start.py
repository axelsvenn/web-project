import logging
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from settings import TOKEN

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        "Здравствуйте! Для начала работы этого бота...\n"
        "...требуется ввести ваши личные данные.\n"
        "Введите ваш номер карты.")
    return 1


def first_response(update, context):
    locality = update.message.text  # номер карты
    update.message.reply_text(f"Какая погода в городе {locality}?")
    return 2


def second_response(update, context):
    weather = update.message.text
    print(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()