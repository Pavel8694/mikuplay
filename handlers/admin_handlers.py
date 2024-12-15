from aiogram import Router, F, exceptions
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database import Admin, Track
from sqlalchemy.future import select
from keyboards.buttons import cancel_button, back_to_menu_button, get_amdin_menu_keyboard, back_admin_menu_keyboard
from handlers.user_handlers import show_user_menu
from middlewares import FileIDState
from functools import wraps
import logging
import asyncio

admin_router = Router()
logger = logging.getLogger(__name__)

MAIN_ADMIN_ID = 0000000000
MAX_TELEGRAM_MESSAGE_LENGTH = 2048  # Ограничение на длину сообщения

class AddTrackState(StatesGroup):
    collecting_tracks = State()
    editing_track = State()
    adding_admin = State()
    removing_admin = State()
    deleting_track = State()
    replacing_audio = State()
    waiting_for_audio = State()

# Враппер для проверки прав администратора
def admin_only(callback_func):
    @wraps(callback_func)
    async def wrapper(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession, *args, **kwargs):
        if not await is_admin(callback_query.from_user.id, session):
            await callback_query.answer("⚠️ У вас нет прав для выполнения этого действия.", show_alert=True)
            return
        return await callback_func(callback_query, state, session, *args, **kwargs)
    return wrapper

async def is_admin(user_id: int, session: AsyncSession):
    if user_id == MAIN_ADMIN_ID:
        return True
    result = await session.execute(select(Admin).where(Admin.telegram_id == user_id))
    return result.scalars().first() is not None

@admin_router.message(Command("start"))
async def start_menu(message: Message, session: AsyncSession):
    if await is_admin(message.from_user.id, session):
        await show_admin_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для админов.")
    else:
        await show_user_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

@admin_router.message(Command("menu"))
async def menu_command(message: Message, session: AsyncSession):
    if await is_admin(message.from_user.id, session):
        await show_admin_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для админов.")
    else:
        await show_user_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

async def show_admin_menu(edit_function):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎵 Поиск треков", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="🔍 Расширенный поиск", callback_data="start_search")
            ],
            [
                InlineKeyboardButton(text="🪪 Профиль", callback_data="profile_button"),
                InlineKeyboardButton(text="🛍️ Магазин", callback_data="shop_button")
            ],
            [
                InlineKeyboardButton(text="👮 Админка", callback_data="admin_menu_button"),
                InlineKeyboardButton(text="🧠 Настройки ИИ", callback_data="ai_button")
            ],
            [
                InlineKeyboardButton(text="🆘 Помощь", callback_data="help_button"),
            ],
            [
                InlineKeyboardButton(text="🫰 Поддержать проект", url="https://boosty.to/mikuplay"),
                InlineKeyboardButton(text="🔗 GitHub", url="https://github.com/Pavel8694/mikuplay")
            ],
        ]
    )
    await edit_function('👋 *Приветствую вас в своей музыкальной обители, Пользователь Интернета!*\n\n👀 _Так-так, посмотрим... Ого! Похоже, вы являетесь администратором здесь! Добро пожаловать! Чувствуйте себя как дома. ᓚᘏᗢ_\n\n💬 *Кстати, ты можешь пообщаться со мной, обращаясь по имени или отвечая на мои сообщения. Пример:* `Мику, привет! Как дела?` _(Условия использования бота и ИИ читайте в меню "Помощь")_\n\n💙 *Выберите действие администратора:*', reply_markup=keyboard, parse_mode="Markdown")
    
