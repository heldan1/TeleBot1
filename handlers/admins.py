from aiogram import types
from aiogram.types import message
from Keyboard import markup as mar
from bot import dp, bot
from data_base import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from handlers import isAdmin, back, wel_admin_panel


''' calling the command admins '''
@dp.callback_query_handler(text='admins')
async def admins(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Админы: ', reply_markup=db.admins_read())



''' add_channels '''
class add_admin(StatesGroup):
    admin = State()

wel_add_admin = '<b>1️⃣ Пришлите имя пользователя ( @durov ):</b>'

@dp.callback_query_handler(text='add_admin')
async def start_add_admin(call: types.CallbackQuery, state: FSMContext):
    global msg
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await call.message.answer(wel_add_admin, reply_markup=mar.back)
    await add_admin.admin.set()



@dp.message_handler(state=add_admin.admin)
async def add_data_of_admin(message: types.Message, state: FSMContext):

    if isAdmin(message.from_user.username, message.from_user.id):
        try:
            await msg.delete()
            await message.delete()

            answer = message.text
            sin = '@'
            id_adm = answer.lstrip(sin)

            markup = InlineKeyboardMarkup(inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text = 'Подтвердить ✅', callback_data = 'next'), 
                                    InlineKeyboardButton(text = '🚫 Отменить', callback_data = 'quit')
                                ]])

            await state.update_data(id_adm=id_adm)
            await message.answer(text=f'Админ: {answer}', reply_markup=markup)
                

        except:
            markup = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                [              
                                    InlineKeyboardButton(text = '🔄 Повторить снова', callback_data = 'add_admin'),     
                                    InlineKeyboardButton(text = '⬅️ Выйти в меню', callback_data = 'back')
                                ]
                            ]) 
            await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup = markup) 
            await state.finish()



@dp.callback_query_handler(text='next', state=add_admin.admin)
async def add_data(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    data = await state.get_data()
    id_adm = data.get('id_adm')
    await state.finish()

    try:
        db.cursor.execute('INSERT INTO admins VALUES(?);', (id_adm,))
        db.connect.commit()
        await call.message.answer('Админы: ', reply_markup=db.admins_read())

    except:
        markup = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                            [              
                                InlineKeyboardButton(text='🔄 Повторить снова', callback_data='add_admin'),     
                                InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='back')
                            ]
                        ]) 

        await call.message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', parse_mode='html', reply_markup=markup) 
        await state.finish()



''' ( ----- remove admin ----- ) '''

mess_del_admin = 'Выбери кого хочешь удалить, нажав на ❌:'

@dp.callback_query_handler(text='remove_admin')
async def remove_admin(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    Keyboard = InlineKeyboardMarkup(row_width=1)

    for adm in db.admins():
        button_url = f'https://t.me/{adm[0]}'
        button = InlineKeyboardMarkup(text=f'👤 {adm[0]}', url=button_url)
        button_2 = InlineKeyboardMarkup(text=f'❌', callback_data=f'rem {adm[0]}')
        Keyboard.row(button,button_2)

    add_back = InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
    Keyboard.insert(add_back)

    await bot.send_message(call.from_user.id, mess_del_admin, reply_markup=Keyboard)



@dp.callback_query_handler(lambda x: x.data and x.data.startswith('rem '))
async def del_admin(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    db.sql_delete_admin(call.data.replace('rem ', ''))
    await call.answer('Админ удален ❌')
    await call.message.answer('Админы: ', reply_markup=db.admins_read())


@dp.callback_query_handler(text='quit', state=add_admin.admin)
async def quit(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.finish()
    await bot.send_message(call.from_user.id, wel_admin_panel ,reply_markup=mar.admin_panel())
