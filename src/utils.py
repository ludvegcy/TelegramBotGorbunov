from pathlib import Path
from aiogram.types import FSInputFile
from src.loader import bot
import logging

logger = logging.getLogger(__name__)
file_id_cache = {}

async def send_photo_with_cache(
    chat_id: int,
    photo_path: Path,
    caption: str = "",
    parse_mode: str = "Markdown"
):
    """Отправляет фото, используя кэш file_id, если возможно."""
    logger.info(f"🔍 Попытка отправить фото: {photo_path}")
    logger.info(f"📁 Файл существует: {photo_path.exists()}")

    if photo_path.exists():
        logger.info(f"✅ Фото найдено: {photo_path}")
        cached_id = file_id_cache.get(str(photo_path))
        if cached_id:
            logger.info(f"🔄 Использую кэшированный file_id для {photo_path}")
            try:
                return await bot.send_photo(
                    chat_id=chat_id,
                    photo=cached_id,
                    caption=caption,
                    parse_mode=parse_mode
                )
            except Exception as e:
                logger.error(f"❌ Ошибка при отправке кэшированного фото: {e}")
                # Если ошибка, пробуем отправить заново
                file_id_cache.pop(str(photo_path), None)

        logger.info(f"📤 Отправляю новое фото: {photo_path}")
        try:
            msg = await bot.send_photo(
                chat_id=chat_id,
                photo=FSInputFile(photo_path),
                caption=caption,
                parse_mode=parse_mode
            )
            if msg.photo:
                file_id_cache[str(photo_path)] = msg.photo[-1].file_id
                logger.info(f"💾 Сохранён file_id для {photo_path}")
            return msg
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке нового фото: {e}")
            return await bot.send_message(chat_id, caption, parse_mode=parse_mode)
    else:
        logger.warning(f"❌ Фото не найдено: {photo_path}")
        return await bot.send_message(chat_id, caption, parse_mode=parse_mode)