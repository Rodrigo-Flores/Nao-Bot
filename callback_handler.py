import os
import json
import qrcode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

from qr_bot import INPUT_TEXT

with open('token.json') as json_file:
    data = json.load(json_file)
    token = data['token']


def start(update, context):
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

    def textCalllBack(update, context):
        query = update.callback_query
        query.answer()

        query.edit_message_text(
            text='You are in the text callback'
        )

        return INPUT_TEXT

if __name__ == '__main__':
    updater = Updater(
        token=token,
        use_context=True
    )

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CallbackQueryHandler(pattern="start", callback=textCallBack))

    # dp.add_handler(ConversationHandler(
    #     entry_points=[
    #         CommandHandler('start', start)
    #     ],

    #     states={
    #         INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
    #     },

    #     fallbacks=[]
    # ))

    updater.start_polling()
    updater.idle()