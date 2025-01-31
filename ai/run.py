from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from ai.modules.gemini import generate_gemini_content, initial_context
from collections import defaultdict, deque
from keyboards.buttons import get_ai_settings_keyboard, get_ai_clear_keyboard
import logging
import re
import asyncio
import time

ai_router = Router()
# Настройка логгера
logger = logging.getLogger(__name__)
# Регулярное выражение для поиска имени "Мику" в любом регистре
miku_pattern = re.compile(r'\bмику\b', re.IGNORECASE)
# Словарь для хранения истории сообщений (по chat_id и user_id)
message_history = defaultdict(lambda: {"messages": deque(maxlen=20), "cleared": False})
# Словарь для хранения временных меток сообщений, используя time.monotonic()
message_timestamps = defaultdict(time.monotonic)
# Очередь сообщений для обработки по одному
message_queue = asyncio.Queue()

def clean_extra_spaces_preserve_formatting(text: str) -> str:
    """
    Удаляет повторные пробелы между словами, сохраняя отступы и переносы строк.
    """
    return re.sub(r' +', ' ', text)

# Функция для обработки сообщений из очереди
async def process_queue():
    while True:
        message = await message_queue.get()
        await handle_miku_message_internal(message)
        message_queue.task_done()
        await asyncio.sleep(0.1)  # Добавляем небольшую паузу для снижения нагрузки

# Основной обработчик сообщений с фильтрацией по имени "Мику" или если сообщение является ответом
@ai_router.message(F.text)
async def handle_miku_message(message: Message):
    bot_user = await message.bot.get_me()  # Получаем информацию о боте (его ID)

    # Проверяем, содержится ли "Мику" в тексте сообщения или это ответ на сообщение от бота
    if (
        miku_pattern.search(message.text) or 
        (message.reply_to_message and message.reply_to_message.from_user.id == bot_user.id)
    ):
        if message_queue.qsize() < 100:  # Ограничиваем до 100 сообщений
            await message_queue.put(message)
        else:
            logger.warning("⚠️ Очередь сообщений переполнена, пропущено сообщение.")

# Задача для очистки старых сообщений через 24 часа
async def auto_clear_old_history():
    while True:
        current_time = time.monotonic()
        for user_key, last_activity in list(message_timestamps.items()):
            if current_time - last_activity > 24 * 60 * 60:  # 24 часа
                if user_key in message_history:
                    del message_history[user_key]
                    message_timestamps.pop(user_key, None)
                    logger.info(f"🕒 История сообщений автоматически очищена для пользователя {user_key}.")
        await asyncio.sleep(3600)  # Проверка каждые 60 минут

@ai_router.callback_query(F.data == "ai_button")
async def show_ai_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"🧠 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню настроек ИИ.")
    await callback_query.message.edit_text('🧠 *Меню действий настроек ИИ.*\n\n'
                                           '💙 *Выберите действие:*',
                                           parse_mode="Markdown",
                                           reply_markup=get_ai_settings_keyboard
                                           )
    
@ai_router.callback_query(F.data == "ai_info_button")
async def show_ai_info_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"ℹ️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в подробности функционала меню настроек ИИ.")
    await callback_query.message.edit_text('ℹ️ *Подробнее о действиях в настройках ИИ:*\n'
                                           '🗑 *Очистить историю — очищает ваш диалог с ИИ.* _(Также история очищается автоматически, если вы не будете общаться с ИИ в течение более 24 часов или если бот/сервер перезапустится.)_',
                                           parse_mode="Markdown",
                                           reply_markup=get_ai_clear_keyboard
                                           )
 
