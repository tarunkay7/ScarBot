import telegram.ext
from requests import *
from telegram import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import openai
from api import API_KEY

import booklinks as bl
import re

token = '5738509972:AAEdL_Z2LvEepQfk3E9TxZNk1AkG5sF3sGY'
openai.api_key = API_KEY

updater = telegram.ext.Updater(token=token, use_context=True)
dispatcher = updater.dispatcher





def Start(update, context):
    re.split("[^a-zA-Z]*", str(update.message.from_user.first_name))
    name = "".join(re.split("[^a-zA-Z]*", str(update.message.from_user.first_name)))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hey {name}, Let's get started! Use the Menu button below to see what I am capable of")


def timetable(update, context):
    year = update.message.from_user.first_name[0:2]
    section_code = update.message.from_user.first_name[4:6]

    if year == "21":
        if section_code == "08":
            context.bot.send_document(chat_id=update.effective_chat.id,
                                      document=open(f"Timetables/Y21/AI-CHO.pdf", 'rb'))


        elif section_code == "04":
            ece_sections = []
            count = 1
            with open('ECE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    ece_sections.append(inline)
                    count = count + 1

            reply_markup = InlineKeyboardMarkup(ece_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?",
                                     reply_markup=reply_markup)

        elif section_code == "03":
            cse_sections = []
            count = 1
            with open('CSE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    cse_sections.append(inline)
                    count = count + 1

            reply_markup = InlineKeyboardMarkup(cse_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?",
                                     reply_markup=reply_markup)
        else:
            pass



    elif year == "22":
        if section_code == "08":
            context.bot.send_document(chat_id=update.effective_chat.id,
                                      document=open(f"Timetables/Y{year}/Y{year}-AIDS.pdf", 'rb'))
        elif section_code == "04":
            ece_sections = []
            count = 1
            with open('ECE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    ece_sections.append(inline)
                    count = count + 1

            reply_markup = InlineKeyboardMarkup(ece_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?",
                                     reply_markup=reply_markup)

        elif section_code == "03":
            cse_sections = []
            count = 1
            with open('CSE.txt') as f:
                for line in f:
                    inline = [InlineKeyboardButton(line.rstrip(), callback_data=f"{year[1:]} {line.rstrip()}")]
                    cse_sections.append(inline)
                    count = count + 1
            reply_markup = InlineKeyboardMarkup(cse_sections)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Which section do you belong to?",
                                     reply_markup=reply_markup)


def library(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to the Library\nHere you can find the books you need\nChoose a subject below to explore more")
    library_options = []
    count = 0
    with open('Library.txt') as f:
        for line in f:
            inline = [InlineKeyboardButton(line.rstrip(), callback_data=subject_codes[count])]
            library_options.append(inline)
            count = count + 1
    reply_markup = InlineKeyboardMarkup(library_options)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option", reply_markup=reply_markup)


def showBooks(update, context, subject):
    context.bot.send_message(chat_id=update.effective_chat.id, text="The books for you are as follows")
    books = []
    count = 1
    with open(f'Books/{subject}.txt') as f:
        for line in f:
            inline = [InlineKeyboardButton(line.rstrip(), callback_data=f'{subject}' + str(count))]
            books.append(inline)
            count = count + 1
    reply_markup = InlineKeyboardMarkup(books)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option", reply_markup=reply_markup)


def query_handler(update, context):
    query = update.callback_query.data
    if query in subject_codes:
        showBooks(update, context, query)
    elif query in bl.book_code.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=bl.book_code[query])

    year = "Y" + query.split()[0]
    department = query.split()[1]
    section = query.split()[2]
    if department in ["CSE", "ECE"]:
        context.bot.send_document(chat_id=update.effective_chat.id,
                                  document=open(f"Timetables/{year}/{year}-{department}-{section}.jpg", 'rb'))










def handle_message(update, context):
    """Handles messages that are not recognized commands"""
    message = update.message.text
    print(message)

   
    messages = [{"role": "system", "content": "Your name is Scar, a telegram bot that helps engineering students. If anyone ever asked you who create you you should say it was Tarun. Use emojis in your answers too whereever needed, you should also be able to show an image from google images when the user asks so "},
                {"role": "user", "content": message}]
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature=0.1
    )
    response = completion.choices[0].message.content.strip()

   
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def graph_function(update, context):
    # Extract the function name from the user's message using regex
    pattern = r'/graph\s+(.+)\s*'
    match = re.match(pattern, update.message.text)
    if not match:
        update.message.reply_text('Invalid command. Usage: /graph <function_name>')
        return
    
    function_name = match.group(1)
    display_name = function_name
    function_name = re.sub(r'\b(sin|cos|tan|sec|csc|cot)\b', r'np.\1', function_name)
    
    # Evaluate the function using numpy
    try:
        function = eval(f"lambda x: {function_name}")
        
    except Exception as e:
        update.message.reply_text(f'Error: {e}')
        return
    
    x = np.linspace(-10, 10, 100)
    y = np.array([function(i) for i in x])
    
    # Create the graph using matplotlib
    fig = plt.figure()
    ax= fig.add_subplot(1,1,1)
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Graph of {display_name}')

    # Save the graph as a PNG image
    fig.savefig('graph.png')

    # Send the graph as an image to the user via the Telegram Bot API
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('graph.png', 'rb'))



