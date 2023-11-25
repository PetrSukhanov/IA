import telebot
import sqlite3
import webbrowser
from telebot import types

bot = telebot.TeleBot("6559970887:AAGVbyhfkGMadusbCOol7WPbj0g7mLizAlQ")

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar (50), password varchar)''')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Hello, now we will registrate you! PLease enter your name.')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
     global name 
  name = message.text.strip()
  bot.send_message(message.chat.id, 'Create password.')
  bot.register_next_step_handler(message, user_pass)

def user_pass(message):
  password = message.text.strip()

  conn = sqlite3.connect('base.sql')
  cur = conn.cursor()

  cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
  conn.commit()
  cur.close()
  conn.close()

  markup = telebot.types.InlineKeyboardMarkup()
  markup.add(telebot.types.InlineKeyboardButton(text='List of users', callback_data='users'))
  bot.reply_to(message, "You have been registrated", reply_markup=markup)



 markup = types.ReplyKeyboardMarkup()
 markup.add(types.KeyboardButton('Go to the site'))
 markup.add(types.KeyboardButton('Delete.'))
 markup.add(types.KeyboardButton('Change the text'))
 bot.send_message(message.chat.id, 'hey!', reply_markup=markup)
 bot.register_next_step_handler(message, on_click)

def on_click(message):
   if message.text == 'Go to the site':
       bot.send_message(message.chat.id, 'Website is opened')
   elif message.text == 'Delete':
       bot.send_message(message.chat.id, 'The photo was deleted')


markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton('Go to the site', url='https://google.com'))
markup.add(types.InlineKeyboardButton('Delete.', callback_data='delete'))
markup.add(types.InlineKeyboardButton('Change the text', callback_data='edit'))

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
   if callback.data=='delete':
       bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
   elif callback.data == 'edit':
       bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

@bot.message_handler(content_types=['photo'])
def get_file(message):
   bot.reply_to(message, 'Ok, I received it.', reply_markup=markup)

@bot.message_handler(commands=['site', 'website'])
def site(message):
   webbrowser.open('https://www.youtube.com')

@bot.message_handler(commands=['start'])
def main(message):
   bot.send_message(message.chat.id, f"hey,  {message.from_user.first_name} {message.from_user.last_name}")

@bot.message_handler(commands=['help'])
def main(message):
   bot.send_message(message.chat.id, "<b>I can help you</b>, <em>what would you like to know?</em>", parse_mode='html')

@bot.message_handler()
def info(message):
   if message.text.lower() == 'hello':
       bot.send_message(message.chat.id, f"hey,  {message.from_user.first_name} {message.from_user.last_name}")
   elif message.text.lower() == 'id':
       bot.reply_to(message, f'ID:{message.from_user.id}')

bot.polling(none_stop=True)
