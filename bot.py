import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import admin_handlers



async def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(admin_handlers.router,)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
