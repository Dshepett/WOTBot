from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!"
                         f" Вас приветствует помощник <b>Tank Lover</b>.\n\nМы подберем для вас наиболее подходящий танк,"
                         f"исходя из ваших предпочтений в технических характеристиках: <i>прочность, бронирование, урон в минуту,"
                         f"скорость и маскировка.</i>\n\nДля начала работы введите /find_tank.\n\nВ случае возникших вопросов,"
                         f"пожалуйста, обращайтесь в техподдержку(@max_ksvy).")
