from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultCachedAudio, InlineQueryResultArticle, InputTextMessageContent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Track
import logging
import re
import unicodedata

inline_router = Router()
logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    """
    Приводит текст к нормализованному виду для поиска, удаляя диакритические символы.
    """
    decomposed = unicodedata.normalize('NFD', text)  # Разложение символов
    return ''.join(c for c in decomposed if not unicodedata.combining(c))  # Удаляем диакритические символы

@inline_router.inline_query()
async def inline_query_handler(inline_query: InlineQuery, session: AsyncSession):
    query = inline_query.query.strip().lower()
    
    logger.info(f"🎵 Получен поисковой запрос: '{query}'")  # Логируем поисковой запрос
    
    if query:
        # Разделяем запрос на отдельные слова
        query_words = query.split()
        # Нормализуем поисковые слова
        query_words = [normalize_text(word) for word in query_words]
        
        # Извлекаем все треки, у которых есть file_id
        tracks_result = await session.execute(select(Track).where(Track.file_id.isnot(None)))
        all_tracks = tracks_result.scalars().all()
        
        matched_tracks = []
        for track in all_tracks:
            # Нормализуем название трека и исполнителя для сравнения
            title_normalized = normalize_text(track.title_lower)
            artist_normalized = normalize_text(track.artist_lower)
            
            # Проверка: каждое слово должно совпадать либо с названием, либо с исполнителем
            matches_all_words = all(
                re.search(re.escape(word), title_normalized) or re.search(re.escape(word), artist_normalized)
                for word in query_words
            )
            
            # Если все слова совпадают, добавляем трек
            if matches_all_words:
                matched_tracks.append(track)
        
        # Ограничиваем количество найденных треков до 50
        matched_tracks = matched_tracks[:50]
    else:
        # Если запрос пуст, возвращаем последние 10 добавленных треков с file_id
        matched_tracks = await session.execute(
            select(Track).where(Track.file_id.isnot(None)).order_by(Track.id.desc()).limit(10)
        )
        matched_tracks = matched_tracks.scalars().all()

    # Логируем найденные треки
    if matched_tracks:
        logger.info(f"🎵 Найденные треки: {[f'ID: {track.id}, Название: {track.title}, Исполнитель: {track.artist}' for track in matched_tracks]}")
    else:
        logger.info("🎵 Не найдено ни одного трека.")

    results = []
    for track in matched_tracks:
        if track.file_id:
            results.append(
                InlineQueryResultCachedAudio(
                    id=str(track.id),
                    audio_file_id=track.file_id,
                    title=track.title,
                    performer=track.artist,
                    caption='<b><a href="https://t.me/MikuPlayBot">💙 Provided by MikuPlay</a></b>',
                    parse_mode="HTML"
                )
            )
        else:
            logger.warning(f"⚠️ Трек с ID {track.id} недоступен, отсутствует file_id.")
            results.append(
                InlineQueryResultArticle(
                    id=f"error-{track.id}",
                    title=f"⚠️ Трек {track.title} недоступен",
                    input_message_content=InputTextMessageContent(
                        message_text=f"⚠️ Трек {track.title} от {track.artist} в данный момент недоступен."
                    )
                )
            )

    if not results:
        await inline_query.answer([], switch_pm_text="⚠️ Нет результатов, попробуйте другой запрос.", switch_pm_parameter="start")
    else:
        await inline_query.answer(results, cache_time=1)

    # Логируем количество отправленных результатов
    logger.info(f"🎵 Количество полученных результатов в поиске: {len(results)}")
