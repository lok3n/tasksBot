from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv
import asyncio
import os
import logging
from handlers import *
from utils.models import Users, Task
from utils.notify import notify_users
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
dp.include_routers(start_router, admin_tasks_router, my_tasks_router)


async def main():
    tables = [Users, Task]
    for i in tables:
        if not i.table_exists():
            i.create_table()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_users, 'cron', hour=12, kwargs={'bot': bot})
    scheduler.start()

    print('started')
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    await bot.set_my_commands([BotCommand(command='start', description='Главное меню')])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
