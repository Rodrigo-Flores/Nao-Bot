import os
import json
import qrcode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ChatAction
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

INPUT_TEXT = 0

with open('token.json') as json_file:
    data = json.load(json_file)
    token = data['token']

def start(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='CLICK 1', callback_data='sn1')],
            [InlineKeyboardButton(text='CLICK 2', callback_data='sn2')],
            [InlineKeyboardButton(text='CLICK 3', callback_data='sn3')]
        ])
    )

# def qr_command_handler(update, context):
#     update.message.reply_text('Enter text to generate QR code')

#     return INPUT_TEXT

def textCalllBack(update, context):
        query = update.callback_query
        # query.answer()

        # send a message
        query.edit_message_text(text="Selected option: {}".format(query.data))

        # query.edit_message_text(
        #     text='You are in the text callback'
        # )


# def generate_qr(text):
#     filename = text + '.png'
#     img = qrcode.make(text)
#     img.save(filename)

#     return filename

# def input_text(update, context):
#     text = update.message.text
#     filename = generate_qr(text)
#     chat = update.message.chat
#     send_qr(filename, chat)
#     os.remove(filename)

#     return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(
        token=token,
        use_context=True
    )

    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start),
        CallbackQueryHandler(textCalllBack)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text, textCalllBack)]
        },
        fallbacks=[CommandHandler('cancel', start)]
    ))

    # dp.add_handler(ConversationHandler(
    #     entry_points=[
    #         CommandHandler('start', start),
    #         CallbackQueryHandler(pattern='start', callback=textCalllBack)
    #     ],

    #     states={
    #         INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
    #     },

    #     fallbacks=[]
    # ))

    updater.start_polling()
    updater.idle()