@admin_router.callback_query(F.data == "admin_menu_button")
@admin_only
async def show_admin_menu_button(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    logger.info(f"👮 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню администраторов.")
    await callback_query.message.edit_text('👮 *Админка:*', parse_mode="Markdown", reply_markup=get_amdin_menu_keyboard)

@admin_router.callback_query(F.data == "add_tracks")
@admin_only
async def start_add_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    logger.info(f"⏳ Началось добавление треков пользователем @{callback_query.from_user.username} ({callback_query.from_user.id}).")
    await state.update_data(tracks=[])  # Инициализируем список треков
    await state.set_state(AddTrackState.collecting_tracks)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ Далее", callback_data="confirm_tracks")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
        ]
    )
    await callback_query.message.edit_text(
        '🎵 *Отправьте аудио-файлы для добавления. Когда закончите, вернитесь к этому сообщению и нажмите* ⏭️ *"Далее" или* ❌ *"Отменить".*\n\n_ᓚᘏᗢ P. S. КАТЕГОРИЧЕСКИ не рекомендуется добавлять аудио без названия/исполнителя (также с другим названием/исполнителем, не соответствующим добавляемому треку.) и с битрейтом ниже 320кб/с тех треков, которые доступны в нём и более высоком качестве. Моя музыкальная обитель должна состоять по большей части только из подлинных и высококачественных композиций!\nА вот что рекомендуется, так это подождать некоторое время, особенно если вы загрузили много треков. Спасибо! UwU_', 
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@admin_router.callback_query(F.data == "confirm_tracks")
@admin_only
async def confirm_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tracks = data.get("tracks", [])

    if not tracks:
        await callback_query.message.edit_text("❌ *Не получено треков для добавления.*", reply_markup=back_to_menu_button, parse_mode="Markdown")
        logger.warning(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался подтвердить добавление без треков.")
        return

    # Изменяем сообщение после нажатия "Далее"
    await callback_query.message.edit_text(
        "✅ *Список добавленных треков успешно отправлен!*",
        parse_mode="Markdown"
    )

    track_info = "\n".join([f"{track.title} - {track.artist}" for track in tracks])
    if len(track_info) > MAX_TELEGRAM_MESSAGE_LENGTH - 500:  # Учёт дополнительного текста
        track_info = track_info[:MAX_TELEGRAM_MESSAGE_LENGTH - 500] + "... (список обрезан)"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="final_confirm_tracks")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
        ]
    )
    await callback_query.message.answer(
        f'👇 <b>Вы добавили следующие треки:</b>\n{track_info}\n\n✅ <b>Подтвердите или ❌ отмените действие.</b>\n\n<i>ᓚᘏᗢ P. S. Треки и информация о них заносятся в базу данных эдакими "чанками" по 10 штук специально каждые 5.5 секунд, чтобы сильно не нагружать её.</i>',
        reply_markup=keyboard, parse_mode="HTML"
    )
    logger.info(f"📝 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) получил список добавленных треков.")

@admin_router.callback_query(F.data == "final_confirm_tracks")
@admin_only
async def final_confirm_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tracks = data.get("tracks", [])
    skipped_tracks = data.get("skipped_tracks", [])  # Получаем пропущенные треки из состояния

    # Изменяем сообщение после нажатия "Подтвердить"
    await callback_query.message.edit_text(
        "⏳ *Треки начали добавляться. Ожидайте завершения по отправке нового сообщения ботом.*",
        parse_mode="Markdown"
    )

    # Обработка треков батчами
    await process_tracks_in_batches(tracks, session, skipped_tracks, batch_size=10)

    await state.clear()

    if skipped_tracks:
        # Формируем сообщение с пропущенными треками
        skipped_info = "\n".join([f"{track['title']} (Причина: {track['reason']})" for track in skipped_tracks])
        if len(skipped_info) > MAX_TELEGRAM_MESSAGE_LENGTH - 200:
            skipped_info = skipped_info[:MAX_TELEGRAM_MESSAGE_LENGTH - 200] + "... (список обрезан)"

        message = (f"🤔 <b>Вроде, треки успешно добавлены.</b>\n\n"
                   f"⚠️ <b>Какие-то треки были пропущены, так как они либо уже существуют в базе данных, либо не являются MP3:</b>\n"
                   f"{skipped_info}")
        logger.warning(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) попытался добавить уже существующие или неподходящие треки: {skipped_info}")
    else:
        message = "✅ <b>Все треки успешно добавлены.</b>"
        logger.info(f"✅ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) добавил {len(tracks)} трек(ов).")

    await callback_query.message.answer(message, reply_markup=back_to_menu_button, parse_mode="HTML")

