import update_files
import keyboards
from config_env import get_token
from config_bd import add_city, add_category
from random import randint

weather_current = {}
all_news ={}
keys_in_weather = ['temp', "condition", "wind"]
api_n = get_token("NW_TOKEN")
check = 1
jokes = []




async def start_welcome(chat_id, bot):
    await bot.send_message(chat_id, update_files.text_welcome(), reply_markup=keyboards.make_keyboard())


async def helper(chat_id, bot):
    await bot.send_message(chat_id, update_files.help_inctruction())


def weather_in_api(current_temp, weather_condition, wind_speed):
    weather_current[keys_in_weather[0]] = current_temp
    weather_current[keys_in_weather[1]] = weather_condition
    weather_current[keys_in_weather[2]] = wind_speed

async def cmd_weather(message, bot):
    await bot.send_message(message.chat.id, "Итак, в ходе моего анализа вот следующая погода, ожидаемая на данное число: ")
    await bot.send_message(message.chat.id, f"Температура: {weather_current[keys_in_weather[0]]} \n Состояние погоды: {weather_current[keys_in_weather[1]]} "
                                            f"\n Скорость ветра: {weather_current[keys_in_weather[2]]}", reply_markup=keyboards.make_keyboard())

async def cmd_news(chat_id, bot, current_index):
    keys = list(all_news.keys())
    value = all_news[keys[current_index]]
    await bot.send_message(chat_id, f"{keys[current_index]}\n{value}")


def clear_list():
    all_news.clear()


def colect_news(key, value):
    all_news[key] = value

async def app_category(message):
    category_ = message.text
    await add_category(category_, message.from_user.id)


async def app_city(message):
    city_ = message.text
    await add_city(city_, message.from_user.id)

def colect_jokes(joke):
    jokes.append(joke)

async def print_jokes(message, bot):
    r = randint(1, len(jokes)-1)
    await bot.send_message(message.chat.id, f"{jokes[r]}")
