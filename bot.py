# Python 3

from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import json

with open('token.json') as json_file:
    data = json.load(json_file)
    token = data['token']


def aux(update, context):
    btn1 = InlineKeyboardButton(
        text='OCTA AEROSPACE',
        url='https://www.octaaerospace.com/'
    )

    btn2 = InlineKeyboardButton(
        text='CENTRO SIMES',
        url='https://aeroespacial.centrosimes.com/'
    )

    update.message.reply_text(
        text='VISIT US!',
        reply_markup=InlineKeyboardMarkup([
            [btn1],
            [btn2]
        ])
    )

def start(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido a la pagina de Aeroespacial")
    update.message.reply_text(
        text='Bienvenido a la pagina de Aeroespacial',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='VISIT US!', callback_data='visit')]
        ])
    )   

if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('aux', aux))
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()