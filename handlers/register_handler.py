import os

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold

from state.register_state import RegisterState
from utils.database import DatabaseManager
from utils.validators import cyrillic_check

router = Router()


@router.message(F.text.capitalize() == 'Начать регистрацию')
async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = DatabaseManager(os.getenv('DATABASE_NAME'))
    user_id = message.from_user.id
    user = db.select_user(user_id)

    if user:
        await bot.send_message(user_id, f'Вы уже зарегестрированы как {user[1]} {user[2]}')
    else:
        await bot.send_message(user_id, '📝 Ваше имя?')
        await state.set_state(RegisterState.regFirstName)


@router.message(RegisterState.regFirstName)
async def register_first_name(message: Message, state: FSMContext, bot: Bot):
    if cyrillic_check(message.text):
        await bot.send_message(message.from_user.id, '📝 Ваша фамилия?')
        await state.update_data(regFirstName=message.text)
        await state.set_state(RegisterState.regLastName)
    else:
        await bot.send_message(
            message.from_user.id,
            'Укажите имя кириллицей и с заглавной буквы!'
        )


@router.message(RegisterState.regLastName)
async def register_last_name(message: Message, state: FSMContext, bot: Bot):
    if cyrillic_check(message.text):
        await state.update_data(regLastName=message.text)
        user_id = message.from_user.id
        reg_data = await state.get_data()
        reg_first_name = reg_data.get('regFirstName')
        reg_last_name = reg_data.get('regLastName')
        content = Text(
            'Приятно познакомиться, ',
            Bold(reg_first_name), ' ', Bold(reg_last_name), '!\n\n',
            '🎉🎉🎉 Регистрация завершена! 🎉🎉🎉'
        )

        await bot.send_message(user_id, **content.as_kwargs())
        db_manager = DatabaseManager(os.getenv('DATABASE_NAME'))
        db_manager.create_user(first_name=reg_first_name, last_name=reg_last_name, tg_id=user_id)
        await state.clear()

    else:
        await bot.send_message(
            message.from_user.id,
            'Укажите фамилию кириллицей и с заглавной буквы!'
        )
