
import os
import types
from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

get_cat_button = InlineKeyboardButton(
    text='Мяу!',
    callback_data='get_cat_button_pressed')

keyboard = InlineKeyboardMarkup(inline_keyboard=[[get_cat_button]])

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Мурр?',
        reply_markup=keyboard)
    

@dp.callback_query(F.data == 'get_cat_button_pressed')
async def get_cat_command(callback: CallbackQuery):
    response = requests.get(API_CATS_URL)
    if response.status_code ==200:
        await callback.message.answer_photo(photo=response.json()[0]["url"])
        await callback.message.answer(
        text='Мурр!',
        reply_markup=keyboard)
    else:
        await callback.message.answer(
        text='Все котятки спят, попробуй еще раз',
        reply_markup=keyboard)

if __name__ == '__main__':
    dp.run_polling(bot)