# Функция для очистки истории сообщений
@ai_router.callback_query(F.data == "ai_clear")
async def clear_message_history(callback_query: CallbackQuery, state: FSMContext):
    # logger.info("✅ Команда очищения истории сообщений с ИИ получена.")  # Проверка вызова
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_key = f"{chat_id}_{user_id}"
    
    # Логируем для отладки
    # logger.info(f"🔍 Проверка ключа: {user_key} в message_history.")
    # logger.info(f"📋 Текущее содержимое message_history: {message_history}.")
    
    # Очищаем историю сообщений пользователя, если она еще не очищена
    if user_key in message_history and not message_history[user_key]["cleared"]:
        message_history[user_key]["messages"].clear()
        message_history[user_key]["cleared"] = True
        message_timestamps.pop(user_key, None)  # Удаляем метку времени
        await callback_query.message.edit_text("🗑 *История сообщений успешно очищена.*", parse_mode="Markdown", reply_markup=get_ai_clear_keyboard)
        logger.info(f"✅ История сообщений очищена для пользователя @{callback_query.from_user.username} ({user_id}) в чате {chat_id}.")
    else:
        await callback_query.message.edit_text("⚠️ *История сообщений уже пуста.*", parse_mode="Markdown", reply_markup=get_ai_clear_keyboard)
        logger.info(f"⚠️ Попытка очистить пустую историю сообщений для пользователя @{callback_query.from_user.username} ({user_id}) в чате {chat_id}.")

# Внутренний обработчик сообщения для использования в очереди
async def handle_miku_message_internal(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or f"Аноним ({user_id})"
    user_message = message.text.strip()

    # Создаем ключ для пользователя в чате (чтобы отслеживать контекст в группах)
    user_key = f"{chat_id}_{user_id}"
    
    # Если у пользователя уже очищена история, сбрасываем статус очистки
    if message_history[user_key]["cleared"]:
        message_history[user_key]["cleared"] = False

    # Добавляем сообщение в историю и обновляем временную метку
    message_history[user_key]["messages"].append(f"{username}: {user_message}")
    message_timestamps[user_key] = time.monotonic()  # Устанавливаем время последней активности

    # Получаем последние сообщения (максимум 20)
    recent_messages = " \n".join(list(message_history[user_key]["messages"])[-20:])
    # Используем initial_context из gemini.py и добавляем к нему историю сообщений и текущее сообщение
    context = (
        f"Пользователь {username} пишет тебе: {user_message}\n"
        f"Последние сообщения из диалога с ним (сохраняются максимум 20):\n{recent_messages}\n"
        f"Твой контекст: {initial_context}\n"
        f"Мику, пожалуйста, ответь на сообщение пользователя с учётом всей беседы и не здоровайся повторно, если это не первое его сообщение тебе. Веди себя естественно, не как ИИ, а как человек, и запомни — ты Мику Хацунэ, а не кто-то другой. Можешь использовать смайлики и слова-паразиты. Также не пиши слишком объёмные ответы на странные сообщения/вопросы."
    )

    # Формируем запрос к модели с учетом контекста
    try:
        response = None  # Инициализируем переменную
        response = await generate_gemini_content(context, chat_id, user_id, username)
        if isinstance(response, str):
            # Удаляем лишние пробелы в ответе
            response = clean_extra_spaces_preserve_formatting(response)
            
            # Проверяем длину ответа и обрезаем, если нужно
            if len(response) > 4096:
                response = response[:4093] + "..."
            # Сохраняем ответ Мику в историю
            message_history[user_key]["messages"].append(f"Мику, это твой ответ: {response}")
            # Отправляем ответ в формате Markdown
            try:
                await message.reply(response, parse_mode="Markdown")
            except Exception as inner_error:
                logger.warning(f"⚠️ Ошибка при отправке ответа с Markdown: {inner_error}")
                # Отправляем без форматирования, если с Markdown не удается
                await message.reply(response, parse_mode=None)
        else:
            logger.error(f"⚠️ Ответ от Gemini API не является строкой: {response}")
            await message.reply("⚠️ *Похоже, произошла ошибка, или я не могу ответить на этот вопрос.*", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"⚠️ Ошибка для пользователя @{username} ({user_id}) в чате {chat_id}: {e}. Этот ответ не дошёл до пользователя: {response}")
        await message.reply("⚠️ *Похоже, произошла ошибка, или я не могу ответить на этот вопрос.*", parse_mode="Markdown")
