from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from data_base import db

#buttons

#main
#main_btn = InlineKeyboardButton(text='Смотреть ▶️', callback_data="checksub")
btn67 = InlineKeyboardButton(text='% Скидки', url = "https://t.me/+cz9376-VGKkzMWUy")
btn68 = InlineKeyboardButton(text='❄️ Зимний ассортимент', url = "https://t.me/+cz9376-VGKkzMWUy")
btn70 = InlineKeyboardButton(text='🆕 NEW DROP', url = "https://t.me/+cz9376-VGKkzMWUy")
btn69 = InlineKeyboardButton(text='🔎 Весь ассортимент', url = "https://t.me/+cz9376-VGKkzMWUy")
Start_btn = InlineKeyboardMarkup(row_width=1)
#Start_btn.insert(main_btn)
Start_btn.insert(btn67)
Start_btn.insert(btn68)
Start_btn.insert(btn69)
Start_btn.insert(btn70)

pod_main_btn = InlineKeyboardButton(text='Смотреть новинку ▶️', callback_data="checksub")
pod_btn = InlineKeyboardMarkup(row_width=1)
#pod_btn.insert(main_btn)



def admin_panel():
    panel = InlineKeyboardMarkup(inline_keyboard=[
            [
                        InlineKeyboardButton(text='vensko', callback_data='add_series')             
                    ],
                    [
                        InlineKeyboardButton(text='📝 Обяз. подписка', callback_data='subscription'),
                        InlineKeyboardButton(text='📊 Статистика', callback_data='Statistics')     
                    ],
                    [
                        InlineKeyboardButton(text='💬 Рассылка', callback_data='mailing'),
                        InlineKeyboardButton(text='👥 Админы', callback_data='admins')
            ]]) 
    return panel

def movie():
    Keyboard = InlineKeyboardMarkup(row_width=1)

    for archive in db.movies():
        button = InlineKeyboardMarkup(text=archive[0], url=archive[1])
        Keyboard.insert(button)

    btn = InlineKeyboardButton(text='Другие сериалы ➡️', callback_data='other_movies')
    btn2 = InlineKeyboardButton(text='🔥Трудные подростки • 4 СЕЗОН', url = "https://t.me/+1gwIDuQZ825jZTZi")
    btn3 = InlineKeyboardButton('😏Бесстыжие • ВСЕ СЕЗОНЫ', url = "https://t.me/+OZtxVH3K-rViMmUy")
    btn4 = InlineKeyboardButton(text='🧀Эйфория • 2 СЕЗОН', url='https://t.me/+_OFZpH6dTlQ2NDQy')
    Keyboard.insert(btn2)
    Keyboard.insert(btn3)
    Keyboard.insert(btn4)
    Keyboard.insert(btn)


    return Keyboard

add_back = InlineKeyboardButton(text='⬅️ Назад', callback_data="quit")
back = InlineKeyboardMarkup(row_width=1)
back.insert(add_back)
