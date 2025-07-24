import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from bot.middleware.check_user import AuthMiddleware
from bot.handlers import registration, start, main_menu, create_team, team
from bot.utils.database import get_database

config = load_config()

bot = Bot(token=config.bot_token) 
dp = Dispatcher(storage=MemoryStorage())


async def main():
    bot.session.default_parse_mode = "HTML"
    db = await get_database()
    
    dp.message.middleware(AuthMiddleware(db))
    
    dp.include_routers(
        start.router,
        registration.router,
        main_menu.router,
        create_team.router,
        team.router,
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Помилка сталася: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())