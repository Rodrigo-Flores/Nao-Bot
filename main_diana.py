from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    ConversationHandler, 
    CallbackQueryHandler
)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import json
import random
import pytz
from datetime import datetime

INPUT_TEXT = range(1)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

tz = pytz.timezone('America/Santiago')
dt = datetime.now(tz)

with open('data.json', 'r') as file:
    data = json.load(file)

updater = Updater(token=data["token"], use_context=True)
job_queue = updater.job_queue

with open('clippings.txt', 'r') as file:
    clippings = file.read()

def start(update, context):
    groupID = data['goodreadID']
    context.bot.send_message(chat_id=groupID, text='[ ! ] Bot is running ...')

def btnMode(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Morning Mode', callback_data='morning')],
            [InlineKeyboardButton(text='Noon Mode', callback_data='noon')],
            [InlineKeyboardButton(text='Night Mode', callback_data='night')]
        ])
    )

def morningMode():
    name = 'Have a good read at morning!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=8, minute=0, second=0, microsecond=0)
    
    return time, days, name

def noonMode():
    name = 'Have a good read at noon!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=23, minute=46, second=0, microsecond=0)

    return time, days, name

def nightMode():
    name = 'Have a good read at night!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=21, minute=30, second=0, microsecond=0)

    return time, days, name


def Callback(context):
    phrase = random.choice(clippings.split('\n'))
    groupID = data['goodreadID']
    context.bot.send_message(chat_id=groupID, text=phrase)


def Sched(update, context):
    query = update.callback_query

    print(query.data)
    if query.data == 'morning':
        time, days, name = morningMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Morning mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    elif query.data == 'noon':
        time, days, name = noonMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Noon mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    # elif context.args[0].lower() == 'night':
    elif query.data == 'night':
        time, days, name = nightMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Night mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    else:
        groupID = data['goodreadID']
        msg = "🙁 ¡Oops! Please, try with a valid argument."
        context.bot.send_message(chat_id=groupID, text=msg)

        return 1

def run_daily(time, days, name):
    job_queue.run_daily(
        Callback,
        time=time,
        days=days,
        name=name
    )


def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sched", Sched, pass_args=True))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('btnMode', btnMode),
        CallbackQueryHandler(Sched)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, Sched)]
        },

        fallbacks=[CommandHandler('cancel', btnMode)]
    ))

    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')
    updater.idle()

if __name__ == '__main__':
    main()