from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from utils.models import Users, Task
from utils.keyboards import my_tasks, back_btn, change_status

my_tasks_router = Router()


@my_tasks_router.callback_query(F.data == 'my_tasks')
async def my_tasks_handler(callback: CallbackQuery):
    user = Users.get_or_none(Users.user_id == callback.from_user.id)
    await callback.message.edit_text(
        '📋 Ниже перечислены Ваши задачи, нажмите на любую, чтобы получить больше информации',
        reply_markup=my_tasks(Task.select().where(Task.user == user)))


@my_tasks_router.callback_query(F.data.startswith('my_task_show'))
async def my_task_show_handler(callback: CallbackQuery):
    task = Task.get_by_id(int(callback.data.split()[1]))
    text = f'''👤 <b>Исполнитель</b>: <i>{task.user.name}</i>
🆔 <b>Название задачи:</b> <i>{task.name}</i>
📝 <b>Задача:</b> <i>{task.text}</i>
📅 <b>Срок:</b> <i>{task.date}</i>
{"🟢" if task.status else "🔴"} <b>Статус:</b> <i>{"выполнена" if task.status else "не выполнена"}</i>'''
    await callback.message.edit_text(text, reply_markup=change_status(task), parse_mode="HTML")


@my_tasks_router.callback_query(F.data.startswith('change_status'))
async def change_status_handler(callback: CallbackQuery):
    task = Task.get_by_id(int(callback.data.split()[1]))
    task.status = 1 if not task.status else 0
    task.save()
    await callback.message.edit_text(f'✅ Вы успешно поменяли статус для задачи {task.name}',
                                     reply_markup=back_btn(f'my_task_show {task}'))
