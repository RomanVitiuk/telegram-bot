from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types

import skeleton
from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
handler = skeleton


@dp.message_handler(commands=['start'])
async def start_information(message: types.Message):
    await message.reply(handler.UserInterfaceOfGeneralInfo.start())


@dp.message_handler(commands=['help'])
async def help_information(message: types.Message):
    await message.reply(handler.UserInterfaceOfGeneralInfo.help_info)


@dp.message_handler(commands=['statistic'])
async def statistic_information(message: types.Message):
    try:
        await message.reply(handler.UserInterfaceOfGeneralInfo.statistics(
            user_id=message.from_user.id
        ))
    except Exception as ex:
        await message.reply(f'''Sorry {message.from_user.first_name}, no information about you!\n 
Apparently you are a new user!\n 
Get start using this bot or go to the /help option!''')


@dp.message_handler()
async def echo(message: types.Message):
    try:
        day_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        current_user = handler.InfoHandler(
            user_id=user_id,
            user_name=user_name,
            measure_value=message.text,
            day=day_time
        )
        if handler.is_first_time_user(user_id=user_id):
            current_user.initial_new_user()
        if handler.is_record_in_db(user_id=user_id, day=day_time):
            current_user.add_new_record()
        current_user.add_measure()
        await message.reply(handler.UserInterfaceOfGeneralInfo.result(
            user_id=user_id,
            user_name=user_name,
            current_day=day_time
        ))
    except Exception as ex:
        await message.reply('Pleas enter value as integer')


if __name__ == "__main__":
    skeleton.initial_db()
    executor.start_polling(dp, skip_updates=True)
