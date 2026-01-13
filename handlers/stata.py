from aiogram import types
from aiogram.types import message
import variables as var
from Keyboard import markup as mar
from bot import dp, bot
from data_base import db
from handlers import back
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from handlers import StartUsers, joinedUsers


#Стастистика
@dp.callback_query_handler(text='Statistics')
async def Statistics(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    for user in StartUsers:
        var.users_sub += 1
    for user in joinedUsers:
        var.joinusers += 1
    for admin in db.admins():
        var.count_admins += 1

    EVERYONE = var.joinusers / var.users_sub
    EVERYONE_SUBSCRIBES = round(EVERYONE, 1)

    wel_stata = f'<b>📊 Статистика бота\n     • Всего пользователей: {var.joinusers}\n     • Всего подписалось: {var.users_sub}\n    〽️ Каждый: {EVERYONE_SUBSCRIBES} подписался на каналы\n\n     • Админов: {var.count_admins}</b>'

    markup = InlineKeyboardMarkup(inline_keyboard=[
                        [              
                            InlineKeyboardButton(text='📋 Файл для True Checker', callback_data='file_for_tc'), 
                        ],
                        [
                            InlineKeyboardButton(text='⬅️ Назад', callback_data='back')
                        ]])

    await bot.send_message(call.from_user.id, wel_stata, reply_markup=markup)
    var.joinusers = 0
    var.count_admins = 0 
    var.users_sub = 0 
    

    @dp.callback_query_handler(text='file_for_tc')
    async def file_for_tc(call: types.CallbackQuery):
        await bot.send_document(call.from_user.id, open("/home/heldan/TeleBot1/txt_files/joined.txt", "rb"))

