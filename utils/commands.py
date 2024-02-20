from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def send_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запускаем бота'
        ),
        BotCommand(
            command='help',
            description='Помощь в работе с ботом'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
