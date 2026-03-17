import asyncio
from src.loader import dp, bot
from src.middleware import TimeLoggingMiddleware
from src import handlers

dp.update.middleware(TimeLoggingMiddleware())

async def main():
    print("🚀 Бот запущен! Нажми Ctrl+C для остановки.")
    print("📁 База данных: data/fitness_bot.db")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())