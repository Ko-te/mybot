#TG bot

import datetime as dt
from telebot import types
import telebot, random, requests, json, time
from bs4 import BeautifulSoup
# https://api.nasa.gov/planetary/apod?date=YYYY-MM-DD&api_key=DEMO_KEY
# https://api.nasa.gov/

token = '6157829694:AAGQ4crNBbsTQpv4Z7P0F43b3CR_GfZvQa8'
bot = telebot.TeleBot(token)


url = 'https://ru.investing.com/currencies/'
response = requests.get(url)
print(response)
bs = BeautifulSoup(response.text,"lxml")


@bot.message_handler(commands=["start"])
def start(message):
    now = dt.datetime.now()
    x = ['Hello! ', 'HI！', 'Привет！', '你們好! ','¡Hola! ']
    x = random.choice(x)
    bot.send_message(message.chat.id, x + f'Время по МСК: {now}')


@bot.message_handler(commands=['day'])
def get_everyday_photo(message):
    try:
        bot.send_photo(chat_id=message.chat.id, photo=get_photo_from_nasa(), timeout=5)
    except:
        bot.send_message(message.chat.id, 'что-то пошло не по плану')


@bot.message_handler(commands=['button'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("€/₽ EUR/RUB")
    btn2 = types.KeyboardButton('$/₽ USD/RUB')
    btn3 = types.KeyboardButton('/day')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, " Выберите что либо: ", reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == '€/₽ EUR/RUB':
        euro = bs.find('td', 'pid-1691-high')
        bot.send_message(message.chat.id, f'1€ = {euro.text} ₽')
    elif message.text == '$/₽ USD/RUB':
        usd = bs.find('td', 'pid-2186-high')
        bot.send_message(message.chat.id, f'1$ = {usd.text} ₽')

#***********************************************************************************************************
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def get_photo_from_nasa():
    data_json = requests.get((f'https://api.nasa.gov/planetary/apod?date={random_date("2016-1-1", "2023-1-1", random.random())}&api_key=E5xv6az3dPxh97JHtqCr7SASt0pocF8TR7xIqD3F'))
    # (f'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
    data = json.loads(data_json.text)
    return data.get('url')
#*************************************************************************************************************



bot.infinity_polling()
