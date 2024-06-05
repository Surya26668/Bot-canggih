import logging
from bot import bot
from message import *

# Kamus whitelist
whitelist = {'6243471475': '30'} 

print("DANA")

@bot.message_handler(commands='start')
async def send_welcome(message):
    user_id = str(message.from_user.id)
    try:
        if user_id in whitelist:
            allowed_amount = whitelist[user_id]
            welcome_message = f"Selamat datang! Anda diizinkan melakukan pembayaran hingga {allowed_amount} unit."
        else:
            welcome_message = "Anda tidak diizinkan melakukan pembayaran."
        await bot.reply_to(message, welcome_message)
    except Exception as e:
        logging.error("Error: ", exc_info=True)

@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    try:
        await bot.send_message(message.chat.id, "Proses dibatalkan.")
        await bot.delete_state(message.from_user.id, message.chat.id)
    except Exception as e:
        logging.error("Error: ", exc_info=True)
