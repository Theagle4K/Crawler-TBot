import telebot
from main import main, respondlink, DOMAIN, headers_, queued_urls, element_list, get_links,visited_urls
from constants import API_KEY
import itertools
import os

bot = telebot.TeleBot(API_KEY, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I can help you find the latest rental houses. Use the /scrap command to get started.")


@bot.message_handler(commands=['scrap'])
def start_scrap(message):
    bot.reply_to(message, "Starting to scrap now, please wait.")
    main(respondlink, DOMAIN, headers_, queued_urls, element_list)
    bot.reply_to(message, "Scraping has finished.")

@bot.message_handler(commands=['showlinks'])
def show_links(message):
    if os.path.isfile('data.json'):
        bot.reply_to(message, "Here are some links I have found while scraping:")
        for url in itertools.islice(get_links(visited_urls), 10) :
            bot.reply_to(message, url)
    else:
        bot.reply_to(message, "There are no links, please first try scrapping using \scrap command")


@bot.message_handler(commands=['senddata'])
def send_data(message):
    chat_id = message.chat.id
    bot.reply_to(message,"Here's the data obtained from the each publication:")
    bot.send_photo(chat_id, photo=open('data.png', 'rb'))
    bot.send_photo(chat_id, photo=open('price_vs_area.png', 'rb'))
    bot.send_photo(chat_id, photo=open('price_vs_rooms.png', 'rb'))

@bot.message_handler(commands=['deletedb'])
def delete_db(message):
    if os.path.isfile('data.json'):
        bot.reply_to(message,"Deleting Database...") 
        os.remove('data.json')
        os.remove('data.html')
        os.remove('data.png')
        bot.reply_to(message,"Database has been deleted.")
    else:
        bot.reply_to(message,'Database could not be deleted')




bot.polling()
