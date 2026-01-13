from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import message
from aiogram import types
import re


async def cr_murkups(message, state):
    global markups
    data = await state.get_data()

    text = data.get('text')
    photo = data.get('photo')
    video = data.get('video')

    markup = message.text
    markups = re.split(' - |\n', markup)
    try:
        send_murkups()

        nextbtn=InlineKeyboardButton(text='Опубликовать ✅', callback_data='next')
        quit=InlineKeyboardButton(text='📛 Отмена', callback_data='quit')


        Keyboard.row(nextbtn,quit)
        if not video:
            if not photo:
                await message.answer(text=text, reply_markup = Keyboard, disable_web_page_preview=True)
            else:
                await message.answer_photo(caption=text, photo=photo, reply_markup = Keyboard)
        else:
            await message.answer_video(caption=text, video=video, reply_markup = Keyboard)

        await state.update_data(name_button=markups[0])


    except:
        markup = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                    [              
                                        InlineKeyboardButton(text='🔄 Повторить снова', callback_data='create_button'),     
                                        InlineKeyboardButton(text='⬅️ Выйти в меню', callback_data='quit')
                                    ]
                                ]) 
        await message.answer(text='<b>Ошибка!📛</b>\nПовторите попытку.', reply_markup=markup) 


def send_murkups():
    global Keyboard
    try:
        Keyboard = InlineKeyboardMarkup(row_width=1)
        try:
            button = InlineKeyboardButton(text=markups[0], url=markups[1])
            button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
            button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
            button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
            button5 = InlineKeyboardButton(text=markups[8], url=markups[9])
            button6 = InlineKeyboardButton(text=markups[10], url=markups[11])
            button7 = InlineKeyboardButton(text=markups[12], url=markups[13])
            button8 = InlineKeyboardButton(text=markups[14], url=markups[15])
            button9 = InlineKeyboardButton(text=markups[16], url=markups[17])
            Keyboard.insert(button)
            Keyboard.insert(button2)
            Keyboard.insert(button3)
            Keyboard.insert(button4)
            Keyboard.insert(button5)
            Keyboard.insert(button6)
            Keyboard.insert(button7)
            Keyboard.insert(button8)
            Keyboard.insert(button9)
        except:
            try:
                button = InlineKeyboardButton(text=markups[0], url=markups[1])
                button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
                button5 = InlineKeyboardButton(text=markups[8], url=markups[9])
                button6 = InlineKeyboardButton(text=markups[10], url=markups[11])
                button7 = InlineKeyboardButton(text=markups[12], url=markups[13])
                button8 = InlineKeyboardButton(text=markups[14], url=markups[15])
                Keyboard.insert(button)
                Keyboard.insert(button2)
                Keyboard.insert(button3)
                Keyboard.insert(button4)
                Keyboard.insert(button5)
                Keyboard.insert(button6)
                Keyboard.insert(button7)
                Keyboard.insert(button8)
       
            except:
                try:
                    button = InlineKeyboardButton(text=markups[0], url=markups[1])
                    button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                    button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                    button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
                    button5 = InlineKeyboardButton(text=markups[8], url=markups[9])
                    button6 = InlineKeyboardButton(text=markups[10], url=markups[11])
                    button7 = InlineKeyboardButton(text=markups[12], url=markups[13])
                    Keyboard.insert(button)
                    Keyboard.insert(button2)
                    Keyboard.insert(button3)
                    Keyboard.insert(button4)
                    Keyboard.insert(button5)
                    Keyboard.insert(button6)
                    Keyboard.insert(button7)
                except:
                    try:
                        button = InlineKeyboardButton(text=markups[0], url=markups[1])
                        button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                        button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                        button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
                        button5 = InlineKeyboardButton(text=markups[8], url=markups[9])
                        button6 = InlineKeyboardButton(text=markups[10], url=markups[11])
                        Keyboard.insert(button)
                        Keyboard.insert(button2)
                        Keyboard.insert(button3)
                        Keyboard.insert(button4)
                        Keyboard.insert(button5)
                        Keyboard.insert(button6)
                    except:
                        try:
                            button = InlineKeyboardButton(text=markups[0], url=markups[1])
                            button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                            button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                            button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
                            button5 = InlineKeyboardButton(text=markups[8], url=markups[9])
                            Keyboard.insert(button)
                            Keyboard.insert(button2)
                            Keyboard.insert(button3)
                            Keyboard.insert(button4)
                            Keyboard.insert(button5)
                        except:
                            try:
                                button = InlineKeyboardButton(text=markups[0], url=markups[1])
                                button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                                button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                                button4 = InlineKeyboardButton(text=markups[6], url=markups[7])
                                Keyboard.insert(button)
                                Keyboard.insert(button2)
                                Keyboard.insert(button3)
                                Keyboard.insert(button4)
                            except:
                                try:
                                    button = InlineKeyboardButton(text=markups[0], url=markups[1])
                                    button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                                    button3 = InlineKeyboardButton(text=markups[4], url=markups[5])
                                    Keyboard.insert(button)
                                    Keyboard.insert(button2)
                                    Keyboard.insert(button3)
                                except:
                                    try:
                                        button = InlineKeyboardButton(text=markups[0], url=markups[1])
                                        button2 = InlineKeyboardButton(text=markups[2], url=markups[3])
                                        Keyboard.insert(button)
                                        Keyboard.insert(button2)
                                    except:
                                        try:

                                            button = InlineKeyboardButton(text=markups[0], url=markups[1])
                                            Keyboard.insert(button) 

                                        except:
                                            pass
        
        return Keyboard                                              
    except:
        pass





