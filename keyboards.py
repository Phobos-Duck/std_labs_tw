from telebot import types

def make_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton("/start")
    bt2 = types.KeyboardButton("/help")
    bt3 = types.KeyboardButton("/settings")
    bt4 = types.KeyboardButton("/weather")
    bt5 = types.KeyboardButton("/news")
    bt6 = types.KeyboardButton("/joke")
    markup.add(bt1, bt2, bt3)
    markup.add(bt4, bt5)
    markup.add(bt6)
    return markup

def keyboard_news():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton("политика")
    bt2 = types.KeyboardButton("спорт")
    bt3 = types.KeyboardButton("технологии")
    bt4 = types.KeyboardButton("бизнес")
    bt5 = types.KeyboardButton("образование")
    bt6 = types.KeyboardButton("главные")
    bt7 = types.KeyboardButton('здоровье')
    bt8 = types.KeyboardButton('наука')
    markup.add(bt1, bt2, bt4)
    markup.add(bt3, bt5)
    markup.add(bt6, bt7, bt8)
    return markup

def list_news():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton("Следующая")
    bt2 = types.KeyboardButton("На этом закончим")
    markup.add(bt1)
    markup.add(bt2)
    return markup

def keyboard_setting():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton("Оба")
    bt2 = types.KeyboardButton("Только город")
    bt3 = types.KeyboardButton("Только категорию")
    bt4 = types.KeyboardButton("Удалить все настройки")
    markup.add(bt1)
    markup.add(bt2, bt3)
    markup.add(bt4)
    return markup