def graph3d(update, context):
    # Extract the function name from the user's message
    function_string = update.message.text.replace('/graph3d', '').strip()

    # Create a lambda function to evaluate the user's input function
    try:
        function = eval(f"lambda x, y: {function_string}")
    except Exception as e:
        update.message.reply_text(f'Error: {e}')
        return

    # Generate the x, y, and z values to plot
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    # Create the 3D plot using matplotlib
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(f'3D Graph of {function_string}')

    # Save the graph as a PNG image
    fig.savefig('graph3d.png')

    # Send the graph as an image to the user via the Telegram Bot API
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('graph3d.png', 'rb'))


def animate_function(update, context):
    # Extract the function name from the user's message using regex
    pattern = r'/animate\s+(.+)\s*'
    match = re.match(pattern, update.message.text)
    if not match:
        update.message.reply_text('Invalid command. Usage: /animate <function>')
        return

    function_string = match.group(1)

    # Create a lambda function to evaluate the user's input function
    try:
        function = eval(f"lambda x: {function_string}")
    except Exception as e:
        update.message.reply_text(f'Error: {e}')
        return

    # Set up the graph using matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Define the animation function
    def animate(i):
        x = np.linspace(-10, i/10, 1000)
        y = function(x)
        ax.clear()
        ax.plot(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Graph of {function_string}')

    # Create the animation using matplotlib
    anim = animation.FuncAnimation(fig, animate, frames=100, interval=20)

    # Save the animation as a GIF image
    anim.save('animation.gif', writer='imagemagick')

    # Send the animation as a file to the user via the Telegram Bot API
    context.bot.send_document(chat_id=update.message.chat_id, document=open('animation.gif', 'rb'))








subjects = {
    "Linear Algebra": "LA",
    "Artificial Intelligence": "AI",
    "Big Data": "BD",
    "Cloud Computing": "CC",
    "Computer Vision": "CV",
    "Data Structures": "DS",
    "Java": "JA",
    "Knowledge Representation": "KR",
    "Machine Learning": "ML",
    "Mathematical Programming": "MP",
    "Parallel Processing CUDA": "PP",
    "Probability": "PR",
    "Python": "PY",
    "Reinforcement Learning": "RL",
    "Signal Processing": "SP",
    "Speech Signal Processing": "SSP",
    "Statistical Signal Processing": "StatSP",
}
subject_codes = [x for x in subjects.values()]

dispatcher.add_handler(telegram.ext.CommandHandler('start', Start))
dispatcher.add_handler(telegram.ext.CommandHandler('library', library))
dispatcher.add_handler(telegram.ext.CommandHandler('cho', timetable))
dispatcher.add_handler(telegram.ext.CommandHandler('graph',graph_function))
dispatcher.add_handler(telegram.ext.CommandHandler('graph3d',graph3d))
dispatcher.add_handler(telegram.ext.CommandHandler('animate',animate_function))
dispatcher.add_handler(telegram.ext.CallbackQueryHandler(query_handler))
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
