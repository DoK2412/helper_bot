import asyncio
import logging
import datetime
import requests



from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message

from sqlmodel import Session, select
from database.connection_db import engin

from database.sql_requests import Users, Notes




from setting import bot_token, bot_token_waiting

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    while True:
        await asyncio.sleep(1)
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == '15:15:00':
            date = datetime.datetime.now().date()
            with Session(engin) as session:
                user_note = session.exec(select(Notes).where(Notes.date == str(date))).all()
                if len(user_note) > 0:
                    one_return = True
                    for i in user_note:

                        user_id = session.exec(select(Users.telegram_id).where(Users.id == i.user_id)).one()
                        if one_return:
                            messeg = f'Доброе утро.\nЗаметки на {i.date}'
                            url = f"https://api.telegram.org/bot{bot_token_waiting}/sendMessage?chat_id={user_id}&text={messeg}"
                            requests.get(url).json()
                            one_return = False
                        messeg = i.note
                        url = f"https://api.telegram.org/bot{bot_token_waiting}/sendMessage?chat_id={user_id}&text={messeg}"
                        requests.get(url).json()
                    one_return = True


async def main():
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

