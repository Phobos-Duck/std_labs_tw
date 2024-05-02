from telebot.async_telebot import AsyncTeleBot
import api_news
import keyboards
from config_bd import add_cmd, add_telegram_user, check_cc, delete_set
from states import Statecommand, Stateweather, Statenews, StateSettings
from bot_command import helper, cmd_weather, cmd_news, app_city, app_category, clear_list, print_jokes
import bot_command
from config_env import get_token
import api_weather
import logging
import api_joke

logging.basicConfig(level=logging.DEBUG)
token = get_token('NF_TOKEN')
api_n = get_token('NW_TOKEN')
api_j = get_token('JS_TOKEN')
bot = AsyncTeleBot(token)
current_state = 0
other_state = 0
cmd = ""
city = ""
category = ""
index = 0


@bot.message_handler(commands=["start"])
async def start(message):
    global cmd
    user_id = message.from_user.id
    user_name = message.from_user.username
    cmd = Statecommand.start
    await bot_command.start_welcome(message.chat.id, bot)
    await add_telegram_user(user_id, user_name)
    await add_cmd(cmd, user_id)


@bot.message_handler(commands=["help"])
async def start_welcome(message):
    user_id = message.from_user.id
    await helper(message.chat.id, bot)
    global cmd
    cmd = Statecommand.help
    await bot.set_state(user_id, cmd)
    await add_cmd(cmd, user_id)


@bot.message_handler(commands=["weather"])
async def weather(message):
    global cmd, current_state, category, city
    city, category = await check_cc(city, category, message.from_user.id)
    if city:
        await bot.send_message(message.chat.id, "Вывожу в городе по умолчанию")
        await bot.send_message(message.chat.id, "Хорошо, а теперь введите дату в формате год-месяц-день:")
        current_state = Stateweather.datetime
    else:
        await bot.send_message(message.chat.id, "Отлично! Для начала напишите город, в котором хотите узнать погоду:")
        current_state = Stateweather.cities
    user_id = message.from_user.id
    cmd = Statecommand.weather
    await add_cmd(cmd, user_id)



@bot.message_handler(func=lambda message: current_state == "city")
async def check_city(message):
    global city, current_state
    if not city:
        city = message.text
    await bot.send_message(message.chat.id, "Хорошо, а теперь введите дату в формате год-месяц-день:")
    current_state = Stateweather.datetime


@bot.message_handler(func=lambda message: current_state == "datetime")
async def check_date(message):
    global city, current_state
    date = message.text
    await bot.send_message(message.chat.id, "Хорошо, обрабатываем запрос...")
    api_weather.check_weather(city, date)
    await cmd_weather(message, bot)
    current_state = 0
    city = ""
    date = ""


@bot.message_handler(commands=["news"])
async def news(message):
    global cmd, current_state, category, city
    city, category = await check_cc(city, category, message.from_user.id)
    if category:
        await bot.send_message(message.chat.id, "Вывожу новости по категории по умолчанию")
        await check_category(message)
    else:
        await bot.send_message(message.chat.id, "Отлично, для начала выберите категорию новостей", reply_markup=keyboards.keyboard_news())
        current_state = Statenews.category
    user_id = message.from_user.id
    cmd = Statecommand.news
    await add_cmd(cmd, user_id)


@bot.message_handler(func=lambda message: current_state == "category")
async def check_category(message):
    global current_state, category
    if not category:
        category = message.text
        await bot.send_message(message.chat.id, "Хорошо, обрабатываем запрос...")
    await bot.send_message(message.chat.id, "Вот что я получил по вашему запросу, если хотите увидеть следующую новость - выберете соответствующую кнопку", reply_markup=keyboards.list_news())
    api_news.get_news(api_n, category)
    await cmd_news(message.chat.id, bot, index)
    category = ""
    current_state = 0


@bot.message_handler(func=lambda message: message.text == "Следующая")
async def next(message):
    global index
    index += 1
    await cmd_news(message.chat.id, bot, index)


@bot.message_handler(func=lambda message: message.text == "На этом закончим")
async def stop(message):
    global index
    index = 0
    clear_list()
    await bot.send_message(message.chat.id, "Хорошо! Выберете новую команду", reply_markup=keyboards.make_keyboard())


@bot.message_handler(commands=["settings"])
async def settings(message):
    global cmd
    user_id = message.from_user.id
    await bot.send_message(message.chat.id, "Хорошо! Вы хотите установить конкретный пунтк или сразу оба(город и категорию)?", reply_markup=keyboards.keyboard_setting())
    cmd = Statecommand.settings
    await add_cmd(cmd, user_id)


@bot.message_handler(func=lambda message:  message.text == "Оба")
async def both(message):
    global other_state, current_state
    await bot.send_message(message.chat.id, "Хорошо! Настраиваюсь..")
    other_state = StateSettings.onlyCity
    current_state = StateSettings.both
    await bot.send_message(message.chat.id, "Отлично! Введите сначала город")


@bot.message_handler(func=lambda message: message.text == "Только город")
async def only_ci(message):
    global other_state
    await bot.send_message(message.chat.id, "Хорошо! Настраиваюсь..")
    await bot.send_message(message.chat.id, "Введите город, в котором вы хотите знать погоду всегда")
    other_state = StateSettings.onlyCity

@bot.message_handler(func=lambda message: message.text == "Удалить все настройки")
async def delet(message):
    global other_state
    await bot.send_message(message.chat.id, "Хорошо! Настраиваюсь..")
    other_state = StateSettings.delete
    await dele(message)

@bot.message_handler(func=lambda message: message.text == "Только категорию")
async def only_ca(message):
    global other_state
    await bot.send_message(message.chat.id, "Хорошо! Настраиваюсь..")
    await bot.send_message(message.chat.id, "Введите категорию, по которой вы хотите узнавать новости", reply_markup=keyboards.keyboard_news())
    other_state = StateSettings.onlyCa


@bot.message_handler(func=lambda message: other_state == "delete")
async def dele(message):
    global other_state
    await delete_set(message.from_user.id)
    other_state = 0
    await bot.send_message(message.chat.id, "Все параметры были удалены", reply_markup=keyboards.make_keyboard())


@bot.message_handler(func=lambda message: other_state == "onlyCi")
async def only_ci(message):
    global other_state, current_state
    if(current_state == "both"):
        await app_city(message)
        other_state = StateSettings.onlyCa
        await bot.send_message(message.chat.id, "Теперь введите категорию новостей", reply_markup=keyboards.keyboard_news())
    else:
        await app_city(message)
        await bot.send_message(message.chat.id, "Отлично! Я запомнил ваш выбор)", reply_markup=keyboards.make_keyboard())
        other_state = 0


@bot.message_handler(func=lambda message: other_state == "onlyCa")
async def only_ca(message):
    global other_state, current_state
    await app_category(message)
    await bot.send_message(message.chat.id, "Отлично! Я запомнил ваш выбор)", reply_markup=keyboards.make_keyboard())
    current_state = 0
    other_state = 0



@bot.message_handler(commands=["joke"])
async def joke(message):
    global cmd
    user_id = message.from_user.id
    cmd = Statecommand.start
    api_joke.parse()
    await bot.send_message(message.chat.id, "Отлично! Первая шутка будет...")
    await add_cmd(cmd, user_id)
    await print_jokes(message, bot)

async def main():
    await bot.polling(none_stop=True)
