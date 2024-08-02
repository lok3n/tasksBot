from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from utils.models import Users, Task
from utils.keyboards import show_users, show_tasks, edit_task, back_btn

admin_tasks_router = Router()

edit_value = State()


@admin_tasks_router.callback_query(F.data == 'admin_tasks')
async def admin_tasks_handler(callback: CallbackQuery):
    await callback.message.edit_text('👥 Выберите пользователя, чьи задачи хотите просмотреть',
                                     reply_markup=show_users(Users.select()))


@admin_tasks_router.callback_query(F.data.startswith('user_show'))
async def user_show_handler(callback: CallbackQuery):
    user = Users.get_by_id(int(callback.data.split()[1]))
    tasks = Task.select().where(Task.user == user)
    await callback.message.edit_text(f'🙋‍♂️ Вы выбрали пользователя {user.name}, ниже перечислены его задачи',
                                     reply_markup=show_tasks(tasks, user))


@admin_tasks_router.callback_query(F.data.startswith('task_show'))
async def task_show_handler(callback: CallbackQuery):
    task = Task.get_by_id(int(callback.data.split()[1]))
    text = f'''👤 <b>Исполнитель</b>: <i>{task.user.name}</i>
🆔 <b>Название задачи:</b> <i>{task.name}</i>
📝 <b>Задача:</b> <i>{task.text}</i>
📅 <b>Срок:</b> <i>{task.date}</i>
{"🟢" if task.status else "🔴"} <b>Статус:</b> <i>{"выполнена" if task.status else "не выполнена"}</i>'''
    await callback.message.edit_text(text, reply_markup=edit_task(task), parse_mode="HTML")


@admin_tasks_router.callback_query(F.data.startswith('add_task'))
async def add_task_handler(callback: CallbackQuery):
    user = Users.get_by_id(int(callback.data.split()[1]))
    task = Task.create(user=user)
    await callback.message.edit_text(f'✅ Вы успешно создали задачу пользователю {user.name}!\n'
                                     f'📝 Нажмите «Показать задачу», чтобы отобразить её',
                                     reply_markup=back_btn(f'task_show {task}', '📝 Показать задачу'))
    await callback.bot.send_message(user.user_id, '📝 Администратор добавил Вам задачу')


@admin_tasks_router.callback_query(F.data.startswith('task_edit'))
async def task_edit_handler(callback: CallbackQuery, state: FSMContext):
    cmd, do, task_id = callback.data.split()
    await state.update_data(do=do, past_msg_id=callback.message.message_id, task=task_id)
    await state.set_state(edit_value)
    await callback.message.edit_text('👉 Введите новое значение',
                                     reply_markup=back_btn(f'task_show {task_id}'))


@admin_tasks_router.message(edit_value)
async def edit_value_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    task = Task.get_by_id(int(data['task']))
    await message.delete()
    await state.clear()
    if data['do'] == 'name':
        task.name = message.text
    elif data['do'] == 'task':
        task.text = message.text
    elif data['do'] == 'date':
        task.date = message.text
    task.save()
    await message.bot.edit_message_text('✅ Вы успешно поменяли значение для задачи!',
                                        chat_id=message.chat.id, message_id=data['past_msg_id'],
                                        reply_markup=back_btn(f'task_show {task}'))


@admin_tasks_router.callback_query(F.data.startswith('task_delete'))
async def task_delete_handler(callback: CallbackQuery):
    task = Task.get_by_id(int(callback.data.split()[1]))
    task.delete_instance()
    await callback.message.edit_text(f'✅ Вы успешно удалили задачу <b>{task.name}</b> у пользователя '
                                     f'<b>{task.user.name}</b>!',
                                     reply_markup=back_btn(f'user_show {task.user}'),
                                     parse_mode="HTML")
    await callback.bot.send_message(task.user.user_id,
                                    f'📝 Администратор удалил у Вас задачу <b>{task.name}</b>',
                                    parse_mode="HTML")
