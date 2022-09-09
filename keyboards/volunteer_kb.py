from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

noPatronymicBtn = KeyboardButton('Нет')

noKbMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

noKbMarkup.add(noPatronymicBtn)

