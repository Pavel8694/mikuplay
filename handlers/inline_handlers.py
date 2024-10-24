from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultCachedAudio, InlineQueryResultArticle, InputTextMessageContent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Track
from fuzzywuzzy import process
import logging

inline_router = Router()
logger = logging.getLogger(__name__)

@inline_router.inline_query()
async def inline_query_handler(inline_query: InlineQuery, session: AsyncSession):
    query = inline_query.query.strip().lower()
    
    if query:
        # Извлекаем все треки, у которых есть file_id, и используем fuzzy matching для поиска подходящих
        tracks_result = await session.execute(select(Track).where(Track.file_id.isnot(None)))
        all_tracks = tracks_result.scalars().all()
        
        matched_tracks = []
        for track in all_tracks:
            title_score = process.extractOne(query, [track.title_lower])
            artist_score = process.extractOne(query, [track.artist_lower])
            if (title_score and title_score[1] > 60) or (artist_score and artist_score[1] > 60):
                matched_tracks.append(track)
        
        # Ограничиваем количество найденных треков до 50
        matched_tracks = matched_tracks[:50]
    else:
        # Если запрос пуст, возвращаем последние 10 добавленных треков с file_id
        matched_tracks = await session.execute(
            select(Track).where(Track.file_id.isnot(None)).order_by(Track.id.desc()).limit(10)
        )
        matched_tracks = matched_tracks.scalars().all()

    results = []
    for track in matched_tracks:
        if track.file_id:
            results.append(
                InlineQueryResultCachedAudio(
                    id=str(track.id),
                    audio_file_id=track.file_id,
                    title=track.title,
                    performer=track.artist,
                    parse_mode="HTML",
                    caption='<b><a href="https://t.me/MikuPlayBot">💙 Provided by MikuPlay</a></b>'
                )
            )
        else:
            # Если file_id отсутствует (не должно происходить из-за фильтрации), добавляем сообщение об ошибке
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
