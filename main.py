import logging
import os

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from utils.commands import send_commands
from handlers import start_handler, register_handler

load_dotenv()
logging.basicConfig(level=logging.INFO)


async def start():
    token = os.getenv('TOKEN')

    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(start_handler.router, register_handler.router)

    await send_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
