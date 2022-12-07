import telegram.ext
from requests import *
from telegram import *

token = '5738509972:AAEdL_Z2LvEepQfk3E9TxZNk1AkG5sF3sGY'
updater = telegram.ext.Updater(token=token, use_context=True)
dispatcher = updater.dispatcher




def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm SCAR .I can help you with your Academic Documents\nType /options to see what I can do.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Here are the list of services")

def options(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="/cho - To get the course handouts for any subject")



def cho(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="The course Handouts for you are as follows");
        course_hand_out_options = []
        count=1
        with open('Subjects.txt') as f:
            for line in f:
                inline = [InlineKeyboardButton(line.rstrip(), callback_data=str(count))]
                course_hand_out_options.append(inline)
                count = count + 1
 
        reply_markup = InlineKeyboardMarkup(course_hand_out_options)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option", reply_markup=reply_markup)

def query_handler(update, context):

    query = update.callback_query.data
    if query == "1":
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("AI_CHO.pdf", 'rb'))
    elif query == "2":
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("DM_CHO.pdf", 'rb'))
    elif query == "3":
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("JAVA_CHO.pdf", 'rb'))
    elif query == "4":
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("PS_CHO.pdf", 'rb'))
    elif query == "5":
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("OS_CHO.pdf", 'rb'))


dispatcher.add_handler(telegram.ext.CommandHandler('start', startCommand))
dispatcher.add_handler(telegram.ext.CommandHandler('cho', cho))
dispatcher.add_handler(telegram.ext.CommandHandler('Options', options))

dispatcher.add_handler(telegram.ext.CallbackQueryHandler(query_handler))
updater.start_polling()
updater.idle()


