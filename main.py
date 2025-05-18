import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from handlers import setup_routers

config = load_config()
bot = Bot(token=config.bot_token)
dp = Dispatcher(storage=MemoryStorage())
setup_routers(dp)


async def main():
    bot.session.default_parse_mode = "HTML"
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())