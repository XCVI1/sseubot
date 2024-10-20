import logging, asyncio

from aiogram import Bot, Dispatcher, F
from config import TOKEN

from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

def reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Кнопка 1'), KeyboardButton(text='Кнопка 2')],
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer(
        'Привет! Выбери действи',
        reply_markup=reply_keyboard()
    )


@dp.message(Command(commands=['registration']))
async def start_registration(message: Message):
    await message.answer('Напиши свое ФИО', reply_markup=bot_keyboard())

    await message.delete()

@dp.message()
async def handle_message(message: Message):
    if message.text == 'Кнопка 1':
        await message.answer('вы нажали кнопку 1')
    elif message.text == 'Кнопка 2':
        await message.answer('Вы нажали кнопку 2')
    else:
        await message.answer('Выберите кнопку')

def bot_keyboard(button1_text='Кнопка 1', button2_text='Кнопка 2', show_button1=True, show_button2=True):
    keyboard = InlineKeyboardBuilder()

    if show_button1:
        keyboard.button(text=button1_text, callback_data='button1')
    if show_button2:
        keyboard.button(text=button2_text, callback_data='button2')

    keyboard.adjust(2)
    return keyboard.as_markup()

@dp.callback_query(F.data == 'button1')
async def button1_clicked(callback: CallbackQuery):
    await callback.message.edit_text('Ты нажал кнопку 1')
    await callback.message.edit_reply_markup(reply_markup=bot_keyboard(show_button1=False))

@dp.callback_query(F.data == 'button2')
async def button2_clicked(callback: CallbackQuery):
    await callback.message.edit_text('Ты нажал кнопку 2')
    await callback.message.edit_reply_markup(reply_markup=bot_keyboard(show_button2=False))




async def main():
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(start_registration, Command(commands=['registration']))
    dp.message.register(handle_message)
    dp.callback_query.register(button1_clicked, F.data == 'button1')
    dp.callback_query.register(button2_clicked, F.data == 'button2')

    

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