@admin_router.message(F.content_type == ContentType.AUDIO, StateFilter(AddTrackState.collecting_tracks))
async def collect_tracks(message: Message, state: FSMContext):
    audio = message.audio

    # Проверка MIME-тип файла
    if audio.mime_type != "audio/mpeg":
        logger.warning(f"⚠️ Файл {audio.file_name or 'без названия'} не является MP3. Пропускаем.")
        data = await state.get_data()
        skipped_tracks = data.get("skipped_tracks", [])
        skipped_tracks.append({"title": audio.file_name or "Без названия", "reason": "не MP3"})
        await state.update_data(skipped_tracks=skipped_tracks)
        return

    track_title = audio.title if audio.title else "Без названия"
    track_artist = audio.performer if audio.performer else "Неизвестный исполнитель"
    track_file_id = audio.file_id

    track_title_normalized = track_title.lower()
    track_artist_normalized = track_artist.lower()

    track = Track(
        title=track_title,
        artist=track_artist,
        file_id=track_file_id,
        title_lower=track_title_normalized,
        artist_lower=track_artist_normalized
    )

    # Получаем данные состояния
    data = await state.get_data()
    tracks = data.get("tracks", [])
    tracks.append(track)
    await state.update_data(tracks=tracks)

    # Логгирование добавленного трека
    logger.info(f"➕ Пользователь @{message.from_user.username} ({message.from_user.id}) добавил трек {track_title} исполнителя {track_artist}.")

async def process_tracks_in_batches(tracks, session, skipped_tracks, batch_size=10):
    for i in range(0, len(tracks), batch_size):
        batch = tracks[i:i + batch_size]
        for track in batch:
            try:
                logger.info(f"👀 Проверяем трек: {track.title}, ID: {track.file_id}.")

                # Проверяем, существует ли трек с таким же file_id
                existing_track = await session.execute(select(Track).where(Track.file_id == track.file_id))
                if existing_track.scalars().first():
                    logger.warning(f"⚠️ Трек с file_id {track.file_id} уже существует. Пропускаем добавление.")
                    skipped_tracks.append({"title": track.title, "reason": "уже существует"})
                    continue

                # Если трека нет, добавляем его в сессию
                session.add(track)

            except Exception as e:
                logger.error(f"⚠️ Ошибка при обработке трека {track.title}: {e}")
                skipped_tracks.append({"title": track.title, "reason": f"ошибка: {e}"})
                continue

        try:
            await session.commit()
            logger.info(f"✅ Успешная попытка добавления группы из {len(batch)} треков.")
        except Exception as e:
            logger.error(f"⚠️ Ошибка при добавлении группы треков: {e}")
            await session.rollback()  # Откатываем транзакцию в случае ошибки

        # Пауза между обработкой батчей
        if i + batch_size < len(tracks):  # Проверяем, нужно ли делать паузу
            # Делаем паузу, чтобы не превысить лимиты API
            await asyncio.sleep(5.5)  # Устанавливаем паузу в 5.5 секунд между обработкой батчей

