from aiogram import types
from aiogram.types import message
from Keyboard import markup as mar
from bot import dp, bot
from data_base import db
import config

wel_admin_panel = '<b>Админ панель : </b>'

def isAdmin(username, id):
    if db.admin_exists(username) or db.admin_exists(id):
        return True
    if id == config.owner:
        return True


''' admin panel '''
@dp.message_handler(text='/admin')
async def admin_panel(message: types.Message):

    if isAdmin(message.from_user.username, message.from_user.id):
        await bot.send_message(message.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())


@dp.message_handler(text='/copy_db_files')
async def file_sub_done(message: types.Message):
    await bot.send_document(message.from_user.id, open("/home/heldan/TeleBot1/txt_files/UsesBot.txt", "rb"))
    await bot.send_document(message.from_user.id, open("/home/heldan/TeleBot1/txt_files/joined.txt", "rb"))


''' ( ----- back ----- ) '''
@dp.callback_query_handler(text='back')
async def back(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())
