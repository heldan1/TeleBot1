from aiogram import types
from aiogram.types import message
import variables as var
from Keyboard import markup as mar
from bot import dp, bot
from data_base import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from handlers import isAdmin, back, wel_admin_panel
from handlers import check_sub_channels
import re


#add_channels
class add_channel(StatesGroup):
    channel = State()

@dp.callback_query_handler(text='add_channel')
async def start_mailing(call: types.CallbackQuery, state: FSMContext):
    global msg
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await bot.send_message(call.from_user.id, var.wel_add_channel, reply_markup=mar.back, disable_web_page_preview=True) 
    await add_channel.channel.set()

@dp.message_handler(state=add_channel.channel)
async def add_button(message: types.Message, state: FSMContext):
    global user
    if isAdmin(message.from_user.username, message.from_user.id):
        user = message.from_user.id
        try:
            await msg.delete()
            await message.delete()

            answer = message.text
            channel = re.split(' - |\n', answer)

            markup = InlineKeyboardMarkup(inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='Подтвердить ✅', callback_data='next'), 
                                    InlineKeyboardButton(text='🚫 Отменить', callback_data='quit')
                                ]])

            await state.update_data(channel=channel)
            await message.answer(text=answer, reply_markup=markup, disable_web_page_preview=True)

        except:
            markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_channel'),     
                                    InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                ]
                            ]) 
            await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 
            await state.finish()

@dp.callback_query_handler(text='next', state=add_channel.channel)
async def add_channels(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    data = await state.get_data()
    channel = data.get('channel')
    await state.finish()


    try:
        db.cursor.execute('INSERT INTO channels VALUES(?,?);', (channel[0],channel[1] ))
        db.connect.commit()
        await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())

    except:
        db.sql_delete_channel(channel[1])
        markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_channel'),     
                                    InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                ]
                            ]) 
        await call.message.answer(text=var.error_channel, reply_markup=markup) 
        await state.finish()        



class add_channels_without_verif(StatesGroup):
    channel = State()

@dp.callback_query_handler(text='add_channels_without_verif')
async def channels_without_verif(call: types.CallbackQuery, state: FSMContext):
    global msg
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await bot.send_message(call.from_user.id, var.wel_channels_without_verif, reply_markup=mar.back, disable_web_page_preview=True) 
    await add_channels_without_verif.channel.set()

@dp.message_handler(state=add_channels_without_verif.channel)
async def add_button(message: types.Message, state: FSMContext):
    if isAdmin(message.from_user.username, message.from_user.id):
        try:
            await msg.delete()
            await message.delete()

            answer = message.text
            markup = InlineKeyboardMarkup(inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='Подтвердить ✅', callback_data='next'), 
                                    InlineKeyboardButton(text='🚫 Отменить', callback_data='quit')
                                ]])

            await state.update_data(channel=answer)
            await message.answer(text=answer, reply_markup=markup, disable_web_page_preview=True)

        except:
            markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_channels_without_verif'),     
                                    InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                ]
                            ]) 
            await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 
            await state.finish()
        


@dp.callback_query_handler(text='next', state=add_channels_without_verif.channel)
async def add_channels(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    data = await state.get_data()
    channel = data.get('channel')
    await state.finish()

    try:
        test_BTN = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Проверка...', url=channel)]])
        msg = await bot.send_message(call.from_user.id, 'Проверка на ошибки', reply_markup=test_BTN)
        await msg.delete()
        try:
            db.cursor.execute('INSERT INTO channels_without_verif VALUES(?);', (channel, ))
            db.connect.commit()

            if await check_sub_channels(db.channels(), call.from_user.id):
                await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())
            else:
                await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())

        except:
            pass
    except:
        db.sql_delete_channel(channel[0])
        markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_channels_without_verif'),     
                                    InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                ]
                            ]) 
        await call.message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 


#Delete channel 
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit '))
async def del_callback_run(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        del_id = call.data.replace('edit ', '')
        db.sql_delete_channel(del_id)
        await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())




'''    class edit_url(StatesGroup):
        new_url = State()

    @dp.callback_query_handler(text='edit_id')
    async def delete_channel(call: types.CallbackQuery):
        global msg

        await bot.delete_message(call.from_user.id, call.message.message_id)
        msg = await bot.send_message(call.from_user.id, '<b>Пришлите новую ссылку на канал:</b>', reply_markup=mar.back, disable_web_page_preview=True)
        await edit_url.new_url.set()

    @dp.message_handler(state=edit_url.new_url)
    async def up_url(message: types.Message, state: FSMContext):
        if isAdmin(message.from_user.username, message.from_user.id):
            try:
                await msg.delete()
                await message.delete()

                answer = message.text
                markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [              
                                        InlineKeyboardButton(text='Подтвердить ✅', callback_data='next'), 
                                        InlineKeyboardButton(text='🚫 Отменить', callback_data='quit')
                                    ]])

                await state.update_data(channel=answer)
                await message.answer(text=answer, reply_markup=markup, disable_web_page_preview=True)

            except:
                markup = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                    [              
                                        InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_channels_without_verif'),     
                                        InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                    ]
                                ]) 
                await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 
                await state.finish()
            


    @dp.callback_query_handler(text='next', state=edit_url.new_url)
    async def add_url(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)

        data = await state.get_data()
        channel = data.get('channel')
        await state.finish()

        
        db.update_url(channel, del_id)
        await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())
        try:
            pass
        except:
            markup = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                    [              
                                        InlineKeyboardButton(text='🔄 Повторить снова', callback_data='edit_id'),     
                                        InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                                    ]
                                ]) 
            await call.message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup)'''




@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit_wv '))
async def del_callback_run(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    db.sql_delete_channel_without_verif(call.data.replace('edit_wv ', ''))
    await call.answer('Канал удален')
    await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())



@dp.callback_query_handler(text='subscription')
async def subscription(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(var.wel_subscription,reply_markup=db.adm_channel_read())



@dp.callback_query_handler(text='quit', state=[add_channels_without_verif.channel, add_channel.channel])
async def quit(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.finish()
    await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())


