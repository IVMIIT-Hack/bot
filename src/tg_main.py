#!seperaokeq/bin/python
from aiogram import Bot, Dispatcher, executor, types            #Telegram API
from aiogram.contrib.fsm_storage.memory import MemoryStorage    #Telegram API
from aiogram.dispatcher import FSMContext                       #Telegram API
from aiogram.dispatcher.filters import Text                     #Telegram API
from aiogram.dispatcher.filters.state import State, StatesGroup #Telegram API

import sys
sys.path.append(r"C:/Users/seper/Documents/IVMIIT-Hack/bot")

from src.tg_message import help_message, start_message, uuid_add_message
from src.tg_database import DatabaseStorageTelegramUsersData   
from src.core import token_telegram_api, db_user_file_path
from src.database import DataBaseAbiturents, DataBaseAbiturentsExport

bot = Bot(token = token_telegram_api);
dp = Dispatcher(bot); 
dba_tg_user_data = DatabaseStorageTelegramUsersData(db_user_file_path)

class Reg(StatesGroup):
    uuid = State()  # Will be represented in storage as 'Form:name'# Will be represented in storage as 'Form:gender'


@dp.message_handler(commands="start")
async def kpfu_bot_start(message: types.Message):
    await message.answer(start_message);
    if dba_tg_user_data.exists_user_db(message.from_user.id):
        await message.answer("Успешно восстановлена сессия!")
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Регистрация"]
        keyboard.add(*buttons)
        await message.answer("Вы не авторизованы! Зарегистрироваться?", reply_markup=keyboard)


@dp.message_handler(text="Регистрация")
async def kpfu_bot_auth(message: types.Message):
    await Reg.uuid.set()
    await message.answer(uuid_add_message)

@dp.message_handler(commands='reg')
@dp.message_handler(state=Reg.uuid)
async def kpfu_bot_auth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dba_tg_user_data.add_user_db(message.from_user.id, message.text, "null")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Меню"]
        keyboard.add(*buttons)
        await message.answer("Открыть меню?", reply_markup=keyboard)

@dp.message_handler(text="Меню" or "Отмена" or "Назад")
@dp.message_handler(state=Reg.uuid)
async def kpfu_bot_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Настройки", "Показать рейтинг"]
    keyboard.add(*buttons)
    await message.answer(help_message, reply_markup=keyboard)

@dp.message_handler(text="Настройки")
async def kpfu_bot_settings(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Уведомления", "Сброс СНИЛС", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Настройки:", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)