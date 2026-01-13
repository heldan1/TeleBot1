from aiogram import types, executor
from aiogram.types import message
from bot import dp, bot
import variables as var
import config 
from data_base import db
from Keyboard import markup as mar
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton




joinedFile = open("/home/heldan/TeleBot1/txt_files/joined.txt", "r")
UsesBotFile = open("/home/heldan/TeleBot1/txt_files/UsesBot.txt", "r")
joinedUsers = set()
StartUsers = set()

for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

for line in UsesBotFile:
    StartUsers.add(line.strip())
UsesBotFile.close()


#StartCommandProcessing 
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    global user
    user = message.chat.id

    def add_user(id):
        user = [message.chat.id]
        db.cursor.execute('INSERT INTO users VALUES(?);', user)
        db.connect.commit()

    
    if(not db.user_exists(message.from_user.id)):
        add_user(message.from_user.id)

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("/home/heldan/TeleBot1/txt_files/joined.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)


    if message.chat.type == 'private':    
        #Sticker
        #sti = open('/home/heldan/TeleBot/pictures/sticker.webp','rb')
        #await bot.send_sticker(message.chat.id, sti)

        #Photo
        photo = open('/home/heldan/TeleBot1/pictures/vnsk.JPEG','rb')
        #photo_3 = open('/home/heldan/TeleBot/pictures/photo 3.jpg','rb')

        await bot.send_photo(message.from_user.id, photo, var.Welcome_message.format(message.from_user),
            reply_markup=mar.Start_btn)
        
        #await bot.send_photo(message.from_user.id, photo_3, var.podrostki,
        #   reply_markup=mar.pod_btn)

#Check sub on channels
async def check_sub_channels(channels, user_id):
    for channel in db.channels():
        chat_member = await bot.get_chat_member(chat_id=channel[0], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True 


@dp.callback_query_handler(text='checksub')
async def checksub(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)    

    if await check_sub_channels(db.channels(), message.from_user.id):
        await bot.send_message(message.from_user.id, var.greeting.format(message.from_user),
            reply_markup=mar.movie())

        if not str(user) in StartUsers:
            UsesBotFile = open("/home/heldan/TeleBot1/txt_files/UsesBot.txt", "a")
            UsesBotFile.write(str(user) + "\n")
            StartUsers.add(user)

    else:
        #Photo
        photo_2 = open('/home/heldan/TeleBot1/pictures/photo 2.jpg','rb')
        await bot.send_photo(message.from_user.id, photo_2 ,var.NOT_SUB_MESSAGE,
            reply_markup=db.channel_read())



#Другие сериалы
@dp.callback_query_handler(text='other_movies')
async def other_movies(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(inline_keyboard=[
                        [              
                            InlineKeyboardButton(text='Подать заявку', url='https://t.me/+JZeq1D9z50I4NGEy')
                        ]])


    await bot.send_message(call.from_user.id, var.main_mess, reply_markup=markup)

