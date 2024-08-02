import os

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.models import Users
from utils.keyboards import main_menu

start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: Message):
    user = Users.get_or_none(Users.user_id == message.from_user.id)
    if not user:
        user = Users.create(user_id=message.from_user.id,
                            name=message.from_user.full_name)
    admins = os.getenv('ADMINS').split(',')
    await message.answer(f'👋 Привет, {message.from_user.full_name}!'
                         f'🤖 Я бот-планировщик, помогу с распределением задач, жми «Мои задачи», чтобы '
                         f'посмотреть на свои задачи',
                         reply_markup=main_menu(str(message.from_user.id) in admins))


@start_router.callback_query(F.data == 'start')
async def start_handler_cb(callback: CallbackQuery):
    admins = os.getenv('ADMINS').split(',')
    await callback.message.edit_text(f'👋 Привет, {callback.from_user.full_name}!'
                                     f'🤖 Я бот-планировщик, помогу с распределением задач, жми «Мои задачи», чтобы '
                                     f'посмотреть на свои задачи',
                                     reply_markup=main_menu(str(callback.from_user.id) in admins))
