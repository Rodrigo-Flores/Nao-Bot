import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import pytz
from datetime import datetime
import random

INPUT_TEXT = 0

with open('token.json') as json_file:
    data = json.load(json_file)
    token = data['token']

def btn(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Morning Mode', callback_data='morning')],
            [InlineKeyboardButton(text='Noon Mode', callback_data='noon')],
            [InlineKeyboardButton(text='Night Mode', callback_data='night')]
        ])
    )

def textCallBack(update, context):
        query = update.callback_query
        query.answer()

        job_queue = updater.job_queue

        if query.data == 'morning':
            job_queue.run_daily(
                Callback,
                datetime.now().replace(hour=8, minute=45, second=0, microsecond=0),
                days=(0, 1, 2, 3, 4, 5, 6),
                context=data["groupID"]
            )

        elif query.data == 'noon':
            job_queue.run_daily(
                Callback,
                datetime.now().replace(hour=16, minute=34, second=0, microsecond=0),
                days=(0, 1, 2, 3, 4, 5, 6),
                context=data["groupID"]
            )

        elif query.data == 'night':
            job_queue.run_daily(
                Callback,
                datetime.now().replace(hour=23, minute=34, second=30, microsecond=0),
                days=(0, 1, 2, 3, 4, 5, 6),
                context=data["groupID"]
            ) 

def Callback(context):
    phrase = "TESTING PHRASE"
    groupID = data["groupID"]
    context.bot.send_message(chat_id=groupID, text=phrase)

if __name__ == '__main__':
    updater = Updater(
        token=token,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('time', time),
        CallbackQueryHandler(textCallBack)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, textCallBack)]
        },

        fallbacks=[CommandHandler('cancel', time)]
    ))

    # job_queue = updater.job_queue
    # job_queue.run_daily(
    #     Callback,
    #     datetime.now().replace(hour=23, minute=21, second=0, microsecond=0),
    #     days=(0, 1, 2, 3, 4, 5, 6),
    #     context=-481968454
    # )

    updater.start_polling()
    updater.idle()
