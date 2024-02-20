from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

profile_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Профиль'
        )
    ]
],
    resize_keyboard=True,
    one_time_keyboard=True,
)
