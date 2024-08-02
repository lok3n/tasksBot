import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv
import asyncio
import os
import logging
from handlers import *
from utils.models import Users, Task

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
dp.include_routers(start_router, admin_tasks_router, my_tasks_router)


async def main():
    tables = [Users, Task]
    for i in tables:
        if not i.table_exists():
            i.create_table()
    print('started')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # logging.basicConfig(filename='logs.log', level=logging.INFO)
    await bot.set_my_commands([BotCommand(command='start', description='Главное меню')])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
