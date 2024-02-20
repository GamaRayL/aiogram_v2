import os

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.register_kb import register_keyboard
from keyboards.profile_kb import profile_keyboard
from utils.database import DatabaseManager

router = Router()


@router.startup()
async def start_bot(bot: Bot):
    admin_id = os.getenv('ADMIN_ID')
    await bot.send_message(admin_id, text='Я запустил бота')


@router.message(Command('start'))
async def get_start(message: Message, bot: Bot):
    db = DatabaseManager(os.getenv('DATABASE_NAME'))
    user_id = message.from_user.id
    user = db.select_user(user_id)

    if user:
        await bot.send_message(
            message.from_user.id,
            f'👋 Здравствуйте, {user[1]}!',
            reply_markup=profile_keyboard
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f'👋 Здравствуйте, {message.from_user.username}',
            reply_markup=register_keyboard
        )
