from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
import asyncio
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Создаем сессию
        async with SessionLocal() as session:
            # Добавляем сессию в контекст данных
            data["session"] = session
            return await handler(event, data)

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 110, timeout: int = 3):
        # limit - количество разрешенных сообщений за время timeout
        # timeout - время в секундах, за которое учитывается количество сообщений
        super().__init__()
        self.limit = limit
        self.timeout = timeout
        self.user_timestamps: Dict[int, list] = {}

    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            current_time = asyncio.get_event_loop().time()
            
            # Если пользователь уже в словаре, обновляем его временные метки
            if user_id in self.user_timestamps:
                timestamps = self.user_timestamps[user_id]
                # Фильтруем временные метки, оставляя только те, что в пределах timeout
                self.user_timestamps[user_id] = [t for t in timestamps if current_time - t < self.timeout]
                self.user_timestamps[user_id].append(current_time)
                
                # Проверяем, превысил ли пользователь лимит сообщений
                if len(self.user_timestamps[user_id]) > self.limit:
                    logger.info(f"🤡 Пользователь с ID {user_id} заблокирован за спам. Игнорируем клоуна {self.timeout} секунд(ы).")
                    return  # Игнорируем событие, ничего не отправляем и не обрабатываем дальше
            else:
                # Если пользователь новый, добавляем его в словарь
                self.user_timestamps[user_id] = [current_time]
                
        # Выполняем основной обработчик
        return await handler(event, data)

# Определение CallbackData
class SearchCallbackData(CallbackData, prefix="search"):
    query: str
    page: int
    
class SearchState(StatesGroup):
    waiting_for_query = State()
    
# Состояние для ожидания файла
class FileIDState(StatesGroup):
    waiting_for_file = State()