# Функция для удаления трека (главный админ)
@admin_router.callback_query(F.data == "delete_track")
@admin_only
async def delete_track_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("⚠️ *Только главный администратор может удалять треки.*", parse_mode="Markdown", reply_markup=back_admin_menu_keyboard)
        logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню удаления треков.")
        return

    await state.set_state(AddTrackState.deleting_track)
    await callback_query.message.edit_text("🆔 *Введите ID трека для удаления (он будет скрыт из поиска).*\n\n_ᓚᘏᗢ P. S. Узнать ID нужного вам трека можно у главного администратора._", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню удаления треков.")

@admin_router.message(StateFilter(AddTrackState.deleting_track))
async def delete_track(message: Message, session: AsyncSession, state: FSMContext):
    try:
        track_id = int(message.text)
        track_result = await session.execute(select(Track).where(Track.id == track_id))
        track = track_result.scalars().first()
        if track:
            track.file_id = None
            await session.commit()
            await message.reply("✅ *Трек успешно скрыт из поиска.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) скрыл трек с ID {track_id}.")
            await state.clear()
        else:
            await message.reply("❌ *Трек с таким ID не найден.*", reply_markup=back_to_menu_button, parse_mode="Markdown")
            logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался скрыть трек с ID {track_id}, но его нет в моей базе.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка при удалении трека: {e}")
        await message.reply("⚠️ *Ошибка при удалении трека. Проверьте введенные данные.*", reply_markup=back_to_menu_button, parse_mode="Markdown")

# Функция для замены аудио-файлов
@admin_router.callback_query(F.data == "replace_audio")
@admin_only
async def replace_audio_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    # if callback_query.from_user.id != MAIN_ADMIN_ID:
        # await callback_query.message.edit_text(
            # "⚠️ *Только главный администратор может заменять треки.*",
            # parse_mode="Markdown",
            # reply_markup=back_admin_menu_keyboard
        # )
        # logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню замены треков.")
        # return

    await state.set_state(AddTrackState.replacing_audio)
    await callback_query.message.edit_text(
        "🆔 *Введите ID треков для замены, разделяя их пробелами. Пример:* `1 2 3 4 5`\n\n_ᓚᘏᗢ P. S. Узнать ID нужных треков можно у главного администратора. Максимальный лимит принимаемых ID за одну замену — 50._",
        reply_markup=cancel_button,
        parse_mode="Markdown"
    )
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню замены треков.")

@admin_router.message(StateFilter(AddTrackState.replacing_audio))
async def receive_track_ids(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text:
        await message.reply("⚠️ *Пожалуйста, введите ID треков в виде текста.*", parse_mode="Markdown", reply_markup=cancel_button)
        return

    track_ids = message.text.split()
    if len(track_ids) > 50:
        await message.reply("⚠️ *Вы указали слишком много ID. Максимум — 50 за раз.*", parse_mode="Markdown", reply_markup=cancel_button)
        return

    try:
        track_ids = list(map(int, track_ids))
    except ValueError:
        await message.reply("⚠️ *Пожалуйста, введите только числовые ID треков, разделяя их пробелами.*", parse_mode="Markdown", reply_markup=cancel_button)
        return

    tracks_result = await session.execute(select(Track).where(Track.id.in_(track_ids)))
    tracks = tracks_result.scalars().all()

    if not tracks:
        await message.reply("❌ *Треки с указанными ID не найдены.*", parse_mode="Markdown", reply_markup=cancel_button)
        return

    # Формируем список треков для подтверждения
    track_list = "\n".join([f"🎵 ID: {track.id}, Название: {track.title}, Исполнитель: {track.artist}" for track in tracks])
    if len(track_list) > MAX_TELEGRAM_MESSAGE_LENGTH:
        track_list = track_list[:MAX_TELEGRAM_MESSAGE_LENGTH - 50] + "... (список обрезан)"

    await state.update_data(track_ids=track_ids, tracks=tracks)
    await state.set_state(AddTrackState.waiting_for_audio)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ Далее", callback_data="confirm_replacement")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
        ]
    )

    await message.reply(
        f"📋 <b>Выбранные треки для замены:</b>\n\n{track_list}\n\n"
        '😊 <b>Теперь отправьте новые аудио-файлы в количестве, точно соответствующем числу выбранных треков. После отправки вернитесь к этому сообщению и нажмите "Далее".</b>\n\n<i>ᓚᘏᗢ P. S. Бот успешно примет только то количество треков, которое вы хотите заменить (первые по списку, как вы отправите, сверху вниз). Больше добавить треки в очередь обновления будет нельзя.</i>',
        parse_mode="HTML",
        reply_markup=keyboard
    )

@admin_router.message(F.content_type == ContentType.AUDIO, StateFilter(AddTrackState.waiting_for_audio))
async def receive_audio_files(message: Message, state: FSMContext):
    data = await state.get_data()
    tracks = data.get("tracks", [])
    received_files = data.get("received_files", [])
    skipped_tracks = data.get("skipped_tracks", [])
    limit_reached_logged = data.get("limit_reached_logged", False)  # Флаг для логирования
    
    # Проверка на лимит треков
    if len(received_files) >= len(tracks):
        if not limit_reached_logged:  # Логируем только один раз
            logger.warning("⚠️ Достигнут лимит отправленных файлов для замены. Пропускаем дальнейшую обработку.")
            await state.update_data(limit_reached_logged=True)  # Устанавливаем флаг
        return

    # Проверка MIME-тип файла
    if message.audio.mime_type != "audio/mpeg":
        logger.warning(f"⚠️ Файл {message.audio.file_name or 'без названия'} не является MP3. Пропускаем.")
        skipped_tracks.append({"title": message.audio.file_name or "Без названия", "reason": "не MP3"})
        await state.update_data(skipped_tracks=skipped_tracks)
        return

    # Сохраняем данные принятого файла
    new_file = {
        "file_id": message.audio.file_id,
        "title": message.audio.title or "Без названия",
        "artist": message.audio.performer or "Неизвестный исполнитель"
    }
    received_files.append(new_file)

    # Обновляем данные в состоянии
    await state.update_data(received_files=received_files)

    # Логгируем принятый файл
    logger.info(f"➕ Пользователь @{message.from_user.username} ({message.from_user.id}) добавил трек {new_file['title']} исполнителя {new_file['artist']} для замены.")

