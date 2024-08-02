from peewee import SqliteDatabase, Model, TextField, IntegerField, ForeignKeyField

db = SqliteDatabase('database.db')


class Users(Model):
    user_id = IntegerField()
    name = TextField()

    class Meta:
        database = db


class Task(Model):
    user = ForeignKeyField(model=Users)
    name = TextField(default='Задача 1')
    text = TextField(default='Задача 1')
    date = TextField(default='1 день')
    status = IntegerField(default=0)

    class Meta:
        database = db
