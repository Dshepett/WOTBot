from aiogram.dispatcher.storage import FSMContext
from states import ChooseCharacteristics
from aiogram import types
from aiogram.types.input_file import InputFile

from loader import dp, db


@dp.message_handler(commands=['find_tank'])
async def ask_health(message: types.Message):
    await message.answer("Введите прочность танка")
    await ChooseCharacteristics.Base.set()


@dp.message_handler(commands=['cancel'], state=ChooseCharacteristics.all_states)
async def cancel_search(message: types.Message, state: FSMContext):
    await message.answer("Отмена поиска....\n\nВведите /find_tank для повторного поиска танка.")
    await state.finish()


@dp.message_handler(state=ChooseCharacteristics.Base)
async def ask_damage(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["health"] = message.text
        await message.answer(f"Введите урон танка")
        await ChooseCharacteristics.ChoseHealth.set()
    else:
        await message.answer(f"Некорректное значение, повторите попытку.")


@dp.message_handler(state=ChooseCharacteristics.ChoseHealth)
async def ask_armor(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["damage"] = message.text
        await message.answer(f"Введите уровень бронирования")
        await ChooseCharacteristics.ChoseDamage.set()
    else:
        await message.answer(f"Некорректное значение, повторите попытку.")


@dp.message_handler(state=ChooseCharacteristics.ChoseDamage)
async def ask_speed(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["armor"] = message.text
        await message.answer(f"Введите скорость танка")
        await ChooseCharacteristics.ChoseArmor.set()
    else:
        await message.answer(f"Некорректное значение, повторите попытку.")


@dp.message_handler(state=ChooseCharacteristics.ChoseArmor)
async def ask_stealth(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["speed"] = message.text
        await message.answer(f"Выберите уровень маскировки танка (в процентах)")
        await ChooseCharacteristics.ChoseSpeed.set()
    else:
        await message.answer(f"Некорректное значение, повторите попытку.")


@dp.message_handler(state=ChooseCharacteristics.ChoseSpeed)
async def find_tanks(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data["stealth"] = message.text
            result = db.find_tank((data["health"], data["health"], data["damage"], data["damage"], data["armor"],
                                  data["armor"], data["speed"], data["speed"], data["stealth"], data["stealth"]))
        if len(result) == 0:
            await message.answer("К сожалению, танков с такими характеристиками нет.")
        else:
            for i in result:
                description = f"<b>Название танка:</b> {i[0]}\n<b>Страна-производитель:</b> {i[1]}\n<b>Прочность танка:</b> {i[2]}\
                    \n<b>Урон в минуту:</b> {i[3]}\n<b>Бронирование<i>(мм)</i>:</b> {i[4]}\n<b>Скорость<i>(км\ч)</i>:</b> {i[5]}\n<b>Маскировка:</b> {i[6]}%"
                photo = InputFile(
                    path_or_bytesio=f"data/tanks_photos/{i[0]}.png")
                await message.answer_photo(photo=photo, caption=description)
        await message.answer(f"Для повторного поиска танка введите /find_tank")
        await state.finish()
    else:
        await message.answer(f"Некорректное значение, повторите попытку.")