@admin_router.callback_query(F.data == "confirm_replacement", StateFilter(AddTrackState.waiting_for_audio))
@admin_only
async def confirm_replacement(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tracks = data.get("tracks", [])
    received_files = data.get("received_files", [])
    skipped_tracks = data.get("skipped_tracks", [])

    if len(received_files) != len(tracks):
        await callback_query.message.reply(
            "⚠️ *Количество отправленных файлов не совпадает с числом выбранных треков, или вы не отправили их вовсе. Также могли быть пропущены файлы не MP3 формата, они не могут быть добавлены в бота.*",
            parse_mode="Markdown",
            reply_markup=cancel_button
        )
        return

    await callback_query.message.edit_text(
        "⏳ *Началась замена треков, ожидайте завершения по отправке нового сообщения ботом.*",
        parse_mode="Markdown"
    )

    try:
        # Подготовка треков для замены
        updated_tracks = []
        for track, new_file in zip(tracks, received_files):
            track.title = new_file["title"]
            track.artist = new_file["artist"]
            track.file_id = new_file["file_id"]
            track.title_lower = new_file["title"].lower()
            track.artist_lower = new_file["artist"].lower()
            updated_tracks.append(track)

        # Разделение на батчи и обновление
        await update_tracks_in_batches(updated_tracks, session, skipped_tracks)

        if skipped_tracks:
            skipped_info = "\n".join([f"{track['title']} (Причина: {track['reason']})" for track in skipped_tracks])
            if len(skipped_info) > MAX_TELEGRAM_MESSAGE_LENGTH - 200:
                skipped_info = skipped_info[:MAX_TELEGRAM_MESSAGE_LENGTH - 200] + "... (список обрезан)"
            message = (f"🤔 <b>Вроде, треки успешно заменены.</b>\n\n"
                       f"⚠️ <b>Какие-то треки были пропущены, так как они либо уже существуют в базе данных, либо не являются MP3:</b>\n"
                       f"{skipped_info}")
        else:
            message = "✅ <b>Все треки успешно заменены.</b>"

        await callback_query.message.reply(
            message,
            parse_mode="HTML",
            reply_markup=back_to_menu_button
        )
        logger.info(f"✅ Успешная попытка замены треков с ID {', '.join(map(str, [t.id for t in updated_tracks]))}.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка при замене треков: {e}")
        await callback_query.message.reply(
            "⚠️ *Произошла ошибка при замене треков.*",
            parse_mode="Markdown",
            reply_markup=back_to_menu_button
        )
    finally:
        await state.clear()

async def update_tracks_in_batches(tracks, session, skipped_tracks, batch_size=10):
    """
    Обновляет треки в базе данных батчами с паузой между обработкой.
    """
    for i in range(0, len(tracks), batch_size):
        batch = tracks[i:i + batch_size]
        try:
            for track in batch:
                try:
                    logger.info(f"👀 Проверяем трек: {track.title}, ID: {track.file_id}.")

                    # Проверяем, существует ли трек с таким же file_id
                    existing_track = await session.execute(select(Track).where(Track.file_id == track.file_id))
                    if existing_track.scalars().first():
                        logger.warning(f"⚠️ Трек с file_id {track.file_id} уже существует. Пропускаем замену.")
                        skipped_tracks.append({"title": track.title, "reason": "уже существует"})
                        continue
                    
                    session.add(track)  # Добавляем изменённый трек в сессию

                except Exception as e:
                    logger.error(f"⚠️ Ошибка при обработке трека {track.title}: {e}")
                    skipped_tracks.append({"title": track.title, "reason": f"ошибка: {e}"})
                    continue

            await session.commit()
            logger.info(f"✅ Успешная попытка замены группы из {len(batch)} треков.")
        except Exception as e:
            logger.error(f"⚠️ Ошибка при замене группы треков: {e}")
            await session.rollback()  # Откатываем изменения в случае ошибки

        if i + batch_size < len(tracks):  # Проверяем, нужно ли делать паузу
            await asyncio.sleep(5.5)  # Устанавливаем паузу в 5.5 секунд
        
@admin_router.callback_query(F.data == "edit_track")
@admin_only
async def edit_track_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может изменять информацию о треках.*", parse_mode="Markdown", reply_markup=back_admin_menu_keyboard)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню изменения информации о треках.")
        return
    
    await state.set_state(AddTrackState.editing_track)
    await callback_query.message.edit_text(
        "🆔 *Введите ID трека для редактирования и новые данные в формате:*\n`ID`\n`Название`\n`Исполнитель`\n\n_ᓚᘏᗢ P. S. Это изменит лишь записи в БД, мета-данные треков останутся прежними! Если хотите заменить метаданные, измените их в самом MP3 файле и замените его в боте. Узнать ID нужного вам трека можно у главного администратора._",
        reply_markup=cancel_button,  # Используем кнопку отмены
        parse_mode="Markdown"
    )
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню редактирования информации о треках.")

