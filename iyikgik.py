# TG bot
from work import *
from telebot import types
import telebot, random, requests, json
from bs4 import BeautifulSoup
import datetime as dt
from telebot import types

# https://api.nasa.gov/planetary/apod?date=YYYY-MM-DD&api_key=DEMO_KEY
# https://api.nasa.gov/

token = '6157829694:AAGQ4crNBbsTQpv4Z7P0F43b3CR_GfZvQa8'
bot = telebot.TeleBot(token)

url = 'https://ru.investing.com/currencies/'
response = requests.get(url)
print(response)
bs = BeautifulSoup(response.text, "lxml")


@bot.message_handler(commands=["start"])
def start(message):
    now = dt.datetime.now()
    x = ['Hello! ', 'HI！', 'Привет！', '你們好! ', '¡Hola! ']
    x = random.choice(x)

    bot.send_message(message.chat.id, x + f'Время по МСК: {now}')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("€/₽ EUR/RUB")
    btn2 = types.KeyboardButton('$/₽ USD/RUB')
    btn3 = types.KeyboardButton('Рандомное фото дня NASA')
    btn4 = types.KeyboardButton('Рандомный коктейль')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.from_user.id, " Выберите что либо: ", reply_markup=markup)



@bot.message_handler(commands=['cocktail'])
def get_cocktail(message):
    data = json.loads(requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic').text)
    index = random.randint(0, len(data.get('drinks')) - 1)

    markup_recipe = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Recipe", callback_data=index)
    button2 = types.InlineKeyboardButton("×", callback_data=index)
    markup_recipe.add(button1, button2)

    try:

        bot.send_photo(chat_id=message.chat.id, photo=random_cocktail_photo(index), caption=get_random_cocktail(index),
                       reply_markup=markup_recipe, timeout=5)
        # bot.send_message(message.chat.id, get_random_cocktail())
    except:
        bot.send_message(message.chat.id, 'что-то пошло не по плану')


@bot.message_handler(commands=['day'])
def get_everyday_photo(message):
    try:
        bot.send_photo(chat_id=message.chat.id, photo=get_photo_from_nasa(), caption=get_date_from_nasa(), timeout=5)

    except:
        bot.send_message(message.chat.id, 'что-то пошло не по плану')


@bot.message_handler(commands=['button'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("€/₽ EUR/RUB")
    btn2 = types.KeyboardButton('$/₽ USD/RUB')
    btn3 = types.KeyboardButton('Рандомное фото дня NASA')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.from_user.id, " Выберите что либо: ", reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    data = json.loads(requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic').text)
    index = random.randint(0, len(data.get('drinks')) - 1)
    markup_recipe = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Recipe", callback_data=index)
    button2 = types.InlineKeyboardButton("×", callback_data=index)
    markup_recipe.add(button1, button2)

    if message.text == '€/₽ EUR/RUB':

        try:
            euro = bs.find('td', 'pid-1691-high')
            bot.send_message(message.chat.id, f'1€ = {euro.text} ₽')

        except:
            bot.send_message(message.chat.id, 'что-то пошло не по плану')

    elif message.text == '$/₽ USD/RUB':

        try:
            usd = bs.find('td', 'pid-2186-high')
            bot.send_message(message.chat.id, f'1$ = {usd.text} ₽')

        except:
            bot.send_message(message.chat.id, 'что-то пошло не по плану')

    elif message.text == 'Рандомное фото дня NASA':

        try:
            bot.send_photo(chat_id=message.chat.id, photo=get_photo_from_nasa(), caption=get_date_from_nasa(),
                           timeout=5)

        except:
            bot.send_message(message.chat.id, 'что-то пошло не по плану')

    elif message.text == 'Рандомный коктейль':

        try:

            bot.send_photo(chat_id=message.chat.id, photo=random_cocktail_photo(index),
                           caption=get_random_cocktail(index), reply_markup=markup_recipe, timeout=5)
            # bot.send_message(message.chat.id, get_random_cocktail())
        except:
            bot.send_message(message.chat.id, 'что-то пошло не по плану')




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        try:
            bot.send_message(call.message.chat.id, f'Recipe: {recipe(int(call.data))}')

        except:
            bot.send_message(call.message.chat.id, "Error in CallBack_query...")


bot.infinity_polling()
