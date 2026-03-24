import asyncio
import os
import logging
from aiohttp import web
from src.loader import dp, bot
from src.middleware import TimeLoggingMiddleware
from src import handlers

dp.update.middleware(TimeLoggingMiddleware())

PORT = int(os.getenv("PORT", 8080))

async def health(request):
    return web.Response(text="OK")

async def start_bot():
    """Запуск polling бота."""
    await dp.start_polling(bot)

async def main():
    app = web.Application()
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"HTTP сервер запущен на порту {PORT}")

    # Запускаем бота
    await start_bot()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())