import sqlite3
from aiogram.types import message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


connect = sqlite3.connect('data')
cursor = connect.cursor()

#create table

'''TABLE USERS'''

cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER)""")
connect.commit()

def user_exists(id):
    result = cursor.execute("SELECT 'id' FROM 'users' WHERE id = ?", (id,))
    return bool(len(result.fetchall()))

def select_all_users(id):
    cursor.execute("SELECT * FROM 'users'").fetchall()
    connect.commit()


'''TABLE ADMINS'''
cursor.execute("""CREATE TABLE IF NOT EXISTS admins(admin_id TEXT)""")
connect.commit()

def admins():
    admins = cursor.execute("SELECT admin_id FROM 'admins'").fetchall()
    connect.commit()
    return admins

def admin_exists(id):
    result = cursor.execute("SELECT 'admin_id' FROM 'admins' WHERE admin_id = ?", (id,))
    return bool(len(result.fetchall()))

'''TABLE ARHI'''
cursor.execute("""CREATE TABLE IF NOT EXISTS archive(name TEXT,
    url TEXT)""")
connect.commit()

def movies():
    movies = cursor.execute("SELECT * FROM 'archive'").fetchall()
    connect.commit()
    return movies


'''TABLE CHANNELS'''
cursor.execute("""CREATE TABLE IF NOT EXISTS channels(chat_id INTEGER,
    url TEXT)""")
connect.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS channels_without_verif(url TEXT)""")
connect.commit()

def channels():
    channels = cursor.execute("SELECT * FROM 'channels'").fetchall()
    connect.commit()
    return channels

def channel():
    channel = cursor.execute("SELECT chat_id FROM 'channels'").fetchall()
    connect.commit()
    return channel

def channel_without_verif():
    channel_without_verif = cursor.execute("SELECT * FROM 'channels_without_verif'").fetchall()
    connect.commit()
    return channel_without_verif


# Your channels, empty url will not show
def channel_read():
    Keyboard = InlineKeyboardMarkup(row_width=2)
    nam_chan = 0

    for channel in channels():
        nam_chan += 1
        button = InlineKeyboardMarkup(text=f'🌄 Канал №{nam_chan}', url=channel[1])
        Keyboard.insert(button)

    for channel in channel_without_verif():
        nam_chan += 1
        button = InlineKeyboardMarkup(text=f'🌄 Канал №{nam_chan}', url=channel[0])
        Keyboard.insert(button)

    btn_check = types.InlineKeyboardButton("Подписался ✅", callback_data="checksub")
    Keyboard.row(btn_check)

    return Keyboard
    nam_chan = 0
    connect.commit()


def adm_channel_read():

    num_of_del = 0
    Keyboard = InlineKeyboardMarkup(row_width=2)


    for channel in channels():
        num_of_del += 1
        button = InlineKeyboardMarkup(text=f'📣 Канал {num_of_del}', url=channel[1])

        button_2 = InlineKeyboardMarkup(text=f'⚙️ Удалить', callback_data=f'edit {channel[1]}')
        Keyboard.row(button,button_2)

    for channel in channel_without_verif():
        num_of_del += 1
        button = InlineKeyboardMarkup(text=f'📣 Канал {num_of_del}', url=channel[0])

        button_2 = InlineKeyboardMarkup(text=f'⚙️ Удалить', callback_data=f'edit_wv {channel[0]}')
        Keyboard.row(button,button_2)



    add_ch_mur = InlineKeyboardButton(text='➕ Добавить канал 📣', callback_data="add_channel")
    Keyboard.row(add_ch_mur)
    add_ch_mur = InlineKeyboardButton(text='➕ Добавить канал 📣 (без проверки)', callback_data="add_channels_without_verif")
    Keyboard.row(add_ch_mur)

    add_back = InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
    Keyboard.row(add_back)

    num_of_del = 0
    return Keyboard

    connect.commit()




def admins_read():
 
    Keyboard = InlineKeyboardMarkup(row_width=1)
    add_admin = InlineKeyboardButton(text='➕ Добавить админа', callback_data="add_admin")
    remove = InlineKeyboardButton(text='➖ Убрать админа', callback_data="remove_admin")
    back = InlineKeyboardButton(text='⬅️ Назад', callback_data="back")


    for adm in admins():
        button_url = f'https://t.me/{adm[0]}'
        button = InlineKeyboardMarkup(text=f'👤 {adm[0]}', url=button_url)
        Keyboard.insert(button) 


    Keyboard.insert(add_admin)
    Keyboard.insert(remove)
    Keyboard.insert(back)
    return Keyboard 

    connect.commit()   


 
def sql_delete_admin(data):
    cursor.execute('DELETE FROM admins WHERE admin_id = ?;', (data,))
    connect.commit()

def sql_delete_channel(data):
    cursor.execute('DELETE FROM channels WHERE url = ?;', (data,))
    connect.commit()

def sql_delete_channel_without_verif(data):
    cursor.execute('DELETE FROM channels_without_verif WHERE url = ?;', (data,))
    connect.commit()

def update_url(data, old_url):
    cursor.execute('''UPDATE channels SET url = ? WHERE url = ?''', (data, old_url))

