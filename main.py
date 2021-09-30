import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import pytz
from datetime import datetime

INPUT_TEXT = 0

with open('token.json') as json_file:
    data = json.load(json_file)
    token = data['token']

def time(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='CHILEAN TIME', callback_data='1')],
            [InlineKeyboardButton(text='FLORIDA, USA TIME', callback_data='2')],
            [InlineKeyboardButton(text='ASIA/KOLKATA', callback_data='3')]
        ])
    )

def textCalllBack(update, context):
        query = update.callback_query
        query.answer()


        if query.data == '1':
            query.edit_message_text(
                text='Chilean time is: ' + str(datetime.now(pytz.timezone('America/Santiago')).strftime('%H:%M:%S'))
            )
        elif query.data == '2':
            query.edit_message_text(
                text='Florida time is: ' + str(datetime.now(pytz.timezone('US/Eastern')).strftime('%H:%M:%S'))
            )
        elif query.data == '3':
            query.edit_message_text(
                text='Asia/Kolkata time is: ' + str(datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'))
            )
        

if __name__ == '__main__':
    updater = Updater(
        token=token,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('time', time),
        CallbackQueryHandler(textCalllBack)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, textCalllBack)]
        },

        fallbacks=[CommandHandler('cancel', time)]
    ))

    updater.start_polling()
    updater.idle()
