from aiogram import types
from aiogram.types import message
import variables as var
from Keyboard import markup as mar
from bot import dp, bot
import function as func
from data_base import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from handlers import isAdmin, back, wel_admin_panel
import asyncio



# The first method of mailing
class mailing(StatesGroup):
    send = State()
    murkup = State()

@dp.callback_query_handler(text='mailing')
async def start_mailing(message: types.Message):
    global msg
    await bot.delete_message(message.from_user.id, message.message.message_id)
    msg = await bot.send_message(message.from_user.id, f'<b>• Рассылка</b> 🗞\nОтправь боту то, что собираешься опубликовать:',reply_markup=mar.back, parse_mode="html")
    await mailing.send.set()


@dp.message_handler(content_types=['text', 'photo', 'video', 'document'], state=mailing.send)
async def send_msg(message: types.Message, state: FSMContext):
    if isAdmin(message.from_user.username, message.from_user.id):
        try:
            await msg.delete()
            await message.delete()

            markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [                  
                                    InlineKeyboardButton(text='➕ Добавить кнопку', callback_data='create_button')
                                ],                        
                                [
                                    InlineKeyboardButton(text='Опубликовать ✅', callback_data='next'),
                                    InlineKeyboardButton(text='📛 Отмена', callback_data='quit')
                                ]])

            if message.text:
                text = message.text

                await message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
                await state.update_data(text=text)
                await mailing.send.set()

              
            elif message.photo:
                text = message.caption
                photo = message.photo[-1].file_id

                await state.update_data(photo=photo, text=text)
                await message.answer_photo(photo=photo, caption=text, reply_markup=markup)
                await mailing.send.set()
               

            elif message.video:
                text = message.caption
                video = message.video.file_id

                await state.update_data(video=video, text=text)
                await message.answer_video(video=video, caption=text, reply_markup=markup)
                await mailing.send.set()

            elif message.document:
                await bot.send_document(message.from_user.id, message.document.file_id)
            else:
                await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.')
        except:
            await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.',reply_markup=mar.back)



#Create button
@dp.callback_query_handler(text='create_button', state=mailing.send)
async def create_button(call: types.CallbackQuery):
    global msg
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await bot.send_message(call.from_user.id, var.send_create_button, disable_web_page_preview=True)
    await mailing.murkup.set()

@dp.message_handler(state=[mailing.murkup,mailing.send])
async def add_button(message: types.Message, state: FSMContext):
    try:
        await message.delete()
        await msg.delete()

        await func.cr_murkups(message, state)
        await mailing.send.set()
    except:
        markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [              
                                        InlineKeyboardButton(text='🔄 Повторить снова', callback_data='create_button'),     
                                        InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='quit')
                                    ]
                                ]) 
        await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 





@dp.callback_query_handler(text='next', state=mailing.send)
async def send(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    users = db.cursor.execute("SELECT * FROM 'users'").fetchall()
    data = await state.get_data()

    text = data.get('text')
    photo = data.get('photo')
    video = data.get('video')
    name_button = data.get('name_button')
    await state.finish()


    if not photo:
        if not video:
            if not name_button:

                for user in users:
                    try:
                        await bot.send_message(chat_id=user[0], text=text, disable_web_page_preview=True)
                        await asyncio.sleep(0.375)
                    except Exception:
                        pass
                await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())

            else:

                for user in users:
                    await bot.send_message(chat_id=user[0], text=text, reply_markup=func.send_murkups(), disable_web_page_preview=True)
                    await asyncio.sleep(0.375)


                await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())                    
        else:

            if not name_button:
                for user in users:
                    try:
                        await bot.send_video(chat_id=user[0], video=video, caption=text)
                        await asyncio.sleep(0.38)
                    except Exception:
                        pass

                await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())
            else:

                for user in users:
                    try:
                        await bot.send_video(chat_id=user[0], video=video, caption=text, reply_markup=func.send_murkups())
                        await asyncio.sleep(0.375)
                    except Exception:
                        pass
                await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())

    else:
        if not name_button:
            for user in users:
                try:
                    await bot.send_photo(chat_id=user[0], photo=photo, caption=text)
                    await asyncio.sleep(0.375)
                except Exception:
                    pass
            await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())

        else:
            for user in users:
                try:
                    await bot.send_photo(chat_id=user[0], photo=photo, caption=text, reply_markup=func.send_murkups())
                    await asyncio.sleep(0.375)
                except Exception:
                    pass
            await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())


@dp.callback_query_handler(text='quit', state=[mailing.send, mailing.murkup])
async def quit(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.finish()
    await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())
