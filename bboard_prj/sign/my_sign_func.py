import datetime
import sqlite3
from pathlib import Path
from django.core.mail import send_mail
from django.conf import settings

def insert_confirmation_code(code_confirm, code_type, confirmation_email):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        sqlite_connection = sqlite3.connect(BASE_DIR/'db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_query = f'INSERT INTO bboardapp_codeconfirmation (code_confirmation, code_confirmation_datetime, code_confirmation_type, code_confirmation_email) VALUES(?, ?, ?, ?)'
        data_tuple = (code_confirm, datetime.datetime.now(), code_type, confirmation_email)

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def select_confirmation_code(c_email):
    code_confirm = [-500]

    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        sqlite_connection = sqlite3.connect(BASE_DIR/'db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        # sqlite_select_query = 'SELECT * from bboardapp_codeconfirmation'
        # cursor.execute(sqlite_select_query)
        sqlite_select_query = 'SELECT code_confirmation from bboardapp_codeconfirmation WHERE code_confirmation_email = ? ORDER BY code_confirmation_datetime DESC LIMIT 1'
        data_tuple = (c_email,)
        cursor.execute(sqlite_select_query, data_tuple)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        code_confirm = records[0]
        print('code_confirm = ', code_confirm[0])
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        return code_confirm[0]
# insert_confirmation_code('234555', 1, 'confirmation@email.ru', 3)
# select_confirmation_code('1@2.3')


def send_conf_code(cc_code, cc_email):
    send_mail(
        subject='Регистрация на сайте MMORPG',  # Категория и дата записи будут в теме для удобства
        message=f'Код подтверждения регистрации: {cc_code}',  # сообщение с кратким описанием
        from_email=settings.EMAIL_HOST_USER,  # здесь указываете почту, с которой будете отправлять
        recipient_list=[cc_email]  # здесь список получателей
    )
# send_conf_code(159, 'k@yandex.ru')
