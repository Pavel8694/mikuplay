import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from database import init_db
from handlers.admin_handlers import admin_router
from handlers.user_handlers import user_router
from handlers.common_handlers import common_router
from handlers.inline_handlers import inline_router
from ai.run import ai_router, auto_clear_old_history, process_queue
from middlewares import DbSessionMiddleware, AntiSpamMiddleware
from logging.handlers import RotatingFileHandler
import logging
import os

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаём директорию logs, если её нет
if not os.path.exists('logs'):
    os.makedirs('logs')

# Путь к файлу логов
log_file_path = os.path.join('logs', 'log.txt')

# Настраиваем обработчик логов с ротацией
rotating_handler = RotatingFileHandler(
    log_file_path, 
    maxBytes=2 * 1024 * 1024,  # 2 MB
    backupCount=5,  # Максимум 5 файлов с логами
    encoding='utf-8'
)

# Формат для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Настраиваем основной логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Отключаем логгирование aiogram.event на уровне INFO
logging.getLogger('aiogram.event').setLevel(logging.WARNING)

# Добавляем оба обработчика к основному логгеру, если они ещё не добавлены
if not logger.hasHandlers():
    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)

async def main():
    await init_db()
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.message.middleware(AntiSpamMiddleware(limit=110, timeout=3))
    dp.callback_query.middleware(AntiSpamMiddleware(limit=5, timeout=2))
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(common_router)
    dp.include_router(inline_router)
    dp.include_router(ai_router)
    asyncio.create_task(process_queue())
    asyncio.create_task(auto_clear_old_history())
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info(f"⚠️ Бот остановлен пользователем.")
    finally:
        await bot.session.close()
        logger.info(f"😴 Сессия завершена, бот завершил работу.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info(f"📴 Бот был выключен.")
