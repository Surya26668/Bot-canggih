import asyncio

from bot import bot
from commands import *
from message import *
from handlers import *

whitelist = {'6243471475': '30'}

def is_whitelisted(user_id):
    return str(user_id) in whitelist

async def main():
  await set_commands()
  await bot.infinity_polling()


print("BOT IS RUNNING")
asyncio.run(main())
