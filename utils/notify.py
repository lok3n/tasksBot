from aiogram import Bot
from utils.models import Users
from utils.keyboards import main_menu


async def notify_users(bot: Bot):
    for user in Users:
        await bot.send_message(user.user_id, 'Привет! Ты помнишь про свои задачи?\n'
                                             'Просмотри их, кликнув по кнопке <b>Мои задачи</b>',
                               reply_markup=main_menu(False),
                               parse_mode="HTML")
