import private
import telebot
from parsing import start_pars
import json
from telebot import types

bot = telebot.TeleBot(private.token)


def read_json():
    with open("news.json","r") as file:
        data = json.load(file)
    return data
    # read json file news.json


@bot.message_handler(commands=["start"])
def bot_start(message):

    bot.send_message(message.chat.id, "start pars in kloop kg...")
    bot.send_message(message.chat.id, "please wait..")

    start_pars()
    data = read_json()

    for x in data:
        bot.send_message(message.chat.id, f"№ {x} {data[x]['title']}")

    message_from_bot = bot.send_message(message.chat.id, 'Выберите число новости для подробной инфоормации(1-20): ')
    bot.register_next_step_handler(message_from_bot, check_number)


def check_number(message):
    keys = [str(x) for x in range(1, 21)]
    if message.text not in keys:

        message_from_bot = bot.send_message(message.chat.id, "Неверно! выберите число новости для подробной "
                                                             "инфоормации(1-20):")
        bot.register_next_step_handler(message_from_bot, check_number)
    else:
        data = read_json()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("Фото")
        button2 = types.KeyboardButton("Описание")

        keyboard.add(button1, button2)
        message_from_bot = bot.send_message(message.chat.id, f"{data[message.text]['title']}", reply_markup=keyboard)

        bot.register_next_step_handler(message_from_bot, show_info, message.text, data)


def show_info(message, number, data):

    if message.text == "Фото":
        bot.send_message(message.chat.id, data[number]["img"])
        message_from_bot = bot.send_message(message.chat.id, 'Выберите число новости для подробной инфоормации(1-20): ')
        bot.register_next_step_handler(message_from_bot, check_number)

    else:
        bot.send_message(message.chat.id, data[number]["description"])
        message_from_bot = bot.send_message(message.chat.id, 'Выберите число новости для подробной инфоормации(1-20): ')
        bot.register_next_step_handler(message_from_bot, check_number)


bot.polling(print("bot started.."))

