import logging
import os
from re import findall
from asyncio import sleep
from telebot.types import Message
from telebot.apihelper import ApiTelegramException

from bot import bot
from message import *
from helpers import *
from state import PecahVcfState

@bot.message_handler(commands='pecahvcf')
async def pecahvcf_command(message):
    try:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.set_state(message.from_user.id, PecahVcfState.filename, message.chat.id)
        await bot.reply_to(message, txt_pecah_vcf)
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.filename, content_types=['document'])
async def vcf_get(message: Message):
    try:
        if not message.document.file_name.endswith(".vcf"):
            return await bot.send_message(message.chat.id, "Kirim file .vcf")
        
        file = await bot.get_file(message.document.file_id)
        filename = f"files/{message.document.file_name}"
        
        await bot.set_state(message.from_user.id, PecahVcfState.name, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['filename'] = filename

        downloaded_file = await bot.download_file(file.file_path)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)

        await bot.send_message(message.chat.id, 'File diterima. Silakan masukkan nama file vcf yang akan dihasilkan:')
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.filename)
async def not_vcf(message: Message):
    try:
        await bot.send_message(message.chat.id, 'Kirim file .vcf')
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.name)
async def name_get(message: Message):
    try:
        if not message.text:
            return await bot.send_message(message.chat.id, 'Masukkan nama file yang valid.')
        
        await bot.send_message(message.chat.id, f'Nama file diatur menjadi: {message.text}. Silakan masukkan jumlah kontak per file:')
        await bot.set_state(message.from_user.id, PecahVcfState.totalc, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.totalc)
async def number_get(message: Message):
    try:
        if not message.text.isdigit():
            return await bot.send_message(message.chat.id, 'Masukkan angka yang valid untuk jumlah kontak per file.')
        
        total_contacts_per_file = int(message.text)
        await bot.send_message(message.chat.id, f'Jumlah kontak per file diatur menjadi: {total_contacts_per_file}. Silakan masukkan jumlah file:')
        await bot.set_state(message.from_user.id, PecahVcfState.totalf, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['totalc'] = total_contacts_per_file
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.totalf)
async def total_files_get(message: Message):
    try:
        if not message.text.isdigit():
            return await bot.send_message(message.chat.id, 'Masukkan angka yang valid untuk jumlah file.')

        total_files = int(message.text)
        await bot.send_message(message.chat.id, f'Jumlah file diatur menjadi: {total_files}. Mulai memecah file...')
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['totalf'] = total_files
            files = pecah_vcf(data)  # Anda harus memastikan fungsi pecah_vcf sesuai dengan batasan ini
            os.remove(data['filename'])
            for file in files:
                try:
                    await bot.send_document(message.chat.id, open(file, 'rb'))
                    os.remove(file)
                except ApiTelegramException as e:
                    if "Too Many Requests" in e.description:
                        delay = int(findall(r'\d+', e.description)[0])
                        await sleep(delay)
                    else:
                        logging.error("Telegram API error: ", exc_info=True)
                except Exception as e:
                    logging.error("Error sending document: ", exc_info=True)

            await bot.send_message(message.chat.id, "Pecah vcf selesai!")
        await bot.delete_state(message.from_user.id, message.chat.id)
    except Exception as e:
        logging.error("error: ", exc_info=True)

@bot.message_handler(state=PecahVcfState.totalc, is_digit=False)
@bot.message_handler(state=PecahVcfState.totalf, is_digit=False)
async def invalid_input(message: Message):
    try:
        await bot.send_message(message.chat.id, 'Masukkan angka yang valid.')
    except Exception as e:
        logging.error("error: ", exc_info=True)
