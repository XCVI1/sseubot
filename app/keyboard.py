from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Регистрация')],
], 
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню')

start_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пройти тест', callback_data='test')
]])

number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить номер телефона', request_contact=True)]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

