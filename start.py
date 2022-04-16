import logging
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from settings import TOKEN

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        "Здравствуйте! Для начала работы этого бота...\n"
        "...требуется ввести ваши личные данные.\n"
        "Как я могу к вам обращаться?")
    return 0


def null_response(update, context):
    name = update.message.text  # name
    update.message.reply_text(
        "Так-с, теперь введите данные вашей карты.\n"
        "Начнём с номера карты. Введите её в формате:\n"
        "xxxx xxxx xxxx xxxx")
    return 1


def first_response(update, context):
    locality = update.message.text  # номер карты
    update.message.reply_text("Хорошо, теперь введите дату истечения срока карты!\n"
                              "Формат карты месяца(M) и года(Y):\n"
                              "MM/YY")
    return 2


def second_response(update, context):
    locality = update.message.text  # дата истечения
    update.message.reply_text("Хорошо, теперь введите ваши...\n"
                              "...имя и фамилию по паспорту.\n"
                              "Формат ввода: GRIGORIY IVANOV")
    return 3


def third_response(update, context):
    locality = update.message.text  # имя собственное
    update.message.reply_text("Ну и последнее - введите...\n"
                              "...число на задней стороне карты.\n"
                              "Формат ввода: xxx")
    return 4


def forth_response(update, context):
    locality = update.message.text  # число сзади
    update.message.reply_text("Хорошо, сбор данных окончен.\n"
                              "Вы можете начать пользоваться мной!")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            0: [MessageHandler(Filters.text, null_response)],
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)],
            3: [MessageHandler(Filters.text, third_response)],
            4: [MessageHandler(Filters.text, forth_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()