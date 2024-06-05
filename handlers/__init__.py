import logging
from bot import bot
from message import *
from .start import *
from .convert import *
from .pecahtxt import *
from .pecahvcf import *
from .convertvcf import *
from .convertxlsx import *

whitelist = {'6243471475': '30'} 
print(whitelist)

@bot.message_handler(commands='start')
async def send_welcome(message):
    try:
        user_id = str(message.from_user.id)  # Mendapatkan user_id dari pengguna
        if user_id in whitelist:
            await bot.reply_to(message, txt_start)
        else:
            await bot.reply_to(message, "Anda tidak diizinkan untuk menggunakan bot ini.")
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    await bot.send_message(message.chat.id, "Proses dibatalkan.")
    await bot.delete_state(message.from_user.id, message.chat.id)
