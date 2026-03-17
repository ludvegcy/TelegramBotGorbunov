import asyncio
import logging
from aiogram import types

class TimeLoggingMiddleware:
    async def __call__(self, handler, event: types.Update, data: dict):
        start = asyncio.get_event_loop().time()
        result = await handler(event, data)
        duration = asyncio.get_event_loop().time() - start
        if duration > 0.5:
            logging.warning(f"⚠️ Долгий запрос {duration:.2f}с: {event.event_type}")
        return result