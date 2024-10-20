import json

from config import TOKEN

import app.keyboard as kb
from app.middlewares import Take_message
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


router = Router()
bot = Bot(token=TOKEN)
storage = MemoryStorage()
router.message.outer_middleware(Take_message())

DATA_FILE = 'users.json'

class Registr(StatesGroup):
    name = State()
    age = State()
    number = State()

class TestStates(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    summary = State()

questions = [
    {
        "question": "Какой аспект IT вам интересен?",
        "answers": [("Разработка программ", "dev"), ("Работа с данными", "data"), ("Администрирование систем", "sysadmin")]
    },
    {
        "question": "Какой формат работы вам больше подходит?",
        "answers": [("Удалённая работа", "remote"), ("Работа в офисе", "office"), ("Смешанный формат", "mixed")]
    },
    {
        "question": "Какой уровень технических знаний у вас?",
        "answers": [("Новичок", "beginner"), ("Средний", "intermediate"), ("Продвинутый", "advanced")]
    }
]

def save_user_registr(user_id, user_data):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
     
    if user_id in data:
        data[user_id].update(user_data)
    else:
        data[user_id] = user_data

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def question_kb(answers):
    keyboard = InlineKeyboardBuilder()
    for text, callback_data in answers:
        keyboard.button(text=text, callback_data=callback_data)
    keyboard.adjust(1)
    return keyboard.as_markup()

@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer(
        'Привет! Выбери действиe',
        reply_markup=kb.main)

@router.message(Command(commands=['registr']))
async def start_registr(message: Message, state: FSMContext):
    bot_message = await message.answer('Введите имя')
    
    await state.update_data(bot_message_id = bot_message.message_id)

    await state.set_state(Registr.name)
    await message.delete()

@router.message(Registr.name)
async def process_nmame(message: Message, state: FSMContext):
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')

    if bot_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    
    await message.delete()

    await state.update_data(name=message.text)

    bot_message = await message.answer('Сколько вам лет?')
    await state.update_data(bot_message_id=bot_message.message_id)

    await state.set_state(Registr.age)

@router.message(Registr.age)
async def process_age(message: Message, state: FSMContext):
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    if bot_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    
    await message.delete()

    await state.update_data(age=message.text)

    bot_message = await message.answer('Отправьте номер телефона', reply_markup=kb.number)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(Registr.number)

@router.message(Registr.number)
async def pocess_city(message: Message, state: FSMContext):
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')

    if bot_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    
    await message.delete()
    
    phone_number = message.contact.phone_number
    
    await state.update_data(number=phone_number)

    user_data = await state.get_data()

    user_info = {
        'name': user_data['name'],
        'age': user_data['age'],
        'number': user_data['number']
    }

    save_user_registr(str(message.from_user.id), user_info)

    await message.answer('Регистрация завершена!', reply_markup=kb.start_test)
    
    await state.clear()

@router.message(F.text == 'Регистрация')
async def connector(message: Message):
    await message.answer('Введите /registr')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')

@router.callback_query(F.data == 'test')
async def start_test(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Начало профориентационного теста.')
    bot_message = await callback.message.answer(questions[0]['question'], reply_markup=question_kb(questions[0]['answers']))
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(TestStates.question1)

@router.callback_query(TestStates.question1)
async def main_question_1(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(q1=answer)
    
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=bot_message_id,
        text=questions[1]['question'],
        reply_markup=question_kb(questions[1]['answers'])
    )
    
    await state.set_state(TestStates.question2)
    
@router.callback_query(TestStates.question2)
async def main_question_2(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(q2=answer)
    
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=bot_message_id,
        text=questions[2]['question'],
        reply_markup=question_kb(questions[2]['answers'])
    )
 
    await state.set_state(TestStates.question3)

@router.callback_query(TestStates.question3)
async def main_question_3(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(q3=answer)
    
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    user_data = await state.get_data()
    
    result_text = (
        f'Тест завершен! Вот ваши ответы: \n'
        f'1. {questions[0]["question"]} - {user_data['q1']} \n'
        f'2. {questions[1]["question"]} - {user_data['q2']} \n'
        f'3. {questions[2]["question"]} - {user_data['q3']} \n'
    )
    
    test_result = {
        'test_results':{
            'question1': user_data['q1'],
            'question2': user_data['q2'],
            'question3': user_data['q3']
        }
    }
    
    save_user_registr(str(callback.from_user.id), test_result)
    
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=bot_message_id,
        text=result_text
    )
    
    await state.clear()