@admin_router.message(StateFilter(AddTrackState.editing_track))
async def edit_track(message: Message, session: AsyncSession, state: FSMContext):
    try:
        data = message.text.split("\n")
        track_id = int(data[0])
        new_title = data[1]
        new_artist = data[2]

        track_result = await session.execute(select(Track).where(Track.id == track_id))
        track = track_result.scalars().first()
        if track:
            track.title = new_title
            track.artist = new_artist
            track.title_lower = new_title.lower()
            track.artist_lower = new_artist.lower()
            await session.commit()
            await message.reply("✅ *Трек успешно обновлен.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Пользователь @{message.from_user.username} ({message.from_user.id}) отредактировал данные трека с ID {track_id}.")
            await state.clear()
        else:
            await message.reply("❌ *Трек с таким ID не найден.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался отредактировать данные трека с ID {track_id}, но его нет в моей базе.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка при редактировании трека: {e}")
        await message.reply("⚠️ *Ошибка при редактировании трека. Проверьте введенные данные.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        
@admin_router.callback_query(F.data == "add_admin")
@admin_only
async def add_admin_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может добавлять других администраторов.*", parse_mode="Markdown", reply_markup=back_admin_menu_keyboard)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню добавления администраторов.")
        return
    
    await state.set_state(AddTrackState.adding_admin)
    await callback_query.message.edit_text("🆔 *Введите ID нового администратора.*", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню добавления администраторов.")

@admin_router.message(StateFilter(AddTrackState.adding_admin))
async def add_admin(message: Message, session: AsyncSession, state: FSMContext):
    try:
        new_admin_id = int(message.text)
        new_admin = Admin(telegram_id=new_admin_id)
        session.add(new_admin)
        await session.commit()
        await message.reply("✅ *Администратор успешно добавлен.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) добавил администратора с ID {new_admin_id}.")
        await state.clear()
    except Exception as e:
        logger.error(f"⚠️ Ошибка при добавлении администратора: {e}")
        await message.reply("⚠️ *Ошибка: проверьте правильность введённых данных.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        
@admin_router.callback_query(F.data == "remove_admin")
@admin_only
async def remove_admin_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может разжаловать администраторов.*", parse_mode="Markdown", reply_markup=back_admin_menu_keyboard)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню разжалования администраторов.")
        return
    
    await state.set_state(AddTrackState.removing_admin)
    await callback_query.message.edit_text("🆔 *Введите ID администратора, которого нужно разжаловать.*", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл меню разжалования администраторов.")

@admin_router.message(StateFilter(AddTrackState.removing_admin))
async def remove_admin(message: Message, session: AsyncSession, state: FSMContext):
    try:
        admin_id_to_remove = int(message.text)

        # Проверяем, существует ли администратор с таким ID
        admin_result = await session.execute(select(Admin).where(Admin.telegram_id == admin_id_to_remove))
        admin = admin_result.scalars().first()

        if admin:
            await session.delete(admin)
            await session.commit()
            await message.reply("✅ *Администратор успешно разжалован.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) разжаловал администратора с ID {admin_id_to_remove}.")
        else:
            await message.reply("❌ *Администратор с таким ID не найден.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"❌ Главный администратор @{message.from_user.username} ({message.from_user.id}) пытался разжаловать администратора с ID {admin_id_to_remove}, но его нет в моей базе.")
        
        await state.clear()

    except ValueError:
        await message.reply("⚠️ *Пожалуйста, введите корректный ID администратора.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
    except Exception as e:
        logger.error(f"⚠️ Ошибка при разжаловании администратора: {e}")
        await message.reply("⚠️ *Ошибка при разжаловании администратора. Попробуйте еще раз.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        await state.clear()
        
# Вывод ID профиля и чата
@admin_router.callback_query(F.data == "get_ids")
@admin_only
async def get_ids(callback_query: CallbackQuery, state: FSMContext, session: object):
    logger.info(f"🆔 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню получения ID профиля и чата.")
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    await callback_query.message.edit_text(
        f"👤 <b>ID вашего профиля:</b> <code>{user_id}</code>\n"
        f"💬 <b>ID текущего чата:</b> <code>{chat_id}</code>",
        parse_mode="HTML",
        reply_markup=back_admin_menu_keyboard
    )

# Ожидание любого файла для получения его ID
@admin_router.callback_query(F.data == "get_file_id")
@admin_only
async def wait_for_file(callback_query: CallbackQuery, state: FSMContext, session: object):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может получать ID файлов.*", parse_mode="Markdown", reply_markup=back_admin_menu_keyboard)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню получения ID файлов.")
        return
    
    logger.info(f"📂 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню получения ID файлов.")
    await state.set_state(FileIDState.waiting_for_file)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")],
        ]
    )
    
    await callback_query.message.edit_text(
        "📂 <b>Отправьте один файл (аудио, фото, видео, документ, стикер или другой файл), чтобы получить его ID:</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# Обработка файла и получение его ID
@admin_router.message(StateFilter(FileIDState.waiting_for_file))
async def get_file_id(message: Message, state: FSMContext):
    # Определяем тип файла и его ID
    file_id = None
    file_type = None
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")],
        ]
    )

    if message.audio:
        file_id = message.audio.file_id
        file_type = "🎵 Аудио"
    elif message.photo:
        file_id = message.photo[-1].file_id  # Берем фото самого высокого качества
        file_type = "🖼️ Фото"
    elif message.video:
        file_id = message.video.file_id
        file_type = "🎥 Видео"
    elif message.document:
        file_id = message.document.file_id
        file_type = "📄 Документ"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = "🎙️ Голосовое сообщение"
    elif message.animation:
        file_id = message.animation.file_id
        file_type = "📽️ Анимация"
    elif message.sticker:
        file_id = message.sticker.file_id
        if message.sticker.is_animated:
            file_type = "🖼️ Анимационный стикер"
        elif message.sticker.is_video:
            file_type = "🎥 Видео-стикер"
        else:
            file_type = "📄 Статичный стикер"
    else:
        await message.reply("⚠️ <b>Вы либо не отправили файл, либо этот тип файла не поддерживается. Отправьте корректный файл или отмените действие.</b>", parse_mode="HTML", reply_markup=keyboard)
        return

    # Логгирование информации о запросе
    logger.info(
        f"📂 Пользователь @{message.from_user.username} ({message.from_user.id}) "
        f"получил ID файла. Тип: {file_type}, ID: {file_id}."
    )

    # Сброс состояния
    await state.clear()

    # Ответ с информацией о файле
    await message.reply(
        f"<b>{file_type} ID:</b> <code>{file_id}</code>",
        parse_mode="HTML",
        reply_markup=back_admin_menu_keyboard
    )
