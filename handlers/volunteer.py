from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
import validators
import re
from aiogram.dispatcher.filters import Text
from db import s, add_volunteer, check_volunteer
from create_bot import dp, bot

from aiogram.types import ReplyKeyboardRemove
from keyboards import noKbMarkup

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# from keyboards import kb_volunteer


# noPatronymicBtn = InlineKeyboardButton(text='Нет', )


def check_FIO(text):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for num in numbers:
        if text.find(num) != -1:
            print(num)
            print('найдена цифра')
            return -1

    return 0


class FSMClient(StatesGroup):
    # FIO = State()
    last_name = State()
    dBirth = State()
    first_name = State()
    patronymic = State()
    tel = State()
    VKLink = State()
    mail = State()


# @dp.message_handler(commands='start', state=None)
async def cm_start(message: types.Message):
    volunteer = check_volunteer(message.from_user.id)
    # print(type(volunteer))
    if not(volunteer):
        await FSMClient.last_name.set()
        await message.answer('Необходимо зарегистрироваться!\nВведи свою фамилию')
    else:
        await message.answer(f'Привет, {volunteer.first_name}!\nСписок действующих мероприятий')

        # Вывод списка действующих мероприятий

    # print(message.from_user.id)


# Выход из состояний
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отменено')


# @dp.message_handler(state=FSMClient.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    print('last name')

    if check_FIO(message.text) == -1:
        await message.reply('Напиши свою фамилию')
        return

    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['last_name'] = message.text
        # data['last_name'] = surname
        # data['patronymic'] = patronymic

    # await FSMClient.next()
    await FSMClient.first_name.set()
    # await message.answer('Напиши год рождения в следующем формате: дд.мм.гггг')
    await message.answer('Напиши свое полное имя')

    # @dp.message_handler(state=FSMClient.patronymic)


# @dp.message_handler(state=FSMClient.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    print('first name')

    if check_FIO(message.text) == -1:
        await message.reply('Напиши свое полное имя')
        return

    async with state.proxy() as data:
        data['first_name'] = message.text

    await FSMClient.patronymic.set()
    # await message.answer('Напиши год рождения в следующем формате: дд.мм.гггг')
    # keyboard = ReplyKeyboardMarkup(row_width=1).add(
    #     InlineKeyboardButton(text='Нет'))

    await message.answer('Напиши свое отчество (при наличии)', reply_markup=noKbMarkup)

# @dp.message_handler(state=FSMClient.first_name)


# @dp.callback_query_handler(text='Нет отчества', state=FSMClient.patronymic)
# async def no_patronymic(callback: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         # data['user_id'] = message.from_user.id
#         data['patronymic'] = 'Нет'
#         await FSMClient.dBirth.set()
#         await bot.send_message(data['user_id'], 'Напиши год рождения в следующем формате: дд.мм.гггг')


async def process_patronymic(message: types.Message, state: FSMContext):
    print('patronymic')

    if check_FIO(message.text) == -1:
        await message.reply('Напиши свое отчество', reply_markup=noKbMarkup)
        return

    async with state.proxy() as data:
        # data['user_id'] = message.from_user.id
        data['patronymic'] = message.text
        # data['last_name'] = surname
        # data['patronymic'] = patronymic

    # await FSMClient.next()
    await FSMClient.dBirth.set()
    await message.answer('Напиши год рождения в следующем формате: дд.мм.гггг', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=FSMClient.dBirth)


async def process_dBirth(message: types.Message, state: FSMContext):
    print('dbirth')

    # Валидация даты рождения
    try:
        valid_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        print('Invalid date!')
        await message.reply('Формат ввода даты рождения: дд.мм.гггг')
        return

    async with state.proxy() as data:
        data['birth_date'] = datetime.strptime(message.text, "%d.%m.%Y")

    # await FSMClient.next()
    await FSMClient.tel.set()
    await message.answer('Введи номер телефона')


# @dp.message_handler(state=FSMClient.tel)
async def process_tel(message: types.Message, state: FSMContext):
    print('tel')

    # Валидация номера телефона
    result = re.match(
        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', message.text)
    if not(result):
        await message.answer('Неверный формат номера телефона\nВведи номер телефона в следующем формате: 89999999999')
        return

    async with state.proxy() as data:
        data['tel'] = message.text

    # await FSMClient.next()
    await FSMClient.VKLink.set()
    await message.answer('Введи ссылку на ВК')


# @dp.message_handler(state=FSMClient.VKLink)
async def process_VKLink(message: types.Message, state: FSMContext):
    print('VkLink')

    # Валидация ссылки на Вк
    if not validators.url(message.text):
        if not validators.url('https://' + message.text):
            await message.reply('Введите ссылку в формате: vk.com/<Ваш ID>')
            return

    async with state.proxy() as data:
        data['VKLink'] = message.text

    # await FSMClient.next()
    await FSMClient.mail.set()
    await message.answer('Введи электронную почту', reply_markup=noKbMarkup)


# @dp.message_handler(state=FSMClient.mail)
async def process_mail(message: types.Message, state: FSMContext):
    print('mail')

    # Валидация электронной почты
    if not validators.email(message.text) and message.text != 'Нет':
        await message.reply('Необходимо ввести почту в формате your_mail@mail.ru', reply_markup=noKbMarkup)
        return

    async with state.proxy() as data:
        data['mail'] = message.text

    if await add_volunteer(state) != 0:
        message.answer('Что-то полшло не так')
        return

    await message.answer(
        'Регистрация прошла успешно\nВыбери интересующее тебя мероприятие (coming soon...)')

    # await FSMClient.next()
    await state.finish()

    await message.answer(data.as_dict(), reply_markup=ReplyKeyboardRemove())


def registerHandlersClient(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='start')
    dp.register_message_handler(process_first_name, state=FSMClient.first_name)
    dp.register_message_handler(process_last_name, state=FSMClient.last_name)
    dp.register_message_handler(process_patronymic, state=FSMClient.patronymic)
    dp.register_message_handler(process_dBirth, state=FSMClient.dBirth)
    dp.register_message_handler(process_tel, state=FSMClient.tel)
    dp.register_message_handler(process_VKLink, state=FSMClient.VKLink)
    dp.register_message_handler(process_mail, state=FSMClient.mail)
