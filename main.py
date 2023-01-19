import telegram.ext
from requests import *
from telegram import *
import booklinks as bl
import re

token = '5738509972:AAEdL_Z2LvEepQfk3E9TxZNk1AkG5sF3sGY'
updater = telegram.ext.Updater(token=token, use_context=True)
dispatcher = updater.dispatcher



def Start(update,context):
    re.split("[^a-zA-Z]*", str(update.message.from_user.first_name))
    name = "".join(re.split("[^a-zA-Z]*", str(update.message.from_user.first_name)))
    context.bot.send_message(chat_id=update.effective_chat.id, text= f"Hey {name}, Let's get started! Use the Menu button below to see what I am capable of")



def timetable(update,context): 
    year = update.message.from_user.first_name[0:2]
    section_code = update.message.from_user.first_name[4:6]

    if year=="21":
        if section_code=="08":
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(f"Timetables/Y{year}/Y{year}-AIDS.jpg", 'rb'))


        elif section_code=="04":
            ece_sections=[]
            count=1
            with open('ECE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    ece_sections.append(inline)
                    count=count+1
    
            reply_markup = InlineKeyboardMarkup(ece_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?", reply_markup=reply_markup)

        elif section_code=="03":
            cse_sections=[]
            count=1
            with open('CSE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    cse_sections.append(inline)
                    count=count+1

            reply_markup = InlineKeyboardMarkup(cse_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?", reply_markup=reply_markup)
        else :
            pass



    elif year=="22":
            if section_code=="08":
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(f"Timetables/Y{year}/Y{year}-AIDS.jpg", 'rb'))
            elif section_code=="04":
                ece_sections=[]
                count=1
                with open('ECE.txt') as f:
                    for line in f:
                        inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                        ece_sections.append(inline)
                        count=count+1
    
                reply_markup = InlineKeyboardMarkup(ece_sections)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?", reply_markup=reply_markup)
    
            elif section_code=="03":
                cse_sections=[]
                count=1
                with open('CSE.txt') as f:
                    for line in f:
                        inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                        cse_sections.append(inline)
                        count=count+1
                reply_markup = InlineKeyboardMarkup(cse_sections)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?", reply_markup=reply_markup)
 



def library(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Library\nHere you can find the books you need\nChoose a subject below to explore more")
    library_options = []
    count=0
    with open('Library.txt') as f:
        for line in f:
            inline = [InlineKeyboardButton(line.rstrip(), callback_data=subject_codes[count])]
            library_options.append(inline)
            count = count+1
    reply_markup = InlineKeyboardMarkup(library_options)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option", reply_markup=reply_markup)

        
def showBooks(update,context,subject):
    context.bot.send_message(chat_id=update.effective_chat.id, text="The books for you are as follows")
    books = []
    count = 1
    with open(f'Books/{subject}.txt') as f:
        for line in f:
            inline = [InlineKeyboardButton(line.rstrip(), callback_data=f'{subject}'+str(count))]
            books.append(inline)
            count = count+1
    reply_markup = InlineKeyboardMarkup(books)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option", reply_markup=reply_markup)

def query_handler(update, context):

    query = update.callback_query.data
    if query in subject_codes:
        showBooks(update,context,query)
    elif query in bl.book_code.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text = bl.book_code[query])

    year = "Y"+query.split()[0]
    department = query.split()[1]
    section = query.split()[2]
    if department in ["CSE","ECE"]:
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(f"Timetables/{year}/{year}-{department}-{section}.jpg", 'rb'))
    
    





subjects={
"Linear Algebra" : "LA",
"Artificial Intelligence": "AI",
"Big Data" : "BD",
"Cloud Computing" : "CC",
"Computer Vision" : "CV",
"Data Structures" : "DS",
"Java" : "JA",
"Knowledge Representation" : "KR",
"Machine Learning" : "ML",
"Mathematical Programming":  "MP",
"Parallel Processing CUDA" : "PP",
"Probability"  : "PR",
"Python" : "PY",
"Reinforcement Learning" : "RL",
"Signal Processing" : "SP",
"Speech Signal Processing" : "SSP",
"Statistical Signal Processing" : "StatSP",
}
subject_codes = [x for x in subjects.values()]




    
       



        
dispatcher.add_handler(telegram.ext.CommandHandler('start',Start))
dispatcher.add_handler(telegram.ext.CommandHandler('library', library))
dispatcher.add_handler(telegram.ext.CommandHandler('timetable', timetable))

dispatcher.add_handler(telegram.ext.CallbackQueryHandler(query_handler))
updater.start_polling()
updater.idle()


