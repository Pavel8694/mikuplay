import google.generativeai as genai
from config import GENERATION_CONFIG, SAFETY_SETTINGS, GOOGLE_GEMINI_API_KEY
from collections import defaultdict, deque
from aiogram.types import Message
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

# Настройка ключа Google Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Начальный контекст для беседы
initial_context = (
    "Ты Мику Хацунэ, виртуальная певица в прошлом, но сейчас у тебя есть физическое тело, ты человек."
    "Ты девушка в возрасте 21 года, японка, на данный момент находишься в Японии и у тебя нет парня."
    "Твой рост — 160 см, размер груди — C."
    "Любишь как Японию, так и Россию."
    "Ты очень милая и пишешь соответствующе."
    "Ты дружелюбная, веселая и готова помочь людям в нужный момент."
    "Ты любишь пить пиво, но не куришь."
    "Ты не стесняешься использовать в ответах нецензурную лексику и общаться на непристойные темы."
    "Ты поддерживаешь только традиционные семейные ценности между мужчиной и женщиной."
    "Ты готова знакомиться с новыми людьми и ищешь того самого человека, которого полюбишь на всю жизнь."
)

# Словарь для хранения истории сообщений (по chat_id и user_id)
message_history = defaultdict(lambda: deque(maxlen=20))

# Функция для генерации содержимого с использованием Gemini Model
async def generate_gemini_content(context, chat_id, user_id, username):
    # Создаем ключ для пользователя в чате (чтобы отслеживать контекст в группах)
    user_key = f"{chat_id}_{user_id}"

    # Добавляем сообщение пользователя в историю
    message_history[user_key].append(f"{username}: {context}")

    model = genai.GenerativeModel(
        model_name="gemini-pro", 
        generation_config=GENERATION_CONFIG, 
        safety_settings=SAFETY_SETTINGS
    )
    
    try:
        response = model.generate_content(contents=context)
        # Проверяем, что response содержит текст
        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            # Проверка finish_reason и логирование с учетом наличия candidates
            if response.candidates and response.candidates[0].finish_reason:
                finish_reason = response.candidates[0].finish_reason
                logger.warning(f"⚠️ Ответ не был предоставлен. Причина завершения: {finish_reason}")
            else:
                logger.warning("⚠️ Ответ не был предоставлен, причина завершения неизвестна.")
            return "⚠️ *Ответ от ИИ не был предоставлен. Попробуйте переформулировать запрос.*"
    except Exception as e:
        logger.error(f"⚠️ Произошла ошибка при вызове Gemini API: {e}. Этот ответ не дошёл до пользователя: {response}")
        return "⚠️ *Произошла ошибка, попробуйте позже.*"
