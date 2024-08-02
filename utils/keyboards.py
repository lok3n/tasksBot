from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.models import Users, Task


def main_menu(is_admin=False):
    builder = InlineKeyboardBuilder()
    builder.button(text='📋 Мои задачи', callback_data='my_tasks')
    if is_admin:
        builder.button(text='⭐ Все задачи', callback_data='admin_tasks')
    return builder.adjust(2).as_markup()


def show_users(users: list[Users]):
    builder = InlineKeyboardBuilder()
    for user in users:
        builder.button(text=f'👤 {user.name}', callback_data=f'user_show {user}')
    builder.button(text='↩️ Назад', callback_data='start')
    return builder.adjust(1).as_markup()


def show_tasks(tasks: list[Task], user: Users):
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.button(text=f'{"🟢" if task.status else "🔴"} {task.name}', callback_data=f'task_show {task}')
    builder.button(text='➕ Добавить задачу', callback_data=f'add_task {user}')
    builder.button(text='↩️ Назад', callback_data='start')
    return builder.adjust(1).as_markup()


def edit_task(task: Task):
    builder = InlineKeyboardBuilder()
    builder.button(text='🆔 Переименовать', callback_data=f'task_edit name {task}')
    builder.button(text='📝 Изменить задачу', callback_data=f'task_edit task {task}')
    builder.button(text='📅 Поменять срок', callback_data=f'task_edit date {task}')
    builder.button(text='🗑️ Удалить задачу', callback_data=f'task_delete {task}')
    builder.button(text='↩️ Назад', callback_data=f'user_show {task.user}')
    return builder.adjust(2).as_markup()


def my_tasks(tasks: list[Task]):
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.button(text=f'{"🟢" if task.status else "🔴"} {task.name}', callback_data=f'my_task_show {task}')
    builder.button(text='↩️ Назад', callback_data='start')
    return builder.adjust(1).as_markup()


def change_status(task: Task):
    builder = InlineKeyboardBuilder()
    builder.button(text='🔄 Поменять статус', callback_data=f'change_status {task}')
    builder.button(text='↩️ Назад', callback_data='my_tasks')
    return builder.adjust(1).as_markup()


def back_btn(callback, name='↩️ Назад'):
    return InlineKeyboardBuilder().button(text=name, callback_data=callback).as_markup()
